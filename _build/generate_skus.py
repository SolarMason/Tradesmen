"""
Generate the full 135-row SKU catalog for Stripe Payment Link setup.

Mirrors the TRADES, TIERS, and DURATIONS data baked into index.html.

Run:  python3 _build/generate_skus.py > skus.csv
"""
import csv
import sys

TRADES = [
    ("concrete",            "structural", "Concrete Workers",        [48,  68,  88]),
    ("drywall",             "structural", "Drywall Hangers",         [42,  62,  82]),
    ("electricians",        "electrical", "Electricians",            [58,  85, 115]),
    ("hvac",                "mechanical", "HVAC Technicians",        [52,  78, 105]),
    ("commercial-hvac",     "mechanical", "Commercial HVAC",         [62,  92, 125]),
    ("ironworkers",         "structural", "Ironworkers",             [55,  80, 108]),
    ("linemen",             "electrical", "Linemen",                 [68,  98, 135]),
    ("masons",              "structural", "Masons",                  [52,  76, 102]),
    ("millwrights",         "heavy",      "Millwrights",             [58,  86, 115]),
    ("plumbers",            "mechanical", "Plumbers",                [55,  82, 110]),
    ("commercial-plumbers", "mechanical", "Commercial Plumbers",     [62,  92, 125]),
    ("riggers",             "heavy",      "Riggers",                 [52,  76, 102]),
    ("welders",             "structural", "Welders",                 [48,  72,  98]),
    ("operating-engineers", "heavy",      "Operating Engineers",     [62,  90, 120]),
    ("heavy-equipment",     "heavy",      "Heavy Equipment Operators", [58, 85, 115]),
]

TIERS = [
    ("apprentice", "Apprentice",         0),
    ("journeyman", "Journeyman",         1),
    ("master",     "Master / Foreman",   2),
]

DURATIONS = [
    ("half",   "Half Day",  4,  1.00),
    ("full",   "Full Day",  8,  1.00),
    ("weekly", "Weekly",   40,  0.92),  # 8% subscription discount
]


def generate_rows():
    rows = []
    for trade_id, cat, trade_name, rates in TRADES:
        for tier_id, tier_name, tier_idx in TIERS:
            base_rate = rates[tier_idx]
            for dur_id, dur_name, hours, mult in DURATIONS:
                total = round(base_rate * hours * mult)
                sku = f"{trade_id}_{tier_id}_{dur_id}"
                product_name = f"{tier_name} {trade_name} — {dur_name} ({hours}h)"
                description = (
                    f"{tier_name}-tier {trade_name.lower()} for {hours} hours "
                    f"({dur_name.lower()}). Includes WC, payroll, GL, and dispatch. "
                    f"Tradesperson deploys to the shipping address provided at checkout."
                )
                rows.append({
                    "sku": sku,
                    "trade_id": trade_id,
                    "trade_name": trade_name,
                    "category": cat,
                    "tier_id": tier_id,
                    "tier_name": tier_name,
                    "duration_id": dur_id,
                    "duration_name": dur_name,
                    "hours": hours,
                    "billable_hourly_usd": base_rate,
                    "multiplier": mult,
                    "total_usd": total,
                    "stripe_product_name": product_name,
                    "stripe_product_description": description,
                    "stripe_price_currency": "usd",
                    "stripe_price_amount_cents": total * 100,
                    "client_reference_id_template": f"{sku}_{total}",
                })
    return rows


def main():
    rows = generate_rows()
    fieldnames = list(rows[0].keys())
    writer = csv.DictWriter(sys.stdout, fieldnames=fieldnames, lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)


if __name__ == "__main__":
    main()
