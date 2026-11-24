# 04-outliers-iqr  (topic: outliers)
fm: title "Outliers: spotting them with IQR and z-scores"; description "Find unusual values and decide what to do with them."; order 4; estimatedMinutes 40; objectives: compute quartiles and IQR; apply the 1.5xIQR fence; compare with z-score rule; decide remove/cap/keep with business reasoning; tags: statistics, outliers, iqr
## Concept
- Analogy: one billionaire walks into a tea stall; the average customer wealth jumps, nothing real changed.
- Quartiles Q1,Q3; IQR=Q3-Q1; fences Q1-1.5*IQR, Q3+1.5*IQR. Box plot reading. Z rule |z|>3 fails when outliers inflate SD; IQR is robust.
- Types: data error (typo, 100x spend), genuine extreme (festive spike), different population. Decision tree: error -> fix/remove; genuine -> keep, report with and without; never delete just because inconvenient.
- Options: remove, cap (winsorise), transform, use median.
- Pandas quantile method note (linear interpolation) so answers match: `quantile(0.25)`.
- FormulaCard: IQR fences.
## Worked examples
1. marketing.ad_spend: spend_inr is TEXT in CSV (some with ₹) -> clean with to_numeric(str.replace(r'[₹,\s]','',regex=True)); 3 rows 100x; IQR fence flags them. (script-check count)
2. food_delivery.deliveries delay_minutes: IQR vs z outliers counts; compare.
3. Effect on mean: mean with and without the flagged rows.
4. SQLite: finding rows above a fixed threshold via subquery (no percentile function; mention).
## Common mistakes
- Deleting every outlier automatically. | using z-rule on tiny/skewed samples. | computing IQR before cleaning text numbers. | forgetting Festive spikes are real. | applying fence to categorical codes.
## Quiz: IQR calc; upper fence calc; which stat robust (median); z rule limitation; correct action for a data-entry 100x.
## Interview Qs: how do you find outliers | what to do with them | IQR vs z | example when you would keep an outlier.
## Takeaways 5. FurtherReading: pandas-docs, khan-stats
## Practice (outliers.json) 10 q
| statistics-outliers-001 | easy | python | food_delivery | Q1 and Q3 of delay_minutes as dict {q1,q3} | dict | quantile | |
| -002 | easy | python | food_delivery | IQR of actual_minutes (2dp) | value | q3-q1 | |
| -003 | medium | python | food_delivery | count of IQR outliers (either side) in actual_minutes | value int | fences | using 1 not 1.5 |
| -004 | medium | python | marketing (ad_spend) | clean spend_inr text to number (ad_spend has duplicates: drop_duplicates first); count IQR outliers on the cleaned column | value int | clean+fence | not dropping dups; text compare |
| -005 | medium | python | marketing | max cleaned spend_inr row's campaign_id and spend: dict | dict | | |
| -006 | hard | python | marketing | mean of cleaned spend_inr (deduped) with and without IQR outliers: dict {with,without} 2dp | dict | | |
| -007 | medium | python | food_delivery | delay_minutes: count flagged by |z|>3 vs IQR: dict {z_rule,iqr_rule} | dict | | |
| -008 | easy | text | none | data 3,5,6,7,8,9,10,40: Q1,Q3 not needed? give IQR using median-of-halves (Q1=5.5,Q3=9.5) | {value} 4 | | |
| -009 | medium | text | none | same data upper fence | {value} 15.5 | Q3+1.5*IQR | |
| -010 | hard | text | none | which value in daily sales 12,14,15,15,16,18,95 (lakh) is outlier? answer 95 -> give value of upper fence with Q1=14,Q3=18 | {value} 24 | | |
## MCQ bank (statistics-1.json, 8)
- IQR | Q1=20 Q3=35 | 15 | 55
- fence | upper fence Q3=35 IQR=15 | 57.5 | 50
- robust | which statistic ignores outliers | median | mean
- z rule | why z fails with extreme outlier | inflates SD | too sensitive
- error vs real | 100x typo in spend | check and correct | always keep
- winsorise | capping meaning | replace with cutoff | delete
- box plot | whiskers extend to | fence limit within data | min and max always
- festive | Diwali spike flagged | investigate; likely genuine | delete
