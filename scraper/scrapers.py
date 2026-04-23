"""
Scraper modules for different ATS platforms.
"""
import hashlib
import logging
import re
import time
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
    "Accept": "application/json, text/html, */*",
    "Accept-Language": "en-US,en;q=0.9,fr;q=0.8,es;q=0.7",
}

SESSION = requests.Session()
SESSION.headers.update(HEADERS)


def make_job_id(firm_name: str, title: str, url: str) -> str:
    """Generate a stable unique ID for a job listing."""
    raw = f"{firm_name}|{title}|{url}".lower().strip()
    return hashlib.md5(raw.encode()).hexdigest()[:12]


# ============================================================
# WORKDAY SCRAPER
# ============================================================
DURATION_PATTERNS = [
    re.compile(r"(\d{1,2}\s*[-\u2013]\s*\d{1,2}\s*(?:week|semaine)s?)", re.I),
    re.compile(r"(\d{1,2}\s*(?:week|semaine)s?)", re.I),
    re.compile(r"(\d{1,2}\s*(?:month|mois)s?)", re.I),
    re.compile(r"(summer\s*(?:analyst\s*)?(?:intern(?:ship)?)?\s*(?:programme?|program)?\s*\d{4})", re.I),
    re.compile(r"(off[\s-]?cycle\s*(?:intern(?:ship)?)?\s*(?:h[12]|spring|autumn|fall)?\s*\d{4})", re.I),
    re.compile(r"(\b(?:H[12]|spring|summer|autumn|fall)\s+\d{4}\b)", re.I),
]

REQUIREMENT_KEYWORDS = [
    "requirement", "qualification", "what we are looking for",
    "what you'll need", "what you will need", "skills", "profile",
    "you will bring", "we're looking for", "we are looking for",
    "minimum qualification", "preferred qualification",
]


def _clean_html(html: str) -> str:
    """Strip HTML tags and normalize whitespace."""
    if not html:
        return ""
    text = BeautifulSoup(html, "lxml").get_text(separator="\n", strip=True)
    return re.sub(r"\n{3,}", "\n\n", text)


def _extract_duration(text: str) -> str:
    """Try to extract internship duration from the description."""
    if not text:
        return ""
    for pat in DURATION_PATTERNS:
        m = pat.search(text)
        if m:
            return m.group(1).strip()
    return ""


def _extract_requirements(text: str, max_items: int = 6, max_chars: int = 600) -> str:
    """Extract a short list of requirements from the description."""
    if not text:
        return ""
    lines = [ln.strip() for ln in text.split("\n") if ln.strip()]
    start = -1
    for i, ln in enumerate(lines):
        low = ln.lower()
        if any(kw in low for kw in REQUIREMENT_KEYWORDS) and len(ln) < 120:
            start = i + 1
            break
    if start < 0:
        return ""
    items = []
    for ln in lines[start : start + 25]:
        # Stop when we hit another section header
        low = ln.lower()
        if any(h in low for h in ["benefit", "about us", "our commitment", "diversity", "equal opportunity", "apply", "responsibilities"]):
            break
        if len(ln) < 8 or len(ln) > 220:
            continue
        items.append(ln.lstrip("\u2022*-\u2013 ").strip())
        if len(items) >= max_items:
            break
    joined = "\n".join(items)
    return joined[:max_chars]


def _fetch_workday_detail(base_url: str, site: str, tenant: str, external_path: str, timeout: int = 12) -> dict:
    """Fetch job detail from Workday CXS API to get start date, time type, description."""
    if not external_path:
        return {}
    detail_url = f"{base_url}/wday/cxs/{tenant}/{site}{external_path}"
    try:
        r = SESSION.get(detail_url, timeout=timeout, headers={"Accept": "application/json"})
        if r.status_code != 200:
            return {}
        info = r.json().get("jobPostingInfo", {})
        desc_html = info.get("jobDescription", "") or ""
        desc_text = _clean_html(desc_html)
        return {
            "start_date": info.get("startDate", "") or "",
            "time_type": info.get("timeType", "") or "",
            "description_text": desc_text,
            "duration": _extract_duration(desc_text),
            "requirements": _extract_requirements(desc_text),
        }
    except Exception as e:
        logger.debug(f"Workday detail fetch failed for {external_path}: {e}")
        return {}


