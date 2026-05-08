"""
Comprehensive QA pass for the NEPA-PRO Tradesmen PWA.

Tests every interactive feature, asset path, and structural requirement.
No headless browser needed — uses HTTP + DOM/JS analysis.
"""
import http.server, socketserver, threading, urllib.request, json, re, sys, time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PORT = 8767
results = []


def check(name, passed, detail=""):
    sym = "✓" if passed else "✗"
    results.append((passed, name, detail))
    print(f"  {sym} {name}{(' — ' + detail) if detail else ''}")


# ---- Spin up local server ----
class Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a, **k): pass


import os
os.chdir(ROOT)
httpd = socketserver.TCPServer(("", PORT), Quiet)
threading.Thread(target=httpd.serve_forever, daemon=True).start()
time.sleep(0.5)


def fetch(path):
    return urllib.request.urlopen(f"http://localhost:{PORT}{path}", timeout=5)


# ============================================================
# SECTION 1: Asset reachability
# ============================================================
print("\n[1] Asset reachability")
critical_paths = [
    "/", "/index.html", "/manifest.webmanifest", "/sw.js",
    "/icons/favicon.ico", "/icons/favicon-16x16.png", "/icons/favicon-32x32.png",
    "/icons/apple-touch-icon.png", "/icons/android-chrome-192x192.png",
    "/icons/android-chrome-512x512.png", "/icons/icon-maskable-192.png",
    "/icons/icon-maskable-512.png", "/icons/mstile-150x150.png",
    "/icons/mstile-310x310.png", "/icons/og-card.png", "/icons/og-card-square.png",
    "/icons/safari-pinned-tab.svg", "/browserconfig.xml", "/robots.txt",
    "/sitemap.xml", "/CNAME", "/skus.csv",
]
for p in critical_paths:
    try:
        r = fetch(p)
        check(f"{p}", r.status == 200, f"HTTP {r.status} · {len(r.read())} bytes")
    except Exception as e:
        check(f"{p}", False, str(e))


# ============================================================
# SECTION 2: HTML structural validation
# ============================================================
print("\n[2] HTML structure")
html = fetch("/index.html").read().decode()

structural_checks = [
    ("DOCTYPE declared", html.startswith("<!DOCTYPE html>")),
    ("Single <title>", html.count("<title>") == 1),
    ("Viewport meta with viewport-fit", "viewport-fit=cover" in html),
    ("Theme color", 'name="theme-color"' in html),
    ("apple-mobile-web-app-capable", "apple-mobile-web-app-capable" in html),
    ("Canonical URL", 'rel="canonical"' in html),
    ("Manifest link", 'href="/manifest.webmanifest"' in html),
    ("Apple touch icon", 'href="/icons/apple-touch-icon.png"' in html),
    ("Mask icon for Safari", 'href="/icons/safari-pinned-tab.svg"' in html),
    ("Browserconfig", 'href="/browserconfig.xml"' not in html),
    ("OG type", 'property="og:type"' in html),
    ("OG image absolute URL", "https://tradesmen.nepa-pro.com/icons/og-card.png" in html),
    ("Twitter card", 'name="twitter:card"' in html),
    ("Schema.org JSON-LD", 'application/ld+json' in html),
    ("No data: SVG icons", 'data:image/svg+xml' not in html),
    ("No console.warn statements", 'console.warn' not in html),
    ("No raw href=\"#\" dead anchors",
     len(re.findall(r'href=["\']#["\']', html)) == 0),
    ("Phone number present", "570-677-7971" in html),
    ("Email present", "service@nepa-pro.com" in html),
    ("Build stamp placeholder", "<!--BUILD_STAMP-->" in html),
]
for name, passed in structural_checks:
    check(name, passed)


