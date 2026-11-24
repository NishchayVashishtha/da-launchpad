# 01-kpis-metrics-by-industry  (topic: kpis; module business; 10 practice, all text)
fm: title "KPIs and metrics by industry"; description "Know which numbers each industry watches, and why a metric is not a KPI until it is tied to a goal."; order 1; estimatedMinutes 45; objectives: tell metric from KPI; list the 5-6 core KPIs of e-commerce, fintech (UPI), SaaS/subscription, food delivery, healthcare, HR; separate input/output/guardrail metrics; pick a North Star for a business; tags: business, kpi, metrics, industry
## Concept
- Metric = any number. KPI = metric tied to a goal, with owner, target, period. Analogy: car dashboard - speed is a metric; "reach Pune by 6 pm" makes speed a KPI.
- Types: input (what team controls, e.g. ad spend), output (result, e.g. revenue), guardrail (must not break, e.g. return rate), vanity (looks good, drives nothing: page views, app downloads).
- Leading vs lagging. North Star metric (one number that captures value delivered).
- Industry table (one per industry, 5-6 KPIs each, with formula): 
  - E-commerce (DesiCart): GMV, orders, AOV, conversion rate, repeat purchase rate, return rate, CAC, cancellation/RTO rate.
  - Fintech/UPI: TPV, txn count, success rate (1 - failure rate), active users (MAU), txns per user, avg ticket, P2M share, fraud-flag rate, KYC completion.
  - SaaS/subscription: MRR, trial->paid, churn, ARPU, LTV, CAC payback, net revenue retention.
  - Food delivery: orders/day, AOV, delivery time, on-time %, cancellation %, rating, partner utilisation, promo cost per order.
  - Healthcare (hospital/diagnostics/telehealth - FICTIONAL): bed occupancy, average length of stay (ALOS), OPD footfall, no-show rate, readmission rate within 30 days, turnaround time (TAT) for lab reports, patient satisfaction (NPS), revenue per bed, claim rejection rate. Add privacy note (health data is sensitive).
  - HR: attrition %, regretted attrition, time-to-hire, offer-accept rate, cost per hire, headcount, absenteeism.
- Each KPI: write formula + one-line "why the business cares" + typical trap.
- FormulaCard: Rate metrics = events / eligible population (state denominator). 
## Worked examples (no SQL needed; 3 are small tables, 1 uses real numbers)
1. DesiCart: AOV = delivered revenue / delivered orders. Dec-24: 423 delivered of 458 orders, revenue Rs 2,059,545 -> AOV 4,868.90 -> show calc; note cancelled orders excluded.
2. UPI app 2024: txns 12,687, TPV Rs 1.70 crore, avg ticket 1,383 (facts) -> which are volume vs value KPIs; success rate 97.3%.
3. Telehealth app: signups 5,200, trials 3,308, paid 1,193 -> trial->paid 36.1%, signup->paid 22.9%.
4. Hospital (invented small table: 120 beds, 96 occupied avg, 410 discharges in month, 1,968 patient-days): occupancy = patient-days / (beds x days) ; ALOS = patient-days / discharges. Compute with 30 days: 1,968/(120x30)=54.67%; ALOS=4.80 days.
## Common mistakes
- Vanity metrics (downloads) as success | rate without stating denominator | averaging averages across segments | too many KPIs (>7) so nothing is owned | optimising one metric and hurting a guardrail (discounts raise orders, kill margin).
## Quiz: KPI vs metric; vanity metric; AOV formula trap (include cancelled); leading vs lagging; bed occupancy denominator.
## Interview Qs: What KPIs would you track for a UPI app? | Metric vs KPI? | Pick a North Star for a food-delivery app and a guardrail | KPIs for a hospital OPD | A KPI went up but business is worse - why?
## Takeaways 5. FurtherReading: alex-the-analyst, kaggle-learn.
## Practice (src/content/practice/business/kpis.json) - all language text, dataset none
| id | diff | ask | output |
| business-kpis-001 | easy | AOV: delivered orders 423, delivered revenue Rs 2,059,545 (Dec-24); AOV rounded 2dp | {value} 4868.90 | dividing by all 458 orders incl. cancelled (gives 4,496.8) |
| -002 | easy | classify 8 metrics as vanity/input/output/guardrail (md answer) | text |
| -003 | easy | conversion rate: 3,308 trials of 5,200 signups | {value} 63.6 |
| -004 | easy | success rate of UPI txns: 21,619 successful out of 22,300 (percent, 2dp) | {value} 96.95 | using failed count |
| -005 | medium | bed occupancy percent: 120 beds, 30 days, 1,968 patient-days (2dp) | {value} 54.67 | |
| -006 | medium | ALOS: 1,968 patient-days / 410 discharges (2dp) | {value} 4.80 | dividing by beds |
| -007 | medium | pick 5 KPIs + 1 guardrail for a diagnostics lab chain's report TAT goal (md) | text |
| -008 | medium | no-show rate: 1,250 booked, 1,075 attended -> 14.0% | {value} 14.0 |
| -009 | hard | revenue up 12% but profit down: list 4 metrics to check and explain (md) | text |
| -010 | hard | annual attrition percent: 544 exits over 2 years, avg headcount 2,400 (2dp) | {value} 11.33 | forgetting to annualise (gives 22.67) |
Mistake col for each: wrong denominator / mixing counts.
