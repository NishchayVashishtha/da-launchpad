# 11 pivot_table, crosstab and apply
plan: title "pivot_table, crosstab and apply" | desc "Reshape summaries like an Excel pivot and apply custom logic." | order 11 | 40 min | tags python, pandas, pivot, apply
objectives: build pivot_table with index/columns/values/aggfunc; add margins; use crosstab and normalize; melt wide to long; use apply/map/np.select safely
## concept
- Analogy: Excel PivotTable you already know, written in code.
- `pd.pivot_table(df, index, columns, values, aggfunc, fill_value, margins=True)`; multiple aggfuncs; `pd.crosstab(a,b,normalize="index")`.
- `melt` and `stack/unstack` idea. 
- `apply(axis=1)` row-wise is slow; prefer `np.select`, `np.where`, `.map(dict)`, `.str`, `.dt`.
- `pd.cut` / `qcut` for buckets (age, order value bands).
- Reset_index to flatten pivot for charts.
## worked examples
1. fintech: pivot txn count by payment_app x status.
2. crosstab normalize: status share per txn_type (rows sum to 1).
3. ecommerce: pd.cut order_items line_total bands; counts.
4. `.map` payment_method to group (UPI/Card/Wallet -> Digital vs COD) then pivot.
## common mistakes
- Default aggfunc is mean not sum. | NaN cells from missing combos (fill_value). | apply row-wise on 1 lakh rows. | cut bins edge inclusion (right=True). | normalize axis confusion. | pivoting without dedupe.
## quiz
1 default aggfunc -> mean. 2 `margins=True` adds totals. 3 crosstab normalize="index" -> row shares. 4 prefer which for if-else column -> np.where/np.select. 5 `pd.cut` returns intervals.
## interview Qs
- pivot_table vs groupby. | apply vs vectorised. | crosstab vs pivot_table. | wide vs long format, why long for plotting. | create age buckets.
## takeaways: pivot_table = Excel pivot; check aggfunc; fill_value; avoid row-wise apply; cut for bands.
further reading: pandas-docs, excel-support
## practice (pivot.json, topic "pivot")
| id | diff | lang | ds | ask | output | approach | mistake |
|---|---|---|---|---|---|---|---|
| python-pivot-001 | easy | python | fintech | Transaction counts by txn_type (rows) and status (cols), dedupe by txn_id; DataFrame | pivot | pivot_table aggfunc count or crosstab | dupes counted |
| python-pivot-002 | medium | python | ecommerce | Orders (dedupe) by sales_channel rows x order_status cols, as % of row (round 1) | crosstab normalize | normalize="index"*100 | normalize all |
| python-pivot-003 | medium | python | subscription | Subscription count by plan x status | pivot | crosstab | |
| python-pivot-004 | medium | python | food_delivery | Average delivery_fee by city (rows) x payment_mode (cols), delivered rows, 1 dp; clean city with strip/title first | pivot | strip/title then pivot | dirty city adds rows |
| python-pivot-005 | medium | python | ecommerce | Bucket order_items by unit_price bands <500, 500-1999, 2000+ ; return count per band in that order Series | Series | pd.cut | edges right=True 500 in wrong band |
| python-pivot-006 | hard | python | retail | Monthly net sales by category (rows month yyyy-mm, cols category) for first 3 months; clean net_amount_inr ₹text, dedupe sale_id, parse dates; 0 for empty | pivot 3 rows | clean+parse+pivot | strings sum |
| python-pivot-007 | hard | python | hr | Wide to long: from performance_reviews build manager_rating & self_rating melted; return mean per (rating_type) | 2 rows | melt+groupby | |
| python-pivot-008 | hard | python | fintech | Tag each txn with segment using np.select: "Small" <500, "Medium" <5000, "Large" else (clean amount, dedupe); return share % of txns per segment 1 dp, Small/Medium/Large order | Series | np.select | conditions order / text amount |