WORKDAY_INTERN_RX = re.compile(
    r"\bintern(ship)?\b|\bstage\b|\bstagiaire\b|\bpr[aá]cticas\b|"
    r"\bbecario\b|\btrainee\b|\bplacement\b|\bsummer analyst\b|"
    r"\bsummer associate\b|\bworking student\b|\bapprentice\b|"
    r"\bgraduate programme?\b|\bgraduate analyst\b|\banalyst programme?\b|"
    r"\brotational programme?\b|\bearly career\b|\boff[- ]cycle\b",
    re.I,
)


def scrape_workday(firm: dict, search_terms: list, target_cities: list) -> list:
    """Scrape jobs from Workday API endpoint.

    Strategy: for each search term, paginate across all matching results
    (no city in the query — cities are filtered locally against
    locationsText, because embedding city in searchText drops many
    valid postings that list the city only in structured facets).
    """
    cfg = firm["scraper"]
    tenant = cfg["tenant"]
    instance = cfg["instance"]
    site = cfg["site"]
    base_url = f"https://{tenant}.wd{instance}.myworkdayjobs.com"
    api_url = f"{base_url}/wday/cxs/{tenant}/{site}/jobs"

    all_jobs = []
    seen_urls = set()
    city_patterns = [re.compile(re.escape(c), re.I) for c in target_cities]
    page_size = 20
    max_pages = 10  # safety cap: 200 postings per term

    for term in search_terms:
        offset = 0
        pages = 0
        while pages < max_pages:
            try:
                payload = {
                    "appliedFacets": {},
                    "limit": page_size,
                    "offset": offset,
                    "searchText": term,
                }
                resp = SESSION.post(api_url, json=payload, timeout=15)
                if resp.status_code != 200:
                    logger.warning(
                        f"Workday {firm['name']}: HTTP {resp.status_code} "
                        f"for '{term}' offset={offset}"
                    )
                    break

                data = resp.json()
                postings = data.get("jobPostings", [])
                total = data.get("total", 0)
                if not postings:
                    break

                for p in postings:
                    ext_path = p.get("externalPath", "")
                    job_url = f"{base_url}/en-US/{site}{ext_path}" if ext_path else ""
                    if not job_url or job_url in seen_urls:
                        continue
                    seen_urls.add(job_url)

                    location_text = p.get("locationsText", "") or ""
                    if not any(pat.search(location_text) for pat in city_patterns):
                        continue

                    title_text = p.get("title", "") or ""
                    if not WORKDAY_INTERN_RX.search(title_text):
                        continue

                    detail = _fetch_workday_detail(base_url, site, tenant, ext_path)
                    time.sleep(0.1)

                    job = {
                        "id": make_job_id(firm["name"], title_text, job_url),
                        "bank": firm["name"],
                        "category": firm.get("category", ""),
                        "title": title_text,
                        "location": location_text,
                        "url": job_url,
                        "posted_date": p.get("postedOn", ""),
                        "description": " | ".join(p.get("bulletFields", [])),
                        "start_date": detail.get("start_date", ""),
                        "time_type": detail.get("time_type", ""),
                        "duration": detail.get("duration", ""),
                        "requirements": detail.get("requirements", ""),
                        "source": "workday",
                    }
                    all_jobs.append(job)

                offset += page_size
                pages += 1
                if offset >= total:
                    break
                time.sleep(0.3)
            except Exception as e:
                logger.error(
                    f"Workday {firm['name']} error for '{term}' offset={offset}: {e}"
                )
                break

    logger.info(f"Workday {firm['name']}: found {len(all_jobs)} jobs")
    return all_jobs


