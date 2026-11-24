# 07 pandas: Series and DataFrame
plan: title "pandas first steps: Series and DataFrame" | desc "Load a table and look at it properly." | order 7 | 40 min | tags python, pandas, dataframe
objectives: create Series/DataFrame; load CSV and inspect with head/info/describe/shape/dtypes; select columns; add computed columns; count values; change dtypes
## concept
- Analogy: DataFrame = Excel sheet in code; Series = one column with an index.
- `pd.read_csv` via `load()`. head/tail/sample/shape/columns/dtypes/info/describe/nunique/value_counts/isna().sum().
- Select `df["c"]`, `df[["a","b"]]`; new column `df["fee"]=df.amount*0.01`; rename, drop, astype.
- Series ops, `.sum() .mean() .max() .idxmax() .unique() .nunique() .value_counts(normalize=True)`.
- pandas 3 note: text columns show dtype `str`/object; the `₹` columns are text, not numbers.
- Method chaining basics. Never loop rows (iterrows) on big data.
- First-look routine: shape -> dtypes -> head -> nulls -> duplicates -> describe.
## worked examples
1. `load("ecommerce","orders")`: shape (10100, 11), dtypes, head(3) (run and paste real).
2. value_counts of `order_status` (+ normalize) – Delivered share; matches instructor note on RTO/cancel.
3. New column: `net = total - discount`? total_amount is text in some rows -> demonstrate failure then use `load("ecommerce","order_items")` line_total mean instead.
4. describe() on order_items; read count/mean/min/max story (100x unit_price outlier visible).
## common mistakes
- Treating text amount as number. | `df.column` with spaces/clashing names. | chained assignment/SettingWithCopy. | forgetting `inplace` doesn't return / not assigning back. | using `len(df)` vs `df.shape[1]`. | `df["a","b"]` instead of double brackets.
## quiz
1 `df.shape` returns -> (rows, cols). 2 `df[["a"]]` returns DataFrame vs `df["a"]` Series. 3 best first call to see dtypes+nulls -> info(). 4 `value_counts(normalize=True)` -> proportions. 5 `df.drop("c", axis=1)` returns new frame.
## interview Qs
- Series vs DataFrame vs ndarray. | head/info/describe what you learn. | difference between `df["a"]` and `df[["a"]]`. | how do you check data quality first? | `inplace` – should you use it?
## takeaways: always look before you analyse; dtypes tell the story; double brackets = DataFrame; add columns vectorised; value_counts is your best friend.
further reading: pandas-docs, kaggle-learn
## practice (pandas-basics.json, topic "pandas-basics")
| id | diff | lang | ds | ask | output | approach | mistake |
|---|---|---|---|---|---|---|---|
| python-pandas-basics-001 | easy | python | ecommerce | Load customers; return number of rows (raw, with duplicates) | 4520 | len(df) | dedup first -> 4500 |
| python-pandas-basics-002 | easy | python | hr | Distinct employment_status values sorted as list | sorted list | unique + sorted | NaN included? (check) |
| python-pandas-basics-003 | easy | python | subscription | Product: how many subscriptions per status (raw rows)? Return Series sorted by count desc | Series index status | value_counts | forgetting that value_counts drops NaN by default |
| python-pandas-basics-004 | easy | python | retail | Mean carpet_area_sqft of stores rounded 1 dp | float | df.col.mean() | sum/len issue none |
| python-pandas-basics-005 | medium | python | ecommerce | order_items: add `gross = quantity*unit_price`; return total gross rounded 2 dp | float | vectorised column | uses line_total (already discounted) |
| python-pandas-basics-006 | medium | python | food_delivery | Proportion of deliveries per delivery_status (normalised, round 3) as Series | Series | value_counts(normalize) | forgetting duplicates (note) |
| python-pandas-basics-007 | medium | python | fintech | Return DataFrame of user_id, full_name, city for first 5 rows of users sorted by user_id | 5x3 | df[[...]].sort_values.head | single brackets -> Series |
