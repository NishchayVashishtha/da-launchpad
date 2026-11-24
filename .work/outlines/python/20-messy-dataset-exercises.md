# 20 Ten messy-dataset mini exercises
plan: title "10 messy-data mini exercises" | desc "Clean real-looking dirty tables and answer a business question each time." | order 20 | 90 min | tags python, cleaning, practice, messy-data
objectives: spot rupee text, mixed dates, duplicates, casing and outliers quickly; apply the 8-step cleaning workflow; produce a checked number; explain assumptions
## concept (short lesson, then the exercises are in PracticeSet)
- How to use: for each exercise first list the problems (use the Problem Spotter table), then clean, then answer.
- Problem Spotter table (the CSVs on this site are deliberately messy): dataset/table/column -> problem. Include: fintech.transactions.amount (₹ text, 100x outliers, ~90 dup rows, mixed txn_datetime); ecommerce.orders.total_amount (₹ text, mixed order_date, dup rows); ecommerce.returns.refund_amount (₹ Indian grouping); hr.salaries.annual_ctc (₹ text, 5 x100); hr.employees (M/F gender, dup rows, mixed dates, city case); subscription.subscriptions.price_inr (text ₹); subscription.events (case issues, dups); retail.sales (mixed sale_datetime, ₹ net, payment_mode case, dup sale_id); food_delivery.deliveries (₹ order_value, mixed order_time, 8 outliers); food_delivery.promo_usage (promo_code case, ₹ discount text); marketing.clicks (dups, city/device case).
- Reusable helper snippets (show in Concept): `clean_inr(s)`, `parse_mixed_date(s)`, `std_text(s)`, outlier flag. Learners paste into each exercise (solutions in site also define them inline since each solution is standalone).
- Ground rules: always dedupe exact rows; treat >10x median as entry error where stated; state assumptions.
- No Further "worked examples" beyond 2: (1) walk through exercise 1 fully; (2) how to verify a result with sanity checks (totals, row counts, min/max).
## common mistakes
- Dedupe after summing. | parse dates with dayfirst only. | clean only the column you see and miss the ₹ rows. | trust NaT silently. | forget to state assumptions.
## quiz
1 first inspect step. 2 ₹ regex. 3 dedupe before/after aggregation. 4 mixed date approach. 5 sanity check example.
## interview Qs
- You get a messy export, first 30 minutes? | How verify cleaning was right. | A total differs from finance by 2% — what do you check? | Explain how you handled outliers.
## takeaways: spot, clean, validate, answer, state assumptions.
further reading: pandas-docs, kaggle-learn
## practice (messy-exercises.json, topic "messy"; all hard, python; each is a 5-step task with a single numeric/table answer)
| id | diff | lang | ds | ask | output | approach | mistake |
|---|---|---|---|---|---|---|---|
| python-messy-001 | hard | python | fintech | UPI ops head: total SUCCESS amount per payment_app (rounded 0), after dedupe by txn_id and excluding amount > 1,000,000 (100x entry errors); columns payment_app,total_amount desc | 5 rows | clean ₹, dedupe, filter, groupby | summing text; dupes |
| python-messy-002 | hard | python | ecommerce | Finance: Delivered revenue (total_amount) per month 2024-01..2024-03 from orders with mixed date formats and ₹ text, dedupe order_id | 3 rows month,revenue | two-format parse | month/day swap |
| python-messy-003 | hard | python | hr | HR: average annual_ctc (₹, rounded 0) per job_level using each employee's latest salary row, ₹ text cleaned and values >5e7 removed | rows per level | sort latest, clean | latest by string date |
| python-messy-004 | hard | python | subscription | Product: average price_inr per plan after cleaning ₹ text (billing cycles kept separate): plan x billing_cycle pivot 0 dp | pivot | clean, pivot | text mean |
| python-messy-005 | hard | python | retail | Retail head: top 5 store_id by net sales after cleaning ₹ text, dedupe sale_id, excluding net_amount_inr > 1,000,000; columns store_id,net_sales(0dp) desc | 5 rows | clean, dedupe, filter, groupby | summing text |
| python-messy-006 | hard | python | food_delivery | Ops: average order_value (clean ₹, drop >40,000 entry errors, dedupe delivery_id) per standardised city top 5 | 5 rows | strip/title city | dirty city splits |
| python-messy-007 | hard | python | ecommerce | Returns: total refund_amount (₹ Indian grouping) per return_reason desc, rounded 0 | rows | clean '₹1,23,456.00' | float() fails |
| python-messy-008 | hard | python | marketing | Growth: after dropping exact duplicate clicks and standardising city (strip/title, drop NULL), top 5 cities by clicks; columns city,clicks desc, city asc tie | 5 rows | | casing splits cities |
| python-messy-009 | hard | python | food_delivery | Promo team: total discount_amount (₹ text) per standardised promo_code (strip/upper), top 5 | 5 rows | | casing splits codes |
| python-messy-010 | hard | python | subscription | Growth: signups per month for 2024 (users dedupe, mixed signup_date) as 12 rows | 12 rows | | |
