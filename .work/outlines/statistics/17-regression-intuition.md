# 17-regression-intuition  (topic: regression)
fm: title "Regression intuition: lines that explain data"; description "Simple linear regression with numpy: slope, intercept, R-squared and the limits."; order 17; estimatedMinutes 50; objectives: explain the best-fit line; compute slope/intercept with numpy; interpret slope and R-squared; make a prediction and know extrapolation risk; tags: statistics, regression, linear-regression
## Concept
- Analogy: best straight road through scattered villages (minimise squared gaps).
- y = a + b x; slope b = r * sy/sx; intercept = ybar - b*xbar. Residual = actual - predicted. R^2 = share of variation explained (1 - SSres/SStot).
- Interpretation in business words: each extra km adds ~X minutes.
- `np.polyfit(x,y,1)` and pandas.
- Assumptions in plain words: roughly linear, no huge outliers, constant spread. Residual plot idea. Extrapolation danger. Correlation != causation again. Multiple regression mention only (more variables, same idea, sklearn/statsmodels not required).
- FormulaCard: slope and intercept; FormulaCard: R^2.
## Worked examples
1. food_delivery: actual_minutes ~ distance_km: slope 4.39 min/km, intercept 26.81, R^2 0.49 (script verified); r=0.70.
2. Predict minutes for 8 km = 61.9; warn for 40 km (beyond data: max 14 km).
3. hr: goals_met_pct ~ manager_rating slope; R^2.
4. Residuals: biggest positive residual delivery (late for its distance).
## Common mistakes
- Extrapolating. | reading slope as cause. | high R^2 = good model always. | ignoring outliers/leverage. | fitting a line to curved data.
## Quiz: slope meaning; R^2 0.49 meaning; predict; residual definition; extrapolation.
## Interview Qs: explain regression to a manager | R^2 | how check assumptions | what if relation is curved | regression vs correlation.
## Takeaways 5. FurtherReading: khan-stats, numpy-docs
## Practice (regression.json) 10 q
| statistics-regression-001 | easy | python | food_delivery | slope of actual_minutes on distance_km (np.polyfit, drop NaN) 2dp | value | | |
| -002 | easy | python | food_delivery | intercept 2dp | value | | |
| -003 | medium | python | food_delivery | R^2 (corr squared) 2dp | value | | |
| -004 | medium | python | food_delivery | predicted minutes for 8 km 1dp | value | | |
| -005 | medium | python | food_delivery | slope by weather: weather,slope sorted by weather | DataFrame | | |
| -006 | medium | python | hr | slope goals_met_pct on manager_rating 2dp | value | | |
| -007 | hard | python | food_delivery | residual of the delivery with the largest positive residual (value 2dp) | value | | |
| -008 | hard | python | food_delivery | R^2 computed as 1-SSres/SStot, equals -003: return 4dp | value | | |
| -009 | easy | text | none | y=10+3x, x=7 | {value} 31 | | |
| -010 | medium | text | none | r=0.6 sx=5 sy=10 slope | {value} 1.2 | | |
## MCQ bank (statistics-5.json, 8)
- slope | per unit x, y changes by | slope | intercept
- r2 | 0.64 | 64% variation explained | 64% correct
- resid | actual - predicted | residual | error rate
- extrap | predict beyond data | risky | safe
- fit | minimises | squared residuals | absolute max
- cause | slope shows | association | cause
- polyfit | degree 1 | line | curve
- intercept | y when x=0 | intercept | slope
