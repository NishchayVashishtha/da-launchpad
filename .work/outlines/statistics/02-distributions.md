# 02-distributions  (topic: distributions)
fm: title "Distributions and the shape of data"; description "Histograms, skew, and the common distributions analysts meet."; order 2; estimatedMinutes 40; objectives: read a histogram; spot skew and bimodality; tell discrete from continuous; use binomial and Poisson intuition for counts; tags: statistics, distributions, histogram, skew
## Concept
- Analogy: a distribution is the "shape of the crowd" at a railway platform: where people stand, how spread out.
- Discrete vs continuous; frequency table, histogram, bins (bin width changes the story).
- Shapes: symmetric, right skew (order value, salary: mean > median), left skew (marks on easy exam), bimodal (two groups mixed, e.g. weekday vs weekend).
- Binomial: n yes/no trials, p success (conversions out of 100 visitors). Poisson: events per time window (failed UPI payments per hour). Uniform one-liner. Say "no formulas to memorise, know when each applies".
- FormulaCard: Binomial mean np, SD sqrt(np(1-p)). FormulaCard: Poisson mean = variance = lambda.
- Skew rule: mean > median -> right skew. Log transform idea only as a mention.
## Worked examples
1. food_delivery.deliveries: pandas `pd.cut` frequency table of actual_minutes in 10-min bins; text histogram counts; right-skew check mean 44.9 vs median.
2. ratings.overall_rating value_counts: discrete, left-skewed.
3. Python: `df.actual_minutes.skew()` by weather; mention hist with matplotlib plain snippet (no render).
4. Binomial by hand: 20 visitors, p=0.1 -> expected 2, SD 1.34.
## Common mistakes
- Judging shape from too few/too many bins. | assuming everything is normal. | calling a rating (1-5) continuous. | ignoring bimodal data and reporting one mean. | mixing up Poisson (count in time) with binomial (count out of n).
## Quiz: mean>median means right skew; discrete vs continuous example; bimodal cause; binomial vs Poisson choice (UPI fails per hour); effect of outliers on skew.
## Interview Qs: what is skew and how detect | give real data that is right-skewed | binomial vs Poisson | why does bin width matter.
## Takeaways: 5. FurtherReading: khan-stats, pandas-docs, matplotlib-docs
## Practice (distributions.json) 10 q
| statistics-distributions-001 | easy | python | food_delivery | share of delivered orders with actual_minutes >= 60 (percent 2dp) | value | mean of boolean*100 | counting NaN rows in denominator |
| -002 | easy | python | food_delivery | skewness of distance_km (round 2) | value | .skew() | thinking sign meaning |
| -003 | medium | python | food_delivery | frequency table: 10-minute bins of actual_minutes (use pd.cut, bins 0..120 step 10, right=False), columns bin_start,orders; | DataFrame orderMatters | cut+value_counts sort_index | bin edge off by one |
| -004 | medium | python | food_delivery | ratings.overall_rating: count per rating 1-5 columns rating,count sorted by rating | DataFrame | value_counts | missing zero counts n/a |
| -005 | medium | python | food_delivery | Is distance_km right-skewed? Return dict {mean,median} (2dp) for distance_km; learner reads the gap | dict | agg | judging from mean alone |
| -006 | easy | text | none | binomial: n=50 visitors p=0.12, expected conversions | {value} 6 | np | n/p |
| -007 | medium | text | none | binomial SD n=50 p=0.12 | {value} 2.30 (script) | sqrt(np(1-p)) | forgetting sqrt |
| -008 | medium | text | none | Poisson lambda=3 failed payments/hour: expected in 4 hours | {value} 12 | scale lambda | using 3 |
| -009 | hard | text | none | P(exactly 0 failures in an hour) with lambda 3, 4dp | {value} 0.0498 (script) | e^-3 | 3e-3 |
| -010 | hard | python | food_delivery | per-weather skew of actual_minutes; output weather,skew 2dp sorted by weather | DataFrame orderMatters | groupby apply skew | including NaN |
## MCQ bank (statistics-1.json, 8)
- skew | mean 52 median 40 | right skew | left skew
- discrete | number of orders per customer | discrete | continuous
- continuous | delivery distance km | continuous | discrete
- bimodal | two peaks usually means | mixed groups | measurement error
- binomial | 15 of 100 visitors buy: model | binomial | Poisson
- poisson | tickets per hour | Poisson | binomial
- bins | too few bins | hide structure | show noise
- uniform | fair die roll shape | uniform | normal
