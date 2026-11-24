# 12 String and datetime handling
plan: title "Text and dates in pandas" | desc "Clean names, cities, rupee text and mixed date formats." | order 12 | 45 min | tags python, pandas, strings, datetime
objectives: use `.str` methods (strip, lower, title, replace, contains, extract, split); convert rupee text to numbers; parse dates incl. DD-MM-YYYY with `pd.to_datetime`; use `.dt` parts; resample / month bucketing; date differences
## concept
- Analogy: text = handwritten forms; dates = forms in two layouts; first make them uniform.
- `.str.strip().str.title()`, `.str.replace(r"[₹,]", "", regex=True).astype(float)`, `str.extract(r"(\d+)")`, `str.split(expand=True)`, `str.len`.
- `pd.to_datetime(s, format="%Y-%m-%d", errors="coerce")`; for mixed formats parse each format separately with errors="coerce" then `combine_first` (safe), or `format="mixed", dayfirst=True` with care (ambiguity 03-04-2024).
- `.dt.year/.month/.day_name()/.hour`; `.dt.to_period("M")`; `df.resample("MS", on=)`; `Timedelta`, `(b-a).dt.days`.
- Always check `isna()` after coerce to spot failures.
- Timezone not needed; IST assumption.
- FormulaCard: cleaning recipe for ₹ text.
## worked examples
1. ecommerce customers.city: value_counts before/after strip+title (Delhi/delhi/' DELHI ').
2. fintech transactions.amount ₹text -> float; before/after describe.
3. order_date mixed ISO and DD-MM-YYYY: parse two-step; show NaT count 0; month counts.
4. delivery days = delivery_date - order_date (ecommerce orders), avg.
## common mistakes
- Regex special chars unescaped. | `.str` on non-text/NaN. | dayfirst misread -> swapped month/day. | `errors="coerce"` hides bad data silently. | comparing date strings. | `.dt` on object column (not converted).
## quiz
1 what does coerce do -> NaT. 2 `dt.month_name()`. 3 regex to drop ₹ and comma. 4 `(d2-d1).dt.days`. 5 ISO format is YYYY-MM-DD sorts correctly as text.
## interview Qs
- Clean a column with mixed date formats. | extract digits from text. | month-over-month with resample. | why strip/lower before group. | handle timezones.
## takeaways: uniform text first; parse dates explicitly; coerce then check NaT; use .dt for parts; ₹ text -> float recipe.
further reading: pandas-docs, python-docs
## practice (text-dates.json, topic "text-dates")
| id | diff | lang | ds | ask | output | approach | mistake |
|---|---|---|---|---|---|---|---|
| python-text-dates-001 | easy | python | ecommerce | Distinct customers.city count after strip+title (dropna) | int | normalise nunique | raw nunique larger |
| python-text-dates-002 | easy | python | none | Clean ₹ list ["₹1,250","₹75.50","300"] -> floats list | [1250.0,75.5,300.0] | regex replace | |
| python-text-dates-003 | medium | python | fintech | Mean amount (2 dp) of SUCCESS txns after ₹ cleaning (dedupe txn_id; note 6 100x outliers not removed) | float | clean, dedupe, mean | text mean error |
| python-text-dates-004 | medium | python | ecommerce | Orders (dedupe) per weekday name, Mon..Sun order; dates mixed formats parsed | Series | two-format parse | dayfirst wrong |
| python-text-dates-005 | medium | python | hr | Average tenure in years (2dp) of employees (dedupe) as of 2025-01-01 using hire_date mixed formats | float | parse, subtract /365.25 | |
| python-text-dates-006 | medium | python | none | Email series ["asha@x.in", ...] 5 strings; extract domain counts dict | dict | str.split / extract | |
| python-text-dates-007 | hard | python | food_delivery | Orders per hour of day (0–23) from order_time with mixed ISO / DD-MM-YYYY HH:MM:SS, delivered or not; top 3 hours (hour, orders) | 3x2 | parse two-step | NaT dropped |
| python-text-dates-008 | hard | python | subscription | Median days from trial_start_date to paid_start_date for paid users; 1 dp; trial dates mixed format | float | parse + dt.days median | NaT rows |
| python-text-dates-009 | hard | python | fintech | Monthly SUCCESS txn count (dedupe, mixed txn_datetime) for 2024: 12 rows month, txns | 12x2 | parse, dt.to_period | month/day swap |
