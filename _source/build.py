"""Assembles the static site into ../iwd-website (GitHub Pages ready)."""
import pathlib, shutil, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import insights

ROOT = pathlib.Path(__file__).parent
OUT = ROOT.parent / "_build"
SITE_URL = "https://www.intelligencewithdata.com/"
EMAIL = "training@intelligencewithdata.com"
PHONE = "+44 7344 099 129"
WA = "https://wa.me/447344099129"

ARROW = '<svg viewBox="0 0 20 20" fill="none" aria-hidden="true"><path d="M4 10h11m-4-5 5 5-5 5" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>'

def ic(path):
    return f'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{path}</svg>'

I = {
    "auto": ic('<path d="M21 12a9 9 0 1 1-3-6.7"/><path d="M21 4v5h-5"/><path d="M8 13l2.5 2.5L16 10"/>'),
    "layers": ic('<path d="m12 3 9 5-9 5-9-5 9-5Z"/><path d="m3 13 9 5 9-5"/>'),
    "people": ic('<circle cx="9" cy="8" r="3.2"/><path d="M3 20a6 6 0 0 1 12 0"/><circle cx="17" cy="9" r="2.5"/><path d="M15.5 14.2A5 5 0 0 1 21 19"/>'),
    "spark": ic('<path d="M12 3v4M12 17v4M3 12h4M17 12h4M6 6l2.5 2.5M15.5 15.5 18 18M6 18l2.5-2.5M15.5 8.5 18 6"/>'),
    "brief": ic('<rect x="3" y="7" width="18" height="13" rx="2"/><path d="M9 7V5a2 2 0 0 1 2-2h2a2 2 0 0 1 2 2v2M3 13h18"/>'),
    "check": ic('<path d="m5 12 4.5 4.5L19 7"/>'),
    "user": ic('<circle cx="12" cy="8" r="4"/><path d="M4 21a8 8 0 0 1 16 0"/>'),
    "flag": ic('<path d="M5 21V4M5 4h11l-2 4 2 4H5"/>'),
    "mic": ic('<rect x="9" y="3" width="6" height="11" rx="3"/><path d="M5 11a7 7 0 0 0 14 0M12 18v3"/>'),
    "chat": ic('<path d="M21 12a8 8 0 0 1-11.6 7.1L4 20l1-4.6A8 8 0 1 1 21 12Z"/>'),
    "kid": ic('<rect x="4" y="5" width="16" height="11" rx="2"/><path d="M8 20h8M12 16v4M9 10l-1.5 1.5L9 13M15 10l1.5 1.5L15 13"/>'),
    "mail": ic('<rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 7 9 6 9-6"/>'),
    "phone": ic('<path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2Z"/>'),
    "globe": ic('<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3a14 14 0 0 1 0 18M12 3a14 14 0 0 0 0 18"/>'),
    "refresh": ic('<path d="M20 11a8 8 0 0 0-14.9-3M4 4v4h4M4 13a8 8 0 0 0 14.9 3M20 20v-4h-4"/>'),
}

LOGO = '''<svg class="brand-mark" viewBox="0 0 40 40" aria-hidden="true"><rect width="40" height="40" rx="11" fill="#142B5E"/><rect x="9" y="22" width="5.5" height="9" rx="1.6" fill="#5B8CFF"/><rect x="17.25" y="15" width="5.5" height="16" rx="1.6" fill="#BFD0FF"/><rect x="25.5" y="8.5" width="5.5" height="22.5" rx="1.6" fill="#C9A227"/></svg>'''

NAV = [("index.html", "Home"), ("services.html", "Consulting"), ("training.html", "Training"), ("free-training.html", "Free Fridays"), ("about.html", "About")]
LUMA = "https://luma.com/aifip615"

def header(active):
    cur = ' aria-current="page"'
    act = "insights.html" if active.startswith("insights-") else active
    links = "".join(f'<a href="{h}"{cur if h == act else ""}>{t}</a>' for h, t in NAV)
    promo_inner = '<span class="topbar-tag"><span class="promo-long">Power BI &middot; Microsoft Fabric &middot; </span>Data consultancy &amp; training &middot; UK</span>' if active == "free-training.html" else f'<a class="promo-bar" href="free-training.html"><span class="promo-dot" aria-hidden="true"></span><span><strong>Free live training</strong><span class="promo-long"> &middot; Power BI &amp; SQL every Friday, 6pm UK</span></span><span class="promo-cta"><span class="promo-cta-text">Save your seat</span> {ARROW}</span></a>'
    promo = f'''<div class="topbar"><div class="container topbar-inner"><span class="topbar-spacer" aria-hidden="true"></span>{promo_inner}<a class="topbar-staff" href="staff.html"{' aria-current="page"' if active == "staff.html" else ''}>{I["user"]}<span>Staff login</span></a></div></div>'''
    return f'''<a class="skip-link" href="#main">Skip to content</a>
{promo}
<header class="site-header" data-header>
  <div class="container nav">
    <a class="brand" href="index.html" aria-label="Intelligence With Data — home">{LOGO}<span class="brand-text"><strong>Intelligence With Data</strong><small>Strategy and Mastery</small></span></a>
    <button class="nav-toggle" aria-expanded="false" aria-controls="nav-menu" data-nav-toggle><span></span><span></span><span></span><span class="sr-only">Menu</span></button>
    <nav id="nav-menu" class="nav-menu" data-nav-menu aria-label="Main">{links}<a class="btn btn--gold btn--sm" href="contact.html">Book a call</a></nav>
  </div>
</header>'''

FOOTER = f'''<footer class="site-footer">
  <div class="container">
    <div class="footer-grid">
      <div class="footer-about">
        <a class="brand" href="index.html">{LOGO}<span class="brand-text"><strong>Intelligence With Data</strong><small>Strategy and Mastery</small></span></a>
        <p>A UK data consultancy automating reporting with Power BI and Microsoft Fabric, and upskilling the people who use it.</p>
      </div>
      <div><h4>Consulting</h4><ul>
        <li><a href="services.html#automation">Report automation</a></li>
        <li><a href="services.html#fabric">Microsoft Fabric</a></li>
        <li><a href="services.html#upskilling">Team upskilling</a></li>
        <li><a href="services.html#ai">AI &amp; prompting</a></li>
        <li><a href="services.html#contract">Contract support</a></li></ul></div>
      <div><h4>Company</h4><ul>
        <li><a href="training.html">Training &amp; careers</a></li>
        <li><a href="free-training.html">Free Friday training</a></li>
        <li><a href="about.html">About us</a></li>
        <li><a href="insights.html">Insights</a></li>
        <li><a href="careers.html">Careers</a></li>
        <li><a href="contact.html">Contact</a></li></ul></div>
      <div><h4>Get in touch</h4><ul>
        <li><a href="mailto:{EMAIL}">{EMAIL}</a></li>
        <li><a href="tel:+447344099129">{PHONE}</a></li>
        <li><a href="{WA}" target="_blank" rel="noopener">WhatsApp us</a></li></ul></div>
    </div>
    <div class="footer-bottom">
      <span>&copy; <span data-year>2026</span> Intelligence With Data Ltd. All rights reserved.</span>
      <span>Microsoft Certified Professional &middot; BCS member &middot; <a href="staff.html" class="staff-link">Staff email</a></span>
    </div>
  </div>
</footer>'''

def cta(title="Ready to get your hours back?", text="Tell us which reports eat your week. In one conversation we'll show you what can be automated and what it's worth."):
    return f'''<section class="cta-band"><div class="container"><div class="cta-inner reveal">
  <div><p class="eyebrow eyebrow--gold">Let's talk</p><h2>{title}</h2><p>{text}</p></div>
  <div class="cta-actions"><a class="btn btn--gold" href="contact.html">Book a discovery call {ARROW}</a><a class="btn btn--ghost" href="{WA}" target="_blank" rel="noopener">Message us on WhatsApp</a></div>
</div></div></section>'''

