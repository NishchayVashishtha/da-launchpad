# Writer brief (Haiku content writers) — DA Launchpad
Repo: /home/dividh/nishchay/da-launchpad. You WRITE final content from a finished outline. Design decisions are already made in the outline; follow it, don't redesign.

Read, in this order and nothing else unless needed:
1. CLAUDE.md (schemas, components, lesson template).
2. .briefs/content-common.md (rules + quality bar). Exception to it: do NOT edit src/data/links.json; use existing ids only (`grep -o '"id": *"[^"]*"' src/data/links.json`), and list any missing link you wanted in your final reply.
3. Your outline files (given in your task) and the module's _plan.md section for your task.
4. Schema of datasets you use: .work/schema/<dataset>.md (small). Query real data with `sqlite3 public/data/sqlite/<id>.sqlite` or .venv/bin/python + pandas.
5. Golden example to match for style/depth: src/content/lessons/sql/13-joins-inner-left.mdx (read Concept + Worked examples + Quiz only, with sed ranges).

Rules specific to this wave:
- Numbers in lesson text (worked example outputs, stats results) must come from actually running code, never from memory or the outline's approximate values. Paste real output as small markdown tables / code blocks.
- Python practice: language "python", `solutionCode` uses `load(dataset, table)` and assigns `result`; only pandas, numpy, math, stdlib (no scipy/sklearn/matplotlib). Never use random sampling (`sample`, `default_rng`, `random`) in solutions; use deterministic subsets instead. Round floats to 2–4 decimals. Fill expectedOutput with `npm run validate -- --file <f> --fill`, inspect it, then re-run without --fill (must pass).
- "text" questions with a numeric answer: put `{ "value": <number> }` in expectedOutput, computed by running code, and the worked calculation in `solution` markdown.
- In MDX prose, never leave bare `<`, `>`, `{`, `}` outside code — wrap formulas/expressions in backticks. Gate: `npm run check:mdx -- <your mdx files>` must report 0 failed.
- Edit ONLY the files your task owns. Scratch dir: /tmp/<your-task-id>/.

Gates before finishing (all must pass): `npm run check:mdx -- <files>`; `npm run validate -- --file <each practice file>`; `npx astro sync 2>&1 | tail -3`; `npm run audit 2>&1 | tail -5` (fix problems in your files only). No build, no commit, no dev server.
Final reply ≤80 words: files written, counts (lessons; questions by difficulty; MCQs), gate results, deviations from outline, missing links.

## Lessons from the statistics wave (apply these)
- `load()` reads public/data/csv/<id>/<table>.csv (messy CSV: some money columns are text like "₹1,234", mixed date formats, exact duplicate rows). Compute lesson numbers with the same pandas `load` data learners use; dedupe by the table's id column when the outline says so; say in the lesson when you clean.
- Don't trust numbers in the outline; recompute and use yours (report differences in your final reply).
- Frontmatter must match the schema exactly (title, description, module, order, estimatedMinutes, objectives, tags), and `npx astro sync` must show no error from YOUR files before you finish.
