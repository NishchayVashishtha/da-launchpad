# MASTER PROMPT: Build "DA Launchpad", a complete self-contained Data Analyst study, practice and job-prep website

You are a senior full-stack engineer, data analytics instructor and career coach in one. Build a personal, static, offline-capable website that is the ONLY resource one fresher needs to go from zero to a job-ready Data Analyst in India. All learning content must be in simple, clear ENGLISH.

Do not ask me questions unless you are blocked. Make sensible decisions, write the full content yourself, and keep going phase by phase until everything is complete.

---

## 0. MY PROFILE (use it to personalize content)

Edit these values before running. If any value is still "[FILL]", use a sensible default and keep it editable in `src/data/profile.json`.

- Name: Nishchay Vashishtha
- Degree / branch / graduation year: 2027 BteCH CSE Core 
- Coding level today (none / basic / intermediate): basic
- Hours I can study per day: 5-6
- Target cities / remote: Any WITHIN INDIA
- Target industries (e.g., e-commerce, fintech, healthcare, consulting): Any but first prio Fintech, then health, then Consulting then etc…
- Current strengths / hobbies / any internship, college project or work experience: current internship in ui ux but not interested in that
- Target timeline to first job: as fast as possible
- Long-term goal: start as Data Analyst, move to Data Engineer or Analytics Engineer in 2-3 years.

Personalization rules:
- Build a "Profile" page that stores these values in localStorage and in profile.json.
- The HR interview module must generate personalized answers ("Tell me about yourself", "Why data analytics?", "Why should we hire you?", "Strengths and weaknesses", "Where do you see yourself in 5 years?") by inserting my profile values into well-written templates. Also provide 2 fully written sample answers using a fictional fresher profile.
- The resume module must produce a resume draft from my profile.

---

## 1. TECH STACK AND ARCHITECTURE

- Framework: Astro (static output) with MDX content collections + React islands for interactive widgets. Tailwind CSS for styling.
- No backend, no database server, no paid APIs. Everything runs in the browser and deploys free on GitHub Pages or Netlify. Include deployment instructions in README.
- Search: Pagefind (or equivalent) for full-text search across all content.
- In-browser SQL playground: sql.js (SQLite compiled to WebAssembly) with preloaded practice databases (see Section 4). Every SQL practice question has a "Run" editor, a "Show hint", a "Show solution" and a "Compare my output with expected output" button.
- Optional in-browser Python runner using Pyodide (lazy-loaded, with pandas) for Python practice questions. If it makes the site too heavy, load it only on the Python module pages.
- Progress and data storage: localStorage with an "Export progress as JSON" and "Import progress" button.
- Content lives in `/src/content/**` as MDX/Markdown/JSON, never hard-coded in components, so I can edit it easily.
- Offline support via a service worker (PWA). Must work well on a phone.
- Add a `CLAUDE.md` (or equivalent agent instructions file) in the repo root with the project rules, folder map, content schemas and quality checklist, so future sessions stay consistent.

---

## 2. UX AND DESIGN REQUIREMENTS

- Clean, modern, minimal, readable. Dark and light mode. Mobile-first and fully responsive. Print-friendly stylesheet for cheat sheets.
- Left sidebar with modules and lessons, breadcrumb, "Next lesson / Previous lesson", "On this page" table of contents, reading-time estimate.
- Global search (Ctrl/Cmd+K).
- Dashboard (home page): today's task from my 12-week plan, overall progress ring, per-module progress bars, streak counter, weekly study hours chart, upcoming revision cards, quick links to "Practice SQL", "Mock Interview", "Application Tracker".
- Every lesson page follows the same template:
  1. Learning objectives
  2. Why this matters for a Data Analyst job
  3. Concept explained in simple language with analogies
  4. Worked examples (step by step, with output)
  5. Common mistakes
  6. Practice questions (Easy, Medium, Hard) with "Show hint" and "Show solution" toggles and a "Mark as done" checkbox
  7. Mini quiz (5 MCQs with explanations)
  8. Interview angle: 3-5 real interview questions on this topic with model answers
  9. Key takeaways (5 bullets)
  10. Further reading (links, see Section 12)
