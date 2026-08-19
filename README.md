# Internship Monitor - Charles Sebah

Dashboard de monitoring des offres de stages en finance (Madrid, Paris, Londres).

## Architecture

```
internship-monitor/
├── docs/                    # Site web (GitHub Pages)
│   ├── index.html
│   ├── style.css
│   ├── app.js
│   └── data/jobs.json       # Data mise à jour quotidiennement
├── scraper/                 # Scripts Python
│   ├── config.py            # 55+ firms, profil candidat, mots-clés
│   ├── scrapers.py          # Modules Workday, Greenhouse, Lever
│   ├── matcher.py           # Scoring profil/offre
│   └── main.py              # Orchestrateur principal
├── .github/workflows/
│   └── daily-scrape.yml     # GitHub Actions - scrape quotidien 9h
└── requirements.txt
```

## Déploiement sur GitHub

1. Créer un repo GitHub (public ou privé)
2. Push le code
3. Settings > Pages > Source: `docs/` folder depuis `main`
4. Le workflow GitHub Actions scrape chaque jour à 9h (Paris)
5. Le site est accessible via `https://<user>.github.io/internship-monitor/`

## 55+ firmes suivies

- **Investment Banks** : JP Morgan, Goldman Sachs, Morgan Stanley, Citi, BofA, Wells Fargo, Deutsche Bank, Barclays, HSBC, UBS, BNP Paribas, SocGen, CACIB, Natixis, Rothschild, Lazard
- **Banques Espagnoles** : BBVA, Santander, CaixaBank, Bankinter
- **Banques Privées Suisses** : Pictet, Lombard Odier, Julius Baer, Edmond de Rothschild
- **Asset Managers** : BlackRock, Fidelity, State Street, Amundi, Schroders, Invesco, PIMCO, Vanguard
- **Hedge Funds** : Millennium, Capula, Point72, LMR, Citadel, Two Sigma, Bridgewater, Man Group, Marshall Wace, Brevan Howard, Balyasny, DE Shaw
- **Private Equity** : Blackstone, KKR, Apollo, Carlyle, Ardian, Apax, Thoma Bravo, CVC, Permira, EQT, Eurazeo, PAI, BC Partners, TPG, Cinven

## Fiabilité du scraping

- **Échecs visibles** : un endpoint ATS injoignable (403/404/réseau) est désormais
  remonté comme `error` (et non plus masqué en `success, count=0`). Le compteur
  `firms_failed` est fiable, un bandeau d'alerte s'affiche sur le site, et une
  notification ntfy part quand une source casse.
- **Postes multi-villes** : les offres Workday affichées « N Locations » sont
  rattrapées via le détail de l'offre au lieu d'être jetées.
- **Refresh automatique** : scrape 3×/jour + un cron hebdomadaire de secours
  (lundi) qui garantit au moins un rafraîchissement par semaine.
- **`direct_link`** : ~29 firmes (banques privées, banques espagnoles…) n'ont pas
  d'API publique exploitable — elles restent en candidature directe via leur page
  carrière (onglet « Career Pages »), c'est volontaire.
- **Synchro cloud** : lecture seule côté navigateur. Aucun token n'est stocké dans
  le code client ; les statuts de candidature persistent localement par appareil.

## Cycle de vie d'une offre (lifecycle)

### 1. Pipeline de données (scraper/main.py, cron GitHub Actions)

```
┌────────────────────────────────────────────────────────────────┐
│        GitHub Actions — cron 3x/jour + rattrapage hebdo          │
└──────────────────────────────┬───────────────────────────────────┘
                                 │
                                 ▼
                       ┌──────────────────────┐
                       │    scraper/main.py     │
                       │     (orchestrateur)     │
                       └───────────┬─────────────┘
                                    │
        ┌───────────────────────────┼───────────────────────────┐
        ▼                            ▼                            ▼
┌────────────────┐        ┌────────────────────┐        ┌─────────────────────┐
│  scrape_firm()   │        │ build_curated_jobs() │        │ load_existing_data() │
│  55+ firmes :     │        │  offres saisies à la │        │  jobs.json existant,  │
│  Workday /        │        │  main (direct_link,  │        │  ré-indexé via         │
│  Greenhouse /     │        │  boards fermés)       │        │  make_job_id()         │
│  Lever            │        └──────────┬───────────┘        └──────────┬─────────────┘
└────────┬─────────┘                    │                                │
         │ success / error / empty       │                                │
         ▼                               │                                │
  scrape_status{}                        │                                │
         │                               │                                │
         └───────────────┬───────────────┘                                │
                           ▼                                              │
                  all_new_jobs[] ─────────────────────────────────────────┤
                                                                            ▼
                                                        ┌──────────────────────────────┐
                                                        │        merge_jobs()            │
                                                        │  • dédup par id (hash stable)   │
                                                        │  • conserve le first_seen le +   │
                                                        │    ancien, rafraîchit last_seen  │
                                                        │  • is_new = pas vu la veille     │
                                                        │  • score_job() + classify_match  │
                                                        │  • purge après 14j d'absence si  │
                                                        │    hors filtre stage/ville        │
                                                        └───────────────┬────────────────┘
                                                                         ▼
                                                                ┌──────────────────┐
                                                                │    save_data()      │
                                                                │ docs/data/jobs.json │
                                                                └─────────┬───────────┘
                                                                          ▼
                                                                ┌───────────────────────┐
                                                                │  GitHub Pages (docs/)   │
                                                                │  index.html + app.js     │
                                                                └─────────┬─────────────────┘
                                                                          ▼
                                                                 Dashboard utilisateur
```

### 2. Statut d'une offre côté utilisateur (docs/app.js, persistant par appareil)

```
                    ┌───────────────┐
   nouveau scrape   │      NEW       │
  ────────────────▶ │ (is_new=true)  │
                    └───────┬────────┘
                             │ affiché / vu
                             ▼
                    ┌───────────────┐
             ┌─────▶│    NOT_YET     │◀─────┐
             │      │   (par défaut)  │      │
             │      └───┬────────┬───┘      │
       "Not Yet"        │        │          │ "Not Yet"
             │   Applied│        │Corbeille │
             │          ▼        ▼          │
             │   ┌────────────┐ ┌────────────┐
             └───│  APPLIED    │ │  TRASHED    │
                 └────────────┘ └──────┬───────┘
                                        │
                                        ▼
                          persiste en local (par appareil),
                          n'empêche pas le re-scrape de l'offre

  En parallèle, côté pipeline : si une offre disparaît des scrapes
  pendant plus de 14 jours ET ne correspond plus aux filtres
  stage/ville, elle est purgée de docs/data/jobs.json.
```

## Lancer en local

```bash
pip install -r requirements.txt
cd scraper && python main.py
cd ../docs && python -m http.server 8080
```