import hashlib
VER = hashlib.md5((ROOT / "assets/css/styles.css").read_bytes() + (ROOT / "assets/js/main.js").read_bytes()).hexdigest()[:8]

def page(file, title, desc, body):
    return f'''<!doctype html>
<html lang="en-GB" class="no-js">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="theme-color" content="#0B1B3F">{'<meta name="robots" content="noindex">' if file in NOINDEX else ''}
<link rel="canonical" href="{SITE_URL}{'' if file == 'index.html' else file}">
<meta property="og:type" content="website">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{SITE_URL}{'' if file == 'index.html' else file}">
<meta property="og:site_name" content="Intelligence With Data">
<meta property="og:image" content="{SITE_URL}assets/img/{'og-free-training.png' if file == 'free-training.html' else ('og-' + file[:-5] + '.png' if file.startswith('insights-') else 'og-default.png')}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="assets/img/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,500;0,9..144,600;1,9..144,500&family=Manrope:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/css/styles.css?v={VER}">
</head>
<body{' class="free-page"' if file == "free-training.html" else ""}>
{header(file)}
<main id="main">
{body}
</main>
{FOOTER}
<script src="assets/js/main.js?v={VER}" defer></script>
</body>
</html>
'''

# ------------------------------------------------------------------ HOME
bars = "".join(f'<span style="--h:{h}%;--i:{i}"></span>' for i, h in enumerate([38, 52, 45, 64, 58, 72, 66, 80, 74, 88, 82, 96]))
HOME = f'''
<section class="hero">
  <div class="grid-bg" aria-hidden="true"></div>
  <div class="container hero-grid">
    <div class="hero-copy">
      <p class="eyebrow eyebrow--gold">Power BI &middot; Microsoft Fabric &middot; AI upskilling</p>
      <h1>Stop rebuilding the same reports. <em>Let them run themselves.</em></h1>
      <p class="lead">Intelligence With Data is a UK data consultancy. We automate your reporting with Power BI and Microsoft Fabric, then upskill your team so the hours you save stay saved.</p>
      <div class="btn-row">
        <a class="btn btn--gold" href="contact.html">Book a discovery call {ARROW}</a>
        <a class="btn btn--ghost" href="services.html">Explore consulting</a>
      </div>
      <ul class="trust"><li>Microsoft Certified Professional</li><li>BCS member</li><li>UK-based &amp; contract-ready</li></ul>
    </div>
    <div class="hero-visual" aria-hidden="true">
      <div class="dash">
        <div class="dash-top"><span class="dot"></span><span class="dot"></span><span class="dot"></span><span class="dash-title">Monthly performance</span><span class="dash-live">&#9679; Live</span></div>
        <div class="kpis">
          <div class="kpi"><span>Revenue</span><strong>&pound;1.28m</strong><em class="up">&#9650; 8.4%</em></div>
          <div class="kpi"><span>Collected</span><strong>92.1%</strong><em class="up">&#9650; 2.3%</em></div>
          <div class="kpi"><span>Open cases</span><strong>3,412</strong><em class="down">&#9660; 5.1%</em></div>
        </div>
        <div class="chart"><svg viewBox="0 0 320 120" preserveAspectRatio="none"><defs><linearGradient id="ga" x1="0" x2="0" y1="0" y2="1"><stop offset="0" stop-color="#2563EB" stop-opacity=".28"/><stop offset="1" stop-color="#2563EB" stop-opacity="0"/></linearGradient></defs><path d="M0,95 C30,88 50,70 80,74 S130,52 160,56 S210,30 240,36 S290,14 320,18 L320,120 L0,120Z" fill="url(#ga)"/><path class="line" d="M0,95 C30,88 50,70 80,74 S130,52 160,56 S210,30 240,36 S290,14 320,18" fill="none" stroke="#2563EB" stroke-width="2.5"/></svg></div>
        <div class="bars">{bars}</div>
      </div>
      <div class="float-badge float-badge--a"><span class="badge-icon">{I["refresh"]}</span><div><strong>Refreshed at 06:00</strong><small>No manual steps</small></div></div>
      <div class="float-badge float-badge--b"><strong>14 hrs</strong><small>back this week</small></div>
    </div>
  </div>
</section>

<section class="section section--tint">
  <div class="container">
    <div class="section-head reveal"><p class="eyebrow">Sound familiar?</p><h2>Your analysts are busy. <em>Mostly copying and pasting.</em></h2></div>
    <div class="pains">
      <div class="pain reveal"><div class="pain-num">01</div><h3>The Monday-morning scramble</h3><p>Exports, VLOOKUPs and manual fixes every week, just to produce a report that looks like last week's.</p></div>
      <div class="pain reveal" style="--d:.1s"><div class="pain-num">02</div><h3>Numbers that don't agree</h3><p>Finance, operations and leadership each have their own spreadsheet — and their own version of the truth.</p></div>
      <div class="pain reveal" style="--d:.2s"><div class="pain-num">03</div><h3>Tools nobody fully uses</h3><p>You pay for Power BI and Microsoft 365, yet your team still falls back on Excel because no one was shown how.</p></div>
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="section-head reveal"><p class="eyebrow">What we do</p><h2>Automate the work. <em>Upskill the people.</em></h2><p class="lead">Technology alone doesn't stick. Every engagement pairs a working solution with the skills your team needs to own it.</p></div>
    <div class="cards">
      <a class="card reveal" href="services.html#automation"><div class="icon">{I["auto"]}</div><h3>Report automation</h3><p>We rebuild your recurring reports in Power BI with clean data models and scheduled refresh, so they update themselves.</p><span class="link">Learn more {ARROW}</span></a>
      <a class="card reveal" href="services.html#fabric" style="--d:.1s"><div class="icon">{I["layers"]}</div><h3>Microsoft Fabric foundations</h3><p>One governed home for your data — pipelines, lakehouse and semantic models that every report can trust.</p><span class="link">Learn more {ARROW}</span></a>
      <a class="card reveal" href="services.html#upskilling"><div class="icon icon--gold">{I["people"]}</div><h3>Team upskilling</h3><p>Practical Excel, SQL and Power BI training built around your own data, so skills transfer straight into daily work.</p><span class="link">Learn more {ARROW}</span></a>
      <a class="card reveal" href="services.html#ai" style="--d:.1s"><div class="icon icon--gold">{I["spark"]}</div><h3>AI &amp; prompt engineering</h3><p>Teach your people to use AI assistants safely and well, with prompt techniques that solve real analysis tasks.</p><span class="link">Learn more {ARROW}</span></a>
    </div>
  </div>
</section>

<section class="section section--navy">
  <div class="container">
    <div class="section-head center reveal"><p class="eyebrow eyebrow--gold">How we work</p><h2>From manual to automatic <em>in four steps.</em></h2></div>
    <div class="process">
      <div class="step reveal"><div class="step-num">1</div><h3>Discover</h3><p>We map your reports, data sources and the hours each one costs.</p></div>
      <div class="step reveal" style="--d:.1s"><div class="step-num">2</div><h3>Design</h3><p>A clear roadmap: what to automate first, the data model, and the quick wins.</p></div>
      <div class="step reveal" style="--d:.2s"><div class="step-num">3</div><h3>Automate</h3><p>We build in Power BI and Fabric, test with your team, and switch on refresh.</p></div>
      <div class="step reveal" style="--d:.3s"><div class="step-num">4</div><h3>Upskill</h3><p>Hands-on training and documentation so your people own it from day one.</p></div>
    </div>
  </div>
</section>

<section class="section section--navy" style="padding-top:0">
  <div class="container">
    <div class="section-head reveal"><p class="eyebrow eyebrow--gold">What's it worth?</p><h2>See how much time <em>manual reporting costs you.</em></h2><p class="lead" style="color:#A9B5D1">Move the sliders to match your team. The numbers update instantly.</p></div>
    <div class="calc reveal" data-calc>
      <div class="calc-inputs">
        <label class="field-range"><span>Reports built manually <output data-out="reports">8</output></span><input type="range" name="reports" min="1" max="40" step="1" value="8"></label>
        <label class="field-range"><span>Hours to produce each one <output data-out="hours">2 hrs</output></span><input type="range" name="hours" min="0.5" max="10" step="0.5" value="2"></label>
        <label class="field-range"><span>Times each is produced per month <output data-out="runs">4</output></span><input type="range" name="runs" min="1" max="22" step="1" value="4"></label>
        <label class="field-range"><span>Hourly cost of the person doing it <output data-out="rate">&pound;35</output></span><input type="range" name="rate" min="15" max="120" step="5" value="35"></label>
      </div>
      <div class="calc-results" aria-live="polite">
        <div><span>Hours on manual reporting / year</span><strong data-result="current">768</strong></div>
        <div class="hl"><span>Hours you could get back</span><strong data-result="saved">614</strong></div>
        <div><span>Estimated annual value</span><strong data-result="value">&pound;21,504</strong></div>
        <p class="fine">Illustrative estimate assuming automation removes around 80% of the manual effort. We'll give you a real figure after a discovery call.</p>
      </div>
    </div>
  </div>
</section>

<section class="section">
  <div class="container split split--center">
    <div class="reveal">
      <p class="eyebrow">Why Intelligence With Data</p>
      <h2>Practitioners, <em>not slide-deck consultants.</em></h2>
      <ul class="why-list">
        <li><span class="tick">{I["check"]}</span><div><h3>We do this work every day</h3><p>Our founder is a working Senior Data Analyst, so our builds are shaped by real reporting pressure, not theory.</p></div></li>
        <li><span class="tick">{I["check"]}</span><div><h3>Microsoft stack specialists</h3><p>Power BI, Fabric, Excel and SQL — deep in the tools you already own, so no expensive platform switch.</p></div></li>
        <li><span class="tick">{I["check"]}</span><div><h3>Knowledge transfer built in</h3><p>We train as we build. When we leave, your team can maintain and extend everything we delivered.</p></div></li>
        <li><span class="tick">{I["check"]}</span><div><h3>Clear scope, clear deliverables</h3><p>Every stage ends with something tangible you can see, use and sign off.</p></div></li>
      </ul>
    </div>
    <div class="quote-panel reveal" style="--d:.15s">
      <p class="big">The goal isn't a prettier dashboard. It's giving people their week back — and the confidence to do more with data.</p>
      <div class="who"><span class="avatar">HF</span><div><strong>Hakeem Falade</strong><small>Founder, Intelligence With Data</small></div></div>
    </div>
  </div>
</section>

<section class="section section--tint">
  <div class="container split split--center">
    <div class="reveal">
      <p class="eyebrow">Training &amp; careers</p>
      <h2>We also build <em>the next generation of analysts.</em></h2>
      <p class="lead">Alongside consulting, we run 1:1 coaching, a simulated data analytics internship, bootcamps and a Saturday tech class for children — for learners across the UK, Canada and Europe.</p>
      <div class="btn-row"><a class="btn btn--navy" href="training.html">Explore training {ARROW}</a></div>
    </div>
    <div class="cards reveal" style="--d:.1s">
      <div class="card"><span class="tag tag--gold">Individuals</span><h3>1:1 coaching</h3><p style="margin:0">Excel, SQL and Power BI at your pace.</p></div>
      <div class="card"><span class="tag">Career-switchers</span><h3>Simulated internship</h3><p style="margin:0">Six weeks of real-world style projects.</p></div>
    </div>
  </div>
</section>
''' + cta()