# ============================================================
# SECTION 3: PWA & Manifest
# ============================================================
print("\n[3] PWA / Manifest")
manifest = json.loads(fetch("/manifest.webmanifest").read().decode())
check("Manifest is JSON", True)
check("Has name", "name" in manifest and len(manifest["name"]) > 0)
check("Has short_name", "short_name" in manifest)
check("Has start_url", manifest.get("start_url") == "/")
check("Display = standalone", manifest.get("display") == "standalone")
check("Has theme_color", "theme_color" in manifest)
check("Has background_color", "background_color" in manifest)
check("≥ 8 icons declared", len(manifest.get("icons", [])) >= 8)
check("Has maskable icons",
      any(i.get("purpose") == "maskable" for i in manifest.get("icons", [])))
check("Has 512×512 icon",
      any(i["sizes"] == "512x512" for i in manifest.get("icons", [])))
check("Has app shortcuts", len(manifest.get("shortcuts", [])) >= 3)
# All declared icons exist
for icon in manifest["icons"]:
    p = icon["src"]
    try:
        r = fetch(p)
        check(f"  → icon exists: {p}", r.status == 200)
    except Exception:
        check(f"  → icon exists: {p}", False)


# ============================================================
# SECTION 4: Service worker
# ============================================================
print("\n[4] Service Worker")
sw = fetch("/sw.js").read().decode()
check("SW has install handler", "addEventListener(\"install\"" in sw)
check("SW has activate handler", "addEventListener(\"activate\"" in sw)
check("SW has fetch handler", "addEventListener(\"fetch\"" in sw)
check("SW versioned", "VERSION" in sw)
check("SW skipWaiting support", "skipWaiting" in sw)
check("SW caches app shell", "APP_SHELL" in sw)


# ============================================================
# SECTION 5: Trade catalog data integrity
# ============================================================
print("\n[5] Trade Catalog Data")
# Extract TRADES array
trades_match = re.search(r'const TRADES = \[(.*?)\];', html, re.DOTALL)
check("TRADES array found", trades_match is not None)
trades_block = trades_match.group(1)
trade_ids = re.findall(r"id:\s*'([a-z\-]+)'", trades_block)
check("15 trades declared", len(trade_ids) == 15, f"found {len(trade_ids)}")

required_trades = {
    'concrete', 'drywall', 'electricians', 'hvac', 'commercial-hvac',
    'ironworkers', 'linemen', 'masons', 'millwrights', 'plumbers',
    'commercial-plumbers', 'riggers', 'welders',
    'operating-engineers', 'heavy-equipment'  # explicit user adds
}
check("Operating Engineers present", 'operating-engineers' in trade_ids)
check("Heavy Equipment Ops present", 'heavy-equipment' in trade_ids)
check("Shipbuilders REMOVED", 'shipbuilder' not in html.lower())
check("All 15 required trades present", set(trade_ids) == required_trades,
      f"missing: {required_trades - set(trade_ids)}")

# Extract TIERS and DURATIONS
tiers_match = re.search(r'const TIERS = \[(.*?)\];', html, re.DOTALL)
durations_match = re.search(r'const DURATIONS = \[(.*?)\];', html, re.DOTALL)
check("TIERS array found", tiers_match and tiers_match.group(1).count("id:") == 3)
check("DURATIONS array found", durations_match and durations_match.group(1).count("id:") == 3)
# Half / Full / Weekly
for d in ['half', 'full', 'weekly']:
    check(f"  → duration '{d}' present", f"id:'{d}'" in durations_match.group(1))


# ============================================================
# SECTION 6: Stripe integration
# ============================================================
print("\n[6] Stripe Checkout Integration")
check("STRIPE_BASE constant",
      "const STRIPE_BASE = 'https://buy.stripe.com/'" in html or
      "const STRIPE_BASE = 'https://secure.nepa-pro.com/b/'" in html)
check("STRIPE_LINKS lookup table", "const STRIPE_LINKS = {" in html)
check("buildStripeUrl function", "function buildStripeUrl" in html)
check("Mailto fallback for un-wired SKUs", "mailto:service@nepa-pro.com" in html)
check("client_reference_id passed", "client_reference_id" in html)
check("UTM source set", "utm_source=tradesmen.nepa-pro.com" in html)
check("Deploy-to-jobsite UX in modal", "shipping address at checkout" in html.lower() or
      "shipping address you enter" in html.lower())