- Callout components: Tip, Warning, Interview Alert, Real-world Example, Common Mistake.
- Accessible: keyboard navigation, proper contrast, semantic HTML.

---

## 3. CONTENT SCHEMAS (enforce with Zod or JSON schema)

Practice question:
`id, module, topic, difficulty (easy|medium|hard), question, dataset, hint, solutionSql/solutionCode, expectedOutput, explanation, commonMistake, interviewFrequency (low|medium|high), estimatedMinutes, tags`

Interview question:
`id, category, question, whatInterviewerIsTesting, modelAnswer, followUps[], commonMistakes[], difficulty`

Project:
`id, title, businessProblem, datasetDescription, skillsUsed, steps[], deliverables, readmeTemplate, interviewTalkingPoints[], extensions[], estimatedHours`

Flashcard:
`id, topic, front, back`

---

## 4. DATASETS (generate them yourself, no external dependency)

Write deterministic Python scripts (fixed random seed) in `/scripts/generate_data/` that create realistic, messy, India-flavored fictional datasets and export both CSV (for Excel and Power BI downloads) and SQLite (for the in-browser playground). Use fictional brand names, never real company data. Include deliberate data quality problems (nulls, duplicates, wrong data types, inconsistent text casing, outliers, date format mix-ups) for cleaning practice.

Datasets (each 5k-100k rows, sized sensibly for the browser):
1. E-commerce: customers, orders, order_items, products, payments, returns
2. Food delivery: restaurants, deliveries, ratings, delivery_partners, promo_usage
3. HR: employees, departments, salaries, attrition, performance_reviews
4. Fintech / UPI-style transactions: users, merchants, transactions, failed_transactions
5. Subscription app: users, subscriptions, events (for funnel, retention, cohort, churn)
6. Marketing: campaigns, ad_spend, clicks, conversions, A/B test results
7. Retail store sales: stores, sales, inventory, targets

Provide a data dictionary page for each dataset (columns, types, relationships, ER diagram).

---

## 5. MODULES AND REQUIRED DEPTH

Write ALL content in full. No placeholders, no "coming soon", no lorem ipsum. Quality over padding, but be thorough.

### Module 0: Start Here
- What a Data Analyst does day to day (with a realistic day-in-the-life), job titles to apply for (Data Analyst, Junior Data Analyst, MIS Executive, Reporting Analyst, Business Analyst, BI Analyst, Operations Analyst, Product Analyst), and how they differ.
- Data Analyst vs Data Engineer vs Data Scientist vs Business Analyst (comparison table, similarities and differences).
- Indian job market overview and realistic fresher expectations (salary ranges described as approximate).
- The 12-week plan, day-by-day for the first 4 weeks and week-by-week after, adjustable to my study hours.
- How to study effectively: active recall, spaced repetition, project-first learning, how to avoid tutorial hell.
- Tool setup guide (Excel, Power BI Desktop, Python/Anaconda or VS Code, Git, GitHub).

### Module 1: Excel for Data Analysis
Topics: interface and shortcuts, data types, cleaning (TRIM, CLEAN, Text to Columns, Remove Duplicates, Find & Replace, Flash Fill), logical functions (IF, IFS, AND, OR), lookup functions (VLOOKUP, HLOOKUP, XLOOKUP, INDEX-MATCH), SUMIFS/COUNTIFS/AVERAGEIFS, text and date functions, dynamic arrays (FILTER, UNIQUE, SORT), pivot tables and pivot charts, slicers, conditional formatting, data validation, charts, Power Query basics, dashboard building, what-if analysis, common Excel test tasks.
Include downloadable practice workbooks (generated by script) and 40+ practice tasks.

