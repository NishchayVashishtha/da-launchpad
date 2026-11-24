# 13 Missing values, duplicates and outliers
plan: title "Missing values, duplicates and outliers" | desc "Find and fix the three most common data problems." | order 13 | 45 min | tags python, pandas, cleaning, missing, duplicates, outliers
objectives: detect NaN with isna; choose drop/fill/flag; find and drop duplicates; detect outliers with IQR and z-score; decide cap/remove/keep and document
## concept
- Analogy: cleaning rice: stones (outliers), empty husks (missing), double packets (duplicates).
- Missing types: by design (cancelled orders no delivery time) vs error; MCAR idea in 1 line. Never fill blindly.
- isna().sum(), `isna().mean()`, dropna(subset), fillna (value, median, ffill), `fillna("Unknown")`, add flag column.
- Duplicates: `duplicated()`, `drop_duplicates(subset, keep)`; exact vs key duplicates; the datasets have exact dupes.
- Outliers: IQR rule Q1-1.5IQR..Q3+1.5IQR; z-score; domain rule (100x entry error) ; clip/winsorise; look at max & describe.
- FormulaCard: IQR fences. Median vs mean robustness.
- Document each cleaning decision (rows before/after).
## worked examples
1. fintech users: missing counts; `city` NaN 3%; fill "Unknown".
2. transactions: duplicates count (~90) and drop; rows before/after.
3. transactions.amount cleaned: IQR fences; 6 rows of 100x flagged.
4. food_delivery: actual_minutes NaN are cancelled; do not impute.
## common mistakes
- fillna(mean) with outliers. | dropping all rows with any NaN. | drop_duplicates on key only when rows differ. | treating NaN-by-design as errors. | removing outliers that are real (festival spikes). | cleaning without a log.
## quiz
1 duplicated default marks which -> later duplicates keep='first'. 2 IQR formula. 3 median robust. 4 `dropna(how="all")`. 5 when not to impute.
## interview Qs
- How do you handle missing data? | Outlier detection methods. | Mean vs median imputation. | How do you decide duplicates? | Real example you cleaned.
## takeaways: ask why missing; log row counts; exact dupes are safe to drop; outliers need domain check; median beats mean for skew.
further reading: pandas-docs, kaggle-learn
## practice (missing.json, topic "missing")
| id | diff | lang | ds | ask | output | approach | mistake |
|---|---|---|---|---|---|---|---|
| python-missing-001 | easy | python | fintech | How many fully duplicate rows are in transactions (raw)? | int (writer reads actual value) | df.duplicated().sum() | using subset=txn_id changes the count |
| python-missing-002 | easy | python | ecommerce | % of customers (raw rows) with NULL email, 2 dp | float | isna().mean()*100 | counting after dedupe |
| python-missing-003 | medium | python | hr | Missing count per column of employees as Series of columns with at least one NULL, desc | Series | isna().sum() filter | |
| python-missing-004 | medium | python | food_delivery | Prove NULL actual_minutes happen only for cancelled orders: after dropping exact dupes, return crosstab of delivery_status (rows) vs actual_minutes isna (cols) | small DataFrame | pd.crosstab(status, isna) | filling NULL with 0 which drags the average down |
| python-missing-005 | medium | python | subscription | users: fill NULL city with "Unknown" after strip/title; value counts top 3 | Series | | |
| python-missing-006 | hard | python | hr | salaries.annual_ctc cleaned; count rows outside IQR fences; and count of exact 100x (>5e7) | dict{iqr_outliers, extreme} | quantile | text; ₹ |
| python-missing-007 | hard | python | retail | sales dedup by sale_id (exact dupes), net_amount cleaned; median net amount per category with outliers excluded by 100x rule (value > 10*category median) 2dp | DataFrame | 2-step | mean skew |
| python-missing-008 | hard | python | marketing | ab_test_results: drop exact dupes, then drop users in both variants; return count of rows and conversion rate per variant 2dp | DataFrame | groupby nunique, isin | |
| python-missing-009 | medium | python | fintech | Users (dedupe): fill missing city with the most common city; return dict {mode_city, filled_count} | dict | mode()[0], isna().sum() | filling before standardising case, so mode is wrong |
