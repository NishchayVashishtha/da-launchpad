# 09-metric-definition-questions  (topic: metricdef; 10 practice, text; 2 have SQL-free numbers)
fm: title "Metric definition questions"; description "Answer 'how would you measure X?' with a clear formula, edge cases and guardrails."; order 9; estimatedMinutes 45; objectives: use a 5-part template to define any metric; handle edge cases (duplicates, refunds, time zones); pick a denominator; define success/health metrics for a feature; tags: business, metrics, interview, definition
## Concept
- Template: 1 Goal (what decision?), 2 Definition (numerator / denominator / unit / time window), 3 Edge cases (duplicates, test users, refunds, cancelled, pending, outliers, time zone IST), 4 Segments to cut, 5 Guardrails + how to validate with a sample.
- Examples to define: "active user", "UPI success rate", "delivery time", "churn", "conversion", "engagement", "customer satisfaction", "readmission rate", "bed occupancy", "attrition".
- Counting units: user vs device vs session vs account; DAU/MAU stickiness; distinct vs total.
- Product success: HEART-lite (happiness, adoption, retention, task success) in plain words; primary vs guardrail.
- Analogy: defining "student attendance": present at any class? full day? late counts?
- FormulaCard: stickiness = DAU/MAU; success rate.
## Worked examples (no SQL or small SQL on fintech/subscription)
1. Define "active user" for a UPI app: >= 1 successful txn in 30 days; compare to "any app open"; fintech count: 2,853 users with a success txn out of 2,873 users with any txn (DISTINCT) - difference small; choose success-based. (verify)
2. Define "delivery time" for FoodKart: order_time -> delivered_time, delivered only, exclude cancelled, median plus p90 (mean 44.9). 
3. Define "retention" for a telehealth app: return paid month vs app open - two definitions give different numbers.
4. Define "patient wait time" for a clinic with edge cases (walk-in, emergency, reschedules).
## Common mistakes
- Vague words ("engaged") | no denominator | ignoring edge cases | one metric only (no guardrail) | mean for skewed data | forgetting time zone/window | not saying how to validate.
## Quiz: denominator choice; DAU/MAU; median vs mean; guardrail; unit of analysis.
## Interview Qs: define active user for a payments app | how measure success of a "Pay later" feature | define delivery time | define churn | define customer satisfaction.
## Takeaways 5. FurtherReading: alex-the-analyst.
## Practice (metricdef.json) all language text
| business-metricdef-001 | easy | Define "UPI success rate" with numerator, denominator, treatment of PENDING (md) | text |
| -002 | easy | DAU 12,000, MAU 48,000: stickiness % | {value} 25.0 |
| -003 | easy | 5 edge cases to handle when counting orders (md) | text |
| -004 | medium | Define "active user" for a telehealth app, two options + pick one (md) | text |
| -005 | medium | Define delivery time and say why median beats mean (md) | text |
| -006 | medium | Return rate: 1,300 returned lines of 6,436 lines (fashion, 1dp) | {value} 20.2 |
| -007 | medium | Success metrics + 2 guardrails for a "split bill" feature (md) | text |
| -008 | hard | Same word "churn", two teams quote 4% and 9%: list 4 definition differences that could explain it (md) | text |
| -009 | hard | Define "readmission within 30 days" for a hospital, with numerator, denominator, exclusions (md) | text |
| -010 | hard | Define a North Star for a UPI app and defend it against 2 alternatives (md) | text |
