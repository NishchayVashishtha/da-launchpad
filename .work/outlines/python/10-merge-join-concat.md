# 10 merge, join and concat
plan: title "Combining tables: merge, join, concat" | desc "Bring related tables together without duplicating rows." | order 10 | 40 min | tags python, pandas, merge, join
objectives: merge on keys with inner/left/right/outer; check row counts before/after; handle key dtype and duplicate keys; use concat to stack; find unmatched rows with indicator
## concept
- Analogy: matching exam roll numbers to marks sheet.
- `pd.merge(left, right, on=, how=, suffixes, indicator=True)`; left_on/right_on; `validate="m:1"`.
- Join types visual; row-count rule: left join with unique right key keeps left rows; duplicate keys -> explosion.
- Anti-join: left merge + indicator, filter `_merge=="left_only"`.
- concat(axis=0) for same-schema months; `ignore_index=True`.
- Dedupe dimension tables first (customers has 20 exact duplicates!).
- SQL bridge: JOIN types same names.
## worked examples
1. ecommerce: orders left join customers (dedupe customers first): rows 10100 stays (note orders dupes).
2. fintech: users with no transactions (anti-join).
3. validate="m:1" raising MergeError on duplicate keys.
4. concat two filtered frames; count rows.
## common mistakes
- Many-to-many join inflates sums. | wrong how -> lost rows. | key dtype mismatch (int vs str). | suffixes `_x/_y` confusion. | not checking row counts. | merge then filter changes meaning (left join + where).
## quiz
1 left join keeps all left rows. 2 duplicate right keys effect. 3 `indicator` use. 4 concat vs merge. 5 what `validate` does.
## interview Qs
- inner vs left. | How do you find customers who never ordered. | merge vs join vs concat. | How to avoid duplicate row explosion. | merge on different column names.
## takeaways: check keys unique; check counts; left join when keeping base; anti-join via indicator; dedupe dims first.
further reading: pandas-docs
## practice (merge.json, topic "merge")
| id | diff | lang | ds | ask | output | approach | mistake |
|---|---|---|---|---|---|---|---|
| python-merge-001 | easy | python | ecommerce | Orders (drop dup rows) joined to customers (drop dups): count rows with customer city NULL | int | merge left + isna | dup customers inflate |
| python-merge-002 | easy | python | hr | Employees (dedup) merge departments: count per department_name, columns name, headcount sorted desc, name asc | DataFrame | merge+groupby | dupes |
| python-merge-003 | medium | python | fintech | Users (dedup) with zero transactions (any status): count | int | anti-join | inner join |
| python-merge-004 | medium | python | ecommerce | Revenue (sum of line_total) by product category, 2dp; columns category, revenue; desc | DataFrame ordered | merge order_items to products then groupby | merging on wrong key or forgetting reset_index |
| python-merge-005 | medium | python | marketing | Click-to-conversion rate % per campaign_name (dedupe clicks); cols campaign_name, conv_rate_pct 2dp top 5 | 5x2 | left merge, mean | inner join -> 100% |
| python-merge-006 | hard | python | subscription | Users who signed up but never had a subscription row, by acquisition_source: counts desc, source asc | DataFrame | dedupe users, anti-join | dup users counted |
| python-merge-007 | hard | python | food_delivery | Average overall_rating per restaurant cuisine for restaurants with >=30 ratings; cols cuisine, avg_rating(2), n | DataFrame | merge ratings->restaurants | filter before merge |
| python-merge-008 | hard | python | fintech | Failure reason breakdown: merge failed_transactions (dedupe) to transactions (dedupe) to get bank; top 5 (bank, failure_code) pairs by count tie by bank, code | 5x3 | double merge | merging on wrong key |