# ------------------------------------------------------------------ SERVICES
def feature(id_, tag, title, copy, items, outcome, icon, gold=False):
    lis = "".join(f"<li>{a}<small>{b}</small></li>" for a, b in items)
    return f'''<div class="feature" id="{id_}">
  <div class="feature-copy reveal"><div class="icon{' icon--gold' if gold else ''}">{I[icon]}</div><span class="tag{' tag--gold' if gold else ''}">{tag}</span><h2>{title}</h2>{copy}</div>
  <div class="deliverables reveal" style="--d:.1s"><h4>What you get</h4><ul class="check-list">{lis}</ul><p class="outcome"><strong>The outcome:</strong> {outcome}</p></div>
</div>'''

SERVICES = f'''
<section class="page-hero">
  <div class="grid-bg" aria-hidden="true"></div>
  <div class="container">
    <p class="crumbs"><a href="index.html">Home</a> &nbsp;/&nbsp; Consulting</p>
    <p class="eyebrow eyebrow--gold">Consulting</p>
    <h1>Data consulting that <em>pays for itself in hours.</em></h1>
    <p class="lead">Power BI and Microsoft Fabric specialists helping UK businesses automate repetitive reporting, build trusted data foundations and upskill their teams.</p>
    <nav class="pill-nav" aria-label="Services"><a href="#automation">Report automation</a><a href="#fabric">Microsoft Fabric</a><a href="#upskilling">Team upskilling</a><a href="#ai">AI &amp; prompting</a><a href="#contract">Contract support</a></nav>
  </div>
</section>

<section class="section"><div class="container">
''' + feature("automation", "Power BI", "Report automation",
    "<p>If someone on your team spends hours every week rebuilding the same spreadsheets, that is time you can get back. We audit your recurring reports, connect Power BI directly to your sources and rebuild them on a solid data model, so they refresh on a schedule with no manual steps.</p><p>From finance packs to operational KPIs and collections performance, we design reports people actually use.</p>",
    [("Reporting audit &amp; automation roadmap", "Every report listed, costed in hours and prioritised"), ("Star-schema data model &amp; DAX measures", "Fast, consistent numbers across every report"), ("Interactive Power BI reports", "Designed for decisions, with drill-through and filters"), ("Scheduled refresh &amp; secure sharing", "Set up in the Power BI Service with the right access"), ("Documentation &amp; handover session", "So your team can maintain and extend it")],
    "the reports your business relies on, delivered on time, every time — without anyone touching a spreadsheet.", "auto") + \
  feature("fabric", "Microsoft Fabric", "Microsoft Fabric data foundations",
    "<p>When data lives in a dozen systems and spreadsheets, every report becomes a reconciliation exercise. We use Microsoft Fabric to bring it together in one governed place: pipelines that load data automatically, a lakehouse or warehouse to store it, and shared semantic models that every report builds on.</p>",
    [("Architecture design", "Sized for your data, team and Microsoft licensing"), ("Data pipelines &amp; Dataflows Gen2", "Automated ingestion from your source systems"), ("Lakehouse or warehouse build", "Clean, modelled, query-ready data"), ("Shared semantic models", "One definition of every KPI, reused everywhere"), ("Governance &amp; access setup", "Workspaces, roles and refresh monitoring")],
    "a single source of truth that ends the arguments about whose numbers are right.", "layers") + \
  feature("upskilling", "Training for teams", "Team upskilling in Excel, SQL &amp; Power BI",
    "<p>Most teams use a fraction of what their tools can do. Our training is hands-on and built around your own data and reports, so people practise on work they recognise and apply it the next morning. We start with a skills assessment and tailor the programme to each level.</p>",
    [("Skills assessment", "A clear picture of where each person is today"), ("Tailored curriculum", "Excel, SQL, Power BI or a combined pathway"), ("Live, hands-on sessions", "Remote or on-site across the UK"), ("Workbooks &amp; practice files", "Built on scenarios from your business"), ("Post-training support", "Follow-up clinics to embed new habits")],
    "a team that can answer its own questions, build its own reports and stop waiting on one overstretched analyst.", "people", True) + \
  feature("ai", "AI enablement", "AI &amp; prompt engineering for teams",
    "<p>AI assistants can draft formulas, explain data, write SQL and summarise findings in seconds — when people know how to ask. We teach practical, responsible use of tools such as Microsoft Copilot, ChatGPT and Claude, with prompt techniques matched to everyday analysis and admin tasks.</p>",
    [("AI awareness workshop", "What AI is good at, where it fails, and how to check it"), ("Prompt engineering masterclass", "Proven structures for reliable, repeatable results"), ("Role-specific prompt library", "Ready-to-use prompts for your team's real tasks"), ("Responsible-use guidelines", "Practical rules on data privacy and verification")],
    "people who use AI confidently to work faster, without putting your data or reputation at risk.", "spark", True) + \
  feature("contract", "UK contracts", "Contract analytics support",
    "<p>Need extra capacity for a migration, a reporting backlog or a new dashboard suite? We work with UK companies on a contract basis as Power BI developers and data analysts, slotting into your team and ways of working, remotely or on-site.</p>",
    [("Power BI development", "Reports, models, DAX and Service administration"), ("Data analysis &amp; insight", "Ad-hoc analysis, KPI design and business reviews"), ("Excel to Power BI migration", "Move legacy spreadsheet reporting onto a modern stack"), ("Flexible terms", "Day-rate or fixed-scope engagements")],
    "experienced hands that deliver from week one, without the cost and delay of a permanent hire.", "brief") + '''
</div></section>

<section class="section section--tint">
  <div class="container">
    <div class="section-head center reveal"><p class="eyebrow">Ways to work with us</p><h2>Choose the model <em>that fits.</em></h2></div>
    <div class="cards cards--3">
      <div class="card model reveal"><span class="tag">Project</span><h3>Fixed-scope project</h3><p>A defined outcome — for example, automating your monthly management pack — with agreed deliverables and a fixed price.</p></div>
      <div class="card model reveal" style="--d:.1s"><span class="tag tag--gold">Contract</span><h3>Contract support</h3><p>Day-rate capacity for UK businesses that need an experienced Power BI developer or analyst embedded in their team.</p></div>
      <div class="card model reveal" style="--d:.2s"><span class="tag">Training</span><h3>Workshops &amp; programmes</h3><p>One-off workshops or multi-week programmes in Excel, SQL, Power BI and AI, delivered live to your team.</p></div>
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="section-head center reveal"><p class="eyebrow">Questions</p><h2>Frequently asked</h2></div>
    <div class="faq reveal">
      <details><summary>Do we need Microsoft Fabric, or is Power BI enough?</summary><p>Many businesses get large gains from Power BI alone. Fabric makes sense when you have several data sources, larger volumes, or want a governed central store. We'll recommend the simplest option that meets your needs during discovery.</p></details>
      <details><summary>How long does a typical automation project take?</summary><p>It depends on the number of reports and data sources. A focused project automating a handful of core reports often takes a few weeks; we'll give you a timeline with the roadmap.</p></details>
      <details><summary>Can you work with our existing data and systems?</summary><p>Yes. Power BI connects to most databases, cloud apps, SharePoint and Excel files. We work with what you have and only suggest changes where they clearly pay off.</p></details>
      <details><summary>Is training delivered remotely or on-site?</summary><p>Both. Most sessions run live online, and we can deliver on-site for teams in the UK.</p></details>
      <details><summary>How do you handle data security?</summary><p>We work inside your own Microsoft environment with the access you grant, follow UK GDPR principles, and avoid copying data outside your systems.</p></details>
    </div>
  </div>
</section>
''' + cta()

