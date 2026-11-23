# Brief: finish dataset generation (DA Launchpad)

Repo: /home/dividh/nishchay/da-launchpad. Python venv: .venv (pandas, numpy, openpyxl installed). Context: master_prompt.md Section 4 (read only that section).

ALREADY DONE (do not rewrite, do not regenerate unless needed for determinism check):
scripts/generate_data/common.py (shared helpers — read it first and reuse), gen_ecommerce.py, gen_food_delivery.py, gen_hr.py, gen_fintech.py, gen_subscription.py, gen_marketing.py, run_one.py (usage: `.venv/bin/python scripts/generate_data/run_one.py gen_hr`). Outputs exist in public/data/sqlite/*.sqlite, public/data/csv/<id>/*.csv, and per-dataset metadata in scripts/generate_data/_meta/<id>.json.

You may ONLY create/edit: scripts/generate_data/**, requirements.txt, public/data/**, src/data/datasets.json.

TODO:
1. Write scripts/generate_data/gen_retail.py following the SAME pattern as gen_hr.py (copy its structure: run() returning meta, writing sqlite + csv + _meta json). Dataset id `retail`, tables: stores, sales, inventory, targets. India-flavored fictional stores (cities, regions, store formats), dates 2023-01-01..2024-12-31 as ISO TEXT, festive spikes (Diwali Oct/Nov), embedded signals: some stores with frequent stockouts losing sales, one region missing targets, a slow-moving category with overstock. Messy data in moderate documented doses like the other generators (some NULLs, a few duplicate rows, casing/whitespace issues, a few outliers; CSV-only mixed date formats if other generators do that). Keep sqlite ≤ 4 MB; sales ~20k–40k rows. Indexes on FKs.
2. Write scripts/generate_data/generate_all.py: runs all 7 generators in order, then builds public/data/zip/<id>.zip of each dataset's CSVs, then assembles src/data/datasets.json = array of the 7 _meta objects in order ecommerce, food_delivery, hr, fintech, subscription, marketing, retail. Each object must have keys: id, title, description, tables[{name,rowCount,description,columns[{name,type,description,nullable,example}]}], relationships[{from:"table.col",to:"table.col",type}], qualityIssues[], er (mermaid erDiagram), downloads{sqlite:"data/sqlite/<id>.sqlite", zip:"data/zip/<id>.zip", csv:[...]}, signals[]. Paths relative, no leading slash. If an existing _meta file lacks a key, fix it in that generator minimally. rowCount must equal real row counts (verify via sqlite3).
3. Write scripts/generate_data/README.md (how to regenerate, list of datasets).
4. Verify cheaply: run generate_all.py twice, compare sha256 of all CSVs (sqlite files may differ in header bytes; if CSVs match, fine). Check each sqlite ≤ 4 MB. Run 2 sanity queries on retail with sqlite3 (monthly sales with strftime; stockout count by store).

Token discipline: don't print whole files or long outputs — pipe through head/tail. Don't re-read the big existing generators beyond what you need (common.py + gen_hr.py as template).

Final reply ≤120 words: retail row counts, file sizes, determinism result, any problems.
