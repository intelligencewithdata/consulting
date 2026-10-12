"""Paid live training programmes page (courses.html) — priced in Ghana cedis with live currency switching."""

# Paste the payment page URL here (e.g. a Paystack or Flutterwave payment link). Leave empty to show
# "we'll send your secure payment link" after the application form is submitted.
PAY_URL = ""
FORM_ENDPOINT = "https://formspree.io/f/mgaozrav"

PROGRAMMES = [
    {
        "id": "excel-ai", "tag": "Programme 1", "name": "Excel &amp; AI for Analytics", "price": 1500,
        "summary": "Turn Excel into a serious analysis tool, then use AI assistants to work faster and smarter.",
        "for": "Beginners and anyone who uses Excel but wants to analyse data with confidence.",
        "weeks": [
            ("Excel foundations for analysis", "Clean, structured data with Tables, sorting, filtering, data validation and the formulas analysts use daily, including XLOOKUP, IF and SUMIFS."),
            ("Summarise and transform", "PivotTables, PivotCharts and Power Query in Excel to combine, clean and reshape messy data without manual copy-and-paste."),
            ("Dashboards that communicate", "Choose the right charts, build an interactive dashboard with slicers, and present insights clearly."),
            ("AI for analytics", "Use AI assistants to write formulas, explain data and draft insights, with prompting techniques, accuracy checks and responsible use. Ends with a capstone project."),
        ],
        "outcomes": ["Clean and analyse real datasets in Excel", "Build an interactive Excel dashboard", "Use AI prompts to speed up everyday analysis", "A capstone project for your portfolio"],
    },
    {
        "id": "power-bi", "tag": "Programme 2", "name": "Advanced Power BI for Advanced Reporting", "price": 1500,
        "summary": "Go from Power BI Desktop all the way to publishing, sharing and collaborating in the Power BI Service, the way companies actually use it.",
        "for": "Learners who know Excel and want professional-grade reporting skills employers ask for.",
        "weeks": [
            ("Power BI Desktop and Power Query", "Connect to multiple sources, then clean, shape and combine data with Power Query."),
            ("Data modelling and DAX", "Star schemas, relationships, a proper date table, and DAX measures for the KPIs businesses need."),
            ("Advanced report design", "Interactive reports with drill-through, bookmarks, tooltips and design that leads people to the insight."),
            ("Publishing, sharing and collaboration", "Publish to the Power BI Service using a corporate (work) email account we set up for you, share data in a workspace, collaborate with others, schedule refresh and manage access, just like a real team."),
        ],
        "outcomes": ["Build complete Power BI reports end to end", "Write DAX measures with confidence", "Publish and collaborate in a real Power BI workspace", "Hands-on Service experience most courses skip"],
    },
    {
        "id": "sql", "tag": "Programme 3", "name": "SQL for Data Analysis", "price": 1500,
        "summary": "Learn the language for getting answers out of databases, which almost every data analyst job asks for.",
        "for": "Anyone aiming for a data analyst role, from complete beginners to self-taught learners filling gaps.",
        "weeks": [
            ("SQL fundamentals", "How databases work, then SELECT, filtering with WHERE, sorting and limiting results."),
            ("Summarising data", "Aggregations, GROUP BY and HAVING, CASE expressions and cleaning data with SQL."),
            ("Combining tables", "INNER and LEFT joins, subqueries and CTEs to break complex questions into clear steps."),
            ("SQL for reporting", "Window functions for rankings and running totals, real-world datasets, and a final analysis project."),
        ],
        "outcomes": ["Write queries to answer real business questions", "Join and summarise data across tables", "Use CTEs and window functions", "A SQL project you can show employers"],
    },
]
BUNDLE = 3500


def price(ghs, cls=""):
    return f'<span class="price {cls}" data-price-ghs="{ghs}">GH&#8373;{ghs:,}</span>'


