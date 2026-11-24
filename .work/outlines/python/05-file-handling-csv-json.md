# 05 File handling: text, CSV and JSON
plan: title "Reading and writing files: text, CSV, JSON" | desc "Open files safely and load data into Python." | order 5 | 30 min | tags python, files, csv, json
objectives: use `with open`; read/write text; parse CSV with csv module and pandas; read/write JSON; handle encoding and missing-file errors
## concept
- Analogy: opening a file = opening a cupboard; `with` shuts it for you.
- Modes r/w/a, encoding="utf-8" (₹ symbol!), newline.
- csv.reader/DictReader; `pd.read_csv` (sep, dtype, parse_dates, na_values, usecols, nrows); read_excel mention.
- json.loads/dumps/load/dump; nested JSON -> `pd.json_normalize`.
- try/except FileNotFoundError; pathlib basics; relative paths.
- In this site's in-browser Python: files not available; use `load("dataset","table")` and StringIO text. Say so plainly.
## worked examples
1. Parse a 4-line CSV string with csv.DictReader (StringIO) -> sum amount.
2. `load("fintech","transactions")` -> shape, dtypes: note `amount` is object (text) because of ₹ rows. Show `df.dtypes`, `df.head(3)`.
3. JSON string of one UPI event -> dict -> read nested field; dumps back with indent.
4. read_csv options shown as code (not run): dtype, parse_dates, na_values.
## common mistakes
- Forgetting encoding -> garbled ₹. | not closing file (no `with`). | reading Indian-grouped number as number. | letting pandas guess dtypes (leading zeros phone). | writing with index=True adds column. | assuming JSON keys exist.
## quiz
1 mode that overwrites -> "w". 2 `json.loads` takes -> str. 3 `index=False` effect. 4 why `amount` dtype object. 5 `with` benefit.
## interview Qs
- read a 5 GB CSV (chunksize, usecols, dtypes). | CSV vs JSON vs Parquet. | handle bad lines. | what does `with` do. | how to read nested JSON.
## takeaways: always `with`; state encoding; check dtypes after loading; JSON <-> dict; write index=False.
further reading: python-docs, pandas-docs
## practice (file-handling.json, topic "file-handling")
| id | diff | lang | ds | ask | output | approach | mistake |
|---|---|---|---|---|---|---|---|
| python-file-handling-001 | easy | python | none | Given CSV text (4 rows, header, in question), count data rows using csv + StringIO | 4 | csv.reader minus header | counting header |
| python-file-handling-002 | easy | python | fintech | Load users; return (rows, columns) count... return dict {"rows":..,"cols":..} | {"rows":4010,"cols":11} | df.shape | confusing rows/cols |
| python-file-handling-003 | medium | python | none | JSON string of 3 txns; return total of amount where status=="SUCCESS" | number | json.loads + sum | string amounts not cast |
| python-file-handling-004 | medium | python | fintech | Load transactions; return list of column names whose dtype is text (object/str) sorted | sorted list | df.select_dtypes | counts amount as numeric |
| python-file-handling-005 | hard | python | none | Nested JSON string with orders each with list of items; flatten to list of (order_id,sku,qty) tuples; return count and sum qty as dict | dict | nested loops / json_normalize | losing orders with empty items |
