# Excel bank: src/content/interview/excel.json | category "excel" | 60 items | ids interview-excel-001..060
Each item must follow schema {id, category, question, whatInterviewerIsTesting, modelAnswer, followUps[2-3], commonMistakes[2-3], difficulty}. modelAnswer 4-8 short sentences, markdown allowed, Indian example, SQLite note where dialect differs. Questions must be distinct from each other (no paraphrases). Use fictional Indian data (sales in Rs, GST, attendance). Name the formula exactly, give a one-line example, mention Excel 365 vs older versions where relevant.
Mix: easy 20, medium 30, hard 10.
Coverage:
- Basics and references (relative/absolute, named ranges, tables, shortcuts, Paste Special, data types) | 8 | 5/3/0 | "What does $A$1 do?"; "Convert text numbers to numbers" | structured references
- Lookup functions (VLOOKUP limits, HLOOKUP, INDEX-MATCH, XLOOKUP, approximate vs exact, two-way lookup, lookup left) | 10 | 2/6/2 | "VLOOKUP vs XLOOKUP vs INDEX-MATCH"; "Why #N/A and how to handle (IFERROR vs IFNA)" | multi-criteria lookup
- Logical and conditional (IF, nested IF, IFS, AND/OR, SWITCH, IFERROR) | 5 | 3/2/0 | slab-based commission with IFS | avoid deep nesting
- Aggregation (SUMIFS, COUNTIFS, AVERAGEIFS, SUMPRODUCT, SUBTOTAL, AGGREGATE) | 7 | 2/4/1 | "SUMIF vs SUMIFS"; "SUMPRODUCT use cases" | wildcard criteria
- Text and date functions (LEFT/MID/RIGHT, TEXTSPLIT or Text to Columns, TRIM, CLEAN, TEXTJOIN, DATEDIF, EOMONTH, NETWORKDAYS) | 6 | 2/3/1 | "Clean a messy phone column" | locale date issues
- Pivot tables and charts (grouping dates, calculated field, slicers, GETPIVOTDATA, refresh, chart choice) | 8 | 2/4/2 | "Why pivot not updating"; "show % of column total" | pivot caches
- Dynamic arrays and modern (FILTER, UNIQUE, SORT, LET, XLOOKUP spill, #SPILL!) | 5 | 0/3/2 | "FILTER vs Advanced Filter" | compatibility
- Data cleaning and validation (remove duplicates, data validation lists, conditional formatting, Flash Fill, Power Query intro) | 6 | 2/3/1 | "Find duplicates without deleting" | Power Query steps
- What-if and analysis (Goal Seek, Scenario, Solver, data tables, forecast) | 2 | 0/1/1 |
- Practical scenarios and best practice (model hygiene, audit trail, large files, protect sheets, macros intro) | 3 | 2/1/0 | "Your file is slow: what do you check?" | 
Totals 60 = 20/30/10 (matches rows).
