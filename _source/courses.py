import json
from media import stock, class_gallery
"""Paid live training programmes page (courses.html).
Prices are set in US dollars and shown in the visitor's currency by assets/js/main.js."""

# Payment links. Leave a link empty to fall back to "we'll send your secure payment link".
# Africa (incl. Ghana until a GHS page exists) -> Paystack NGN page (customer enters the amount shown on our site).
PAYSTACK_NGN_URL = "https://paystack.shop/pay/gu76pth3gz"
PAYSTACK_GHS_URL = ""        # add when GHS is enabled on Paystack (enables mobile money for Ghana)
# UK + rest of world -> Stripe (priced in USD; Stripe Adaptive Pricing shows local currency, e.g. GBP in the UK).
STRIPE_LINKS = {
    "excel-ai|no": "https://buy.stripe.com/cNi8wPbQX5jA8QMc9DeIw00",
    "excel-ai|yes": "https://buy.stripe.com/bJe3cv2gncM2c2YflPeIw01",
    "power-bi|no": "https://buy.stripe.com/28EbJ1f394fwc2YflPeIw02",
    "power-bi|yes": "https://buy.stripe.com/8x2cN59IP8vMd726PjeIw03",
    "sql|no": "https://buy.stripe.com/5kQ28rcV1eUa6IEb5zeIw04",
    "sql|yes": "https://buy.stripe.com/14A8wPaMTaDU0kgc9DeIw05",
    "bundle|no": "https://buy.stripe.com/00w3cv8ELdQ64Awa1veIw06",
    "bundle|yes": "https://buy.stripe.com/5kQ4gzf39cM20kgddHeIw08",
}
FORM_ENDPOINT = "https://formspree.io/f/mgaozrav"

EXCEL_USD = 150                      # base fee
INTERNSHIP_RATE = 0.40               # optional remote internship = 40% of the chosen course fee...
INTERNSHIP_CAP = 79                  # ...capped at this (USD), so it stays below the standalone internship ($99)


def addon(usd):
    return min(round(usd * INTERNSHIP_RATE), INTERNSHIP_CAP)
BUNDLE_DISCOUNT = 1 - 3500 / 4500    # ~22% off when taking all three

# Cohorts: a new cohort every 6 weeks, Saturdays 10:00–13:00 UK time, starting from this date.
COHORT_FIRST = "2026-11-07"
COHORT_EVERY_WEEKS = 6

