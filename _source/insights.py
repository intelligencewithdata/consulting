"""Insights (articles) — listing page, article pages and home-page teaser."""
import datetime, html, json, math, pathlib, re
import markdown
from figures import FIGURES

HERE = pathlib.Path(__file__).parent

CATS = {
    "Power BI": {"key": "powerbi", "icon": '<rect x="9" y="22" width="5.5" height="9" rx="1.6"/><rect x="17.25" y="15" width="5.5" height="16" rx="1.6"/><rect x="25.5" y="8.5" width="5.5" height="22.5" rx="1.6"/>'},
    "Microsoft Fabric": {"key": "fabric", "icon": '<path d="M20 7 33 14 20 21 7 14Z"/><path d="M7 20l13 7 13-7" fill="none" stroke-width="2.4"/><path d="M7 26l13 7 13-7" fill="none" stroke-width="2.4"/>'},
    "SQL": {"key": "sql", "icon": '<path d="M14 11 7 20l7 9M26 11l7 9-7 9" fill="none" stroke-width="2.8"/><path d="M22.5 9 17.5 31" fill="none" stroke-width="2.4"/>'},
    "Careers": {"key": "careers", "icon": '<path d="M7 31 15 22l6 5 12-15" fill="none" stroke-width="2.8"/><path d="M27 12h6v6" fill="none" stroke-width="2.8"/>'},
}

# Author rotation for new articles (Hakeem writes personal/career pieces):
# Efua Angela -> Elijah Parker -> Thomas Forrester -> Jayne Carter
AUTHORS = {
    "hakeem-falade": {"name": "Hakeem Falade", "role": "Founder, Intelligence With Data", "initials": "HF",
        "bio": "Senior Data Analyst, Microsoft Certified Professional and BCS member. Founder of Intelligence With Data, helping businesses automate reporting and helping people build careers in data."},
    "efua-angela": {"name": "Efua Angela", "role": "Senior Supply Chain Analyst", "initials": "EA",
        "bio": "Senior Supply Chain Analyst at Intelligence With Data."},
    "elijah-parker": {"name": "Elijah Parker", "role": "Microsoft Fabric Consultant", "initials": "EP",
        "bio": "Microsoft Fabric Consultant at Intelligence With Data."},
    "thomas-forrester": {"name": "Thomas Forrester", "role": "AI Engineer", "initials": "TF",
        "bio": "AI Engineer at Intelligence With Data."},
    "jayne-carter": {"name": "Jayne Carter", "role": "Data Engineer", "initials": "JC",
        "bio": "Data Engineer at Intelligence With Data."},
}

SQL_KW = r"\b(SELECT|FROM|WHERE|AND|OR|IN|BETWEEN|ORDER BY|GROUP BY|HAVING|LIMIT|TOP|DESC|ASC|AS|INNER JOIN|LEFT JOIN|JOIN|ON|IS NULL|IS|NULL|CASE|WHEN|THEN|ELSE|END|WITH|OVER|PARTITION BY|COUNT|SUM|AVG|ROW_NUMBER)\b"


def highlight_sql(code):
    out = []
    for part in re.split(r"(&#x27;.*?&#x27;|'.*?')", code):
        if part.startswith(("'", "&#x27;")):
            out.append(f'<span class="tok-str">{part}</span>')
        else:
            out.append(re.sub(SQL_KW, r'<span class="tok-kw">\1</span>', part))
    return "".join(out)