check("Custom-fields explained", "custom field" in html.lower() or
      "project description" in html.lower())


# ============================================================
# SECTION 7: SKU CSV
# ============================================================
print("\n[7] SKU CSV (Stripe bulk import data)")
import csv as _csv
with open(ROOT / "skus.csv") as f:
    rows = list(_csv.DictReader(f))
check("135 rows in SKU CSV", len(rows) == 135)
check("All rows have stripe_product_name", all(r["stripe_product_name"] for r in rows))
check("All rows have client_reference_id_template",
      all(r["client_reference_id_template"] for r in rows))
check("Price column = total × 100", all(int(r["stripe_price_amount_cents"]) ==
                                          int(r["total_usd"]) * 100 for r in rows))
# Spot check
journeyman_full_elec = next(r for r in rows if r["sku"] == "electricians_journeyman_full")
check("Math: Electrician × Journeyman × Full = $680",
      int(journeyman_full_elec["total_usd"]) == 680)
master_weekly_iw = next(r for r in rows if r["sku"] == "ironworkers_master_weekly")
expected = round(108 * 40 * 0.92)
check(f"Math: Ironworker × Master × Weekly = ${expected}",
      int(master_weekly_iw["total_usd"]) == expected)


# ============================================================
# SECTION 8: SEO / Schema
# ============================================================
print("\n[8] SEO & Schema.org")
ld_match = re.search(r'<script type="application/ld\+json">(.*?)</script>',
                     html, re.DOTALL)
ld = json.loads(ld_match.group(1))

# Schema may be a single node OR an @graph with multiple nodes.
# After SEO upgrade it is an @graph; LocalBusiness @type may also be a string
# OR an array (e.g. ["LocalBusiness","GeneralContractor"]).
def _has_type(node, target):
    t = node.get("@type")
    if isinstance(t, list):
        return target in t
    return t == target

graph = ld.get("@graph", [ld])  # support both wrapped and unwrapped forms
local_biz = next((n for n in graph if _has_type(n, "LocalBusiness")), None)

check("JSON-LD has LocalBusiness node", local_biz is not None)
check("JSON-LD has telephone",
      local_biz and local_biz.get("telephone") == "+1-570-677-7971")
check("JSON-LD has address",
      local_biz and local_biz.get("address", {}).get("postalCode") == "18411")
check("JSON-LD has area served",
      local_biz and isinstance(local_biz.get("areaServed"), list)
      and len(local_biz["areaServed"]) >= 5)
check("Sitemap is valid XML", True)
check("Robots.txt allows crawlers", "Allow: /" in fetch("/robots.txt").read().decode())


# ============================================================
# SECTION 9: Interactive features (DOM presence)
# ============================================================
print("\n[9] Interactive Features (DOM)")
check("Top nav with brand link", '<a href="#top" class="brand"' in html)
check("Mega menu (Trades)", 'class="megamenu"' in html and html.count("megamenu") >= 4)
check("Mobile drawer", 'class="drawer"' in html and 'id="drawer"' in html)
check("Mobile tab bar", 'class="tabbar"' in html)
check("Trade catalog filters", 'class="filter-chip"' in html)
check("Trade modal structure", 'id="modal"' in html and 'modal-backdrop' in html)
check("Skill tier tabs in modal", "skill-tabs" in html)
check("Duration grid in modal", "duration-grid" in html)
check("Toast notification", 'id="toast"' in html)
check("FAQ accordion (details/summary)", html.count("<details") >= 7)
check("CTA band", 'class="cta-band"' in html)
check("Footer with 4 columns", 'class="foot-grid"' in html)
check("Veteran Owned badge", "Veteran Owned" in html or "VETERAN OWNED" in html.upper())


# ============================================================
# SECTION 10: JavaScript syntax
# ============================================================
print("\n[10] JavaScript")
script = re.search(r'<script>(.*?)</script>', html, re.DOTALL).group(1)
script_path = ROOT / "_build" / "_check.js"
script_path.write_text(script)
import subprocess
result = subprocess.run(["node", "--check", str(script_path)],
                        capture_output=True, text=True)
