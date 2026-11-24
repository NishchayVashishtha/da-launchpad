# Lesson 06: Live SQL / Excel / Power BI test strategy (hub section 6)
Path: src/content/lessons/interview/06-live-test-strategy.mdx | order 6 | estimatedMinutes 35
- title "Live tests: time, thinking aloud, and getting unstuck" | description "A calm plan for SQL, Excel and Power BI live rounds."
- objectives: Split time in a 45-minute test; Think aloud in a useful way; Use a 5-step unstuck routine; Check your answers fast; Handle tool-specific traps
- tags ["live-test","sql","excel","power-bi"]
## Concept
- Analogy: pilot checklist: calm routine beats talent under stress.
- Universal 5 steps: read twice and restate; check tables/columns; write skeleton (SELECT/FROM/WHERE) then add; test on small output; sanity-check totals.
- Time management table: 45 min -> 5 read all, easy first, 8 min cap per question, 5 min final check.
- Think-aloud script lines (6 phrases): "I understand you want X per Y", "I'll start with ...", "Assumption: ...", "Edge case: NULLs/duplicates", "Let me verify with ...", "If I had more time I'd ...".
- Stuck routine: (1) simplify to 1 table (2) run partial query (3) check data with SELECT * LIMIT 5 (4) state what you tried, ask a hint (5) write pseudo-code, partial credit.
- SQL specifics: aggregate with duplicates, JOIN fan-out, NULL in NOT IN, HAVING vs WHERE, window function ORDER BY, dialect differences (SQLite strftime vs MySQL DATE_FORMAT/Postgres DATE_TRUNC), always ORDER BY + LIMIT when asked top N.
- Excel specifics: XLOOKUP vs VLOOKUP exact match, absolute refs, helper columns allowed, pivot first, Ctrl shortcuts (list 8), avoid merged cells.
- Power BI specifics: model relationship direction, measure vs calculated column, check filter context, name measures, visuals sorted, cards for KPIs.
- Camera/screen share etiquette; internet fail plan; ask whether Google allowed.
- Personalise: basic coding level -> practise 20 minutes daily in the SQL playground; the "talk while typing" habit from UI/UX walkthroughs.
## Worked examples (3 SQL, ecommerce or fintech; SqlPlayground, real output)
1 Top 3 merchant categories by transaction value: with narrated think-aloud as comments. 2 A JOIN fan-out bug and fix (orders x order_items sum double counted: show wrong vs right; ecommerce). 3 NOT IN with NULL pitfall (fintech: users with no transactions using NOT EXISTS vs NOT IN with merchant_id NULL).
## Common mistakes: silent typing; perfectionism on Q1; not testing; copy tweaks without understanding; ignoring duplicates; saying "I don't know" and stopping.
## Quiz 5: first action when stuck; time cap per question; NOT IN with NULL result; WHERE vs HAVING; best think-aloud habit.
## Interview Qs 3: What do you do if your query returns an unexpected number? How do you validate a join? Describe how you handle a question you can't solve.
## Takeaways 5; Further reading: sqlbolt, mode-sql, excel-support, power-bi-docs
## Practice (validated SQL)
| interview-pr-live-001 | medium | sql | ecommerce | Total revenue per order without double count from order_items (check columns) | order_id, revenue top 10 | writer inspects | joining payments too |
| 002 | medium | sql | fintech | Users with zero transactions (NOT EXISTS) count | value | NOT EXISTS | NOT IN + NULL |
| 003 | hard | sql | fintech | Top merchant category by txn value per month for 2024, ties by category | month, category, total | window rank | ties |
| 004 | easy | text | none | Write the 6 think-aloud sentences for a GROUP BY question | text | solution md | silence |
| 005 | medium | excel | none | Which formula returns the latest price for an item? (XLOOKUP w/ search_mode -1) | text value | solution md | VLOOKUP approximate |
