# Intelligence With Data — Website

Premium static website for **Intelligence With Data Ltd** (Power BI & Microsoft Fabric consultancy, training and careers).
Plain HTML, CSS and JavaScript — no build tools, no frameworks — so it runs directly on **GitHub Pages**.

## Pages

| File | Page |
|---|---|
| `index.html` | Home — hero, services, process, time-savings calculator, training teaser |
| `services.html` | Consulting — report automation, Fabric, upskilling, AI & prompting, contract support, FAQ |
| `training.html` | Training & careers — coaching, internship, bootcamps, Analytics Hub, Kids in Tech |
| `about.html` | Founder story, credentials, principles |
| `contact.html` | Enquiry form, email, phone, WhatsApp |
| `404.html` | Not-found page (GitHub Pages uses it automatically) |

Shared files: `assets/css/styles.css`, `assets/js/main.js`, `assets/img/favicon.svg`.

## Publish on GitHub Pages (about 5 minutes)

1. Sign in to GitHub and create a new **public** repository, e.g. `iwd-website`.
2. Click **Add file → Upload files**, drag in **everything inside this folder** (including the `assets` folder and the hidden `.nojekyll` file), then **Commit changes**.
3. Go to **Settings → Pages**. Under *Build and deployment*, choose **Deploy from a branch**, branch **main**, folder **/ (root)**, then **Save**.
4. After a minute your site is live at `https://<your-username>.github.io/iwd-website/`.

> Tip: on a Mac, press `Cmd + Shift + .` in Finder to show hidden files like `.nojekyll`.

## Use your own domain (intelligencewithdata.com)

1. In **Settings → Pages → Custom domain**, enter `www.intelligencewithdata.com` and save (GitHub adds a `CNAME` file).
2. At your domain registrar, add DNS records:
   - `CNAME` record: `www` → `<your-username>.github.io`
   - `A` records for the root domain `@` → `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`
3. Once DNS has updated, tick **Enforce HTTPS**.

## Make the contact form deliver to your inbox

By default the form opens the visitor's email app pre-filled to `training@intelligencewithdata.com`.
To receive submissions directly instead:

1. Create a free form at [formspree.io](https://formspree.io) and copy its endpoint URL.
2. In `contact.html`, find `data-endpoint=""` and paste the URL between the quotes.

To change the destination email, edit `data-email="…"` on the same line.

## Common edits

- **Colours:** top of `assets/css/styles.css` (`--navy`, `--blue`, `--gold` …).
- **Calculator assumption (80% automation):** `AUTOMATION_SHARE` in `assets/js/main.js`.
- **Contact details:** search all files for `7344` or `training@`.
