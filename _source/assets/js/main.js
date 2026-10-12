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

  /* Currency switcher: prices are set in GHS and estimated in the visitor's currency */
  const curSelect = document.querySelector("[data-currency-select]");
  if (curSelect) {
    const BASE = "GHS";
    const CURRENCIES = {
      GHS: "Ghana cedi", NGN: "Nigerian naira", USD: "US dollar", GBP: "British pound", EUR: "Euro",
      CAD: "Canadian dollar", KES: "Kenyan shilling", ZAR: "South African rand", XOF: "West African CFA franc",
      XAF: "Central African CFA franc", UGX: "Ugandan shilling", TZS: "Tanzanian shilling", RWF: "Rwandan franc",
      AUD: "Australian dollar", AED: "UAE dirham", INR: "Indian rupee",
    };
    // Fallback rates (1 GHS = x), from ExchangeRate-API on 11 Oct 2026; replaced by live rates when available.
    let rates = { GHS: 1, NGN: 114.883963, GBP: 0.063997, USD: 0.08466, EUR: 0.075587, CAD: 0.12073, KES: 10.985664, ZAR: 1.401013, XOF: 49.581951 };
    let updated = "11 Oct 2026";
    const TZ_MAP = {
      "Africa/Lagos": "NGN", "Africa/Accra": "GHS", "Europe/London": "GBP", "Africa/Nairobi": "KES",
      "Africa/Johannesburg": "ZAR", "Africa/Abidjan": "XOF", "Africa/Dakar": "XOF", "Africa/Lome": "XOF",
      "Africa/Douala": "XAF", "Africa/Kampala": "UGX", "Africa/Dar_es_Salaam": "TZS", "Africa/Kigali": "RWF",
      "Asia/Dubai": "AED", "Asia/Kolkata": "INR", "Asia/Calcutta": "INR",
    };
    const detect = () => {
      try { const saved = localStorage.getItem("iwd-currency"); if (saved && CURRENCIES[saved]) return saved; } catch (e) {}
      const tz = Intl.DateTimeFormat().resolvedOptions().timeZone || "";
      if (TZ_MAP[tz]) return TZ_MAP[tz];
      if (/^America\/(Toronto|Vancouver|Edmonton|Winnipeg|Halifax|Regina|St_Johns|Montreal)/.test(tz)) return "CAD";
      if (tz.startsWith("America/")) return "USD";
      if (tz.startsWith("Australia/")) return "AUD";
      if (tz.startsWith("Europe/")) return "EUR";
      return "GHS";
    };
    let current = detect();
    const fmt = (amount, cur) => {
      try {
        return new Intl.NumberFormat("en-GB", { style: "currency", currency: cur, currencyDisplay: "narrowSymbol", maximumFractionDigits: 0 }).format(amount);
      } catch (e) { return cur + " " + Math.round(amount).toLocaleString("en-GB"); }
    };
    const round = (v, cur) => (cur === BASE ? v : v >= 10000 ? Math.round(v / 100) * 100 : v >= 1000 ? Math.round(v / 10) * 10 : Math.round(v));
    const note = document.querySelector("[data-fx-note]");
    const field = document.querySelector("[data-currency-field]");
    const fill = () => {
      curSelect.innerHTML = Object.keys(CURRENCIES).filter((c) => rates[c]).map((c) => `<option value="${c}"${c === current ? " selected" : ""}>${c} · ${CURRENCIES[c]}</option>`).join("");
    };
    const render = () => {
      if (!rates[current]) current = "GHS";
      const r = rates[current];
      document.querySelectorAll("[data-price-ghs]").forEach((el) => {
        const ghs = +el.dataset.priceGhs;
        el.textContent = current === BASE ? "GH₵" + ghs.toLocaleString("en-GB") : "≈ " + fmt(round(ghs * r, current), current);
        el.title = current === BASE ? "" : "GH₵" + ghs.toLocaleString("en-GB");
      });
      document.querySelectorAll("s [data-price-ghs]").forEach((el) => (el.textContent = el.textContent.replace("≈ ", "")));
      if (field) field.value = current;
      if (note) {
        note.innerHTML = current === BASE
          ? "Prices are set in Ghana cedis (GH₵). Choose your currency above to see an estimate."
          : `Estimated at GH₵1 = ${current} ${r < 1 ? r.toFixed(4) : r.toFixed(2)} (rates updated ${updated}). You pay in Ghana cedis; your bank's rate may differ slightly. ` +
            `<a href="https://www.oanda.com/currency-converter/en/?from=GHS&to=${current}&amount=1500" target="_blank" rel="noopener">Check on OANDA</a> · <a href="https://www.exchangerate-api.com" target="_blank" rel="noopener">Rates by Exchange Rate API</a>`;
      }
    };
    curSelect.addEventListener("change", () => {
      current = curSelect.value;
      try { localStorage.setItem("iwd-currency", current); } catch (e) {}
      render();
    });
    fill(); render();
    fetch("https://open.er-api.com/v6/latest/GHS")
      .then((r) => r.json())
      .then((d) => {
        if (d && d.result === "success" && d.rates) {
          rates = { ...rates, ...d.rates, GHS: 1 };
          const t = new Date(d.time_last_update_unix * 1000);
          if (!isNaN(t)) updated = t.toLocaleDateString("en-GB", { day: "numeric", month: "short", year: "numeric" });
          fill(); render();
        }
      })
      .catch(() => {});
  }

  /* Programme buttons pre-select the programme in the application form */
  const progSelect = document.querySelector("[data-programme-select]");
  if (progSelect) {
    document.querySelectorAll("[data-choose]").forEach((b) =>
      b.addEventListener("click", () => {
        const want = b.dataset.choose.replace(/&amp;/g, "&").toLowerCase();
        const opt = [...progSelect.options].find((o) => o.text.toLowerCase().startsWith(want));
        if (opt) progSelect.value = opt.value;
      })
    );
  }

  /* Footer year */
  document.querySelectorAll("[data-year]").forEach((el) => (el.textContent = new Date().getFullYear()));
})();
