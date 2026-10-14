"""Shared imagery: calm Unsplash stock photos (free licence) and real screenshots from our live classes."""


def unsplash(pid, w, ratio):
    return f"https://images.unsplash.com/{pid}?auto=format&fit=crop&w={w}&h={round(w / ratio)}&q=70"


def stock(pid, alt, ratio=16 / 9, cls="", sizes="(max-width: 900px) 100vw, 560px"):
    """A static, lazily loaded photo in the site's standard rounded frame."""
    src = lambda w: unsplash(pid, w, ratio)
    h = round(1000 / ratio)
    return (f'<figure class="feature-photo {cls}" style="aspect-ratio:{ratio:.4f}"><img src="{src(1000)}" '
            f'srcset="{src(640)} 640w, {src(1000)} 1000w, {src(1400)} 1400w" sizes="{sizes}" width="1000" height="{h}" '
            f'loading="lazy" decoding="async" alt="{alt}"></figure>')


CLASS_SHOTS = [
    ("class-star-schema", 1328, 747, "Data modelling: the star schema explained",
     "Slide from a live Power BI class showing a central fact table linked to product, branch, calendar and location dimension tables"),
    ("class-powerbi-model", 1438, 782, "Hands-on: building the model in Power BI Desktop",
     "Power BI Desktop model view from a live class, showing a fact table linked to customer, product and calendar tables"),
    ("class-dax", 1329, 653, "DAX functions, one at a time",
     "Slide from a live Power BI class explaining SUM, AVERAGE, MAX, MIN, DIVIDE and ROUND in DAX"),
    ("class-revenue-whiteboard", 1440, 758, "Working it out live: how revenue is calculated",
     "Power BI table view with a hand-drawn note showing revenue as units sold from the fact table times unit price from the product table"),
    ("class-kpi-measures", 1440, 758, "The result: revenue, COGS and gross profit as KPI cards",
     "Power BI report page with KPI cards for revenue, cost of goods sold, gross profit, number of sales and number of customers"),
    ("class-dashboard-practices", 1328, 747, "Dashboard best practices for real stakeholders",
     "Slide listing six dashboard best practices: KPI cards first, the right chart type, slicers, one page per theme, consistent colours and telling a story"),
]


def shot(name, w, h, label, alt):
    return f'''<figure class="class-shot reveal">
  <div class="class-shot-bar" aria-hidden="true"><span></span><span></span><span></span><em>Live on Google Meet</em></div>
  <a href="assets/img/{name}.jpg" target="_blank" rel="noopener" aria-label="Open full size: {label}"><picture><source srcset="assets/img/{name}.webp" type="image/webp"><img src="assets/img/{name}.jpg" width="{w}" height="{h}" loading="lazy" decoding="async" alt="{alt}"></picture></a>
  <figcaption>{label}<small><a href="assets/img/{name}.jpg" target="_blank" rel="noopener">Open full size</a></small></figcaption>
</figure>'''


def class_gallery(eyebrow="Inside a live class", title="See how we <em>actually teach.</em>",
                  lead="Highlights from one of our recent live Power BI classes: a clear slide for each idea, then we build it together in Power BI Desktop, from data model to finished KPIs.",
                  tint=False):
    shots = "".join(shot(*s) for s in CLASS_SHOTS)
    return f'''
<section class="section{' section--tint' if tint else ''}">
  <div class="container">
    <div class="section-head center reveal"><p class="eyebrow">{eyebrow}</p><h2>{title}</h2><p class="lead">{lead}</p></div>
    <div class="class-gallery">{shots}</div>
  </div>
</section>'''
