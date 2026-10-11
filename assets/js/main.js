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

  /* Footer year */
  document.querySelectorAll("[data-year]").forEach((el) => (el.textContent = new Date().getFullYear()));
})();
