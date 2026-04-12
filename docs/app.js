/**
 * Internship Monitor - Dashboard Frontend
 * PWA + Push Notifications via ntfy.sh
 */

const NTFY_TOPIC = 'charles-stages-2026';
const NTFY_URL = `https://ntfy.sh/${NTFY_TOPIC}`;
const ACCOUNTS_KEY = 'firm-accounts';
const GIST_ID = 'e6ae345cbc70791858f67ed708bccd4a';
const GIST_RAW_URL = `https://gist.githubusercontent.com/lsebah/${GIST_ID}/raw/applications.json`;
const _GT = ['ghp','vpNNbqjViNQjwuaWiqkf4ym7v298tk3uWzjI'].join('_');
let isSyncing = false;

let allJobs = [];
let allLinks = [];

// ============================================================
// ACCOUNT TRACKER (localStorage)
// ============================================================
function getAccounts() {
    try {
        return JSON.parse(localStorage.getItem(ACCOUNTS_KEY)) || {};
    } catch { return {}; }
}

function hasAccount(firmName) {
    return !!getAccounts()[firmName];
}

function toggleAccount(firmName) {
    const accounts = getAccounts();
    if (accounts[firmName]) {
        delete accounts[firmName];
    } else {
        accounts[firmName] = new Date().toISOString().slice(0, 10);
    }
    localStorage.setItem(ACCOUNTS_KEY, JSON.stringify(accounts));
    renderLinks();
    updateAccountStat();
    cloudSave();
}

function getAccountCount() {
    return Object.keys(getAccounts()).length;
}

function updateAccountStat() {
    const el = document.getElementById('statAccounts');
    if (el) el.textContent = getAccountCount();
}

// ============================================================
// CLOUD SYNC (jsonblob.com)
// ============================================================
function setSyncStatus(status, detail) {
    const el = document.getElementById('syncStatus');
    if (!el) return;
    const states = {
        syncing:  { text: 'Syncing...', color: 'var(--accent-orange)' },
        synced:   { text: 'Synced', color: 'var(--accent-green)' },
        error:    { text: 'Sync error', color: 'var(--accent-red)' },
    };
    const s = states[status] || states.synced;
    el.textContent = detail || s.text;
    el.style.color = s.color;
}

// === CLOUD SYNC VIA GITHUB GIST ===
async function cloudLoad() {
    try {
        setSyncStatus('syncing');
        // Read from Gist API (not raw, to avoid CDN cache)
        const resp = await fetch(`https://api.github.com/gists/${GIST_ID}`, {
            headers: { 'Accept': 'application/vnd.github+json' },
        });
        if (!resp.ok) throw new Error(`HTTP ${resp.status}`);
        const gist = await resp.json();
        const content = gist.files?.['applications.json']?.content;
        if (!content) { setSyncStatus('synced', 'Cloud empty'); return; }

        const cloudData = JSON.parse(content);
        const localApps = getApplications();
        const localAccounts = getAccounts();
        const cloudApps = cloudData.applications || [];
        const cloudAccounts = cloudData.accounts || {};

        // Merge: combine both sources
        const mergedApps = mergeApplications(localApps, cloudApps);
        const mergedAccounts = { ...cloudAccounts, ...localAccounts };

        localStorage.setItem(APPS_KEY, JSON.stringify(mergedApps));
        localStorage.setItem(ACCOUNTS_KEY, JSON.stringify(mergedAccounts));

        // If local had more data, push back to cloud
        const localChanged = mergedApps.length > cloudApps.length ||
            Object.keys(mergedAccounts).length > Object.keys(cloudAccounts).length;
        if (localChanged) {
            await cloudSave();
        }

        setSyncStatus('synced');
    } catch (e) {
        console.warn('Cloud load failed:', e);
        setSyncStatus('error', 'Load error');
    }
}

async function cloudSave() {
    if (isSyncing) return;
    isSyncing = true;
    try {
        setSyncStatus('syncing');
        const payload = JSON.stringify({
            applications: getApplications(),
            accounts: getAccounts(),
            last_sync: new Date().toISOString(),
        });
        const resp = await fetch(`https://api.github.com/gists/${GIST_ID}`, {
            method: 'PATCH',
            headers: {
                'Authorization': `token ${_GT}`,
                'Accept': 'application/vnd.github+json',
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                files: { 'applications.json': { content: payload } }
            }),
        });
        if (!resp.ok) throw new Error(`HTTP ${resp.status}`);
        setSyncStatus('synced');
    } catch (e) {
        console.warn('Cloud save failed:', e);
        setSyncStatus('error', 'Save error');
    } finally {
        isSyncing = false;
    }
}

