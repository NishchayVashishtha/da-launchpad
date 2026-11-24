# 05-cohort-retention  (topic: cohort; 10 practice: 7 sql subscription, 3 text)
fm: title "Cohort analysis and retention"; description "Group users by when they started and see how many stay."; order 5; estimatedMinutes 55; objectives: define a cohort and a retention curve; build a cohort table in SQL; read a heatmap; spot a bad cohort; tags: business, cohort, retention, sql, subscription
## Concept
- Cohort = group of users sharing a start event/time (signup month, first payment month). Retention at month N = share of the cohort still active in month N. Analogy: class of students admitted in 2023: how many still enrolled each year.
- Why not overall churn: mixes old and new users; cohorts show if product got better/worse. Calendar vs relative (month 0,1,2) axes.
- Retention types: classic, rolling/unbounded. Cohort table: rows cohort month, columns month 0..N, cells % ; heatmap colour. Survivorship caution: recent cohorts have fewer months.
- Define "active" explicitly (paid and not cancelled / any app_open / any txn).
- Fintech: first-txn cohorts, "active in month N = at least 1 txn". Health: patients with a repeat visit within 90 days.
- FormulaCard: retention(N) = active users in month N / cohort size.
## Worked examples (subscription)
1. Cohort size = paid users by signup month, then 60-day churn: 2024-03 54.0% (27 of 50) vs ~20-25% neighbours (facts list). 
2. Month-1/2 retention table via events (app_open by month since signup) for 2024-01..2024-06 cohorts (script; paste real). Mention instructor signal: March worse.
3. Read the heatmap for March 2024; hypotheses to test next (campaign, pricing change, bug) - no claims without data.
4. UPI first-txn cohort (fintech; txn_datetime, DISTINCT): share of 2023-01 first-txn users active again in month +1, +2 (script).
## Common mistakes
- Using calendar month instead of months since start | counting inactive recent cohort as 0 retention | different "active" definitions per cohort | small cohort conclusions (n=27) | not de-duping users | mixing paid and trial cohorts.
## Quiz: what is a cohort; month 0 = 100%; survivorship; reading drop between M0 and M1; choosing active definition.
## Interview Qs: how would you analyse retention of a new UPI app | cohort vs segmentation | what retention curve flattening means | March cohort churned 2x - what next | how to define active for a hospital app.
## Takeaways 5. FurtherReading: mode-sql, sqlite-docs.
## Practice (cohort.json) dataset subscription unless noted; DISTINCT users/subs
| business-cohort-001 | easy | sql | Signups per month in 2024, cols signup_month (YYYY-MM), signups, ordered by month | 12 rows; Mar = 244 on DISTINCT users (raw table gives 245); other months: fill with script | substr(signup_date,1,7) | counting raw duplicate users |
| -002 | easy | sql | Paid users per signup month for 2024 (paid_start_date not null) cols signup_month, paid_users | Jan 55, Feb 39, Mar 50, Apr 52, May 72, Jun 50, Jul 66 ... | join | |
| -003 | medium | sql | Trial->paid % per 2024 signup month, 1dp; ordered by month | Jan 35.0 ... Dec 29.5 | | |
| -004 | medium | sql | For signup months 2023-10..2024-07: paid users, users cancelled within 60 days of paid_start_date, churn60_pct (1dp) | 2024-03 -> 50, 27, 54.0 | julianday diff | counting any cancel (not within 60) |
| -005 | hard | sql | Same as -004 but return ONLY months whose churn60_pct is more than 1.5x the average of all those months' churn60_pct; (expect only 2024-03) | 1 row | window avg / CTE | comparing to median |
| -006 | hard | sql | Cohort table: for each 2024 signup month (Jan-Jun), number of users with an app_open event in month 0, 1, 2 after signup month (cols cohort, m0, m1, m2); use LOWER(event_name) | (fill) | strftime + date math | not lowercasing |
| -007 | medium | sql | fintech: users by first-transaction month (DISTINCT txns), top 6 months by count; cols first_month, new_users | (fill) | MIN(txn_datetime) per user | using signup_date (dirty formats) |
| -008 | easy | text | Cohort 200 users, 140 active in month 1 -> retention % | {value} 70.0 | |
| -009 | medium | text | Cohort of 50 paid, 27 cancelled in 60 days vs avg 22%: how many cancellations would be expected at 22%? (value, 1dp) | {value} 11.0 | |
| -010 | hard | text | Name 4 hypotheses for the March 2024 cohort and the one data cut for each (md) | text | |
