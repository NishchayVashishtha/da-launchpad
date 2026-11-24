# Python module plan
Notes for all writers
- Python solutions run via scripts/py_harness.py: pandas 3.x + numpy only (no sklearn, no matplotlib). `load("ds","table")` reads the MESSY CSVs (₹ text, DD-MM-YYYY mixes, exact duplicate rows, casing issues). Assign `result`.
- Always inspect real values before fixing expectedOutput (use `--fill`, then read it). Several outline asks say "inspect real value" — resolve from data.
- Mixed dates: parse with two explicit formats + errors="coerce" + combine_first (ISO first, then `%d-%m-%Y`); for datetimes use `%Y-%m-%d %H:%M:%S` then `%d-%m-%Y %H:%M:%S`. Check formats against the data first. ₹ clean: `s.astype(str).str.replace(r"[₹,\s]", "", regex=True).astype(float)`.
- Return types: DataFrame/Series/scalar/list/dict (harness serialises). Round money 2 dp. Use sort + tie-breakers whenever a DataFrame order matters (orderMatters true).
- viz / jupyter / git questions: language "text", `solution` md field, no expectedOutput. Viz lesson code blocks are shown, not run (runner cannot draw).
- Fintech first: where an outline offers a choice, prefer fintech/ecommerce/subscription tables.
- PracticeSet in each lesson: `<PracticeSet topic="<topic>" module="python" />`. Messy-lesson uses topic "messy".
- Sample links: all further-reading ids exist in src/data/links.json already (python-docs, kaggle-learn, numpy-docs, pandas-docs, matplotlib-docs, seaborn-docs, git-docs, github-docs, jupyter, anaconda, vscode, khan-stats, mode-sql, excel-support). No new links needed.
- Lesson files go to src/content/lessons/python/<NN-slug>.mdx; slug = outline filename.

## Lessons (20) and practice files (130 questions)
| # | lesson | practice file (topic) | E/M/H | total |
|---|---|---|---|---|
| 01 | variables-types-operators | basics.json | 3/1/0 | 4 |
| 02 | control-flow-loops | loops.json | 3/1/0 | 4 |
| 03 | functions | functions.json | 2/2/0 | 4 |
| 04 | lists-dicts-comprehensions | comprehensions.json | 1/2/1 | 4 |
| 05 | file-handling-csv-json | file-handling.json | 2/2/1 | 5 |
| 06 | numpy-basics | numpy.json | 3/3/1 | 7 |
| 07 | pandas-series-dataframe | pandas-basics.json | 4/3/0 | 7 |
| 08 | indexing-filtering-sorting | indexing.json | 4/4/2 | 10 |
| 09 | groupby-aggregation | groupby.json | 3/4/3 | 10 |
| 10 | merge-join-concat | merge.json | 2/3/3 | 8 |
| 11 | pivot-crosstab-apply | pivot.json | 1/4/3 | 8 |
| 12 | strings-and-datetime | text-dates.json | 2/4/3 | 9 |
| 13 | missing-duplicates-outliers | missing.json | 2/4/3 | 9 |
| 14 | data-cleaning-workflow | cleaning.json | 0/3/3 | 6 |
| 15 | eda-workflow | eda.json | 1/2/2 | 5 |
| 16 | matplotlib-seaborn | viz.json (3 text) | 2/2/2 | 6 |
| 17 | regression-overview | regression.json | 1/2/2 | 5 |
| 18 | jupyter-notebooks | jupyter.json (all text) | 3/1/0 | 4 |
| 19 | git-github-basics | git.json (all text) | 3/2/0 | 5 |
| 20 | messy-dataset-exercises | messy-exercises.json | 0/0/10 | 10 |
Totals: 130 = 42 easy / 49 medium / 39 hard (hard includes the 10 messy exercises); 117 python, 13 text.
Gap check vs spec topics: basics, loops, functions, comprehensions, files, NumPy, Series/DataFrame, loc/iloc, filtering, sorting, groupby, merge, pivot, apply, strings, datetime, missing, duplicates, outliers, cleaning workflow, EDA, matplotlib/seaborn, regression, Jupyter, Git/GitHub: all covered. 10 messy exercises = lesson 20.
Writers may add 2-4 extra questions per file if validation shows a question is unusable (keep ids unique).

## Extra assets
1. EDA checklist (reusable): lesson 15 holds the 10-step list as `<FormulaCard>`; also Task F writes a downloadable text: `public/downloads/eda-checklist.md` (10 steps, each with 2 check bullets and a pandas one-liner). Cleaning checklist (8 steps) similar, in same file.
2. Starter notebooks (a script generates .ipynb from specs; Task G writes the specs as JSON `scripts/notebooks/specs/<name>.json`: {title, dataset, cells:[{type:"markdown"|"code", source}]}; outputs into `public/downloads/notebooks/<name>.ipynb`). Specs, each ~12–18 cells, code uses `pd.read_csv("<dataset>/<table>.csv")` with a note on where to put the CSVs (zip on site) and a first markdown cell explaining purpose:
 - 01-eda-template.ipynb: generic EDA skeleton with the 10 checklist steps as markdown headings and generic code (df placeholder via variable `PATH`; fill by learner; no TODO text — use "Set PATH to your file").
 - 02-fintech-upi-cleaning.ipynb: fintech.transactions: ₹ text, mixed dates, dupes, outliers, cleaned export, cleaning log.
 - 03-fintech-failure-analysis.ipynb: failure rate by bank/hour/app, peak pattern, pivot, findings template.
 - 04-ecommerce-sales-eda.ipynb: orders+items+products+customers merge, monthly revenue, category returns, Prime vs non-Prime.
 - 05-subscription-funnel-retention.ipynb: trial->paid conversion by platform/source, monthly cohort retention table.
 - 06-pandas-cheatsheet-practice.ipynb: 20 short exercises with empty code cells ("Write your code below") for groupby/merge/pivot on ecommerce.
 - 07-matplotlib-seaborn-gallery.ipynb: 8 charts on fintech/ecommerce data with chart-chooser markdown.
 - 08-regression-intro.ipynb: delivery distance vs minutes, numpy and (commented) sklearn, residual plot.
 Download links used in lessons 15/16/17/18 via `<Download href="/downloads/notebooks/..." />` (only after the files exist; writer of lesson adds links last, check path).

## Writer tasks (Haiku), 9 tasks
- A: lessons 01,02,03,04 + basics, loops, functions, comprehensions (16 q; none dataset).
- B: lessons 05,06 + file-handling, numpy (12 q).
- C: lessons 07,08 + pandas-basics, indexing (17 q).
- D: lessons 09,10 + groupby, merge (18 q).
- E: lessons 11,12 + pivot, text-dates (17 q).
- F: lessons 13,14 + missing, cleaning (15 q) + public/downloads/eda-checklist.md? (only if orchestrator confirms path convention).
- G: lessons 15,17 + eda, regression (10 q) + notebook specs (8 JSON files).
- H: lessons 16,18,19 + viz, jupyter, git (15 q, mostly text).
- I: lesson 20 + messy-exercises (10 hard q) — heaviest; give a stronger model or split 5/5.

## Open questions
- Where do downloadable files live (public/downloads/?) and which script consumes notebook specs? Needs orchestrator decision.
- fintech transactions raw full-row dupes counted 48 (not ~90 as schema note); writers must read real values.
- campaigns.budget_inr is text in CSV for some rows (₹8,000): avoid thresholds on it.
