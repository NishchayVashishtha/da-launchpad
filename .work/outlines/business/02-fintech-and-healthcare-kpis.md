# 02-fintech-and-healthcare-kpis  (topic: fintechkpi; 12 practice: 8 sql fintech, 4 text) PRIORITY LESSON (fintech > health)
fm: title "Fintech and healthcare analytics: KPIs in practice"; description "Compute UPI success rate, TPV and fraud-flag rate in SQL, then apply the same thinking to hospital and telehealth numbers."; order 2; estimatedMinutes 60; objectives: compute TPV, success rate, avg ticket, active users from raw transactions; cut a rate by app/bank/hour; handle duplicates and outliers; read fraud flags as precision/recall trade-off; explain healthcare KPIs and privacy limits; tags: business, fintech, healthcare, sql, kpi
## Concept
- Fintech vocabulary: TPV (total payment value, successful only), success rate, technical decline vs business decline (failure_code), P2P vs P2M, MAU, take rate (explain: a PSP earns on merchant fees), retry rate, fraud rate, KYC tiers.
- Always: success = status='SUCCESS'; PENDING excluded from both TPV and failure numerators but kept in denominator (say so, show alternative).
- Clean first: DISTINCT txns; amounts > 50,000 are suspicious (10 rows) - check, don't silently delete.
- Healthcare KPIs again, with data caveats: small counts, seasonality (monsoon fevers), privacy (never show patient-level rows; aggregates with n<10 suppressed).
- Analogy: UPI success rate is like a railway's punctuality %: one bad station (bank) hurts the whole line.
## Worked examples (dataset fintech, run sqlite3 and paste actual output)
1. TPV and success rate by year (DISTINCT) -> facts: 2023 Rs 12,828,210; 2024 Rs 17,045,673; txns 9,613/12,687.
2. Failure rate by payment_app: NammaPay 5.10% vs ~2.2% others -> follow-up cut by day: outage days.
3. Failure rate by bank, ordered; Kaveri Co-op 6.58 (raw numbers; with DISTINCT slightly different - paste actual).
4. Flag rate by hour bucket (night vs day: 5.03% vs 1.26%).
## Common mistakes
- Forgetting DISTINCT (inflates ~0.4%) | failure rate = failed/success instead of failed/all | counting TPV on FAILED txns | averaging per-bank rates instead of weighted | reading a 5% rate from 12 txns | treating PENDING as failed without stating.
## Quiz: TPV definition; failure-rate denominator; why average ticket flat but TPV up; precision vs recall of fraud rule; healthcare no-show denominator.
## Interview Qs: success rate dropped 1pp today - what do you check? | define TPV | how would you measure UPI app health | fraud flag rule trade-off | KPIs for a telehealth consult.
## Takeaways 5. FurtherReading: mode-sql, sqlite-docs.
## Practice (fintech.json -> topic fintechkpi; file src/content/practice/business/fintechkpi.json; language sql unless noted; dataset fintech)
| id | diff | lang | ask | output | approach | mistake |
| business-fintechkpi-001 | easy | sql | Ops head: total number of transactions and total TPV (SUCCESS only, Rs, rounded 0dp). cols txn_count, tpv | 1 row 22300, 29873883 (verify) | CTE DISTINCT, SUM CASE | counting raw 22,389 |
| -002 | easy | sql | Overall failure rate % (2dp) of distinct transactions | cols failure_rate_pct; 2.70 | AVG(status='FAILED')*100 | dividing by successes |
| -003 | easy | sql | Txn count and failure % per payment_app, worst first. cols payment_app, txns, failure_pct | 5 rows NammaPay first 5.10 | GROUP BY | no DISTINCT |
| -004 | medium | sql | Average ticket (success only) per txn_type, 1dp, highest first. cols txn_type, avg_ticket | 4 rows | AVG(amount) WHERE SUCCESS | including failed amounts |
| -005 | medium | sql | Monthly TPV in Rs lakh (1dp) for 2024. cols month ('2024-01'), tpv_lakh; ordered by month; 12 rows | 11.0 ... 15.7 | strftime | strftime on text dates wrong format -> none |
| -006 | medium | sql | Banks with failure % > 3 and at least 500 txns. cols bank, txns, failure_pct; orderMatters failure_pct desc | Kaveri, PayNova (fill) | HAVING | HAVING on alias without min-volume |
| -007 | medium | sql | Active users (distinct user_id with >= 1 success) per year; cols year, active_users | 2023 ~1,7xx, 2024 ~2,6xx (fill) | COUNT DISTINCT | counting txns |
| -008 | hard | sql | Flagged-rate % (2dp) for night (23-04h) vs day. cols time_band ('night','day'), txns, flagged, flag_rate_pct | night 577/29/5.03; day 21723/273/1.26 | CASE on strftime('%H') | forgetting hours 0-4 wrap |
| -009 | medium | text | Hospital telehealth: 1,400 booked consults, 1,176 held; 8% of held needed repeat. Compute consult completion % | {value} 84.0 | | |
| -010 | medium | text | Why must a hospital dashboard suppress cells with n < 10? (md, 3 bullets) | text | | |
| -011 | hard | text | Fraud rule "flag all night txns" hits 577 txns of which 29 were truly flagged. Precision percent (2dp)? | {value} 5.03 | confusing precision with recall (recall = 29/302 = 9.60) |
| -012 | hard | sql | Failure percent for Healthcare+Pharmacy merchant txns vs all other merchant categories (join merchants; P2P rows have no merchant so drop out). cols segment (health, other), txns, failure_pct; order by segment | health 1227 txns 2.53; other 15648 2.74 | JOIN + CASE | joining on users |
