# 12-t-tests  (topic: ttest)
fm: title "t-tests: comparing means"; description "One-sample, two-sample (Welch) and paired t-tests with numpy and pandas."; order 12; estimatedMinutes 55; objectives: choose the right t-test; compute t statistic for two groups (Welch); read df and approximate p; run it in pandas; tags: statistics, t-test
## Concept
- Analogy: are Rain-day deliveries slower, or did we just draw unlucky orders?
- t used when sigma unknown and n small; heavier tails than normal; approaches z as n grows (n>~100 use normal p). IMPORTANT: no scipy in harness/browser -> compute t statistic and Welch df; for p use normal approximation when df>100 (state clearly), else compare to a printed critical-value table (df 10:2.23, 20:2.09, 30:2.04, 60:2.00, inf:1.96).
- Types: one-sample, independent two-sample (Welch: do not assume equal variance), paired (before/after, same rows -> difference column).
- Welch t = (x1-x2)/sqrt(s1^2/n1+s2^2/n2). Assumptions: independence, roughly normal or big n, no extreme outliers.
- Effect size: mean difference and Cohen's d idea.
- FormulaCard: Welch t; FormulaCard: paired t.
## Worked examples
1. food_delivery: Rain vs Clear actual_minutes (delivered): diff ~5.4 min, t big. (script-check)
2. hr.performance_reviews: self_rating vs manager_rating paired (same review row) -> mean diff and t.
3. Small sample: 12 Heavy Rain vs 12 Clear orders (random_state) with critical table.
4. Reporting: "Rain adds 5.4 min (95% CI ...), p<0.001".
## Common mistakes
- Using independent test on paired data. | assuming equal variance blindly. | many pairwise t-tests (multiple comparisons). | ignoring effect size. | treating p as probability effect is real.
## Quiz: which test for before/after; Welch purpose; df meaning; t large means; assumption.
## Interview Qs: when t vs z | paired vs independent | assumptions | what if non-normal (Mann-Whitney mention).
## Takeaways 5. FurtherReading: khan-stats, numpy-docs
## Practice (ttest.json) 10 q
| statistics-ttest-001 | easy | python | food_delivery | difference in mean actual_minutes Rain minus Clear (2dp) | value | | sign |
| -002 | medium | python | food_delivery | Welch t statistic Rain vs Clear (2dp) | value | formula | pooled var |
| -003 | medium | python | food_delivery | Welch t Heavy Rain vs Clear | value | | |
| -004 | medium | python | hr | paired t statistic self_rating - manager_rating (2dp) | value | diff.mean/(diff.std/sqrt n) | independent test |
| -005 | medium | python | hr | mean paired difference self - manager and its SE: dict | dict | | |
| -006 | hard | python | food_delivery | Welch df (Satterthwaite) Rain vs Clear 1dp | value | | |
| -007 | hard | python | food_delivery | two-sided p (normal approximation, df large) for Welch t Heavy Rain vs Clear, state 6dp. Use erfc | value | | |
| -008 | easy | text | none | means 50, 46; SEs combined sqrt(4)=2: t | {value} 2 | | |
| -009 | medium | text | none | which test: same 10 riders before/after training: answer 'paired' md | text | | |
| -010 | hard | text | none | x1=52 s1=10 n1=50, x2=48 s2=12 n2=50 Welch t 2dp | {value} 1.77 (script) | | |
## MCQ bank (statistics-4.json, 8)
- paired | same users before/after | paired | independent
- welch | unequal variances | Welch | pooled
- t vs z | large n | z about t | t invalid
- df | bigger df | t closer normal | wider
- diff | CI of difference includes 0 | not significant | significant
- assumption | independence | observations independent | normal always
- onesample | compare mean to target | one-sample | two-sample
- multiple | 10 t-tests | inflates error | fine
