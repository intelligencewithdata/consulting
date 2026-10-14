"""Data Analytics Internship page (internship.html).
Every apply button sends visitors to the systeme.io checkout, where payment triggers the automated onboarding."""

APPLY_URL = "https://intelligencewithdata.systeme.io/analytics_internship"
PRICE = "$29.99"          # keep in line with the price on the systeme.io checkout

WEEKS = [
    ("Week 1", "Data discovery &amp; audit",
     "Profile two client databases in SQL Server, document data quality issues and deliver a formal data audit report. Then build a recurring weekly sales report in Excel, automated with Power Query."),
    ("Week 2", "Power BI dashboard",
     "Gather requirements from the client brief, design a star schema model, write DAX measures and build a three-page dashboard, published to the Power BI Service."),
    ("Week 3", "Advanced SQL",
     "Answer harder business questions with CTEs and window functions: supplier performance analysis and customer churn tracking."),
    ("Week 4", "Analytics &amp; storytelling",
     "Forecasting, What-If parameters and AI visuals, then a 10-slide executive presentation delivered live to a panel."),
    ("Launch", "Career launch",
     "Turn the work into results: CV rewrite, LinkedIn profile, interview preparation and a certification pathway guide."),
]

DELIVERABLES = [
    ("SQL query library", "50+ queries you wrote and can explain"),
    ("Automated Excel report", "SQL-connected sales report with a written SOP"),
    ("Power BI dashboard", "A three-page dashboard published to the Power BI Service"),
    ("Analytics reports", "Supplier and customer churn analysis"),
    ("Executive presentation", "10 slides, presented live to a panel"),
    ("Data dictionary &amp; audit", "A formal audit report and documented data model"),
    ("Updated CV", "Plus answers to five real interview questions"),
]

TOOLS = [
    ("SQL Server &amp; SSMS", "Query, profile and audit real databases"),
    ("Microsoft Excel", "Reporting, analysis and automation"),
    ("Power Query (M)", "Repeatable data cleaning and refresh"),
    ("Power BI", "Data modelling, DAX and dashboards"),
    ("PowerPoint", "Executive-ready storytelling"),
]

FAQ = [
    ("How is this different from a Udemy or YouTube course?",
     "A course shows you how to follow along. This internship puts you in a data analyst role: you get a client brief, a deadline every Friday and a senior analyst who reviews your work and challenges your decisions, just like a real job."),
    ("Is it online or in person?",
     "Fully online and one-to-one, by video call, so you can join from the UK, Canada, Europe, Africa or anywhere else."),
    ("Will this help me get a job?",
     "The biggest problem for new analysts is having nothing to show an employer. You finish with real experience to talk about in interviews, a portfolio of seven deliverables, a rewritten CV and interview preparation."),
    ("What computer do I need?",
     "A Windows laptop or desktop. SQL Server Management Studio and Power BI Desktop are Windows applications and are free to download. You'll also need Excel 2016 or Microsoft 365."),
    ("What happens after I pay?",
     "Your place is confirmed straight away and your onboarding details arrive by email automatically, so you can get set up and start Week 1."),
    ("Is this the same as the internship add-on on the Saturday programmes?",
     "The Saturday programmes teach the skills in a live group class; the internship is where you use them on client work. If you're joining a Saturday cohort, you can add the internship when you apply on the programmes page."),
]


