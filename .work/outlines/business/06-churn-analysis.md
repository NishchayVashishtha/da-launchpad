# 06-churn-analysis  (topic: churn; 10 practice: 6 sql subscription, 4 text)
fm: title "Churn analysis: who leaves and why"; description "Measure churn correctly, compare segments, and separate voluntary from payment-failure churn."; order 6; estimatedMinutes 50; objectives: define customer and revenue churn; compute churn by plan and billing cycle; read survival-style numbers; separate voluntary vs involuntary churn; propose actions; tags: business, churn, subscription, sql
## Concept
- Churn rate = customers lost in period / customers at start of period. Customer churn vs revenue churn vs net revenue retention. Monthly vs annual (monthly 5% = ~46% annual: 1-0.95^12). Analogy: leaky bucket.
- Voluntary (cancels) vs involuntary (card fails: payment_failed ~45% of failed renewals lead to cancel per instructor note; verify with data only if possible). Early vs late churn. Cancelled vs expired trial (trial_expired is NOT churn of paying users).
- Always define: churn of whom (paid users), when (observation end 2024-12-31), right-censoring: active users may still churn.
- Drivers via segments: plan, billing cycle, source, platform, tenure. Action menu: onboarding, annual-plan nudges, dunning (retry failed payments), win-back.
- Healthcare angle: patient drop-out from a chronic-care programme; employee churn = attrition (link lesson 01).
- FormulaCard: churn rate; annualised churn from monthly.
## Worked examples (subscription; DISTINCT subs; paid = paid_start_date not null; churned = status='cancelled')
1. Overall: 654 of 1,193 paid cancelled = 54.8%.
2. By billing cycle: monthly 621/998 = 62.2%; annual 33/195 = 16.9%. By plan within monthly: Basic 67.2, Standard 61.7, Premium 55.3.
3. Revenue-weighted view: churned monthly revenue = sum price_inr of cancelled monthly subs (script).
4. Tenure at cancel: days between paid_start_date and cancel_date buckets 0-30, 31-60, 61-90, 90+ (script-fill) -> early churn.
## Common mistakes
- Counting trial_expired as churn | dividing by all users | ignoring censoring (comparing 2024 starters with 2023 starters) | blending monthly+annual | confusing churn % with retention % | recommending discounts without checking why.
## Quiz: churn formula; annualised churn; trial_expired; voluntary vs involuntary; why annual plans look better.
## Interview Qs: churn rose from 4% to 6% - walk me through | how to define churn for a UPI wallet | voluntary vs involuntary actions | how will you estimate revenue lost to churn | attrition vs churn.
## Takeaways 5. FurtherReading: mode-sql, sqlite-docs.
## Practice (churn.json) dataset subscription (DISTINCT subscriptions)
| business-churn-001 | easy | sql | Paid subscriptions and cancelled count (status='cancelled' among paid). cols paid, cancelled | 1193, 654 | SUM(status='cancelled') | counting trial_expired |
| -002 | easy | sql | Churn % (1dp) among paid subs | 54.8 | | |
| -003 | medium | sql | Churn % by billing_cycle: cols billing_cycle, paid, cancelled, churn_pct (1dp) ordered by churn desc | Monthly 998/621/62.2; Annual 195/33/16.9 | | |
| -004 | medium | sql | Monthly-billing churn % by plan (1dp) cols plan, paid, churn_pct ordered desc | Basic 67.2; Standard 61.7; Premium 55.3 (paid counts 302/517/179) | | mixing annual |
| -005 | medium | sql | Monthly revenue lost: sum of price_inr of cancelled monthly paid subs, by plan; cols plan, lost_mrr | (fill) | | summing annual |
| -006 | hard | sql | Tenure buckets at cancellation for cancelled paid subs: '0-30','31-60','61-90','90+' days, counts, share % (1dp) | (fill) | CASE + julianday | NULL cancel_date rows |
| -007 | easy | text | Monthly churn 5%: annualised churn percent (1-0.95^12), 1dp | {value} 46.0 | multiplying 5x12=60 |
| -008 | medium | text | 1,000 customers at start, 80 left, 120 joined: churn % and ending count (value churn) | {value} 8.0 | using ending base |
| -009 | medium | text | A telehealth programme: 400 enrolled, 128 dropped by month 3: dropout % | {value} 32.0 | |
| -010 | hard | text | Management wants a 20% discount to cut churn. List 4 checks before agreeing (md) | text | |