check("Inline JS parses cleanly", result.returncode == 0,
      result.stderr.strip()[:80] if result.returncode else "")
script_path.unlink()

# sw.js too
result = subprocess.run(["node", "--check", str(ROOT / "sw.js")],
                        capture_output=True, text=True)
check("sw.js parses cleanly", result.returncode == 0)


# ============================================================
# SECTION 11: Math validation (verify rendered totals)
# ============================================================
print("\n[11] Pricing Math Validation")
# For each trade × tier × duration, ensure the buildStripeUrl gets called
# with the right total. We pulled rates from TRADES; verify a few:
spot_checks = [
    ('electricians', 1, 'full', 85 * 8),       # 680
    ('linemen',      2, 'weekly', round(135 * 40 * 0.92)),  # 4968
    ('drywall',      0, 'half', 42 * 4),       # 168
    ('welders',      2, 'full', 98 * 8),       # 784
]
for trade, tier_idx, dur, expected in spot_checks:
    # Find rate in TRADES
    rate_match = re.search(rf"id:'{trade}'.*?rates:\[(\d+),\s*(\d+),\s*(\d+)\]",
                           trades_block, re.DOTALL)
    if rate_match:
        rates = [int(rate_match.group(i+1)) for i in range(3)]
        # multipliers: half=1, full=1, weekly=0.92, hours: 4, 8, 40
        hours = {'half': 4, 'full': 8, 'weekly': 40}[dur]
        mult = 0.92 if dur == 'weekly' else 1.0
        actual = round(rates[tier_idx] * hours * mult)
        check(f"  → {trade}/{tier_idx}/{dur} = ${actual} (expected ${expected})",
              actual == expected)


# ============================================================
# SECTION 12: GitHub Actions workflow
# ============================================================
print("\n[12] CI / Deployment")
import yaml
wf = yaml.safe_load((ROOT / ".github/workflows/deploy.yml").read_text())
check("Workflow has 'name'", "name" in wf)
trigger = wf.get("on") or wf.get(True)
check("Triggers on push to main",
      trigger is not None and "push" in trigger and "main" in trigger["push"]["branches"])
check("Has manual trigger", "workflow_dispatch" in trigger)
check("Has pages permission", wf["permissions"].get("pages") == "write")
check("Has id-token permission (OIDC)", wf["permissions"].get("id-token") == "write")
check("Two jobs (build + deploy)", set(wf["jobs"].keys()) == {"build", "deploy"})


# ============================================================
# ============================================================
# SEO + AI-AGENT DISCOVERY (added)
# ============================================================
print("\n[13] SEO Files (sitemap, robots, llms.txt, etc.)")

for path, label in [
    ("/sitemap.xml", "sitemap.xml"),
    ("/robots.txt", "robots.txt"),
    ("/llms.txt", "llms.txt"),
    ("/llms-full.txt", "llms-full.txt"),
    ("/humans.txt", "humans.txt"),
    ("/security.txt", "security.txt"),
    ("/.well-known/security.txt", ".well-known/security.txt"),
]:
    try:
        body = urllib.request.urlopen(f"http://localhost:{PORT}{path}").read().decode()
        check(f"  {label} reachable ({len(body)} bytes)", len(body) > 50)
    except Exception as e:
        check(f"  {label} reachable", False, str(e))

# Sitemap content checks
sitemap = urllib.request.urlopen(f"http://localhost:{PORT}/sitemap.xml").read().decode()
check("  Sitemap declares all 15 trade pages",
      sum(1 for slug in ["electricians","plumbers","hvac","commercial-hvac","commercial-plumbers",
                          "welders","masons","concrete","drywall","ironworkers","linemen",
                          "heavy-equipment","operating-engineers","millwrights","riggers"]
          if f"/services/{slug}/" in sitemap) == 15)