PROGRAMMES = [
    {
        "id": "excel-ai", "n": "1", "sessions": "Sessions 1 &amp; 2", "name": "Excel &amp; AI for Analytics", "short": "Excel & AI",
        "price": EXCEL_USD,
        "summary": "Turn Excel into a serious analysis tool, then use AI assistants to work faster and smarter.",
        "for": "Beginners and anyone who uses Excel but wants to analyse data with confidence.",
        "sessions_detail": [
            ("Excel for analysis", "Clean, structured data with Tables, sorting, filtering and validation; the formulas analysts use daily (XLOOKUP, IF, SUMIFS); PivotTables and Power Query in Excel to summarise and reshape messy data."),
            ("Dashboards &amp; AI for analytics", "Build an interactive dashboard with charts and slicers, then use AI assistants to write formulas, explain data and draft insights, with prompting techniques, accuracy checks and responsible use."),
        ],
        "outcomes": ["Clean and analyse real datasets", "Build an interactive Excel dashboard", "Use AI prompts to speed up analysis"],
    },
    {
        "id": "power-bi", "n": "2", "sessions": "Sessions 3 &amp; 4", "name": "Advanced Power BI for Advanced Reporting", "short": "Advanced Power BI",
        "price": round(EXCEL_USD * 1.2),
        "summary": "From Power BI Desktop all the way to publishing, sharing and collaborating in the Power BI Service, the way companies actually use it.",
        "for": "Learners who know Excel and want professional-grade reporting skills employers ask for.",
        "sessions_detail": [
            ("Desktop, Power Query &amp; modelling", "Connect to multiple sources, clean and shape data with Power Query, build a star-schema model with relationships and a date table, and write DAX measures for real KPIs."),
            ("Advanced reports, publishing &amp; collaboration", "Drill-through, bookmarks and tooltips; then publish to the Power BI Service using a corporate (work) email account we set up for you, share data in a workspace, collaborate with others and schedule refresh."),
        ],
        "outcomes": ["Build complete reports end to end", "Write DAX measures with confidence", "Publish and collaborate in a real workspace"],
    },
    {
        "id": "sql", "n": "3", "sessions": "Sessions 5 &amp; 6", "name": "SQL for Data Analysis", "short": "SQL",
        "price": round(EXCEL_USD * 1.1),
        "summary": "Learn the language for getting answers out of databases, which almost every data analyst job asks for.",
        "for": "Anyone aiming for a data analyst role, from complete beginners to self-taught learners filling gaps.",
        "sessions_detail": [
            ("Querying &amp; summarising", "How databases work; SELECT, WHERE, ORDER BY; aggregations with GROUP BY and HAVING; CASE expressions and cleaning data with SQL."),
            ("Joins, CTEs &amp; window functions", "INNER and LEFT joins, subqueries and CTEs, window functions for rankings and running totals, applied to a real-world analysis project."),
        ],
        "outcomes": ["Answer business questions with SQL", "Join and summarise data across tables", "Use CTEs and window functions"],
    },
]
FULL = sum(p["price"] for p in PROGRAMMES)
BUNDLE = round(FULL * (1 - BUNDLE_DISCOUNT) / 5) * 5          # $385


def price(usd, cls=""):
    return f'<span class="price {cls}" data-price-usd="{usd}">${usd:,}</span>'


