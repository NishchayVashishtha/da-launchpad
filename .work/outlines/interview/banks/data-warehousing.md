# Data warehousing and ETL for analysts: src/content/interview/data-warehousing.json | category "data-warehousing" | 30 items | ids interview-dw-001..030
Each item must follow schema {id, category, question, whatInterviewerIsTesting, modelAnswer, followUps[2-3], commonMistakes[2-3], difficulty}. modelAnswer 4-8 short sentences, markdown allowed, Indian example, SQLite note where dialect differs. Questions must be distinct from each other (no paraphrases).
Mix: easy 10, medium 14, hard 6. Keep analyst-level (no deep engineering). Mention career path to Data/Analytics Engineer where natural (profile long-term goal).
Coverage:
- Concepts (OLTP vs OLAP, data warehouse vs data lake vs lakehouse in plain words, data mart, ODS) | 5 | 3/2/0 | "OLTP vs OLAP with a UPI example" | where does a DA sit
- Modelling (star vs snowflake, fact vs dimension, grain, surrogate keys, SCD types 1/2/3, conformed dimensions, factless fact) | 8 | 2/4/2 | "What is grain and why decide it first"; "SCD Type 2 example: customer changes city" | late-arriving data
- ETL/ELT and pipelines (ETL vs ELT, batch vs streaming, orchestration (Airflow idea), incremental vs full load, idempotency, CDC idea, dbt idea) | 8 | 2/4/2 | "ETL vs ELT and why ELT is common now" | backfills
- Data quality and governance (validations, null/dupe checks, reconciliation, lineage, PII masking, data contracts light) | 5 | 1/3/1 | "How do you check a pipeline loaded correctly" |
- Analyst-facing practicalities (partitioning, indexes, columnar storage, materialised views, cost awareness on cloud warehouses, semantic layer / metrics definitions) | 4 | 2/1/1 | "Why are columnar stores fast for analytics"
Totals 30.