# ============================================================
# GREENHOUSE SCRAPER
# ============================================================
def scrape_greenhouse(firm: dict, search_terms: list, target_cities: list) -> list:
    """Scrape jobs from Greenhouse API."""
    cfg = firm["scraper"]
    board = cfg.get("board", "")
    if not board:
        return []

    api_url = f"https://boards-api.greenhouse.io/v1/boards/{board}/jobs"
    all_jobs = []

    try:
        resp = SESSION.get(api_url, timeout=15)
        if resp.status_code != 200:
            logger.warning(f"Greenhouse {firm['name']}: HTTP {resp.status_code}")
            return []

        data = resp.json()
        jobs_data = data.get("jobs", [])

        city_patterns = [re.compile(re.escape(c), re.IGNORECASE) for c in target_cities]

        for j in jobs_data:
            title = j.get("title", "")
            location_name = ""
            if j.get("location"):
                location_name = j["location"].get("name", "")

            # Require an intern/graduate-style title (filters out senior roles
            # that would slip through on a city match alone).
            if not WORKDAY_INTERN_RX.search(title):
                continue

            # Require a target city in the location text. If location is blank
            # or global ("Remote", "Worldwide"), accept — some firms skip the
            # city field but the title still signals a target geography.
            loc_lower = location_name.lower()
            is_global = (not location_name
                         or loc_lower in ("remote", "worldwide", "global", "europe"))
            if not is_global and not any(p.search(location_name) for p in city_patterns):
                continue

            job_url = j.get("absolute_url", "")
            job = {
                "id": make_job_id(firm["name"], title, job_url),
                "bank": firm["name"],
                "category": firm.get("category", ""),
                "title": title,
                "location": location_name,
                "url": job_url,
                "posted_date": (j.get("updated_at") or "")[:10],
                "description": "",
                "source": "greenhouse",
            }
            all_jobs.append(job)

    except Exception as e:
        logger.error(f"Greenhouse {firm['name']} error: {e}")

    logger.info(f"Greenhouse {firm['name']}: found {len(all_jobs)} jobs")
    return all_jobs


# ============================================================
# LEVER SCRAPER
# ============================================================
def scrape_lever(firm: dict, search_terms: list, target_cities: list) -> list:
    """Scrape jobs from Lever API."""
    cfg = firm["scraper"]
    company = cfg.get("company", "")
    if not company:
        return []

    api_url = f"https://api.lever.co/v0/postings/{company}"
    all_jobs = []

    try:
        resp = SESSION.get(api_url, timeout=15)
        if resp.status_code != 200:
            logger.warning(f"Lever {firm['name']}: HTTP {resp.status_code}")
            return []

        postings = resp.json()
        city_patterns = [re.compile(re.escape(c), re.IGNORECASE) for c in target_cities]

        for p in postings:
            title = p.get("text", "")
            location_name = p.get("categories", {}).get("location", "") or ""

            if not WORKDAY_INTERN_RX.search(title):
                continue

            loc_lower = location_name.lower()
            is_global = (not location_name
                         or loc_lower in ("remote", "worldwide", "global", "europe"))
            if not is_global and not any(pat.search(location_name) for pat in city_patterns):
                continue

            job_url = p.get("hostedUrl", "")
            job = {
                "id": make_job_id(firm["name"], title, job_url),
                "bank": firm["name"],
                "category": firm.get("category", ""),
                "title": title,
                "location": location_name,
                "url": job_url,
                "posted_date": "",
                "description": p.get("descriptionPlain", "")[:200],
                "source": "lever",
            }
            all_jobs.append(job)

    except Exception as e:
        logger.error(f"Lever {firm['name']} error: {e}")

    logger.info(f"Lever {firm['name']}: found {len(all_jobs)} jobs")
    return all_jobs