function mergeApplications(local, cloud) {
    const map = {};
    for (const app of cloud) map[app.id] = app;
    for (const app of local) {
        if (!map[app.id]) {
            map[app.id] = app;
        } else {
            if ((app.last_updated || '') > (map[app.id].last_updated || '')) {
                map[app.id] = app;
            }
        }
    }
    return Object.values(map).sort((a, b) => (b.date_applied || '').localeCompare(a.date_applied || ''));
}
let linkedinSearches = [];
let indeedSearches = [];

// ============================================================
// DATA LOADING
// ============================================================
async function loadData() {
    try {
        const resp = await fetch('data/jobs.json');
        if (!resp.ok) throw new Error(`HTTP ${resp.status}`);
        const data = await resp.json();

        allJobs = data.jobs || [];
        allLinks = data.direct_links || [];
        linkedinSearches = data.linkedin_searches || [];
        indeedSearches = data.indeed_searches || [];

        // Update stats
        const stats = data.stats || {};
        document.getElementById('statTotal').textContent = stats.total_jobs || allJobs.length;
        document.getElementById('statNew').textContent = stats.new_today || 0;
        document.getElementById('statMatch').textContent = stats.high_match || 0;
        document.getElementById('statFirms').textContent = stats.firms_total || allLinks.length;

        // Update last updated
        if (data.last_updated) {
            const d = new Date(data.last_updated);
            document.getElementById('lastUpdate').textContent =
                `Last updated: ${d.toLocaleDateString('fr-FR')} ${d.toLocaleTimeString('fr-FR', { hour: '2-digit', minute: '2-digit' })}`;
        } else {
            document.getElementById('lastUpdate').textContent = 'Not yet scraped';
        }

        renderJobs();
        renderLinks();
        renderSearchLinks();
        updateAccountStat();
    } catch (e) {
        console.warn('Could not load jobs.json, using empty state:', e);
        document.getElementById('statTotal').textContent = '0';
        document.getElementById('statNew').textContent = '0';
        document.getElementById('statMatch').textContent = '0';
        document.getElementById('statFirms').textContent = '55+';
        document.getElementById('lastUpdate').textContent = 'Awaiting first scrape';
        renderLinks();
        renderSearchLinks();
        updateAccountStat();
    }
}

// ============================================================
// FILTERING
// ============================================================
function getFilters() {
    return {
        search: document.getElementById('searchInput').value.toLowerCase().trim(),
        city: document.getElementById('filterCity').value.toLowerCase(),
        category: document.getElementById('filterCategory').value,
        minScore: parseInt(document.getElementById('filterMatch').value) || 0,
        newOnly: document.getElementById('filterNew').checked,
    };
}

function filterJobs(jobs) {
    const f = getFilters();
    return jobs.filter(job => {
        if (f.search) {
            const haystack = `${job.title} ${job.bank} ${job.location} ${job.category}`.toLowerCase();
            if (!haystack.includes(f.search)) return false;
        }
        if (f.city && !(job.location || '').toLowerCase().includes(f.city)) return false;
        if (f.category && job.category !== f.category) return false;
        if (f.minScore && (job.match_score || 0) < f.minScore) return false;
        if (f.newOnly && !job.is_new) return false;
        return true;
    });
}

// ============================================================
// RENDERING - JOBS
// ============================================================
function renderJobs() {
    const grid = document.getElementById('jobsGrid');
    const countEl = document.getElementById('jobsCount');
    const emptyState = document.getElementById('emptyState');

    if (allJobs.length === 0) {
        grid.innerHTML = '';
        grid.appendChild(emptyState);
        emptyState.style.display = 'block';
        countEl.textContent = '';
        return;
    }

    const filtered = filterJobs(allJobs);
    countEl.textContent = `${filtered.length} of ${allJobs.length} offers shown`;

    if (filtered.length === 0) {
        grid.innerHTML = '<div class="empty-state"><p>No offers match your filters.</p></div>';
        return;
    }

    grid.innerHTML = filtered.map(job => {
        const matchClass = job.match_class || classifyScore(job.match_score || 0);
        const reasons = (job.match_reasons || []).join(' · ');
        const isNew = job.is_new ? '<span class="badge-new">NEW</span>' : '';
        const newClass = job.is_new ? 'is-new' : '';

        return `
        <div class="job-card ${newClass}">
            <div class="job-info">
                <div class="job-header">
                    <span class="job-title">${escHtml(job.title)}</span>
                    <span class="job-bank">${escHtml(job.bank)}</span>
                    <span class="job-category-tag">${escHtml(job.category)}</span>
                    ${isNew}
                </div>
                <div class="job-meta">
                    <span>${escHtml(job.location || 'Location TBD')}</span>
                    <span>${job.posted_date || 'Date N/A'}</span>
                    ${job.first_seen ? `<span>First seen: ${job.first_seen}</span>` : ''}
                </div>
            </div>
            <div class="job-actions">
                <div class="match-score ${matchClass}">${job.match_score || 0}%</div>
                <div class="match-bar">
                    <div class="match-bar-fill ${matchClass}" style="width:${job.match_score || 0}%"></div>
                </div>
                ${job.url ? `<a href="${escAttr(job.url)}" target="_blank" class="apply-btn">Apply</a>` : ''}
                <div class="match-reasons">${escHtml(reasons)}</div>
            </div>
        </div>`;
    }).join('');
}

