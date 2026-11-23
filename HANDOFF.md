# HANDOFF: resume point for DA Launchpad

Last session: 2026-11-24. Read this first, then CLAUDE.md. The product spec is master_prompt.md.

## Workflow (keep using it; it saves main-context and usage)
- **Orchestrator** (big model): plans the work, writes short prompts pointing at brief files, and reads only short agent verdicts.
- **Briefs** in `.briefs/`:
  - `content-common.md`: rules for every content agent, including the "Quality bar" section.
  - `reviewer.md`: the Haiku reviewer rubric and its FIX mode.
  - `phase1-*.md`: done.
- **Model tiers:**
  - Sonnet: lessons, original questions, tools/UI.
  - Haiku: mechanical scripts, generators, reviewers, glossary, flashcards, test assembly.
  - Scripts (no model): validation and data.
- **Free checks:** `npx astro sync` (schemas), `npm run validate -- --file X [--fill]`, `npm run audit`, `npm run lint:quality` (writes reports/quality.json).
- Content agents never run `npm run build` or commit. The orchestrator builds once per wave.

## Status

### Done
- **Phase 1:** scaffold, components, progress store, dashboard, profile, playground, PWA, search, the validate/audit/lint scripts, all 7 datasets (`scripts/generate_data/generate_all.py`, deterministic), and `docs/schema-cheatsheet.md` (regenerate it with `.venv/bin/python scripts/schema_cheatsheet.py`).
- **Module 0 (start-here):** 6 lessons, 30 text practice questions, full `src/data/plan.json`.
- **Excel:** 16 lessons and 58 tasks. Workbooks are in `public/data/excel/` (generator: `scripts/generate_data/excel_workbooks.py`, doc: `docs/excel-workbooks.md`).
- **Power BI:** 19 lessons (incl. 3 dashboard walkthroughs and the 90-minute practical test in lesson 19) and 83 practice questions (about 70 DAX).
- **SQL lessons 01–12 and their practice:** 79 questions (49 easy / 25 medium / 5 hard). Explanations are thin and need enrichment.

### Possibly incomplete (4 Sonnet agents were still running when the session ended)
Check each item with `ls`, audit and validate:
- DONE: SQL 13–17 (joins, subqueries, CTEs, set ops): 5 lessons + 34 questions (8 easy / 16 medium / 10 hard), validated.
- DONE: SQL 18–25 (windows, cleaning, dedup, pivot, optimisation, DDL/DML): 8 lessons + 36 questions (8 easy / 16 medium / 12 hard), validated.
- DONE: SQL 26–33 patterns: 8 lessons + 30 questions (3 easy / 12 medium / 15 hard), validated.
- DONE: SQL 34–42 patterns: 9 lessons + 30 questions (3 easy / 12 medium / 15 hard), validated. TODO: lesson 41's cheat table lists the 26–33 patterns without links; add links to /sql/<slug>/.
- Targets: SQL needs 200+ questions in total (about 70 easy / 80 medium / 50 hard). Re-run `npm run audit` for the count. If any lesson or practice file above is missing or broken, relaunch a Sonnet agent for just that slice, using the same prompt pattern (read `.briefs/content-common.md`; list owned files).

## Known issues / next actions, in order
1. **Build is broken by an MDX error:** `src/content/lessons/excel/06-sumifs-countifs-averageifs.mdx:61` has a bare formula containing `"<="` outside a code block. Wrap Excel formulas in backticks or fenced code. Grep all excel and power-bi lessons for bare `<` in prose, then run `npx astro build` until it passes.
2. Finish or verify the SQL wave (above), then run the Haiku reviewer (`.briefs/reviewer.md`, FIX mode) on the SQL module. Make sure it enriches the thin explanations, commonMistakes and hints flagged by `lint:quality`, especially in the SQL 01–12 practice files.
3. **Fintech data signal is weak:** only 19 fraud-flagged transactions, and the outage windows hold only 25 transactions. Strengthen it in `scripts/generate_data/gen_fintech.py` (Haiku), regenerate, re-run `npm run validate`, and fix or re-fill any changed fintech expectedOutputs. Do this before Project 5.
4. **Retail data:** East-region stores have NO targets (the brief meant "misses its targets"). Optionally change that.
5. **SQL screening tests:** Haiku assembles 10 tests × 5 questions (45 minutes each, mixed difficulty) in `src/content/tests/` from the existing SQL practice ids, plus the timed test UI at /tools/sql-tests/ (Sonnet).
6. Then Phases 4–7 per master_prompt §9:
   - Phase 4: Python (120+ questions, Pyodide; questions assign `result`) and Statistics (100+ MCQs).
   - Phase 5: Business cases (25) and the Interview hub (banks, aptitude 300+ via Haiku with careful checking, mock mode).
   - Phase 6: Projects (8), job toolkit (resume builder, tracker), cheat sheets, glossary 300+ and flashcards 500+ (Haiku).
   - Phase 7: polish, Lighthouse, README, final counts report.
   - Tool pages go at /tools/<name>/ and get registered in `src/data/tools.json` with `enabled: true`.

## Notes for authors
- The validator reuses one DB per dataset for the whole run. DDL questions must `DROP ... IF EXISTS` and use unique `_q` table names.
- `ecommerce.orders.order_id` and `hr.employees.employee_id` contain exact duplicate rows (deliberate), so use DISTINCT or dedupe first.

## Lesson learned
- Parallel agents collided in a shared /tmp dir. Tell each agent to use its own scratch dir (e.g. /tmp/<task-slug>/).

## Git
Phase 1 is committed. Everything after it is committed as "WIP: Module 0, Excel, Power BI, SQL partial" (the build is not yet green; see item 1).

## Working approach for next phases (user-agreed)
- **The orchestrator stays in charge.** The main session plans and dispatches and reads only short verdicts. It never touches content directly.
- **Sonnet writes outlines only** (topics, examples, traps, question specs) in `.work/outlines/`. **Haiku writes all the content** from those outlines. Don't underestimate Haiku, and don't add extra layers.
- **Selective context:** each agent gets a small task packet (its outline, its dataset's schema only, a rules excerpt, 1 golden example, the gate commands). Start every packet with the same rules text so it can be cached.
- **Strong gates:** validate, audit and lint, plus an MDX compile check (to be added). Cross-check MCQs blind. Run a sampled Haiku reviewer pass.
- **Use worktrees** for parallel UI agents. Use reusable templates, briefs and scripts wherever possible.
- **Add custom agent files or hooks only if they clearly pay for themselves.**
- **Prefer smart compaction or forking** over fresh sessions. HANDOFF.md alone doesn't carry everything.
