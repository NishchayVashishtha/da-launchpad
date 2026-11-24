# Lesson 03: Case-round framework (hub section 4)
Path: src/content/lessons/interview/03-case-round-framework.mdx | order 3 | estimatedMinutes 40
- title "Case round: a framework you can repeat" | description "A 6-step method to break down any business problem, plus a scoring rubric."
- objectives: Run the 6-step CLEAR-style framework (name it "CASE-6" below); Clarify before solving; Build a metric tree; Form and rank hypotheses; Recommend with numbers; Self-score with the rubric
- tags ["case","framework","business"]
## Concept
- Analogy: doctor visit: ask symptoms, test, diagnose, prescribe.
- CASE-6 framework: 1 Clarify (goal, metric, time window, definitions, constraints) 2 Break down (metric tree, e.g., revenue = users x orders/user x AOV) 3 Hypotheses (internal vs external; top 3, ranked) 4 Data to check (which table/column/query; segment cuts: time, city, product, channel, new vs old) 5 Findings (what each result would mean; sanity check) 6 Recommend (action, expected impact, risk, next step, metric to monitor).
- Case types: metric drop, metric improvement, launch decision (go/no-go), A/B interpretation, estimation/market sizing (Fermi), KPI definition, dashboard design.
- Time plan for 30 min: 5 clarify, 5 structure, 10 analysis, 5 recommend, 5 Q&A.
- Thinking aloud script phrases.
- Rubric (FormulaCard / table, 5 criteria x 0-4): Structure, Business sense, Data approach, Numbers/rigour, Communication+recommendation; 16+ = strong, 12-15 = ok, <12 = practice. Hub links to the 10 mock cases (/cases/mock-case-01-.../ routes; check route naming from src/pages when writing; use links only if cases route exists, else mention "Cases section").
- Fermi estimation mini: steps, round numbers, sanity check.
- Personalise: fintech-first: example vocab (UPI success rate, failed payments, KYC, ticket size).
## Worked examples (3), with a Mermaid metric tree and SqlPlayground on fintech
1 Metric tree: "UPI app payment success rate dropped" -> Mermaid tree; SQL: failure rate by bank (`SELECT bank, COUNT(*) n, ROUND(100.0*SUM(status='FAILED')/COUNT(*),2) fail_pct FROM (SELECT DISTINCT * FROM transactions) GROUP BY bank ORDER BY fail_pct DESC;` -> Kaveri Co-op Bank 6.06% vs ~2.2-2.9% others, 1700 txns). 2 Same case second cut: by payment_app (NammaPay 5.10% vs 1.85-2.25%). 3 Fermi: how many UPI QR stickers in a mid-sized city? Show numbered steps.
## Common mistakes: jump to SQL without clarifying; list 15 hypotheses, no ranking; only internal causes; no recommendation; numbers without sanity check; ignoring duplicates in data.
## Quiz 5: first step of case (clarify); % drop in revenue tree term; which hypothesis is external (festival, competitor outage); segmenting by time shows sudden drop -> release/outage; recommendation must include (action+impact+next step).
## Interview Qs 3: Walk me through how you would approach "orders dropped 15% last week". How do you prioritise hypotheses? How do you end a case?
## Takeaways 5; Further reading: mode-sql, kaggle-learn
## Practice: PracticeSet. Rows (SQL on fintech, validated):
| interview-pr-case-001 | easy | sql | fintech | Ops lead wants failure rate by bank | bank, n_txns, fail_pct; 2dp; order fail_pct desc, bank | dedupe via subquery DISTINCT, SUM(status='FAILED') | Not deduping, counts ~90 duplicate rows |
| interview-pr-case-002 | medium | sql | fintech | Failure rate by payment_app | payment_app, n_txns, fail_pct | same | PENDING counted as failed |
| interview-pr-case-003 | medium | sql | fintech | Kaveri Co-op Bank failure rate by hour (hours >=100 txns? check) | hour, n_txns, fail_pct, top 5 | strftime('%H') | text hour sort |
| interview-pr-case-004 | medium | sql | fintech | failure_code mix for FAILED txns | failure_code, n, pct_of_failures | group, window or subquery total | percent of all txns instead |
| interview-pr-case-005 | hard | sql | fintech | Share of failures with retry that succeeded by failure_code | failure_code, retried, succeeded, success_pct | join failed_transactions dedupe | NULL retry_succeeded for retried=0 |
| interview-pr-case-006 | easy | text | none | Write 4 clarifying questions for "revenue dropped" | list | solution md | asking nothing |
| interview-pr-case-007 | medium | text | none | Build a metric tree for "food delivery late deliveries up" | tree | solution md | one-branch tree |
| interview-pr-case-008 | hard | text | none | Fermi: daily UPI QR payments at tea stalls in one city | number with steps | solution md | no sanity check |
Writer: validate with --fill and read outputs; 6 SQL/Python-free text ones do not need validate.