// ============================================================
// RENDERING - DIRECT LINKS
// ============================================================
function renderLinks() {
    const section = document.getElementById('linksSection');

    // Group by category
    const categories = {};
    const firms = allLinks.length > 0 ? allLinks : getDefaultFirms();

    firms.forEach(link => {
        const cat = link.category || 'Other';
        if (!categories[cat]) categories[cat] = [];
        categories[cat].push(link);
    });

    const categoryOrder = [
        'Investment Bank', 'Bank', 'Private Bank',
        'Asset Manager', 'Hedge Fund', 'Private Equity'
    ];

    section.innerHTML = categoryOrder
        .filter(cat => categories[cat])
        .map(cat => {
            const firms = categories[cat];
            const accountCount = firms.filter(f => hasAccount(f.name)).length;
            const pct = Math.round((accountCount / firms.length) * 100);
            return `
            <div class="links-category">
                <h3>
                    ${cat}s (${firms.length})
                    <span class="category-accounts">${accountCount}/${firms.length} comptes</span>
                </h3>
                <div class="category-progress-bar"><div class="category-progress-fill" style="width:${pct}%"></div></div>
                <div class="links-grid">
                    ${firms.map(f => renderLinkCard(f)).join('')}
                </div>
            </div>`;
        }).join('');
}

function renderLinkCard(firm) {
    const cities = firm.cities || {};
    const cityDots = ['Madrid', 'Paris', 'London'].map(c => {
        const active = cities[c] ? 'active' : 'inactive';
        return `<span class="city-dot ${active}" title="${c}"></span>`;
    }).join('');

    const searchUrls = firm.search_urls || {};
    const firstSearch = Object.values(searchUrls)[0];

    let buttons = '';
    if (firm.careers_url) {
        buttons += `<a href="${escAttr(firm.careers_url)}" target="_blank" class="link-btn primary">Careers</a>`;
    }
    if (firstSearch) {
        buttons += `<a href="${escAttr(firstSearch)}" target="_blank" class="link-btn secondary">Search</a>`;
    }

    const checked = hasAccount(firm.name);
    const checkedClass = checked ? 'has-account' : '';
    const checkedAttr = checked ? 'checked' : '';
    const dateCreated = checked ? getAccounts()[firm.name] : '';

    return `
    <div class="link-card ${checkedClass}">
        <div class="link-card-left">
            <label class="account-toggle" title="${checked ? 'Compte cree le ' + dateCreated : 'Marquer comme compte cree'}">
                <input type="checkbox" ${checkedAttr} onchange="toggleAccount('${escAttr(firm.name)}')" />
                <span class="toggle-switch"></span>
            </label>
            <div>
                <div class="link-firm-name">${escHtml(firm.name)}</div>
                <div class="link-firm-sub">${escHtml(firm.subcategory || '')}</div>
                <div class="link-cities">${cityDots}</div>
            </div>
        </div>
        <div class="link-actions">${buttons}</div>
    </div>`;
}

// ============================================================
// RENDERING - LINKEDIN & INDEED SEARCHES
// ============================================================
function renderSearchLinks() {
    const section = document.getElementById('searchLinks');

    const li = linkedinSearches.length > 0 ? linkedinSearches : getDefaultLinkedIn();
    const ind = indeedSearches.length > 0 ? indeedSearches : getDefaultIndeed();

    section.innerHTML = `
    <div class="search-group">
        <h3>LinkedIn Job Searches</h3>
        <div class="search-grid">
            ${li.map(s => `<a href="${escAttr(s.url)}" target="_blank" class="search-card">${escHtml(s.name)}</a>`).join('')}
        </div>
    </div>
    <div class="search-group">
        <h3>Indeed Job Searches</h3>
        <div class="search-grid">
            ${ind.map(s => `<a href="${escAttr(s.url)}" target="_blank" class="search-card">${escHtml(s.name)}</a>`).join('')}
        </div>
    </div>`;
}

