# 01-descriptive-statistics  (topic: descriptive)
fm: title "Descriptive statistics: summarising data"; description "Mean, median, mode, spread and percentiles in plain English."; order 1; estimatedMinutes 40; objectives: compute and choose mean/median/mode; measure spread with range, variance, SD, IQR; read percentiles; summarise a column with pandas `describe`; tags: statistics, descriptive, mean, median
## Concept (order)
- Analogy: describing a cricket team's batting with a few numbers instead of reading every score.
- Centre: mean (sum/n), median (middle after sorting), mode (most common). Skewed data (order value, salary): median is the honest "typical".
- Spread: range, variance, SD (sample uses n-1, say why: "we only saw a sample, so we under-guess spread"), IQR, coefficient of variation (SD/mean) to compare spread across different units.
- Percentiles/quartiles; P90 delivery time as an SLA idea.
- Population vs sample (symbols mu, sigma vs x-bar, s). pandas `.std()` is sample (ddof=1); numpy `np.std` is population (ddof=0) -> mistake source.
- FormulaCard: Mean; FormulaCard: Sample SD s = sqrt( sum (x - xbar)^2 / (n-1) ).
- Tip: always report centre AND spread; mean alone hides risk.
## Worked examples
1. food_delivery.deliveries (delivered rows, drop NaN actual_minutes): mean vs median vs P90 of actual_minutes; show mean 44.9, SD 13.2 (script-check).
2. SQLite SqlPlayground: AVG, MIN, MAX, COUNT on deliveries by weather (SQLite has no MEDIAN/STDDEV: show median via ORDER BY LIMIT 1 OFFSET (n/2) trick in one example, flag MySQL/Postgres differences PERCENTILE_CONT).
3. Python: `df.actual_minutes.describe()` and `groupby('weather')` mean+std+count; Rain adds ~5-10 min.
4. Toy 7-number list by hand (e.g. rider tips 20,25,30,30,35,40,200): mean 54.3 vs median 30 -> outlier pulls mean.
## Common mistakes
- Using mean on skewed income/order value -> "typical" overstated. | np.std vs pandas std ddof confusion -> numbers differ slightly, interviewer notices. | Averaging averages across groups of different sizes -> wrong overall mean (need weighted). | Reporting centre without spread. | Treating NaN/cancelled rows as 0 minutes -> mean too low.
## Quiz (5): mean vs median with outlier (trap: choose mean); n-1 reason; mode of a categorical column; weighted mean of two groups (trap: simple average of 40 & 50 with sizes 90/10); IQR definition (trap: max-min).
## Interview Qs: mean vs median when? | variance vs SD | why n-1 | how to compare spread of salary vs age (CV) | how would you summarise delivery times for a manager (median + P90).
## Takeaways: 5 bullets (centre+spread; median for skew; sample SD n-1; percentiles for SLAs; clean NaN first).
## FurtherReading: khan-stats, pandas-docs, numpy-docs
## Practice (file practice/statistics/descriptive.json) - 10 q
| id | diff | lang | ds | ask | output | approach | mistake |
| statistics-descriptive-001 | easy | python | food_delivery | Ops lead wants mean delivery time. Delivered orders only | value, 2dp | dropna actual_minutes; mean; round | counting cancelled (NaN fine, but ok) / forgetting round |
| -002 | easy | python | food_delivery | median actual_minutes | value | median | quoting mean |
| -003 | easy | python | food_delivery | sample SD of actual_minutes | value 2dp | .std() | np.std ddof=0 |
| -004 | medium | python | food_delivery | P90 of actual_minutes (SLA) | value 2dp | quantile(0.9) | using max |
| -005 | medium | python | hr (performance_reviews) | mean and median goals_met_pct; return dict {mean,median} 2dp | dict | agg | - |
| -006 | medium | python | food_delivery | per-weather mean actual_minutes, table weather,mean_minutes sorted desc | DataFrame orderMatters | groupby | grouping before dropna incl NaN effect none; sort asc |
| -007 | easy | text | none | mean of 12,15,18,22,28 | {value} 19 | hand calc | dividing by 4 |
| -008 | medium | text | none | sample SD of 4,8,6,5,7 | {value} 1.58 (script) | n-1 | dividing by n gives 1.41 |
| -009 | medium | text | none | weighted mean: Pune 80 orders avg 35 min, Surat 20 orders avg 55 | {value} 39 | weights | simple avg 45 |
| -010 | hard | python | food_delivery | coefficient of variation (SD/mean*100, %) of actual_minutes for Heavy Rain vs Clear; return dict | dict | groupby agg | comparing SD only |
## MCQ bank (file statistics-1.json, 8 extra beyond quiz; ids stat-mcq-001..)
topic | idea | correct | trap
- mean-median | salaries 4 at 5L and one 90L, best typical | median | mean
- mode | most common shoe size in a store | mode | mean
- n-1 | why sample SD divides by n-1 | sample underestimates spread | "to make it smaller"
- CV | compare spread of age vs salary | CV | raw SD
- percentile | P90=52 min means | 90% of orders take <=52 | 90% take 52 exactly / 10% faster
- range | range of 4,9,15 | 11 | 15
- variance units | variance of rupees is in | rupees squared | rupees
- add constant | add 5 to every value: SD changes? | unchanged | +5
