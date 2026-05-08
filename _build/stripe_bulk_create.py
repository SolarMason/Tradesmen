#!/usr/bin/env python3
"""
NEPA-PRO Tradesmen — Stripe bulk Payment Link creation.

Reads skus.csv (135 SKUs), then for each one:
  1. Creates a Stripe Product (with jobsite-deploy description)
  2. Creates a Price (one-time, USD)
  3. Creates a Payment Link with:
       • shipping_address_collection  (US, REQUIRED) ← this is the JOBSITE
       • phone_number_collection      (enabled)
       • custom_fields × 3:
           - Project description / scope of work     (text, required)
           - On-site contact name & cell             (text, required)
           - Access notes / gate codes / supervisor  (text, optional)
       • after_completion             (redirect → tradesmen.nepa-pro.com/?booked=1)
       • custom_text                  (clarifies "shipping = jobsite")
       • metadata                     (sku, trade, tier, duration for reconciliation)

Then saves stripe_links.json (full mapping) and patches index.html in place.

Idempotent: if stripe_links.json already exists, only creates missing SKUs.
Safe: validates env, dry-run mode, retries with backoff on rate limits.

USAGE:

  # 1. Install Stripe SDK (one time)
  pip install stripe

  # 2. Export your Stripe secret key (TEST mode first to verify!)
  export STRIPE_SECRET_KEY=sk_test_...

  # 3. Dry run (validates without creating anything)
  python3 _build/stripe_bulk_create.py --dry-run

  # 4. Real run
  python3 _build/stripe_bulk_create.py

  # 5. After verification, switch to live key and re-run
  export STRIPE_SECRET_KEY=sk_live_...
  python3 _build/stripe_bulk_create.py

The script writes stripe_links.json incrementally — if anything fails partway
through, just re-run; it picks up where it left off.

After successful run, index.html is automatically patched with all 135 link IDs.
"""
from __future__ import annotations
import argparse
import csv
import json
import os
import re
import sys
import time
from pathlib import Path
from typing import Optional

ROOT = Path(__file__).resolve().parent.parent
SKUS_CSV = ROOT / "skus.csv"
LINKS_JSON = ROOT / "stripe_links.json"
INDEX_HTML = ROOT / "index.html"

REDIRECT_URL = "https://tradesmen.nepa-pro.com/?booked=1"
SUPPORT_EMAIL = "service@nepa-pro.com"
SUPPORT_PHONE = "570-677-7971"

# ============================================================
# Helpers
# ============================================================

def log(msg, level="INFO"):
    colors = {"INFO": "\033[94m", "OK": "\033[92m", "WARN": "\033[93m",
              "ERR": "\033[91m", "DIM": "\033[90m"}
    reset = "\033[0m"
    print(f"  {colors.get(level, '')}{level:<4}{reset} {msg}", flush=True)


def with_retry(fn, *, max_attempts=5, base_delay=1.0):
    """Retry a Stripe call on rate-limit / transient errors with exponential backoff."""
    import stripe
    for attempt in range(1, max_attempts + 1):
        try:
            return fn()
        except stripe.RateLimitError:
            wait = base_delay * (2 ** (attempt - 1))
            log(f"Rate limited; sleeping {wait:.1f}s (attempt {attempt}/{max_attempts})", "WARN")
            time.sleep(wait)
        except stripe.APIConnectionError as e:
            wait = base_delay * (2 ** (attempt - 1))
            log(f"Connection error: {e}; retry in {wait:.1f}s", "WARN")
            time.sleep(wait)
        except Exception:
            raise
    raise RuntimeError("Exhausted retries")


def load_existing_links() -> dict:
    """Load previously-created link mappings so we can resume."""
    if not LINKS_JSON.exists():
        return {}
    try:
        return json.loads(LINKS_JSON.read_text())
    except Exception as e:
        log(f"stripe_links.json unreadable ({e}); starting fresh", "WARN")
        return {}


def save_links(mapping: dict):
    """Persist mapping after each successful SKU so failures are resumable."""
    LINKS_JSON.write_text(json.dumps(mapping, indent=2, sort_keys=True))


# ============================================================
# Resource builders
# ============================================================

def build_product_description(row: dict) -> str:
    return (
        f"{row['tier_name']}-tier {row['trade_name']} for "
        f"{row['hours']} hours ({row['duration_name'].lower()}). "
        f"Includes workers compensation, payroll, general liability, and dispatch. "
        f"Tradesperson is deployed to the shipping address you provide at checkout — "
        f"that address is the JOBSITE. We confirm by phone within one business hour. "
        f"Questions: {SUPPORT_PHONE} · {SUPPORT_EMAIL}"
    )