def page(I, ARROW, WA):
    go = f'href="{APPLY_URL}"'
    weeks = "".join(f'<li class="reveal"><span class="wk{" wk--gold" if w == "Launch" else ""}">{w}</span><div><strong>{t}</strong><p>{d}</p></div></li>' for w, t, d in WEEKS)
    delivs = "".join(f'<li class="reveal" style="--d:{i * 0.05:.2f}s"><b>{i + 1:02d}</b><strong>{t}</strong><small>{d}</small></li>' for i, (t, d) in enumerate(DELIVERABLES))
    tools = "".join(f'<li><strong>{t}</strong><small>{d}</small></li>' for t, d in TOOLS)
    faq = "".join(f'<details><summary>{q}</summary><p>{a}</p></details>' for q, a in FAQ)
    return f'''
<section class="hero courses-hero">
  <div class="grid-bg" aria-hidden="true"></div>
  <div class="container hero-grid">
    <div class="hero-copy">
      <span class="live-chip"><span class="promo-dot"></span>Data Analytics Internship &middot; 4 weeks &middot; One-to-one, online</span>
      <h1>Stop doing courses. <em>Start getting experience.</em></h1>
      <p class="lead">Work as a junior data analyst on two client accounts for four weeks, with a senior analyst as your manager and deliverables due every Friday. You finish with real experience, a portfolio and a CV that gets interviews.</p>
      <div class="btn-row">
        <a class="btn btn--gold" {go}>Apply for the internship {ARROW}</a>
        <a class="btn btn--ghost" href="#weeks">See the four weeks</a>
      </div>
      <ul class="trust"><li>One-to-one with a senior analyst</li><li>SQL, Excel, Power BI</li><li>Portfolio &amp; career support</li></ul>
    </div>
    <div class="price-card">
      <div class="cohort-strip"><span>Limited places</span><strong>One-to-one, so we take only a few interns each cohort</strong></div>
      <p class="session-label">Your internship includes</p>
      <ul class="check-list intern-includes">
        <li>4 weeks working on two client accounts</li>
        <li>Weekly reviews from a senior analyst</li>
        <li>7 portfolio deliverables you keep</li>
        <li>CV rewrite &amp; interview preparation</li>
      </ul>
      <div class="bundle-box"><div><span class="bundle-tag">Secure your place</span><strong>Data Analytics Internship</strong><small>4 weeks &middot; one-to-one &middot; online</small></div><span class="price price--lg">{PRICE}</span></div>
      <a class="btn btn--gold session-btn" {go}>Apply &amp; secure your place {ARROW}</a>
      <p class="fx-note">Secure checkout. Your onboarding details arrive by email automatically after payment.</p>
    </div>
  </div>
</section>

<section class="section section--tint" style="padding:56px 0">
  <div class="container facts">
    <div><strong>4 weeks</strong><span>A real analyst role</span></div>
    <div><strong>1:1</strong><span>With a senior analyst</span></div>
    <div><strong>2</strong><span>Client accounts</span></div>
    <div><strong>7</strong><span>Portfolio deliverables</span></div>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="section-head center reveal"><p class="eyebrow">Why it works</p><h2>A job, <em>done properly.</em></h2><p class="lead">Employers don't hire certificates. They hire people who have done the work. That's the gap this internship closes.</p></div>
    <div class="vs reveal">
      <div class="vs-col">
        <p class="vs-head">A typical online course</p>
        <ul>
          <li>Follow along with someone else's screen</li>
          <li>Clean, ready-made practice data</li>
          <li>No deadlines, no one checking your work</li>
          <li>A certificate, but nothing to show</li>
        </ul>
      </div>
      <div class="vs-col vs-col--win">
        <p class="vs-head">This internship</p>
        <ul>
          <li>A client brief and a deadline every Friday</li>
          <li>Messy databases you audit and fix yourself</li>
          <li>A senior analyst reviewing and challenging your decisions</li>
          <li>Seven pieces of real work for your portfolio</li>
        </ul>
      </div>
    </div>
  </div>
</section>

<section class="section section--tint" id="weeks">
  <div class="container split">
    <div class="reveal intern-sticky">
      <p class="eyebrow">Week by week</p>
      <h2>Four weeks that feel <em>like the job.</em></h2>
      <p class="lead">Each week ends with a deliverable on Friday, reviewed by your manager the way it would be at work.</p>
      <div class="client-cards">
        <div><span class="tag">Client 1</span><strong>Adventure Outdoors PLC</strong><small>Outdoor equipment retailer selling online and through resellers</small></div>
        <div><span class="tag tag--gold">Client 2</span><strong>Nordic Foods Ltd</strong><small>Food wholesaler with suppliers, orders and shipping data</small></div>
      </div>
      <p class="client-note">Simulated client accounts built on industry-standard Microsoft sample databases.</p>
    </div>
    <ol class="weeks intern-weeks">{weeks}</ol>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="section-head center reveal"><p class="eyebrow">What you'll leave with</p><h2>A portfolio that <em>proves it.</em></h2><p class="lead">Seven deliverables to share with employers and talk through in interviews.</p></div>
    <ol class="deliv-grid">{delivs}</ol>
  </div>
</section>

<section class="section section--navy">
  <div class="container split split--center">
    <div class="reveal">
      <p class="eyebrow eyebrow--gold">The toolkit</p>
      <h2>The tools employers <em>actually ask for.</em></h2>
      <p class="lead" style="color:#C3CDE4">Everything runs on a Windows laptop and is free to download. Excel 2016 or Microsoft 365 is all you need to buy.</p>
    </div>
    <ul class="tool-grid reveal" style="--d:.1s">{tools}</ul>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="section-head center reveal"><p class="eyebrow">How to join</p><h2>Start in <em>three steps.</em></h2></div>
    <ol class="join-steps join-steps--3">
      <li class="reveal"><span>1</span><strong>Apply</strong><small>Click apply and enter your name and email on our secure checkout.</small></li>
      <li class="reveal" style="--d:.08s"><span>2</span><strong>Pay securely</strong><small>Payment confirms your place straight away.</small></li>
      <li class="reveal" style="--d:.16s"><span>3</span><strong>Start Week 1</strong><small>Your onboarding email arrives automatically, with everything you need to begin.</small></li>
    </ol>
    <div class="btn-row" style="justify-content:center;margin-top:40px"><a class="btn btn--gold" {go}>Apply for the internship {ARROW}</a></div>
  </div>
</section>

<section class="section section--tint">
  <div class="container split split--center">
    <div class="quote-panel reveal">
      <p class="big">I went from oil and gas engineering to a UK data analyst role in six months. What made the difference was practical, real-world experience.</p>
      <div class="who"><span class="avatar">HF</span><div><strong>Hakeem Falade</strong><small>Founder &middot; Senior Data Analyst</small></div></div>
    </div>
    <div class="reveal" style="--d:.1s">
      <p class="eyebrow">Who's behind it</p>
      <h2>Built by analysts, <em>for future analysts.</em></h2>
      <p class="lead">Intelligence With Data is a UK data consultancy. Our founder, Hakeem Falade, is a Senior Data Analyst, a Microsoft Certified Professional and a member of BCS, The Chartered Institute for IT. The internship mirrors how analytics work is done for our clients.</p>
      <div class="btn-row"><a class="btn btn--navy" href="about.html">Read his story {ARROW}</a></div>
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="section-head center reveal"><p class="eyebrow">Questions</p><h2>Good to know</h2></div>
    <div class="faq reveal">{faq}</div>
  </div>
</section>

<section class="cta-band"><div class="container"><div class="cta-inner reveal">
  <div><p class="eyebrow eyebrow--gold">Limited places</p><h2>Ready to stop studying and start working?</h2><p>Places are one-to-one, so each cohort is small. Apply now to secure yours.</p></div>
  <div class="cta-actions"><a class="btn btn--gold" {go}>Apply for the internship {ARROW}</a><a class="btn btn--ghost" href="{WA}" target="_blank" rel="noopener">Ask a question on WhatsApp</a></div>
</div></div></section>
'''
