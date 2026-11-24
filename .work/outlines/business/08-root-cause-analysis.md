# 08-root-cause-analysis  (topic: rca; 12 practice: 5 sql ecommerce+fintech, 7 text) KEY LESSON
fm: title "Root cause analysis: why did sales drop 15%?"; description "A step-by-step framework to find why a number moved, without guessing."; order 8; estimatedMinutes 65; objectives: apply a 6-step RCA framework; separate data problems from real change; decompose by time, segment and metric tree; test hypotheses with data; write the conclusion with next steps; tags: business, rca, root-cause, interview, sql
## Concept
- Framework (name it "CLEAR-D"? simpler: 6 steps): 1 Clarify (which metric, how defined, which period, how big, compared to what: WoW, MoM, YoY); 2 Validate data (pipeline, duplicates, tracking bug, late data, outliers); 3 Context (seasonality, festivals, holidays, price/promo, launches, outages, competitors); 4 Decompose (metric tree: orders x AOV; then by channel, category, city, platform, new vs repeat); 5 Hypotheses -> test each with one data cut, rank by size of explained gap; 6 Conclude + act (cause, size, confidence, next step, monitor).
- Internal vs external factors; "one number, many causes"; use "contribution to change" = segment change / total change.
- Analogy: doctor: symptoms -> tests -> diagnosis.
- Interview answer template (60 seconds spoken).
- Healthcare/fintech variants: "UPI success rate fell 1pp"; "OPD footfall fell 12%".
- FormulaCard: contribution to change; percent change (MoM, YoY).
## Worked examples (full RCA of ecommerce Nov-24 -> Dec-24; real outputs)
1. Clarify + size: delivered revenue 2,591,559 -> 2,059,545 (-20.5%); orders 533 -> 458 (-14.1%). Which is "sales"? State both.
2. Data check: duplicates removed, 3 outlier orders excluded (>=100000).
3. Context + YoY: Dec-24 vs Dec-23 orders +5.5% (458 vs 434), revenue +7.9%; Nov-23->Dec-23 also fell (-2.7% orders); Nov-24 had Diwali tail (window to Nov 3). So mostly seasonal hangover.
4. Decompose: orders x AOV (-14.7% and -6.8% on delivered); every channel fell (Android 262->239, iOS 98->79, Website 109->86, Mobile Web 64->54), all categories down (Fashion 423->325 units ...), cancellations flat 27 vs 27, coupon use 110->77, buyers 448->392. Not one broken channel -> demand-wide.
5. Conclusion: seasonal comedown plus fewer coupons; YoY healthy; action: plan Dec offers, compare to last year's Dec rather than Nov.
## Common mistakes
- Jumping to causes before sizing | comparing against a festive month | skipping data validation | one-segment tunnel vision | confusing correlation with cause | no recommendation | quoting causes without numbers.
## Quiz: first step of RCA; MoM vs YoY; contribution to change; data bug vs real drop; what to do when all segments fall.
## Interview Qs: Sales dropped 15% - how do you investigate? | UPI success rate fell from 97.5 to 96.5 | active users dropped on one day | OPD footfall fell 12% | how decide which hypothesis first.
## Takeaways 5. FurtherReading: mode-sql, alex-the-analyst.
## Practice (rca.json)
| business-rca-001 | easy | sql | ecommerce: delivered revenue (0dp) and delivered orders per month for 2024-11 and 2024-12 (DISTINCT, total_amount<100000) cols month, revenue, delivered_orders | 2591559/496; 2059545/423 | | outliers/dupes |
| -002 | medium | sql | ecommerce: orders by sales_channel for Nov-24 and Dec-24 side by side; cols sales_channel, nov_orders, dec_orders, change_pct (1dp) order by change_pct | Mobile Web 64/54 -15.6; Website 109/86 -21.1; iOS 98/79 -19.4; Android 262/239 -8.8 (all statuses; verify) | CASE sums | |
| -003 | medium | sql | ecommerce Dec-24 vs Dec-23: orders and delivered revenue; cols year, orders, revenue | 2023: 434 / 1,9xx,xxx ; 2024: 458 / 2,059,545 (fill) | strftime | comparing to Nov |
| -004 | hard | sql | ecommerce: category-level units sold Nov-24 vs Dec-24 using LOWER(TRIM(category)), cols category, nov_units, dec_units, change_pct (1dp), order by change_pct asc (7 clean categories) | Books -35..., (fill) | join order_items+products | dirty category labels split |
| -005 | hard | sql | fintech: NammaPay txns on 2023-09-21 by hour (DISTINCT); cols hour (integer), txns, failure_pct (1dp); only hours with at least 1 txn; order by hour | outage 18-21h high (fill) | strftime | not restricting app |
| -006 | easy | text | Order of RCA: put 6 steps in order (md/number list) | text | |
| -007 | easy | text | Revenue Nov 2,591,559, Dec 2,059,545: percent change 1dp | {value} -20.5 | dividing by Dec |
| -008 | medium | text | Dec-24 vs Dec-23 orders 458 vs 434: YoY % 1dp | {value} 5.5 | |
| -009 | medium | text | Revenue fell by Rs 532,014; Android accounted for Rs 150,000 of the fall: contribution percent (1dp) | {value} 28.2 | |
| -010 | medium | text | Daily active users halved only on iOS from one date. Top 3 checks (md) | text | |
| -011 | hard | text | "Sales dropped 15%": write a 6-sentence interview answer using the framework (md) | text | |
| -012 | hard | text | UPI success rate fell 97.5% to 96.5% overnight; list hypotheses in priority order, each with the data cut (md) | text | |
