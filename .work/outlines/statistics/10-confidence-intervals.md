# 10-confidence-intervals  (topic: ci)
fm: title "Confidence intervals"; description "Give a range, not a single guess, and say what 95% really means."; order 10; estimatedMinutes 45; objectives: build CI for a mean and for a proportion; interpret 95% correctly; see how n and SD change width; report CI in business language; tags: statistics, confidence-interval
## Concept
- Analogy: "I'll reach between 7:50 and 8:10" vs "8:00 exactly".
- CI = estimate +/- critical * SE. z=1.96 for 95% (use for large n; mention t for small n, next lessons). For proportion: p +/- 1.96*sqrt(p(1-p)/n).
- Correct reading: if we repeated the study many times, 95% of such intervals would cover the true value. NOT "95% chance true value is inside this one" (explain softly).
- Width shrinks with sqrt(n), grows with SD and confidence level. Margin of error. Overlap of CIs caution.
- Business wording: "conversion between 9.8% and 11.5%".
- FormulaCard: CI mean; CI proportion.
## Worked examples
1. food_delivery mean actual_minutes: 44.87 +/- 0.21 (script-check).
2. marketing ab: control conversion CI (cleaned).
3. Python sample n=100 vs n=1000 CI width comparison.
4. Margin of error planning: n for +/-2pp at p=0.5 -> 2401.
## Common mistakes
- "95% probability this interval has mu". | using z for tiny n. | forgetting to clean dups before computing p-hat. | CI of data (percentiles) vs CI of mean. | reporting without units.
## Quiz: 95% interpretation; width vs n; z value; compute margin; CI of proportion.
## Interview Qs: explain CI to a PM | what changes width | difference CI vs prediction interval (brief) | overlap of two CIs implies?
## Takeaways 5. FurtherReading: khan-stats
## Practice (ci.json) 10 q
| statistics-ci-001 | easy | python | food_delivery | 95% CI lower bound for mean actual_minutes (z=1.96, 2dp) | value | | |
| -002 | easy | python | food_delivery | upper bound | value | | |
| -003 | medium | python | food_delivery | 95% CI for mean actual_minutes in Heavy Rain: dict {lower,upper} 2dp | dict | | n small ok |
| -004 | medium | python | marketing | cleaned ab test: control conversion rate and 95% CI as dict {p,lower,upper} 4dp | dict | | not cleaning |
| -005 | medium | python | marketing | treatment same | dict | | |
| -006 | hard | python | marketing | do control and treatment 95% CIs overlap? return dict with bounds & overlap boolean(as 1/0) | dict | | |
| -007 | easy | text | none | mean 50 SE 2: 95% margin | {value} 3.92 | 1.96*2 | |
| -008 | medium | text | none | n=400, p-hat 0.1: margin of error 4dp | {value} 0.0294 | | |
| -009 | medium | text | none | n for +/-3pp at p=0.5 (95%), round up | {value} 1068 | script | |
| -010 | hard | text | none | CI width at n=100 is 8; width at n=400 | {value} 4 | sqrt | 2 |
## MCQ bank (statistics-3.json, 8)
- meaning | 95% CI | method covers truth 95% of repeats | 95% chance this interval holds
- width n | more data | narrower | wider
- level | 99% vs 95% | wider | narrower
- crit | z for 95% | 1.96 | 1.64
- margin | z*SE | margin of error | SE
- sd | bigger SD | wider | narrower
- zero | CI for difference includes 0 | no clear difference | proven
- units | CI in | same units as estimate | percent always
