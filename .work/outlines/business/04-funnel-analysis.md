# 04-funnel-analysis  (topic: funnel; 10 practice: 6 sql subscription, 4 text)
fm: title "Funnel analysis: where do users drop off?"; description "Count users at each step, find the leakiest step and size the fix."; order 4; estimatedMinutes 50; objectives: define funnel steps and the unit (user vs session); compute step and overall conversion; segment a funnel (platform, source); size an improvement; tags: business, funnel, conversion, sql, subscription
## Concept
- Funnel = ordered steps users must pass. Step conversion = users at step n / users at step n-1; overall = last / first. Analogy: a water pipe with leaks; fix the biggest leak that is fixable.
- Rules: count DISTINCT users, keep time order, same cohort window, define each step by an event. Drop-off % vs conversion %. Strict vs loose funnels.
- Segmenting: platform, source, device, city tier. Simpson's-paradox warning (mix shift).
- Sizing: "if trial->paid rose 36.1% -> 40%, extra paid users = 3,308 x 0.039 = 129".
- Fintech funnel (explain only): app open -> enter amount -> authenticate -> success; healthcare: search doctor -> view slots -> book -> attend.
- FormulaCard: step conversion; overall conversion.
## Worked examples (subscription; LOWER(event_name); paste real outputs)
1. Distinct users per event: signup 5,200 -> trial_start 3,308 -> payment_success 1,193 -> renewal_success 766. Step rates 63.6%, 36.1%, 64.2%. Overall 22.9% signup->paid.
2. Funnel by platform using users + subscriptions: trial->paid Android 31.0%, Web 39.6%, iOS 45.9% (signups 3,209/863/1,128). Note: telehealth app framing = "wellness app".
3. By acquisition_source trial->paid: Influencer 16.0% vs Referral 47.1%.
4. Sizing: if Android reached the iOS rate 45.9%, extra payers = 1,973 x (0.459-0.310)=~294 (script-check).
## Common mistakes
- Counting events not users | not lower-casing event_name (splits 'signup'/'SIGNUP', undercounts by 99%) | denominator = all signups at every step | comparing funnels of different periods | ignoring users who skip a step | percent drop vs percentage points.
## Quiz: step vs overall conversion; distinct count; drop-off %; biggest leak; platform mix shift.
## Interview Qs: signup->purchase conversion fell; how do you find the cause? | design a funnel for a UPI first payment | how to measure a funnel with time windows | conversion by source vs by user quality | funnel for hospital appointment booking.
## Takeaways 5. FurtherReading: mode-sql, sqlite-docs.
## Practice (funnel.json) dataset subscription (dedupe: users/subscriptions DISTINCT; events: LOWER(event_name))
| business-funnel-001 | easy | sql | Count distinct users who signed up (event signup). col signups | 5200 | COUNT(DISTINCT user_id) WHERE LOWER(event_name)='signup' | case-sensitive match returns 58? (only uppercase rows) |
| -002 | easy | sql | Distinct users per funnel event: signup, trial_start, payment_success, renewal_success; cols event_name, users; ordered by users desc | 5200/3308/1193/766 | filter IN, LOWER | no DISTINCT counts events (e.g. 5,179 signups lowercase +58) |
| -003 | medium | sql | Trial-to-paid % (2dp) = subscriptions with paid_start_date / all subscriptions. col trial_to_paid_pct | 36.06 | AVG(paid_start_date IS NOT NULL)*100 on DISTINCT subs | dividing by users |
| -004 | medium | sql | Trial-to-paid by platform: cols platform, trials, paid, conversion_pct (1dp), best first | iOS 833/382/45.9; Web 502/199/39.6; Android 1973/612/31.0 | JOIN users, GROUP BY | duplicate users inflate counts |
| -005 | medium | sql | Trial-to-paid by acquisition_source, 1dp, lowest first; cols acquisition_source, trials, paid, conversion_pct | Influencer 16.0 first ... Referral 47.1 | | |
| -006 | hard | sql | One row funnel: signups (users table), trials, paid, with step rates trial_rate_pct, paid_of_trial_pct, overall_pct (1dp). | 5200, 3308, 1193, 63.6, 36.1, 22.9 | subqueries/CTE | using events table counts mixing case |
| -007 | easy | text | Step conversion: 3,308 trials -> 1,193 paid; percent 1dp | {value} 36.1 | |
| -008 | medium | text | Sizing: if Android trial->paid (1,973 trials) rose from 31.0% to iOS 45.9%, extra payers (round) - use exact rates 612/1973 and 382/833 | {value} (script-compute) | rounding rates early |
| -009 | medium | text | Funnel signup 1,000 -> view slot 700 -> book 280 -> attend 238 (clinic). overall % and the leakiest step (value: overall %) | {value} 23.8 | |
| -010 | hard | text | Mix shift: platform A converts 40%, B 20%; overall rate fell although each platform's rate rose - explain with an example (md) | text | |
