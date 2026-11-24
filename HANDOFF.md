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


### Session 2 (2026-11-24): done
- **Build green.** Use the `npm run check:mdx [-- files]` gate (per-file MDX compile).
- **Enrichment:** 210 thin practice fields enriched (SQL, Excel, Power BI). New gate `node scripts/check-protected.mjs [--allow f]` checks that only text fields changed against HEAD.
- **Fintech data:** fraud flags are 1.35%; there are 4 NammaPay outage windows (38.7% failed vs 2.2%). 25 SQL expectedOutputs were refilled, and SQL and Power BI lesson numbers were refreshed.
- **Statistics:** 17 lessons, 170 practice, 136 MCQs (`mcq/statistics-t1..t9.json`), 25 interview Qs.
  - Blind MCQ check (`scripts/mcq-blind.mjs`) found 5 wrong keys; all are fixed.
  - Text `{value}` answers: 52/52 matched an independent recomputation.
- **Python:** 20 lessons, 130 practice (42/49/39), `public/downloads/eda-checklist.md`, 8 notebooks. Rebuild them with `.venv/bin/python scripts/notebooks/build.py`; specs are in `scripts/notebooks/specs/`.
- **Pipeline that worked:**
  - Sonnet outliner → `.work/outlines/<module>/` (FORMAT.md).
  - Haiku writers with `.work/writer-brief.md` plus per-dataset `.work/schema/<id>.md`.
  - Gates, then blind verification, then a Haiku reviewer.
  - `.work/` is gitignored; copy anything durable out of it.

### Usage log (subagent tokens, approximate)
- Sonnet outliner: about 100k each.
- Haiku writer (2 lessons + 20 questions): 95–150k.
- Haiku enricher (about 40–70 questions): 85–105k.
- Haiku blind verifier: about 50k.
- Resuming a finished agent with SendMessage for a follow-up: about 7k (vs about 65k for a fresh agent). Prefer this for fixes.
- 2 of 9 Haiku writers stopped partway. Resuming them with SendMessage finished the job.

### Gotchas learned
- The Python harness `load()` reads CSVs: money columns are often text ("₹1,234"), dates are mixed, and there are exact duplicate rows. Dedupe by the id column, and clean before deduping.
- DataFrame results need `reset_index(drop=True)`.
- `.venv` has pandas 3 (text dtype is `str`). Pyodide may differ; check in the browser in Phase 7.
- No scipy, sklearn or matplotlib in the harness.
- Outline numbers are often wrong. Writers must recompute.

## Totals so far (from reports/counts.json)
| Module | Lessons | Practice | Other |
|---|---|---|---|
| Start Here | 6 | 30 | plan.json |
| Excel | 16 | 58 | 6 workbooks |
| SQL | 42 | 209 | 10 screening tests |
| Power BI | 19 | 83 | |
| Python | 20 | 130 | 8 notebooks, EDA checklist |
| Statistics | 17 | 170 | 136 MCQs |
| Interview | 8 | 41 | 475 bank items, 320 aptitude MCQs, 10 mock cases |
| Business | 14 | 132 | 25 written case studies |

Tool pages are built and registered in tools.json:
- /interview/banks/
- /tools/aptitude/
- /tools/mcq/
- /tools/sql-tests/
- /tools/mock-interview/

They are NOT yet checked in a browser.

## NEXT SESSION: do these in order
1. **[DONE] Interview hub writers:**
   - Tasks L1–L5: 8 lessons + 41 practice, ids `interview-pr-*`.
   - Tasks C1–C2: 10 mock cases in `src/content/cases/mock-case-NN-*.mdx`, type "mock-case".
   - Deleted placeholder `sample-case.mdx` and `_sample.json`. All 4 gates green (check:mdx, validate, audit, build).
2. **[DONE] Business writers:**
   - 14 lessons in `src/content/lessons/business/01..14-*.mdx`, all 10 required H2s.
   - 14 practice sets in `src/content/practice/business/*.json`: 132 questions total (39 SQL, 93 text), fully validated against SQLite datasets.
   - 25 written case studies in `src/content/cases/*.mdx`: 10 Fintech (F1-F10), 7 Healthcare (H1-H7), 8 Consulting (C1-C8), all with the 7 standard H2s.
   - Added official DPDP Act link to `src/data/links.json`.
   - All 4 gates green (check:mdx 179 files, validate 491 runnable passed, audit passed, build 215 pages + 184 indexed).
3. **[DONE] Fix the aptitude syllogism template** in `scripts/generate_aptitude.py`:
   - Updated `p_syllogism` to enforce non-empty models (existential import: each term has $\ge 1$ element).
   - Constrained conclusion candidates and distractors strictly to end terms (`end1` and `end2`), eliminating trivial single-premise conversions.
   - Guaranteed distractors are false in at least one valid model.
   - Clarified question prompt: "assume each group has at least one member".
   - Regenerated all 320 aptitude questions (`scripts/generate_aptitude.py`).
   - Ran blind MCQ check (`node scripts/mcq-blind.mjs prep aptitude-logical 1` -> independent blind solver -> `compare`): **60 answered, 0 disagree** (100% pass).
