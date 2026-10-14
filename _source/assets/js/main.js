/* Intelligence With Data — site behaviour */
(function () {
  document.documentElement.classList.remove("no-js");

  /* Mobile navigation */
  const toggle = document.querySelector("[data-nav-toggle]");
  const menu = document.querySelector("[data-nav-menu]");
  if (toggle && menu) {
    toggle.addEventListener("click", () => {
      const open = toggle.getAttribute("aria-expanded") === "true";
      toggle.setAttribute("aria-expanded", String(!open));
      menu.classList.toggle("is-open", !open);
    });
    menu.querySelectorAll("a").forEach((a) =>
      a.addEventListener("click", () => {
        toggle.setAttribute("aria-expanded", "false");
        menu.classList.remove("is-open");
      })
    );
  }

  /* Keep the page still while a dropdown is used (some mobile browsers jump to the top) */
  document.querySelectorAll("form select").forEach((sel) => {
    let keep = null;
    const save = () => { keep = window.scrollY; };
    const restore = () => {
      if (keep === null) return;
      const y = keep;
      requestAnimationFrame(() => { if (Math.abs(window.scrollY - y) > 150) window.scrollTo({ top: y, behavior: "instant" }); });
      setTimeout(() => { if (Math.abs(window.scrollY - y) > 150) window.scrollTo({ top: y, behavior: "instant" }); keep = null; }, 350);
    };
    sel.addEventListener("pointerdown", save);
    sel.addEventListener("focus", () => { if (keep === null) save(); });
    sel.addEventListener("change", restore);
    sel.addEventListener("blur", restore);
  });

  /* Header shade on scroll */
  const header = document.querySelector("[data-header]");
  const onScroll = () => header && header.classList.toggle("is-scrolled", window.scrollY > 10);
  window.addEventListener("scroll", onScroll, { passive: true });
  onScroll();

  /* Reveal on scroll */
  const reveals = document.querySelectorAll(".reveal");
  if ("IntersectionObserver" in window) {
    const io = new IntersectionObserver(
      (entries) =>
        entries.forEach((e) => {
          if (e.isIntersecting) {
            e.target.classList.add("is-visible");
            io.unobserve(e.target);
          }
        }),
      { threshold: 0.12, rootMargin: "0px 0px -40px 0px" }
    );
    reveals.forEach((el) => io.observe(el));
  } else {
    reveals.forEach((el) => el.classList.add("is-visible"));
  }

  /* Time-savings calculator */
  const calc = document.querySelector("[data-calc]");
  if (calc) {
    const num = new Intl.NumberFormat("en-GB");
    const gbp = new Intl.NumberFormat("en-GB", { style: "currency", currency: "GBP", maximumFractionDigits: 0 });
    const AUTOMATION_SHARE = 0.8;
    const val = (n) => parseFloat(calc.querySelector(`[name="${n}"]`).value);
    const set = (k, v) => (calc.querySelector(`[data-result="${k}"]`).textContent = v);
    const update = () => {
      calc.querySelectorAll('input[type="range"]').forEach((r) => {
        const pct = ((r.value - r.min) / (r.max - r.min)) * 100;
        r.style.setProperty("--pct", pct + "%");
        const out = calc.querySelector(`[data-out="${r.name}"]`);
        if (out) {
          const v = parseFloat(r.value);
          out.textContent = r.name === "rate" ? gbp.format(v) : r.name === "hours" ? v + " hrs" : v;
        }
      });
      const current = val("reports") * val("hours") * val("runs") * 12;
      const saved = current * AUTOMATION_SHARE;
      set("current", num.format(Math.round(current)));
      set("saved", num.format(Math.round(saved)));
      set("value", gbp.format(saved * val("rate")));
    };
    calc.addEventListener("input", update);
    update();
  }

  /* Contact form
     - If the form has data-endpoint (e.g. a Formspree URL), it posts there.
     - Otherwise it opens the visitor's email app with the message pre-filled. */
  const form = document.querySelector("[data-contact-form]");
  if (form) {
    const status = form.querySelector(".form-status");
    const say = (msg, err) => {
      status.textContent = msg;
      status.classList.toggle("is-error", !!err);
    };
    form.addEventListener("submit", async (e) => {
      e.preventDefault();
      if (!form.reportValidity()) return;
      const data = new FormData(form);
      window.IWD_lastEmail = data.get("email") || "";
      const endpoint = (form.dataset.endpoint || "").trim();
      if (endpoint) {
        try {
          const btn = form.querySelector("button[type=submit]");
        btn.disabled = true;
        say("Sending…");
        const res = await fetch(endpoint, { method: "POST", body: data, headers: { Accept: "application/json" } });
          if (!res.ok) throw new Error();
          form.reset();
          say("Thank you — your message has been sent. We'll be in touch soon.");
          const ok = form.querySelector("[data-apply-success]");
          if (ok && window.IWD_showPayment) window.IWD_showPayment(ok);
          if (ok) {
            [...form.children].forEach((el) => { if (el !== ok && el.type !== "hidden") el.hidden = true; });
            ok.hidden = false;
            ok.scrollIntoView({ behavior: "smooth", block: "center" });
          }
        } catch {
          say("Sorry, something went wrong. Please email or WhatsApp us directly.", true);
        } finally {
          form.querySelector("button[type=submit]").disabled = false;
        }
        return;
      }
      const subject = `Enquiry: ${data.get("interest")} — ${data.get("name")}`;
      const body =
        `Name: ${data.get("name")}\nEmail: ${data.get("email")}\nCompany: ${data.get("company") || "-"}\n` +
        `Interested in: ${data.get("interest")}\n\n${data.get("message")}`;
      window.location.href = `mailto:${form.dataset.email}?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`;
      say("Your email app should now open with your message ready to send.");
    });
  }

  /* Next-session countdown: every Friday 18:00 Europe/London */
  const cd = document.querySelector("[data-countdown]");
  if (cd) {
    const TZ = "Europe/London", DAY = 5, HOUR = 18, LIVE_MINUTES = 90;
    const londonParts = (d) => {
      const p = {};
      new Intl.DateTimeFormat("en-GB", { timeZone: TZ, hourCycle: "h23", year: "numeric", month: "numeric", day: "numeric", hour: "numeric", minute: "numeric", second: "numeric" })
        .formatToParts(d).forEach((x) => (p[x.type] = +x.value));
      return p;
    };
    // UTC instant for a London wall-clock time (handles BST/GMT)
    const londonToUtc = (y, m, d, h) => {
      const guess = Date.UTC(y, m - 1, d, h);
      const p = londonParts(new Date(guess));
      const offset = Date.UTC(p.year, p.month - 1, p.day, p.hour, p.minute) - guess;
      return new Date(guess - offset);
    };
    const nextSession = (now) => {
      for (let i = 0; i < 8; i++) {
        const day = new Date(now.getTime() + i * 864e5);
        const p = londonParts(day);
        const wd = new Date(Date.UTC(p.year, p.month - 1, p.day)).getUTCDay();
        if (wd !== DAY) continue;
        const start = londonToUtc(p.year, p.month, p.day, HOUR);
        if (now < new Date(start.getTime() + LIVE_MINUTES * 6e4)) return start;
      }
    };
    const box = cd.querySelector(".countdown");
    const els = { d: cd.querySelector('[data-cd="d"]'), h: cd.querySelector('[data-cd="h"]'), m: cd.querySelector('[data-cd="m"]'), s: cd.querySelector('[data-cd="s"]') };
    let start = nextSession(new Date());
    const fmt = (opts) => new Intl.DateTimeFormat("en-GB", opts).format(start);
    const label = () => {
      cd.querySelector("[data-next-date]").textContent = fmt({ timeZone: TZ, weekday: "long", day: "numeric", month: "long" }) + ", 6:00 PM UK";
      const userTz = Intl.DateTimeFormat().resolvedOptions().timeZone;
      const local = cd.querySelector("[data-local-time]");
      if (userTz && userTz !== TZ && fmt({ timeZone: userTz, hour: "numeric", minute: "2-digit" }) !== fmt({ timeZone: TZ, hour: "numeric", minute: "2-digit" })) {
        local.textContent = "That's " + new Intl.DateTimeFormat(undefined, { weekday: "long", hour: "numeric", minute: "2-digit", timeZoneName: "short" }).format(start) + " where you are";
      } else local.textContent = "Live on Google Meet";
    };
    const pad = (n) => String(n).padStart(2, "0");
    const tick = () => {
      const now = new Date();
      if (now - start > LIVE_MINUTES * 6e4) { start = nextSession(now); label(); }
      const diff = start - now;
      if (diff > 0 && box.classList.contains("is-live")) return location.reload();
      if (diff <= 0) {
        box.classList.add("is-live");
        box.textContent = "Live now. Register to get the joining link.";
        return;
      }
      const t = Math.floor(diff / 1000);
      els.d.textContent = pad(Math.floor(t / 86400));
      els.h.textContent = pad(Math.floor((t % 86400) / 3600));
      els.m.textContent = pad(Math.floor((t % 3600) / 60));
      els.s.textContent = pad(t % 60);
    };
    if (start) { label(); tick(); setInterval(tick, 1000); }
  }

  /* Sticky register bar (mobile) after the hero scrolls away */
  const sticky = document.querySelector("[data-sticky-reg]");
  const heroEl = document.querySelector(".free-hero");
  if (sticky && heroEl && "IntersectionObserver" in window) {
    new IntersectionObserver(([e]) => sticky.classList.toggle("is-shown", !e.isIntersecting)).observe(heroEl);
  }

  /* Insights filter */
  const grid = document.querySelector("[data-post-grid]");
  if (grid) {
    const chips = document.querySelectorAll(".chip[data-filter]");
    const empty = document.querySelector("[data-no-posts]");
    chips.forEach((chip) =>
      chip.addEventListener("click", () => {
        chips.forEach((c) => c.classList.toggle("is-active", c === chip));
        let shown = 0;
        grid.querySelectorAll(".post-card").forEach((card) => {
          const all = chip.dataset.filter === "all";
          const ok = all ? !card.hasAttribute("data-featured") : card.dataset.cat === chip.dataset.filter;
          card.hidden = !ok;
          if (ok) { card.classList.add("is-visible"); shown++; }
        });
        if (empty) empty.hidden = shown > 0;
      })
    );
  }

  /* Article: reading progress, active TOC, copy link */
  const article = document.querySelector("[data-article]");
  if (article) {
    const bar = document.querySelector("[data-read-progress]");
    const tocLinks = [...document.querySelectorAll(".toc a")];
    const heads = tocLinks.map((a) => document.getElementById(a.hash.slice(1))).filter(Boolean);
    const onRead = () => {
      const r = article.getBoundingClientRect();
      const pct = Math.min(1, Math.max(0, -r.top / (r.height - window.innerHeight)));
      if (bar) bar.style.width = pct * 100 + "%";
      let current = heads[0];
      heads.forEach((h) => { if (h.getBoundingClientRect().top < 140) current = h; });
      tocLinks.forEach((a) => a.classList.toggle("is-active", current && a.hash === "#" + current.id));
    };
    window.addEventListener("scroll", onRead, { passive: true });
    onRead();
    document.querySelectorAll("[data-copy-link]").forEach((b) =>
      b.addEventListener("click", async () => {
        try { await navigator.clipboard.writeText(b.dataset.copyLink); b.textContent = "Copied"; }
        catch { b.textContent = "Copy failed"; }
        setTimeout(() => (b.textContent = "Copy"), 1800);
      })
    );
  }

  /* ---------- Paid programmes page: currency, plan calculator, cohorts ---------- */
  const curSelect = document.querySelector("[data-currency-select]");
  if (curSelect) {
    const BASE = "USD";
    const CURRENCIES = {
      USD: "US dollar", NGN: "Nigerian naira", GHS: "Ghana cedi", GBP: "British pound", EUR: "Euro",
      CAD: "Canadian dollar", KES: "Kenyan shilling", ZAR: "South African rand", XOF: "West African CFA franc",
      XAF: "Central African CFA franc", UGX: "Ugandan shilling", TZS: "Tanzanian shilling", RWF: "Rwandan franc",
      AUD: "Australian dollar", AED: "UAE dirham", INR: "Indian rupee",
    };
    // Fallback rates (1 USD = x), derived from ExchangeRate-API data of 11 Oct 2026; replaced by live rates when available.
    let rates = { USD: 1, GHS: 11.812, NGN: 1357.0, GBP: 0.7559, EUR: 0.8928, CAD: 1.4261, KES: 129.76, ZAR: 16.549, XOF: 585.66 };
    let updated = "11 Oct 2026";
    const TZ_MAP = {
      "Africa/Lagos": "NGN", "Africa/Accra": "GHS", "Europe/London": "GBP", "Africa/Nairobi": "KES",
      "Africa/Johannesburg": "ZAR", "Africa/Abidjan": "XOF", "Africa/Dakar": "XOF", "Africa/Lome": "XOF",
      "Africa/Douala": "XAF", "Africa/Kampala": "UGX", "Africa/Dar_es_Salaam": "TZS", "Africa/Kigali": "RWF",
      "Asia/Dubai": "AED", "Asia/Kolkata": "INR", "Asia/Calcutta": "INR",
    };
    const detect = () => {
      try { const saved = localStorage.getItem("iwd-currency-v2"); if (saved && CURRENCIES[saved]) return saved; } catch (e) {}
      const tz = Intl.DateTimeFormat().resolvedOptions().timeZone || "";
      if (TZ_MAP[tz]) return TZ_MAP[tz];
      if (/^America\/(Toronto|Vancouver|Edmonton|Winnipeg|Halifax|Regina|St_Johns|Montreal)/.test(tz)) return "CAD";
      if (tz.startsWith("Australia/")) return "AUD";
      if (tz.startsWith("Europe/")) return "EUR";
      return "USD";
    };
    let current = detect();
    const fmt = (amount, cur) => {
      try {
        const narrow = ["USD", "NGN", "GHS", "GBP", "EUR", "INR"].includes(cur);   // unambiguous symbols; others e.g. CA$, A$
        return new Intl.NumberFormat("en-GB", { style: "currency", currency: cur, currencyDisplay: narrow ? "narrowSymbol" : "symbol", maximumFractionDigits: 0 }).format(amount);
      } catch (e) { return cur + " " + Math.round(amount).toLocaleString("en-GB"); }
    };
    const round = (v, cur) => (cur === BASE ? Math.round(v) : v >= 10000 ? Math.round(v / 100) * 100 : v >= 1000 ? Math.round(v / 10) * 10 : Math.round(v));
    const show = (usd, cur = current) => (cur === BASE ? fmt(usd, BASE) : "≈ " + fmt(round(usd * rates[cur], cur), cur));
    const note = document.querySelector("[data-fx-note]");
    const field = document.querySelector("[data-currency-field]");
    const fill = () => {
      curSelect.innerHTML = Object.keys(CURRENCIES).filter((c) => rates[c]).map((c) => `<option value="${c}"${c === current ? " selected" : ""}>${c} · ${CURRENCIES[c]}</option>`).join("");
    };

    /* Plan calculator */
    const RATE = window.IWD_INTERNSHIP_RATE || 0.4;
    const progSel = document.querySelector("[data-programme-select]");
    const internSel = document.querySelector("[data-internship-select]");
    const plan = () => {
      if (!progSel) return;
      const opt = progSel.selectedOptions[0];
      const course = +opt.dataset.usd;
      const CAP = window.IWD_INTERNSHIP_CAP || Infinity;
      const intern = internSel && internSel.value === "yes" ? Math.min(Math.round(course * RATE), CAP) : 0;
      const total = course + intern;
      const q = (sel) => document.querySelector(sel);
      q("[data-plan-name]").textContent = opt.text.replace(/\s*\(\$.*\)$/, "") + (intern ? " + remote internship" : "");
      q("[data-plan-course]").textContent = show(course);
      q("[data-plan-intern-row]").hidden = !intern;
      q("[data-plan-intern]").textContent = show(intern);
      q("[data-plan-sum]").textContent = show(total);
      q("[data-total-field]").value = "$" + total;
      window.IWD_lastPlan = { prog: progSel.value, intern: internSel ? internSel.value : "no", usd: total };
      q("[data-total-display-field]").value = show(total);
    };

    const render = () => {
      if (!rates[current]) current = BASE;
      document.querySelectorAll("[data-price-usd]").forEach((el) => {
        const usd = +el.dataset.priceUsd;
        el.textContent = show(usd);
        el.title = current === BASE ? "" : "US$" + usd.toLocaleString("en-GB");
      });
      document.querySelectorAll("s [data-price-usd]").forEach((el) => (el.textContent = el.textContent.replace("≈ ", "")));
      if (field) field.value = current;
      if (note) {
        const r = rates[current];
        note.innerHTML = current === BASE
          ? "Prices are set in US dollars. Choose your currency above to see an estimate."
          : `Estimated at US$1 = ${current} ${r < 1 ? r.toFixed(4) : r.toFixed(2)} (rates updated ${updated}). Your bank's rate may differ slightly. ` +
            `<a href="https://www.oanda.com/currency-converter/en/?from=USD&to=${current}&amount=1" target="_blank" rel="noopener">Check on OANDA</a> · <a href="https://www.exchangerate-api.com" target="_blank" rel="noopener">Rates by Exchange Rate API</a>`;
      }
      plan();
    };
    curSelect.addEventListener("change", () => {
      current = curSelect.value;
      try { localStorage.setItem("iwd-currency-v2", current); } catch (e) {}
      render();
    });
    [progSel, internSel].forEach((el) => el && el.addEventListener("change", plan));
    document.querySelectorAll("[data-choose]").forEach((b) => b.addEventListener("click", () => { if (progSel) { progSel.value = b.dataset.choose; plan(); } }));
    document.querySelectorAll("[data-internship]").forEach((b) => b.addEventListener("click", () => { if (internSel) { internSel.value = "yes"; plan(); } }));
    /* Payment routing: Africa -> Paystack (NGN, or GHS when available); UK -> Stripe GBP; elsewhere -> Stripe USD */
    window.IWD_showPayment = (panel) => {
      const PAY = window.IWD_PAY || {};
      const tz = Intl.DateTimeFormat().resolvedOptions().timeZone || "";
      const AFRICA = ["NGN", "GHS", "KES", "ZAR", "XOF", "XAF", "UGX", "TZS", "RWF"];
      const inAfrica = tz.startsWith("Africa/") || AFRICA.includes(current);
      const inGhana = tz === "Africa/Accra" || current === "GHS";
      const inUK = tz === "Europe/London" || current === "GBP";
      const usd = +(document.querySelector("[data-total-field]").value || "0").replace(/[^0-9.]/g, "");
      const lp = window.IWD_lastPlan || {};
      let route = null;
      if (inAfrica && inGhana && PAY.ghs && rates.GHS) route = { url: PAY.ghs, cur: "GHS", provider: "Paystack", step: 10 };
      else if (inAfrica && PAY.ngn && rates.NGN) route = { url: PAY.ngn, cur: "NGN", provider: "Paystack", step: 100 };
      else if (!inAfrica && PAY.stripe && PAY.stripe[`${lp.prog}|${lp.intern}`]) {
        const em = window.IWD_lastEmail ? "?prefilled_email=" + encodeURIComponent(window.IWD_lastEmail) : "";
        route = { url: PAY.stripe[`${lp.prog}|${lp.intern}`] + em, cur: "USD", provider: "Stripe", step: 1, fixed: true };
      }
      const block = panel.querySelector("[data-pay-block]");
      const later = panel.querySelector("[data-pay-later]");
      if (!route || !usd) { block.hidden = true; later.hidden = false; return; }
      const amount = route.fixed ? usd : Math.ceil((usd * rates[route.cur]) / route.step) * route.step;
      const text = fmt(amount, route.cur);
      block.hidden = false; later.hidden = true;
      panel.querySelector("[data-pay-amount]").textContent = text;
      if (route.fixed) {
        block.hidden = false; later.hidden = true;
        const local = current !== "USD" && rates[current] ? ` (${show(usd)})` : "";
        panel.querySelector("[data-pay-amount]").textContent = "US$" + usd + local;
        panel.querySelector("[data-pay-hint]").textContent = "Your price is already set on the secure checkout. Stripe shows it in your local currency where available (for example GBP in the UK).";
        panel.querySelector("[data-pay-label]").textContent = "Pay securely with card";
        panel.querySelector("[data-pay-provider]").textContent = "Stripe";
        panel.querySelector("[data-pay-link]").href = route.url;
        return;
      }
      const inNigeria = tz === "Africa/Lagos" || current === "NGN";
      panel.querySelector("[data-pay-hint]").textContent = route.cur === "NGN" && !inNigeria
        ? `Enter exactly ${text} on the payment page (US$${usd}). Pay by card; your bank converts it from your local currency automatically.`
        : `Enter exactly ${text} on the payment page. Equivalent to US$${usd} at today's rate.`;
      panel.querySelector("[data-pay-label]").textContent = "Pay " + text + " securely";
      panel.querySelector("[data-pay-provider]").textContent = route.provider;
      panel.querySelector("[data-pay-link]").href = route.url;
    };

    fill(); render();
    fetch("https://open.er-api.com/v6/latest/USD")
      .then((r) => r.json())
      .then((d) => {
        if (d && d.result === "success" && d.rates) {
          rates = { ...rates, ...d.rates, USD: 1 };
          const t = new Date(d.time_last_update_unix * 1000);
          if (!isNaN(t)) updated = t.toLocaleDateString("en-GB", { day: "numeric", month: "short", year: "numeric" });
          fill(); render();
        }
      })
      .catch(() => {});

    /* Cohorts: every N weeks from a fixed first Saturday, 10:00–13:00 Europe/London */
    const TZ = "Europe/London";
    const londonOffsetMs = (utcMs) => {
      const p = {};
      new Intl.DateTimeFormat("en-GB", { timeZone: TZ, hourCycle: "h23", year: "numeric", month: "numeric", day: "numeric", hour: "numeric", minute: "numeric" })
        .formatToParts(new Date(utcMs)).forEach((x) => (p[x.type] = +x.value));
      return Date.UTC(p.year, p.month - 1, p.day, p.hour, p.minute) - utcMs;
    };
    const CFG = window.IWD_COHORT || { first: "2026-11-07", everyWeeks: 6 };
    const ukStart = (y, m, d) => { const guess = Date.UTC(y, m, d, 10); return new Date(guess - londonOffsetMs(guess)); };
    const [fy, fm, fd] = CFG.first.split("-").map(Number);
    // Christmas break: no sessions from 20 Dec to 4 Jan. A cohort whose six Saturdays touch the break
    // moves to the first Saturday after it, and the six-week cycle continues from there.
    const DAY = 864e5;
    const inBreak = (t) => { const d = new Date(t); const m = d.getUTCMonth(), day = d.getUTCDate(); return (m === 11 && day >= 20) || (m === 0 && day <= 4); };
    const firstSatAfterBreak = (t) => { const y = new Date(t).getUTCMonth() === 11 ? new Date(t).getUTCFullYear() + 1 : new Date(t).getUTCFullYear(); let x = Date.UTC(y, 0, 5, 12); while (new Date(x).getUTCDay() !== 6) x += DAY; return x; };
    const now = new Date();
    const cohorts = [];
    let t = Date.UTC(fy, fm - 1, fd, 12);
    for (let guard = 0; cohorts.length < 3 && guard < 400; guard++) {
      const sats = Array.from({ length: 6 }, (_, i) => t + i * 7 * DAY);
      const clash = sats.find(inBreak);
      if (clash) { t = firstSatAfterBreak(clash); continue; }
      const c = new Date(t);
      const d = ukStart(c.getUTCFullYear(), c.getUTCMonth(), c.getUTCDate());
      if (d > now) cohorts.push(d);
      t += CFG.everyWeeks * 7 * DAY;
    }
    const dayFmt = (d) => d.toLocaleDateString("en-GB", { timeZone: TZ, weekday: "long", day: "numeric", month: "long", year: "numeric" });
    const nextEl = document.querySelector("[data-next-cohort]");
    if (nextEl && cohorts[0]) {
      nextEl.textContent = dayFmt(cohorts[0]);
      const userTz = Intl.DateTimeFormat().resolvedOptions().timeZone;
      const local = document.querySelector("[data-cohort-local]");
      const ukT = cohorts[0].toLocaleTimeString("en-GB", { timeZone: TZ, hour: "numeric", minute: "2-digit" });
      const loT = userTz ? cohorts[0].toLocaleTimeString("en-GB", { timeZone: userTz, hour: "numeric", minute: "2-digit" }) : ukT;
      if (local) local.textContent = userTz && loT !== ukT
        ? `10:00–13:00 UK time · ${new Intl.DateTimeFormat(undefined, { hour: "numeric", minute: "2-digit", timeZoneName: "short" }).format(cohorts[0])} where you are`
        : "Saturdays, 10:00–13:00 UK time";
    }
    const cohortSel = document.querySelector("[data-cohort-select]");
    if (cohortSel) cohortSel.innerHTML = cohorts.map((d) => `<option>${dayFmt(d)}</option>`).join("") + "<option>Not sure yet</option>";
  }

  /* Footer year */
  document.querySelectorAll("[data-year]").forEach((el) => (el.textContent = new Date().getFullYear()));
})();
