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
}

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
        "scraper": {"type": "oracle_hcm"},
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
        "scraper": {"type": "direct_link"},
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
        "scraper": {"type": "direct_link"},
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
            "campus": "https://campus.bankofamerica.com/careers/",
        },
        "scraper": {"type": "direct_link"},
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
        "scraper": {"type": "direct_link"},
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
            "search": "https://db.recsolu.com/external/requisitions",
        },
        "scraper": {"type": "direct_link"},
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
        "scraper": {"type": "direct_link"},
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
        "careers_url": "https://www.ca-cib.com/en/careers/students-and-young-graduates",
        "search_urls": {
            "students": "https://www.ca-cib.com/en/careers/students-and-young-graduates",
            "jobs_portal": "https://jobs.ca-cib.com/homepage.aspx?LCID=2057",
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
        "scraper": {"type": "direct_link"},
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
        "scraper": {"type": "direct_link"},
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
        },
        "scraper": {"type": "direct_link"},
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
        "search_urls": {},
        "scraper": {"type": "direct_link"},
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
        },
        "scraper": {"type": "direct_link"},
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
        "scraper": {"type": "direct_link"},
        "cities": {"Madrid": False, "Paris": True, "London": True},
    },
    {
        "name": "Fidelity International",
        "short": "FIL",
        "category": "Asset Manager",
        "subcategory": "Global",
        "careers_url": "https://www.fidelityinternational.com/careers/",
        "search_urls": {},
        "scraper": {"type": "direct_link"},
        "cities": {"Madrid": False, "Paris": False, "London": True},
    },
    {
        "name": "State Street",
        "short": "STT",
        "category": "Asset Manager",
        "subcategory": "Global",
        "careers_url": "https://careers.statestreet.com/",
        "search_urls": {},
        "scraper": {"type": "direct_link"},
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
        "scraper": {"type": "direct_link"},
        "cities": {"Madrid": False, "Paris": False, "London": True},
    },
    {
        "name": "Invesco",
        "short": "IVZ",
        "category": "Asset Manager",
        "subcategory": "Global",
        "careers_url": "https://careers.invesco.com/",
        "search_urls": {},
        "scraper": {"type": "direct_link"},
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
        "search_urls": {},
        "scraper": {"type": "direct_link"},
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
            "jobs": "https://careers.point72.com/CSCareerSearch/CareerSearch.aspx",
        },
        "scraper": {"type": "direct_link"},
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
        "scraper": {"type": "direct_link"},
        "cities": {"Madrid": False, "Paris": False, "London": True},
    },
    {
        "name": "Bridgewater Associates",
        "short": "BWA",
        "category": "Hedge Fund",
        "subcategory": "Macro",
        "careers_url": "https://www.bridgewater.com/careers",
        "search_urls": {},
        "scraper": {"type": "direct_link"},
        "cities": {"Madrid": False, "Paris": False, "London": True},
    },
    {
        "name": "Man Group",
        "short": "MAN",
        "category": "Hedge Fund",
        "subcategory": "Multi-Strategy",
        "careers_url": "https://www.man.com/careers",
        "search_urls": {},
        "scraper": {"type": "direct_link"},
        "cities": {"Madrid": False, "Paris": False, "London": True},
    },
    {
        "name": "Marshall Wace",
        "short": "MW",
        "category": "Hedge Fund",
        "subcategory": "Long/Short Equity",
        "careers_url": "https://www.marshallwace.com/careers",
        "search_urls": {},
        "scraper": {"type": "direct_link"},
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
        "search_urls": {},
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
        "search_urls": {},
        "scraper": {"type": "direct_link"},
        "cities": {"Madrid": True, "Paris": True, "London": True},
    },
    {
        "name": "Apollo Global Management",
        "short": "APO",
        "category": "Private Equity",
        "subcategory": "Mega Cap",
        "careers_url": "https://www.apollo.com/careers",
        "search_urls": {},
        "scraper": {"type": "direct_link"},
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
        "search_urls": {},
        "scraper": {"type": "direct_link"},
        "cities": {"Madrid": True, "Paris": True, "London": True},
    },
    {
        "name": "Apax Partners",
        "short": "APAX",
        "category": "Private Equity",
        "subcategory": "European",
        "careers_url": "https://www.apax.com/careers/",
        "search_urls": {},
        "scraper": {"type": "direct_link"},
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
        "search_urls": {},
        "scraper": {"type": "direct_link"},
        "cities": {"Madrid": True, "Paris": True, "London": True},
    },
    {
        "name": "EQT",
        "short": "EQT",
        "category": "Private Equity",
        "subcategory": "Nordic",
        "careers_url": "https://eqtgroup.com/careers/",
        "search_urls": {},
        "scraper": {"type": "direct_link"},
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
        "search_urls": {},
        "scraper": {"type": "direct_link"},
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
