"""
Internship Monitor - Main scraper orchestrator.
Scrapes career pages, scores matches, and outputs JSON for the dashboard.
"""
import json
import logging
import os
import sys
from datetime import datetime, timezone

from config import FIRMS, SEARCH_TERMS, TARGET_CITIES, LINKEDIN_SEARCHES, INDEED_SEARCHES
from scrapers import scrape_firm
from matcher import score_job, classify_match

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger(__name__)

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "docs", "data", "jobs.json")


def load_existing_data() -> dict:
    """Load existing job data from JSON file."""
    try:
        with open(DATA_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {"last_updated": None, "jobs": [], "scrape_status": {}, "stats": {}}


def save_data(data: dict):
    """Save job data to JSON file."""
    os.makedirs(os.path.dirname(DATA_PATH), exist_ok=True)
    with open(DATA_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    logger.info(f"Saved {len(data['jobs'])} jobs to {DATA_PATH}")


def merge_jobs(existing_jobs: list, new_jobs: list, today: str) -> list:
    """Merge new jobs into existing list, preserving first_seen dates."""
    existing_map = {j["id"]: j for j in existing_jobs}
    merged = {}

    # Keep track of all current job IDs from this scrape
    current_ids = set()

    for job in new_jobs:
        jid = job["id"]
        current_ids.add(jid)

        if jid in existing_map:
            # Job already known - keep first_seen, update rest
            existing = existing_map[jid]
            job["first_seen"] = existing.get("first_seen", today)
            job["is_new"] = False
        else:
            # New job
            job["first_seen"] = today
            job["is_new"] = True

        # Score the job
        match = score_job(job)
        job["match_score"] = match["score"]
        job["match_reasons"] = match["reasons"]
        job["match_class"] = classify_match(match["score"])
        job["excluded"] = match.get("excluded", False)
        job["last_seen"] = today

        merged[jid] = job

    # Retain stale intern/stage jobs up to 14 days after last seen, but purge
    # entries that fail the current intern + geography filters (they were
    # collected before the filters existed).
    import re
    from config import TARGET_CITIES
    intern_rx = re.compile(
        r"\bintern(ship)?\b|\bstage\b|\bstagiaire\b|\bpr[aá]cticas\b|"
        r"\bbecario\b|\btrainee\b|\bplacement\b|\bsummer analyst\b|"
        r"\bworking student\b|\bapprentice\b|\bgraduate programme\b|"
        r"\boff[- ]cycle\b",
        re.I,
    )
    city_rx = re.compile("|".join(re.escape(c) for c in TARGET_CITIES), re.I)

    for jid, job in existing_map.items():
        if jid in merged:
            continue
        title = job.get("title", "") or ""
        location = job.get("location", "") or ""
        if not intern_rx.search(title):
            continue  # purge: not an internship title
        if not city_rx.search(location):
            continue  # purge: outside target cities

        last_seen = job.get("last_seen", today)
        try:
            days_since = (datetime.strptime(today, "%Y-%m-%d") -
                          datetime.strptime(last_seen, "%Y-%m-%d")).days
        except ValueError:
            days_since = 0

        if days_since <= 14:
            job["is_new"] = False
            merged[jid] = job

    return list(merged.values())


def build_direct_links() -> list:
    """Build list of direct career page links for the dashboard."""
    links = []
    for firm in FIRMS:
        link = {
            "name": firm["name"],
            "short": firm.get("short", ""),
            "category": firm.get("category", ""),
            "subcategory": firm.get("subcategory", ""),
            "careers_url": firm.get("careers_url", ""),
            "search_urls": firm.get("search_urls", {}),
            "cities": firm.get("cities", {}),
            "has_scraper": firm.get("scraper", {}).get("type", "direct_link") != "direct_link",
        }
        links.append(link)
    return links


def main():
    logger.info("=" * 60)
    logger.info("INTERNSHIP MONITOR - Starting scrape")
    logger.info("=" * 60)

    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    now_iso = datetime.now(timezone.utc).isoformat()

    # Load existing data
    existing_data = load_existing_data()
    existing_jobs = existing_data.get("jobs", [])

    # Scrape all firms with active scrapers
    all_new_jobs = []
    scrape_status = {}
    firms_scraped = 0

    for firm in FIRMS:
        scraper_type = firm.get("scraper", {}).get("type", "direct_link")
        if scraper_type == "direct_link":
            scrape_status[firm["name"]] = {"status": "link_only", "count": 0}
            continue

        logger.info(f"Scraping {firm['name']} ({scraper_type})...")
        try:
            jobs = scrape_firm(firm, SEARCH_TERMS[:8], TARGET_CITIES)
            all_new_jobs.extend(jobs)
            scrape_status[firm["name"]] = {
                "status": "success",
                "count": len(jobs),
                "timestamp": now_iso,
            }
            firms_scraped += 1
        except Exception as e:
            logger.error(f"Failed to scrape {firm['name']}: {e}")
            scrape_status[firm["name"]] = {
                "status": "error",
                "error": str(e),
                "timestamp": now_iso,
            }

    # Merge with existing data
    merged_jobs = merge_jobs(existing_jobs, all_new_jobs, today)

    # Filter out excluded jobs for display
    display_jobs = [j for j in merged_jobs if not j.get("excluded", False)]

    # Sort by match score (descending), then by date
    display_jobs.sort(key=lambda j: (-j.get("match_score", 0), j.get("posted_date", "")))

    # Calculate stats
    new_today = sum(1 for j in display_jobs if j.get("is_new", False))
    high_match = sum(1 for j in display_jobs if j.get("match_score", 0) >= 60)

    # Build output
    output = {
        "last_updated": now_iso,
        "scrape_status": scrape_status,
        "jobs": display_jobs,
        "direct_links": build_direct_links(),
        "linkedin_searches": LINKEDIN_SEARCHES,
        "indeed_searches": INDEED_SEARCHES,
        "stats": {
            "total_jobs": len(display_jobs),
            "new_today": new_today,
            "high_match": high_match,
            "firms_scraped": firms_scraped,
            "firms_total": len(FIRMS),
        },
    }

    save_data(output)

    logger.info(f"Done! {len(display_jobs)} jobs total, {new_today} new today, {high_match} high match")
    return output


if __name__ == "__main__":
    main()
