# 11-hypothesis-testing-p-values  (topic: hypothesis)
fm: title "Hypothesis testing and p-values"; description "A step-by-step way to decide if a difference is real or just luck."; order 11; estimatedMinutes 50; objectives: write H0 and H1; compute a z test for one proportion/mean; interpret p-value correctly; use alpha and one vs two tails; tags: statistics, hypothesis-testing, p-value
## Concept
- Analogy: court trial; innocent (H0) until evidence beyond doubt.
- Steps: state H0/H1, pick alpha (0.05), compute test statistic, p-value, decide, write business conclusion.
- p-value = probability of results at least this extreme if H0 were true. NOT P(H0 true), NOT effect size.
- z statistic for one mean z=(xbar-mu0)/(s/sqrt n); two-sided p = erfc(|z|/sqrt2) (math module, no scipy).
- One vs two-tailed; "fail to reject" not "accept H0". Statistical vs practical significance (huge n makes tiny differences significant).
- FormulaCard: test statistic; FormulaCard: p from z via erfc.
## Worked examples
1. "Promised 40 min average, is actual 44.87?" one-sample z on delivered orders: z huge, p ~ 0.
2. Small n: sample 30 deliveries to show p not tiny (random_state). (script-check)
3. One proportion: late rate vs 20% target.
4. Practical vs statistical: tiny difference with big n.
## Common mistakes
- "p=0.03 means 3% chance H0 true". | "p>0.05 proves no effect". | p-hacking, many looks. | one-tailed after seeing direction. | ignoring effect size.
## Quiz: H0 example; p meaning; decision at p=0.04; fail to reject; practical significance.
## Interview Qs: explain p-value to a manager | H0 vs H1 | what alpha means | p<0.05 but tiny effect?
## Takeaways 5. FurtherReading: khan-stats
## Practice (hypothesis.json) 10 q
| statistics-hypothesis-001 | easy | python | food_delivery | one-sample z statistic: H0 mean actual_minutes=40 (delivered), 2dp | value | (m-40)/(s/sqrt n) | |
| -002 | medium | python | food_delivery | Two-sided p-value for H0 mean actual_minutes = 44.8 (delivered), via math.erfc on the z; 4dp | value | z then erfc | halving the p |
| -003 | medium | python | food_delivery | late rate (delay>10) vs 20% target: z for one proportion using p0 in SE (3dp) | value | | SE with p-hat |
| -004 | medium | python | food_delivery | sample 30 delivered rows (random_state=3): z vs mu0=40 using sample SD 3dp | value | | |
| -005 | hard | python | food_delivery | Heavy Rain mean vs 44.87 overall: z and two-sided p dict 4dp | dict | | |
| -006 | hard | python | hr | goals_met_pct H0 mean 70: z and p dict | dict | | |
| -007 | easy | text | none | z=2.5: reject at alpha 0.05 two-sided? answer 1 yes 0 no | {value} 1 | | |
| -008 | medium | text | none | p=0.07 alpha 0.05 conclusion md | text | | |
| -009 | medium | text | none | z=1.96 two-sided p approx | {value} 0.05 | | |
| -010 | hard | text | none | xbar 52 mu0 50 s 10 n 100 z | {value} 2 | | s/n |
## MCQ bank (statistics-4.json, 8)
- h0 | null says | no effect | effect
- p | small p means | data unlikely under H0 | H0 unlikely
- decision | p=0.2 | fail to reject | accept H0
- alpha | alpha is | accepted false-alarm rate | prob of H1
- tails | direction unknown | two-tailed | one
- practical | huge n tiny diff | significant but maybe unimportant | important
- hack | test 20 metrics | inflate false positives | more power
- reject | reject H0 proves | strong evidence not proof | certainty
