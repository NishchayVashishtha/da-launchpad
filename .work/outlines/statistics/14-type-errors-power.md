# 14-type-errors-power  (topic: errors)
fm: title "Type I and Type II errors, power and multiple testing"; description "The two ways a test can be wrong, and how sample size and many tests change the risk."; order 14; estimatedMinutes 45; objectives: define Type I/II; link alpha, beta, power; see what drives power; explain multiple-comparison inflation and Bonferroni; tags: statistics, type-1-error, power
## Concept
- Analogy: fire alarm: false alarm (Type I) vs missed fire (Type II).
- Table 2x2: truth x decision. alpha=P(Type I); beta=P(Type II); power=1-beta.
- Power rises with larger n, bigger effect, larger alpha, lower variance. Typical target 80%.
- Costs differ: fraud model (miss is costly -> accept more false alarms) vs launching a risky feature.
- Multiple testing: 20 metrics at 0.05 -> P(at least one false positive)=1-0.95^20=64.2%; Bonferroni alpha/m; mention FDR name.
- Peeking/stopping early inflates Type I.
- FormulaCard: family-wise error; Bonferroni.
## Worked examples
1. Table with numbers: 1000 A/A tests at alpha 0.05 -> ~50 false positives; simulate with numpy (rng 11).
2. 20 segments in marketing ab (device x tier etc.) -> expected false hits.
3. Power by simulation: effect +1.5pp, n=3000/arm -> approx power (script computed; script-check).
4. Bonferroni threshold for 5 tests.
## Common mistakes
- Believing alpha 0.05 means 5% of significant results are wrong. | not planning power -> inconclusive tests. | slicing many segments and reporting the lucky one. | stopping when p dips below .05. | treating non-significant as "no effect".
## Quiz: define Type I; power=1-beta; what increases power; family error calc; which error is missing a real lift.
## Interview Qs: Type I vs II with example | what is power | how to handle multiple metrics | peeking problem.
## Takeaways 5. FurtherReading: khan-stats
## Practice (errors.json) 10 q
| statistics-errors-001 | easy | python | none | family-wise error for 20 tests at 0.05 (4dp) | value | 1-0.95**20 | 0.05*20 |
| -002 | easy | python | none | Bonferroni alpha for 8 tests | value | | |
| -003 | medium | python | none | A/A simulation: rng=np.random.default_rng(11), 2000 experiments, each 2 groups n=200 Bernoulli p=0.1, two-proportion |z|>1.96 count rate (%) 1dp | value | | |
| -004 | medium | python | marketing | Segment hunt: for each device_type x city_tier in cleaned ab test compute z of treatment-control; count |z|>1.96 -> dict {segments, significant} | dict | | |
| -005 | hard | python | none | power by simulation: p0=0.095, p1=0.11, n=6000/arm, 2000 sims rng 5, two-sided z at 1.96; power % 0dp | value | | |
| -006 | hard | python | marketing | Cleaned ab test: for the 4 device_type x city_tier cells... (use all device_type x city_tier cells), apply Bonferroni: count cells where two-sided p of treatment-control proportion z < 0.05/number_of_cells; dict {cells, significant_bonferroni} | dict | z per cell, erfc | comparing to 0.05 |
| -007 | easy | text | none | prob of at least one false positive for 5 tests at 0.05 3dp | {value} 0.226 | | |
| -008 | medium | text | none | Alpha 5%, 1 test: expected false positives in 200 independent null tests | {value} 10 | | |
| -009 | medium | text | none | beta=0.2 -> power | {value} 0.8 | | |
| -010 | hard | text | none | Which error: shipping a feature that does nothing? answer 'Type I' md | text | | |
## MCQ bank (statistics-5.json, 8)
- t1 | false positive | Type I | Type II
- t2 | miss real effect | Type II | Type I
- power | 1-beta | power | alpha
- alpha | alpha is | P(reject H0 | H0 true) | P(H0)
- n | more n | more power | less
- multiple | many tests | more false positives | none
- bonf | 4 tests alpha .05 | .0125 | .2
- peek | stopping on first p<.05 | inflates false positives | fine
