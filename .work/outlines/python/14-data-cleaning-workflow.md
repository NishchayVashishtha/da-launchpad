# 14 The data cleaning workflow
plan: title "A repeatable data cleaning workflow" | desc "Clean any messy table in the same eight steps." | order 14 | 45 min | tags python, pandas, cleaning, workflow
objectives: apply an 8-step cleaning checklist; build a `clean_*` function; log before/after counts; validate with asserts; save a cleaned file
## concept
- Analogy: kitchen mise-en-place; same order each time.
- Steps: 1 Load raw read-only copy. 2 Inspect (shape, dtypes, nulls, dupes, value_counts). 3 Fix types (₹ text, dates). 4 Standardise text (strip, case, map synonyms 'M'->'Male'). 5 Handle missing. 6 Remove duplicates. 7 Handle outliers. 8 Validate (asserts) and export.
- Keep raw untouched; write cleaning as a function/pipeline `.pipe()`; assertions (`assert df.txn_id.is_unique`).
- Cleaning log table (step, rows before, rows after, note).
- Do not over-clean; keep decision notes (README).
- FormulaCard: 8-step checklist.
## worked examples
1. hr employees: gender M/F map, city standardise, dates parse, dedupe; log.
2. clean function for fintech transactions: amount, datetime, dedupe; assert unique txn_id.
3. validate with asserts; show passing & a failing example.
4. cleaning log printed as DataFrame.
## common mistakes
- Cleaning in place on the only copy. | fixing types after dedupe (dupes differ?). | silent coerce. | no validation. | mapping synonyms but forgetting NaN. | irreproducible manual edits.
## quiz
1 order of steps first -> inspect. 2 why `.pipe`. 3 assert purpose. 4 map for M/F. 5 keep raw copy.
## interview Qs
- Describe your cleaning process. | How do you make cleaning reproducible. | How do you validate. | Biggest issue found. | Tell about a time cleaning changed the answer.
## takeaways: same steps every time; raw stays raw; function + log; assert after; document decisions.
further reading: pandas-docs, kaggle-learn
## practice (cleaning.json, topic "cleaning")
| id | diff | lang | ds | ask | output | approach | mistake |
|---|---|---|---|---|---|---|---|
| python-cleaning-001 | medium | python | hr | Employees: map gender M/F to Male/Female, dedupe; return counts per gender incl NaN as "Unknown" | Series | map+fillna | dedupe order |
| python-cleaning-002 | medium | python | ecommerce | Clean customers: dedupe, strip/title city; return rows and distinct cities as dict | dict | | |
| python-cleaning-003 | hard | python | fintech | Clean transactions (amount ₹text->float, dedupe by txn_id); return dict {rows, total_success_amount excluding amounts >1e6 (100x outliers)} 2dp | dict | multi step | |
| python-cleaning-004 | hard | python | subscription | Clean events: dedupe, event_name lower, platform title; return top 5 event_name counts | Series | | uppercase split groups |
| python-cleaning-005 | hard | python | retail | Clean sales: dedupe, payment_mode strip/lower with NaN as "unknown", net ₹ text; share % of net sales by payment mode 1 dp | Series | | |
| python-cleaning-006 | medium | python | marketing | Clean clicks: dedupe, device lower/strip, city title; counts per device | Series | | |
