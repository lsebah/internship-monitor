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

## Lancer en local

```bash
pip install -r requirements.txt
cd scraper && python main.py
cd ../docs && python -m http.server 8080
```
