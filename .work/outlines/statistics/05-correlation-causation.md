# 05-correlation-causation  (topic: correlation)
fm: title "Correlation vs causation"; description "Measure how two columns move together, and why that is not proof of cause."; order 5; estimatedMinutes 45; objectives: compute Pearson and Spearman; read r from -1 to 1; explain confounders; spot spurious and Simpson-style patterns; tags: statistics, correlation, causation
## Concept
- Analogy: ice-cream sales and drowning both rise in summer; heat is the hidden third thing.
- Covariance idea; Pearson r (linear, sensitive to outliers); Spearman (rank, monotonic, robust). r^2 = share of variation explained (careful wording).
- Strength guide: |r|<0.3 weak, 0.3-0.7 moderate, >0.7 strong (rules of thumb, domain dependent).
- Causation needs: experiment (A/B), or careful controls. Confounder, reverse causality, coincidence, selection bias. Simpson's paradox short example.
- Pandas: `df[['a','b']].corr()`, `.corr(method='spearman')`. Correlation 0 does not mean no relation (curved).
- FormulaCard: Pearson r. 
## Worked examples
1. food_delivery.deliveries: corr(distance_km, actual_minutes)=0.70 (script-check), strong; corr(distance,order_value-clean) near 0.
2. hr.performance_reviews: manager_rating vs self_rating 0.78; overtime vs goals_met ~0 -> the "overtime pays off" myth.
3. Spearman vs Pearson on a skewed pair (order_value vs delivery_fee) to show difference.
4. Confounder story: weather drives both delay and cancellations; group by weather and re-compute correlation within groups.
## Common mistakes
- "r=0.7 so X causes Y". | r near 0 -> "no relationship" (curved). | correlating categories coded as numbers. | ignoring outliers that create r. | correlating cumulative/time series trending together.
## Quiz: r=-0.9 meaning; r vs r^2; confounder example; Spearman when; experiment is how to show cause.
## Interview Qs: correlation vs causation with example | how to establish causation | Pearson vs Spearman | what is a confounder / Simpson.
## Takeaways 5. FurtherReading: khan-stats, pandas-docs
## Practice (correlation.json) 10 q
| statistics-correlation-001 | easy | python | food_delivery | Pearson r of distance_km and actual_minutes (2dp) | value | corr | cancelled NaN handled by pandas |
| -002 | easy | python | hr | r between manager_rating and self_rating in performance_reviews | value | | |
| -003 | medium | python | hr | r between avg_monthly_overtime_hours and goals_met_pct | value | | claiming a cause |
| -004 | medium | python | food_delivery | Spearman of distance_km and actual_minutes | value | method='spearman' | |
| -005 | medium | python | food_delivery | per-weather Pearson r of distance and actual_minutes: weather,r sorted by weather | DataFrame | groupby | |
| -006 | hard | python | food_delivery | rating drivers: join ratings to deliveries on delivery_id; r between delay_minutes and delivery_rating (2dp) | value | merge+corr | not merging; ratings only exist for some |
| -007 | easy | text | none | r=0.8: r^2 as % | {value} 64 | square | 80 |
| -008 | medium | text | none | shop with ice cream & AC sales r=0.92; what to call hidden driver? answer solution md; expectedOutput omitted | text | | |
| -009 | medium | text | none | if all Y values double, r changes to? | {value} 1 given r=1? use: r=0.6 after doubling Y | {value} 0.6 | scaling |
| -010 | hard | python | food_delivery | within Clear weather only, delay_minutes vs delivery_rating r after merge | value | | |
## MCQ bank (statistics-2.json, 8)
- range | possible r values | -1 to 1 | 0 to 1
- sign | r=-0.6 means | as one rises other tends to fall | weak
- cause | strong r proves cause? | no | yes
- outlier | one outlier can change r | yes | no
- spearman | monotonic non-linear | Spearman | Pearson
- r2 | r=0.5 -> r^2 | 0.25 | 0.5
- zero | r=0 | no linear relation | no relation
- confounder | definition | hidden third variable | measurement error