def load():
    arts = []
    for f in sorted((HERE / "articles").glob("*.md")):
        raw = f.read_text(encoding="utf-8")
        _, fm, body = raw.split("---", 2)
        meta = dict(line.split(": ", 1) for line in fm.strip().splitlines())
        md = markdown.Markdown(extensions=["fenced_code", "tables", "toc"], extension_configs={"toc": {"toc_depth": "2"}})
        body_html = md.convert(body)
        body_html = re.sub(r'(<code class="language-sql">)(.*?)(</code>)', lambda m: m.group(1) + highlight_sql(m.group(2)) + m.group(3), body_html, flags=re.S)
        body_html = re.sub(r"<p>\[\[fig:([a-z-]+)\]\]</p>", lambda m: FIGURES[m.group(1)], body_html)
        words = len(re.sub(r"<[^>]+>", " ", body_html).split())
        d = datetime.date.fromisoformat(meta["date"])
        arts.append({
            **meta,
            "file": meta["slug"] + ".html",
            "html": body_html,
            "toc": [(t["id"], t["name"]) for t in md.toc_tokens],
            "mins": max(3, math.ceil(words / 220)),
            "date_h": f"{d.day} {d:%B %Y}",
            "au": AUTHORS[meta.get("author", "hakeem-falade")],
        })
    # Newest first; launch articles (same date) keep their curated order.
    launch = ["insights-automate-business-reporting", "insights-engineer-to-data-analyst", "insights-microsoft-fabric-explained", "insights-10-sql-queries"]
    arts.sort(key=lambda a: (a["date"], -launch.index(a["slug"]) if a["slug"] in launch else 1), reverse=True)
    return arts


def cover(a, size=""):
    c = CATS[a["category"]]
    return f'''<div class="cover cover--{c["key"]} {size}" aria-hidden="true"><span class="cover-grid"></span><svg class="cover-icon" viewBox="0 0 40 40">{c["icon"]}</svg><span class="cover-label">{html.escape(a["category"])}</span></div>'''


def card(a, extra=""):
    return f'''<a class="post-card reveal" href="{a["file"]}" data-cat="{CATS[a["category"]]["key"]}"{extra}>
  {cover(a)}
  <div class="post-body"><span class="post-cat">{html.escape(a["category"])}</span><h3>{html.escape(a["title"])}</h3><p>{html.escape(a["dek"])}</p>
  <span class="post-meta">{a["au"]["name"]} &middot; {a["date_h"]} &middot; {a["mins"]} min read</span></div>
</a>'''


def listing(arts, ARROW):
    feat, rest = arts[0], arts[1:]
    cats = "".join(f'<button class="chip" data-filter="{v["key"]}">{k}</button>' for k, v in CATS.items())
    return f'''
<section class="page-hero">
  <div class="grid-bg" aria-hidden="true"></div>
  <div class="container">
    <p class="crumbs"><a href="index.html">Home</a> &nbsp;/&nbsp; Insights</p>
    <p class="eyebrow eyebrow--gold">Insights</p>
    <h1>Practical thinking on <em>data, reporting and careers.</em></h1>
    <p class="lead">Guides, explainers and lessons from the field on Power BI, SQL, Microsoft Fabric and building a career in data.</p>
  </div>
</section>

<section class="section">
  <div class="container">
    <a class="feature-post reveal" href="{feat["file"]}">
      {cover(feat, "cover--lg")}
      <div class="feature-post-body">
        <span class="post-cat">Featured &middot; {html.escape(feat["category"])}</span>
        <h2>{html.escape(feat["title"])}</h2>
        <p>{html.escape(feat["dek"])}</p>
        <div class="byline"><span class="avatar avatar--sm">{feat["au"]["initials"]}</span><span><strong>{feat["au"]["name"]}</strong><small>{feat["date_h"]} &middot; {feat["mins"]} min read</small></span></div>
        <span class="link">Read article {ARROW}</span>
      </div>
    </a>

    <div class="filter-bar reveal" role="group" aria-label="Filter articles"><button class="chip is-active" data-filter="all">All</button>{cats}</div>
    <div class="post-grid" data-post-grid>{card(feat, ' data-featured hidden')}{"".join(card(a) for a in rest)}</div>
    <p class="no-posts" data-no-posts hidden>More articles in this topic are coming soon.</p>
  </div>
</section>
'''


