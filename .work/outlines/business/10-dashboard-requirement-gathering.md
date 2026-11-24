# 10-dashboard-requirement-gathering  (topic: dashreq; 8 practice, text)
fm: title "Dashboard requirement gathering"; description "Ask the right questions before you build a single chart."; order 10; estimatedMinutes 40; objectives: run a requirements conversation; convert a vague ask into a one-page spec; choose KPIs, filters, refresh, audience; avoid the 'everything dashboard'; tags: business, dashboard, requirements, stakeholders
## Concept
- Why: most rework comes from unclear asks. Analogy: a tailor takes measurements first.
- 8 questions: who uses it, what decision, how often, which KPIs (max 5-7), what comparison (target, last period), which filters/drill-downs, data source/owner + refresh, access/privacy (role-based, patient/customer PII), definition owners, success of the dashboard itself.
- Spec template (one page): purpose, audience, KPI list with formulas, filters, layout sketch (top: KPI cards; middle: trend; bottom: breakdown table), refresh, owner, acceptance criteria.
- Chart choice by question (trend=line, compare=bar, share=stacked; avoid pie > 5, 3-D). Layout: most important top-left.
- Pushback phrases ("Which decision will this change?"). Scope creep handling. Versioning and sign-off.
- Examples: UPI ops dashboard (daily success rate by app/bank/hour, TPV, top failure codes, alerts); hospital OPD dashboard (footfall, no-show, wait time; PII hidden); HR attrition dashboard.
## Worked examples (docs only)
1. Vague ask "make me a sales dashboard" -> question list -> answers invented -> final KPI list.
2. Spec for UPI ops dashboard using real KPI names from fintech data (failure by app/bank, hourly).
3. Spec for clinic no-show dashboard.
4. Review a bad dashboard description (25 charts) and trim to 6 visuals.
## Common mistakes
- Starting with charts | too many KPIs | undefined metrics | no owner | ignoring audience (CEO vs ops) | no refresh/ latency info | showing PII.
## Quiz: first question; max KPIs; chart type for trend; role-based access; acceptance criteria.
## Interview Qs: A manager says 'build me a dashboard' - what do you do? | how do you decide the KPIs | how do you handle conflicting asks | how do you test a dashboard | what if the stakeholder keeps adding requests.
## Takeaways 5. FurtherReading: power-bi-docs, alex-the-analyst.
## Practice (dashreq.json) text
| business-dashreq-001 | easy | List 6 questions to ask before building a dashboard (md) |
| -002 | easy | Which chart type suits a monthly TPV trend, and why (md, 2 sentences) | text |
| -003 | medium | Turn "I want to see how payments are doing" into a 5-KPI spec for an ops head (md) |
| -004 | medium | Write acceptance criteria for a clinic no-show dashboard (md) |
| -005 | medium | CFO and ops head ask for different definitions of "revenue": how do you resolve (md) |
| -006 | hard | Trim a 25-chart sales dashboard to 6 visuals; justify (md) |
| -007 | hard | Privacy design: patient names in the OPD dashboard - what do you show/hide and why (md) |
| -008 | hard | Scope creep: three new asks after sign-off; write the reply (md) |
