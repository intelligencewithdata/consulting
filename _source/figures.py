"""Branded, responsive HTML/CSS figures embedded in Insights articles via [[fig:name]]."""


def step(title, sub="", cls=""):
    return f'<div class="fstep {cls}"><strong>{title}</strong>{f"<small>{sub}</small>" if sub else ""}</div>'


def flow(*steps):
    return '<div class="flow">' + "".join(steps) + "</div>"


def table(caption, head, rows, hl=()):
    th = "".join(f"<th>{h}</th>" for h in head)
    hl_attr = ' class="hl"'
    trs = "".join(
        "<tr" + (hl_attr if i in hl else "") + ">" + "".join(f"<td>{c}</td>" for c in r) + "</tr>"
        for i, r in enumerate(rows)
    )
    return f'<div class="mini-table"><p>{caption}</p><table><thead><tr>{th}</tr></thead><tbody>{trs}</tbody></table></div>'


FIGURES = {
    # ---------------------------------------------------------------- automation
    "manual-vs-automated": f'''
<figure class="fig">
  <div class="fig-row">
    <div class="fig-label fig-label--bad"><span>Manual</span><em>Every week, by hand</em></div>
    {flow(step("Export", "from each system", "bad"), step("Copy &amp; paste", "into the template", "bad"), step("Fix formulas", "that broke", "bad"), step("Check totals", "line by line", "bad"), step("Email it", "and hope it's right", "bad"))}
  </div>
  <div class="fig-row">
    <div class="fig-label fig-label--good"><span>Automated</span><em>Set up once</em></div>
    {flow(step("Connect", "to the sources", "good"), step("Power Query", "cleans the data", "good"), step("Data model", "one KPI definition", "good"), step("Scheduled refresh", "runs overnight", "good"), step("Report ready", "when people arrive", "good gold"))}
  </div>
  <figcaption>The same report, two ways. Automation captures the manual steps once and repeats them reliably on a schedule.</figcaption>
</figure>''',

    # ---------------------------------------------------------------- fabric
    "fabric-architecture": f'''
<figure class="fig">
  <div class="arch">
    <div class="arch-col"><p class="arch-h">Your data sources</p>{step("CRM")}{step("Finance system")}{step("Excel &amp; SharePoint")}{step("Cloud apps")}</div>
    <div class="arch-arrow" aria-hidden="true"></div>
    <div class="arch-col arch-col--fabric">
      <p class="arch-h arch-h--light">Microsoft Fabric</p>
      {step("Data Factory", "pipelines &amp; Dataflows Gen2", "dark")}
      <div class="arch-lake"><p>OneLake <small>one copy of your data</small></p><div class="arch-pair">{step("Lakehouse", "", "dark")}{step("Warehouse", "", "dark")}</div></div>
      {step("Semantic model", "one definition of every KPI", "dark")}
    </div>
    <div class="arch-arrow" aria-hidden="true"></div>
    <div class="arch-col"><p class="arch-h">Everyone sees</p>{step("Power BI reports", "", "gold")}{step("Dashboards", "", "gold")}{step("Excel analysis", "", "gold")}</div>
  </div>
  <figcaption>How the pieces fit: data is loaded once into OneLake, modelled once, and reused by every report.</figcaption>
</figure>''',

    # ---------------------------------------------------------------- career
    "career-journey": '''
<figure class="fig">
  <ol class="journey">
    <li><span class="j-dot"></span><div><em>Nigeria</em><strong>Asset Production Engineer, NNPC</strong><small>Oil production facilities</small></div></li>
    <li><span class="j-dot"></span><div><em>The move</em><strong>Relocated to the UK</strong><small>To join my wife</small></div></li>
    <li><span class="j-dot j-dot--muted"></span><div><em>Survival jobs</em><strong>Fish factory, then solar panels</strong><small>One week, then five months</small></div></li>
    <li><span class="j-dot j-dot--blue"></span><div><em>Evenings</em><strong>Self-taught Excel, SQL &amp; Power BI</strong><small>Focused on what UK employers asked for</small></div></li>
    <li><span class="j-dot j-dot--gold"></span><div><em>Within six months</em><strong>UK Data Analyst</strong><small>First role in data</small></div></li>
    <li><span class="j-dot j-dot--gold"></span><div><em>Today</em><strong>Senior Data Analyst &amp; founder</strong><small>Intelligence With Data</small></div></li>
  </ol>
  <figcaption>The journey at a glance.</figcaption>
</figure>''',

    # ---------------------------------------------------------------- sql joins
    "sql-joins": f'''
<figure class="fig">
  <div class="tbl-grid">
    {table("customers", ["customer_id", "name"], [["1", "Ada"], ["2", "Ben"], ["3", "Cy"]])}
    {table("orders", ["order_id", "customer_id", "amount"], [["10", "1", "120"], ["11", "1", "900"], ["13", "2", "600"]])}
  </div>
  <div class="tbl-grid">
    {table("INNER JOIN &rarr; matches only", ["name", "order_id"], [["Ada", "10"], ["Ada", "11"], ["Ben", "13"]])}
    {table("LEFT JOIN &rarr; every customer", ["name", "order_id"], [["Ada", "10"], ["Ada", "11"], ["Ben", "13"], ["Cy", '<span class="null">NULL</span>']], hl=(3,))}
  </div>
  <figcaption>Cy has never ordered. An INNER JOIN drops her; a LEFT JOIN keeps her with a NULL, which is exactly how you find customers who haven't bought.</figcaption>
</figure>''',

    # ---------------------------------------------------------------- window
    "sql-window": f'''
<figure class="fig">
  <div class="tbl-grid tbl-grid--one">
    {table("ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY order_date DESC)", ["customer_id", "order_id", "order_date", "order_rank"],
           [["1", "11", "2026-02-10", "<b>1</b>"], ["1", "10", "2026-01-05", "2"], ["2", "13", "2026-03-20", "<b>1</b>"], ["2", "12", "2026-03-01", "2"]], hl=(0, 2))}
  </div>
  <figcaption>Numbering restarts for each customer. Keep <code>order_rank = 1</code> and you have each customer's latest order.</figcaption>
</figure>''',
}
