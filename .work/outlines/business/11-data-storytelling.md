# 11-data-storytelling  (topic: story; 8 practice, text)
fm: title "Data storytelling for non-technical stakeholders"; description "Turn analysis into a clear message and a clear ask."; order 11; estimatedMinutes 45; objectives: structure findings as answer-first (BLUF/pyramid); write an insight headline with a number; choose one chart per message; write an executive summary and recommendation; tailor to audience; tags: business, storytelling, communication, presentation
## Concept
- Insight vs observation: observation "failures are 2.7%"; insight "NammaPay fails 5.1%, double the others, almost all inside four outage windows - ask the vendor for an SLA." Formula: What + So what + Now what.
- Answer first (pyramid): conclusion, 3 supporting points, evidence, appendix. One slide = one message; action title (sentence with a number).
- Structure: context -> question -> answer -> evidence -> recommendation -> risks/next steps. Analogy: a doctor's discharge summary (diagnosis, treatment, follow-up).
- Visual rules: one chart one message, label directly, start axis at zero for bars, highlight the one bar that matters, remove clutter, consistent colours; avoid pie>5, dual axes.
- Audience: CXO (1 slide, decision), ops head (detail, action list), clinician/hospital admin (plain language, no jargon, privacy), tech (method).
- Talking numbers: round, give comparison (vs last month/benchmark), say uncertainty honestly (n=27).
- Template: 3-line executive summary; email template; a 5-slide outline.
## Worked examples
1. Rewrite a weak slide title ("Failure rate by app") into an action title using fintech facts (NammaPay 5.10% vs 2.2%; outage days 38.8% failure).
2. Executive summary for the March 2024 cohort (54.0% 60-day churn vs ~22%).
3. Choose a chart for each of 4 findings (trend, compare, share, distribution).
4. Convert a technical paragraph (p-value, CI) to plain language for hospital admin: A/B result (10.57% vs 11.72%).
## Common mistakes
- Burying the answer | 12 charts no message | jargon | no recommendation | misleading axis | hiding uncertainty | blaming people.
## Quiz: action title; BLUF; chart choice; audience tailoring; honest uncertainty.
## Interview Qs: explain a finding to a non-technical manager | how do you structure a presentation | stakeholder disagrees with your insight | what makes a good chart | tell me about a time your analysis changed a decision.
## Takeaways 5. FurtherReading: alex-the-analyst.
## Practice (story.json) text
| business-story-001 | easy | Rewrite the slide title "Monthly TPV" as one action title using: 2023 TPV Rs 1.28 crore, 2024 TPV Rs 1.70 crore (md, 1 sentence) | text |
| -002 | easy | Which chart type for trial->paid by platform (3 values)? | text |
| -003 | medium | Write a 3-line exec summary: Dec-24 orders fell 14.1% vs Nov; Dec up 5.5% YoY; all channels fell (md) | text |
| -004 | medium | Spot 4 problems in a described slide (md) | text |
| -005 | medium | Explain "95% confidence interval [0.02, 2.27] pp" to a hospital administrator in 3 sentences (md) | text |
| -006 | hard | Turn the A/B result (control 10.57%, treatment 11.72%, Desktop -1.4pp, Mobile +2.3pp) into a recommendation with risk (md) | text |
| -007 | hard | Write a 150-word email to a CXO on the Kaveri Co-op Bank peak-hour failures (9.98% vs 4.77%) (md) | text |
| -008 | hard | A VP disagrees with your finding. List the steps of your reply (md) | text |