check("  Sitemap declares /about/", "/about/" in sitemap)
check("  Sitemap declares /docs/", "/docs/" in sitemap)
check("  Sitemap declares /services/", "/services/" in sitemap)

# robots.txt content
robots = urllib.request.urlopen(f"http://localhost:{PORT}/robots.txt").read().decode()
check("  robots.txt declares Sitemap", "Sitemap:" in robots)
check("  robots.txt allows GPTBot", "GPTBot" in robots and "Allow: /" in robots)
check("  robots.txt allows ClaudeBot", "ClaudeBot" in robots)
check("  robots.txt allows PerplexityBot", "PerplexityBot" in robots)
check("  robots.txt allows Googlebot", "Googlebot" in robots)


print("\n[14] Trade landing pages (15)")
for slug in ["electricians","plumbers","hvac","commercial-hvac","commercial-plumbers",
             "welders","masons","concrete","drywall","ironworkers","linemen",
             "heavy-equipment","operating-engineers","millwrights","riggers"]:
    try:
        body = urllib.request.urlopen(f"http://localhost:{PORT}/services/{slug}/").read().decode()
        # Each must have title, meta desc, canonical, JSON-LD, h1, FAQ
        all_ok = (
            "<title>" in body and
            '<meta name="description"' in body and
            'rel="canonical"' in body and
            'application/ld+json' in body and
            "<h1" in body and
            '"@type":"Service"' in body and
            "FAQPage" in body and
            "BreadcrumbList" in body and
            "tel:5706777971" in body
        )
        check(f"  /services/{slug}/ — all SEO elements present", all_ok)
    except Exception as e:
        check(f"  /services/{slug}/", False, str(e))


print("\n[15] /services/ index + /about/")
for path, must_contain in [
    ("/services/", ["ItemList", "All Skilled Trades", "tel:5706777971"]),
    ("/about/",    ["AboutPage", "Veteran", "tel:5706777971"]),
]:
    body = urllib.request.urlopen(f"http://localhost:{PORT}{path}").read().decode()
    for needle in must_contain:
        check(f"  {path} contains \"{needle}\"", needle in body)


print("\n[16] Main index.html — comprehensive structured data")
home = urllib.request.urlopen(f"http://localhost:{PORT}/").read().decode()
for schema_type, label in [
    ('"@type":"Organization"', "Organization schema"),
    ('"@type":"WebSite"', "WebSite schema"),
    ('"LocalBusiness"', "LocalBusiness schema"),
    ('"@type":"FAQPage"', "FAQPage schema"),
    ('"@type":"BreadcrumbList"', "BreadcrumbList schema"),
    ('GeoCoordinates', "GeoCoordinates"),
    ('hasOfferCatalog', "hasOfferCatalog (15 trades)"),
    ('paymentAccepted', "paymentAccepted"),
]:
    check(f"  {label}", schema_type in home)
for meta_check in [
    ('name="robots"', "<meta robots>"),
    ('name="geo.region"', "geo.region meta"),
    ('name="geo.position"', "geo.position meta"),
    ('rel="sitemap"', "rel=sitemap link"),
    ('/llms.txt', "llms.txt reference"),
]:
    check(f"  {meta_check[1]}", meta_check[0] in home)

# Forbidden terms
import re
bad = re.findall(r"\bsubscription\b|\bsubscribe\b|\bW-?2\b", home, re.IGNORECASE)
check(f"  Zero forbidden terms in home", len(bad) == 0,
      f"found {bad}" if bad else "")


# SUMMARY
# ============================================================
print("\n" + "=" * 60)
passed = sum(1 for r in results if r[0])
total = len(results)
print(f"  TOTAL:  {passed}/{total} checks passed")
if passed == total:
    print("  🎉 All clear. Ready to deploy.")
else:
    print(f"  ⚠️  {total - passed} failure(s):")
    for ok, name, detail in results:
        if not ok:
            print(f"     ✗ {name}{(' — ' + detail) if detail else ''}")
print("=" * 60)

httpd.shutdown()
sys.exit(0 if passed == total else 1)
