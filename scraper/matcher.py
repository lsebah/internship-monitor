"""
Profile matching engine.
Scores job listings against Charles's profile.
"""
import re
from config import (
    PROFILE, TARGET_CITIES, TARGET_COUNTRIES, DEPARTMENT_KEYWORDS, EXCLUDE_KEYWORDS,
    DURATION_KEYWORDS, START_2027_KEYWORDS,
)

# Role demands a degree Charles does not yet hold. He is in the penultimate
# year (3rd of 4) of a BBA — NOT graduated and NOT a Master's student — so a
# posting requiring a *completed* Bachelor's, any Master's/MBA/PhD, or final-
# year/recent-graduate status is a hard eligibility mismatch, no matter how well
# the domain/location match. Without this, roles like Ardian's "completed
# Bachelor's or advanced Master's degree" internship scored 95%.
LEVEL_TOO_HIGH_RX = re.compile(
    r"completed\s+bachelor|completed\s+(?:undergraduate\s+)?degree|"
    r"advanced\s+master|master'?s?\s+degree|master'?s?\s+student|"
    r"graduate\s+degree|postgraduate|\bmba\b|\bph\.?\s?d\b|"
    r"final[\s-]year|graduating\s+(?:in|student|this)|recent\s+graduate|"
    r"recently\s+graduated|last\s+year\s+of\s+(?:your\s+)?(?:master|studies)",
    re.I,
)
# Counter-signals: the posting explicitly welcomes penultimate/undergrad
# students, OR welcomes bachelor's AND master's alike (i.e. not master-only).
# When present, the "too high" flag is suppressed — avoids penalising a role
# that says "pursuing a Bachelor's or Master's" or "Bachelor's/Master's students".
LEVEL_OK_RX = re.compile(
    r"penultimate|second[\s-]year|third[\s-]year|2nd[\s-]year|3rd[\s-]year|"
    r"undergraduate|bachelor\s+student|currently\s+(?:studying|enrolled|pursuing)|"
    r"pursuing\s+(?:a\s+)?bachelor|"
    r"bachelor'?s?\s+(?:degree\s+)?(?:and|or|/|&)\s+(?:a\s+)?master|"
    r"all\s+years|any\s+year|all\s+disciplines",
    re.I,
)


