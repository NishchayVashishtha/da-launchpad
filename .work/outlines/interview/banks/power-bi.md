# Power BI / DAX bank: src/content/interview/power-bi.json | category "power-bi" | 60 items | ids interview-powerbi-001..060
Each item must follow schema {id, category, question, whatInterviewerIsTesting, modelAnswer, followUps[2-3], commonMistakes[2-3], difficulty}. modelAnswer 4-8 short sentences, markdown allowed, Indian example, SQLite note where dialect differs. Questions must be distinct from each other (no paraphrases). DAX in fenced blocks. Use fictional sales/subscription/HR data. 
Mix: easy 18, medium 28, hard 14.
Coverage:
- Power BI basics and components (Desktop/Service/Mobile, Import vs DirectQuery vs Live vs Composite, refresh, gateway, workspaces, licences in plain words) | 8 | 5/3/0 | "Import vs DirectQuery trade-offs" | when composite
- Power Query / ETL (steps, merge vs append, unpivot, data types, query folding, parameters, error handling, M basics) | 9 | 3/4/2 | "What is query folding and why care" | incremental refresh
- Data modelling (star schema, relationships, cardinality, cross-filter direction, role-playing dims, date table, many-to-many, hide fields) | 10 | 2/5/3 | "Why a dedicated date table"; "bi-directional filter risks" | snowflake
- DAX fundamentals (measure vs calculated column, row context vs filter context, implicit vs explicit measures, SUM vs SUMX, DIVIDE) | 8 | 3/4/1 | "Measure vs calculated column" | storage and memory
- DAX CALCULATE and filters (CALCULATE, FILTER, ALL, ALLEXCEPT, REMOVEFILTERS, KEEPFILTERS, VALUES, context transition) | 8 | 0/4/4 | "How does CALCULATE work"; "% of total measure" | context transition
- Time intelligence (TOTALYTD, SAMEPERIODLASTYEAR, DATEADD, rolling 3 months, YoY%, MTD) | 5 | 0/3/2 | "YoY growth measure" | fiscal year April-March (Indian FY)
- Visuals and storytelling (chart choice, slicers, drill-through, bookmarks, tooltips, conditional formatting, avoid clutter) | 5 | 3/2/0 | "Pick a visual for trend vs comparison" | mobile layout
- Security and sharing (RLS static/dynamic, workspace roles, apps, sensitivity labels) | 3 | 1/1/1 | "Implement RLS by region"
- Performance and best practice (Performance Analyzer, DAX Studio mention, reduce cardinality, avoid calculated columns, aggregations, naming) | 4 | 1/2/1 | "Report loads slowly: steps"
Totals 60 = 18/28/14 (matches rows).