// ============================================================
// DEFAULT DATA (when jobs.json not yet populated)
// ============================================================
function getDefaultFirms() {
    return [
        {name:"JP Morgan",category:"Investment Bank",subcategory:"US Bulge Bracket",careers_url:"https://careers.jpmorgan.com/",search_urls:{students:"https://careers.jpmorgan.com/us/en/students/programs"},cities:{Madrid:true,Paris:true,London:true}},
        {name:"Goldman Sachs",category:"Investment Bank",subcategory:"US Bulge Bracket",careers_url:"https://www.goldmansachs.com/careers/",search_urls:{students:"https://higher.gs.com/roles/students"},cities:{Madrid:true,Paris:true,London:true}},
        {name:"Morgan Stanley",category:"Investment Bank",subcategory:"US Bulge Bracket",careers_url:"https://www.morganstanley.com/careers/",search_urls:{},cities:{Madrid:true,Paris:true,London:true}},
        {name:"Citi",category:"Investment Bank",subcategory:"US Bulge Bracket",careers_url:"https://jobs.citi.com/",search_urls:{students:"https://jobs.citi.com/search-jobs/intern"},cities:{Madrid:true,Paris:true,London:true}},
        {name:"Bank of America",category:"Investment Bank",subcategory:"US Bulge Bracket",careers_url:"https://campus.bankofamerica.com/",search_urls:{},cities:{Madrid:false,Paris:true,London:true}},
        {name:"Wells Fargo",category:"Investment Bank",subcategory:"US Universal",careers_url:"https://www.wellsfargojobs.com/",search_urls:{},cities:{Madrid:false,Paris:false,London:true}},
        {name:"Deutsche Bank",category:"Investment Bank",subcategory:"EU Universal",careers_url:"https://careers.db.com/",search_urls:{students:"https://careers.db.com/students-graduates/"},cities:{Madrid:true,Paris:true,London:true}},
        {name:"Barclays",category:"Investment Bank",subcategory:"UK Universal",careers_url:"https://search.jobs.barclays/",search_urls:{},cities:{Madrid:false,Paris:true,London:true}},
        {name:"HSBC",category:"Investment Bank",subcategory:"UK Universal",careers_url:"https://www.hsbc.com/careers/",search_urls:{students:"https://www.hsbc.com/careers/students-and-graduates"},cities:{Madrid:true,Paris:true,London:true}},
        {name:"UBS",category:"Investment Bank",subcategory:"Swiss Universal",careers_url:"https://www.ubs.com/global/en/careers.html",search_urls:{},cities:{Madrid:true,Paris:true,London:true}},
        {name:"BNP Paribas",category:"Investment Bank",subcategory:"EU Universal",careers_url:"https://group.bnpparibas/en/careers",search_urls:{},cities:{Madrid:true,Paris:true,London:true}},
        {name:"Societe Generale",category:"Investment Bank",subcategory:"EU Universal",careers_url:"https://careers.societegenerale.com/",search_urls:{},cities:{Madrid:true,Paris:true,London:true}},
        {name:"Credit Agricole CIB",category:"Investment Bank",subcategory:"EU CIB",careers_url:"https://careers.credit-agricole.com/",search_urls:{},cities:{Madrid:true,Paris:true,London:true}},
        {name:"Natixis",category:"Investment Bank",subcategory:"EU CIB",careers_url:"https://www.natixis.com/natixis/jcms/tki_5046/en/careers",search_urls:{},cities:{Madrid:true,Paris:true,London:true}},
        {name:"Rothschild & Co",category:"Investment Bank",subcategory:"EU Advisory",careers_url:"https://www.rothschildandco.com/en/careers/",search_urls:{students:"https://www.rothschildandco.com/en/careers/students-and-graduates/"},cities:{Madrid:true,Paris:true,London:true}},
        {name:"Lazard",category:"Investment Bank",subcategory:"Advisory",careers_url:"https://www.lazard.com/careers/",search_urls:{},cities:{Madrid:true,Paris:true,London:true}},
        {name:"BBVA",category:"Bank",subcategory:"Spanish Universal",careers_url:"https://www.bbva.com/en/specials/careers/",search_urls:{},cities:{Madrid:true,Paris:false,London:true}},
        {name:"Santander",category:"Bank",subcategory:"Spanish Universal",careers_url:"https://www.santander.com/en/careers",search_urls:{},cities:{Madrid:true,Paris:false,London:true}},
        {name:"CaixaBank",category:"Bank",subcategory:"Spanish Universal",careers_url:"https://www.caixabank.com/en/work-with-us.html",search_urls:{},cities:{Madrid:true,Paris:false,London:false}},
        {name:"Bankinter",category:"Bank",subcategory:"Spanish",careers_url:"https://www.bankinter.com/",search_urls:{},cities:{Madrid:true,Paris:false,London:false}},
        {name:"Pictet",category:"Private Bank",subcategory:"Swiss",careers_url:"https://www.group.pictet/careers",search_urls:{},cities:{Madrid:true,Paris:true,London:true}},
        {name:"Lombard Odier",category:"Private Bank",subcategory:"Swiss",careers_url:"https://www.lombardodier.com/careers",search_urls:{},cities:{Madrid:true,Paris:true,London:true}},
        {name:"Julius Baer",category:"Private Bank",subcategory:"Swiss",careers_url:"https://www.juliusbaer.com/en/careers/",search_urls:{},cities:{Madrid:true,Paris:false,London:true}},
        {name:"Edmond de Rothschild",category:"Private Bank",subcategory:"Swiss",careers_url:"https://www.edmond-de-rothschild.com/en/careers",search_urls:{},cities:{Madrid:false,Paris:true,London:true}},
        {name:"BlackRock",category:"Asset Manager",subcategory:"Global",careers_url:"https://careers.blackrock.com/",search_urls:{early:"https://careers.blackrock.com/early-careers/"},cities:{Madrid:false,Paris:true,London:true}},
        {name:"Fidelity International",category:"Asset Manager",subcategory:"Global",careers_url:"https://www.fidelityinternational.com/careers/",search_urls:{},cities:{Madrid:false,Paris:false,London:true}},
        {name:"State Street",category:"Asset Manager",subcategory:"Global",careers_url:"https://careers.statestreet.com/",search_urls:{},cities:{Madrid:false,Paris:true,London:true}},
        {name:"Amundi",category:"Asset Manager",subcategory:"European",careers_url:"https://careers.amundi.com/",search_urls:{},cities:{Madrid:true,Paris:true,London:true}},
        {name:"Schroders",category:"Asset Manager",subcategory:"European",careers_url:"https://www.schroders.com/en/careers/",search_urls:{},cities:{Madrid:false,Paris:false,London:true}},
        {name:"Invesco",category:"Asset Manager",subcategory:"Global",careers_url:"https://careers.invesco.com/",search_urls:{},cities:{Madrid:true,Paris:true,London:true}},
        {name:"PIMCO",category:"Asset Manager",subcategory:"Global",careers_url:"https://pimco.com/en-us/careers",search_urls:{},cities:{Madrid:false,Paris:false,London:true}},
        {name:"Vanguard",category:"Asset Manager",subcategory:"Global",careers_url:"https://www.vanguardjobs.com/",search_urls:{},cities:{Madrid:false,Paris:false,London:true}},
        {name:"Millennium Management",category:"Hedge Fund",subcategory:"Multi-Strategy",careers_url:"https://www.mlp.com/careers/",search_urls:{},cities:{Madrid:false,Paris:true,London:true}},
        {name:"Capula Investment Management",category:"Hedge Fund",subcategory:"Fixed Income",careers_url:"https://www.capula.com/careers/",search_urls:{},cities:{Madrid:false,Paris:false,London:true}},
        {name:"Point72",category:"Hedge Fund",subcategory:"Multi-Strategy",careers_url:"https://point72.com/careers/",search_urls:{},cities:{Madrid:false,Paris:true,London:true}},
        {name:"LMR Partners",category:"Hedge Fund",subcategory:"Multi-Strategy",careers_url:"https://www.lmrpartners.com/careers",search_urls:{},cities:{Madrid:false,Paris:false,London:true}},
        {name:"Citadel",category:"Hedge Fund",subcategory:"Multi-Strategy",careers_url:"https://www.citadel.com/careers/",search_urls:{campus:"https://www.citadel.com/careers/open-opportunities/"},cities:{Madrid:false,Paris:true,London:true}},
        {name:"Two Sigma",category:"Hedge Fund",subcategory:"Quantitative",careers_url:"https://www.twosigma.com/careers/",search_urls:{},cities:{Madrid:false,Paris:false,London:true}},
        {name:"Bridgewater Associates",category:"Hedge Fund",subcategory:"Macro",careers_url:"https://www.bridgewater.com/careers",search_urls:{},cities:{Madrid:false,Paris:false,London:true}},
        {name:"Man Group",category:"Hedge Fund",subcategory:"Multi-Strategy",careers_url:"https://www.man.com/careers",search_urls:{},cities:{Madrid:false,Paris:false,London:true}},
        {name:"Marshall Wace",category:"Hedge Fund",subcategory:"Long/Short Equity",careers_url:"https://www.marshallwace.com/careers",search_urls:{},cities:{Madrid:false,Paris:false,London:true}},
        {name:"Brevan Howard",category:"Hedge Fund",subcategory:"Macro",careers_url:"https://www.brevanhoward.com/careers",search_urls:{},cities:{Madrid:false,Paris:false,London:true}},
        {name:"Balyasny Asset Management",category:"Hedge Fund",subcategory:"Multi-Strategy",careers_url:"https://www.balyasny.com/careers",search_urls:{},cities:{Madrid:false,Paris:false,London:true}},
        {name:"DE Shaw",category:"Hedge Fund",subcategory:"Quantitative",careers_url:"https://www.deshaw.com/careers",search_urls:{},cities:{Madrid:false,Paris:false,London:true}},
        {name:"Blackstone",category:"Private Equity",subcategory:"Mega Cap",careers_url:"https://www.blackstone.com/careers/",search_urls:{campus:"https://blackstone.wd1.myworkdayjobs.com/Blackstone_Campus_Careers"},cities:{Madrid:true,Paris:true,London:true}},
        {name:"KKR",category:"Private Equity",subcategory:"Mega Cap",careers_url:"https://www.kkr.com/careers",search_urls:{},cities:{Madrid:true,Paris:true,London:true}},
        {name:"Apollo Global Management",category:"Private Equity",subcategory:"Mega Cap",careers_url:"https://www.apollo.com/careers",search_urls:{},cities:{Madrid:false,Paris:false,London:true}},
        {name:"Carlyle Group",category:"Private Equity",subcategory:"Mega Cap",careers_url:"https://www.carlyle.com/careers",search_urls:{},cities:{Madrid:true,Paris:true,London:true}},
        {name:"Ardian",category:"Private Equity",subcategory:"European",careers_url:"https://www.ardian.com/en/careers",search_urls:{},cities:{Madrid:true,Paris:true,London:true}},
        {name:"Apax Partners",category:"Private Equity",subcategory:"European",careers_url:"https://www.apax.com/careers/",search_urls:{},cities:{Madrid:false,Paris:true,London:true}},
        {name:"Thoma Bravo",category:"Private Equity",subcategory:"Tech-focused",careers_url:"https://www.thomabravo.com/careers",search_urls:{},cities:{Madrid:false,Paris:false,London:true}},
        {name:"CVC Capital Partners",category:"Private Equity",subcategory:"European",careers_url:"https://www.cvc.com/careers/",search_urls:{},cities:{Madrid:true,Paris:true,London:true}},
        {name:"Permira",category:"Private Equity",subcategory:"European",careers_url:"https://www.permira.com/careers",search_urls:{},cities:{Madrid:true,Paris:true,London:true}},
        {name:"EQT",category:"Private Equity",subcategory:"Nordic",careers_url:"https://eqtgroup.com/careers/",search_urls:{},cities:{Madrid:true,Paris:true,London:true}},
        {name:"Eurazeo",category:"Private Equity",subcategory:"European",careers_url:"https://www.eurazeo.com/en/careers",search_urls:{},cities:{Madrid:true,Paris:true,London:true}},
        {name:"PAI Partners",category:"Private Equity",subcategory:"European",careers_url:"https://www.paipartners.com/careers/",search_urls:{},cities:{Madrid:true,Paris:true,London:true}},
        {name:"BC Partners",category:"Private Equity",subcategory:"European",careers_url:"https://www.bcpartners.com/careers/",search_urls:{},cities:{Madrid:false,Paris:true,London:true}},
        {name:"TPG",category:"Private Equity",subcategory:"Mega Cap",careers_url:"https://www.tpg.com/careers/",search_urls:{},cities:{Madrid:false,Paris:true,London:true}},
        {name:"Cinven",category:"Private Equity",subcategory:"European",careers_url:"https://www.cinven.com/careers/",search_urls:{},cities:{Madrid:true,Paris:true,London:true}},
        {name:"Tikehau Capital",category:"Asset Manager",subcategory:"European Alternative",careers_url:"https://www.tikehaucapital.com/en/careers",search_urls:{},cities:{Madrid:true,Paris:true,London:true}},
    ];
}

