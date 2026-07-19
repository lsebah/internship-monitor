"""
Internship Monitor - Configuration
All firm configurations, search parameters, and candidate profile.
"""

# ============================================================
# CANDIDATE PROFILE (Charles Sebah)
# ============================================================
PROFILE = {
    "name": "Charles Sebah",
    "school": "IE University (Instituto de Empresa)",
    "degree": "BBA",
    "year": 2,
    "graduation_year": 2027,
    "languages": ["French", "English", "Spanish"],
    "skills": [
        "quantitative analysis", "statistics", "statistical modelling",
        "data analysis", "python", "financial accounting",
        "microsoft 365", "excel",
    ],
    "interests": [
        "finance", "private banking", "wealth management",
        "asset management", "investment banking", "capital markets",
        "corporate banking", "M&A", "risk management",
        "trading", "sales & trading", "financial markets",
    ],
    "linkedin": "https://www.linkedin.com/in/charlesdsebah",
    # Target programme: 6-month internship starting January 2027 in Finance / CIB / Markets
    "target_duration_months": 6,
    "target_start_date": "2027-01",
}

# Keywords that signal a 6-month / long-format programme (off-cycle H1/H2).
DURATION_KEYWORDS = [
    "6 month", "6-month", "six month", "six-month",
    "6 mois", "6-mois", "six mois",
    "6 meses", "seis meses",
    "off-cycle", "off cycle",
    "spring internship", "h1 internship", "h1 2027",
]

# Keywords that signal a January/H1 2027 start.
START_2027_KEYWORDS = [
    "january 2027", "jan 2027", "janvier 2027", "enero 2027",
    "h1 2027", "spring 2027", "winter 2027",
    "2027 spring", "2027 h1",
]

# ============================================================
# SEARCH CONFIGURATION
# ============================================================
TARGET_CITIES = ["Madrid", "Paris", "London", "Londres", "París"]
TARGET_COUNTRIES = ["Spain", "España", "France", "United Kingdom", "UK", "England"]

SEARCH_TERMS = [
    "intern", "internship", "stage", "stagiaire",
    "prácticas", "practicas", "becario", "beca",
    "summer analyst", "summer associate",
    "working student", "graduate", "junior",
    "off-cycle", "off cycle",
    "placement", "trainee",
]

DEPARTMENT_KEYWORDS = [
    "finance", "banking", "wealth management", "private banking",
    "asset management", "investment banking", "M&A",
    "capital markets", "corporate banking", "risk",
    "trading", "sales", "equity", "fixed income",
    "advisory", "restructuring", "leveraged finance",
    "private equity", "venture capital", "portfolio",
    "fund", "compliance", "audit", "strategy",
    "corporate finance", "financial analysis",
    "research", "economics",
]

EXCLUDE_KEYWORDS = [
    "senior", "VP", "vice president", "director", "managing director",
    "experienced hire", "5+ years", "7+ years", "10+ years",
    "head of", "chief", "lead engineer", "senior developer",
    "IT infrastructure", "facilities",
]

# ============================================================
# FIRM CONFIGURATIONS
# ============================================================
# Each firm has:
#   name, short, category, subcategory,
#   careers_url (main careers page),
#   search_urls (pre-filtered for internships in target cities),
#   scraper (type + config for automated scraping),
#   cities (known offices in target cities)

