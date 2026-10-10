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
          const res = await fetch(endpoint, { method: "POST", body: data, headers: { Accept: "application/json" } });
          if (!res.ok) throw new Error();
          form.reset();
          say("Thank you — your message has been sent. We'll be in touch soon.");
        } catch {
          say("Sorry, something went wrong. Please email or WhatsApp us directly.", true);
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

  /* Footer year */
  document.querySelectorAll("[data-year]").forEach((el) => (el.textContent = new Date().getFullYear()));
})();
