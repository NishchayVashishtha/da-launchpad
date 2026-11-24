# 10 mock cases (hub section 4). Files: src/content/cases/mock-case-NN-<slug>.mdx (id = filename, "mock-case-NN" prefix). Frontmatter: title, industry, difficulty, type: mock-case, estimatedMinutes (30-45), no draft.
Body H2s for every case (same order): Problem | Clarifying questions to ask | Suggested structure | Analysis plan (with data/SQL idea) | Model recommendation | Evaluation rubric (5 criteria 0-4: Structure, Business sense, Data approach, Numbers/rigour, Communication) | Follow-up questions.
Each case body 450-700 words. Fictional brands only. India context. Numbers in cases are illustrative, state "assume".
Where a dataset exists, add an optional "Try it" SqlPlayground (fintech/ecommerce/etc.) with a validated query; otherwise pure reasoning.
Writer split: 2 writers x 5 cases (see _plan.md).

## 01 upi-failure-spike | fintech | medium | 40 min
- Problem: UPI app "SabPay"-style: payment failure rate up from 2.3% to 3.4% in a month. Find cause, recommend.
- Clarify: definition of failure (PENDING?), which month baseline, all users or segment, any release/outage.
- Structure: rate = failures/attempts; cut by bank, app, hour, amount band, failure code, device, new vs old users; check release timeline.
- Analysis: fintech failure rate by bank (Kaveri Co-op Bank ~6.1% vs ~2.2-2.9%), by app (NammaPay 5.1%), hour for Kaveri peaks (9h, 19-20h); failure_code mix. Dedupe first.
- Rec: bank timeout escalation + peak-hour retry with backoff, outage status page; monitor failure rate by bank daily; success metric: back to <2.8% in 30 days.
- Follow-ups: how to know if retries help; guardrails; how to alert.
## 02 food-late-deliveries | food delivery | medium | 40
- Problem: late deliveries (>45 min) rose 20% in 3 weeks in two cities. Why, what to do?
- Structure: delivery time = accept + prep + pickup travel + ride + handover; cuts by city, restaurant, partner, hour, rain; supply-demand ratio.
- Data: food_delivery.deliveries/restaurants/delivery_partners (writer inspects columns; optional validated SQL: late % by city).
- Rec: surge incentives for partners at peak, prep-time SLA for slow restaurants, dynamic ETA; test via pilot.
- Follow-ups: customer vs ops metric; trade-off cost vs speed.
## 03 ecommerce-returns-rise | e-commerce | medium | 40
- Problem: returns rate in Fashion rose from 12% to 17% after Diwali sale. Diagnose.
- Structure: returns/orders; cut by category, reason, size, discount depth, city, courier, new customers; sale-cohort effect.
- Data: ecommerce.returns/orders/order_items/products (optional SQL: return rate by category; validated).
- Rec: size-guide improvements, QC for high-return SKUs, return fee on deep-discount, track net revenue after returns.
- Follow-ups: cost of a return; what if returns are fraud.
## 04 subscription-churn | subscription app | hard | 45
- Problem: monthly churn rose from 5% to 7%. Where and why, and what experiment?
- Structure: cohort curves, plan, platform, acquisition source, tenure, engagement events before cancel; voluntary vs involuntary (payment failure).
- Data: subscription.users/subscriptions/events (optional cohort retention SQL; validated).
- Rec: dunning for failed payments, onboarding nudge in first 7 days, annual plan discount test; A/B design with churn at 30 days.
- Follow-ups: LTV impact; survivorship bias in churn analysis.
## 05 marketing-roi | marketing | medium | 40
- Problem: CMO wants to cut the weakest campaign channel; which one? Rs 40 lakh monthly budget.
- Structure: CAC, ROAS, conversion rate, CPA by channel; attribution caveats; incremental vs last-click; seasonality.
- Data: marketing.campaigns/ad_spend/clicks/conversions (optional ROAS SQL validated).
- Rec: shift budget gradually, run geo holdout, keep brand channel for incrementality; ask what "weakest" means.
- Follow-ups: how to measure incrementality; small-n campaigns.
## 06 hr-attrition | HR/people | medium | 40
- Problem: attrition 22% vs 14% last year in one department. What now?
- Structure: attrition by dept, tenure band, manager, salary vs band, performance rating, promotion gap; voluntary vs regretted.
- Data: hr.employees/attrition/salaries/performance_reviews (optional SQL attrition by tenure band validated).
- Rec: pay-band fix for top performers, manager coaching, stay interviews; track regretted attrition.
- Follow-ups: ethics of predicting who will leave; cost of attrition.
## 07 retail-store-underperform | retail | medium | 40
- Problem: store cluster missed targets by 10% for 2 quarters; close or fix?
- Structure: sales vs targets, footfall proxy, inventory stockouts, product mix, store age/city; profitability vs revenue.
- Data: retail.stores/sales/inventory/targets (optional SQL target attainment by store validated).
- Rec: fix stockouts, localise assortment, review rent; decision rule for closure (2 more quarters, <70% attainment).
- Follow-ups: cannibalisation; seasonal targets.
## 08 launch-go-no-go | fintech product | hard | 45
- Problem: "Pay Later" feature launched to 10% users; conversions up 4% but defaults up. Decide on full rollout.
- Structure: success metric + guardrails, uplift with CI, risk segments, unit economics (margin per user - expected loss), A/B validity (randomisation, novelty).
- No dataset; give assumed numbers table; writer computes break-even example.
- Rec: staged rollout 25%, tighter credit limits on thin-file users, monitor 60-day delinquency.
- Follow-ups: how long to wait for default data; fairness.
## 09 market-sizing-ev-charging | estimation | medium | 30
- Problem: Estimate number of public EV chargers needed in a tier-1 city of 1.2 crore people in 5 years.
- Structure: vehicles -> EV share -> charging need -> chargers per kWh/throughput -> utilisation -> sanity vs current.
- Fermi steps with assumed numbers; sensitivity table (low/base/high).
- Rec: how analyst would validate with data (registrations, charger logs).
- Follow-ups: which assumption matters most; how to refine.
## 10 dashboard-for-ops | KPI/dashboard design | easy | 30
- Problem: Build the first dashboard for a loan-collections ops head: what KPIs, layout, refresh, and caveats?
- Structure: audience & decisions, KPI tree (collection efficiency, roll rate, contact rate, promise-to-pay kept), filters, drill, alerts, definitions page.
- Include layout sketch in Mermaid or table; tie to UI/UX strength (hierarchy, whitespace) for the learner.
- Rec: 5 KPI cards + 2 trends + 1 table; weekly review ritual.
- Follow-ups: how to avoid vanity metrics; data freshness.