# ------------------------------------------------------------------ TRAINING
TRAINING = f'''
<section class="page-hero">
  <div class="grid-bg" aria-hidden="true"></div>
  <div class="container">
    <p class="crumbs"><a href="index.html">Home</a> &nbsp;/&nbsp; Training</p>
    <p class="eyebrow eyebrow--gold">Training &amp; careers</p>
    <h1>Learn data skills <em>the way they're used at work.</em></h1>
    <p class="lead">Coaching, internships and programmes for career-switchers and professionals across the UK, Canada and Europe — and a Saturday tech class for children.</p>
    <div class="btn-row"><a class="btn btn--gold" href="{WA}" target="_blank" rel="noopener">Chat on WhatsApp {ARROW}</a><a class="btn btn--ghost" href="contact.html">Send an enquiry</a></div>
  </div>
</section>

<section class="section" style="padding-bottom:0">
  <div class="container">
    <a class="free-feature reveal" href="free-training.html">
      <div class="free-feature-copy">
        <span class="live-chip"><span class="promo-dot"></span>Free &middot; Live every Friday</span>
        <h2>Power BI &amp; SQL Fridays</h2>
        <p>A free, live online class every Friday at 6pm UK time. Learn Power BI and SQL hands-on, ask questions, and build skills employers look for.</p>
        <span class="btn btn--gold">See what you'll learn {ARROW}</span>
      </div>
      <div class="free-feature-when" aria-hidden="true">
        <div class="cal"><span>Every</span><strong>FRI</strong><em>6:00 PM UK</em></div>
      </div>
    </a>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="section-head reveal"><p class="eyebrow">Programmes</p><h2>Find the right <em>starting point.</em></h2></div>
    <div class="cards cards--3">
      <div class="card reveal"><div class="icon">{I["user"]}</div><span class="tag">1:1</span><h3>1:1 coaching</h3><p>Personal programmes in Excel, SQL and Power BI, from beginner to advanced, shaped around your goals and schedule.</p></div>
      <div class="card reveal" style="--d:.1s"><div class="icon icon--gold">{I["flag"]}</div><span class="tag tag--gold">6 weeks</span><h3>Simulated data analytics internship</h3><p>Work on realistic client projects with simulated managers and stakeholders, and finish with portfolio pieces you can talk about in interviews.</p></div>
      <div class="card reveal" style="--d:.2s"><div class="icon">{I["mic"]}</div><span class="tag">Group</span><h3>Bootcamps &amp; webinars</h3><p>Structured group learning for career-switchers who want a guided route into a data analyst role.</p></div>
      <div class="card reveal"><div class="icon icon--gold">{I["chat"]}</div><span class="tag tag--gold">Weekly</span><h3>The Analytics Hub</h3><p>A weekly 30-minute group mentorship session to keep learners accountable, unblocked and moving forward.</p></div>
      <div class="card reveal" style="--d:.1s"><div class="icon">{I["kid"]}</div><span class="tag">Saturdays</span><h3>Kids in Tech</h3><p>A Saturday-morning technology class that gives children a confident, creative start with computers and digital skills.</p></div>
      <div class="card reveal" style="--d:.2s"><div class="icon icon--gold">{I["people"]}</div><span class="tag tag--gold">Teams</span><h3>Corporate training</h3><p>Upskilling for whole teams, built around your own data. <a href="services.html#upskilling" style="color:var(--blue);font-weight:700">See consulting &rarr;</a></p></div>
    </div>
  </div>
</section>

<section class="section section--navy">
  <div class="container">
    <div class="section-head center reveal"><p class="eyebrow eyebrow--gold">Your pathway</p><h2>From first lesson <em>to first data role.</em></h2></div>
    <div class="process">
      <div class="step reveal"><div class="step-num">1</div><h3>Assess</h3><p>We check your current level and agree a realistic goal.</p></div>
      <div class="step reveal" style="--d:.1s"><div class="step-num">2</div><h3>Learn</h3><p>Excel, SQL and Power BI taught through real business scenarios.</p></div>
      <div class="step reveal" style="--d:.2s"><div class="step-num">3</div><h3>Build</h3><p>Internship-style projects that become your portfolio.</p></div>
      <div class="step reveal" style="--d:.3s"><div class="step-num">4</div><h3>Launch</h3><p>CV, interview practice and mentoring as you apply.</p></div>
    </div>
  </div>
</section>

<section class="section">
  <div class="container split split--center">
    <div class="reveal">
      <p class="eyebrow">Taught by a practitioner</p>
      <h2>Learn from someone <em>who made the switch.</em></h2>
      <p class="lead">Our founder moved from oil and gas engineering into a UK data analyst role within six months of arriving, self-taught in Excel, Power BI and SQL. Every programme is built on that same practical route.</p>
      <div class="btn-row"><a class="btn btn--navy" href="about.html">Read the story {ARROW}</a></div>
    </div>
    <div class="deliverables reveal" style="--d:.1s"><h4>Every learner gets</h4><ul class="check-list">
      <li>A personalised learning plan<small>Matched to your starting level and target role</small></li>
      <li>Real-world projects<small>Scenarios drawn from day-to-day analyst work</small></li>
      <li>Portfolio-ready deliverables<small>Dashboards and reports you can show employers</small></li>
      <li>Ongoing mentorship<small>Support while you learn and while you apply</small></li></ul></div>
  </div>
</section>
''' + cta("Ready to start your data career?", "Tell us where you are today and where you want to be. We'll recommend the right programme.")

