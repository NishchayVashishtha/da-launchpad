# 03-normal-distribution-z-scores  (topic: normal)
fm: title "The normal distribution and z-scores"; description "The bell curve, the 68-95-99.7 rule and how to standardise values."; order 3; estimatedMinutes 45; objectives: describe the normal curve; apply the empirical rule; compute and read z-scores; convert z to a percentile with a table or erf; tags: statistics, normal, z-score
## Concept
- Analogy: heights of 10,000 students; most near average, few very tall/short. Bell shape fully set by mean and SD.
- Empirical rule 68/95/99.7. Standard normal (mean 0, SD 1). z = (x-mu)/sigma = "how many SDs from average". Compare across different scales (a 78 in maths vs 65 in stats).
- Percentile from z: common values table (z=1 ->84.1%, 1.64->95%, 1.96->97.5%, 2.58->99.5%). In Python: `0.5*(1+math.erf(z/math.sqrt(2)))` (no scipy in the browser; teach this).
- Not all data normal: check mean~median, histogram, skew. Many metrics (delivery time) roughly normal; money is not.
- FormulaCard: z-score. FormulaCard: normal CDF via erf.
## Worked examples
1. Delivery time: mu=44.87, sigma=13.16 -> an order of 70 min: z=1.91; about 97th percentile. (script-check)
2. Python: add `z` column with vectorised formula; count |z|>2 and compare with 5% expectation.
3. Compare two things: Rahul scored 82 (mean 70, sd 8) vs Priya 74 in a test with mean 60 sd 6 -> z 1.5 vs 2.33.
4. Empirical rule check on actual data: share within 1 SD of mean, vs 68%.
## Common mistakes
- Using z-score on very skewed data and trusting the percentile. | mixing sample SD and population SD (small). | forgetting to subtract the mean. | reading z=2 as "2% of data". | using table value for one tail vs two tails.
## Quiz: share within 2 SD; z for x=70 mu=50 sd=10; which z is more extreme; z=0 meaning; two-tailed 95% cutoff 1.96.
## Interview Qs: what is a z-score and use | explain 68-95-99.7 | how to check normality quickly | z-score vs percentile.
## Takeaways 5. FurtherReading: khan-stats, numpy-docs
## Practice (normal.json) 10 q
| statistics-normal-001 | easy | python | food_delivery | Z-score (2dp) of a 70-minute delivery using the mean and sample SD of delivered actual_minutes | value | (70-mean)/std | population SD |
| -002 | easy | python | food_delivery | count of delivered orders with |z|>2 on actual_minutes | value int | abs(z)>2 sum | |
| -003 | medium | python | food_delivery | % of orders within 1 SD of mean (2dp) | value | boolean mean | |
| -004 | medium | python | food_delivery | upper cut-off minutes such that only 5% of orders are slower, assuming normal: mean+1.645*sd (2dp) | value | formula | using 1.96 |
| -005 | medium | python | food_delivery | percentile (%) of a 60-minute delivery under normal model using math.erf, 2dp | value | erf | one-tail slip |
| -006 | hard | python | hr | goals_met_pct z-score per employee review: count of reviews with z< -1.5 | value | standardise | |
| -007 | easy | text | none | z for x=85, mean 70, sd 5 | {value} 3 | | sd/mean swap |
| -008 | medium | text | none | exam A 78 (mean 65, sd 10) vs exam B 70 (mean 55, sd 5): z of better relative performance | {value} 3 (B) | compare | raw marks |
| -009 | medium | text | none | mean 200 sd 20; x for z=-1.5 | {value} 170 | x=mu+z sd | |
| -010 | hard | text | none | Order values mean ₹800 sd ₹100 normal; % above ₹1000 (2dp) | {value} 2.28 (script) | z=2 | doubling to 4.56 |
## MCQ bank (statistics-1.json, 8)
- empirical | share within 1 SD | about 68% | 95%
- z calc | x=60 mu=50 sd=5 | 2 | 10 / 0.5
- negative z | z=-1 means | 1 SD below mean | invalid value
- z=0 | value equals the mean | yes | median of nothing
- compare | z 1.8 vs z -2.3 which more unusual | -2.3 | 1.8 (ignore sign)
- 1.96 | cut for central 95% | 1.96 | 1.645
- 99.7 | within 3 SD | 99.7% | 99%
- standardised | standard normal mean/SD | 0 and 1 | 1 and 0
