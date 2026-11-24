# EDA checklist (exploratory data analysis)

Use this list on any new table. Work in order. Write down what you find at each step.
Load the raw file as a copy. Never overwrite the original.

## 1. Shape and columns
- Check the row count and column count against the source note.
- Check the column names. Are they spelled the same across tables?
- Pandas: `df.shape` and `df.columns.tolist()`

## 2. Data types
- Numbers stored as text (rupee signs, commas) show up as `object`.
- Dates stored as text need parsing.
- Pandas: `df.dtypes`

## 3. Missing values
- Count the blanks per column. Ask whether each blank is expected or an error.
- Pandas: `df.isna().sum()` and `df.isna().mean() * 100`

## 4. Duplicates
- Check exact copies and repeated key values separately.
- Pandas: `df.duplicated().sum()` and `df.duplicated(subset=["id_column"]).sum()`

## 5. Categories
- List the values of each text column with counts. Look for case and space variants.
- Pandas: `df["city"].value_counts(dropna=False)`

## 6. Numbers: range and spread
- Look at min, max, median and quartiles. Compare the mean and median.
- Pandas: `df["amount"].describe()`

## 7. Outliers
- Use the IQR fences, then a domain rule. Check each flagged row before you remove it.
- Pandas: `q1, q3 = s.quantile([0.25, 0.75])`

## 8. Dates and time range
- Check the first and last date. Look for gaps and impossible dates.
- Pandas: `df["date"].min()` and `df["date"].max()`

## 9. Relationships
- Check how numbers move together. Correlation does not prove cause.
- Pandas: `df[["a", "b"]].corr()`

## 10. Write down the findings
- List the problems found, the fix chosen and the rows before and after each fix.
- Note any question the data cannot answer.

## Cleaning checklist (short form)
1. Keep the raw copy read-only.
2. Inspect shape, types, blanks and duplicates.
3. Fix types (rupee text, mixed dates).
4. Standardise text (strip, case, synonyms).
5. Handle missing values with a reason for each column.
6. Remove exact duplicates, then key duplicates.
7. Handle outliers after a domain check.
8. Validate with asserts and save a cleaned file with a log.