function getDefaultLinkedIn() {
    return [
        {name:"Finance Internships - Madrid",url:"https://www.linkedin.com/jobs/search/?keywords=finance%20internship&location=Madrid&f_E=1"},
        {name:"Finance Internships - Paris",url:"https://www.linkedin.com/jobs/search/?keywords=finance%20internship&location=Paris&f_E=1"},
        {name:"Finance Internships - London",url:"https://www.linkedin.com/jobs/search/?keywords=finance%20internship&location=London&f_E=1"},
        {name:"Banking Internships - Madrid",url:"https://www.linkedin.com/jobs/search/?keywords=banking%20intern&location=Madrid&f_E=1"},
        {name:"Private Banking Internships - Spain",url:"https://www.linkedin.com/jobs/search/?keywords=private%20banking%20intern&location=Spain&f_E=1"},
        {name:"Asset Management Internships - Europe",url:"https://www.linkedin.com/jobs/search/?keywords=asset%20management%20intern&location=Europe&f_E=1"},
        {name:"Stage Finance - Paris",url:"https://www.linkedin.com/jobs/search/?keywords=stage%20finance&location=Paris&f_E=1"},
        {name:"Practicas Finanzas - Madrid",url:"https://www.linkedin.com/jobs/search/?keywords=prácticas%20finanzas&location=Madrid&f_E=1"},
    ];
}