FIRMS = [
    # ==========================================================
    # US INVESTMENT BANKS
    # ==========================================================
    {
        "name": "JP Morgan",
        "short": "JPM",
        "category": "Investment Bank",
        "subcategory": "US Bulge Bracket",
        "careers_url": "https://careers.jpmorgan.com/",
        "search_urls": {
            "internships": "https://careers.jpmorgan.com/us/en/students/programs",
            "Madrid": "https://jpmc.fa.oraclecloud.com/hcmRestApi/resources/latest/recruitingCEJobRequisitions?onlyData=true&expand=requisitionList.secondaryLocations&finder=findReqs;siteNumber=CX_1001,facetsList=LOCATIONS%7CWORK_LOCATION%7CWORKPLACE_TYPE%7CTITLE%7CCATEGORIES%7CORGANIZATIONS%7CPOSTING_DATES%7CFLEX_FIELDS,limit=25,keyword=intern,locationId=300000000289498,sortBy=POSTING_DATES_DESC",
        },
        "scraper": {
            "type": "oracle_hcm",
            "domain": "jpmc.fa.oraclecloud.com",
            "site_number": "CX_1001",
            "job_url_template": "https://jpmc.fa.oraclecloud.com/hcmUI/CandidateExperience/en/sites/CX_1001/job/{id}",
        },
        "cities": {"Madrid": True, "Paris": True, "London": True},
    },
    {
        "name": "Goldman Sachs",
        "short": "GS",
        "category": "Investment Bank",
        "subcategory": "US Bulge Bracket",
        "careers_url": "https://www.goldmansachs.com/careers/",
        "search_urls": {
            "students": "https://higher.gs.com/roles/students",
        },
        "scraper": {
            "type": "oracle_hcm",
            "domain": "hdpc.fa.us2.oraclecloud.com",
            "site_number": "CampusHiring",
            "job_url_template": "https://hdpc.fa.us2.oraclecloud.com/hcmUI/CandidateExperience/en/sites/CampusHiring/job/{id}",
        },
        "cities": {"Madrid": True, "Paris": True, "London": True},
    },
    {
        "name": "Morgan Stanley",
        "short": "MS",
        "category": "Investment Bank",
        "subcategory": "US Bulge Bracket",
        "careers_url": "https://www.morganstanley.com/careers/",
        "search_urls": {
            "students": "https://morganstanley.tal.net/vx/lang-en-GB/mobile-0/brand-2/xf-53515a97a3a0/candidate/jobboard/vacancy/1/adv",
        },
        "scraper": {
            "type": "oleeo",
            "list_url": "https://morganstanley.tal.net/vx/lang-en-GB/mobile-0/brand-2/xf-53515a97a3a0/candidate/jobboard/vacancy/1/adv",
            "base": "https://morganstanley.tal.net",
        },
        "cities": {"Madrid": True, "Paris": True, "London": True},
    },
    {
        "name": "Citi",
        "short": "CITI",
        "category": "Investment Bank",
        "subcategory": "US Bulge Bracket",
        "careers_url": "https://jobs.citi.com/",
        "search_urls": {
            "students": "https://jobs.citi.com/search-jobs/intern",
        },
        "scraper": {
            "type": "workday",
            "tenant": "citi",
            "instance": 5,
            "site": "2",
        },
        "cities": {"Madrid": True, "Paris": True, "London": True},
    },
    {
        "name": "Bank of America",
        "short": "BofA",
        "category": "Investment Bank",
        "subcategory": "US Bulge Bracket",
        "careers_url": "https://campus.bankofamerica.com/",
        "search_urls": {
            "campus": "https://bankcampuscareers.tal.net/",
        },
        "scraper": {
            "type": "oleeo",
            "feed_url": "https://bankcampuscareers.tal.net/vx/mobile-0/appcentre-1/brand-1/candidate/jobboard/vacancy/1/feed",
            "base": "https://bankcampuscareers.tal.net",
        },
        "cities": {"Madrid": False, "Paris": True, "London": True},
    },
    {
        "name": "Wells Fargo",
        "short": "WF",
        "category": "Investment Bank",
        "subcategory": "US Universal",
        "careers_url": "https://www.wellsfargojobs.com/",
        "search_urls": {
            "internships": "https://www.wellsfargojobs.com/en/jobs/?search=intern&country=United+Kingdom&country=Spain&country=France",
        },
        "scraper": {
            "type": "workday",
            "tenant": "wf",
            "instance": 1,
            "site": "WellsFargoJobs",
        },
        "cities": {"Madrid": False, "Paris": False, "London": True},
    },

    # ==========================================================
    # EUROPEAN INVESTMENT BANKS
    # ==========================================================
    {
        "name": "Deutsche Bank",
        "short": "DB",
        "category": "Investment Bank",
        "subcategory": "EU Universal",
        "careers_url": "https://careers.db.com/",
        "search_urls": {
            "internships": "https://careers.db.com/students-graduates/",
            "search": "https://db.wd3.myworkdayjobs.com/en-US/DBWebsite",
        },
        "scraper": {
            "type": "workday",
            "tenant": "db",
            "instance": 3,
            "site": "DBWebsite",
        },
        "cities": {"Madrid": True, "Paris": True, "London": True},
    },
    {
        "name": "Barclays",
        "short": "BARC",
        "category": "Investment Bank",
        "subcategory": "UK Universal",
        "careers_url": "https://search.jobs.barclays/",
        "search_urls": {
            "early_careers": "https://search.jobs.barclays/search-jobs/intern",
        },
        "scraper": {
            "type": "workday",
            "tenant": "barclays",
            "instance": 3,
            "site": "External_Career_Site_Barclays",
        },
        "cities": {"Madrid": False, "Paris": True, "London": True},
    },
    {
        "name": "HSBC",
        "short": "HSBC",
        "category": "Investment Bank",
        "subcategory": "UK Universal",
        "careers_url": "https://www.hsbc.com/careers/students-and-graduates/find-a-programme?programme-type=internship-programme",
        "search_urls": {
            "students": "https://www.hsbc.com/careers/students-and-graduates/find-a-programme?programme-type=internship-programme",
        },
        "scraper": {"type": "direct_link"},
        "cities": {"Madrid": True, "Paris": True, "London": True},
    },
    {
        "name": "UBS",
        "short": "UBS",
        "category": "Investment Bank",
        "subcategory": "Swiss Universal",
        "careers_url": "https://www.ubs.com/global/en/careers.html",
        "search_urls": {
            "internships": "https://jobs.ubs.com/TGnewUI/Search/Home/Home?partnerid=25008&siteid=5131#keyWordSearch=intern&locationSearch=",
        },
        "scraper": {"type": "direct_link"},
        "cities": {"Madrid": True, "Paris": True, "London": True},
    },
    {
        "name": "BNP Paribas",
        "short": "BNPP",
        "category": "Investment Bank",
        "subcategory": "EU Universal",
        "careers_url": "https://group.bnpparibas/en/careers",
        "search_urls": {
            "early_careers": "https://group.bnpparibas/en/careers/job-offers?type=internship",
        },
        "scraper": {"type": "direct_link"},
        "cities": {"Madrid": True, "Paris": True, "London": True},
    },
    {
        "name": "Societe Generale",
        "short": "SG",
        "category": "Investment Bank",
        "subcategory": "EU Universal",
        "careers_url": "https://careers.societegenerale.com/",
        "search_urls": {
            "internships": "https://careers.societegenerale.com/en/job-offers?contract=internship",
        },
        "scraper": {"type": "direct_link"},
        "cities": {"Madrid": True, "Paris": True, "London": True},
    },
    {
        "name": "Credit Agricole CIB",
        "short": "CACIB",
        "category": "Investment Bank",
        "subcategory": "EU CIB",
        "careers_url": "https://groupecreditagricole.jobs/fr/nos-offres/contrats/579/localisations/74-79/",
        "search_urls": {
            "internships": "https://groupecreditagricole.jobs/fr/nos-offres/contrats/579/localisations/74-79/",
        },
        "scraper": {"type": "direct_link"},
        "cities": {"Madrid": True, "Paris": True, "London": True},
    },
    {
        "name": "Natixis",
        "short": "NAT",
        "category": "Investment Bank",
        "subcategory": "EU CIB",
        "careers_url": "https://www.natixis.com/natixis/jcms/tki_5046/en/careers",
        "search_urls": {},
        "scraper": {"type": "direct_link"},
        "cities": {"Madrid": True, "Paris": True, "London": True},
    },
    {
        "name": "Rothschild & Co",
        "short": "ROTH",
        "category": "Investment Bank",
        "subcategory": "EU Advisory",
        "careers_url": "https://www.rothschildandco.com/en/careers/",
        "search_urls": {
            "early_careers": "https://www.rothschildandco.com/en/careers/students-and-graduates/",
        },
        "scraper": {
            "type": "workday",
            "tenant": "rothschildandco",
            "instance": 3,
            "site": "RothschildAndCo_Lateral",
        },
        "cities": {"Madrid": True, "Paris": True, "London": True},
    },
    {
        "name": "Lazard",
        "short": "LAZ",
        "category": "Investment Bank",
        "subcategory": "Advisory",
        "careers_url": "https://www.lazard.com/careers/",
        "search_urls": {
            "early_careers": "https://lazard-careers.tal.net/vx/lang-en-GB/mobile-0/brand-4/xf-a4bba4c3553c/candidate/jobboard/vacancy/2/adv",
        },
        "scraper": {
            "type": "oleeo",
            "feed_url": "https://lazard-careers.tal.net/vx/mobile-0/appcentre-1/brand-4/candidate/jobboard/vacancy/2/feed",
            "list_url": "https://lazard-careers.tal.net/vx/lang-en-GB/mobile-0/brand-4/xf-a4bba4c3553c/candidate/jobboard/vacancy/2/adv",
            "base": "https://lazard-careers.tal.net",
        },
        "cities": {"Madrid": True, "Paris": True, "London": True},
    },

    # ==========================================================
    # SPANISH BANKS
    # ==========================================================
    {
        "name": "BBVA",
        "short": "BBVA",
        "category": "Bank",
        "subcategory": "Spanish Universal",
        "careers_url": "https://www.bbva.com/en/specials/careers/",
        "search_urls": {
            "jobs": "https://bbva.csod.com/ux/ats/careersite/2/home?c=bbva",
            "workday": "https://bbva.wd3.myworkdayjobs.com/es/BBVA",
        },
        "scraper": {
            "type": "workday",
            "tenant": "bbva",
            "instance": 3,
            "site": "BBVA",
        },
        "cities": {"Madrid": True, "Paris": False, "London": True},
    },
    {
        "name": "Santander",
        "short": "SAN",
        "category": "Bank",
        "subcategory": "Spanish Universal",
        "careers_url": "https://www.santander.com/en/careers",
        "search_urls": {
            "early_careers": "https://santandercareers.wd3.myworkdayjobs.com/SantanderCareers",
        },
        "scraper": {
            "type": "workday",
            "tenant": "santander",
            "instance": 3,
            "site": "SantanderCareers",
        },
        "cities": {"Madrid": True, "Paris": False, "London": True},
    },
    {
        "name": "CaixaBank",
        "short": "CABK",
        "category": "Bank",
        "subcategory": "Spanish Universal",
        "careers_url": "https://www.caixabank.com/en/work-with-us.html",
        "search_urls": {},
        "scraper": {"type": "direct_link"},
        "cities": {"Madrid": True, "Paris": False, "London": False},
    },
    {
        "name": "Bankinter",
        "short": "BKNT",
        "category": "Bank",
        "subcategory": "Spanish",
        "careers_url": "https://www.bankinter.com/",
        "search_urls": {},
        "scraper": {"type": "direct_link"},
        "cities": {"Madrid": True, "Paris": False, "London": False},
    },

    # ==========================================================
    # SWISS PRIVATE BANKS
    # ==========================================================
    {
        "name": "Pictet",
        "short": "PICT",
        "category": "Private Bank",
        "subcategory": "Swiss",
        "careers_url": "https://www.group.pictet/careers",
        "search_urls": {
            "jobs": "https://career5.successfactors.eu/careers?company=picaborneP",
        },
        "scraper": {"type": "direct_link"},
        "cities": {"Madrid": True, "Paris": True, "London": True},
    },
    {
        "name": "Lombard Odier",
        "short": "LO",
        "category": "Private Bank",
        "subcategory": "Swiss",
        "careers_url": "https://www.lombardodier.com/careers",
        "search_urls": {
            "workday": "https://lombardodier.wd3.myworkdayjobs.com/Lombard_Odier_Careers",
        },
        "scraper": {
            "type": "workday",
            "tenant": "lombardodier",
            "instance": 3,
            "site": "Lombard_Odier_Careers",
        },
        "cities": {"Madrid": True, "Paris": True, "London": True},
    },
    {
        "name": "Julius Baer",
        "short": "JB",
        "category": "Private Bank",
        "subcategory": "Swiss",
        "careers_url": "https://www.juliusbaer.com/en/careers/",
        "search_urls": {
            "jobs": "https://jobs.juliusbaer.com/",
            "workday": "https://juliusbaer.wd3.myworkdayjobs.com/External",
        },
        "scraper": {
            "type": "workday",
            "tenant": "juliusbaer",
            "instance": 3,
            "site": "External",
        },
        "cities": {"Madrid": True, "Paris": False, "London": True},
    },
    {
        "name": "Edmond de Rothschild",
        "short": "EdR",
        "category": "Private Bank",
        "subcategory": "Swiss",
        "careers_url": "https://www.edmond-de-rothschild.com/en/careers",
        "search_urls": {},
        "scraper": {"type": "direct_link"},
        "cities": {"Madrid": False, "Paris": True, "London": True},
    },

    # ==========================================================
    # ASSET MANAGERS
    # ==========================================================
    {
        "name": "BlackRock",
        "short": "BLK",
        "category": "Asset Manager",
        "subcategory": "Global",
        "careers_url": "https://careers.blackrock.com/",
        "search_urls": {
            "early_careers": "https://careers.blackrock.com/early-careers/",
        },
        "scraper": {
            "type": "workday",
            "tenant": "blackrock",
            "instance": 1,
            "site": "BlackRock_Professional",
        },
        "cities": {"Madrid": False, "Paris": True, "London": True},
    },
    {
        "name": "Fidelity International",
        "short": "FIL",
        "category": "Asset Manager",
        "subcategory": "Global",
        "careers_url": "https://www.fidelityinternational.com/careers/",
        "search_urls": {
            "workday": "https://fil.wd3.myworkdayjobs.com/001",
        },
        "scraper": {
            "type": "workday",
            "tenant": "fil",
            "instance": 3,
            "site": "001",
        },
        "cities": {"Madrid": False, "Paris": False, "London": True},
    },
    {
        "name": "State Street",
        "short": "STT",
        "category": "Asset Manager",
        "subcategory": "Global",
        "careers_url": "https://careers.statestreet.com/",
        "search_urls": {
            "workday": "https://statestreet.wd1.myworkdayjobs.com/Global",
        },
        "scraper": {
            "type": "workday",
            "tenant": "statestreet",
            "instance": 1,
            "site": "Global",
        },
        "cities": {"Madrid": False, "Paris": True, "London": True},
    },
    {
        "name": "Amundi",
        "short": "AMUN",
        "category": "Asset Manager",
        "subcategory": "European",
        "careers_url": "https://careers.amundi.com/",
        "search_urls": {
            "internships": "https://careers.amundi.com/search/?q=intern",
        },
        "scraper": {"type": "direct_link"},
        "cities": {"Madrid": True, "Paris": True, "London": True},
    },
    {
        "name": "Schroders",
        "short": "SCHR",
        "category": "Asset Manager",
        "subcategory": "European",
        "careers_url": "https://www.schroders.com/en/careers/",
        "search_urls": {
            "early_careers": "https://www.schroders.com/en/careers/early-careers/",
        },
        "scraper": {
            "type": "oracle_hcm",
            "domain": "ekbq.fa.em2.oraclecloud.com",
            "site_number": "CX_2",
            "job_url_template": "https://ekbq.fa.em2.oraclecloud.com/hcmUI/CandidateExperience/en/sites/CX_2/job/{id}",
        },
        "cities": {"Madrid": False, "Paris": False, "London": True},
    },
    {
        "name": "Invesco",
        "short": "IVZ",
        "category": "Asset Manager",
        "subcategory": "Global",
        "careers_url": "https://careers.invesco.com/",
        "search_urls": {
            "workday": "https://invesco.wd1.myworkdayjobs.com/IVZ",
        },
        "scraper": {
            "type": "workday",
            "tenant": "invesco",
            "instance": 1,
            "site": "IVZ",
        },
        "cities": {"Madrid": True, "Paris": True, "London": True},
    },
    {
        "name": "PIMCO",
        "short": "PIMCO",
        "category": "Asset Manager",
        "subcategory": "Global",
        "careers_url": "https://pimco.com/en-us/careers",
        "search_urls": {},
        "scraper": {"type": "direct_link"},
        "cities": {"Madrid": False, "Paris": False, "London": True},
    },
    {
        "name": "Vanguard",
        "short": "VAN",
        "category": "Asset Manager",
        "subcategory": "Global",
        "careers_url": "https://www.vanguardjobs.com/",
        "search_urls": {
            "workday": "https://vanguard.wd5.myworkdayjobs.com/vanguard_external",
        },
        "scraper": {
            "type": "workday",
            "tenant": "vanguard",
            "instance": 5,
            "site": "vanguard_external",
        },
        "cities": {"Madrid": False, "Paris": False, "London": True},
    },
    {
        "name": "Tikehau Capital",
        "short": "TKO",
        "category": "Asset Manager",
        "subcategory": "European Alternative",
        "careers_url": "https://www.tikehaucapital.com/en/careers",
        "search_urls": {},
        "scraper": {"type": "direct_link"},
        "cities": {"Madrid": True, "Paris": True, "London": True},
    },

    # ==========================================================
    # HEDGE FUNDS
    # ==========================================================
    {
        "name": "Millennium Management",
        "short": "MLP",
        "category": "Hedge Fund",
        "subcategory": "Multi-Strategy",
        "careers_url": "https://www.mlp.com/careers/",
        "search_urls": {},
        "scraper": {"type": "direct_link"},
        "cities": {"Madrid": False, "Paris": True, "London": True},
    },
    {
        "name": "Capula Investment Management",
        "short": "CAPULA",
        "category": "Hedge Fund",
        "subcategory": "Fixed Income",
        "careers_url": "https://www.capulaglobal.com/working-at-capula/",
        "search_urls": {},
        "scraper": {"type": "direct_link"},
        "cities": {"Madrid": False, "Paris": False, "London": True},
    },
    {
        "name": "Point72",
        "short": "P72",
        "category": "Hedge Fund",
        "subcategory": "Multi-Strategy",
        "careers_url": "https://point72.com/careers/",
        "search_urls": {
            "greenhouse": "https://job-boards.greenhouse.io/point72",
        },
        "scraper": {"type": "greenhouse", "board": "point72"},
        "cities": {"Madrid": False, "Paris": True, "London": True},
    },
    {
        "name": "LMR Partners",
        "short": "LMR",
        "category": "Hedge Fund",
        "subcategory": "Multi-Strategy",
        "careers_url": "https://www.lmrpartners.com/careers",
        "search_urls": {},
        "scraper": {"type": "direct_link"},
        "cities": {"Madrid": False, "Paris": False, "London": True},
    },
    {
        "name": "Citadel",
        "short": "CIT",
        "category": "Hedge Fund",
        "subcategory": "Multi-Strategy",
        "careers_url": "https://www.citadel.com/careers/",
        "search_urls": {
            "campus": "https://www.citadel.com/careers/open-opportunities/",
        },
        # Citadel uses a private/gated Greenhouse board — public API returns 404.
        "scraper": {"type": "direct_link"},
        "cities": {"Madrid": False, "Paris": True, "London": True},
    },
    {
        "name": "Two Sigma",
        "short": "2SIG",
        "category": "Hedge Fund",
        "subcategory": "Quantitative",
        "careers_url": "https://www.twosigma.com/careers/",
        "search_urls": {},
        # Two Sigma uses a private/gated Greenhouse board — public API returns 404.
        "scraper": {"type": "direct_link"},
        "cities": {"Madrid": False, "Paris": False, "London": True},
    },
    {
        "name": "Bridgewater Associates",
        "short": "BWA",
        "category": "Hedge Fund",
        "subcategory": "Macro",
        "careers_url": "https://www.bridgewater.com/careers",
        "search_urls": {
            "greenhouse": "https://job-boards.greenhouse.io/bridgewater89",
        },
        "scraper": {"type": "greenhouse", "board": "bridgewater89"},
        "cities": {"Madrid": False, "Paris": False, "London": True},
    },
    {
        "name": "Man Group",
        "short": "MAN",
        "category": "Hedge Fund",
        "subcategory": "Multi-Strategy",
        "careers_url": "https://www.man.com/careers",
        "search_urls": {
            "greenhouse": "https://job-boards.eu.greenhouse.io/mangroup",
        },
        "scraper": {"type": "greenhouse", "board": "mangroup"},
        "cities": {"Madrid": False, "Paris": False, "London": True},
    },
    {
        "name": "Marshall Wace",
        "short": "MW",
        "category": "Hedge Fund",
        "subcategory": "Long/Short Equity",
        "careers_url": "https://www.marshallwace.com/careers",
        "search_urls": {
            "greenhouse": "https://job-boards.greenhouse.io/marshallwace",
        },
        "scraper": {"type": "greenhouse", "board": "marshallwace"},
        "cities": {"Madrid": False, "Paris": False, "London": True},
    },
    {
        "name": "Brevan Howard",
        "short": "BH",
        "category": "Hedge Fund",
        "subcategory": "Macro",
        "careers_url": "https://www.brevanhoward.com/careers",
        "search_urls": {},
        "scraper": {"type": "direct_link"},
        "cities": {"Madrid": False, "Paris": False, "London": True},
    },
    {
        "name": "Balyasny Asset Management",
        "short": "BAM",
        "category": "Hedge Fund",
        "subcategory": "Multi-Strategy",
        "careers_url": "https://www.balyasny.com/careers",
        "search_urls": {
            "workday": "https://bamfunds.wd1.myworkdayjobs.com/External",
        },
        # Workday tenant now returns HTTP 401 (gated behind auth) — no public
        # API to scrape. Kept as a direct link until the board reopens.
        "scraper": {"type": "direct_link"},
        "cities": {"Madrid": False, "Paris": False, "London": True},
    },
    {
        "name": "DE Shaw",
        "short": "DES",
        "category": "Hedge Fund",
        "subcategory": "Quantitative",
        "careers_url": "https://www.deshaw.com/careers",
        "search_urls": {},
        "scraper": {"type": "direct_link"},
        "cities": {"Madrid": False, "Paris": False, "London": True},
    },

    # ==========================================================
    # PRIVATE EQUITY
    # ==========================================================
    {
        "name": "Blackstone",
        "short": "BX",
        "category": "Private Equity",
        "subcategory": "Mega Cap",
        "careers_url": "https://www.blackstone.com/careers/",
        "search_urls": {
            "campus": "https://blackstone.wd1.myworkdayjobs.com/Blackstone_Campus_Careers",
        },
        "scraper": {
            "type": "workday",
            "tenant": "blackstone",
            "instance": 1,
            "site": "Blackstone_Campus_Careers",
        },
        "cities": {"Madrid": True, "Paris": True, "London": True},
    },
    {
        "name": "KKR",
        "short": "KKR",
        "category": "Private Equity",
        "subcategory": "Mega Cap",
        "careers_url": "https://www.kkr.com/careers",
        "search_urls": {
            "workday": "https://kkr.wd5.myworkdayjobs.com/External_Career",
        },
        # KKR's Workday tenant currently redirects to a maintenance page (HTTP 403 on API).
        # Re-enable once the migration completes.
        "scraper": {"type": "direct_link"},
        "cities": {"Madrid": True, "Paris": True, "London": True},
    },
    {
        "name": "Apollo Global Management",
        "short": "APO",
        "category": "Private Equity",
        "subcategory": "Mega Cap",
        "careers_url": "https://www.apollo.com/careers",
        "search_urls": {
            "workday": "https://athene.wd5.myworkdayjobs.com/Apollo_Careers",
        },
        "scraper": {
            "type": "workday",
            "tenant": "athene",
            "instance": 5,
            "site": "Apollo_Careers",
        },
        "cities": {"Madrid": False, "Paris": False, "London": True},
    },
    {
        "name": "Carlyle Group",
        "short": "CG",
        "category": "Private Equity",
        "subcategory": "Mega Cap",
        "careers_url": "https://www.carlyle.com/careers",
        "search_urls": {},
        "scraper": {"type": "direct_link"},
        "cities": {"Madrid": True, "Paris": True, "London": True},
    },
    {
        "name": "Ardian",
        "short": "ARD",
        "category": "Private Equity",
        "subcategory": "European",
        "careers_url": "https://www.ardian.com/en/careers",
        "search_urls": {
            "workday": "https://ardian.wd103.myworkdayjobs.com/ArdianCareers",
        },
        "scraper": {
            "type": "workday",
            "tenant": "ardian",
            "instance": 103,
            "site": "ArdianCareers",
        },
        "cities": {"Madrid": True, "Paris": True, "London": True},
    },
    {
        "name": "Apax Partners",
        "short": "APAX",
        "category": "Private Equity",
        "subcategory": "European",
        "careers_url": "https://www.apax.com/careers/",
        "search_urls": {
            "lever": "https://jobs.lever.co/apax",
        },
        "scraper": {"type": "lever", "company": "apax"},
        "cities": {"Madrid": False, "Paris": True, "London": True},
    },
    {
        "name": "Thoma Bravo",
        "short": "TB",
        "category": "Private Equity",
        "subcategory": "Tech-focused",
        "careers_url": "https://www.thomabravo.com/careers",
        "search_urls": {},
        "scraper": {"type": "direct_link"},
        "cities": {"Madrid": False, "Paris": False, "London": True},
    },
    {
        "name": "CVC Capital Partners",
        "short": "CVC",
        "category": "Private Equity",
        "subcategory": "European",
        "careers_url": "https://www.cvc.com/careers/",
        "search_urls": {},
        "scraper": {"type": "direct_link"},
        "cities": {"Madrid": True, "Paris": True, "London": True},
    },
    {
        "name": "Permira",
        "short": "PERM",
        "category": "Private Equity",
        "subcategory": "European",
        "careers_url": "https://www.permira.com/careers",
        "search_urls": {
            "greenhouse": "https://job-boards.eu.greenhouse.io/permiraexternalprivate",
        },
        "scraper": {"type": "greenhouse", "board": "permiraexternalprivate"},
        "cities": {"Madrid": True, "Paris": True, "London": True},
    },
    {
        "name": "EQT",
        "short": "EQT",
        "category": "Private Equity",
        "subcategory": "Nordic",
        "careers_url": "https://eqtgroup.com/careers/",
        "search_urls": {
            "greenhouse": "https://job-boards.eu.greenhouse.io/eqtpartners",
        },
        "scraper": {"type": "greenhouse", "board": "eqtpartners"},
        "cities": {"Madrid": True, "Paris": True, "London": True},
    },
    {
        "name": "Eurazeo",
        "short": "EURA",
        "category": "Private Equity",
        "subcategory": "European",
        "careers_url": "https://www.eurazeo.com/en/careers",
        "search_urls": {},
        "scraper": {"type": "direct_link"},
        "cities": {"Madrid": True, "Paris": True, "London": True},
    },
    {
        "name": "PAI Partners",
        "short": "PAI",
        "category": "Private Equity",
        "subcategory": "European",
        "careers_url": "https://www.paipartners.com/careers/",
        "search_urls": {},
        "scraper": {"type": "direct_link"},
        "cities": {"Madrid": True, "Paris": True, "London": True},
    },
    {
        "name": "BC Partners",
        "short": "BCP",
        "category": "Private Equity",
        "subcategory": "European",
        "careers_url": "https://www.bcpartners.com/careers/",
        "search_urls": {},
        "scraper": {"type": "direct_link"},
        "cities": {"Madrid": False, "Paris": True, "London": True},
    },
    {
        "name": "TPG",
        "short": "TPG",
        "category": "Private Equity",
        "subcategory": "Mega Cap",
        "careers_url": "https://www.tpg.com/careers/",
        "search_urls": {
            "greenhouse": "https://job-boards.greenhouse.io/tpgcareers",
        },
        "scraper": {"type": "greenhouse", "board": "tpgcareers"},
        "cities": {"Madrid": False, "Paris": True, "London": True},
    },
    {
        "name": "Cinven",
        "short": "CINV",
        "category": "Private Equity",
        "subcategory": "European",
        "careers_url": "https://www.cinven.com/careers/",
        "search_urls": {},
        "scraper": {"type": "direct_link"},
        "cities": {"Madrid": True, "Paris": True, "London": True},
    },

    # ==========================================================
    # ADVISORY BOUTIQUES / NEW LEADS (report §7 — Jan 2027 off-cycle)
    # ==========================================================
    {
        "name": "Evercore",
        "short": "EVR",
        "category": "Investment Bank",
        "subcategory": "Elite Boutique",
        "careers_url": "https://www.evercore.com/careers/",
        "search_urls": {
            "early_careers": "https://evercore.tal.net/vx/lang-en-GB/mobile-0/appcentre-1/brand-6/candidate/jobboard/vacancy/1/adv",
        },
        # Evercore runs an Oleeo/TalentLink board (evercore.tal.net). The list
        # surface exposes /opp/{id}-{slug} rows the oleeo scraper understands.
        "scraper": {
            "type": "oleeo",
            "list_url": "https://evercore.tal.net/vx/lang-en-GB/mobile-0/appcentre-1/brand-6/candidate/jobboard/vacancy/1/adv",
            "base": "https://evercore.tal.net",
        },
        "cities": {"Madrid": False, "Paris": True, "London": True},
    },
    {
        "name": "Houlihan Lokey",
        "short": "HL",
        "category": "Investment Bank",
        "subcategory": "Advisory / Restructuring",
        "careers_url": "https://hl.wd1.myworkdayjobs.com/HL_Careers",
        "search_urls": {
            "workday": "https://hl.wd1.myworkdayjobs.com/HL_Careers",
        },
        # Guessed Workday tenant/site returned an error — no confirmed public
        # endpoint. Kept as a direct link until the real CXS path is verified.
        "scraper": {"type": "direct_link"},
        "cities": {"Madrid": True, "Paris": True, "London": True},
    },
    {
        "name": "Clipperton",
        "short": "CLIP",
        "category": "Investment Bank",
        "subcategory": "Tech M&A Boutique",
        "careers_url": "https://clipperton.workable.com/",
        "search_urls": {
            "workable": "https://clipperton.workable.com/",
        },
        # Workable SPI endpoint for this subdomain returned an error (board may
        # not expose the public API). Kept as a direct link; the Jan-2027 role
        # is still reachable via the careers page + jobboard searches.
        "scraper": {"type": "direct_link"},
        "cities": {"Madrid": False, "Paris": True, "London": True},
    },
    {
        "name": "Alantra",
        "short": "ALN",
        "category": "Investment Bank",
        "subcategory": "European Advisory",
        "careers_url": "https://www.alantra.com/join-us/",
        "search_urls": {
            "wttj": "https://www.welcometothejungle.com/en/companies/alantra/jobs",
        },
        "scraper": {"type": "direct_link"},
        "cities": {"Madrid": True, "Paris": True, "London": True},
    },
    {
        "name": "Scalene Partners",
        "short": "SCAL",
        "category": "Investment Bank",
        "subcategory": "M&A Boutique",
        "careers_url": "https://www.welcometothejungle.com/fr/companies/scalene-partners/jobs",
        "search_urls": {},
        "scraper": {"type": "direct_link"},
        "cities": {"Madrid": False, "Paris": True, "London": False},
    },
    {
        "name": "Avolta Partners",
        "short": "AVOL",
        "category": "Investment Bank",
        "subcategory": "M&A Boutique",
        "careers_url": "https://www.welcometothejungle.com/fr/companies/avolta-partners/jobs",
        "search_urls": {},
        "scraper": {"type": "direct_link"},
        "cities": {"Madrid": False, "Paris": True, "London": False},
    },
    {
        "name": "Arcano Partners",
        "short": "ARC",
        "category": "Investment Bank",
        "subcategory": "Spanish Advisory / AM",
        "careers_url": "https://talento.arcanopartners.com/jobs",
        "search_urls": {
            "jobs": "https://talento.arcanopartners.com/jobs",
        },
        "scraper": {"type": "direct_link"},
        "cities": {"Madrid": True, "Paris": False, "London": False},
    },

    # ==========================================================
    # BROKERS / TRADING (markets-adjacent — accessible to a junior profile)
    # No reliably-public ATS API for most; surfaced as career links + covered
    # by the jobboard searches. Wire a scraper here if an endpoint is confirmed.
    # ==========================================================
    {
        "name": "TP ICAP",
        "short": "TPICAP",
        "category": "Broker",
        "subcategory": "Interdealer Broker",
        "careers_url": "https://www.tpicap.com/tpicap/careers",
        "search_urls": {},
        "scraper": {"type": "direct_link"},
        "cities": {"Madrid": True, "Paris": True, "London": True},
    },
    {
        "name": "BGC Group",
        "short": "BGC",
        "category": "Broker",
        "subcategory": "Interdealer Broker",
        "careers_url": "https://www.bgcg.com/careers/",
        "search_urls": {},
        "scraper": {"type": "direct_link"},
        "cities": {"Madrid": False, "Paris": True, "London": True},
    },
    {
        "name": "Compagnie Financière Tradition",
        "short": "CFT",
        "category": "Broker",
        "subcategory": "Interdealer Broker",
        "careers_url": "https://www.tradition.com/careers/",
        "search_urls": {},
        "scraper": {"type": "direct_link"},
        "cities": {"Madrid": False, "Paris": True, "London": True},
    },
    {
        "name": "Marex",
        "short": "MRX",
        "category": "Broker",
        "subcategory": "Commodities / Markets Broker",
        "careers_url": "https://www.marex.com/careers/",
        "search_urls": {},
        "scraper": {"type": "direct_link"},
        "cities": {"Madrid": False, "Paris": True, "London": True},
    },
    {
        "name": "Sucden Financial",
        "short": "SUC",
        "category": "Broker",
        "subcategory": "Derivatives Broker",
        "careers_url": "https://www.sucdenfinancial.com/careers/",
        "search_urls": {},
        "scraper": {"type": "direct_link"},
        "cities": {"Madrid": False, "Paris": False, "London": True},
    },
    {
        "name": "StoneX",
        "short": "SNEX",
        "category": "Broker",
        "subcategory": "Markets / Execution",
        "careers_url": "https://www.stonex.com/careers/",
        "search_urls": {},
        "scraper": {"type": "direct_link"},
        "cities": {"Madrid": False, "Paris": True, "London": True},
    },
    {
        "name": "Susquehanna (SIG)",
        "short": "SIG",
        "category": "Broker",
        "subcategory": "Trading / Market Maker",
        "careers_url": "https://careers.sig.com/",
        "search_urls": {},
        "scraper": {"type": "direct_link"},
        "cities": {"Madrid": False, "Paris": False, "London": True},
    },
    {
        "name": "IMC Trading",
        "short": "IMC",
        "category": "Broker",
        "subcategory": "Trading / Market Maker",
        "careers_url": "https://careers.imc.com/",
        "search_urls": {},
        "scraper": {"type": "direct_link"},
        "cities": {"Madrid": False, "Paris": False, "London": True},
    },
    {
        "name": "Optiver",
        "short": "OPT",
        "category": "Broker",
        "subcategory": "Trading / Market Maker",
        "careers_url": "https://optiver.com/working-at-optiver/career-opportunities/",
        "search_urls": {},
        "scraper": {"type": "direct_link"},
        "cities": {"Madrid": False, "Paris": False, "London": True},
    },
]