def article_page(a, arts, ARROW, SITE_URL, WA):
    toc = "".join(f'<li><a href="#{i}">{html.escape(n)}</a></li>' for i, n in a["toc"])
    related = [x for x in arts if x["slug"] != a["slug"]][:3]
    url = SITE_URL + a["file"]
    share_text = html.escape(a["title"])
    from urllib.parse import quote
    enc_url, enc_title = quote(url, safe=""), quote(a["title"], safe="")
    if a["audience"] == "consulting":
        cta = f'''<div class="article-cta"><p class="eyebrow eyebrow--gold">Work with us</p><h3>Want your reporting to run itself?</h3><p>We automate reporting with Power BI and Microsoft Fabric, then train your team to own it. Tell us which reports eat your week.</p><div class="btn-row"><a class="btn btn--gold" href="contact.html">Book a discovery call {ARROW}</a><a class="btn btn--ghost" href="services.html">Explore consulting</a></div></div>'''
    else:
        cta = f'''<div class="article-cta"><p class="eyebrow eyebrow--gold">Free every Friday</p><h3>Learn Power BI &amp; SQL live, for free</h3><p>Join our free live class every Friday at 6pm UK time: hands-on lessons, live Q&amp;A and career tips from a working Senior Data Analyst.</p><div class="btn-row"><a class="btn btn--gold" href="free-training.html">Reserve your free seat {ARROW}</a><a class="btn btn--ghost" href="training.html">See all programmes</a></div></div>'''
    ld = json.dumps({
        "@context": "https://schema.org", "@type": "Article", "headline": a["title"], "description": a["dek"],
        "datePublished": a["date"], "author": {"@type": "Person", "name": a["au"]["name"], "jobTitle": a["au"]["role"]},
        "publisher": {"@type": "Organization", "name": "Intelligence With Data Ltd"},
        "image": SITE_URL + "assets/img/og-" + a["slug"] + ".png", "mainEntityOfPage": url,
    })
    return f'''
<div class="read-progress" aria-hidden="true"><span data-read-progress></span></div>
<section class="page-hero article-hero">
  <div class="grid-bg" aria-hidden="true"></div>
  <div class="container article-head">
    <p class="crumbs"><a href="index.html">Home</a> &nbsp;/&nbsp; <a href="insights.html">Insights</a> &nbsp;/&nbsp; {html.escape(a["category"])}</p>
    <span class="post-cat post-cat--light">{html.escape(a["category"])}</span>
    <h1>{html.escape(a["title"])}</h1>
    <p class="lead">{html.escape(a["dek"])}</p>
    <div class="byline byline--light"><span class="avatar avatar--sm">{a["au"]["initials"]}</span><span><strong>{a["au"]["name"]}</strong><small>{a["au"]["role"]} &middot; {a["date_h"]} &middot; {a["mins"]} min read</small></span></div>
  </div>
</section>

<section class="section article-section">
  <div class="container article-layout">
    <aside class="article-aside">
      <nav class="toc" aria-label="On this page"><p>On this page</p><ol>{toc}</ol></nav>
      <div class="share"><p>Share</p>
        <a href="https://www.linkedin.com/sharing/share-offsite/?url={enc_url}" target="_blank" rel="noopener" aria-label="Share on LinkedIn">in</a>
        <a href="https://wa.me/?text={enc_title}%20{enc_url}" target="_blank" rel="noopener" aria-label="Share on WhatsApp">WA</a>
        <a href="https://x.com/intent/post?text={enc_title}&amp;url={enc_url}" target="_blank" rel="noopener" aria-label="Share on X">X</a>
        <button type="button" data-copy-link="{url}" aria-label="Copy link">Copy</button>
      </div>
    </aside>
    <article class="prose" data-article>
      {a["html"]}
      <div class="author-box"><span class="avatar">{a["au"]["initials"]}</span><div><strong>{a["au"]["name"]}</strong><p>{a["au"]["bio"]}</p></div></div>
      {cta}
    </article>
  </div>
</section>

<section class="section section--tint">
  <div class="container">
    <div class="section-head reveal"><p class="eyebrow">Keep reading</p><h2>More <em>insights.</em></h2></div>
    <div class="post-grid">{"".join(card(r) for r in related)}</div>
  </div>
</section>
<script type="application/ld+json">{ld}</script>
'''


def home_teaser(arts, ARROW):
    return f'''
<section class="section">
  <div class="container">
    <div class="section-head split-head reveal"><div><p class="eyebrow">Insights</p><h2>Latest <em>thinking.</em></h2></div><a class="btn btn--outline" href="insights.html">All insights {ARROW}</a></div>
    <div class="post-grid">{"".join(card(a) for a in arts[:3])}</div>
  </div>
</section>
'''