### Module 2: SQL (the most important module; build it deepest)
Topics in order: databases and tables, SELECT, WHERE, operators, ORDER BY, LIMIT, DISTINCT, NULL handling, aggregate functions, GROUP BY, HAVING, CASE WHEN, string functions, date functions, joins (INNER, LEFT, RIGHT, FULL, SELF, CROSS, anti-join), subqueries, CTEs, set operations, window functions (ROW_NUMBER, RANK, DENSE_RANK, LAG, LEAD, running totals, moving averages, NTILE, FIRST_VALUE), data cleaning in SQL, deduplication, pivoting with CASE, query optimization basics (indexes, execution thinking), views, basic DDL/DML.
Then "SQL Interview Patterns" lessons: second/Nth highest value, top N per group, running total, month-over-month growth, YoY, retention and cohort analysis, funnel analysis, consecutive days/streaks (gaps and islands), duplicates, median in SQL, customers who never ordered, sessionization, RFM segmentation, percent of total, and A/B test summary queries.
Requirements: minimum 200 original practice questions (about 70 easy, 80 medium, 50 hard) plus 10 full timed "SQL screening tests" (5 questions each, 45 minutes). Write original problems on my datasets. Do NOT copy problem text from LeetCode, DataLemur, StrataScratch or any other site; only mirror the common patterns.
Note that SQL dialect differences (MySQL / PostgreSQL / SQL Server) must be called out in a comparison table. The playground uses SQLite; flag syntax that differs.

### Module 3: Power BI (plus a Tableau comparison lesson)
Topics: BI concepts, Power BI Desktop and Service, getting data, Power Query (cleaning and shaping), data modeling (star schema, relationships, cardinality, filter direction), DAX (calculated columns vs measures, CALCULATE, FILTER, ALL, time intelligence, SUMX, RANKX, variables), visuals and when to use each, formatting, drill-through, tooltips, bookmarks, slicers, row-level security basics, publishing and sharing, performance tips, dashboard design principles and storytelling.
Include step-by-step guided exercises (each with a downloadable CSV set), 3 full dashboard walkthroughs with business questions, 40+ DAX practice questions with answers, and a "Power BI practical test" simulation (given dataset + business brief + 90 minutes + evaluation rubric).

### Module 4: Python for Data Analysis
Topics: Python basics (variables, types, loops, functions, list/dict comprehension, file handling), NumPy, pandas (Series, DataFrame, indexing, loc/iloc, filtering, sorting, groupby, merge/join, pivot_table, apply, string and datetime handling, missing values, duplicates, outliers), data cleaning workflow, EDA workflow, visualization (matplotlib, seaborn), basic regression overview, Jupyter notebooks, Git and GitHub basics.
Include 120+ practice questions with solutions, 10 mini exercises on messy datasets, and a reusable EDA checklist. Provide downloadable `.ipynb` starter notebooks.

### Module 5: Statistics and Probability for Analysts
Topics: descriptive stats, distributions, normal distribution, z-scores, outliers (IQR), correlation vs causation, sampling, central limit theorem, confidence intervals, hypothesis testing, p-values, t-test, chi-square, Type I/II errors, A/B testing end to end (design, sample size intuition, interpreting results, pitfalls), probability basics, Bayes theorem intro, regression intuition.
Each concept uses plain-English explanation, an example, a formula card and 10 practice questions. Include 100+ MCQs and a statistics interview Q&A bank.

### Module 6: Business Thinking and Analytics Case Studies
Topics: KPIs and metrics by industry (e-commerce, fintech, SaaS, food delivery, healthcare, HR), metric trees, funnel, cohort and retention, churn, LTV, CAC, AOV, conversion, root cause analysis framework ("Why did sales drop 15%?"), metric definition questions, dashboard requirement gathering, data storytelling and presenting insights to non-technical stakeholders, estimation/guesstimate basics, data ethics and privacy basics.
Include 25 written case studies with step-by-step model solutions.

