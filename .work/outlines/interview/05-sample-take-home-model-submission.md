# Lesson 05: Sample assignment with a model submission (hub section 5, part 2)
Path: src/content/lessons/interview/05-sample-take-home-model-submission.mdx | order 5 | estimatedMinutes 50
- title "Sample take-home: UPI failures, with a model submission" | description "Read a real-style brief, then study a full model answer."
- objectives: Read a brief and extract tasks; See a complete SQL-based analysis; Study how findings become a recommendation; Compare your own attempt to the model; Reuse the template
- tags ["take-home","fintech","upi","model-answer"]
## Content shape (differs from standard: Concept = the brief; Worked examples = the model submission)
- Concept: THE BRIEF (blockquote, fictional company "PayZippy Ops team" is a dataset app; use "Ops head at PayZippy-like app" - use fictional only; dataset fintech): "Payment failures rose. In 4 hours: (1) overall failure rate and trend by month, (2) where failures concentrate (bank, app, hour, amount band), (3) top failure reasons and whether retries recover them, (4) 3 recommendations with expected impact. Deliver SQL + 1-page summary." Plus grading rubric (table: 5 criteria, weights 25/20/20/20/15).
- Worked examples = Model submission, 6 numbered steps each with SqlPlayground (writer runs and pastes real output):
 1 Data checks: duplicates (txn_id), outliers (6 rows ~100x), PENDING 80 rows, NULL merchant for P2P. Decide: use `SELECT DISTINCT *` CTE `clean`; define failure rate = FAILED / (SUCCESS+FAILED) (state in assumptions; note PENDING excluded).
 2 Overall and monthly failure rate (strftime('%Y-%m')). 
 3 By bank: Kaveri Co-op Bank ~6.06% (all-status denominators) vs 2.2-2.9% others; by app NammaPay 5.10% vs 1.85-2.25%.
 4 Hour cut for Kaveri: peak hours (9, 19, 20) 10-13%; hour 4 = 50% on tiny volume (warn: small n; treat as noise). Amount-band cut (>50,000 fails ~2.5x).
 5 Failure codes: INSUFFICIENT_FUNDS 139, UPI_SYSTEM_DOWN 118, BANK_DECLINED 100, INCORRECT_PIN 72, NETWORK_ERROR 71, LIMIT_EXCEEDED 65, BANK_SERVER_TIMEOUT 42 (writer re-verify); retry success by code (join failed_transactions).
 6 Written summary (the "1-page" as markdown blockquote): headline, 3 findings with numbers, 3 recommendations (bank-specific timeout fix/retry with backoff at peak for Kaveri; status page + auto-retry for NammaPay outage windows; clearer limit warning for > Rs 50,000), limits (no cost data, causal not proven, small n), next steps.
- Optional Python version: pandas snippet in a plain code block (not run).
- "Self-check" table: what a 4/4 vs 2/4 submission looks like per criterion.
## Common mistakes: reporting failure rate with duplicates; using PENDING as success; claiming the hour-4 spike matters; recommendations without numbers; no limits section.
## Quiz 5: denominator choice; why dedupe; small-n hour; best first recommendation target (largest excess failures: compute excess = n*(rate-baseline)); what to put in limits.
## Interview Qs 3: Walk me through your take-home. What would you do with one more day? How did you decide the failure-rate definition?
## Takeaways 5; Further reading: mode-sql, sqlite-docs
## Practice (all fintech SQL, validated; model-submission queries as exercises)
| interview-pr-sampletake-001 | easy | sql | fintech | Monthly failure rate (dedupe) | month, n_txns, fail_pct order month; limit 50 | strftime | duplicates |
| 002 | medium | sql | fintech | Excess failures by bank = failed - n*overall_rate; top 3 | bank, failed, expected, excess | CTE with overall rate | using raw rate not excess |
| 003 | medium | sql | fintech | Amount band (<=500, 501-5000, 5001-50000, >50000) failure rate | band, n_txns, fail_pct order by band min | CASE | banding order |
| 004 | hard | sql | fintech | For FAILED txns: retry recovery rate by failure_code (retried=1 only) | failure_code, retried_n, recovered_n, recovery_pct | join failed_transactions dedupe | NULL logic |
| 005 | hard | sql | fintech | NammaPay outage windows: days where NammaPay failure rate >20% (n>=10) | txn_date, n_txns, fail_pct | group by date | tiny n days |
Writer must verify numbers with sqlite3 before writing prose.
