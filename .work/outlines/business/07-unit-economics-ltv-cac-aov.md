# 07-unit-economics-ltv-cac-aov  (topic: unitecon; 10 practice: 5 sql (ecommerce/marketing), 5 text)
fm: title "Unit economics: AOV, conversion, CAC, LTV, ROAS"; description "Know what one customer is worth and what it costs to get them."; order 7; estimatedMinutes 55; objectives: compute AOV, conversion rate, CAC, ROAS, CPC from data; estimate LTV (simple and churn-based); judge LTV:CAC and payback; clean spend outliers before computing; tags: business, ltv, cac, aov, roas, marketing, sql
## Concept
- Definitions with formula: AOV; conversion rate = conversions/visitors (clicks); CPC; CAC = marketing spend / new customers (paid vs blended); ROAS = revenue/ad spend (note: revenue not profit); ARPU; LTV = ARPU x gross margin x lifetime; lifetime = 1/churn; payback = CAC / (monthly margin per customer); LTV:CAC >= 3 rule of thumb; payback < 12 months.
- Analogy: opening a chai stall: Rs 300 to get a regular, who spends Rs 40/visit x 30 visits.
- Caveats: last-click attribution undercounts awareness channels (YouTube/Display); revenue vs margin; channel CAC with tiny n.
- FormulaCards: CAC, LTV (simple), ROAS.
## Worked examples
1. Marketing (CLEAN: ad_spend DISTINCT and spend_inr<3000; conversions DISTINCT; Purchase only): channel spend, purchases, revenue -> ROAS and CAC table from facts (Search 5.76/255; Meta 3.96/319; Influencer 0.64/2,171; Email 109/15).
2. "Influencer Mega Reach Oct-24": raw spend 134,880 vs clean 35,243; 2 conversions. Show how the outlier row changes the verdict.
3. Subscription LTV: Standard monthly Rs 299, monthly churn from facts (assume lifetime from 62.2% cumulative churn is not monthly - so use illustrative 8% monthly churn): LTV simple = 299/0.08 = 3,737.5; with margin 70% = 2,616.25. Label ILLUSTRATIVE.
4. AOV: ecommerce Dec-24 AOV 4,868.90 (delivered). 
## Common mistakes
- Using spend with the 100x outlier | CAC over all customers incl. organic (blended) mislabelled | LTV with revenue not margin | ROAS read as profit | infinite lifetime when churn=0 | comparing channels with 2 conversions.
## Quiz: CAC formula; ROAS vs ROI; LTV simple; LTV:CAC 3; effect of outlier.
## Interview Qs: how would you compute CAC for a fintech app with referral cashback | LTV for a subscription | channel ROAS vs CAC conflict | why last-click misleads | what is a healthy payback.
## Takeaways 5. FurtherReading: mode-sql, alex-the-analyst.
## Practice (unitecon.json)
| business-unitecon-001 | easy | sql | marketing: clean total spend by channel (DISTINCT, spend_inr<3000), cols channel, spend (0dp) highest first | Google Search 95526; Influencer 45602; Meta 44958; YouTube 14861; Display 11164; Affiliate 2677; WhatsApp 1520; Email 836 | join campaigns | raw includes 99,637 row |
| -002 | medium | sql | CAC per channel = clean spend / Purchase conversions, 1dp, lowest first, cols channel, purchases, cac | Email 14.9 ... Influencer 2171.5 (fill) | two aggregates then join (avoid fan-out) | joining spend rows to conversions multiplies rows |
| -003 | medium | sql | ROAS per channel = conversion revenue / clean spend, 2dp, best first | Email 109.37 ... Influencer 0.64 (fill) | | revenue NULL treated |
| -004 | hard | sql | ecommerce: AOV (delivered, DISTINCT, <100000) by sales_channel, 2dp, cols sales_channel, orders, aov | (fill) | | outliers |
| -005 | medium | sql | marketing clicks: CPC per campaign channel? Simpler: conversion rate % = purchases / clicks per channel using clicks table (DISTINCT) | (fill) | | |
| -006 | easy | text | AOV: Rs 360000 revenue / 800 orders | {value} 450 | |
| -007 | easy | text | CAC: Rs 90,000 spend, 300 new customers | {value} 300 | |
| -008 | medium | text | LTV simple: monthly ARPU 299, margin 70%, monthly churn 8% | {value} 2616.25 | forgetting margin 3737.5 |
| -009 | medium | text | LTV:CAC if LTV 2,616.25 and CAC 255 (1dp) | {value} 10.3 | |
| -010 | hard | text | Influencer channel: ROAS 0.64, CAC 2,171 but brand reach high - recommend (md, 4 bullets) | text | |