# ------------------------------------------------------------------ ABOUT
ABOUT = f'''
<section class="page-hero">
  <div class="grid-bg" aria-hidden="true"></div>
  <div class="container">
    <p class="crumbs"><a href="index.html">Home</a> &nbsp;/&nbsp; About</p>
    <p class="eyebrow eyebrow--gold">About us</p>
    <h1>Strategy and mastery, <em>built from experience.</em></h1>
    <p class="lead">Intelligence With Data helps organisations get more from their data and helps people build careers in it. Both start from the same belief: the right skills turn data from a chore into an advantage.</p>
  </div>
</section>

<section class="section">
  <div class="container split">
    <div class="reveal">
      <p class="eyebrow">Our story</p>
      <h2>From engineering <em>to data.</em></h2>
      <p>Intelligence With Data was founded by Hakeem Falade, a Senior Data Analyst, Microsoft Certified Professional and member of BCS, The Chartered Institute for IT.</p>
      <p>Hakeem began his career as an Asset Production Engineer across oil production facilities in Nigeria. After relocating to the UK, he took on whatever work was available while teaching himself Excel, Power BI and SQL — and landed a UK data analyst role within six months.</p>
      <p>That journey shapes everything we do: practical, outcome-focused work that helps businesses save time, and training that gives people a real route into data.</p>
    </div>
    <ol class="timeline reveal" style="--d:.1s">
      <li><span class="when">Chapter one</span><h3>Asset Production Engineer</h3><p>Operational and production data across oil facilities in Nigeria.</p></li>
      <li><span class="when">The move</span><h3>Relocating to the UK</h3><p>Survival jobs by day, self-teaching Excel, Power BI and SQL by night.</p></li>
      <li><span class="when">Within six months</span><h3>UK Data Analyst</h3><p>Into analytics, building reporting that teams depend on.</p></li>
      <li><span class="when">Today</span><h3>Intelligence With Data</h3><p>Consulting, training and mentoring — helping others make the same leap.</p></li>
    </ol>
  </div>
</section>

<section class="section section--navy">
  <div class="container">
    <div class="section-head reveal"><p class="eyebrow eyebrow--gold">Credentials</p><h2>Qualified, practising, <em>accountable.</em></h2></div>
    <div class="creds">
      <div class="cred reveal"><strong>Senior Data Analyst</strong><span>Working in industry, not just teaching it</span></div>
      <div class="cred reveal" style="--d:.1s"><strong>Microsoft Certified</strong><span>Professional certification on the Microsoft stack</span></div>
      <div class="cred reveal" style="--d:.2s"><strong>BCS member</strong><span>The Chartered Institute for IT</span></div>
      <div class="cred reveal" style="--d:.3s"><strong>UK-based</strong><span>Serving clients and learners in the UK, Canada &amp; Europe</span></div>
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="section-head center reveal"><p class="eyebrow">What we stand for</p><h2>Our <em>principles.</em></h2></div>
    <div class="cards cards--3">
      <div class="card reveal"><div class="icon">{I["auto"]}</div><h3>Time is the metric</h3><p>We measure success in hours given back and decisions made faster, not in dashboards delivered.</p></div>
      <div class="card reveal" style="--d:.1s"><div class="icon icon--gold">{I["people"]}</div><h3>Leave people stronger</h3><p>Every engagement transfers skills, so you're never dependent on us to keep things running.</p></div>
      <div class="card reveal" style="--d:.2s"><div class="icon">{I["check"]}</div><h3>Clarity at every stage</h3><p>Plain English, agreed scope and explicit deliverables from discovery to handover.</p></div>
    </div>
  </div>
</section>
''' + cta("Let's build something useful together.", "Whether you need reports automated, a team upskilled or extra capacity on contract, we'd like to hear about it.")

# ------------------------------------------------------------------ CONTACT
CONTACT = f'''
<section class="page-hero" style="padding-bottom:190px">
  <div class="grid-bg" aria-hidden="true"></div>
  <div class="container">
    <p class="crumbs"><a href="index.html">Home</a> &nbsp;/&nbsp; Contact</p>
    <p class="eyebrow eyebrow--gold">Contact</p>
    <h1>Let's talk about <em>your data.</em></h1>
    <p class="lead">Tell us a little about what you need. We'll reply to arrange a discovery call or recommend the right programme.</p>
  </div>
</section>

<section class="section" style="padding-top:0">
  <div class="container contact-grid">
    <!-- To receive messages directly (no email app), create a free form at formspree.io
         and paste its URL into data-endpoint, e.g. data-endpoint="https://formspree.io/f/xxxxxxx" -->
    <form class="form-card" data-contact-form data-endpoint="https://formspree.io/f/mgaozrav" data-email="{EMAIL}" novalidate>
      <input type="hidden" name="_subject" value="New website enquiry — Intelligence With Data">
      <input type="text" name="_gotcha" tabindex="-1" autocomplete="off" aria-hidden="true" style="position:absolute;left:-9999px;width:1px;height:1px;opacity:0">
      <div class="form-grid">
        <div class="field"><label for="name">Full name</label><input id="name" name="name" autocomplete="name" required></div>
        <div class="field"><label for="email">Work email</label><input id="email" name="email" type="email" autocomplete="email" required></div>
        <div class="field"><label for="company">Company <span style="color:var(--muted);font-weight:500">(optional)</span></label><input id="company" name="company" autocomplete="organization"></div>
        <div class="field"><label for="interest">I'm interested in</label>
          <select id="interest" name="interest" required>
            <option>Report automation (Power BI)</option>
            <option>Microsoft Fabric</option>
            <option>Team upskilling</option>
            <option>AI &amp; prompt engineering training</option>
            <option>Contract analytics support</option>
            <option>Individual training or internship</option>
            <option>Kids in Tech</option>
            <option>Something else</option>
          </select></div>
        <div class="field field--full"><label for="message">How can we help?</label><textarea id="message" name="message" placeholder="For example: we spend two days a month building our management pack in Excel…" required></textarea></div>
      </div>
      <div class="form-foot"><small>We only use your details to reply to your enquiry.</small><button class="btn btn--gold" type="submit">Send message {ARROW}</button></div>
      <p class="form-status" role="status"></p>
    </form>
    <aside class="contact-side">
      <a class="contact-item" href="mailto:{EMAIL}"><span class="icon">{I["mail"]}</span><div><strong>Email</strong><span>{EMAIL}</span></div></a>
      <a class="contact-item" href="tel:+447344099129"><span class="icon icon--gold">{I["phone"]}</span><div><strong>Phone</strong><span>{PHONE}</span></div></a>
      <a class="contact-item" href="{WA}" target="_blank" rel="noopener"><span class="icon">{I["chat"]}</span><div><strong>WhatsApp</strong><span>Message us for a quick reply</span></div></a>
      <div class="contact-item"><span class="icon icon--gold">{I["globe"]}</span><div><strong>Where we work</strong><span>UK-based. Remote across the UK, Canada &amp; Europe; on-site in the UK.</span></div></div>
    </aside>
  </div>
</section>
'''

