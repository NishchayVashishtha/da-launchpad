# Interview module plan (hub sections 1,4,5,6,8,10 + banks)
## Conventions
- Lessons: src/content/lessons/interview/<NN-slug>.mdx, module `interview`, slug = outline filename. Route /interview/<slug>/. 10 H2s as CLAUDE.md. Outline files here use the shape of FORMAT.md (some lessons adapt Concept/Worked examples; see each file's "Content shape" note).
- Practice ids: `interview-pr-<topic>-NNN` (NOT `interview-<category>-NNN`, which is reserved for interview banks). Files: src/content/practice/interview/<topic>.json. Topics: hiring, aptitude, case, takehome, sampletake, live, offer, final. Language text/excel need `solution` md; SQL ones need solutionSql + validate --fill.
- Bank ids: existing `interview-stats-001..025` (statistics.json) and `sample-int-1` (_sample.json). New: interview-sql-NNN, interview-excel-NNN, interview-powerbi-NNN, interview-python-NNN, interview-stats-026..060, interview-dw-NNN, interview-hybrid-NNN, interview-hr-NNN (3-digit). Fields category values: sql, excel, power-bi, python, statistics, data-warehousing, hybrid, hr. Verify with `grep -h '"id"' src/content/interview/*.json | sort | uniq -d` (must be empty).
- Mock cases: src/content/cases/mock-case-NN-<slug>.mdx (outline in mock-cases.md). Case frontmatter has no id; ids come from filename.
- Interview bank files hold JSON arrays. Writers write in chunks of <=40 items per task; each task its own file (chunk files below) and the orchestrator concatenates? NO: to avoid shared files, large banks are split into per-chunk files. The loader globs src/content/interview/*.json (check src/content.config.ts before writing; if the category is read from each item, multiple files per category are fine). Chunk file names: <category>-a.json, -b.json etc. (statistics-2.json already single).
- Shared guardrails: the sample file _sample.json is deletable (orchestrator). Datasets for SQL examples are fictional; run queries on public/data/sqlite/<id>.sqlite.
- Checks per task: `npx astro sync`, `npm run validate -- --file <practice file>` for SQL practice, `npm run audit`. Bank JSON must parse (`python3 -m json.tool`).

## Lessons (8) and practice (E/M/H)
| # | slug | practice file | q count | E/M/H |
|---|---|---|---|---|
| 01 | how-hiring-works | hiring.json | 2 | 1/1/0 |
| 02 | aptitude-shortcuts | aptitude.json | 8 | 4/3/1 |
| 03 | case-round-framework | case.json | 8 | 2/4/2 (incl 3 text) |
| 04 | take-home-guide | takehome.json | 4 | 2/2/0 |
| 05 | sample-take-home-model-submission | sampletake.json | 5 | 1/2/2 |
| 06 | live-test-strategy | live.json | 5 | 1/3/1 |
| 07 | salary-offer-scams | offer.json | 5 | 1/3/1 |
| 08 | last-7-days-and-24-hours | final.json | 4 | 3/1/0 |
Totals 41 practice (counts per file in table are authoritative; writers may add 1-2 extras). SQL ones: case 5, takehome 2, sampletake 5, live 3, final 1 = 16.
Mock cases: 10 (see mock-cases.md): difficulty 1 easy, 6 medium, 3 hard as labelled there (04, 08 hard; 10 easy).
## Bank counts (total 390 new)
sql 100 (30/46/24), excel 60 (20/30/10), power-bi 60 (18/28/14), python 80 (26/37/17), statistics-2 35 (9/15/11), data-warehousing 30 (10/14/6), hybrid 25 (6/12/7), hr 60 (20/31/9). Total statistics becomes 60.
Combined with 25 existing stat items spec target 60+ met.

## Haiku writer tasks (20). Each owns only the files listed.
Lessons (reads outline + dataset schema + CLAUDE.md + .briefs/content-common.md)
- L1: lessons 01 + 02 -> src/content/lessons/interview/01-*.mdx, 02-*.mdx; practice/interview/hiring.json, aptitude.json (10 q)
- L2: lessons 03 + 04 -> 03-*.mdx, 04-*.mdx; case.json, takehome.json (12 q; fintech schema .work/schema/fintech.md)
- L3: lesson 05 -> 05-*.mdx; sampletake.json (5 q; fintech). Needs sqlite verification of every number.
- L4: lessons 06 + 07 -> 06-*.mdx, 07-*.mdx; live.json, offer.json (10 q; ecommerce + fintech schemas)
- L5: lesson 08 -> 08-*.mdx; final.json (4 q)
Cases
- C1: mock-case-01..05 (.mdx) ; C2: mock-case-06..10 (.mdx). Use matching dataset schema files (fintech, food_delivery, ecommerce, subscription, marketing | hr, retail, none).
Banks (id ranges fixed so no overlap; each own file)
- B1: sql-a.json ids 001-035 (basics, aggregation, joins) ; B2: sql-b.json 036-070 (subqueries, windows, dates, set ops) ; B3: sql-c.json 071-100 (analytics, modelling, perf, practical). Coverage rows sliced in order of the spec; counts per row from sql.md.
 Slice map: sql-a = Basics 10 + Aggregation 10 + Joins 12 + first 3 Subqueries = 35; sql-b = remaining subqueries 5, Window 14, Dates 6, Set 6, + 4 of Analytics (ids 036-070 is 35 items: 5+14+6+6+4); sql-c = remaining Analytics 10, Modelling 6, Perf 6, Practical 8 = 30 (ids 071-100).
- B4: excel-a.json 001-030 (basics, lookup, logical, aggregation, text/date partly: first 30 rows in spec order) ; B5: excel-b.json 031-060 (rest). Slice: a = basics 8 + lookup 10 + logical 5 + aggregation 7 = 30; b = text/date 6 + pivot 8 + dynamic 5 + cleaning 6 + whatif 2 + practical 3 = 30.
- B6: powerbi-a.json 001-030 (basics 8, PQ 9, modelling 10, DAX fundamentals first 3) ; B7: powerbi-b.json 031-060 (DAX fundamentals remaining 5, CALCULATE 8, time 5, visuals 5, security 3, perf 4 = 30).
- B8: python-a.json 001-040 (basics 8, control 8, errors 4, numpy 5, pandas core 10, cleaning first 5) ; B9: python-b.json 041-080 (cleaning remaining 4, groupby 8, merge 7, time 5, perf 5, viz 4, practical 4, coding 3 = 40).
- B10: statistics-2.json 026-060 (35; read statistics.json first)
- B11: data-warehousing.json 001-030 (30) + hybrid.json 001-025 (25) = 55 items (over 40 limit; Haiku-safe because short; if needed split hybrid into B12)
- B12: hr.json 001-060 (60 explicit questions; split into two files hr-a.json 001-030 and hr-b.json 031-060, tasks B12a, B12b).
Total tasks: L1-L5 (5) + C1-C2 (2) + B1-B10 (10) + B11 (1) + B12a-b (2) = 20.
Since 'category' per item is its own category string, multiple chunk files per category are fine (confirm in src/content.config.ts interview schema; if category must equal file name, rename chunks and tell orchestrator).
## Gates after writing
- JSON valid; ids unique across src/content/interview; counts per category vs spec (script: count per category, difficulty tallies); `npm run validate -- --file` per practice file; `npm run audit`; blind-check hard SQL/Python bank code by executing snippets (sqlite3 / .venv python).
- Mock-case SqlPlayground queries run on the dataset.
## Open items
- Aptitude 300+ questions + timed mode: separate agent; lesson 02 links to /tools/aptitude/ only once enabled.
- Mock interview mode, tools/hr script pages: not in scope here.
- Profile-based HR answers assume Nishchay's profile; if the site is multi-learner, keep "Replace with your own" notes.
- Practice-id prefix `interview-pr-` chosen to avoid bank id collisions.
