# 13-chi-square-proportions  (topic: chisquare)
fm: title "Chi-square test and comparing proportions"; description "Test whether two categories are linked, and compare conversion rates."; order 13; estimatedMinutes 50; objectives: build a contingency table; compute expected counts and chi-square; use df and critical values; run a two-proportion z-test; tags: statistics, chi-square, proportions
## Concept
- Analogy: Are Android and iOS users equally likely to buy, or is the gap just noise?
- Contingency table; expected = row total * col total / grand total; chi2 = sum (O-E)^2/E; df=(r-1)(c-1). Critical values at 0.05: df1 3.84, df2 5.99, df3 7.81, df4 9.49. For df=1 p=erfc(sqrt(chi2/2)).
- 2x2 chi2 equals square of two-proportion z. Pooled SE formula.
- Assumption: expected counts >=5; independent observations. Association not cause; chi-square tells "linked?" not "how strong" (mention Cramer's V name only).
- FormulaCard: chi-square; FormulaCard: two-proportion z.
## Worked examples
1. subscription: platform (iOS/Android; clean case via str.title? platform in users is clean; events has casing issue) vs trial->paid: build users x subscriptions; chi2. Check first with sqlite: join subscriptions to users, paid = paid_start_date not null.
2. marketing ab (cleaned): converted x variant 2x2 chi2 and p; equals z^2.
3. Python manual expected counts with numpy.
4. Heavy Rain vs Clear cancellation 2x2 (delivery_status).
## Common mistakes
- Running chi-square on percentages not counts. | tiny expected counts. | treating chi-square as causation. | not cleaning duplicates/contaminated users first. | wrong df.
## Quiz: expected count formula; df for 3x4; large chi2 means; when not to use; 2x2 -> z relation.
## Interview Qs: when to use chi-square | explain expected counts | chi-square vs t-test | two-proportion test for A/B.
## Takeaways 5. FurtherReading: khan-stats
## Practice (chisquare.json) 10 q
| statistics-chisquare-001 | easy | python | food_delivery | cancellation rate % in Heavy Rain vs Clear dict {heavy_rain,clear} 2dp | dict | | |
| -002 | medium | python | food_delivery | 2x2 counts weather in (Clear,Heavy Rain) x cancelled: dict of 4 counts | dict | | |
| -003 | medium | python | food_delivery | chi-square statistic for that 2x2 (numpy only) 2dp | value | | Yates not required |
| -004 | medium | python | food_delivery | p-value df=1 via erfc 6dp | value | | |
| -005 | medium | python | marketing | clean ab (drop dups, drop users in both variants): conversion counts per variant dict | dict | | |
| -006 | hard | python | marketing | two-proportion z (pooled) treatment vs control 3dp | value | | unpooled |
| -007 | hard | python | marketing | chi-square 2x2 on same data 3dp, return also z^2 equal: dict {chi2, z_squared} | dict | | |
| -008 | easy | text | none | O=30 E=20 contribution (O-E)^2/E | {value} 5 | | |
| -009 | medium | text | none | 3 rows x 4 cols df | {value} 6 | | |
| -010 | medium | text | none | row total 200 col total 150 grand 1000 expected | {value} 30 | | |
## MCQ bank (statistics-4.json, 8)
- use | two categorical vars | chi-square | t-test
- df | 2x2 | 1 | 4
- expected | formula | row*col/total | O
- big | large chi2 | evidence of association | no link
- counts | input should be | counts | percentages
- critical | df1 5% | 3.84 | 1.96
- small | expected <5 | unreliable | fine
- cause | chi-square shows | association | cause