# ============================================================
# LINKEDIN / JOB BOARD SEARCH URLS
# ============================================================
LINKEDIN_SEARCHES = [
    {
        "name": "Finance Internships - Madrid",
        "url": "https://www.linkedin.com/jobs/search/?keywords=finance%20internship&location=Madrid&f_E=1",
    },
    {
        "name": "Finance Internships - Paris",
        "url": "https://www.linkedin.com/jobs/search/?keywords=finance%20internship&location=Paris&f_E=1",
    },
    {
        "name": "Finance Internships - London",
        "url": "https://www.linkedin.com/jobs/search/?keywords=finance%20internship&location=London&f_E=1",
    },
    {
        "name": "Banking Internships - Madrid",
        "url": "https://www.linkedin.com/jobs/search/?keywords=banking%20intern&location=Madrid&f_E=1",
    },
    {
        "name": "Private Banking Internships - Spain",
        "url": "https://www.linkedin.com/jobs/search/?keywords=private%20banking%20intern&location=Spain&f_E=1",
    },
    {
        "name": "Asset Management Internships - Europe",
        "url": "https://www.linkedin.com/jobs/search/?keywords=asset%20management%20intern&location=Europe&f_E=1",
    },
    {
        "name": "Stage Finance - Paris",
        "url": "https://www.linkedin.com/jobs/search/?keywords=stage%20finance&location=Paris&f_E=1",
    },
    {
        "name": "Prácticas Finanzas - Madrid",
        "url": "https://www.linkedin.com/jobs/search/?keywords=prácticas%20finanzas&location=Madrid&f_E=1",
    },
]