NOTFOUND = f'''
<section class="page-hero notfound">
  <div class="grid-bg" aria-hidden="true"></div>
  <div class="container">
    <div class="big404">404</div>
    <h1>This page didn't refresh.</h1>
    <p class="lead" style="margin-inline:auto">The page you're looking for has moved or doesn't exist.</p>
    <div class="btn-row" style="justify-content:center"><a class="btn btn--gold" href="index.html">Back to home {ARROW}</a></div>
  </div>
</section>
'''

REG = f'href="{LUMA}" target="_blank" rel="noopener"'

def module_list(items):
    return "".join(f'<li><span class="mod-num">{i:02d}</span><div><strong>{t}</strong><small>{d}</small></div></li>' for i, (t, d) in enumerate(items, 1))

PBI = [
    ("Introduction to Power BI", "The interface, the workflow, and how analysts use it day to day"),
    ("Power Query", "Connect to data, then clean and transform it without formulas"),
    ("Data modelling", "Relationships and star schemas that keep reports fast and accurate"),
    ("DAX", "Measures and calculated columns for the numbers businesses ask for"),
    ("Visualisation &amp; storytelling", "Choose the right visual and lead people to the insight"),
    ("Power BI Service", "Publish, share and refresh reports and dashboards"),
    ("Real-world projects", "Build reports you can show in interviews"),
]
SQL = [
    ("SQL fundamentals", "How databases and tables work, and why every analyst needs SQL"),
    ("SELECT queries", "Pull exactly the columns and rows you need"),
    ("Filtering &amp; sorting", "WHERE, ORDER BY and the logic behind them"),
    ("Aggregations &amp; GROUP BY", "Totals, averages and counts by category"),
    ("Joins", "Combine tables correctly, and avoid duplicate-row traps"),
    ("Subqueries &amp; CTEs", "Break hard questions into readable steps"),
    ("SQL for reporting", "Analyse real-world datasets and feed your reports"),
]

FREE = f'''
<section class="hero free-hero">
  <div class="grid-bg" aria-hidden="true"></div>
  <div class="container hero-grid">
    <div class="hero-copy">
      <span class="live-chip"><span class="promo-dot"></span>Free &middot; Live online &middot; Every Friday</span>
      <h1>Power BI &amp; SQL Fridays. <em>Learn live, for free.</em></h1>
      <p class="lead">Join a free weekly class with a working Senior Data Analyst. Learn the two skills that open data analyst roles, ask your questions live, and leave each session able to do something new.</p>
      <div class="btn-row">
        <a class="btn btn--gold" {REG}>Reserve my free seat {ARROW}</a>
        <a class="btn btn--ghost" href="#curriculum">What you'll learn</a>
      </div>
      <ul class="trust"><li>100% free</li><li>Beginner-friendly</li><li>Live Q&amp;A every week</li></ul>
    </div>
    <div class="session-card" data-countdown>
      <p class="session-label">Next live session</p>
      <p class="session-date" data-next-date>Friday, 6:00 PM UK</p>
      <p class="session-local" data-local-time></p>
      <div class="countdown" aria-live="off">
        <div><strong data-cd="d">--</strong><span>Days</span></div>
        <div><strong data-cd="h">--</strong><span>Hours</span></div>
        <div><strong data-cd="m">--</strong><span>Mins</span></div>
        <div><strong data-cd="s">--</strong><span>Secs</span></div>
      </div>
      <ul class="session-facts">
        <li><span>{I["globe"]}</span>Live on Google Meet</li>
        <li><span>{I["refresh"]}</span>Every Friday, 6:00 PM UK time</li>
        <li><span>{I["check"]}</span>Free. Registration required</li>
      </ul>
      <a class="btn btn--gold session-btn" {REG}>Register on Luma {ARROW}</a>
      <p class="session-note">You'll get the joining link by email after you register.</p>
    </div>
  </div>
</section>

<section class="section section--tint">
  <div class="container">
    <div class="section-head center reveal"><p class="eyebrow">Is this for you?</p><h2>Built for people <em>ready to grow with data.</em></h2></div>
    <div class="cards cards--3">
      <div class="card reveal"><div class="icon">{I["flag"]}</div><h3>Career-switchers</h3><p style="margin:0">New to data and want a clear, practical path into an analyst role.</p></div>
      <div class="card reveal" style="--d:.1s"><div class="icon icon--gold">{I["brief"]}</div><h3>Portfolio builders</h3><p style="margin:0">Want real projects to show employers, not just certificates.</p></div>
      <div class="card reveal" style="--d:.2s"><div class="icon">{I["spark"]}</div><h3>Working professionals</h3><p style="margin:0">Already use Excel and want to step up to Power BI and SQL.</p></div>
    </div>
  </div>
</section>

<section class="section" id="curriculum">
  <div class="container">
    <div class="section-head reveal"><p class="eyebrow">The curriculum</p><h2>What you'll learn <em>across the sessions.</em></h2><p class="lead">Sessions rotate through two tracks, so you can join any Friday and pick up something useful.</p></div>
    <div class="tracks">
      <div class="track reveal">
        <div class="track-head"><span class="track-badge track-badge--gold">Power BI</span><h3>From raw data to dashboards</h3></div>
        <ol class="mods">{module_list(PBI)}</ol>
      </div>
      <div class="track reveal" style="--d:.1s">
        <div class="track-head"><span class="track-badge">SQL</span><h3>Ask any question of your data</h3></div>
        <ol class="mods">{module_list(SQL)}</ol>
      </div>
    </div>
  </div>
</section>

<section class="section section--navy">
  <div class="container">
    <div class="section-head center reveal"><p class="eyebrow eyebrow--gold">Inside a session</p><h2>Every Friday, <em>you leave with a new skill.</em></h2></div>
    <div class="process">
      <div class="step reveal"><div class="step-num">1</div><h3>Live teaching</h3><p>A focused walkthrough of one Power BI or SQL topic.</p></div>
      <div class="step reveal" style="--d:.1s"><div class="step-num">2</div><h3>Hands-on analysis</h3><p>Work through it yourself on realistic business data.</p></div>
      <div class="step reveal" style="--d:.2s"><div class="step-num">3</div><h3>Live Q&amp;A</h3><p>Bring your questions, whether from the session, your job or your studies.</p></div>
      <div class="step reveal" style="--d:.3s"><div class="step-num">4</div><h3>Career tips</h3><p>Practical advice on portfolios, CVs and landing a data role.</p></div>
    </div>
  </div>
</section>

<section class="section">
  <div class="container split split--center">
    <div class="quote-panel reveal">
      <p class="big">I went from oil and gas engineering to a UK data analyst role in six months, self-taught. These Fridays are the class I wish I'd had.</p>
      <div class="who"><span class="avatar">HF</span><div><strong>Hakeem Falade</strong><small>Your host &middot; Senior Data Analyst</small></div></div>
    </div>
    <div class="reveal" style="--d:.1s">
      <p class="eyebrow">Your host</p>
      <h2>Taught by someone <em>who does the job.</em></h2>
      <p class="lead">Hakeem Falade is a Senior Data Analyst, Microsoft Certified Professional and BCS member, and the founder of Intelligence With Data. He teaches the way analysts actually work, with the shortcuts, habits and judgement that take years to pick up alone.</p>
      <div class="btn-row"><a class="btn btn--navy" {REG}>Join this Friday {ARROW}</a></div>
    </div>
  </div>
</section>

<section class="section section--tint">
  <div class="container">
    <div class="section-head center reveal"><p class="eyebrow">Questions</p><h2>Good to know</h2></div>
    <div class="faq reveal">
      <details><summary>Is it really free?</summary><p>Yes. The Friday sessions are completely free. You just need to register on Luma so we can send you the joining link.</p></details>
      <details><summary>Do I need any experience?</summary><p>No. Sessions are beginner-friendly, and there's always something for people who already know the basics.</p></details>
      <details><summary>What do I need to join?</summary><p>A laptop or desktop with an internet connection. Power BI Desktop is free and runs on Windows; Mac users can still follow along and learn the concepts.</p></details>
      <details><summary>What time is it where I live?</summary><p>Sessions start at 6:00 PM UK time every Friday. The countdown at the top of this page shows the start time in your own time zone.</p></details>
      <details><summary>Can I join any week?</summary><p>Yes. Join whenever you can. Each session stands on its own, and regular attendance builds your skills week by week.</p></details>
      <details><summary>I want faster progress. Is there more?</summary><p>Yes. We also offer 1:1 coaching and a simulated data analytics internship. <a href="training.html" style="color:var(--blue);font-weight:700">Explore our programmes</a>.</p></details>
    </div>
  </div>
</section>

<section class="cta-band" style="padding-top:110px"><div class="container"><div class="cta-inner reveal">
  <div><p class="eyebrow eyebrow--gold">See you Friday</p><h2>Your data career starts with one free session.</h2><p>Every Friday at 6:00 PM UK time, live on Google Meet. Reserve your seat in under a minute.</p></div>
  <div class="cta-actions"><a class="btn btn--gold" {REG}>Reserve my free seat {ARROW}</a><a class="btn btn--ghost" href="{WA}" target="_blank" rel="noopener">Questions? WhatsApp us</a></div>
</div></div></section>

<div class="sticky-reg" data-sticky-reg><div><strong>Power BI &amp; SQL Fridays</strong><span>Free &middot; 6pm UK</span></div><a class="btn btn--gold btn--sm" {REG}>Register free</a></div>
'''