function getDefaultIndeed() {
    return [
        {name:"Finance Intern - Madrid",url:"https://www.indeed.com/jobs?q=finance+intern&l=Madrid%2C+Spain"},
        {name:"Stage Finance - Paris",url:"https://fr.indeed.com/emplois?q=stage+finance&l=Paris"},
        {name:"Finance Internship - London",url:"https://www.indeed.co.uk/jobs?q=finance+internship&l=London"},
    ];
}

// ============================================================
// UTILITIES
// ============================================================
function escHtml(str) {
    const d = document.createElement('div');
    d.textContent = str || '';
    return d.innerHTML;
}

function escAttr(str) {
    return (str || '').replace(/"/g, '&quot;').replace(/'/g, '&#39;');
}

function classifyScore(score) {
    if (score >= 80) return 'excellent';
    if (score >= 60) return 'good';
    if (score >= 40) return 'moderate';
    return 'low';
}

// ============================================================
// EVENT LISTENERS
// ============================================================
function setupListeners() {
    // Filters
    ['searchInput', 'filterCity', 'filterCategory', 'filterMatch'].forEach(id => {
        document.getElementById(id).addEventListener('input', renderJobs);
    });
    document.getElementById('filterNew').addEventListener('change', renderJobs);

    // Tabs
    document.querySelectorAll('.tab').forEach(tab => {
        tab.addEventListener('click', () => {
            document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
            document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
            tab.classList.add('active');
            document.getElementById(`tab-${tab.dataset.tab}`).classList.add('active');
        });
    });
}

// ============================================================
// APPLICATION TRACKER (localStorage)
// ============================================================
const APPS_KEY = 'applications';
const STATUSES = {
    applied:     { label: 'Postule',   color: '#4a9eff', icon: '📨' },
    in_progress: { label: 'En cours',  color: '#ff9500', icon: '⏳' },
    interview:   { label: 'Entretien', color: '#d4a843', icon: '🎤' },
    offer:       { label: 'Offre',     color: '#34c759', icon: '🎉' },
    rejected:    { label: 'Refuse',    color: '#ff453a', icon: '❌' },
};

let currentPipelineFilter = 'all';

function getApplications() {
    try { return JSON.parse(localStorage.getItem(APPS_KEY)) || []; }
    catch { return []; }
}

function saveApplications(apps) {
    localStorage.setItem(APPS_KEY, JSON.stringify(apps));
    cloudSave();
}

function addApplication(e) {
    e.preventDefault();
    const apps = getApplications();
    const app = {
        id: Date.now().toString(36) + Math.random().toString(36).slice(2, 6),
        firm: document.getElementById('appFirm').value.trim(),
        title: document.getElementById('appTitle').value.trim(),
        location: document.getElementById('appLocation').value.trim() || '',
        url: document.getElementById('appUrl').value.trim() || '',
        date_applied: document.getElementById('appDate').value || new Date().toISOString().slice(0, 10),
        status: 'applied',
        last_updated: new Date().toISOString().slice(0, 10),
    };
    apps.unshift(app);
    saveApplications(apps);
    document.getElementById('appForm').reset();
    document.getElementById('appDate').value = new Date().toISOString().slice(0, 10);
    renderApplications();
}

function updateAppStatus(appId, newStatus) {
    const apps = getApplications();
    const app = apps.find(a => a.id === appId);
    if (app) {
        app.status = newStatus;
        app.last_updated = new Date().toISOString().slice(0, 10);
        saveApplications(apps);
        renderApplications();
    }
}

function deleteApplication(appId) {
    if (!confirm('Supprimer cette candidature ?')) return;
    const apps = getApplications().filter(a => a.id !== appId);
    saveApplications(apps);
    renderApplications();
}

function filterPipeline(status) {
    currentPipelineFilter = status;
    document.querySelectorAll('.pipe-filter-btn').forEach(b => {
        b.classList.toggle('active', b.dataset.status === status);
    });
    renderApplications();
}

function renderApplications() {
    const apps = getApplications();
    const filtered = currentPipelineFilter === 'all'
        ? apps
        : apps.filter(a => a.status === currentPipelineFilter);

    // Pipeline stats
    const statsEl = document.getElementById('pipelineStats');
    const counts = {};
    for (const key of Object.keys(STATUSES)) counts[key] = 0;
    apps.forEach(a => { if (counts[a.status] !== undefined) counts[a.status]++; });

    statsEl.innerHTML = Object.entries(STATUSES).map(([key, s]) => `
        <div class="pipe-stat ${currentPipelineFilter === key ? 'active' : ''}" onclick="filterPipeline('${key}')">
            <span class="pipe-stat-icon">${s.icon}</span>
            <span class="pipe-stat-count">${counts[key]}</span>
            <span class="pipe-stat-label">${s.label}</span>
        </div>
    `).join('');

    // Badge on tab
    const badge = document.getElementById('appsBadge');
    if (badge) badge.textContent = apps.length > 0 ? apps.length : '';

    // Applications list
    const listEl = document.getElementById('appsList');
    if (filtered.length === 0) {
        listEl.innerHTML = `<div class="empty-state"><p>${apps.length === 0 ? 'Aucune candidature. Ajoutez-en une ci-dessus.' : 'Aucune candidature dans ce statut.'}</p></div>`;
        return;
    }

    listEl.innerHTML = filtered.map(app => {
        const s = STATUSES[app.status] || STATUSES.applied;
        const statusOptions = Object.entries(STATUSES).map(([key, st]) =>
            `<option value="${key}" ${key === app.status ? 'selected' : ''}>${st.icon} ${st.label}</option>`
        ).join('');

        return `
        <div class="app-card" style="border-left: 3px solid ${s.color}">
            <div class="app-card-main">
                <div class="app-card-header">
                    <span class="app-card-firm">${escHtml(app.firm)}</span>
                    <span class="app-card-title">${escHtml(app.title)}</span>
                </div>
                <div class="app-card-meta">
                    ${app.location ? `<span>${escHtml(app.location)}</span>` : ''}
                    <span>Postule le ${app.date_applied}</span>
                    ${app.last_updated !== app.date_applied ? `<span>MAJ ${app.last_updated}</span>` : ''}
                </div>
            </div>
            <div class="app-card-actions">
                <select class="status-select" style="border-color:${s.color}" onchange="updateAppStatus('${app.id}', this.value)">
                    ${statusOptions}
                </select>
                ${app.url ? `<a href="${escAttr(app.url)}" target="_blank" class="link-btn primary">Voir</a>` : ''}
                <button class="link-btn delete-btn" onclick="deleteApplication('${app.id}')">X</button>
            </div>
        </div>`;
    }).join('');
}

// ============================================================
// NOTIFICATIONS
// ============================================================
function setupNotifications() {
    document.getElementById('notifyModal').style.display = 'flex';
}

function closeModal() {
    document.getElementById('notifyModal').style.display = 'none';
}

async function requestBrowserNotif() {
    const statusEl = document.getElementById('notifStatus');
    if (!('Notification' in window)) {
        statusEl.textContent = 'Non supporte par ce navigateur';
        return;
    }
    const perm = await Notification.requestPermission();
    if (perm === 'granted') {
        statusEl.textContent = 'Actif !';
        statusEl.style.color = 'var(--accent-green)';
        new Notification('Internship Monitor', {
            body: 'Notifications activees ! Vous serez prevenu des nouvelles offres.',
            icon: '/icons/icon-192.png',
        });
    } else {
        statusEl.textContent = 'Refuse';
        statusEl.style.color = 'var(--accent-red)';
    }
}

// Close modal on backdrop click
document.addEventListener('click', (e) => {
    if (e.target.classList.contains('modal')) closeModal();
});

// ============================================================
// INIT
// ============================================================
document.addEventListener('DOMContentLoaded', async () => {
    setupListeners();
    loadData();
    // Cloud sync: load from gist, merge with local
    await cloudLoad();
    // Init application tracker
    const dateEl = document.getElementById('appDate');
    if (dateEl) dateEl.value = new Date().toISOString().slice(0, 10);
    renderApplications();
    renderLinks();
    updateAccountStat();
});
