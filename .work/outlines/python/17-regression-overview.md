# 17 Basic regression overview
plan: title "Linear regression: a first look" | desc "Draw the best straight line through data and read what it says." | order 17 | 40 min | tags python, regression, numpy, statistics
objectives: explain slope/intercept; fit simple regression with `np.polyfit`; compute R² and correlation; predict; know limits (causation, outliers, extrapolation)
## concept
- Analogy: line of best fit through scatter of auto-rickshaw distance vs fare.
- y = a + b x; slope = change in y per 1 unit x; residual = actual - predicted; least squares idea (minimise squared residuals).
- `np.polyfit(x,y,1)`, `np.corrcoef`, R² = 1 - SS_res/SS_tot; interpret.
- Multiple regression & scikit-learn mentioned only (`LinearRegression().fit`) as local-notebook code; runner here uses numpy.
- Assumptions in plain words; outliers pull the line; don't extrapolate; correlation != causation; don't oversell for analyst job (what interviewers expect).
- FormulaCard: slope b = cov(x,y)/var(x); R².
## worked examples
1. delivery: distance_km vs actual_minutes (delivered): slope minutes per km.
2. predict minutes for 8 km.
3. R² and corr.
4. effect of removing outliers.
## common mistakes
- Treating R² as accuracy of prediction. | extrapolating beyond data. | ignoring outliers. | causation claims. | using text-dtype columns. | confusing slope units.
## quiz
1 slope meaning. 2 R² range. 3 residual. 4 `polyfit(x,y,1)` returns (slope, intercept). 5 correlation vs causation.
## interview Qs
- Explain linear regression to non-technical person. | What is R²? | Assumptions. | What if outliers. | When not to use.
## takeaways: slope = per-unit effect; R² = share explained; check outliers; no causal claims; numpy polyfit is enough for simple cases.
further reading: numpy-docs, khan-stats
## practice (regression.json, topic "regression")
| id | diff | lang | ds | ask | output | approach | mistake |
|---|---|---|---|---|---|---|---|
| python-regression-001 | easy | python | none | x=[1,2,3,4,5], y=[2,4,5,4,5]: slope rounded 2dp | 0.6 | polyfit | |
| python-regression-002 | medium | python | food_delivery | Slope (min per km, 2dp) of actual_minutes on distance_km, delivered rows | float | polyfit | NaN |
| python-regression-003 | medium | python | none | y predicted at x=6 for above fit, 2dp | 5.8 | | |
| python-regression-004 | hard | python | food_delivery | R² (3dp) of that regression | float | corr**2 | |
| python-regression-005 | hard | python | food_delivery | Delivered rows: slope (2dp) of actual_minutes on distance_km, once with all rows and once excluding distance_km>15; return dict {slope_all, slope_trim} | dict | two polyfits | not dropping NaN rows first |
