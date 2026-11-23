# DA Launchpad dataset generators

Deterministic, fictional, India-flavoured datasets. Every generator uses a fixed seed, so re-running produces identical CSVs.

## Regenerate

```bash
.venv/bin/python scripts/generate_data/generate_all.py      # all 7 datasets
.venv/bin/python scripts/generate_data/run_one.py gen_hr    # one dataset (e.g. gen_retail)
```

Requirements: `pip install -r requirements.txt` (pandas, numpy, openpyxl). SQLite and zip use the standard library.

`generate_all.py` runs each generator, rebuilds `public/data/zip/<id>.zip` from the CSVs, checks that every `rowCount` matches the SQLite table, and writes `src/data/datasets.json`.

## Outputs

- `public/data/sqlite/<id>.sqlite` - for the in-browser playground (each under 4 MB)
- `public/data/csv/<id>/<table>.csv` - for Excel and Power BI downloads (includes CSV-only messiness such as mixed date formats and rupee-formatted text)
- `public/data/zip/<id>.zip` - all CSVs of a dataset
- `scripts/generate_data/_meta/<id>.json` - data dictionary, relationships, quality issues, ER diagram, signals

## Datasets

| id | Title | Tables |
|---|---|---|
| `ecommerce` | E-commerce | customers, products, orders, order_items, payments, returns |
| `food_delivery` | Food delivery | restaurants, delivery_partners, deliveries, ratings, promo_usage |
| `hr` | HR analytics | departments, employees, salaries, attrition, performance_reviews |
| `fintech` | UPI-style transactions | users, merchants, transactions, failed_transactions |
| `subscription` | Subscription app | users, subscriptions, events |
| `marketing` | Marketing | campaigns, ad_spend, clicks, conversions, ab_test_results |
| `retail` | Retail store sales | stores, sales, inventory, targets |

## Files

- `common.py` - shared helpers (random data, messiness, SQLite/CSV/meta writer)
- `gen_<id>.py` - one generator per dataset, each exposing `run()`
- `run_one.py` - runs a single generator and prints row counts
- `generate_all.py` - runs everything, zips, validates and assembles `src/data/datasets.json`
- `_meta/` - generated per-dataset metadata