INDEED_SEARCHES = [
    {
        "name": "Finance Intern - Madrid",
        "url": "https://www.indeed.com/jobs?q=finance+intern&l=Madrid%2C+Spain",
    },
    {
        "name": "Finance Intern - Paris",
        "url": "https://fr.indeed.com/emplois?q=stage+finance&l=Paris",
    },
    {
        "name": "Finance Intern - London",
        "url": "https://www.indeed.co.uk/jobs?q=finance+internship&l=London",
    },
]

# Generalist jobboards that cannot be scraped reliably (bot protection / auth),
# surfaced as one-click pre-filled searches instead. Channel choices follow the
# report §7.5 ranking (eFinancialCareers best for markets/PB across all 3 cities;
# WTTJ strong for Paris; InfoJobs for Madrid; Bright Network for London).
JOBBOARD_SEARCHES = [
    {
        "name": "eFinancialCareers - Internships Madrid",
        "url": "https://www.efinancialcareers.com/search?q=internship&location=Madrid",
    },
    {
        "name": "eFinancialCareers - Internships Paris",
        "url": "https://www.efinancialcareers.fr/search?q=stage&location=Paris",
    },
    {
        "name": "eFinancialCareers - Internships London",
        "url": "https://www.efinancialcareers.co.uk/search?q=off-cycle+internship&location=London",
    },
    {
        "name": "Welcome to the Jungle - Stage Finance Paris",
        "url": "https://www.welcometothejungle.com/fr/jobs?query=stage%20finance&aroundQuery=Paris",
    },
    {
        "name": "Welcome to the Jungle - Stage M&A Janvier 2027",
        "url": "https://www.welcometothejungle.com/fr/jobs?query=stage%20M%26A%20janvier%202027",
    },
    {
        "name": "InfoJobs - Prácticas Finanzas Madrid",
        "url": "https://www.infojobs.net/ofertas-trabajo/practicas-finanzas/madrid",
    },
    {
        "name": "Glassdoor - Finance Internship Madrid",
        "url": "https://www.glassdoor.com/Job/madrid-finance-internship-jobs-SRCH_IL.0,6_IC2664319_KO7,25.htm",
    },
    {
        "name": "Bright Network - Off-Cycle Internships UK",
        "url": "https://www.brightnetwork.co.uk/search/?query=off-cycle+internship",
    },
]