def build_custom_fields() -> list:
    """Three custom fields collected at checkout — required for dispatch."""
    return [
        {
            "key": "projectscope",
            "label": {"type": "custom", "custom": "Project description / scope of work"},
            "type": "text",
            "text": {"minimum_length": 10, "maximum_length": 500},
            "optional": False,
        },
        {
            "key": "sitecontact",
            "label": {"type": "custom", "custom": "On-site contact name & cell phone"},
            "type": "text",
            "text": {"minimum_length": 5, "maximum_length": 100},
            "optional": False,
        },
        {
            "key": "accessnotes",
            "label": {"type": "custom", "custom": "Access notes (gate codes, parking, supervisor, etc.)"},
            "type": "text",
            "text": {"maximum_length": 500},
            "optional": True,
        },
    ]


def build_custom_text() -> dict:
    return {
        "shipping_address": {
            "message": "This is the JOBSITE — where the tradesperson will be dispatched on your start date."
        },
        "submit": {
            "message": (
                "We'll call to confirm within one business hour. "
                f"Questions: {SUPPORT_PHONE}."
            )
        },
    }


# ============================================================
# Main create flow
# ============================================================

def create_one_sku(stripe, row: dict, dry_run: bool = False) -> dict:
    """Create Product + Price + Payment Link for one SKU. Returns mapping entry."""
    sku = row["sku"]
    name = row["stripe_product_name"]
    description = build_product_description(row)
    amount_cents = int(row["stripe_price_amount_cents"])
    metadata = {
        "sku": sku,
        "trade": row["trade_id"],
        "tier": row["tier_id"],
        "duration": row["duration_id"],
        "category": row["category"],
        "hours": row["hours"],
        "billable_hourly_usd": row["billable_hourly_usd"],
    }

    if dry_run:
        log(f"  DRY: would create {name}  (${amount_cents/100:,.2f})", "DIM")
        return {
            "sku": sku,
            "product_id": "prod_DRY",
            "price_id": "price_DRY",
            "payment_link_id": "plink_DRY",
            "url": f"https://buy.stripe.com/DRY_{sku}",
            "amount_cents": amount_cents,
        }

    # 1. Product
    product = with_retry(lambda: stripe.Product.create(
        name=name,
        description=description,
        metadata=metadata,
        shippable=True,  # because we ship labor to a jobsite
        statement_descriptor="NEPAPRO TRADES"[:22],  # 22-char max
        unit_label="booking",
    ))

    # 2. Price (one-time)
    price = with_retry(lambda: stripe.Price.create(
        product=product.id,
        unit_amount=amount_cents,
        currency="usd",
        metadata=metadata,
        nickname=sku,
    ))

    # 3. Payment Link with full config
    link = with_retry(lambda: stripe.PaymentLink.create(
        line_items=[{"price": price.id, "quantity": 1}],
        shipping_address_collection={"allowed_countries": ["US"]},
        phone_number_collection={"enabled": True},
        custom_fields=build_custom_fields(),
        after_completion={
            "type": "redirect",
            "redirect": {"url": REDIRECT_URL},
        },
        custom_text=build_custom_text(),
        metadata=metadata,
        allow_promotion_codes=True,
        billing_address_collection="auto",  # collect billing if different from shipping
    ))

    return {
        "sku": sku,
        "product_id": product.id,
        "price_id": price.id,
        "payment_link_id": link.id,
        "url": link.url,
        "amount_cents": amount_cents,
        "name": name,
    }


# ============================================================
# index.html patcher
# ============================================================

def patch_index_html(mapping: dict, dry_run: bool = False) -> None:
    """Replace the STRIPE_LINKS = {...} block in index.html with the populated map."""
    html = INDEX_HTML.read_text()

    # Build the JS object literal
    lines = ["const STRIPE_LINKS = {"]
    for sku in sorted(mapping.keys()):
        entry = mapping[sku]
        url = entry["url"]
        # Extract the link ID from the URL.
        # Supports both stripe.com (https://buy.stripe.com/{id})
        # and custom domains (https://*.nepa-pro.com/b/{id})
        m = re.search(r"/(?:b/)?([A-Za-z0-9]+)$", url.split("?")[0])
        link_path = m.group(1) if m else url
        lines.append(f"  '{sku}': '{link_path}',")
    lines.append("};")
    new_block = "\n".join(lines)

    # Find existing block and replace
    pattern = r"const STRIPE_LINKS = \{[\s\S]*?\};"
    if not re.search(pattern, html):
        log("Could not find STRIPE_LINKS block in index.html; aborting patch", "ERR")
        return

    new_html = re.sub(pattern, new_block, html, count=1)

    if dry_run:
        log(f"  DRY: would patch index.html with {len(mapping)} link mappings", "DIM")
        return

    INDEX_HTML.write_text(new_html)
    log(f"Patched index.html with {len(mapping)} STRIPE_LINKS entries", "OK")


