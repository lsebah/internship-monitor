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


def scrape_workday(firm: dict, search_terms: list, target_cities: list) -> list:
    """Scrape jobs from Workday API endpoint."""
    cfg = firm["scraper"]
    tenant = cfg["tenant"]
    instance = cfg["instance"]
    site = cfg["site"]
    base_url = f"https://{tenant}.wd{instance}.myworkdayjobs.com"
    api_url = f"{base_url}/wday/cxs/{tenant}/{site}/jobs"

    all_jobs = []
    seen_urls = set()

    for term in search_terms[:5]:  # Limit search terms to avoid rate limiting
        for city in target_cities:
            try:
                payload = {
                    "appliedFacets": {},
                    "limit": 20,
                    "offset": 0,
                    "searchText": f"{term} {city}",
                }
                resp = SESSION.post(api_url, json=payload, timeout=15)
                if resp.status_code != 200:
                    logger.warning(f"Workday {firm['name']}: HTTP {resp.status_code} for '{term} {city}'")
                    continue

                data = resp.json()
                postings = data.get("jobPostings", [])

                city_patterns = [re.compile(re.escape(c), re.I) for c in target_cities]
                intern_rx = re.compile(
                    r"intern(ship)?|stage\b|stagiaire|pr[aá]cticas|becario|trainee|"
                    r"placement|summer analyst|working student|apprentice|"
                    r"graduate programme|off[- ]cycle",
                    re.I,
                )

                for p in postings:
                    ext_path = p.get("externalPath", "")
                    job_url = f"{base_url}/en-US/{site}{ext_path}" if ext_path else ""
                    if job_url in seen_urls:
                        continue
                    seen_urls.add(job_url)

                    # Geography guard: Workday's searchText is fuzzy and returns
                    # global results ("intern Madrid" brings back Manila, Sao Paulo,
                    # etc.). Only keep jobs whose location text mentions a target city.
                    location_text = p.get("locationsText", "") or ""
                    if not any(pat.search(location_text) for pat in city_patterns):
                        continue

                    # Programme guard: only keep intern / stage titles. Workday's
                    # searchText also returns full-time / SVP / Director roles
                    # that just contain the word "intern" somewhere else.
                    title_text = p.get("title", "") or ""
                    if not intern_rx.search(title_text):
                        continue

                    detail = _fetch_workday_detail(base_url, site, tenant, ext_path)
                    time.sleep(0.15)

                    job = {
                        "id": make_job_id(firm["name"], p.get("title", ""), job_url),
                        "bank": firm["name"],
                        "category": firm.get("category", ""),
                        "title": p.get("title", ""),
                        "location": p.get("locationsText", ""),
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

                time.sleep(0.5)  # Rate limiting

            except Exception as e:
                logger.error(f"Workday {firm['name']} error for '{term} {city}': {e}")
                continue

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
        term_patterns = [re.compile(re.escape(t), re.IGNORECASE) for t in search_terms]

        for j in jobs_data:
            title = j.get("title", "")
            location_name = ""
            if j.get("location"):
                location_name = j["location"].get("name", "")

            # Check if location matches
            loc_match = any(p.search(location_name) for p in city_patterns)
            # Check if title matches search terms
            term_match = any(p.search(title) for p in term_patterns)

            if loc_match or term_match:
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
        term_patterns = [re.compile(re.escape(t), re.IGNORECASE) for t in search_terms]

        for p in postings:
            title = p.get("text", "")
            location_name = p.get("categories", {}).get("location", "")

            loc_match = any(pat.search(location_name) for pat in city_patterns)
            term_match = any(pat.search(title) for pat in term_patterns)

            if loc_match or term_match:
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
# DISPATCHER
# ============================================================
SCRAPER_MAP = {
    "workday": scrape_workday,
    "greenhouse": scrape_greenhouse,
    "lever": scrape_lever,
}


def scrape_firm(firm: dict, search_terms: list, target_cities: list) -> list:
    """Dispatch to the appropriate scraper for a firm."""
    scraper_type = firm.get("scraper", {}).get("type", "direct_link")
    scraper_fn = SCRAPER_MAP.get(scraper_type)
    if scraper_fn:
        return scraper_fn(firm, search_terms, target_cities)
    return []
