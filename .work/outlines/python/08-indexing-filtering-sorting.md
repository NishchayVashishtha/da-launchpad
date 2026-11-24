# 08 Indexing, loc/iloc, filtering and sorting
plan: title "Selecting rows: loc, iloc, filters and sort" | desc "Pull out exactly the rows and columns you need." | order 8 | 40 min | tags python, pandas, loc, iloc, filter, sort
objectives: use loc and iloc; filter with boolean masks and `&|~`; use isin, between, str.contains, query; sort by multiple keys; get top-N
## concept
- Analogy: loc = find by label (roll number); iloc = by position (bench seat).
- Slicing: loc end-inclusive, iloc end-exclusive.
- Mask: `df[df.status=="FAILED"]`; combine with `&`, `|`, `~` + parentheses; isin; between; isna; str.contains(case=False,na=False).
- `df.query("amount > 5000")`; `.loc[mask, "col"]` for safe set.
- sort_values(by=[...], ascending=[False,True]); nlargest/nsmallest; head; reset_index(drop=True); set_index.
- Boolean indexing returns a copy; avoid SettingWithCopy by `.loc`.
- Tie in sort: be deterministic (add tie-breaker).
## worked examples
1. fintech transactions: failed UPI P2M txns; count (status=="FAILED" & txn_type=="P2M").
2. ecommerce customers with Prime and city Pune (watch ' Pune' whitespace -> then strip).
3. nlargest 5 order_items by line_total with product_id tie-break.
4. loc vs iloc same 3 rows with output.
## common mistakes
- `and` instead of `&`. | missing parentheses (precedence). | `==` on NaN. | using iloc with labels after filtering (index not reset). | `df[df.a==1]["b"]=0` no effect. | sorting strings that look numeric ('₹' text).
## quiz
1 loc[2:4] returns 3 rows. 2 `~mask`. 3 `isin(["Pune","Delhi"])`. 4 `df.sort_values("a", ascending=False)` ... 5 safe assignment pattern `.loc[mask,"col"]=`.
## interview Qs
- loc vs iloc. | why `&` not `and`. | SettingWithCopyWarning cause. | get top 3 per group (preview groupby). | filter rows where a string contains a word ignoring case/NaN.
## takeaways: masks are boolean columns; parenthesise; loc for labels, iloc for position; sort with tie-breakers; assign only through .loc.
further reading: pandas-docs
## practice (indexing.json, topic "indexing")
| id | diff | lang | ds | ask | output | approach | mistake |
|---|---|---|---|---|---|---|---|
| python-indexing-001 | easy | python | fintech | Count of FAILED transactions (raw rows) | int | mask sum | includes PENDING |
| python-indexing-002 | easy | python | ecommerce | order_items with quantity >= 5: row count | int | filter len | `>` vs `>=` |
| python-indexing-003 | easy | python | hr | HR: how many employees (raw rows) have work_mode "Remote"? | int | filter, len | case-sensitive typo "remote" gives 0 |
| python-indexing-004 | easy | python | marketing | Marketing: campaign_name list (sorted) for campaigns on channel "Meta Ads" | list | mask + sorted | returning DataFrame not list; exact channel spelling |
| python-indexing-005 | medium | python | fintech | Fraud desk: count transactions (raw rows) with is_flagged==1 and txn_type=="P2P" and status=="SUCCESS" | int | multi-mask with & and parentheses | missing parentheses -> ValueError/precedence bug |
| python-indexing-006 | medium | python | ecommerce | Top 5 order_items by line_total: columns order_item_id, line_total; ties by order_item_id asc | 5x2, orderMatters | sort_values two keys + head | no tie-break |
| python-indexing-007 | medium | python | food_delivery | Deliveries delivered late (delay_minutes>15) in rainy weather (check values): count | int | mask | NaN delay rows from cancelled |
| python-indexing-008 | medium | python | retail | Stores whose city contains "pur" (case-insens.) names sorted | list | str.contains(case=False, na=False) | case-sensitive misses |
| python-indexing-009 | hard | python | subscription | Users not on iOS and not on Android (platform) with signup in 2024: count — platform values must be inspected; handle DD-MM-YYYY signup_date via parse | int | normalise date, mask | string compare of dates mixes formats |
| python-indexing-010 | hard | python | hr | Employees hired on or after 2022-01-01 with job_level in two named levels, sorted by hire_date then employee_id; return first 10 employee_id, hire_date(ISO) | 10x2 | parse mixed dates, isin, sort | DD-MM-YYYY strings sort wrongly |