# ============================================================
# Entry point
# ============================================================

def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--dry-run", action="store_true",
                        help="Validate without creating any Stripe resources")
    parser.add_argument("--no-patch", action="store_true",
                        help="Skip the index.html patch step")
    parser.add_argument("--only", type=str, default=None,
                        help="Only create one SKU (for testing). e.g. --only electricians_journeyman_full")
    parser.add_argument("--limit", type=int, default=None,
                        help="Only process first N SKUs (for testing)")
    args = parser.parse_args()

    # Verify Stripe SDK (only if we're actually going to call the API)
    stripe = None
    if not args.dry_run:
        try:
            import stripe as _stripe
            stripe = _stripe
        except ImportError:
            log("Stripe SDK not installed. Run:  pip install stripe", "ERR")
            sys.exit(1)

    # Verify API key
    api_key = os.environ.get("STRIPE_SECRET_KEY", "").strip()
    if not args.dry_run:
        if not api_key:
            log("STRIPE_SECRET_KEY not set in environment", "ERR")
            log("  export STRIPE_SECRET_KEY=sk_test_...   (test mode first)", "DIM")
            sys.exit(1)
        if not (api_key.startswith("sk_test_") or api_key.startswith("sk_live_")):
            log(f"STRIPE_SECRET_KEY format unexpected (must start with sk_test_ or sk_live_)", "ERR")
            sys.exit(1)
        stripe.api_key = api_key
        mode = "TEST" if api_key.startswith("sk_test_") else "LIVE"
        color = "WARN" if mode == "LIVE" else "INFO"
        log(f"Stripe mode: {mode}", color)
        if mode == "LIVE":
            confirm = input("\n  ⚠️  LIVE MODE — this creates REAL Stripe resources. Continue? (yes/no): ").strip().lower()
            if confirm != "yes":
                log("Aborted by user", "WARN")
                sys.exit(0)

    # Load SKUs
    if not SKUS_CSV.exists():
        log(f"skus.csv not found at {SKUS_CSV}", "ERR")
        log("  Run: python3 _build/generate_skus.py > skus.csv", "DIM")
        sys.exit(1)
    with open(SKUS_CSV) as f:
        all_rows = list(csv.DictReader(f))
    log(f"Loaded {len(all_rows)} SKUs from skus.csv", "OK")

    # Filter
    rows = all_rows
    if args.only:
        rows = [r for r in rows if r["sku"] == args.only]
        if not rows:
            log(f"SKU '{args.only}' not found", "ERR")
            sys.exit(1)
    if args.limit:
        rows = rows[: args.limit]
    log(f"Processing {len(rows)} SKU(s)", "INFO")

    # Resume
    mapping = load_existing_links()
    if mapping:
        log(f"Resuming — {len(mapping)} SKU(s) already created", "INFO")

    # Process each SKU
    created = 0
    skipped = 0
    failed = []
    print()
    for i, row in enumerate(rows, 1):
        sku = row["sku"]
        if sku in mapping and not args.dry_run:
            log(f"[{i:>3}/{len(rows)}] {sku}  ↪ already created, skipping", "DIM")
            skipped += 1
            continue
        log(f"[{i:>3}/{len(rows)}] {sku}", "INFO")
        try:
            entry = create_one_sku(stripe, row, dry_run=args.dry_run)
            mapping[sku] = entry
            if not args.dry_run:
                save_links(mapping)
                log(f"        ✓ {entry['url']}", "OK")
                created += 1
        except Exception as e:
            log(f"        ✗ FAILED: {e}", "ERR")
            failed.append((sku, str(e)))
            if not args.dry_run:
                save_links(mapping)
            # Continue to next SKU rather than aborting the whole run

    # Summary
    print()
    log("=" * 60, "DIM")
    log(f"Created:   {created}", "OK")
    log(f"Skipped:   {skipped}", "INFO")
    log(f"Failed:    {len(failed)}", "ERR" if failed else "INFO")
    log(f"Total in mapping: {len(mapping)}/{len(all_rows)}",
        "OK" if len(mapping) == len(all_rows) else "WARN")
    if failed:
        log("Failures (re-run to retry):", "ERR")
        for sku, err in failed[:10]:
            log(f"  {sku}: {err[:100]}", "ERR")

    # Patch index.html if mapping is complete
    if not args.no_patch and mapping:
        if len(mapping) < len(all_rows):
            log(f"Mapping incomplete ({len(mapping)}/{len(all_rows)}); patching with what we have", "WARN")
        patch_index_html(mapping, dry_run=args.dry_run)
    else:
        log("Skipped index.html patch", "DIM")

    sys.exit(0 if not failed else 1)


if __name__ == "__main__":
    main()