4. **[DONE] Light dedupe of the interview banks:**
   - Replaced `interview-powerbi-031` with dedicated question on `RELATED` vs `RELATEDTABLE` in DAX (scalar navigation many-to-one vs table navigation one-to-many).
   - Replaced `interview-sql-071` with Top-3 highest-spending customer ranking per city using `ROW_NUMBER() OVER (PARTITION BY ...)` with clean data handling (`UPPER(TRIM(city))`) tested against `ecommerce.sqlite`.
   - Verified `statistics-2.json` vs `statistics.json`: 0 duplicate questions, clean progression from foundational descriptive/probability concepts (25 Qs) to advanced A/B testing/regression concepts (35 Qs).
   - All 4 gates green (audit 475 questions, check:mdx 179 files, validate 491 solutions, build 215 pages).
5. **[DONE] Reviewer pass** (`.briefs/reviewer.md`, FIX mode) on interview banks + Phase 5 content:
   - Fixed `business-churn-004` and `business-churn-005` case sensitivity in SQLite (`LOWER(billing_cycle) = 'monthly'`) and refreshed expected output with real database values.
   - Added 3rd `<InterviewQ>` to business lessons 09–14, and expanded word count of lesson 11 to >1,200 words.
   - Enriched 57 business practice explanations and common mistakes with detailed analytical takeaways and failure modes (all explanations $\ge 25$ words, common mistakes $\ge 12$ words).
   - Enriched `interview-pr-final-004` common mistake text.
   - Re-ran quality lint: 0 warnings across all business and interview modules (total warnings reduced from 184 to 110, all remaining warnings are in start-here).
   - Generated review report in `reports/review-phase5.md`. All 4 gates green (check:mdx 179 files, validate 491 runnable passed, audit passed, build 215 pages + 184 indexed).
6. **[DONE] Browser smoke test** of the tool pages and the Python runner in Pyodide:
   - Previewed build at `http://localhost:4321/` using the browser subagent (`7647c29f-538b-4ac9-a2ad-fa67d86c0ac4`).
   - Verified `/interview/banks/`: Category filters (8 categories, 475 questions), search, filtering, and model answer toggle with follow-ups and common mistakes.
   - Verified `/tools/aptitude/`: Categories (Quant, Logic, DI, Verbal), timed session with countdown timer, question pagination, radio selection, and answer feedback + shortcuts on submit.
   - Verified `/tools/mcq/`: 136 statistics MCQs across topic groups, timed test execution, score report, and detailed statistical explanation.
   - Verified `/tools/sql-tests/`: All 10 SQL screening tests listed, 45-min timer, problem prompt, SQL code editor, and "Run" button.
   - Verified `/tools/mock-interview/`: Category checkboxes, question counts/timers, prep notes editor with script saving.
   - Verified `/python/pandas-series-dataframe/`: Interactive code runner in practice section, "Run" and "Compare with expected", and Pyodide initialization.
   - All pages loaded cleanly (HTTP 200, 0 console errors).
7. **Phase 6:**
   - Projects (8): Sonnet outlines, then Haiku writers.
   - Job toolkit: resume builder + tracker UI (Sonnet).
   - Cheat sheets, glossary 300+ and flashcards 500+: Haiku, derived from existing lessons; dedupe by script.
8. **Phase 7:** polish, Lighthouse, README, final counts report.
9. **Optional:** retail East-region targets (see the old note below).

## Known issues / older notes
- Retail: East-region stores have NO targets (the brief meant "misses its targets"). Optional fix.
- Salary lesson (interview 07) needs a "numbers are approximate; check current postings" disclaimer (flagged in its outline).

## Notes for authors
- The validator reuses one DB per dataset for the whole run. DDL questions must `DROP ... IF EXISTS` and use unique `_q` table names.
- `ecommerce.orders.order_id` and `hr.employees.employee_id` contain exact duplicate rows (deliberate), so use DISTINCT or dedupe first.

## Lesson learned
- Parallel agents collided in a shared /tmp dir. Tell each agent to use its own scratch dir (e.g. /tmp/<task-slug>/).

## Git
Everything is committed on master and the build is green. Outlines and briefs in `.work/` are tracked; `.work/verify` and `.work/enrich` are not.

## Working approach for next phases (user-agreed)
- **The orchestrator stays in charge.** The main session plans and dispatches and reads only short verdicts. It never touches content directly.
- **Sonnet writes outlines only** (topics, examples, traps, question specs) in `.work/outlines/`. **Haiku writes all the content** from those outlines. Don't underestimate Haiku, and don't add extra layers.
- **Selective context:** each agent gets a small task packet (its outline, its dataset's schema only, a rules excerpt, 1 golden example, the gate commands). Start every packet with the same rules text so it can be cached.
- **Strong gates:** validate, audit and lint, plus an MDX compile check (to be added). Cross-check MCQs blind. Run a sampled Haiku reviewer pass.
- **Use worktrees** for parallel UI agents. Use reusable templates, briefs and scripts wherever possible.
- **Add custom agent files or hooks only if they clearly pay for themselves.**
- **Prefer smart compaction or forking** over fresh sessions. HANDOFF.md alone doesn't carry everything.