NOINDEX = {"staff.html"}  # insights pages added below while in preview
WEBMAIL = "https://server801.web-hosting.com:2096"

STAFF = f'''
<section class="page-hero staff-hero">
  <div class="grid-bg" aria-hidden="true"></div>
  <div class="container staff-wrap">
    <div class="staff-card reveal">
      <div class="staff-icon">{I["mail"]}</div>
      <p class="eyebrow">Staff portal</p>
      <h1>Team email</h1>
      <p class="staff-lead">Sign in to your <strong>@intelligencewithdata.com</strong> mailbox through our secure webmail.</p>
      <a class="btn btn--gold staff-btn" href="{WEBMAIL}" rel="noopener">Go to webmail {ARROW}</a>
      <p class="staff-url">{I["check"]}<span>You'll be taken to our secure mail server at <strong>server801.web-hosting.com</strong></span></p>
      <div class="staff-help">
        <h2>Before you sign in</h2>
        <ul>
          <li>Use your <strong>full email address</strong> as the username.</li>
          <li>Only enter your password on the <strong>server801.web-hosting.com</strong> webmail page, and check the padlock in the address bar.</li>
          <li>We will never ask for your password by email, phone or WhatsApp.</li>
          <li>Forgotten password or locked out? Contact <a href="mailto:training@intelligencewithdata.com">training@intelligencewithdata.com</a> or WhatsApp <a href="{WA}" target="_blank" rel="noopener">+44 7344 099 129</a>.</li>
        </ul>
      </div>
    </div>
  </div>
</section>
'''

