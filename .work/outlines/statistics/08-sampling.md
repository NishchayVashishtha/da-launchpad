# 08-sampling  (topic: sampling)
fm: title "Sampling and sampling bias"; description "How to pick a fair sample and how samples go wrong."; order 8; estimatedMinutes 40; objectives: separate population and sample; describe random, stratified, cluster, systematic sampling; spot bias types; compute sample vs population gaps with pandas; tags: statistics, sampling, bias
## Concept
- Analogy: tasting one spoon of dal to judge the pot (stir first = random).
- Population, sample, parameter, statistic, sampling frame.
- Methods: simple random, systematic, stratified (keep city mix), cluster, convenience. When each used.
- Biases: selection, survivorship, non-response, voluntary response (only angry users rate!). Example: ratings exist only for 57% of deliveries.
- Sampling error vs bias: more data cures error, not bias.
- Pandas: `df.sample(n, random_state=...)`, stratified via groupby.sample.
- FormulaCard: sampling fraction / standard error preview (SE=s/sqrt(n)).
## Worked examples
1. food_delivery.deliveries random sample of 500 (random_state=42): mean actual_minutes vs population mean (script-check).
2. Stratified by city: proportions preserved; compare to simple random.
3. Rating bias: share of deliveries with a rating, and average delay of rated vs unrated (merge).
4. Repeat sampling 5 times to show estimates wobble.
## Common mistakes
- Convenience sample treated as representative. | ignoring non-response. | sampling after filtering the wrong rows. | forgetting random_state -> irreproducible. | "bigger sample fixes bias".
## Quiz: stratified use; survivorship example; voluntary response; bias vs error; census definition.
## Interview Qs: how choose sample for survey of 10 lakh users | selection bias example | stratified vs cluster.
## Takeaways 5. FurtherReading: khan-stats, pandas-docs
## Practice (sampling.json) 10 q
| statistics-sampling-001 | easy | python | food_delivery | population mean actual_minutes (2dp) | value | | |
| -002 | easy | python | food_delivery | mean of random sample n=500, random_state=42 (2dp). NOTE harness uses pandas; ok deterministic w/ same pandas version | value | sample | |
| -003 | medium | python | food_delivery | share of deliveries with a rating (ratings table delivery_id unique? dedupe) % 2dp | value | nunique/ len | duplicates |
| -004 | medium | python | food_delivery | mean delay_minutes: rated vs unrated deliveries (delivered only) dict | dict | merge indicator | |
| -005 | medium | python | food_delivery | city counts in full data vs proportional stratified sample: return DataFrame city,orders sorted by city | DataFrame | | |
| -006 | hard | python | food_delivery | sample 100 per city (random_state=1), return city, mean actual_minutes rounded, sorted by city | DataFrame | groupby.sample | |
| -007 | easy | text | none | 12 lakh users, 600 surveyed; sampling fraction % | {value} 0.05 | | |
| -008 | medium | text | none | app asks only users who finished checkout to rate the checkout: name the bias (md) | text | | |
| -009 | medium | text | none | strata sizes 6000 Metro, 4000 Tier-2, sample 500 proportional: Tier-2 count | {value} 200 | | |
| -010 | hard | text | none | Of 1000 sampled, 200 respond; non-responders differ - effect on estimate explanation md; give response rate % | {value} 20 | | |
## MCQ bank (statistics-3.json, 8)
- stratified | ensure each city represented | stratified | cluster
- convenience | surveying friends | biased | random
- survivor | studying only successful startups | survivorship bias | selection
- error vs bias | larger n reduces | sampling error | bias
- frame | list users sampled from | sampling frame | population
- random | each unit equal chance | simple random | systematic
- statistic | sample mean is a | statistic | parameter
- nonresponse | only 10% reply | non-response bias | none
