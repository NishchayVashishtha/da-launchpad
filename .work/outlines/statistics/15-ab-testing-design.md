# 15-ab-testing-design  (topic: abdesign)  [A/B part 1 of 2]
fm: title "A/B testing, part 1: design and sample size"; description "Plan an experiment before you run it: hypothesis, metrics, randomisation and sample size."; order 15; estimatedMinutes 55; objectives: write an A/B hypothesis and pick primary, guardrail metrics; explain randomisation and unit of analysis; estimate sample size per arm; plan test duration; tags: statistics, ab-testing, experiment-design, sample-size
## Concept
- Story (fictional): a shopping app tests a "free shipping banner" at checkout. Why experiments: only way to show cause.
- Steps checklist: problem -> hypothesis -> primary metric (conversion), guardrails (AOV, refund rate), unit (user not session), randomisation, MDE (minimum detectable effect), alpha 0.05, power 80%, sample size, duration (full weeks, cover weekday/weekend, avoid festive skews), decision rule written BEFORE.
- Sample size per arm (two proportions) n ~ 2*(z_a/2 + z_b)^2 * p(1-p)/delta^2 with z 1.96+0.84 => n ~ 15.7*p(1-p)/delta^2 (use p = avg of baseline & target, simplified rule). Intuition: halve the MDE -> 4x sample; low baseline -> need more.
- Pitfalls at design time: sample ratio mismatch (SRM), contamination (user in both arms), novelty effect, network effects, peeking, too many metrics, seasonal clash.
- Baseline from data: subscription trial->paid rate; marketing ab baseline 10.6%.
- FormulaCard: sample size per arm (rule of thumb); FormulaCard: SRM check chi-square on counts.
## Worked examples
1. Baseline from marketing ab_test_results (cleaned): control conv 10.57%; MDE +1.5pp -> ~7,006 users per arm (script: 15.7*pbar*(1-pbar)/delta^2). Note the real test had ~6,000 per arm, so was slightly underpowered for 1.5pp; honest teaching moment.
2. subscription: trial-to-paid baseline = 36.06% (1193 of 3308 subscription rows have paid_start_date; all have trial_start_date; no duplicate ids). n for +3pp via formula (script-check).
3. Duration: daily traffic 700 users/day both arms -> days needed.
4. SRM check: control 6016 vs treatment 5974 -> chi2 vs 50/50 (script-check); ok.
## Common mistakes
- No pre-set sample size -> peek and stop. | randomising by session not user. | choosing many primary metrics. | running 2 days over Diwali. | forgetting to remove contaminated/duplicate users before analysis.
## Quiz: guardrail metric; MDE meaning; effect of halving MDE on n; SRM; unit of randomisation.
## Interview Qs: how design an A/B test for a new checkout | how choose sample size | what is SRM | what metrics primary vs guardrail | when A/B not possible.
## Takeaways 5. FurtherReading: khan-stats
## Practice (abdesign.json) 10 q
| statistics-abdesign-001 | easy | python | marketing | cleaned (dedupe, drop users with both variants) row count per variant dict {control,treatment} | dict | | skipping contamination |
| -002 | easy | python | marketing | number of contaminated users (appear in both variants; after dedupe) | value | | |
| -003 | medium | python | marketing | baseline conversion % of control cleaned 2dp | value | | |
| -004 | medium | python | marketing | SRM chi-square for variant counts vs 50/50 cleaned 3dp | value | | |
| -005 | medium | python | subscription | Trial->paid rate % among subscriptions with trial_start_date: share with paid_start_date not null, 2dp (expected 36.06) | value | notna mean | dividing by users table count |
| -006 | hard | python | marketing | Planning: using cleaned control baseline p1 and MDE delta=0.015, n per arm = ceil(15.7*pbar*(1-pbar)/delta^2) with pbar=p1+delta/2 (expected ~7006; script-verified) | value int | formula | using p1 not pbar; per-arm vs total |
| -007 | medium | text | none | baseline 10%, MDE 2pp, pbar=0.11: n per arm = 15.7*0.11*0.89/0.02^2, round up | {value} 3843 (script-compute) | formula | using 0.1 |
| -008 | medium | text | none | MDE halved: n multiplier | {value} 4 | | |
| -009 | medium | text | none | need 20000 users per arm, 1,600 eligible users/day total: days (ceil) | {value} 25 | | per arm vs total |
| -010 | hard | text | none | choose primary vs guardrail for a UPI cashback test (md, no value) | text | | |
## MCQ bank (statistics-5.json, 8)
- hypothesis | good H1 | specific & measurable | vague
- guardrail | metric to ensure no harm | guardrail | primary
- unit | randomise by | user | session
- mde | MDE | smallest lift worth detecting | observed lift
- n | MDE halves | 4x n | 2x
- srm | counts 6000 vs 5000 | SRM red flag | normal
- duration | include | full weeks | 1 day
- novelty | effect fades | novelty | seasonality