CAREERS = f'''
<section class="page-hero">
  <div class="grid-bg" aria-hidden="true"></div>
  <div class="container">
    <p class="crumbs"><a href="index.html">Home</a> &nbsp;/&nbsp; Careers</p>
    <p class="eyebrow eyebrow--gold">Careers</p>
    <h1>Do work that <em>gives people their time back.</em></h1>
    <p class="lead">We're a growing UK data consultancy and training company. When we hire, we look for curious, practical people who love turning messy data into clear answers, and who enjoy helping others learn.</p>
    <div class="btn-row"><a class="btn btn--gold" href="#talent">Join our talent network {ARROW}</a><a class="btn btn--ghost" href="#roles">Current openings</a></div>
  </div>
</section>

<section class="section" id="roles">
  <div class="container">
    <div class="section-head reveal"><p class="eyebrow">Open positions</p><h2>Current <em>openings.</em></h2></div>
    <div class="no-roles reveal">
      <div class="no-roles-icon">{I["brief"]}</div>
      <div>
        <h3>No open positions right now</h3>
        <p>We don't have any vacancies at the moment, but we're always glad to hear from talented people. Join our talent network and we'll contact you first when a role that fits you opens up.</p>
      </div>
      <a class="btn btn--navy" href="#talent">Register your interest {ARROW}</a>
    </div>
    <div class="roles-note reveal"><p>Roles we typically hire for</p><ul class="role-tags"><li>Data Analyst</li> <li>Power BI Developer</li> <li>Data Engineer (Microsoft Fabric)</li> <li>Data &amp; AI Trainer</li> <li>Kids in Tech Tutor</li></ul></div>
  </div>
</section>

<section class="section section--tint">
  <div class="container">
    <div class="section-head center reveal"><p class="eyebrow">Why join us</p><h2>What working with us <em>looks like.</em></h2></div>
    <div class="cards cards--3">
      <div class="card reveal"><div class="icon">{I["auto"]}</div><h3>Real, varied work</h3><p style="margin:0">Client reporting projects, Microsoft Fabric builds and training delivery. No two weeks look the same.</p></div>
      <div class="card reveal" style="--d:.1s"><div class="icon icon--gold">{I["spark"]}</div><h3>Learning built in</h3><p style="margin:0">We teach for a living, so your own development is part of the job, from certifications to mentoring.</p></div>
      <div class="card reveal" style="--d:.2s"><div class="icon">{I["globe"]}</div><h3>Flexible &amp; remote-friendly</h3><p style="margin:0">UK-based, working with clients and learners across the UK, Canada and Europe.</p></div>
      <div class="card reveal"><div class="icon icon--gold">{I["people"]}</div><h3>Impact you can see</h3><p style="margin:0">Your work saves clients real hours and helps career-switchers land their first data role.</p></div>
      <div class="card reveal" style="--d:.1s"><div class="icon">{I["check"]}</div><h3>Clarity &amp; ownership</h3><p style="margin:0">Clear scope, clear deliverables, and the trust to own your work from start to finish.</p></div>
      <div class="card reveal" style="--d:.2s"><div class="icon icon--gold">{I["layers"]}</div><h3>Modern Microsoft stack</h3><p style="margin:0">Power BI, Microsoft Fabric, SQL, Excel and AI tools, used on real business problems.</p></div>
    </div>
  </div>
</section>

<section class="section section--navy">
  <div class="container">
    <div class="section-head center reveal"><p class="eyebrow eyebrow--gold">How we hire</p><h2>A simple, <em>respectful process.</em></h2></div>
    <div class="process">
      <div class="step reveal"><div class="step-num">1</div><h3>Apply</h3><p>Send your details and a link to your CV or LinkedIn.</p></div>
      <div class="step reveal" style="--d:.1s"><div class="step-num">2</div><h3>Intro call</h3><p>A relaxed 20-minute chat about you and the role.</p></div>
      <div class="step reveal" style="--d:.2s"><div class="step-num">3</div><h3>Practical task</h3><p>A short, realistic task. No trick questions.</p></div>
      <div class="step reveal" style="--d:.3s"><div class="step-num">4</div><h3>Offer</h3><p>A clear decision, with feedback whatever the outcome.</p></div>
    </div>
  </div>
</section>

<section class="section" id="talent">
  <div class="container split">
    <div class="reveal">
      <p class="eyebrow">Talent network</p>
      <h2>Be first to hear <em>when we're hiring.</em></h2>
      <p class="lead">Tell us about yourself and the kind of role you're looking for. We'll keep your details on file and contact you when something fits.</p>
      <ul class="check-list" style="margin-top:28px">
        <li>No spam<small>We only contact you about relevant roles</small></li>
        <li>Your data stays private<small>Used only for recruitment, and deleted on request</small></li>
      </ul>
    </div>
    <form class="form-card form-card--inline reveal" data-contact-form data-endpoint="https://formspree.io/f/mgaozrav" data-email="training@intelligencewithdata.com" novalidate style="--d:.1s">
      <input type="hidden" name="_subject" value="Careers: talent network registration">
      <input type="hidden" name="interest" value="Careers / talent network">
      <input type="text" name="_gotcha" tabindex="-1" autocomplete="off" aria-hidden="true" style="position:absolute;left:-9999px;width:1px;height:1px;opacity:0">
      <div class="form-grid">
        <div class="field"><label for="c-name">Full name</label><input id="c-name" name="name" autocomplete="name" required></div>
        <div class="field"><label for="c-email">Email</label><input id="c-email" name="email" type="email" autocomplete="email" required></div>
        <div class="field"><label for="c-role">Role you're interested in</label>
          <select id="c-role" name="role" required>
            <option>Data Analyst</option><option>Power BI Developer</option><option>Data Engineer (Microsoft Fabric)</option>
            <option>Data &amp; AI Trainer</option><option>Kids in Tech Tutor</option><option>Something else</option>
          </select></div>
        <div class="field"><label for="c-link">LinkedIn or CV link</label><input id="c-link" name="link" type="url" placeholder="https://"></div>
        <div class="field field--full"><label for="c-msg">A little about you</label><textarea id="c-msg" name="message" placeholder="Your experience, skills and what you're looking for…" required></textarea></div>
      </div>
      <div class="form-foot"><small>We use your details only for recruitment.</small><button class="btn btn--gold" type="submit">Join the network {ARROW}</button></div>
      <p class="form-status" role="status"></p>
    </form>
  </div>
</section>
'''

ARTS = insights.load()
INSIGHTS_PREVIEW = False  # approved 12 Oct 2026
if not INSIGHTS_PREVIEW:
  HOME = HOME.replace('<section class="cta-band">', insights.home_teaser(ARTS, ARROW) + '<section class="cta-band">', 1)

PAGES = [
    ("index.html", "Intelligence With Data | Power BI & Microsoft Fabric Consultancy, UK", "UK data consultancy automating reporting with Power BI and Microsoft Fabric, and upskilling teams in Excel, SQL, Power BI and AI.", HOME),
    ("insights.html", "Insights | Power BI, SQL & Microsoft Fabric | Intelligence With Data", "Practical guides and explainers on Power BI, SQL, Microsoft Fabric and building a career in data, from Intelligence With Data.", insights.listing(ARTS, ARROW)),
    ("services.html", "Consulting | Power BI, Fabric & AI Upskilling | Intelligence With Data", "Report automation, Microsoft Fabric foundations, team upskilling, AI and prompt engineering training, and UK contract analytics support.", SERVICES),
    ("training.html", "Training & Careers | Intelligence With Data", "1:1 coaching, a simulated data analytics internship, bootcamps, mentorship and a Saturday tech class for children.", TRAINING),
    ("free-training.html", "Free Power BI & SQL Training, Every Friday | Intelligence With Data", "Free live Power BI and SQL training every Friday at 6pm UK time. Hands-on lessons, live Q&A and career tips from a Senior Data Analyst. Register free.", FREE),
    ("about.html", "About | Intelligence With Data", "Founded by Senior Data Analyst Hakeem Falade, Intelligence With Data combines consulting and training on the Microsoft data stack.", ABOUT),
    ("contact.html", "Contact | Intelligence With Data", "Book a discovery call or ask about training. Email, phone or WhatsApp Intelligence With Data.", CONTACT),
    ("careers.html", "Careers | Intelligence With Data", "Careers at Intelligence With Data: data analytics, Power BI, Microsoft Fabric and training roles. Join our talent network.", CAREERS),
    ("staff.html", "Staff Email | Intelligence With Data", "Staff access to Intelligence With Data webmail.", STAFF),
] + [
    (a["file"], a["title"] + " | Intelligence With Data", a["dek"], insights.article_page(a, ARTS, ARROW, SITE_URL, WA)) for a in ARTS
] + [
    ("404.html", "Page not found | Intelligence With Data", "Page not found.", NOTFOUND),
]

FAVICON = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 40 40"><rect width="40" height="40" rx="11" fill="#0B1B3F"/><rect x="9" y="22" width="5.5" height="9" rx="1.6" fill="#5B8CFF"/><rect x="17.25" y="15" width="5.5" height="16" rx="1.6" fill="#BFD0FF"/><rect x="25.5" y="8.5" width="5.5" height="22.5" rx="1.6" fill="#C9A227"/></svg>'

if INSIGHTS_PREVIEW:
    NOINDEX |= {"insights.html"} | {a["file"] for a in ARTS}
else:
    NAV.insert(4, ("insights.html", "Insights"))

def main():
    if OUT.exists():
        shutil.rmtree(OUT)
    shutil.copytree(ROOT / "assets", OUT / "assets")
    (OUT / "assets/img").mkdir(parents=True, exist_ok=True)
    (OUT / "assets/img/favicon.svg").write_text(FAVICON)
    for f, t, d, b in PAGES:
        (OUT / f).write_text(page(f, t, d, b), encoding="utf-8")
    (OUT / ".nojekyll").write_text("")
    (OUT / "CNAME").write_text("www.intelligencewithdata.com\n")
    (OUT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {SITE_URL}sitemap.xml\n")
    urls = "".join(f"<url><loc>{SITE_URL}{'' if f == 'index.html' else f}</loc></url>" for f, *_ in PAGES if f != "404.html" and f not in NOINDEX)
    (OUT / "sitemap.xml").write_text(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>\n')
    shutil.copy(ROOT / "README.md", OUT / "README.md")
    for img in (ROOT / "og").glob("*.png"):
        shutil.copy(img, OUT / "assets/img" / img.name)
    print("built", [p.name for p in OUT.iterdir()])

if __name__ == "__main__":
    main()