### Module 7: Interview and Screening Preparation (all rounds in one place)
Create a dedicated hub with these sections:
1. **How hiring works**: stages, typical timelines, what each round tests (online assessment, SQL test, aptitude, take-home, technical, case, manager, HR).
2. **Aptitude and screening tests**: quantitative aptitude (percentages, ratios, averages, profit and loss, time and work, probability, permutations), logical reasoning, data interpretation (tables, bar/line/pie charts, caselets), verbal basics. 300+ questions with solutions in total, timed practice mode with score and review, and shortcut tricks.
3. **Technical interview banks** with model answers: SQL (100+), Excel (60+), Power BI/DAX (60+), Python/pandas (80+), Statistics (60+), Data warehousing and ETL basics for analysts (30+), Behavioral-technical hybrid questions.
4. **Case-study rounds**: framework, 10 mock cases, evaluation rubric.
5. **Take-home assignment guide**: how to structure analysis, what hiring managers look for, a sample assignment with a model submission.
6. **Live SQL / Excel / Power BI test strategy**: time management, how to think aloud, what to do when stuck.
7. **HR and behavioral round**: 60+ questions with model answers (STAR method), personalized from my profile, covering: Tell me about yourself, Why this role/company, strengths/weaknesses, failure and conflict stories, handling pressure, teamwork, gap in education, relocation, shift work, notice period, expected salary, "Do you have any questions for us?" (with good questions to ask).
8. **Salary and offer**: fresher salary negotiation scripts, evaluating offers (CTC vs in-hand, bond, variable pay), red flags in job offers and fake-job/scam warnings.
9. **Mock interview mode**: random question generator by category with a countdown timer, a self-rating form, and a score history chart. Also a "Talk through your project" practice script.
10. **Last 7 days and last 24 hours checklists**.

### Module 8: Projects Hub (unique, portfolio-grade)
Provide 8 detailed projects, each following the Project schema, with a full build guide (problem framing, data cleaning, SQL analysis, Python EDA, dashboard, insight writing, recommendations), a README template, screenshots-to-capture checklist, a 2-minute pitch script and 10 likely interview questions about the project:
1. Food delivery: delivery time delays and customer rating drivers
2. E-commerce: sales performance, returns and customer segmentation (RFM)
3. Subscription app: funnel, cohort retention and churn analysis
4. HR attrition analysis and dashboard
5. UPI/fintech transactions: failure-rate and anomaly analysis
6. Marketing A/B test and campaign ROI analysis
7. Retail store performance and inventory optimization dashboard
8. A "capstone": end-to-end analytics case combining SQL + Python + Power BI + a written executive summary

Also include: how to choose and present projects, how to avoid tutorial-copy projects, how to customize a project to make it unique, GitHub repo structure, how to publish a Power BI report publicly, how to write LinkedIn posts about projects.

### Module 9: Job Search Toolkit
- Fresher resume guide, ATS rules, a one-page template, 30 strong bullet examples using the Action + Task + Result + Number formula, and a resume builder form that exports a clean printable page.
- LinkedIn profile checklist with headline, about section and project post templates.
- GitHub profile and portfolio website guide.
- Where to apply in India (job portals, startup boards, company career pages, off-campus drives), with a daily application routine.
- Referral and cold-outreach message templates (connection request, follow-up, thank-you, asking for referral).
- Application tracker (add/edit/delete, status: Applied, Screening, Interview, Offer, Rejected; filters; follow-up reminders; export CSV).
- Rejection handling and iteration loop.
- First 90 days on the job, and the roadmap from Data Analyst to Data Engineer / Analytics Engineer (skills: advanced SQL, Python, data modeling, Airflow, Spark, a cloud platform, dbt) with a 12-month learning plan.