def score_job(job: dict) -> dict:
    """Score a job listing against the candidate profile.
    Returns dict with score (0-100) and match reasons."""
    score = 0
    reasons = []
    title = (job.get("title") or "").lower()
    location = (job.get("location") or "").lower()
    description = (job.get("description") or "").lower()
    duration = (job.get("duration") or "").lower()
    requirements = (job.get("requirements") or "").lower()
    start_date = (job.get("start_date") or "").lower()
    combined = f"{title} {location} {description} {duration} {requirements} {start_date}"

    # --- Exclusion check ---
    for kw in EXCLUDE_KEYWORDS:
        if kw.lower() in title:
            return {"score": 0, "reasons": [f"Excluded: '{kw}' in title"], "excluded": True}

    # --- Location match (0-30 points) ---
    city_match = None
    for city in TARGET_CITIES:
        if city.lower() in location:
            city_match = city
            break
    if city_match:
        if city_match.lower() in ["madrid"]:
            score += 30
            reasons.append(f"Location: {city_match} (preferred)")
        else:
            score += 25
            reasons.append(f"Location: {city_match}")
    else:
        for country in TARGET_COUNTRIES:
            if country.lower() in location:
                score += 15
                reasons.append(f"Country: {country}")
                break

    # --- Job type match (0-20 points) ---
    intern_keywords = ["intern", "internship", "stage", "stagiaire", "prácticas",
                       "practicas", "becario", "summer analyst", "trainee"]
    for kw in intern_keywords:
        if kw in combined:
            score += 20
            reasons.append("Type: Internship/Stage")
            break

    # --- Department/domain match (0-25 points) ---
    dept_matches = []
    for kw in DEPARTMENT_KEYWORDS:
        if kw.lower() in combined and kw not in dept_matches:
            dept_matches.append(kw)
    if dept_matches:
        dept_score = min(25, len(dept_matches) * 5)
        score += dept_score
        top_depts = dept_matches[:3]
        reasons.append(f"Domain: {', '.join(top_depts)}")

    # --- Language match (0-15 points) ---
    lang_matches = []
    for lang in PROFILE["languages"]:
        if lang.lower() in combined:
            lang_matches.append(lang)
    if lang_matches:
        score += min(15, len(lang_matches) * 5)
        reasons.append(f"Languages: {', '.join(lang_matches)}")

    # --- Education level match (0-10 points) ---
    edu_keywords = ["undergraduate", "bachelor", "bba", "penultimate",
                    "second year", "2nd year", "university student"]
    for kw in edu_keywords:
        if kw in combined:
            score += 10
            reasons.append("Level: Undergraduate")
            break

    # --- Duration match (0-15 points): target is 6-month / off-cycle ---
    for kw in DURATION_KEYWORDS:
        if kw in combined:
            score += 15
            reasons.append("Duration: 6-month / off-cycle")
            break

    # --- Start date match (0-15 points): target is January 2027 ---
    for kw in START_2027_KEYWORDS:
        if kw in combined:
            score += 15
            reasons.append("Start: Jan 2027")
            break
    # Also accept start_date field if it lands in Jan 2027
    if start_date.startswith("2027-01") and "Start: Jan 2027" not in reasons:
        score += 15
        reasons.append("Start: Jan 2027 (field)")

    # --- CIB / Markets strong signals (0-10 points, stacked with domain) ---
    # "structuring" / "structured products" is Charles's single most
    # differentiating keyword (his CMF experience) — it was previously unscored.
    # Markets in the broad sense — structuring is ONE flavour, not the only one.
    # Equities, FICC, rates, FX, commodities and brokerage all count equally.
    cib_keywords = ["cib", "corporate & investment", "markets",
                    "s&t", "sales and trading", "sales & trading",
                    "equities", "cash equities", "equity derivatives",
                    "fixed income", "ficc", "rates", "credit trading",
                    "fx", "foreign exchange", "commodities", "flow",
                    "derivatives", "brokerage", "execution", "market making",
                    "structuring", "structured product", "structured solutions",
                    "structured note", "structured finance"]
    for kw in cib_keywords:
        if kw in combined:
            score += 10
            reasons.append("Markets (Equities / FICC / Structuration)")
            break

    # --- Preferred track (0-10): corporate finance / banking / IBD ---
    # Charles has a very junior profile; the goal is a corporate-finance /
    # banking / advisory role. Markets stay scored (accessible fallback), but
    # a genuine banking/corporate role gets a tilt so it ranks above an
    # equal-fit markets role.
    preferred_track = ["investment banking", "m&a", "mergers", "corporate finance",
                       "corporate banking", "advisory", "coverage",
                       "leveraged finance", "debt advisory", "restructuring"]
    for kw in preferred_track:
        if kw in combined:
            score += 10
            reasons.append("Track privilégié: Corporate / Banking")
            break

    # --- Education-level eligibility (hard mismatch penalty) ---
    # A role requiring a completed degree / Master's / final-year status is not
    # open to a penultimate-year BBA student. Heavily penalise so it cannot sit
    # in the high-match band, and flag it so the dashboard can hide it.
    level_mismatch = bool(LEVEL_TOO_HIGH_RX.search(combined)) and not LEVEL_OK_RX.search(combined)
    if level_mismatch:
        score = max(0, score - 45)
        reasons.append("⚠ Niveau requis: diplôme complété / Master")

    # Cap at 100
    score = min(100, score)

    return {
        "score": score,
        "reasons": reasons,
        "excluded": False,
        "level_mismatch": level_mismatch,
    }


def classify_match(score: int) -> str:
    """Classify match quality."""
    if score >= 80:
        return "excellent"
    elif score >= 60:
        return "good"
    elif score >= 40:
        return "moderate"
    elif score >= 20:
        return "low"
    return "minimal"
