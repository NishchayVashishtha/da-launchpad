# Common rules for ALL content agents (DA Launchpad)

Repo: /home/dividh/nishchay/da-launchpad. Read CLAUDE.md first (schemas, components, lesson template). Read docs/schema-cheatsheet.md for dataset tables/columns (do NOT read src/data/datasets.json — too big; query sqlite directly if you need detail: `sqlite3 public/data/sqlite/<id>.sqlite`). Read the product spec section for your module in master_prompt.md (only your section + §2, §3, §7).

Audience: a fresher in India (B.Tech CSE, basic coding), aiming for first Data Analyst job fast; target industries fintech > health > consulting. Write simple, clear English: short sentences, define each term the first time, use analogies, Indian examples (₹, UPI, Swiggy-style but FICTIONAL brands only — never real company names in data or examples), lakh/crore where natural.

Originality: all text, examples, questions and answers are your own. Never copy problem text from LeetCode/DataLemur/StrataScratch etc. Mirror patterns only.

Lessons: every non-draft lesson has the 10 H2 headings exactly and in order (see CLAUDE.md). Real depth: concept with analogy, 2–4 worked examples with real output (for SQL, run the query with sqlite3 and paste actual output as a small markdown table), 4–6 common mistakes, `<PracticeSet>` referencing your practice questions, a `<Quiz>` with exactly 5 MCQs + explanations, 3–5 `<InterviewQ>` with model answers, 5 key takeaways, `<FurtherReading>` with ids from src/data/links.json (you may ADD entries to links.json only for stable official/home pages of resources in master_prompt §7; if another agent is editing it, add at the end, keep valid JSON). No placeholders, no "coming soon", no TODO.

Practice questions: JSON per CLAUDE.md schema. Questions must be realistic business questions on the datasets. Every SQL/Python question needs a solution that runs; generate expectedOutput with `npm run validate -- --file <your file> --fill`, then LOOK at the filled output and confirm it is sensible (non-empty, plausible, ≤50 rows). Then run `npm run validate -- --file <file>` (must pass). For orderMatters:true use a fully deterministic ORDER BY (add tie-breakers). Avoid questions whose answer depends on floating-point noise; ROUND to 2 decimals.

Checks before you finish: `npx astro sync` (schema check; must have no errors), `npm run validate -- --file ...` for each of your files, `npm run audit` (fix any problems in YOUR files; ignore others' and mention them). Do NOT run `npm run build` (the orchestrator does that). Do NOT git commit. Do NOT start dev servers.

File ownership: edit ONLY the files/folders assigned in your task (+ append-only to src/data/links.json). Other agents are working in parallel.

Token discipline: don't cat big files; pipe command output through tail/head/grep; don't re-read files you just wrote; write each file in one go.

Final reply ≤150 words: files created, counts (lessons; questions by difficulty), validate/audit status, any issues. No content excerpts.

## Quality bar for question fields (added after pilot review)
- `explanation`: 2–4 sentences. Explain WHY the solution works and what each key clause does, in beginner terms, not a one-liner.
- `commonMistake`: name the concrete wrong query/approach AND what wrong result it produces.
- `hint`: nudges toward the approach without giving the answer.
- `question`: a business framing (who is asking and why) in 1–2 sentences, then exact output spec (columns, order).
- Note: playground SQLite (sql.js) is version 3.54.1 — RIGHT JOIN and FULL OUTER JOIN ARE supported; window functions supported.
