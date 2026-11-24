# Business module plan (master_prompt §5 Module 6)
Route: /business/<NN-slug>/ (lessons dir src/content/lessons/business/, module: business). Cases: src/content/cases/<id>.mdx -> /business/cases/<id>/ (collection `cases`, page src/pages/business/cases/[id].astro, id = file name; schema title, industry, difficulty, type enum case-study|mock-case|take-home, estimatedMinutes, draft). Check `business` is in the lessons module enum (per CLAUDE.md yes); the cases index/hub page /business/ should list cases (orchestrator check).
Read first: _facts.md (all numbers verified; re-verify with sqlite3 / validate --fill).

## Lessons (14)
01 kpis-metrics-by-industry | 02 fintech-and-healthcare-kpis | 03 metric-trees | 04 funnel-analysis | 05 cohort-retention | 06 churn-analysis | 07 unit-economics-ltv-cac-aov | 08 root-cause-analysis | 09 metric-definition-questions | 10 dashboard-requirement-gathering | 11 data-storytelling | 12 guesstimates | 13 data-ethics-privacy | 14 case-study-method
Coverage vs master_prompt: KPIs by industry (01,02), metric trees (03), funnel (04), cohort/retention (05), churn (06), LTV/CAC/AOV/conversion (07), RCA (08), metric definition (09), dashboard requirements (10), storytelling (11), guesstimates (12), ethics/privacy (13), + case method (14) and 25 cases.

## Counts (practice, files src/content/practice/business/<topic>.json)
kpis 10 (T0) | fintechkpi 12 (8 sql) | metrictree 8 (2 sql) | funnel 10 (6 sql) | cohort 10 (7 sql) | churn 10 (6 sql) | unitecon 10 (5 sql) | rca 12 (5 sql) | metricdef 10 | dashreq 8 | story 8 | guess 10 | ethics 8 | casemethod 6 = 132 total (SQL 39 / text 93).
Difficulty approx: easy 37 / medium 55 / hard 40 (follow table cells; adjust honestly). Ids business-<topic>-NNN. `module` field for practice entries: "business"; check src/content.config.ts practice schema accepts module business and language text/sql (orchestrator).
Text questions: language "text", dataset "none", `solution` markdown model answer, expectedOutput {value} only where a number is given. Every {value} computed by a python one-liner before saving.
SQL: dedupe per _facts.md; run `npm run validate -- --file ... --fill` and eyeball against facts; fix questions whose output differs rather than the facts. Note SQLite differences (strftime, julianday) in explanations.
MCQ: none required (lessons have 5-MCQ quiz). Optional later: interview bank business.json (not in this plan).
Interview bank: lesson InterviewQs only.

## Cases: 25 (see cases.md): files src/content/cases/<id>.mdx, ids in cases.md. Fintech 10, Health 7, Consulting 8. Difficulty mix 4 easy / 16 medium / 5 hard. All type case-study.
Case MDX body H2s (writers keep consistent): Problem | Data you have | Approach | Step-by-step solution | Key insight | Recommendation | What a weak answer looks like. Show SQL as fenced code in solution with real output tables (run sqlite3). Include a collapsed-style heading? (no special component; just headings).

## Extra assets
- Optional: downloadable "RCA checklist" and "Metric definition template" as one-page md within lessons 08/09 (no files needed).
- links.json: existing ids only (alex-the-analyst, kaggle-learn, mode-sql, sqlite-docs, power-bi-docs). OPEN: official DPDP Act page for lesson 13 (orchestrator may add to links.json).

## Writer tasks (8 Haiku tasks; each has its lessons + practice; cases split in T6-T8 plus the two largest lessons are separate)
T1: lessons 01 + 02 (+ kpis, fintechkpi; 22 q) - needs fintech schema; most review
T2: lessons 03 + 04 (+ metrictree, funnel; 18 q) - ecommerce + subscription schemas
T3: lessons 05 + 06 (+ cohort, churn; 20 q) - subscription schema
T4: lessons 07 + 08 (+ unitecon, rca; 22 q) - marketing + ecommerce + fintech schemas; most review
T5: lessons 09 + 10 + 11 (+ metricdef, dashreq, story; 26 q text) 
T6: lessons 12 + 13 + 14 (+ guess, ethics, casemethod; 24 q text) AND no cases
T7: cases F1-F10 (fintech; 10 mdx) - fintech schema
T8: cases H1-H7 + C1-C8 (15 mdx; split into T8a health 7 + T8b consulting 8 if budget allows -> total 9 tasks)
Sequencing: T14 lesson links to case ids so cases ids fixed in cases.md. T7/T8 can run any time. Run validate for lesson practice files; for cases run `npx astro sync` + audit.
Quality: remind writers all data brand names fictional (DesiCart, NammaPay, FoodKart); health examples only aggregate and fictional; no legal advice in lesson 13.
