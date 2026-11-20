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

    # ---------------------------------------------------------------- medallion
    "medallion-flow": f'''
<figure class="fig">
  <div class="arch">
    <div class="arch-col"><p class="arch-h">Sources</p>{step("Online shop", "JSON orders")}{step("Stock system", "CSV files")}{step("CRM", "customer export")}</div>
    <div class="arch-arrow" aria-hidden="true"></div>
    <div class="arch-col arch-col--fabric">
      <p class="arch-h arch-h--light">OneLake, one layer per lakehouse</p>
      {step("Bronze", "raw: stored exactly as it arrived", "dark")}
      {step("Silver", "cleaned: fixed, standardised, de-duplicated", "dark")}
      {step("Gold", "curated: shaped for reports", "dark")}
    </div>
    <div class="arch-arrow" aria-hidden="true"></div>
    <div class="arch-col"><p class="arch-h">People use</p>{step("Power BI reports", "", "gold")}{step("SQL queries", "", "gold")}{step("Excel analysis", "", "gold")}</div>
  </div>
  <figcaption>Data flows one way: it lands untouched in bronze, is cleaned in silver, and is shaped for reporting in gold. Reports read from gold only.</figcaption>
</figure>''',

    "medallion-data": f'''
<figure class="fig">
  <div class="tbl-grid">
    {table("Bronze: as it arrived", ["order_id", "order_date", "amount"], [["101", "03/11/2026", "120"], ["101", "03/11/2026", "120"], ["102", "2026-11-03", "80"], ["TEST1", "2026-11-03", "1"]], hl=(1, 3))}
    {table("Silver: cleaned", ["order_id", "order_date", "amount"], [["101", "2026-11-03", "120"], ["102", "2026-11-03", "80"]])}
  </div>
  <div class="tbl-grid tbl-grid--one">
    {table("Gold: ready for the report", ["order_date", "orders", "sales"], [["2026-11-03", "2", "200"]], hl=(0,))}
  </div>
  <figcaption>The same orders at each layer. Silver removes the duplicate and the test order and fixes the date format; gold summarises the clean rows into daily sales.</figcaption>
</figure>''',

    # ---------------------------------------------------------------- sql order of execution
    "sql-logical-order": f'''
<figure class="fig">
  <div class="tbl-grid">
    {table("As you write it", ["#", "clause"], [["1", "SELECT"], ["2", "FROM"], ["3", "WHERE"], ["4", "GROUP BY"], ["5", "HAVING"], ["6", "ORDER BY"]], hl=(0,))}
    {table("As SQL processes it", ["#", "clause", "what happens"], [["1", "FROM &amp; JOIN", "find the rows"], ["2", "WHERE", "filter rows"], ["3", "GROUP BY", "make groups"], ["4", "HAVING", "filter groups"], ["5", "SELECT", "calculate columns, name aliases"], ["6", "DISTINCT", "remove duplicates"], ["7", "ORDER BY", "sort"], ["8", "TOP / LIMIT", "keep the first rows"]], hl=(4,))}
  </div>
  <figcaption>You write SELECT first, but SQL works it out almost last. Anything named in SELECT, such as an alias, doesn't exist yet for WHERE, GROUP BY or HAVING. It does exist for ORDER BY.</figcaption>
</figure>''',

    "sql-where-having": f'''
<figure class="fig">
  <div class="tbl-grid">
    {table("1. WHERE status = 'Complete'", ["order_id", "region", "value", "status"], [["2", "North", "400", "Complete"], ["3", "South", "100", "Cancelled"], ["4", "South", "300", "Complete"], ["6", "East", "25", "Complete"]], hl=(1,))}
    {table("2. GROUP BY region", ["region", "sales"], [["North", "800"], ["South", "660"], ["East", "75"]])}
  </div>
  <div class="tbl-grid tbl-grid--one">
    {table("3. HAVING SUM(...) &gt; 200", ["region", "sales"], [["North", "800"], ["South", "660"]], hl=(0, 1))}
  </div>
  <figcaption>WHERE removes individual rows before grouping (the cancelled order goes). GROUP BY then totals what is left, and HAVING removes whole groups afterwards (East, at 75, goes). Only some of the orders are shown in step 1.</figcaption>
</figure>''',
}
