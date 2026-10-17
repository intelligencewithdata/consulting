"""Newsletter: the subscribe page, an inline signup band, and a gentle slide-in.

Subscriptions are posted to Formspree (same account as the contact form). To send the newsletter
from systeme.io instead, replace ENDPOINT with a systeme.io-connected endpoint or export from Formspree."""

ENDPOINT = "https://formspree.io/f/mgaozrav"   # backup copy of every sign-up (Formspree inbox)
# Make.com custom webhook that creates the contact in systeme.io and tags it "Data Brief".
# Paste the webhook URL from Make here; while empty, sign-ups go to Formspree only.
MAKE_WEBHOOK = ""
NAME = "The Data Brief"
CADENCE = "One short email a week"

# Pages where the slide-in may appear (never on application, payment, checkout-adjacent or utility pages)
SLIDEIN_PAGES_EXCLUDE = {"newsletter.html", "courses.html", "internship.html", "contact.html", "careers.html",
                         "free-training.html", "payment-success.html", "staff.html", "404.html"}

PERKS = [
    ("New Insights, first", "The week's practical guides on Power BI, Microsoft Fabric and SQL, with the key takeaway up front."),
    ("One idea you can use", "A tip, formula or modelling pattern you can try in your own work that week."),
    ("What's coming up", "Dates for free Friday classes, new Saturday cohorts and internship intakes, before anyone else."),
]


def _fields(idp, compact=False, source="Newsletter page"):
    role = "" if compact else f'''
        <div class="field"><label for="{idp}-role">I'm mainly here as</label>
          <select id="{idp}-role" name="reader_type"><option value="Business">A business owner or manager</option><option value="Data professional">A data professional</option><option value="Learner">A learner or career-switcher</option></select></div>'''
    name = "" if compact else f'''
        <div class="field"><label for="{idp}-name">First name</label><input id="{idp}-name" name="first_name" autocomplete="given-name"></div>'''
    return f'''<input type="hidden" name="_subject" value="New newsletter subscriber ({NAME})">
      <input type="hidden" name="interest" value="Newsletter subscription">
      <input type="hidden" name="signup_source" value="{source}">
      <div hidden aria-hidden="true"><input type="text" name="_gotcha" tabindex="-1" autocomplete="off"></div>
      <div class="nl-fields{' nl-fields--compact' if compact else ''}">{name}
        <div class="field"><label for="{idp}-email">Email address</label><input id="{idp}-email" name="email" type="email" autocomplete="email" required placeholder="you@example.com"></div>{role}
      </div>
      <label class="nl-consent"><input type="checkbox" name="consent" value="Yes, send me {NAME}" required><span>Yes, send me {NAME}. I can unsubscribe at any time.</span></label>
      <button class="btn btn--gold nl-btn" type="submit">Subscribe</button>
      <p class="nl-status" data-nl-status role="status" aria-live="polite"></p>'''


def form(idp="nl", compact=False, source="Newsletter page", cls=""):
    return f'''<form class="nl-form {cls}" data-newsletter-form data-endpoint="{ENDPOINT}" data-webhook="{MAKE_WEBHOOK}" novalidate>
      {_fields(idp, compact, source)}
    </form>'''


def page(ARROW):
    perks = "".join(f'<li><strong>{t}</strong><small>{d}</small></li>' for t, d in PERKS)
    return f'''
<section class="hero nl-hero">
  <div class="grid-bg" aria-hidden="true"></div>
  <div class="container hero-grid">
    <div class="hero-copy">
      <span class="live-chip"><span class="promo-dot"></span>Free newsletter &middot; {CADENCE.lower()}</span>
      <h1>{NAME}: <em>practical data, in your inbox.</em></h1>
      <p class="lead">Power BI, Microsoft Fabric and SQL explained plainly, by people who do the work. Short enough to read with your coffee, useful enough to keep.</p>
      <ul class="trust"><li>{CADENCE}</li><li>No spam, ever</li><li>Unsubscribe in one click</li></ul>
    </div>
    <div class="price-card nl-card" id="subscribe">
      <p class="session-label">Subscribe free</p>
      <h2 class="nl-card-title">Join {NAME}</h2>
      {form("nlp")}
      <div class="nl-done" data-nl-done hidden>
        <p class="session-label">You're subscribed</p>
        <h2 class="nl-card-title">Welcome to {NAME}.</h2>
        <p>Your first issue arrives in your inbox soon. While you wait, the latest Insights are ready to read.</p>
        <a class="btn btn--navy" href="insights.html">Read the latest Insights {ARROW}</a>
      </div>
    </div>
  </div>
</section>

<section class="section">
  <div class="container split split--center">
    <div class="reveal">
      <p class="eyebrow">What you'll get</p>
      <h2>Three things, <em>every issue.</em></h2>
      <p class="lead">No long essays and no hard sell. Just the useful parts, written for busy business owners, analysts and career-switchers.</p>
    </div>
    <ol class="nl-perks reveal" style="--d:.1s">{perks}</ol>
  </div>
</section>

<section class="section section--tint">
  <div class="container">
    <div class="section-head center reveal"><p class="eyebrow">Good to know</p><h2>Before you subscribe</h2></div>
    <div class="faq reveal">
      <details><summary>How often will I hear from you?</summary><p>{CADENCE}. If there's nothing worth sending, we skip the week.</p></details>
      <details><summary>Is it free?</summary><p>Yes, completely free. Occasionally we'll mention a programme or class we think you'll find useful, and you're never obliged to buy anything.</p></details>
      <details><summary>What do you do with my email address?</summary><p>We only use it to send you {NAME}. We never sell or share it. Every email includes an unsubscribe link, or you can reply and ask us to remove you.</p></details>
      <details><summary>I run a business. Is this for me?</summary><p>Yes. Each issue includes ideas for getting more from your reports and data, not just technical tutorials.</p></details>
    </div>
  </div>
</section>
'''


def band(source="Newsletter band"):
    """Inline signup strip placed above the footer on content pages."""
    return f'''
<section class="nl-band-wrap">
  <div class="container">
    <div class="nl-band reveal">
      <div class="nl-band-copy">
        <p class="eyebrow eyebrow--gold">{NAME}</p>
        <h2>Practical data tips, <em>once a week.</em></h2>
        <p>New guides on Power BI, Fabric and SQL, plus class and cohort dates first. Free, and you can unsubscribe any time.</p>
      </div>
      <div>
        {form("nlb", compact=True, source=source, cls="nl-form--dark")}
        <div class="nl-done nl-done--dark" data-nl-done hidden><strong>You're subscribed.</strong><span>Look out for your first issue soon.</span></div>
      </div>
    </div>
  </div>
</section>'''


def slidein(file):
    if file in SLIDEIN_PAGES_EXCLUDE:
        return ""
    return f'''
<aside class="nl-slide" data-nl-slide hidden aria-labelledby="nl-slide-title">
  <button class="nl-close" type="button" data-nl-close aria-label="Close and don't show again for a while">&times;</button>
  <p class="session-label">Free weekly newsletter</p>
  <h2 id="nl-slide-title">Enjoying this? Get {NAME}.</h2>
  <p class="nl-slide-text">One short email a week with practical Power BI, Fabric and SQL tips.</p>
  {form("nls", compact=True, source="Slide-in: " + file)}
  <div class="nl-done" data-nl-done hidden><strong>You're subscribed.</strong><span>Thank you. Your first issue is on its way soon.</span></div>
  <a class="nl-more" href="newsletter.html">What's in it?</a>
</aside>'''
