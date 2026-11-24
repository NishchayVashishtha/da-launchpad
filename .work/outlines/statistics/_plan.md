# Statistics module plan (master_prompt §5 Module 5)
Route: /statistics/<NN-slug>/ ; lessons dir src/content/lessons/statistics/ ; module: statistics (check `statistics` is in the content schema enum; yes per CLAUDE.md module list).

## Lessons (17, outline file = lesson slug) - all topics covered
01 descriptive-statistics | 02 distributions | 03 normal-distribution-z-scores | 04 outliers-iqr | 05 correlation-causation | 06 probability-basics | 07 bayes-theorem | 08 sampling | 09 central-limit-theorem | 10 confidence-intervals | 11 hypothesis-testing-p-values | 12 t-tests | 13 chi-square-proportions | 14 type-errors-power | 15 ab-testing-design | 16 ab-testing-analysis | 17 regression-intuition
Topic coverage check: descriptive, distributions, normal, z, IQR outliers, correlation/causation, sampling, CLT, CI, hypothesis, p-values, t-test, chi-square, Type I/II, A/B end-to-end (2 lessons: design + analysis), probability, Bayes, regression.

## Counts
- Practice: 170 total = 46 easy / 85 medium / 39 hard; 112 python, 58 text (10 per lesson, files src/content/practice/statistics/<topic>.json, topics in each outline header).
- Lesson quizzes: 85 inline MCQs (5 per lesson, written in the lesson).
- MCQ bank: 136 (8 per lesson), 5 files, ids stat-mcq-001..136 (module "statistics", topic = outline topic, section = lesson title):
  statistics-1.json lessons 01-04 (ids 001-032); statistics-2.json lessons 05-07 (033-056); statistics-3.json 08-10 (057-080); statistics-4.json 11-13 (081-104); statistics-5.json 14-17 (105-136). Mix easy/medium/hard roughly 40/45/15; options 4 each; answerIndex spread evenly 0-3 (NOT mostly 1); every wrong option = the "trap" from the outline; explanation 2 sentences; shortcut optional.
- Interview: src/content/interview/statistics.json 25 items (see _interview-bank.md).
- Delete src/content/mcq/_sample.json only if the orchestrator says so (sample id sample-mcq-1 is deletable).

## HARNESS FACTS (checked)
- NO scipy in .venv or the Pyodide harness: only numpy + pandas + python math. Use `math.erf/erfc` for normal CDF/p-values. t and chi-square p-values for df>1: do NOT compute; ask for the statistic, df, or use critical-value tables in explanation. Two-sided normal p = math.erfc(abs(z)/math.sqrt(2)). chi-square df=1 p = math.erfc(math.sqrt(chi2/2)).
- Python questions: `load("food_delivery","deliveries")` etc.; assign `result` (round to stated dp; scalars -> {"value": x}; dicts and DataFrames supported by serialize).
- CSV is DIRTY for money-like text columns (str dtype): ecommerce.orders.total_amount, food_delivery.deliveries.order_value, hr.salaries.annual_ctc, retail.sales.net_amount_inr, fintech.transactions.amount, marketing.ad_spend.spend_inr, subscription.subscriptions.price_inr. AVOID them except in outlier lesson (ad_spend) where cleaning is the point: CLEAN = pd.to_numeric(s.astype(str).str.replace(r"[₹,\s]","",regex=True), errors="coerce").
- Clean numeric columns safe to use directly: food_delivery.deliveries distance_km, actual_minutes (NaN for cancelled: dropna), delay_minutes, promised_minutes; ratings.*_rating; hr.performance_reviews all; marketing.ab_test_results converted (revenue_inr NaN->0 check), clicks.cost_inr; fintech is_flagged/status; subscription.subscriptions dates.
- Standard A/B CLEAN helper (writers paste into each solution): df=load("marketing","ab_test_results").drop_duplicates(); both=df.groupby("user_id")["variant"].nunique(); df=df[~df.user_id.isin(both[both>1].index)] -> 11,990 rows (control 6,016; treatment 5,974).
- Random-based solutions: use np.random.default_rng(seed) or DataFrame.sample(random_state=); results are deterministic per pandas/numpy version, so validate runs in both .venv and Pyodide if possible; if Pyodide numpy differs, prefer deterministic questions. Writers: prefer non-random alternatives when a question is flaky; PCG64 default_rng streams are stable across numpy versions, DataFrame.sample is stable per pandas version (acceptable).
- Instructor-note vs data mismatch: the marketing A/B Desktop segment is -1.4pp, Mobile +2.3pp in the cleaned data (notes say +1.8 / +0.3). Always use script output.

