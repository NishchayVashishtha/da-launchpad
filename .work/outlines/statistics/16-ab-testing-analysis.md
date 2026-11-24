# 16-ab-testing-analysis  (topic: abanalysis)  [A/B part 2 of 2]
fm: title "A/B testing, part 2: analysis, interpretation and pitfalls"; description "Clean the data, test the lift, read the confidence interval and write the recommendation."; order 16; estimatedMinutes 60; objectives: clean a raw experiment table; run two-proportion z-test and CI for lift; check revenue per user and segments; write a ship/no-ship recommendation; tags: statistics, ab-testing, analysis
## Concept
- Pipeline: validate (dupes, contamination, SRM) -> primary metric test -> CI on difference -> guardrails (AOV, revenue/user) -> segments (exploratory only) -> decision.
- Absolute vs relative lift (pp vs %). CI on difference: (p2-p1) +/- 1.96*sqrt(p1(1-p1)/n1+p2(1-p2)/n2).
- Revenue per user = conversion * AOV; treatment AOV lower -> revenue lift smaller than conversion lift. Revenue is skewed/zeros -> use Welch t (n large).
- Segment findings: Mobile lift, Desktop flat/negative -> heterogeneity, but multiple-comparison caution, interaction question.
- Pitfalls: peeking, Simpson's paradox, novelty, ignoring guardrails, "significant therefore ship".
- Write-up template: Summary, Setup, Result with CI, Guardrails, Risks, Recommendation, Next test.
- FormulaCard: CI for difference; relative lift.
## Worked examples (marketing.ab_test_results, test checkout_free_shipping_banner, 2024-09-02..09-29)
1. Cleaning: 12,030 rows -> drop exact dups -> remove 10 users in both arms -> 11,990 rows: control 6016 conv 10.57%, treatment 5974 conv 11.72%; diff +1.15pp; pooled z=1.99, two-sided p=0.046; 95% CI of diff [+0.02pp, +2.27pp] (script verified). Borderline result: teach caution.
2. Revenue per user and AOV (converters only) by variant.
3. Segments (script verified): Mobile 8.47% -> 10.81% (+2.3pp), Desktop 15.35% -> 13.91% (-1.4pp). Instructor note differs; use script output only. Teach: heterogeneity but exploratory, check interaction, multiple comparisons.
4. Write the stakeholder summary paragraph.
## Common mistakes
- Not cleaning contaminated users. | quoting p without CI/effect size. | declaring winner from a segment. | ignoring AOV drop. | relative vs absolute confusion (+10.9% relative = +1.15pp).
## Quiz: absolute vs relative lift; CI includes 0; guardrail drop; why segments exploratory; unit when revenue per user used.
## Interview Qs: walk through analysing an A/B test | results ambiguous what do you do | metric up but revenue flat | Simpson's paradox | how to explain p to PM | when to stop test.
## Takeaways 5. FurtherReading: khan-stats, pandas-docs
## Practice (abanalysis.json) 10 q (all use CLEAN helper from _plan)
| statistics-abanalysis-001 | easy | python | marketing | conversion rate % per variant dict 2dp cleaned | dict | | uncleaned |
| -002 | easy | python | marketing | absolute lift in pp (treatment-control) 2dp | value | | relative |
| -003 | medium | python | marketing | relative lift % 1dp | value | | |
| -004 | medium | python | marketing | pooled two-proportion z 3dp | value | | |
| -005 | medium | python | marketing | two-sided p-value via erfc 4dp | value | | |
| -006 | medium | python | marketing | 95% CI for difference dict {lower,upper} 4dp | dict | | pooled SE in CI |
| -007 | hard | python | marketing | revenue per user by variant (revenue_inr fill NaN->0) dict 2dp | dict | | converters only |
| -008 | hard | python | marketing | AOV among converters per variant dict 2dp (treatment lower) | dict | | |
| -009 | hard | python | marketing | per device_type: lift pp and z; DataFrame device_type,lift_pp,z sorted by device_type | DataFrame | | |
| -010 | hard | text | none | write recommendation (md) given lift +1.15pp CI [0.02,2.27], AOV -4%: ship/no? solution md with reasoning | text | | |
## MCQ bank (statistics-5.json, 8)
- lift | 10% to 11% | +1pp, +10% relative | +1%
- ci | diff CI [-0.5,2.0]pp | not significant | win
- guard | conversion up AOV down | check revenue/user | ship
- segment | winning only in mobile | exploratory | ship mobile
- clean | before test | remove dups/contaminated | skip
- p | p=0.03 means | unlikely under H0 | 97% sure
- decision | CI tiny positive but costly | practical significance | ship always
- simpson | overall vs group reversal | Simpson | noise
