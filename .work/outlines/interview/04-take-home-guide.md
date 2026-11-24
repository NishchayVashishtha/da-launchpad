# Lesson 04: Take-home assignment guide (hub section 5, part 1)
Path: src/content/lessons/interview/04-take-home-guide.mdx | order 4 | estimatedMinutes 35
- title "Take-home assignments: structure that gets you hired" | description "How to plan, analyse and present a take-home in 4 hours." 
- objectives: Plan a take-home in a time budget; Structure a submission (summary first); Clean and document assumptions; Write findings for a manager; Avoid the 6 common rejection reasons
- tags ["take-home","portfolio","analysis"]
## Concept
- Analogy: a take-home is a "work sample": the reviewer reads 10 minutes; you win with clarity, not code volume.
- What hiring managers look for (checklist): answers the asked question; summary on top; correct numbers; assumptions listed; data quality noted; reproducible (SQL/notebook runs top to bottom); simple chart choices; recommendation with next step; stayed in scope/time.
- Time budget for a 4-hour task: 20 min read/ask, 30 min explore+clean, 100 min analyse, 40 min visuals, 40 min write-up, 10 min review.
- Submission structure (FormulaCard): 1 Executive summary (3-5 bullets, numbers) 2 Question restated 3 Data and assumptions 4 Method 5 Findings (chart + 1-line headline each) 6 Recommendation 7 Limits and next steps 8 Appendix (code).
- Format guide: Notebook or SQL file + 1-2 page PDF/doc; naming; README; no 40-page decks.
- When to email the recruiter: ambiguous ask, missing data, deadline conflict; how to phrase.
- Don'ts: plagiarising, using real client data, ML overkill, hidden hardcoding, pasting raw tables.
- Personalise: use UPI/fintech dataset; fresher w/ basic Python: SQL-first + small pandas; use own UI/UX strength for clean charts and layout (RealWorld).
## Worked examples (3)
1 Bad vs good executive summary rewrite (text, two blockquotes). 2 SqlPlayground fintech: duplicate check `SELECT COUNT(*) AS rows, COUNT(DISTINCT txn_id) AS unique_ids FROM transactions;` -> 22389 rows vs ~22300 unique (writer: run and paste real output); 3 Assumptions log example table (5 rows: duplicates removed, PENDING excluded from rate, 6 amount outliers (100x) flagged, NULL merchant for P2P by design, rupee text only in CSV not here).
## Common mistakes: no summary; unlisted assumptions; charts without titles/units; code that doesn't run; overbuilding ML; ignoring duplicates/outliers.
## Quiz 5: what goes first (summary); best chart for failure rate by bank (sorted bar); what if instructions unclear (ask + state assumption); how long reviewers read; PENDING handling (state assumption).
## Interview Qs 3: Tell me about a time you analysed data end to end. How do you validate your numbers? How would you present to a non-technical manager?
## Takeaways 5; Further reading: kaggle-learn, mode-sql
## Practice (fintech, SQL validated)
| interview-pr-takehome-001 | easy | sql | fintech | Count rows and unique txn_id in transactions | cols total_rows, unique_txn_ids | COUNT(*), COUNT(DISTINCT) | assuming id is unique |
| 002 | medium | sql | fintech | Flag amount outliers: transactions where amount > 100000 (check data), top 10 | txn_id, amount | writer inspects | not deduping |
| 003 | medium | text | none | Write exec summary (3 bullets) from supplied numbers | md | solution md | burying finding |
| 004 | easy | text | none | List 5 assumptions you would note for the UPI data | list | solution md | none |