def page(I, ARROW, WA):
    progs = ""
    for i, p in enumerate(PROGRAMMES):
        sess = "".join(f'<li><span class="wk">Session {int(p["n"]) * 2 - 1 + k}</span><div><strong>{t}</strong><p>{d}</p></div></li>' for k, (t, d) in enumerate(p["sessions_detail"]))
        outs = "".join(f"<li>{o}</li>" for o in p["outcomes"] + ["Assignments, a test and a certificate"])
        progs += f'''
    <article class="prog reveal" id="{p["id"]}">
      <div class="prog-main">
        <span class="tag{' tag--gold' if i == 1 else ''}">Programme {p["n"]} &middot; {p["sessions"]} &middot; 2 Saturdays</span>
        <h3>{p["name"]}</h3>
        <p class="prog-sum">{p["summary"]}</p>
        <p class="prog-for"><strong>Who it's for:</strong> {p["for"]}</p>
        <ol class="weeks">{sess}</ol>
      </div>
      <aside class="prog-side">
        <p class="prog-price-label">Programme fee</p>
        {price(p["price"], "price--xl")}
        <p class="price-note">2 live sessions &middot; 6 hours of teaching</p>
        <p class="addon-line">+ optional 4-week remote internship: {price(addon(p["price"]))}</p>
        <ul class="check-list prog-outs">{outs}</ul>
        <a class="btn btn--gold prog-btn" href="#apply" data-choose="{p["id"]}">Apply for this programme {ARROW}</a>
      </aside>
    </article>'''

    opts = "".join(f'<option value="{p["id"]}" data-usd="{p["price"]}">{p["short"]} (${p["price"]})</option>' for p in PROGRAMMES)
    pay_cfg = {"ngn": PAYSTACK_NGN_URL, "ghs": PAYSTACK_GHS_URL, "stripe": STRIPE_LINKS}
    return f'''
<section class="hero courses-hero">
  <div class="grid-bg" aria-hidden="true"></div>
  <div class="container hero-grid">
    <div class="hero-copy">
      <span class="live-chip"><span class="promo-dot"></span>New cohort every 6 weeks &middot; Saturdays &middot; Live on Google Meet</span>
      <h1>Become a job-ready data analyst <em>in six Saturdays.</em></h1>
      <p class="lead">Master Excel &amp; AI, Advanced Power BI and SQL in live weekend classes with a working Senior Data Analyst. Assignments, tests and a certificate, then an optional remote internship to put it all into practice.</p>
      <div class="btn-row">
        <a class="btn btn--gold" href="#apply">Apply for the next cohort {ARROW}</a>
        <a class="btn btn--ghost" href="#programmes">See the programmes</a>
      </div>
      <ul class="trust"><li>Saturdays, 10am&ndash;1pm UK</li><li>Certificate on completion</li><li>Optional remote internship</li></ul>
    </div>
    <div class="price-card" id="pricing">
      <div class="cohort-strip"><span>Next cohort starts</span><strong data-next-cohort>Saturday 7 November 2026</strong><small data-cohort-local>10:00&ndash;13:00 UK time</small></div>
      <div class="cur-row">
        <p class="session-label">Programme fees</p>
        <label class="cur-select"><span class="sr-only">Show prices in</span><select data-currency-select aria-label="Show prices in"></select></label>
      </div>
      <ul class="price-list">
        {"".join(f'<li><span>{p["name"]}<small>{p["sessions"]}</small></span>{price(p["price"])}</li>' for p in PROGRAMMES)}
      </ul>
      <div class="bundle-box">
        <div><span class="bundle-tag">Best value</span><strong>All three programmes</strong><small>6 Saturdays &middot; <s>{price(FULL)}</s></small></div>
        {price(BUNDLE, "price--lg")}
      </div>
      <p class="save-line">Save {price(FULL - BUNDLE)} when you take all three together</p>
      <p class="fx-note" data-fx-note>Prices are set in US dollars. Choose your currency to see an estimate.</p>
      <a class="btn btn--gold session-btn" href="#apply">Apply now {ARROW}</a>
    </div>
  </div>
</section>

<section class="section section--tint" style="padding:56px 0">
  <div class="container facts">
    <div><strong>6</strong><span>Live Saturday sessions</span></div>
    <div><strong>3 hrs</strong><span>Per session, 10am&ndash;1pm UK</span></div>
    <div><strong>Every 6 weeks</strong><span>A new cohort begins</span></div>
    <div><strong>4 weeks</strong><span>Optional remote internship</span></div>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="section-head center reveal"><p class="eyebrow">Your journey</p><h2>From first class <em>to real-world work.</em></h2></div>
    <ol class="journey-flow">
      <li class="reveal"><span>1</span><strong>Learn live</strong><small>6 Saturday sessions on Google Meet: two each for Excel &amp; AI, Power BI and SQL.</small></li>
      <li class="reveal" style="--d:.08s"><span>2</span><strong>Practise &amp; prove it</strong><small>Assignments after every session and a test for each programme.</small></li>
      <li class="reveal" style="--d:.16s"><span>3</span><strong>Get certified</strong><small>Receive your Intelligence With Data certificate on completion.</small></li>
      <li class="reveal" style="--d:.24s"><span>4</span><strong>Remote internship</strong><small>Optional 4 weeks working with us on real-world style projects to consolidate your learning.</small></li>
      <li class="reveal gold" style="--d:.32s"><span>5</span><strong>Consulting work</strong><small>Best-performing students get the chance to work with us on our consulting projects, behind the scenes.</small></li>
    </ol>
  </div>
</section>

<section class="section section--tint" id="programmes">
  <div class="container">
    <div class="section-head reveal"><p class="eyebrow">The programmes</p><h2>Everything you'll learn, <em>session by session.</em></h2><p class="lead">Each programme is two live Saturday sessions of three hours. Take one, or all three across six Saturdays as a complete path from spreadsheets to dashboards to databases.</p></div>
    <div class="progs">{progs}</div>
  </div>
</section>

{class_gallery()}

<section class="section section--navy">
  <div class="container">
    <div class="bundle-feature reveal">
      <div>
        <p class="eyebrow eyebrow--gold">The complete analyst path</p>
        <h2>All three programmes. <em>Six Saturdays.</em></h2>
        <p class="lead" style="color:#C3CDE4">Excel &amp; AI for Analytics, Advanced Power BI and SQL for Data Analysis: the core toolkit employers look for in a data analyst, with assignments, tests and a certificate.</p>
        <ul class="trust" style="margin-top:22px"><li>Excel &amp; AI</li><li>Advanced Power BI</li><li>SQL</li><li>Certificate</li></ul>
      </div>
      <div class="bundle-price">
        <span>Instead of <s>{price(FULL)}</s></span>
        {price(BUNDLE, "price--hero")}
        <em>You save {price(FULL - BUNDLE)}</em>
        <small class="bundle-addon">Add the 4-week remote internship for {price(addon(BUNDLE))}</small>
        <a class="btn btn--gold" href="#apply" data-choose="bundle">Apply for all three {ARROW}</a>
      </div>
    </div>
  </div>
</section>

<section class="section">
  <div class="container split split--center">
    <div class="reveal">
      {stock("photo-1590650516494-0c8e4a4dd67e", "Two analysts reviewing work together on a computer screen")}
      <p class="eyebrow">Optional add-on</p>
      <h2>Remote internship: <em>4 weeks of real-world practice.</em></h2>
      <p class="lead">Learning sticks when you use it. After your training, join our 4-week remote internship to work on realistic projects with deadlines and stakeholders, consolidating everything you've learned and giving you experience to talk about in interviews.</p>
      <ul class="check-list" style="margin-top:26px">
        <li>4 weeks, fully remote<small>Work alongside our team on real-world style analytics projects</small></li>
        <li>40% of your course fee, never more than $79<small>Choose it when you apply; it's completely optional</small></li>
        <li>A path to consulting work<small>Top performers get the chance to support our live consulting projects behind the scenes</small></li>
      </ul>
    </div>
    <div class="intern-card reveal" style="--d:.1s">
      <p class="session-label">Internship add-on</p>
      <ul class="price-list">
        {"".join(f'<li><span>With {p["short"]}</span>{price(addon(p["price"]))}</li>' for p in PROGRAMMES)}
        <li><span>With all three programmes</span>{price(addon(BUNDLE))}</li>
      </ul>
      <a class="btn btn--navy session-btn" href="#apply" data-internship="yes">Apply with the internship {ARROW}</a>
    </div>
  </div>
</section>

<section class="section section--tint">
  <div class="container">
    <div class="section-head center reveal"><p class="eyebrow">How to join</p><h2>Five simple steps <em>to your first Saturday.</em></h2></div>
    <ol class="join-steps">
      <li class="reveal"><span>1</span><strong>Apply</strong><small>Choose your programme and internship option, and tell us about you.</small></li>
      <li class="reveal" style="--d:.08s"><span>2</span><strong>Confirmation</strong><small>We review your application and confirm your cohort.</small></li>
      <li class="reveal" style="--d:.16s"><span>3</span><strong>Pay securely</strong><small>Pay your fee in your preferred currency through our secure link.</small></li>
      <li class="reveal" style="--d:.24s"><span>4</span><strong>Onboarding</strong><small>Receive your onboarding materials and Google Meet details by email.</small></li>
      <li class="reveal" style="--d:.32s"><span>5</span><strong>Start learning</strong><small>Join your cohort's first Saturday, 10am&ndash;1pm UK time.</small></li>
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
      <details><summary>When are the classes?</summary><p>Every Saturday from 10:00 to 13:00 UK time, live on Google Meet. A new cohort starts every six weeks, as soon as the previous one finishes; the next dates are shown in the application form. The page shows the start time in your own time zone.</p></details>
      <details><summary>How long is each programme?</summary><p>Each programme is two Saturday sessions of three hours. All three programmes run across six consecutive Saturdays: sessions 1&ndash;2 Excel &amp; AI, 3&ndash;4 Power BI, 5&ndash;6 SQL.</p></details>
      <details><summary>Will I get a certificate?</summary><p>Yes. You complete assignments and a test for each programme, and receive an Intelligence With Data certificate on completion.</p></details>
      <details><summary>How does the remote internship work?</summary><p>It's an optional 4-week remote programme after your training, priced at 40% of your course fee and never more than $79. You choose it when you apply. You'll work on real-world style analytics projects to consolidate what you've learned, and the best-performing students get the chance to support our consulting work behind the scenes.</p></details>
      <details><summary>Which currency do I pay in?</summary><p>Fees are set in US dollars. The currency switcher shows an estimate in your local currency from recent exchange rates; the exact amount may vary slightly with your bank or payment provider.</p></details>
      <details><summary>What do I need for the Power BI sessions?</summary><p>A Windows laptop is best, because Power BI Desktop runs on Windows. For the Power BI Service, we set you up with a corporate (work) email account so you can publish, share and collaborate in a real workspace.</p></details>
      <details><summary>When do I receive my onboarding materials?</summary><p>As soon as your payment is confirmed, we email your onboarding pack, schedule and Google Meet details.</p></details>
    </div>
  </div>
</section>

<section class="section" id="apply">
  <div class="container split">
    <div class="reveal apply-aside">
      <p class="eyebrow">Apply</p>
      <h2>Tell us about you, <em>and where you want to go.</em></h2>
      <p class="lead">This helps us understand your background, current skill level and expectations, so we can place you in the right cohort and make the training count.</p>
      <div class="plan-total" data-plan-total>
        <p>Your plan</p>
        <strong data-plan-name>All three programmes</strong>
        <div class="plan-lines"><span>Training</span><span data-plan-course></span></div>
        <div class="plan-lines" data-plan-intern-row hidden><span>Remote internship</span><span data-plan-intern></span></div>
        <div class="plan-lines plan-sum"><span>Total</span><span data-plan-sum></span></div>
      </div>
      <p style="margin-top:18px;color:var(--muted);font-size:.92rem">Questions first? <a href="{WA}" target="_blank" rel="noopener" style="color:var(--blue);font-weight:700">Chat with us on WhatsApp</a></p>
    </div>
    <form class="form-card form-card--inline reveal" data-contact-form data-apply-form data-endpoint="{FORM_ENDPOINT}" data-email="training@intelligencewithdata.com" novalidate>
      <input type="hidden" name="_subject" value="New training application (Saturday cohort)">
      <input type="hidden" name="interest" value="Paid training programme application">
      <input type="hidden" name="display_currency" data-currency-field value="USD">
      <input type="hidden" name="total_usd" data-total-field value="">
      <input type="hidden" name="total_display" data-total-display-field value="">
      <div hidden aria-hidden="true"><input type="text" name="_gotcha" tabindex="-1" autocomplete="off"></div>
      <p class="form-sec">Your plan</p>
      <div class="form-grid">
        <div class="field field--full"><label for="a-prog">Programme</label>
          <select id="a-prog" name="programme" required data-programme-select>
            <option value="bundle" data-usd="{BUNDLE}" selected>All three programmes (${BUNDLE})</option>{opts}
          </select></div>
        <div class="field field--full"><label for="a-intern">Add the 4-week remote internship?</label>
          <select id="a-intern" name="remote_internship" data-internship-select>
            <option value="no">No, training only</option><option value="yes">Yes, add the internship</option>
          </select></div>
        <div class="field field--full"><label for="a-cohort">Preferred cohort</label>
          <select id="a-cohort" name="cohort" data-cohort-select required></select></div>
      </div>
      <p class="form-sec">About you</p>
      <div class="form-grid">
        <div class="field"><label for="a-name">Full name</label><input id="a-name" name="name" autocomplete="name" required></div>
        <div class="field"><label for="a-email">Email</label><input id="a-email" name="email" type="email" autocomplete="email" required></div>
        <div class="field"><label for="a-phone">WhatsApp number</label><input id="a-phone" name="whatsapp" type="tel" autocomplete="tel" placeholder="Include country code" required></div>
        <div class="field"><label for="a-country">Country</label><input id="a-country" name="country" autocomplete="country-name" required></div>
      </div>
      <p class="form-sec">Background &amp; current level</p>
      <div class="form-grid">
        <div class="field"><label for="a-role">Current role or situation</label><input id="a-role" name="current_role" placeholder="e.g. Accountant, student, job seeker" required></div>
        <div class="field"><label for="a-edu">Highest qualification &amp; field</label><input id="a-edu" name="education" placeholder="e.g. BSc Economics"></div>
        <div class="field"><label for="a-excel">Excel level</label><select id="a-excel" name="excel_level"><option>None</option><option>Beginner</option><option>Intermediate</option><option>Advanced</option></select></div>
        <div class="field"><label for="a-pbi">Power BI level</label><select id="a-pbi" name="power_bi_level"><option>None</option><option>Beginner</option><option>Intermediate</option><option>Advanced</option></select></div>
        <div class="field"><label for="a-sql">SQL level</label><select id="a-sql" name="sql_level"><option>None</option><option>Beginner</option><option>Intermediate</option><option>Advanced</option></select></div>
        <div class="field"><label for="a-laptop">Laptop</label><select id="a-laptop" name="laptop"><option>Windows</option><option>Mac</option><option>No laptop yet</option></select></div>
      </div>
      <p class="form-sec">Your expectations</p>
      <div class="form-grid">
        <div class="field field--full"><label for="a-goal">What do you want to achieve from this training?</label><textarea id="a-goal" name="expectations" placeholder="e.g. Move into a data analyst role within 6 months, build dashboards at work, prepare for interviews…" required></textarea></div>
        <div class="field field--full"><label for="a-heard">How did you hear about us?</label><select id="a-heard" name="heard_about"><option>WhatsApp</option><option>LinkedIn</option><option>TikTok</option><option>YouTube</option><option>Friend or colleague</option><option>Google</option><option>Other</option></select></div>
      </div>
      <div class="form-foot"><small>No payment needed to apply. We use your details only to process your application.</small><button class="btn btn--gold" type="submit">Submit application {ARROW}</button></div>
      <p class="form-status" role="status"></p>
      <div class="apply-success" data-apply-success hidden>
        <div class="staff-icon" style="margin:0 0 16px">{I["check"]}</div>
        <h3>Application received. Thank you!</h3>
        <div data-pay-block hidden>
          <p>Secure your place by paying your fee now. Your onboarding materials and Google Meet details will be emailed once payment is confirmed.</p>
          <div class="pay-box">
            <span>Amount to pay</span>
            <strong data-pay-amount></strong>
            <small data-pay-hint></small>
          </div>
          <div class="btn-row"><a class="btn btn--gold" data-pay-link href="#" target="_blank" rel="noopener"><span data-pay-label>Pay securely now</span> {ARROW}</a></div>
          <p class="pay-small">Payments are processed securely by <span data-pay-provider>Paystack</span>. Please include your name and programme on the payment page so we can match it to your application.</p>
        </div>
        <p data-pay-later>We'll review your details and send your secure payment link by email and WhatsApp, usually within 24 hours. Once payment is confirmed, you'll receive your onboarding materials and Google Meet details.</p>
        <div class="btn-row"><a class="btn btn--outline" href="{WA}" target="_blank" rel="noopener">Message us on WhatsApp</a></div>
      </div>
    </form>
  </div>
</section>
<script>window.IWD_PAY = {json.dumps(pay_cfg)}; window.IWD_INTERNSHIP_RATE = {INTERNSHIP_RATE}; window.IWD_INTERNSHIP_CAP = {INTERNSHIP_CAP}; window.IWD_COHORT = {{ first: "{COHORT_FIRST}", everyWeeks: {COHORT_EVERY_WEEKS} }};</script>
'''
