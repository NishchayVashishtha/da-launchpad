# SQL bank: src/content/interview/sql.json | category "sql" | 100 items | ids interview-sql-001..100
Each item must follow schema {id, category, question, whatInterviewerIsTesting, modelAnswer, followUps[2-3], commonMistakes[2-3], difficulty}. modelAnswer 4-8 short sentences, markdown allowed, Indian example, SQLite note where dialect differs. Questions must be distinct from each other (no paraphrases).
Mix: easy 30, medium 46, hard 24. Datasets for examples: ecommerce, fintech, subscription (fictional). Where a query is in the answer, put it in a fenced ```sql block and it must be valid SQLite (or flag the dialect). Writer should run each query with sqlite3 on public/data/sqlite/<id>.sqlite at least once per subtopic to confirm correctness.
Coverage (subtopic | count | E/M/H | example Qs + what a strong answer must contain | follow-ups)
- Basics and filtering (SELECT, WHERE, LIKE, IN, BETWEEN, NULL logic, ORDER, LIMIT, DISTINCT) | 10 | 7/3/0 | "Difference between WHERE and HAVING"; "How does NULL behave in comparisons?" (3-valued logic, IS NULL, COALESCE) | What does NULL = NULL return?
- Aggregation and GROUP BY | 10 | 4/5/1 | "COUNT(*) vs COUNT(col) vs COUNT(DISTINCT col)"; "Why does selecting a non-grouped column fail in strict engines?" | conditional aggregation with CASE
- Joins | 12 | 3/6/3 | "INNER vs LEFT vs FULL"; "Find customers with no orders (anti-join: LEFT JOIN IS NULL vs NOT EXISTS vs NOT IN)"; "Join fan-out causes double counting: how to detect and fix" | self join; cross join use
- Subqueries and CTEs | 8 | 2/4/2 | "CTE vs subquery vs temp table"; "Correlated subquery: what and cost"; recursive CTE intro | readability vs performance
- Window functions | 14 | 1/7/6 | "ROW_NUMBER vs RANK vs DENSE_RANK"; "Top N per group"; "Running total, moving average"; "LAG for month-over-month"; "second highest salary 3 ways" | frame clause ROWS vs RANGE
- Dates and strings | 6 | 2/3/1 | "Monthly revenue in SQLite (strftime) vs Postgres DATE_TRUNC vs MySQL DATE_FORMAT"; "extract domain from email"; "cohort month" | time zones
- Set operations and dedupe | 6 | 2/3/1 | "UNION vs UNION ALL"; "remove duplicates keep latest row"; "find duplicate emails" | performance
- Analytics patterns | 14 | 1/6/7 | "Retention/cohort query logic"; "funnel conversion"; "gaps and islands (consecutive days)"; "percent of total"; "median in SQL"; "YoY growth"; "sessionisation" | edge cases
- Data modelling and keys | 6 | 3/3/0 | "primary vs foreign key"; "normalisation 1NF-3NF in plain words"; "star schema vs OLTP"; "surrogate key" | denormalise when?
- Performance and indexes | 6 | 2/3/1 | "What is an index; when does it not help"; "EXPLAIN reading basics"; "why SELECT * is risky"; "avoid functions on indexed column in WHERE" | covering index
- Practical and debugging | 8 | 3/3/2 | "Your query returns a bigger total than finance; debug steps"; "How do you validate a query result"; "handle NULLs in averages"; "order of execution FROM->WHERE->GROUP->HAVING->SELECT->ORDER" | idempotent queries
Totals 100 = 30/46/24 (matches rows).
