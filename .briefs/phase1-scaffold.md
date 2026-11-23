# Phase 1 brief: site framework (DA Launchpad)

Product spec: /home/dividh/nishchay/da-launchpad/master_prompt.md. You own the SITE FRAMEWORK only. Never touch scripts/generate_data/**, public/data/**, src/data/datasets.json (dataset agent). Content (lessons/questions) comes later from other agents following the CLAUDE.md you write.

Stack: Astro (static) + MDX + React islands + Tailwind v4 + TS. Pagefind (postbuild) with Ctrl/Cmd+K modal. sql.js (wasm self-hosted in public/). Pyodide lazy from jsDelivr only on pages with Python practice (pandas). PWA: hand-written SW (precache shell + built pages, runtime cache for data + Pyodide CDN), manifest, icons. `base` via env SITE_BASE; base-aware `url()` helper everywhere. Dark/light toggle (persisted, no flash). Mobile-first, accessible, print stylesheet.

## 1. Content collections (Zod)
- lessons: MDX src/content/lessons/<module>/<NN-slug>.mdx. Frontmatter: title, description, module (enum), order, estimatedMinutes, objectives[], tags[], draft?.
- practice: JSON arrays at src/content/practice/<module>/<topic>.json (each element an entry): id, module, topic, difficulty easy|medium|hard, language sql|python|excel|dax|text, question (md), dataset (id or "none"), hint, solutionSql?/solutionCode?, solution? (md), expectedOutput ({columns,rows} or {value}; optional for non-code), orderMatters? (default false), explanation, commonMistake, interviewFrequency low|medium|high, estimatedMinutes, tags. Global unique ids.
- interview: JSON arrays src/content/interview/<category>.json: id, category, question, whatInterviewerIsTesting, modelAnswer (md), followUps[], commonMistakes[], difficulty.
- projects: MDX, frontmatter = Project schema (id, title, businessProblem, datasetDescription, skillsUsed, steps[], deliverables, readmeTemplate, interviewTalkingPoints[], extensions[], estimatedHours); body = full build guide.
- flashcards: JSON arrays id, topic, front, back.
- glossary: JSON arrays id, term, definition, example?, related?[].
- mcq: JSON arrays id, module, topic, section?, difficulty, question, options[], answerIndex, explanation, shortcut?.
- cases: MDX (title, industry, difficulty, type case-study|mock-case|take-home, estimatedMinutes).
- tests: JSON id, title, durationMinutes, questionIds[].
One tiny clearly-marked sample per collection (deletable later). One sample lesson start-here/00-sample.mdx, draft: true, demonstrating every component. Do NOT write real module content.
Module slugs in order: start-here, excel, sql, power-bi, python, statistics, business, interview, projects, job-search, cheat-sheets.

## 2. Layout
Sidebar (modules -> lessons, collapsible, current highlighted, completion ticks), breadcrumb, prev/next, "On this page" TOC, reading time, header (search, theme, Dashboard/Profile/Practice/Tools). Module index /<module>/ (lessons + practice counts). Lesson route /<module>/<slug>/.

## 3. MDX components (auto-mapped, no imports needed)
Tip, Warning, InterviewAlert, RealWorld, CommonMistake; `<PracticeSet topic module />` or `<PracticeSet ids />` (grouped by difficulty; hint/solution toggles; Mark done w/ timestamp; bookmark; sql: editor + Run via sql.js on public/data/sqlite/<dataset>.sqlite, result table, Compare with expected — order-insensitive unless orderMatters, numeric tol 1e-6, show diff; python: Pyodide, helper `load(dataset, table)` -> DataFrame from public/data/csv/<dataset>/<table>.csv, code assigns `result`; record pass/fail to progress). `<Quiz questions={[{q, options, answer, explanation}]} />`. `<InterviewQ q="...">md</InterviewQ>`. `<FurtherReading ids={[...]} />` from src/data/links.json (stable official/home pages only for resources in master_prompt §7). `<SqlPlayground dataset query />`. `<FormulaCard title>`. `<Mermaid>`. `<Download href label />` base-aware. Notes box + "Mark lesson complete" auto-appended to every lesson.

## 4. Progress store src/lib/progress.ts
Lessons done, questions done/pass/fail + timestamps, quiz scores, bookmarks, notes, study-hours log, streak, weekly goals, mock test history, flashcard Leitner boxes, application tracker records, profile. Export/Import JSON (Dashboard + Profile).

## 5. Pages
Dashboard (/): today's task from src/data/plan.json ([{week, day, title, tasks[], links[]}]), progress ring, per-module bars, streak, weekly hours SVG chart, hours logger, revision cards (due flashcards + weak topics), weak-topic detector, quick links. /profile/ (seeded from src/data/profile.json with user's values from master_prompt §0; localStorage). /practice/ hub with filters (module, topic, difficulty, done, bookmarked). /bookmarks/. /datasets/ and /datasets/<id>/ rendering src/data/datasets.json, shape: [{id, title, description, tables:[{name,rowCount,description,columns:[{name,type,description,nullable,example}]}], relationships:[{from,to,type}], qualityIssues[], er (mermaid), downloads:{sqlite, zip, csv[]}, signals[]}] — paths relative, no leading slash; signals are instructor notes (show collapsed or hide). Robust if file missing (fallback src/data/datasets.test.json). /playground/ with dataset picker, table list, schema viewer.
Tool pages (flashcards, tracker, resume, mock interview, aptitude, glossary, sql tests) come later at /tools/<name>/: don't link them yet, no "coming soon"; document in CLAUDE.md (src/data/tools.json may list them with an `enabled` flag).

## 6. Scripts
dev, build (astro build && pagefind && sw gen), preview, validate (scripts/validate.mjs: SQL solutions via sql.js in Node vs public/data/sqlite, shared comparator with browser; Python via .venv/bin/python (fallback python3) + scripts/py_harness.py providing load() and serializing result (DataFrame->{columns,rows}, Series->frame, scalar/list/dict->{value}), batched per process; exit 1 on failures; flags --file <path>, --fill (write missing expectedOutput, print what was filled), --only sql|python). audit (scripts/audit.mjs: every non-draft lesson has these 10 H2 headings in order exactly: "Learning objectives", "Why this matters for a Data Analyst job", "Concept", "Worked examples", "Common mistakes", "Practice questions", "Mini quiz", "Interview angle", "Key takeaways", "Further reading"; flag placeholders (lorem, TODO, coming soon, TBD, [FILL]); duplicate ids across collections; FurtherReading ids exist; PracticeSet refs resolve; internal links resolve; print counts per collection/module/difficulty; write reports/counts.json).

## 7. CLAUDE.md (repo root)
Rules (original content, simple English, India-flavored fictional data, no placeholders), folder map, every schema with a full example, lesson template with the 10 headings + skeleton showing component usage, practice conventions (SQLite dialect — flag differences; results ≤50 rows via LIMIT; deterministic ORDER BY when orderMatters; Python assigns `result`), how to run validate --fill/--file and audit, quality checklist, rule that parallel agents edit only assigned files. Also .gitignore (node_modules, dist, .venv, .astro, __pycache__), README stub.
