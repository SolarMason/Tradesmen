# NEPA-PRO Tradesmen

> **Skilled trade labor on subscription.** The first labor-as-a-service marketplace built for contractors in Northeast Pennsylvania.

[![Deploy](https://github.com/SolarMason/tradesmen-nepa-pro/actions/workflows/deploy.yml/badge.svg)](https://github.com/SolarMason/tradesmen-nepa-pro/actions/workflows/deploy.yml)
[![Live Site](https://img.shields.io/badge/live-tradesmen.nepa--pro.com-4a9eff)](https://tradesmen.nepa-pro.com/)
[![PWA](https://img.shields.io/badge/PWA-installable-ff6b35)](https://web.dev/articles/pwa-checklist)

A single-page Progressive Web App that lets contractors book vetted, insured tradespeople by the half-day, full day, or week — with all workers' compensation, payroll, and general liability covered by NEPA-PRO. 15 trades × 3 skill tiers × 3 durations = 135 Stripe-ready checkout SKUs.

![NEPA-PRO Tradesmen — social card](icons/og-card.png)

---

## Table of Contents

1. [Quick Start](#quick-start)
2. [Repository Layout](#repository-layout)
3. [Deployment to GitHub Pages](#deployment-to-github-pages)
4. [Custom Domain Setup](#custom-domain-setup)
5. [Wiring Stripe Payment Links](#wiring-stripe-payment-links)
6. [Adding or Editing Trades](#adding-or-editing-trades)
7. [Updating Branding & Icons](#updating-branding--icons)
8. [Local Development](#local-development)
9. [Service Worker & Cache Busting](#service-worker--cache-busting)
10. [SEO, Analytics, and Schema](#seo-analytics-and-schema)
11. [Browser Support](#browser-support)
12. [Troubleshooting](#troubleshooting)

---

## Quick Start

```bash
git clone https://github.com/SolarMason/tradesmen-nepa-pro.git
cd tradesmen-nepa-pro

# Serve locally (any static server works — pick one)
python3 -m http.server 8080
# or:  npx serve .
# or:  php -S localhost:8080

# Open http://localhost:8080
```

That's it. No build step, no `npm install`. The whole site is one HTML file plus assets.

---

## Repository Layout

```
tradesmen-nepa-pro/
├── .github/workflows/
│   └── deploy.yml              ← GitHub Actions → Pages deployment
├── _build/
│   ├── generate_icons.py       ← One-shot icon + OG card generator
│   ├── generate_skus.py        ← Emit all 135 SKUs as CSV for Stripe import
│   ├── qa.py                   ← Comprehensive 123-check QA suite
│   └── test_checkout.js        ← Headless test of all 135 checkout URLs
├── icons/
│   ├── favicon.ico             ← multi-resolution (16/32/48)
│   ├── favicon-16x16.png
│   ├── favicon-32x32.png
│   ├── favicon-48x48.png
│   ├── apple-touch-icon.png    ← iOS home screen (180×180)
│   ├── android-chrome-192x192.png
│   ├── android-chrome-512x512.png
│   ├── icon-maskable-192.png   ← Android adaptive
│   ├── icon-maskable-512.png
│   ├── mstile-150x150.png      ← Windows pinned tile
│   ├── mstile-310x310.png
│   ├── safari-pinned-tab.svg   ← Safari pinned tab (monochrome)
│   ├── og-card.png             ← OG / social share / business card (1200×630)
│   └── og-card-square.png      ← Square variant for IG / iMessage (1080×1080)
├── index.html                  ← The whole app (~98 KB)
├── manifest.webmanifest        ← PWA manifest
├── sw.js                       ← Service worker (offline shell)
├── skus.csv                    ← 135-row Stripe Payment Link import sheet
├── browserconfig.xml           ← Windows tile config
├── robots.txt
├── sitemap.xml
├── CNAME                       ← tradesmen.nepa-pro.com
├── LICENSE                     ← Proprietary, all rights reserved
└── README.md
```

### Pre-deploy QA

Run the full test suite locally before pushing:

```bash
python3 _build/qa.py            # 123 structural & runtime checks
node _build/test_checkout.js    # All 135 checkout URLs validated
```

Both must pass green before deploy.

---

## Deployment to GitHub Pages

The repo is configured for **GitHub Pages via Actions** (the modern flow Noel uses on Solar-Mason-Dev).

### One-time repo setup

1. **Create the repo** on GitHub (public or private both work; private requires Pro/Team for Pages).
   ```bash
   git remote add origin https://github.com/SolarMason/tradesmen-nepa-pro.git
   git push -u origin main
   ```

2. **Enable Pages → Actions** in the repo:
   - Settings → **Pages**
   - **Source:** *GitHub Actions* (not "Deploy from a branch")

3. **Add the deploy permissions secret if needed.** With the default `GITHUB_TOKEN` and the workflow's `permissions:` block, no PAT is required for new repos. If you're mirroring Noel's existing Solar-Mason-Dev pattern with a classic PAT, add it as `GH_PAGES_PAT` in *Settings → Secrets and variables → Actions* and edit the workflow's `actions/checkout@v4` step to use `token: ${{ secrets.GH_PAGES_PAT }}`.

### Every push to `main`

The workflow at [`.github/workflows/deploy.yml`](.github/workflows/deploy.yml) runs automatically:

1. Validates the required files (`index.html`, `manifest.webmanifest`, `sw.js`, `CNAME`, all icons).
2. Stamps the build SHA + UTC timestamp into the footer (replaces `<!--BUILD_STAMP-->`).
3. Uploads the entire repo as a Pages artifact.
4. Deploys to `tradesmen.nepa-pro.com`.

To trigger manually: *Actions → Deploy NEPA-PRO Tradesmen to GitHub Pages → Run workflow*.

---

## Custom Domain Setup

The `CNAME` file in the repo root tells GitHub Pages to serve from `tradesmen.nepa-pro.com`.

### DNS configuration

In Cloudflare (or whatever you use for `nepa-pro.com`), add:

| Type    | Name        | Target                  | Proxy   |
|---------|-------------|-------------------------|---------|
| `CNAME` | `tradesmen` | `solarmason.github.io`  | DNS-only* |

> *⚠️ Set Cloudflare to **DNS-only** (gray cloud) for the initial cert provisioning. After GitHub provisions the Let's Encrypt cert (~10–30 min), you can switch to proxied (orange cloud) if you want CF's edge caching in front. Keep "Always Use HTTPS" on.*

In **Settings → Pages**, set the custom domain to `tradesmen.nepa-pro.com` and tick **Enforce HTTPS**.

---

## Wiring Stripe Payment Links

The site has **no backend** — all checkout logic runs through Stripe Payment Links configured in the Stripe Dashboard. Each of the 135 trade × tier × duration SKUs gets one Payment Link.

### Required Payment Link configuration (per SKU)

In the Stripe Dashboard → **Payment Links → New** (or via Stripe API), set each link up like this:

| Setting | Value |
|---|---|
| **Product** | One product per SKU. Name format: *"Journeyman Electrician — Full Day (8h)"* |
| **Price** | Match the rate in `index.html` (rate × hours × multiplier) |
| **Collect customer's address** | ✅ **Shipping** (this is the jobsite) |
| **Collect phone number** | ✅ Required |
| **Custom field 1** | Label: *"Project description / scope of work"* · Type: **Text (long)** · Required |
| **Custom field 2** | Label: *"On-site contact name &amp; cell"* · Type: **Text (short)** · Required |
| **Custom field 3** | Label: *"Access notes — gate codes, parking, supervisor, dog warnings, etc."* · Type: **Text (long)** · Optional |
| **Confirmation page** | Redirect to `https://tradesmen.nepa-pro.com/?booked=1` |
| **Custom message** | *"We'll confirm your booking by phone within one business hour. Tradesperson dispatches to the shipping address on your selected start date."* |

> 💡 **Tip:** Build one "template" Payment Link in Stripe with all of the above, then use the Stripe Dashboard's *Duplicate* feature to clone it 134 times — change only the product, price, and name on each copy.

### Wiring the link IDs into the site

After creating each Payment Link, Stripe gives you a URL like `https://buy.stripe.com/cN200gawL2DfaiI288`. The `cN200gawL2DfaiI288` part is the **link ID**.

Open `index.html`, find the `STRIPE_LINKS` object (search for `STRIPE_LINKS = {`), and populate it:

```js
const STRIPE_LINKS = {
  // SKU format:  {trade-id}_{tier-id}_{duration-id}
  'electricians_apprentice_half':   '7sI3cs1JG3jFciYbIM',
  'electricians_apprentice_full':   'aEU14k7krfqb4Yo3cd',
  'electricians_apprentice_weekly': '00g7sI4VS9I3aaQ288',
  'electricians_journeyman_half':   'cN200gawL2DfaiI288',
  'electricians_journeyman_full':   'cN200gawL2DfaiI288',
  // … 130 more — one for each trade × tier × duration combination
};
```

The full SKU list (all 135) is documented in the comment block in `index.html` and can be regenerated by iterating `TRADES × TIERS × DURATIONS`.

### What happens until you wire the links

**Nothing breaks.** Until `STRIPE_LINKS` is populated, every "Book &amp; Pay" button gracefully falls back to a pre-filled `mailto:service@nepa-pro.com` email containing the trade, tier, duration, and quoted total — so dispatch can quote and book manually while you finish the Stripe setup. No dead links, no 404s.

### Reconciliation

Every successful Stripe checkout fires with a `client_reference_id` of `{sku}_{total}` — visible in the Stripe Dashboard payment record. That's how you match a payment back to the trade/tier/duration the contractor selected.

---

## Adding or Editing Trades

All trade data lives in a single `TRADES` array near the bottom of `index.html`. Each entry:

```js
{
  id:    'electricians',                      // URL-safe, used in Stripe SKU
  cat:   'electrical',                        // electrical | mechanical | structural | heavy
  name:  'Electricians',
  tagline: 'Resi & light commercial wiring.',
  desc:  'IBEW-grade inside wiremen…',
  rates: [58, 85, 115],                       // [apprentice, journeyman, master] $/hr billable
  icon:  'bolt'                               // key into ICONS object
}
```

**To add a trade:**

1. Append a new object to the `TRADES` array.
2. If it needs a new icon, add an SVG snippet to the `ICONS` object (24×24 viewBox, `stroke="currentColor"`).
3. Add a corresponding `<a class="mm-link" data-trade="newid">…</a>` to the desktop mega-menu (around the `<nav class="topnav">` block) so it appears in the dropdown.
4. Commit & push — the Action redeploys everything.

**To re-price:** just edit the `rates` array. The half-day / full-day / weekly totals and Stripe SKU references recompute automatically.

---

## Updating Branding & Icons

All icons + the OG card are generated from a single Python script.

```bash
# Edit the brand tokens / mark geometry in _build/generate_icons.py
python3 _build/generate_icons.py

# Output goes to /icons — review, then commit
git add icons/ && git commit -m "Refresh brand icons"
git push
```

The script generates **15 files** from the same vector primitives — no Photoshop or external service needed:

| File | Use |
|------|-----|
| `favicon.ico` | Browser tab |
| `favicon-{16,32,48}x.png` | High-DPI tab favicons |
| `apple-touch-icon.png` (180×180) | iOS home screen |
| `android-chrome-{192,512}.png` | Chrome Android |
| `icon-maskable-{192,512}.png` | Android adaptive icons (safe-zone padded) |
| `mstile-{150,310}.png` | Windows pinned tiles |
| `safari-pinned-tab.svg` | Safari pinned-tab monochrome |
| `og-card.png` (1200×630) | Open Graph, Twitter, iMessage, LinkedIn, Slack, Discord |
| `og-card-square.png` (1080×1080) | Instagram, square iMessage previews |

---

## Local Development

```bash
# Serve from the repo root (service workers require HTTP, not file://)
python3 -m http.server 8080
```

Then in DevTools:
- **Application → Manifest** — verify the manifest, icons, and theme colors load.
- **Application → Service Workers** — confirm `sw.js` registers and activates.
- **Lighthouse → PWA category** — should hit 100. Installable, offline-capable, themed.

To **test the install prompt**, open the site in Chrome on Android (or Edge on desktop) over HTTPS and look for the install banner / address-bar install icon.

---

## Service Worker & Cache Busting

The service worker at [`sw.js`](sw.js) uses:
- **Network-first** for HTML (always fresh when online, cached as fallback).
- **Stale-while-revalidate** for icons, manifest, and other static assets.
- **Pass-through** for Stripe and other cross-origin requests.

**To force a cache flush after a major update:**

Bump the `VERSION` constant at the top of `sw.js`:

```js
const VERSION = "v1.1.0";   // was v1.0.0
```

The next page load will install the new SW, delete old caches, and reload all clients via `controllerchange`.

---

## SEO, Analytics, and Schema

The site ships with:

- ✅ **`<title>`, meta description, canonical URL, keywords**
- ✅ **Open Graph + Twitter Card tags** pointing at `og-card.png`
- ✅ **Schema.org JSON-LD `LocalBusiness`** with address, phone, hours, area served, and parent organization
- ✅ **`sitemap.xml`** with section anchors
- ✅ **`robots.txt`** allowing crawlers, blocking `_build/`

To add analytics, drop a Google Analytics 4 / Plausible / Fathom snippet into `<head>` of `index.html`. Recommended: privacy-friendly Plausible if you don't want a cookie banner.

---

## Browser Support

| Browser | Status |
|---------|--------|
| Safari iOS 16+ | ✅ Full PWA, install-to-home-screen, status-bar styling |
| Chrome Android 90+ | ✅ Full PWA with adaptive icon |
| Chrome / Edge desktop | ✅ Installable, mega-menu hover |
| Firefox | ✅ Functional (no install prompt by design in FF) |
| Safari macOS | ✅ Functional |
| IE11 | ❌ Not supported (uses CSS Grid, backdrop-filter, ES2018+) |

---

## Troubleshooting

**The icons aren't updating after I changed `generate_icons.py`.**
The service worker is serving the old cached copy. Bump `VERSION` in `sw.js` or hard-refresh with DevTools open and "Disable cache" checked.

**The Stripe checkout button opens to a 404.**
You haven't wired real Payment Links yet — the placeholder URLs in `buildStripeUrl()` are pattern strings, not real routes. See [Wiring Stripe Payment Links](#wiring-stripe-payment-links).

**The custom domain isn't working / shows a `404` from GitHub.**
Three usual culprits:
1. The `CNAME` file isn't in the repo root.
2. DNS is proxied through Cloudflare *before* GitHub provisioned the cert. Set the CNAME record to **DNS-only** (gray cloud), wait 10–30 minutes, then optionally re-enable proxy.
3. The Pages source isn't set to **GitHub Actions** in repo settings.

**The OG card isn't showing in iMessage / WhatsApp / LinkedIn previews.**
- Re-validate with [Facebook's Sharing Debugger](https://developers.facebook.com/tools/debug/) — it will force a re-scrape.
- Verify `og-card.png` is reachable at `https://tradesmen.nepa-pro.com/icons/og-card.png` (must be absolute HTTPS).
- iMessage caches link previews aggressively per recipient; test with a contact who hasn't seen the link before.

**`generate_icons.py` complains about fonts.**
The script falls back to FreeSans / Liberation Sans, which ship with most Linux distros. On macOS:
```bash
brew install --cask font-liberation
# or just edit load_font() to point at /System/Library/Fonts/Helvetica.ttc
```

---

## Contact

| | |
|---|---|
| 📞 | **[570-677-7971](tel:5706777971)** |
| ✉️ | **[service@nepa-pro.com](mailto:service@nepa-pro.com)** |
| 🌐 | **[tradesmen.nepa-pro.com](https://tradesmen.nepa-pro.com/)** |
| 📍 | Clarks Summit, PA — serving NEPA |

★ **Veteran Owned & Operated**

---

© 2026 NEPA-PRO LLC. All rights reserved. See [LICENSE](LICENSE).
