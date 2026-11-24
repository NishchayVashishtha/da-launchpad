# Python / pandas bank: src/content/interview/python.json | category "python" | 80 items | ids interview-python-001..080
Each item must follow schema {id, category, question, whatInterviewerIsTesting, modelAnswer, followUps[2-3], commonMistakes[2-3], difficulty}. modelAnswer 4-8 short sentences, markdown allowed, Indian example, SQLite note where dialect differs. Questions must be distinct from each other (no paraphrases). Code in fenced python blocks; pandas 3.x style; assumed df examples from ecommerce/fintech with load("fintech","transactions") when useful (answers may show plain pandas). Writers should run snippets with .venv/bin/python (pandas available) at least once per subtopic.
Mix: easy 26, medium 37, hard 17.
Coverage:
- Python basics (types, mutability, list vs tuple vs set vs dict, is vs ==, *args/**kwargs, f-strings, scope) | 8 | 6/2/0 | "list vs tuple" | hashing
- Control flow, functions, comprehensions, generators (lambda, map/filter, list comp vs loop, generator, decorators light) | 8 | 3/4/1 | "Why use a generator" | speed
- Errors and files (try/except, with, CSV/JSON read, encoding, pathlib) | 4 | 2/2/0 |
- NumPy (array vs list, broadcasting, vectorisation, axis, boolean masks) | 5 | 2/2/1 | "Why NumPy is faster" |
- pandas core (Series/DataFrame, dtypes, loc/iloc, boolean filter, query, copy vs view, SettingWithCopy) | 10 | 3/5/2 | "loc vs iloc" | chained assignment
- Cleaning (isna/fillna/dropna strategies, duplicates, astype, str methods, to_datetime errors=coerce, outliers) | 9 | 2/5/2 | "How do you handle missing values" | imputation bias
- GroupBy, aggregation, pivot (agg named, transform vs apply, pivot_table, crosstab, value_counts) | 8 | 1/4/3 | "transform vs agg" | multi-index
- Merge/join/concat (how=, validate=, indicator, key mismatch, many-to-many blow-up) | 7 | 1/3/3 | "merge vs join vs concat" | row count checks
- Time series and dates (resample, rolling, shift, dt accessor, timezone) | 5 | 0/3/2 | "month-over-month growth in pandas" |
- Performance and large data (vectorise vs apply, categoricals, chunksize, memory_usage, Parquet) | 5 | 0/2/3 | "1 GB CSV won't fit: what do you do?"
- Visualisation and EDA (matplotlib/seaborn choices, EDA steps, correlation heatmap caution) | 4 | 2/2/0 |
- Python for analysts practical (Jupyter, virtual env, Git basics, reproducibility, SQL vs pandas when) | 4 | 2/2/0 | "When SQL vs pandas?"
- Coding-style questions with short code (reverse string, FizzBuzz-level, count word freq, flatten list, find duplicates, second largest) | 3 | 2/1/0 |
Totals 80 = 26/37/17 (matches rows).
