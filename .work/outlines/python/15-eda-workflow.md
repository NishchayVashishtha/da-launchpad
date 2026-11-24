# 15 EDA workflow and checklist
plan: title "Exploratory data analysis (EDA) workflow" | desc "Explore a new dataset in a fixed order and write down what you find." | order 15 | 45 min | tags python, eda, pandas, checklist
objectives: run a 10-step EDA checklist; profile single columns and pairs; spot trends and segments; turn findings into 3 business insights; write an EDA summary
## concept
- Analogy: doctor's check-up: vitals first, then focused tests.
- EDA checklist (the reusable one; also asset): 1 Business question & grain (one row = ?). 2 Load, shape, dtypes. 3 Quality: nulls, dupes, impossible values. 4 Clean per lesson 14. 5 Univariate: describe, value_counts, histogram idea. 6 Time: trend by month, seasonality. 7 Segments: groupby key dimensions. 8 Relationships: correlation, crosstab. 9 Outliers & anomalies. 10 Insights + next questions + caveats.
- Grain check, row counts reconciled to SQL/Excel.
- Correlation: `df.corr(numeric_only=True)`; correlation != causation (link to stats module).
- Fintech example flow: failure rate by bank/hour -> Kaveri Co-op peak hour pattern.
- Document: "Findings -> evidence -> action" format.
## worked examples
1. fintech transactions EDA quick pass (shape, clean amount, status mix, daily volume shape).
2. segment: failure rate by hour; show the 9–10 and 18–20 peaks.
3. subscription: trial->paid conversion by platform (iOS vs Android).
4. write 3 insights in a template.
## common mistakes
- Jumping to charts before cleaning. | no grain check -> double counting. | only averages, no distribution. | reporting correlation as cause. | ignoring time. | no written conclusions.
## quiz
1 first step -> business question/grain. 2 `corr` range. 3 why check grain. 4 segment vs overall (Simpson). 5 median vs mean in skew.
## interview Qs
- Walk me through EDA on a new table. | What would you check first in a transactions table? | How do you find drivers of churn? | How do you present EDA findings? | Correlation vs causation.
## takeaways: same checklist every time; reconcile counts; segments hide truths; time matters; end with insights.
further reading: pandas-docs, kaggle-learn
## practice (eda.json, topic "eda")
| id | diff | lang | ds | ask | output | approach | mistake |
|---|---|---|---|---|---|---|---|
| python-eda-001 | easy | python | subscription | Which platform has more users: return dict of counts after dedupe users | dict | | dupes |
| python-eda-002 | medium | python | fintech | Failure rate % by hour of day (dedupe, mixed datetime) for hours 18 and 9 only | 2 rows | parse, groupby | NaT |
| python-eda-003 | medium | python | food_delivery | Correlation (2dp) between distance_km and actual_minutes (delivered rows) | float | .corr | cancelled NaN |
| python-eda-004 | hard | python | subscription | Trial-to-paid conversion % by platform (users who started trial; paid = paid_start_date not null; join subs->users dedupe) 1dp desc | DataFrame | | counting trial users from users table |
| python-eda-005 | hard | python | fintech | Failure rate by bank at peak vs off-peak (peak hours 9,10,18,19,20), pivot with banks rows 2dp, top 3 banks by peak rate | 3x3 | | |
