"""
Curated offers — hand-entered leads from the human review (report §7.1).

These come from firms whose postings the automated scrapers cannot read
(direct_link career sites, WTTJ/Workable boards, gated ATS). They are merged
into the pipeline like scraped jobs: scored by the matcher, deduped, and shown
on the dashboard. Update this list when the weekly review surfaces new leads;
remove an entry once its posting closes.

Each entry needs at least: bank, title, location, url. The description text is
used by the matcher, so keep it faithful to the real posting (domain, duration,
start month) — do NOT invent an eligibility level that isn't stated.
"""

CURATED_OFFERS = [
    # ---- PARIS ----
    {
        "bank": "Evercore",
        "category": "Investment Bank",
        "title": "Off-Cycle Internship – Telecoms Team (January–June 2027)",
        "location": "Paris, France",
        "url": "https://evercore.tal.net/vx/lang-en-GB/mobile-0/appcentre-1/brand-6/xf-b317e3c9c730/candidate/so/pm/1/pl/2/opp/3145-Paris-Off-Cycle-Internship-Telecoms-Team-January-June-2027/en-GB",
        "start_date": "2027-01",
        "duration": "6-month off-cycle internship",
        "description": "Off-cycle investment banking internship, Telecoms M&A advisory team, January to June 2027, 6 months. Open to penultimate-year students. Deadline 19/09/2026.",
    },
    {
        "bank": "Alantra",
        "category": "Investment Bank",
        "title": "Stage M&A – Janvier/Mars 2027",
        "location": "Paris, France",
        "url": "https://www.welcometothejungle.com/en/companies/alantra/jobs/stage-m-a-janvier-mars-2027_paris",
        "start_date": "2027-01",
        "duration": "6-month internship",
        "description": "Stage M&A / corporate finance advisory, 6 mois, démarrage janvier ou mars 2027. Ouvert aux étudiants en avant-dernière année.",
    },
    {
        "bank": "Clipperton",
        "category": "Investment Bank",
        "title": "Technology M&A Analyst Internship (January/March 2027)",
        "location": "Paris, France",
        "url": "https://clipperton.workable.com/jobs/5775228",
        "start_date": "2027-01",
        "duration": "6-month internship",
        "description": "Technology M&A advisory internship, 6 months, starting January or March 2027. Open to penultimate-year students pursuing a Bachelor's or Master's.",
    },
    {
        "bank": "Scalene Partners",
        "category": "Investment Bank",
        "title": "Stage Analyste M&A – Janvier 2027",
        "location": "Paris, France",
        "url": "https://www.welcometothejungle.com/fr/companies/scalene-partners/jobs/stage-analyste-m-a-janvier-2027_paris",
        "start_date": "2027-01",
        "duration": "6-month internship",
        "description": "Stage analyste M&A, démarrage 3 janvier 2027, 6 mois. Boutique de conseil en fusions-acquisitions.",
    },
    {
        "bank": "Avolta Partners",
        "category": "Investment Bank",
        "title": "Stage M&A – Levée de fonds (Janvier 2027)",
        "location": "Paris, France",
        "url": "https://www.welcometothejungle.com/fr/companies/avolta-partners/jobs/stage-m-a-levee-de-fonds-janvier-2027_paris",
        "start_date": "2026-12",
        "duration": "6-month internship",
        "description": "Stage M&A et levée de fonds tech, démarrage fin décembre 2026 / janvier 2027, 6 mois.",
    },
    # ---- MADRID ----
    {
        "bank": "Arcano Partners",
        "category": "Investment Bank",
        "title": "Prácticas semestrales Banca de Inversión (Enero–Junio 2027)",
        "location": "Madrid, Spain",
        "url": "https://talento.arcanopartners.com/jobs/7882300-practicas-semestrales-banca-de-inversion-enero-junio-2027",
        "start_date": "2027-01",
        "duration": "6-month internship (enero-junio)",
        "description": "Prácticas semestrales en Banca de Inversión / corporate finance, enero a junio 2027, 6 meses. Abierto a estudiantes de grado (bachelor).",
    },
    # ---- LONDON ----
    {
        "bank": "Lazard",
        "category": "Investment Bank",
        "title": "Financial Advisory Off-Cycle Internship – January 2027 (6 months)",
        "location": "London, United Kingdom",
        "url": "https://www.lazard.com/careers/students/",
        "start_date": "2027-01",
        "duration": "6-month off-cycle internship",
        "description": "Financial advisory (M&A) off-cycle internship, January 2027, 6 months. Open to penultimate-year students.",
    },
    {
        "bank": "UBS",
        "category": "Investment Bank",
        "title": "2027 Off-Cycle Internship – Global Banking",
        "location": "London, United Kingdom",
        "url": "https://jobs.ubs.com/TGnewUI/Search/home/HomeWithPreLoad?partnerid=25008&siteid=5131&PageType=JobDetails&jobid=348155",
        "start_date": "2027-01",
        "duration": "6-month off-cycle internship",
        "description": "Global Banking (investment banking / advisory) off-cycle internship 2027, London. Application window closes 3 August 2026. Open to penultimate-year students.",
    },
    {
        "bank": "UBS",
        "category": "Private Bank",
        "title": "2027 Off-Cycle Internship – Global Wealth Management",
        "location": "London, United Kingdom",
        "url": "https://jobs.ubs.com/TGnewUI/Search/home/HomeWithPreLoad?partnerid=25008&siteid=5131&PageType=JobDetails&jobid=348157",
        "start_date": "2027-01",
        "duration": "6-month off-cycle internship",
        "description": "Global Wealth Management off-cycle internship 2027, London. Closes 3 August 2026. Wealth management / private banking. Open to penultimate-year students.",
    },
]