def page(I, ARROW, WA):
    progs = ""
    for i, p in enumerate(PROGRAMMES):
        weeks = "".join(f'<li><span class="wk">Week {n}</span><div><strong>{t}</strong><p>{d}</p></div></li>' for n, (t, d) in enumerate(p["weeks"], 1))
        outs = "".join(f"<li>{o}</li>" for o in p["outcomes"])
        progs += f'''
    <article class="prog reveal" id="{p["id"]}">
      <div class="prog-main">
        <span class="tag{' tag--gold' if i == 1 else ''}">{p["tag"]} &middot; 4 weeks &middot; Live on Google Meet</span>
        <h3>{p["name"]}</h3>
        <p class="prog-sum">{p["summary"]}</p>
        <p class="prog-for"><strong>Who it's for:</strong> {p["for"]}</p>
        <ol class="weeks">{weeks}</ol>
      </div>
      <aside class="prog-side">
        <p class="prog-price-label">Programme fee</p>
        {price(p["price"], "price--xl")}
        <p class="price-note" data-price-note>for 4 weeks of live training</p>
        <ul class="check-list prog-outs">{outs}</ul>
        <a class="btn btn--gold prog-btn" href="#apply" data-choose="{p["name"]}">Apply for this programme {ARROW}</a>
      </aside>
    </article>'''

    full = sum(p["price"] for p in PROGRAMMES)
    options = "".join(f'<option>{p["name"].replace("&amp;", "&")} (GH₵{p["price"]:,})</option>' for p in PROGRAMMES)
    pay_btn = (f'<a class="btn btn--gold" href="{PAY_URL}" target="_blank" rel="noopener">Pay securely now {ARROW}</a>'
               if PAY_URL else "")
    return f'''
<section class="hero courses-hero">
  <div class="grid-bg" aria-hidden="true"></div>
  <div class="container hero-grid">
    <div class="hero-copy">
      <span class="live-chip"><span class="promo-dot"></span>Live online &middot; Google Meet &middot; 4-week programmes</span>
      <h1>Become a job-ready data analyst. <em>Live, practical, guided.</em></h1>
      <p class="lead">Master Excel &amp; AI, Power BI and SQL in live online classes with a working Senior Data Analyst, then get interview preparation and a remote internship opportunity to put your skills to work.</p>
      <div class="btn-row">
        <a class="btn btn--gold" href="#apply">Apply now {ARROW}</a>
        <a class="btn btn--ghost" href="#programmes">See the programmes</a>
      </div>
      <ul class="trust"><li>100% live classes</li><li>Interview preparation</li><li>Remote internship opportunity</li></ul>
    </div>
    <div class="price-card" id="pricing">
      <div class="cur-row">
        <p class="session-label">Programme fees</p>
        <label class="cur-select"><span class="sr-only">Show prices in</span>
          <select data-currency-select aria-label="Show prices in"></select>
        </label>
      </div>
      <ul class="price-list">
        {"".join(f'<li><span>{p["name"]}</span>{price(p["price"])}</li>' for p in PROGRAMMES)}
      </ul>
      <div class="bundle-box">
        <div><span class="bundle-tag">Best value</span><strong>All three programmes</strong><small>12 weeks &middot; <s>{price(full)}</s></small></div>
        {price(BUNDLE, "price--lg")}
      </div>
      <p class="save-line">Save {price(full - BUNDLE)} when you take all three together</p>
      <p class="fx-note" data-fx-note>Prices are set in Ghana cedis (GH&#8373;). Choose your currency to see an estimate.</p>
      <a class="btn btn--gold session-btn" href="#apply">Apply now {ARROW}</a>
    </div>
  </div>
</section>

<section class="section section--tint" style="padding:56px 0">
  <div class="container facts">
    <div><strong>3</strong><span>Focused programmes</span></div>
    <div><strong>4 weeks</strong><span>Per programme</span></div>
    <div><strong>100%</strong><span>Live on Google Meet</span></div>
    <div><strong>1 path</strong><span>From learning to interview-ready</span></div>
  </div>
</section>

<section class="section" id="programmes">
  <div class="container">
    <div class="section-head reveal"><p class="eyebrow">The programmes</p><h2>Everything you'll learn, <em>week by week.</em></h2><p class="lead">Take one programme, or all three as a complete path from spreadsheets to dashboards to databases.</p></div>
    <div class="progs">{progs}</div>
  </div>
</section>

<section class="section section--navy">
  <div class="container">
    <div class="bundle-feature reveal">
      <div>
        <p class="eyebrow eyebrow--gold">The complete analyst path</p>
        <h2>All three programmes. <em>One price.</em></h2>
        <p class="lead" style="color:#C3CDE4">Excel &amp; AI for Analytics, Advanced Power BI and SQL for Data Analysis: 12 weeks of live training that covers the core toolkit employers look for in a data analyst.</p>
        <ul class="trust" style="margin-top:22px"><li>Excel &amp; AI</li><li>Advanced Power BI</li><li>SQL</li><li>Interview preparation</li></ul>
      </div>
      <div class="bundle-price">
        <span>Instead of <s>{price(full)}</s></span>
        {price(BUNDLE, "price--hero")}
        <em>You save {price(full - BUNDLE)}</em>
        <a class="btn btn--gold" href="#apply" data-choose="All three programmes (bundle)">Apply for all three {ARROW}</a>
      </div>
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="section-head center reveal"><p class="eyebrow">Beyond the classroom</p><h2>From skills <em>to the job.</em></h2></div>
    <div class="cards">
      <div class="card reveal"><div class="icon icon--gold">{I["mic"]}</div><h3>Interview preparation</h3><p style="margin:0">Practise the technical and competency questions data analyst interviews ask, learn how to talk about your projects, and get feedback on your CV and approach.</p></div>
      <div class="card reveal" style="--d:.1s"><div class="icon">{I["brief"]}</div><h3>Remote internship opportunity</h3><p style="margin:0">Committed learners can join our remote data analytics internship: real-world style projects, deadlines and stakeholders, giving you experience to talk about and work to show.</p></div>
    </div>
  </div>
</section>

<section class="section section--tint">
  <div class="container">
    <div class="section-head center reveal"><p class="eyebrow">How to join</p><h2>Five simple steps <em>to your first class.</em></h2></div>
    <ol class="join-steps">
      <li class="reveal"><span>1</span><strong>Apply</strong><small>Complete the short form below about your background and goals.</small></li>
      <li class="reveal" style="--d:.08s"><span>2</span><strong>Confirmation</strong><small>We review your application and confirm your programme.</small></li>
      <li class="reveal" style="--d:.16s"><span>3</span><strong>Pay securely</strong><small>Pay your programme fee through our secure payment link.</small></li>
      <li class="reveal" style="--d:.24s"><span>4</span><strong>Onboarding</strong><small>Receive your onboarding materials and class schedule by email.</small></li>
      <li class="reveal" style="--d:.32s"><span>5</span><strong>Start learning</strong><small>Join your live classes on Google Meet.</small></li>
    </ol>
  </div>
</section>

<section class="section">
  <div class="container split split--center">
    <div class="quote-panel reveal">
      <p class="big">I went from oil and gas engineering to a UK data analyst role in six months. These programmes teach the practical skills that made the difference.</p>
      <div class="who"><span class="avatar">HF</span><div><strong>Hakeem Falade</strong><small>Lead trainer &middot; Senior Data Analyst</small></div></div>
    </div>
    <div class="reveal" style="--d:.1s">
      <p class="eyebrow">Your trainer</p>
      <h2>Learn from someone <em>who does the job.</em></h2>
      <p class="lead">Hakeem Falade is a Senior Data Analyst in the UK, a Microsoft Certified Professional and a member of BCS, The Chartered Institute for IT. He founded Intelligence With Data to teach analytics the way it's practised at work.</p>
      <div class="btn-row"><a class="btn btn--navy" href="about.html">Read his story {ARROW}</a></div>
    </div>
  </div>
</section>

<section class="section section--tint">
  <div class="container">
    <div class="section-head center reveal"><p class="eyebrow">Questions</p><h2>Good to know</h2></div>
    <div class="faq reveal">
      <details><summary>How are the classes delivered?</summary><p>Every programme is taught live and remotely on Google Meet, so you can join from anywhere with a laptop and a stable internet connection.</p></details>
      <details><summary>How long is each programme?</summary><p>Each programme runs for 4 weeks. Taking all three gives you 12 weeks of live training.</p></details>
      <details><summary>Which currency do I pay in?</summary><p>Fees are set in Ghana cedis (GH&#8373;). The currency switcher shows an estimate in your local currency based on recent exchange rates. The exact amount you pay may vary slightly depending on your bank or payment provider.</p></details>
      <details><summary>What do I need for the Power BI programme?</summary><p>A Windows laptop is best, because Power BI Desktop runs on Windows. For the Power BI Service part of the course, we set you up with a corporate (work) email account so you can publish, share and collaborate in a real workspace.</p></details>
      <details><summary>Do I need any experience?</summary><p>No experience is needed for Excel &amp; AI or SQL. For Advanced Power BI, basic Excel skills help. The application form tells us your level so we can guide you.</p></details>
      <details><summary>When do I receive my onboarding materials?</summary><p>As soon as your payment is confirmed, we email your onboarding pack, class schedule and joining details.</p></details>
    </div>
  </div>
</section>

<section class="section" id="apply">
  <div class="container split">
    <div class="reveal">
      <p class="eyebrow">Apply</p>
      <h2>Tell us about you, <em>and where you want to go.</em></h2>
      <p class="lead">This helps us understand your background, current skill level and expectations, so we can place you on the right programme and make the training count.</p>
      <ul class="check-list" style="margin-top:28px">
        <li>Takes about 3 minutes<small>No payment needed to apply</small></li>
        <li>Personal guidance<small>We'll recommend the right starting point</small></li>
        <li>Questions first?<small><a href="{WA}" target="_blank" rel="noopener" style="color:var(--blue);font-weight:700">Chat with us on WhatsApp</a></small></li>
      </ul>
    </div>
    <form class="form-card form-card--inline reveal" data-contact-form data-apply-form data-endpoint="{FORM_ENDPOINT}" data-email="training@intelligencewithdata.com" novalidate>
      <input type="hidden" name="_subject" value="New training application (Excel, Power BI, SQL programmes)">
      <input type="hidden" name="interest" value="Paid training programme application">
      <input type="hidden" name="display_currency" data-currency-field value="GHS">
      <input type="text" name="_gotcha" tabindex="-1" autocomplete="off" aria-hidden="true" style="position:absolute;left:-9999px;width:1px;height:1px;opacity:0">
      <p class="form-sec">About you</p>
      <div class="form-grid">
        <div class="field"><label for="a-name">Full name</label><input id="a-name" name="name" autocomplete="name" required></div>
        <div class="field"><label for="a-email">Email</label><input id="a-email" name="email" type="email" autocomplete="email" required></div>
        <div class="field"><label for="a-phone">WhatsApp number</label><input id="a-phone" name="whatsapp" type="tel" autocomplete="tel" placeholder="+233 / +234 …" required></div>
        <div class="field"><label for="a-country">Country</label><input id="a-country" name="country" autocomplete="country-name" required></div>
      </div>
      <p class="form-sec">Programme</p>
      <div class="form-grid">
        <div class="field field--full"><label for="a-prog">Which programme are you applying for?</label>
          <select id="a-prog" name="programme" required data-programme-select>
            {options}<option>All three programmes (bundle) (GH₵{BUNDLE:,})</option><option>Not sure yet, please advise me</option>
          </select></div>
      </div>
      <p class="form-sec">Background &amp; current level</p>
      <div class="form-grid">
        <div class="field"><label for="a-role">Current role or situation</label><input id="a-role" name="current_role" placeholder="e.g. Accountant, student, job seeker" required></div>
        <div class="field"><label for="a-edu">Highest qualification &amp; field</label><input id="a-edu" name="education" placeholder="e.g. BSc Economics"></div>
        <div class="field"><label for="a-excel">Excel level</label><select id="a-excel" name="excel_level"><option>None</option><option>Beginner</option><option>Intermediate</option><option>Advanced</option></select></div>
        <div class="field"><label for="a-pbi">Power BI level</label><select id="a-pbi" name="power_bi_level"><option>None</option><option>Beginner</option><option>Intermediate</option><option>Advanced</option></select></div>
        <div class="field"><label for="a-sql">SQL level</label><select id="a-sql" name="sql_level"><option>None</option><option>Beginner</option><option>Intermediate</option><option>Advanced</option></select></div>
        <div class="field"><label for="a-hours">Hours per week you can commit</label><select id="a-hours" name="hours_per_week"><option>Less than 5</option><option>5–10</option><option>10–15</option><option>More than 15</option></select></div>
      </div>
      <p class="form-sec">Your expectations</p>
      <div class="form-grid">
        <div class="field field--full"><label for="a-goal">What do you want to achieve from this training?</label><textarea id="a-goal" name="expectations" placeholder="e.g. Move into a data analyst role within 6 months, build dashboards at work, prepare for interviews…" required></textarea></div>
        <div class="field"><label for="a-int">Interested in the remote internship?</label><select id="a-int" name="internship_interest"><option>Yes</option><option>Maybe</option><option>No</option></select></div>
        <div class="field"><label for="a-heard">How did you hear about us?</label><select id="a-heard" name="heard_about"><option>WhatsApp</option><option>LinkedIn</option><option>TikTok</option><option>YouTube</option><option>Friend or colleague</option><option>Google</option><option>Other</option></select></div>
      </div>
      <div class="form-foot"><small>We use your details only to process your application.</small><button class="btn btn--gold" type="submit">Submit application {ARROW}</button></div>
      <p class="form-status" role="status"></p>
      <div class="apply-success" data-apply-success hidden>
        <div class="staff-icon" style="margin:0 0 16px">{I["check"]}</div>
        <h3>Application received. Thank you!</h3>
        <p>{"Complete your payment below to secure your place. Your onboarding materials and class schedule will be emailed to you once payment is confirmed." if PAY_URL else "We'll review your details and send your secure payment link by email and WhatsApp, usually within 24 hours. Once payment is confirmed, you'll receive your onboarding materials and class schedule."}</p>
        <div class="btn-row">{pay_btn}<a class="btn btn--outline" href="{WA}" target="_blank" rel="noopener">Message us on WhatsApp</a></div>
      </div>
    </form>
  </div>
</section>
'''