### Module 10: Cheat Sheets and Glossary
Printable one-pagers: SQL, Excel functions, pandas, matplotlib/seaborn, DAX, statistics formulas, A/B testing checklist, EDA checklist, KPI glossary. Plus a searchable glossary of 300+ terms. Spaced-repetition flashcards (500+) with a daily review queue (Leitner-box logic).

---

## 6. PROGRESS, TRACKING AND PERSONAL TOOLS

- Per-lesson and per-question completion checkboxes with timestamps.
- Study streak, study-hours logger, weekly goals.
- Weak-topic detector: based on quiz/practice results, suggest what to revise.
- Mock test history and score trends.
- Notes feature: a personal notes box on every lesson (saved locally, exportable).
- Bookmark/favorite any question.

---

## 7. SOURCES, ORIGINALITY AND COPYRIGHT RULES

Base the curriculum structure, topic order and teaching approach on the best publicly available learning resources and interview patterns, such as: SQLBolt, Mode SQL Tutorial, LeetCode SQL 50 (patterns only), DataLemur and StrataScratch (patterns only), Microsoft Learn PL-300 path, Kaggle Learn (Python, Pandas, Data Visualization), Alex The Analyst's Data Analyst Bootcamp (topic coverage), CampusX, Ankit Bansal's SQL interview series, Chandoo and ExcelIsFun, Khan Academy statistics, official docs for pandas, SQLite, PostgreSQL, DAX Guide and Microsoft Excel support.
- All explanations, examples, questions, case studies and answers must be ORIGINAL text written by you. Never copy or closely paraphrase copyrighted material, problem statements or video content.
- In "Further reading", link only to stable, well-known official pages or home pages of the resources above. Do not invent deep URLs. Add a note "Verify link before use" in the README, and keep all links in one `links.json` so they are easy to update.

---

## 8. QUALITY GATES (mandatory)

1. **Run every solution.** Write a validation script (`npm run validate`) that executes EVERY SQL solution against the SQLite datasets and every Python solution in a test environment, and fails if the output does not match `expectedOutput`. Fix all failures before moving on.
2. Validate all content files against the schemas.
3. Check for broken internal links and empty sections.
4. Lighthouse performance and accessibility score of 90+ on key pages.
5. Content audit: each lesson must contain all 10 template sections; no placeholder text anywhere.
6. Keep reading level simple: short sentences, define every term the first time it appears.

---

## 9. BUILD PLAN (follow in order, commit after each phase)

- Phase 1: Project scaffold, design system, layout, search, dark mode, PWA, progress system, profile page, `CLAUDE.md`, dataset generators and SQL playground. Module 0 complete.
- Phase 2: Module 2 (SQL) complete with all practice questions, SQL tests and validation script.
- Phase 3: Module 1 (Excel) and Module 3 (Power BI).
- Phase 4: Module 4 (Python) and Module 5 (Statistics).
- Phase 5: Module 6 (Business thinking) and Module 7 (Interview and Screening hub, including mock mode and aptitude practice).
- Phase 6: Module 8 (Projects), Module 9 (Job toolkit, resume builder, tracker), Module 10 (cheat sheets, glossary, flashcards).
- Phase 7: Polish, validation, accessibility, performance, README with setup and deployment steps, and a final content audit report listing counts of lessons, questions, interview Q&As, flashcards and projects against the targets above.

At the end of every phase, print a short status report (what is done, counts, what is next) and continue automatically. If a target count cannot be met in one pass, continue in additional passes until it is. Do not stop at a skeleton or sample content; the finished site must contain the complete material.

---

## 10. DEFINITION OF DONE

- Site builds with `npm run build` and runs with `npm run dev`; deploys to GitHub Pages with documented steps.
- All modules above are complete with the required depth and counts.
- All SQL and Python solutions pass validation.
- Dashboard, tracker, mock interview mode, resume builder, flashcards and search all work offline on mobile and desktop.
- A new learner could follow only this site, with no outside resource, from zero to interview-ready.
