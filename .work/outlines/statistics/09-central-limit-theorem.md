# 09-central-limit-theorem  (topic: clt)
fm: title "The central limit theorem and standard error"; description "Why sample averages behave nicely even when the data does not."; order 9; estimatedMinutes 45; objectives: define sampling distribution; compute standard error; state CLT and when n is large enough; simulate with numpy; tags: statistics, clt, standard-error
## Concept
- Analogy: one day's average delivery time jumps around; the average of 1000 days barely moves.
- Sampling distribution of the mean: mean mu, SD = sigma/sqrt(n) = standard error. Four times the data halves SE.
- CLT: mean of many independent samples is approx normal whatever the original shape (rule: n>=30 mild skew, more for heavy skew).
- SE vs SD difference (SD describes data, SE describes the estimate). SE for proportion sqrt(p(1-p)/n).
- Simulation: draw 1,000 samples of n=50, take means, plot histogram.
- FormulaCard: SE mean; SE proportion.
## Worked examples
1. food_delivery: SD 13.16, n=14407 -> SE 0.11 (script-check). Single sample n=100 -> SE 1.3.
2. Simulation (np.random.default_rng(7)) of sample means from skewed distance_km: mean of means ~ population mean; SD of means ~ SE.
3. Skewed order_value (ecommerce.orders total_amount TEXT -> clean) -> means still bell shaped.
4. Proportion: conversion 10% with n=400 -> SE 0.015.
## Common mistakes
- Confusing SE and SD. | thinking CLT makes data normal (only the mean). | applying CLT with n=5 on heavy skew. | expecting SE to shrink linearly (it's sqrt). | forgetting dependence among observations (same customer many orders).
## Quiz: SE formula; n 4x -> SE half; CLT statement; SE for proportion; when does CLT struggle.
## Interview Qs: explain CLT to a non-technical person | SE vs SD | why do A/B tests rely on CLT.
## Takeaways 5. FurtherReading: khan-stats, numpy-docs
## Practice (clt.json) 10 q
| statistics-clt-001 | easy | python | food_delivery | SE of mean actual_minutes (delivered, 4dp) | value | std/sqrt(n) | using SD |
| -002 | easy | python | hr | SE of mean goals_met_pct (4dp) | value | | |
| -003 | medium | python | food_delivery | rng=np.random.default_rng(7): 1000 sample means of 50 distance_km draws (rng.choice replace=True); return SD of those means (3dp) | value | | numpy version stable w/ PCG64 fixed |
| -004 | medium | python | food_delivery | the same simulation: mean of the sample means minus population mean, abs 3dp | value | | |
| -005 | medium | python | marketing | SE of conversion proportion in control (cleaned ab_test: drop dups, remove users in both variants) 5dp | value | | not cleaning |
| -006 | hard | python | food_delivery | n needed so that SE of actual_minutes mean <=0.5: ceil((sd/0.5)^2) | value int | | |
| -007 | easy | text | none | sigma 20 n=100 SE | {value} 2 | | |
| -008 | medium | text | none | to halve SE by how many times n | {value} 4 | | |
| -009 | medium | text | none | p=0.2 n=400 SE of proportion 4dp | {value} 0.02 | | |
| -010 | hard | text | none | sigma 15; want SE 1 -> n | {value} 225 | | |
## MCQ bank (statistics-3.json, 8)
- se | SE=sigma/? | sqrt n | n
- clt | CLT says distribution of | sample means | raw data
- n | quadruple n | SE halves | quarters
- sd vs se | SE measures | estimate precision | data spread
- skew | n=3 heavy skew | clt not reliable | works
- proportion | SE p=.5 n=100 | 0.05 | 0.5
- independence | repeated rows per customer | break assumption | no issue
- shape | sampling dist mean | centred on mu | centred on x
