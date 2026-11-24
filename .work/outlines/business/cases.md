# 25 written cases (src/content/cases/<id>.mdx; route /business/cases/<id>/; frontmatter: title, industry, difficulty, type, estimatedMinutes)
Read _facts.md first (every number below comes from it or was re-queried; writers re-run the SQL with sqlite3 and paste real output; if a number differs, trust the script and tell the orchestrator). All type: case-study.
Body H2s (every case, in order): ## Problem | ## Data you have | ## Approach | ## Step-by-step solution | ## Key insight | ## Recommendation | ## What a weak answer looks like. Solution steps carry a small SQL block + result table where data exists (SQLite; dedupe per _facts.md). Brands fictional; health cases use aggregate numbers only. Simple English.
Mix: fintech 10, health 7, consulting 8. Difficulty: easy 4 (F3,F5,H2,C7), medium 16, hard 5 (F4,F10,H3,C5,C8). Est. minutes 20-45.
Dataset framing notes: telehealth/wellness app = subscription db; diagnostics+telehealth company staff = hr db; home sample collection = food_delivery db; Vasudha retail = retail db.

## FINTECH (dataset fintech unless noted)
### F1 | upi-nammapay-outage-windows | "NammaPay failure rate is double its rivals" | Fintech | medium | 35 min
- Prompt: Head of payments asks why NammaPay's failure rate is high. Is the app broken all the time?
- Data: DISTINCT txns; failure by app: NammaPay 5.10% (3,922 txns) vs 1.85-2.25% others; failed_transactions codes UPI_SYSTEM_DOWN 118.
- Solution: 1 clarify failure def; 2 size by app; 3 cut NammaPay by date/hour -> find clusters; 4 compare inside windows (2023-03-14 10-12h, 2023-09-21 18-21h, 2024-02-06 9-11h, 2024-07-16 19-21h: 304 txns, 38.82% fail) vs outside (3,601 txns, 2.25%); 5 failure code check (UPI_SYSTEM_DOWN); 6 retry success for that code 61.0%.
- Insight: NammaPay is normal except four short outages; the average hides an incident problem, not a chronic one.
- Rec: SLA/monitoring alerts, graceful retry, don't penalise product team; report failure excluding incidents separately.
### F2 | kaveri-bank-peak-hour-failures | "One bank, bad evenings" | Fintech | medium | 35
- Prompt: Which bank causes most failures and when?
- Data: bank failure %: Kaveri Co-op 6.58 (1,703 txns) vs 2.4-3.1; Kaveri peak (9h,18h,19h) 9.98% (421) vs 4.77% (1,279); other banks 2.19% vs 2.49%; BANK_SERVER_TIMEOUT 42 failures all Kaveri.
- Solution: rate by bank (min volume) -> by hour for worst bank -> compare with peers -> failure code -> impact sizing (extra failures = 421 x (0.0998-0.0219) ~ 33 failures per the 2 years - state honest small number) -> recommendation.
- Insight: problem is capacity at peak, not the whole bank; but magnitude small in this extract: volume-weighted impact.
- Rec: shift routing / throttle at peak, escalate with bank; add auto-retry after 2 min for timeouts (74.1% retry success).
### F3 | salary-day-failures-myth | "Support says payments fail on salary day" | Fintech | easy | 20
- Prompt: Ops believes failures rise on 1st-3rd of the month. Check it.
- Data: day 1-3: 2,474 txns 2.63% fail; rest 19,826 2.70%; amounts > 50,000 only 10 txns (1 failed).
- Solution: restate hypothesis; define groups; compute; compare with sample-size caution; also check volume by day-of-month; conclude NOT supported; what else could explain tickets (perception, social media).
- Insight: test beliefs; no effect is a valid finding; volume may rise but rate doesn't.
- Rec: don't add capacity for failures; monitor daily; share data with support.
### F4 | night-fraud-flag-rule | "Should we auto-block night transactions?" | Fintech | hard | 45
- Prompt: Risk team proposes blocking all txns 23:00-04:59. Evaluate.
- Data: 302 flagged of 22,300 (1.35%); night 577 txns 29 flagged (5.03%) vs day 21,723 / 273 (1.26%); new accounts (<30 days) 960 txns 69 flagged (7.19%) vs 1.09%; Travel 5.55%, Electronics 4.89%; amount >= 5,000 1,154 txns 46 flagged (4.0%).
- Solution: define precision/recall; night rule precision 5.03%, recall 29/302 = 9.6% -> blocks 548 good txns to catch 29; compare alternative rules (new account, Travel/Electronics, amount) -> best combined rule (script: new account AND amount>=5,000? compute); cost/benefit with assumed rupee values (state assumptions); recommend step-up auth (OTP/biometric) rather than block.
- Insight: flags are rare, so even 4x lift rules mostly hit good customers; combine signals, use friction not blocks.
- Rec: risk score, step-up auth, monitor false-positive complaints.
### F5 | tpv-growth-users-not-ticket | "Where did 33% TPV growth come from?" | Fintech | easy | 25
- Data: TPV 2023 Rs 12,828,210 -> 2024 Rs 17,045,673 (+32.9%); txns 9,613 -> 12,687 (+32.0%); avg ticket 1,380 -> 1,383; active users 1,732 -> 2,650 (+53%); type mix.
- Solution: metric tree (users x txns/user x ticket); compute txns per user falls; mix by txn_type.
- Insight: growth is new users, not deeper engagement (txns per user down) - retention/engagement work needed.
- Rec: activation + habit features for new users; track txns/user monthly.
### F6 | failed-payment-retry-policy | "Should we auto-retry failed payments?" | Fintech | medium | 35
- Data: 601 failed (DISTINCT); retried 291 (48.4%); retry success 168 (57.7%); by code: INSUFFICIENT_FUNDS 13.5% (7/52), UPI_SYSTEM_DOWN 61.0 (50/82), BANK_DECLINED 66.7, INCORRECT_PIN 84.0, NETWORK_ERROR 67.3, LIMIT_EXCEEDED 65.0, BANK_SERVER_TIMEOUT 74.1.
- Solution: baseline; by code table; recoverable failures (technical) vs user-side (funds); estimate gain if all technical failures were retried (script); risk of double debit; define success metric.
- Insight: retry only technical failures; insufficient-funds retry wastes effort/annoys users.
- Rec: auto-retry NETWORK/TIMEOUT/SYSTEM_DOWN with backoff; for funds failures, nudge top-up; A/B test.
### F7 | kyc-tier-limits-decision | "Do Min-KYC users deserve a higher limit?" | Fintech | medium | 30
- Data: users Full 2,874 / Min 883 / Pending 243; txns per user 5.57 / 5.65 / 5.40; avg amount 1,387 / 1,369 / 1,419; failure 2.74 / 2.46 / 2.97; flags (compute).
- Solution: compare behaviour; check whether tier is correlated with age/city; flag rates by tier (script); conclude tier doesn't change usage so limits don't hurt activity; fraud by tier decides.
- Insight: behaviour is similar, so the decision should be on risk (flags), not on activity; correlation is not cause (tiers not randomised).
- Rec: pilot higher limits for Min-KYC with monitoring.
### F8 | unverified-merchants-risk | "Are unverified merchants worth keeping?" | Fintech | medium | 30
- Data: 343 verified / 57 unverified merchants; txns per merchant 45.1 vs 24.7; failure 2.68% vs 3.20%; flag rate 1.56% (242/15,467) vs 0.71% (10/1,408); avg ticket 1,442 vs 1,481.
- Solution: size share of TPV (script); surprising: unverified have FEWER flags per txn; check by category mix (Travel/Electronics) as confounder; per-merchant economics.
- Insight: verification isn't the risk driver in this data; category mix is; don't judge by one cut.
- Rec: risk-based onboarding by category; push verification for high-risk categories.
### F9 | diwali-peak-capacity-plan | "Plan capacity for the festive month" | Fintech | medium | 35
- Data: monthly TPV (lakh): Sep-24 14.8, Oct-24 18.0, Nov-24 16.6, Dec-24 15.7; txns Sep 1,102, Oct 1,327, Nov 1,162; Oct-23 12.2 vs Sep-23 12.4 (2023 had earlier festive spike Nov 13.7); failure Sep-24 3.18%, Oct 2.64, Nov 2.24; busiest hours 19h 2,020, 18h 2,000, 10h 1,725, 20h 1,599 (all-time DISTINCT).
- Solution: festive uplift % (Oct vs Sep +21.6% TPV, +20.4% txns); hour-of-day peak share; headroom rule (peak hour = X% of day); forecast Oct-25 with YoY growth + uplift (state assumptions; keep simple); failure watch.
- Insight: festival adds ~20% over a trend that already grows ~33% YoY; plan for the 18-20h peak, not the monthly average.
- Rec: pre-scale 25-30% over last year's peak, load test, freeze deployments.
### F10 | tpv-number-dispute | "Finance says TPV is Rs 3.10 crore, Ops says 2.99 crore" | Fintech | hard | 40
- Data: raw sum of all amounts 31,012,144 (22,389 rows); raw SUCCESS 30,000,812; DISTINCT SUCCESS 29,873,883; DISTINCT, SUCCESS and amount < 50,000: 29,224,601 (10 large txns = 649,282); 89 txn_ids duplicated.
- Solution: lay out the reconciliation bridge: all rows -> remove failed/pending -> remove duplicates -> inspect large amounts (verify vs source, don't silently drop) -> agreed definition; document; note outlier rows 100x the median (556).
- Insight: both teams are right under different definitions; a metric needs a written definition and a bridge.
- Rec: single TPV definition (successful, distinct txn_id), data-quality checks in pipeline, outlier review queue.

## HEALTH
### H1 | diagnostics-staff-attrition | "Who is leaving the diagnostics company?" | Healthcare | medium | 35 | dataset hr
- Prompt: HR head of a diagnostics + telehealth company sees 22.7% of staff exited in two years.
- Data: 2,400 employees, 544 exits; by dept Customer Support (patient support) 33.6%, Sales (home-collection sales) 31.2%, Operations (lab ops) 24.4%, Engineering 16.8%, Finance 14.6%; overtime > 10h: 25.3% vs 14.7%; manager rating < 3: 28.8% vs 12.2%; tenure < 2y 32.3% vs 15.3%; reasons: compensation 117, growth 110, manager 66, overtime 54; regretted 67.
- Solution: size + annualise; by dept; drivers (overtime, manager rating, tenure); month seasonality (Dec 70, May 56); reasons; combine drivers (script); regretted vs non-regretted.
- Insight: attrition concentrated in patient support/sales with overtime and weak managers among new joiners; a few levers cover most exits.
- Rec: overtime cap, manager coaching, 90-day buddy programme in Support.
### H2 | telehealth-trial-to-paid-funnel | "Why do few trial users pay?" | Healthcare | easy | 25 | dataset subscription (wellness app)
- Data: signups 5,200 -> trials 3,308 (63.6%) -> paid 1,193 (36.1% of trials, 22.9% overall) -> renewal users 766 (64.2%); platform: iOS 45.9%, Web 39.6%, Android 31.0% (signups 1,128/863/3,209); source: Influencer 16.0%, Referral 47.1%.
- Solution: funnel (LOWER(event_name) trap); step rates; platform and source cuts; size gain if Android reached iOS (~294 users with exact rates; script); avoid mix shift trap.
- Insight: biggest leaks = Influencer traffic and Android trial experience.
- Rec: fix Android onboarding; cap Influencer spend; invest in referrals.
### H3 | march-2024-cohort-churn-spike | "March cohort leaves fast" | Healthcare | hard | 45 | dataset subscription
- Data: 60-day churn of paid by signup month: Oct-23 17.2%, Nov 25.5, Dec 23.5, Jan-24 20.0, Feb 25.6, Mar-24 54.0% (27 of 50), Apr 23.1, May 22.2, Jun 20.0, Jul 19.7; Mar trial->paid 32.7% (normal).
- Solution: confirm with sample sizes (n=50; expected ~11 at 22%, observed 27); cut the March cohort by plan, source, platform, billing cycle (script) to find the concentration; check events (payment_failed) timing; rule out data error; hypotheses (pricing, bug, campaign); next steps.
- Insight: one cohort, not the whole product, is broken - look for what was different at acquisition.
- Rec: root-cause with product/marketing calendar; win-back; guard with cohort alerts.
### H4 | home-sample-pickup-delays | "Late pickups and bad ratings" | Healthcare | medium | 35 | dataset food_delivery (home sample collection)
- Data: 15,000 pickups (rename deliveries): cancelled 710 (4.7%); avg 44.9 min; late (>10 min) 18.1%; ratings: late 3.27 delivery vs on-time 4.44 (1,890 vs 6,740 rated); distance <3 km 36.0 min 13.5% late; 3-6 km 45.4 / 18.1; 6+ km 60.5 / 26.9.
- Solution: define late; late vs rating; distance cut; cancel cut; rating bias (only 8,630 rated of 14,290 delivered); recommend zone/capacity.
- Insight: distance drives delay, delay drives rating; fix zoning, not the average time.
- Rec: cap radius per phlebotomist, promise time by distance, track on-time % by zone.
### H5 | monsoon-capacity-home-collection | "Rain days: how many extra staff?" | Healthcare | medium | 30 | dataset food_delivery
- Data: Clear 10,309 deliveries avg 44.0 min cancel 4.1%; Cloudy 2,653 / 43.7 / 5.0%; Rain 1,347 / 49.5 / 7.1%; Heavy Rain 691 / 53.9 / 9.3%.
- Solution: by weather; extra minutes per pickup (+5.5 rain, +9.9 heavy); capacity math: pickups per staff-hour fall (60/44.0=1.36 -> 60/53.9=1.11 = -18%) -> extra staff % = 22%; cancellations impact on revenue; plan.
- Insight: rain costs capacity (~20% more staff-hours) and cancellations; plan from weather forecast.
- Rec: surge staffing, shorter promise radius, reminder messages.
### H6 | hospital-kpi-scorecard | "Build a KPI scorecard for a 120-bed hospital" | Healthcare | medium | 30 | INVENTED small table (fictional, say so): month: beds 120, patient-days 1,968, discharges 410, OPD visits 6,200, OPD no-shows 810, ER arrivals 940, lab reports 5,400 with 4,860 on time (<=6h), readmissions 41, claims filed 300 rejected 36.
- Solution: pick 8 KPIs with formulas: occupancy 54.67%, ALOS 4.80, no-show 810/(6,200+810)=11.6% (define!), on-time lab 90.0%, 30-day readmission 41/410=10.0%, claim rejection 12.0%; targets/RAG; guardrails; privacy (aggregates only); what to show the CEO vs nursing head.
- Insight: low occupancy but high readmission and claim rejection = revenue leakage not demand problem; define denominators.
- Rec: 3 priority actions.
### H7 | telehealth-market-sizing | "Size a telehealth consultation market for a mid-size Indian city" | Healthcare | medium | 30 | NO data (guesstimate)
- Prompt: 20 lakh population city. Steps: households 20 lakh/4.5 = 4.44 lakh; adoption 15%; consults 3/yr; price Rs 400 -> 4.44 lakh x 0.15 x 3 x 400 = Rs 8.0 crore (compute exactly: 444,444 x 0.15 x 3 x 400 = 80,000,000 = 8.0 crore); cross-check bottom-up: 150 doctors online x 12 consults/day x 300 days x 400 = 21.6 crore -> 2.7x gap -> reconcile (assumptions).
- Insight: two methods disagree - range Rs 8-22 crore and say what you'd validate.
- Rec: pilot, measure conversion; state assumptions.

## CONSULTING
### C1 | desicart-december-sales-drop | "Sales dropped 15%" | E-commerce | medium | 40 | dataset ecommerce  (full model RCA; same as lesson 08)
- Data: Nov-24 -> Dec-24 orders 533 -> 458 (-14.1%); delivered revenue 2,591,559 -> 2,059,545 (-20.5%); delivered orders 496 -> 423; AOV 5,224.92 -> 4,868.90; buyers 448 -> 392; channels all down; cancellations 27 vs 27; coupons 110 -> 77; YoY Dec +5.5% orders, +7.9% revenue; Nov-23 -> Dec-23 orders -2.7%.
- Insight: seasonal Diwali hangover; YoY healthy; AOV fall from fewer coupons? (compute AOV of coupon vs non-coupon first).
- Rec: compare YoY, seasonal targets, December campaign.
### C2 | fashion-returns-profit-leak | "Are returns eating our profit?" | E-commerce | medium | 35
- Data: return rate fashion 20.2% (1,300/6,436), footwear 14.9%, electronics 6.3%, grocery 1.2%; refunds Rs lakh: electronics 16.59, fashion 15.92; size/fit 748 of fashion+footwear returns; margin ~33% (mrp-cost)/mrp.
- Solution: rate and rupee refund by category; reasons; margin vs return cost (assume return shipping Rs 100 - state); electronics has low rate but highest refund value; what to fix.
- Insight: rate and rupees tell different stories: fashion = size problem (fixable with size guides), electronics = value risk.
- Rec: size charts/fit finder, stricter electronics QC.
### C3 | cod-cancellation-policy | "Should we restrict cash on delivery?" | E-commerce | medium | 30
- Data: COD 2,288 orders cancel 10.4%, RTO 7.3%; prepaid cancel 3.7-4.5%, RTO 0; AOV similar (~5,300 vs 5,000-5,600); COD share 22.7%; Tier-2 heavier COD per instructor (verify by city script).
- Solution: loss per cancelled/RTO order (assume Rs 150 two-way shipping); total leakage; effect of restricting (volume loss risk); alternatives (COD fee, prepaid discount, OTP confirm).
- Insight: COD costs ~17.7% failed orders vs ~4% but is a growth channel in Tier-2: use nudges before bans.
- Rec: A/B test prepaid incentive for high-risk COD.
### C4 | influencer-budget-reallocation | "Where should next quarter's Rs budget go?" | Marketing consulting | medium | 35 | dataset marketing
- Data (clean spend<3000): Search 95,526 spend / 375 purchases / Rs 550,502 (ROAS 5.76, CAC 255); Meta 44,958/141/177,912 (3.96/319); Influencer 45,602/21/28,967 (0.64/2,171); Email 836/56/91,438; WhatsApp 1,520/46/74,391; Mega Reach Oct-24: clean spend 35,243 (raw 134,880 incl. 99,637 outlier), 2,204 clicks, 2 conversions.
- Solution: clean outlier; ROAS/CAC table; small-n caution (Email/WhatsApp scale limits); awareness caveat (last-click); reallocation math with diminishing returns (move 50% of influencer budget); test plan.
- Insight: Mega Reach drains money for ~0 sales; cheap owned channels (Email/WhatsApp) are best but limited.
- Rec: cut influencer, grow Search/Meta with caps, hold-out test for YouTube/awareness.
### C5 | free-shipping-banner-ship-decision | "Ship the free-shipping banner?" | E-commerce | hard | 45 | dataset marketing
- Data: control 6,016 users 10.57% conv, rev/user 113.3, AOV 1,072; treatment 5,974 / 11.72% / 124.0 / 1,058; Desktop 15.35% -> 13.91%, Mobile 8.47% -> 10.81%; z 1.99 p 0.046; cleaning removes contaminated users.
- Solution: clean; primary metric; significance (two-proportion z); CI; guardrail AOV and revenue per user (+9.4%); segment: Desktop negative, Mobile positive (Simpson/heterogeneity, small n); shipping cost assumption; decision rule; recommendation to ship on mobile only + follow-up test.
- Insight: borderline p; effect concentrated on mobile; don't generalise from overall.
- Rec: staged rollout, extend test, pre-register segments.
### C6 | vasudha-stockout-stores | "Four stores are underperforming" | Retail consulting | medium | 35 | dataset retail
- Data: stockout share (SKU-month snapshots with days_out_of_stock>0): Gomti Nagar 42.5%, Adajan 41.7%, Kharadi 40.5%, Velachery 38.4% vs ~2.4-3.0% peers (chain 8.4%); sales lines Gomti Nagar 682, Velachery 741 vs ~1,040 peers; Adajan 384, Kharadi 409 vs ~575 other Express stores (about -30%).
- Solution: compare within format; stockout vs sales; lost sales estimate (30% x peer sales); inventory by category; root cause hypotheses (supply route, ordering, reorder levels); caveat: sampled extract.
- Insight: sales gap closely matches stockouts; fix replenishment not marketing.
- Rec: raise reorder levels, weekly stockout KPI, supplier SLA.
### C7 | home-decor-overstock | "Home Decor sits on the shelf" | Retail consulting | easy | 25 | dataset retail
- Data: Home Decor 5.2% of units; stock cover 7.4 months vs 1.0 for all other categories (avg stock 10.5 vs 1.4 sold per month); category revenue shares.
- Solution: cover calc; capital tied up (script: stock x avg price); options: markdown, bundle, reduce reorder; recommended plan with milestones.
- Insight: overstock hides in one category; lower reorder, clear stock.
- Rec: markdown ladder, buy plan cut 60%.
### C8 | prime-membership-worth | "Is Prime membership worth its cost?" | E-commerce | hard | 40 | dataset ecommerce
- Data: 985 Prime of 4,500 customers; orders per customer 3.83 vs 1.77; AOV 5,697 vs 4,978; shipping fee 5.3 vs 6.8 (87.4% of all orders already free shipping).
- Solution: gross value; confound (heavy buyers choose Prime: selection bias); compare before/after joining not possible -> propose test; incremental margin with assumed margin 33% (from data) minus membership cost assumption; breakeven.
- Insight: Prime customers are 2x as active but not necessarily because of Prime; need test.
- Rec: A/B offer free trial of Prime to similar customers.
