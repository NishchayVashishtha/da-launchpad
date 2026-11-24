# 03-metric-trees  (topic: metrictree; 8 practice: 6 text, 2 sql ecommerce)
fm: title "Metric trees: breaking a goal into drivers"; description "Split one big number into small parts you can measure and move."; order 3; estimatedMinutes 45; objectives: build a metric tree for revenue, profit, UPI TPV, subscription revenue; separate additive and multiplicative splits; find which branch moved; connect each leaf to an owner/action; tags: business, metric-tree, kpi, decomposition
## Concept
- Metric tree = goal at the top, drivers below, until each leaf is something a team can act on. Analogy: a family tree of a number; or checking why the electricity bill rose (units x rate; units = fans x hours).
- Two split types: multiplicative (revenue = orders x AOV) and additive (revenue = sum over categories/channels). Pick the split that matches how the business is run; MECE (no overlap, no gap).
- Trees to draw (use <Mermaid> for 2): E-commerce revenue = visitors x conversion x AOV (and buyers x orders/buyer x AOV); UPI TPV = active users x txns/user x avg ticket x success rate; Subscription MRR = paying users x ARPU, paying users = prev + new - churned; Telehealth: consults = demand x slot capacity x show-up rate; Profit = revenue - cost.
- How to use: find the leaf that moved by comparing two periods branch by branch (feeds RCA lesson 08). Leaves need owners (marketing owns visitors, product owns conversion).
- FormulaCard: % change of product ~ sum of % changes of factors (approx for small changes): ln-change idea in plain words: -14.7% orders and -6.8% AOV => revenue -20.5% (1-0.853x0.932).
## Worked examples
1. Dec-24 vs Nov-24 (ecommerce, DISTINCT orders, total_amount<100000, delivered only): delivered orders 496->423, AOV 5,224.92->4,868.90, revenue 2,591,559->2,059,545 (-20.53%). Orders explain most. Show table, SQL.
2. Go one level deeper: delivered orders = buyers x orders/buyer: buyers 448->392 (-12.5%), orders/buyer 1.19->1.168 (all orders) -> buyers branch is the main driver.
3. UPI app (fintech) 2024 vs 2023: TPV +32.9% = active users 1,732->2,650 (+53%) x txns/user x ticket (flat 1,380->1,383) x success. Compute txns per active user for both years (script-fill, do not guess). Insight: growth from users, engagement per user fell.
4. Hospital (invented): OPD revenue = patients x visits x fee; draw tree.
## Common mistakes
- Overlapping branches (double counting) | tree stops at vague leaves ("customer experience") | using additive sum of rates | mixing time periods | assuming correlation = driver | building tree without data to fill it.
## Quiz: multiplicative vs additive; MECE; which leaf owner; revenue change decomposition; TPV tree missing success rate.
## Interview Qs: break down Swiggy-style (fictional "FoodKart") revenue | profit drop - build a tree | how to prioritise leaves | metric tree for a hospital | what makes a good leaf.
## Takeaways 5. FurtherReading: alex-the-analyst.
## Practice (src/content/practice/business/metrictree.json)
| business-metrictree-001 | easy | text | revenue = orders x AOV: 800 orders x Rs 450 -> revenue | {value} 360000 | |
| -002 | easy | text | Name the 3 first-level drivers of e-commerce revenue (md) | text | |
| -003 | medium | text | Orders -14.7%, AOV -6.8% -> revenue change % (2dp) from delivered orders 496->423 and AOV 5224.92->4868.90 (revenue = orders x AOV); answer percent change in revenue, 2dp | {value} -20.53 | adding percentages gives -21.5 |
| -004 | medium | text | UPI TPV tree: draw the 4 drivers (md) | text | |
| -005 | medium | text | MRR 500000; new +60000, churned -45000, expansion +10000 -> ending MRR | {value} 525000 | |
| -006 | hard | text | Telehealth consults fell: build a 3-level tree and name the owner of each leaf (md) | text | |
| -007 | medium | sql | ecommerce: for Nov-24 and Dec-24 (DISTINCT orders, <100000, Delivered) return month, delivered_orders, revenue, aov (2dp) ordered by month; expected 496/2591559/5224.92 ; 423/2059545/4868.90 | | no Delivered filter |
| -008 | hard | sql | ecommerce Dec-24 vs Nov-24: unique buyers and orders per buyer (all statuses, 3dp), cols month, buyers, orders_per_buyer; 448/1.190 ; 392/1.168 | | COUNT(*) vs COUNT DISTINCT |
