# 09 groupby and aggregation
plan: title "groupby: summarise by category" | desc "Split, summarise, combine: the heart of analysis." | order 9 | 45 min | tags python, pandas, groupby, agg
objectives: use groupby with one/many keys; named aggregation; transform and size/count/nunique; rank within groups; rate/share calculations; reset_index
## concept
- Analogy: sort bills into piles by month, then total each pile (split-apply-combine).
- `df.groupby("c")["v"].sum()`; `.agg(total=("v","sum"), n=("v","count"))`; size vs count (count skips NaN); nunique.
- Multiple keys -> MultiIndex; `reset_index()`; `as_index=False`.
- `transform` (add group total column -> share of group); `rank(method)`; `idxmax`; `groupby().head(n)` / `nlargest` within group.
- Mean of rates vs rate of sums (weighted) – Simpson trap.
- groupby drops NaN keys by default (`dropna=False`).
- SQL bridge: GROUP BY == groupby; HAVING == filter after agg.
- FormulaCard: "Rate = sum(events) / sum(attempts), not mean of group rates".
## worked examples
1. fintech: failure rate by `bank` (status=="FAILED" mean) sorted desc (Kaveri Co-op Bank signal; dedupe first).
2. ecommerce: orders per `sales_channel`, cancel share.
3. transform: each order_item's share of its order total.
4. top product per category via sort + groupby.head(1).
## common mistakes
- Averaging averages. | forgetting reset_index then merge fails. | size vs count confusion. | grouping on dirty keys (' Pune' vs 'Pune'). | dedupe missing -> inflated counts. | agg on text column.
## quiz
1 `size` vs `count`. 2 rate by group of boolean. 3 what groupby does with NaN keys. 4 named agg syntax. 5 transform returns same length as input.
## interview Qs
- groupby internals (split-apply-combine). | find top 3 products per category. | agg vs transform vs apply. | count distinct customers per month. | why mean of means is wrong.
## takeaways: groupby = GROUP BY; named agg is readable; rate = sum/sum; clean keys first; dedupe first; transform keeps shape.
further reading: pandas-docs, mode-sql
## practice (groupby.json, topic "groupby"). Note: writers must dedupe where noted.
| id | diff | lang | ds | ask | output | approach | mistake |
|---|---|---|---|---|---|---|---|
| python-groupby-001 | easy | python | ecommerce | Orders per order_status after dropping exact duplicate rows; Series sorted desc | Series | drop_duplicates + value_counts | dupes inflate Delivered |
| python-groupby-002 | easy | python | hr | Headcount per department_id (employees dedup by employee_id), asc by id | DataFrame department_id, headcount | groupby size | dupes |
| python-groupby-003 | easy | python | marketing | Total spend_inr per campaign_id (drop dup ad_spend rows), top 5 by spend, columns campaign_id,total_spend round 2 | 5x2 ordered | groupby sum | 100x outliers mention (not removed here) |
| python-groupby-004 | medium | python | fintech | Failure rate % per payment_app (dedupe by txn_id), 2 dp, desc, columns payment_app, failure_rate_pct | 5x2 ordered | groupby mean of boolean *100 | includes PENDING in denominator? define: denom all rows |
| python-groupby-005 | medium | python | subscription | Number of distinct users per plan with a subscription row; columns plan, users | 3x2 | nunique | count rows rather than users |
| python-groupby-006 | medium | python | food_delivery | Average actual_minutes and delivery count per weather (delivered only), 1 dp | DataFrame | named agg | NaN of cancelled |
| python-groupby-007 | medium | python | retail | Total units quantity per store_id per category (top 10 by qty tie store_id,category) | 10x3 | multi-key groupby | forgot reset_index |
| python-groupby-008 | hard | python | ecommerce | Return rate per product category: returned order_items / total order_items; join order_items->products, left merge returns; cols category, return_rate_pct (2dp) desc | rows by category | merge + groupby | inner join drops non-returned items -> 100% |
| python-groupby-009 | hard | python | fintech | For each user (dedupe txn), share of their total amount that is in their largest txn; return top 5 users with at least 5 SUCCESS txns by share; amount cleaned from ₹ text | 5x2 | clean amount, groupby agg max/sum | amount text sum concatenates strings |
| python-groupby-010 | hard | python | hr | Top-paid employee per department from latest salary row per employee (latest effective_date), clean annual_ctc text, cap outliers? (exclude ctc>5e7); cols department_id, employee_id, annual_ctc | by dept | sort+groupby.head(1) | 100x outlier wins; text sort |
