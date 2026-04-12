"""
Profile matching engine.
Scores job listings against Charles's profile.
"""
import re
from config import PROFILE, TARGET_CITIES, TARGET_COUNTRIES, DEPARTMENT_KEYWORDS, EXCLUDE_KEYWORDS


def score_job(job: dict) -> dict:
    """Score a job listing against the candidate profile.
    Returns dict with score (0-100) and match reasons."""
    score = 0
    reasons = []
    title = (job.get("title") or "").lower()
    location = (job.get("location") or "").lower()
    description = (job.get("description") or "").lower()
    combined = f"{title} {location} {description}"

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

    # Cap at 100
    score = min(100, score)

    return {
        "score": score,
        "reasons": reasons,
        "excluded": False,
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