# ============================================================
# ORACLE HCM SCRAPER (Oracle Recruiting Cloud)
# ============================================================
def scrape_oracle_hcm(firm: dict, search_terms: list, target_cities: list) -> list:
    """Scrape jobs from Oracle HCM Cloud (Oracle Recruiting Cloud)."""
    cfg = firm["scraper"]
    domain = cfg.get("domain", "")
    site_number = cfg.get("site_number", "")
    job_url_template = cfg.get("job_url_template", "")
    if not domain or not site_number:
        logger.warning(f"Oracle HCM {firm['name']}: missing domain or site_number")
        return []

    api_url = f"https://{domain}/hcmRestApi/resources/latest/recruitingCEJobRequisitions"
    all_jobs = []
    seen_ids = set()
    city_patterns = [re.compile(re.escape(c), re.I) for c in target_cities]
    page_size = 50
    max_pages = 4  # 200 per term

    for term in search_terms:
        offset = 0
        pages = 0
        while pages < max_pages:
            finder = (
                f"findReqs;siteNumber={site_number},"
                f"facetsList=LOCATIONS%7CTITLE%7CCATEGORIES%7CPOSTING_DATES,"
                f"limit={page_size},offset={offset},keyword={term},"
                f"sortBy=POSTING_DATES_DESC"
            )
            params = {
                "onlyData": "true",
                "expand": "requisitionList.secondaryLocations",
                "finder": finder,
            }
            try:
                resp = SESSION.get(api_url, params=params, timeout=15,
                                   headers={"Accept": "application/json"})
                if resp.status_code != 200:
                    logger.warning(
                        f"Oracle HCM {firm['name']}: HTTP {resp.status_code} "
                        f"for '{term}' offset={offset}"
                    )
                    break
                data = resp.json()
                items = data.get("items", [])
                if not items:
                    break
                reqs = items[0].get("requisitionList", [])
                if not reqs:
                    break

                for r in reqs:
                    rid = str(r.get("Id", ""))
                    if not rid or rid in seen_ids:
                        continue
                    seen_ids.add(rid)

                    title = r.get("Title", "") or ""
                    primary_loc = r.get("PrimaryLocation", "") or ""
                    secondary_locs = r.get("secondaryLocations", []) or []
                    all_locs_text = primary_loc + " | " + " | ".join(
                        s.get("Name", "") for s in secondary_locs if isinstance(s, dict)
                    )

                    if not any(p.search(all_locs_text) for p in city_patterns):
                        continue
                    if not WORKDAY_INTERN_RX.search(title):
                        continue

                    job_url = (job_url_template.format(id=rid)
                               if job_url_template
                               else f"https://{domain}/hcmUI/CandidateExperience/en/sites/{site_number}/job/{rid}")

                    job = {
                        "id": make_job_id(firm["name"], title, job_url),
                        "bank": firm["name"],
                        "category": firm.get("category", ""),
                        "title": title,
                        "location": all_locs_text.strip(" |"),
                        "url": job_url,
                        "posted_date": (r.get("PostedDate") or "")[:10],
                        "description": r.get("ShortDescriptionStr", "") or "",
                        "start_date": "",
                        "time_type": r.get("JobSchedule", "") or "",
                        "duration": "",
                        "requirements": "",
                        "source": "oracle_hcm",
                    }
                    all_jobs.append(job)

                offset += page_size
                pages += 1
                if len(reqs) < page_size:
                    break
                time.sleep(0.3)
            except Exception as e:
                logger.error(
                    f"Oracle HCM {firm['name']} error for '{term}' offset={offset}: {e}"
                )
                break

    logger.info(f"Oracle HCM {firm['name']}: found {len(all_jobs)} jobs")
    return all_jobs


# ============================================================
# DISPATCHER
# ============================================================
SCRAPER_MAP = {
    "workday": scrape_workday,
    "greenhouse": scrape_greenhouse,
    "lever": scrape_lever,
    "oracle_hcm": scrape_oracle_hcm,
}


class UnsupportedScraperError(Exception):
    """Raised when a firm's scraper type has no implementation."""


def scrape_firm(firm: dict, search_terms: list, target_cities: list) -> list:
    """Dispatch to the appropriate scraper for a firm."""
    scraper_type = firm.get("scraper", {}).get("type", "direct_link")
    if scraper_type == "direct_link":
        return []
    scraper_fn = SCRAPER_MAP.get(scraper_type)
    if scraper_fn is None:
        raise UnsupportedScraperError(
            f"No scraper implementation for type '{scraper_type}' "
            f"(firm: {firm.get('name','?')})"
        )
    return scraper_fn(firm, search_terms, target_cities)