## Numeric answers that MUST come from a script, not a model
Any python question: use `npm run validate -- --file ... --fill`, then eyeball. For `text` {value} questions the writer must compute with a python one-liner and paste: normal-risk items: SD of 4,8,6,5,7 (1.58); binomial SD (2.30); Poisson P(0)=0.0498; 2.28% tail; Bayes posteriors (4.3, 31.3, 15.5, 1998 false flags); chi-square/t/Welch examples (12-10 Welch t=1.77); sample size n=3843, CI margins 0.0294, n=1068 for +-3pp; family-wise 0.226/0.642; power by simulation; every pp/CI/p/z in lessons 15-16 (facts: control 10.57%, treatment 11.72%, z 1.99, p 0.046, CI [0.02,2.27]pp, SRM chi2 0.147, n/arm 7006, subscription trial->paid 36.06%). Other verified facts: deliveries delivered n=14,407 mean 44.87 SD 13.16 SE 0.110; z(70)=1.91 (97.2th pct); Rain-Clear diff 5.40 min Welch t 13.83; distance slope 4.39 intercept 26.81 R2 0.49 pred(8km)=61.9; late rate (delay>10) 18.07%; corr(distance,minutes)=0.70.
Scratch fact script: /tmp/outline-stats/facts.py (copy to writers if needed; run with .venv/bin/python from repo root). Orchestrator: recommend writers run a `scripts`-style check for every text {value} (one python -c each) before saving.
Some outline cells say "(script)" or hold approximate numbers: treat as placeholders to be recomputed.

## Writer task split (9 Haiku tasks, 1-2 lessons + practice + MCQ chunk each)
T1: lessons 01+02 (+ practice descriptive, distributions; 20 q) 
T2: lessons 03+04 (normal, outliers; 20 q) 
T3: lessons 05+06 (correlation, probability; 20 q) 
T4: lessons 07+08 (bayes, sampling; 20 q) 
T5: lessons 09+10 (clt, ci; 20 q) 
T6: lessons 11+12 (hypothesis, ttest; 20 q) 
T7: lessons 13+14 (chisquare, errors; 20 q) 
T8: lessons 15+16 (A/B design + analysis; 20 q) - give most review; needs sqlite + facts
T9: lesson 17 (regression, 10 q) + interview bank (25 items)
MCQ files: each task writes the MCQ lines for its lessons into a per-task partial file (e.g. src/content/mcq/statistics-tN.json with unique id ranges) to avoid edit conflicts; ids allocated per lesson: stat-mcq-<lessonNN>-<k> (k=1..8) is simpler than global numbering, use that instead of 001-136. File grouping then = per task (9 files statistics-t1..t9), ignoring the 5-file split above. (Orchestrator may merge later.)
Sequencing: T1-T7 any order; T8 after T6/T7 if consistent wording of p-values wanted (not blocking).

## Extra assets
- Optional: statistics formula cheat sheet (Module 10) will reuse FormulaCards; no notebook required.
- links.json: all lessons use existing ids khan-stats, pandas-docs, numpy-docs, matplotlib-docs. No additions needed.
- Quiz and PracticeSet: PracticeSet in each lesson uses `topic="<topic>" module="statistics"`.

## Open questions
- Confirm Pyodide numpy/pandas version determinism for sample()/default_rng questions.
- Confirm `language: text` with `{value}` expectedOutput is graded numerically in the UI.
- Whether to reduce to ~14 lessons (merge 06+07, 13+14) if time is tight.
