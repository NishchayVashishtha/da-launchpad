# 13-data-ethics-privacy  (topic: ethics; 8 practice, text)
fm: title "Data ethics and privacy basics"; description "Handle personal and health data responsibly and spot biased analysis."; order 13; estimatedMinutes 40; objectives: classify personal and sensitive data; apply minimisation, anonymisation, access control; explain India's DPDP Act in plain words; spot bias and misleading analysis; tags: business, ethics, privacy, dpdp, healthcare
## Concept
- PII (name, phone, email, UPI id, Aadhaar - never store raw), sensitive (health, financial, biometrics, caste/religion). Principles: consent, purpose limitation, data minimisation, retention limits, security, accountability. Analogy: borrowed house keys.
- Techniques: masking, hashing (limits), pseudonymisation vs anonymisation (re-identification risk with small groups; k-anonymity idea: suppress cells n<10), aggregation, role-based access, audit logs.
- India: Digital Personal Data Protection Act 2023 in plain words: data principal/fiduciary, consent, rights; (state high level only, advise checking official text; do NOT give legal advice). Healthcare: extra care; fintech: RBI data localisation rules (high level, no details).
- Analyst ethics: dataset bias (sampling), proxies for protected traits, cherry-picking, p-hacking, misleading charts, transparent assumptions; fairness in models (loan approvals); explaining limits.
- What to do when asked for data you should not share: say no politely, offer aggregate.
## Worked examples
1. fintech.users columns: tag each as PII / sensitive / safe (phone, upi_id, full_name, city, age_group, kyc_status).
2. Safe version of an hr extract for a manager: drop names, group salary into bands, suppress small cells.
3. Re-identification: a "male, 52, Chennai, Cardiology" row in a small hospital - why anonymisation fails.
4. Biased conclusion: "women have lower hikes" without controlling for dept (hr) - how to check honestly (no numbers claimed).
## Common mistakes
- Sharing raw extracts by email | thinking hashing = anonymous | small groups | collecting more than needed | only reading headline, ignoring bias | copying data to personal laptop/cloud.
## Quiz: PII vs sensitive; anonymisation vs pseudonymisation; data minimisation; consent; suppress small cells.
## Interview Qs: you find customer phone numbers in a CSV - what do you do? | how would you share health data with a vendor | how do you spot bias in a dataset | tell me about a time you pushed back on a data request | what is DPDP in one minute.
## Takeaways 5. FurtherReading: alex-the-analyst. (No external legal links; if needed ask orchestrator to add official govt DPDP page to links.json - open question.)
## Practice (ethics.json) text
| business-ethics-001 | easy | Classify: phone, city, diagnosis, UPI id, order count (md table) | text |
| -002 | easy | Name 4 data protection principles (md) | text |
| -003 | medium | Cell has 3 patients: what to do before showing in a dashboard? (md) | text |
| -004 | medium | A friend asks for the full customer CSV for his project: reply (md) | text |
| -005 | medium | Hash of phone number is shared: why not anonymous? (md) | text |
| -006 | hard | Credit-scoring model uses pin code; explain proxy-bias risk and 2 checks (md) | text |
| -007 | hard | Design a minimal, privacy-safe extract for an attrition analysis (columns kept/dropped/transformed) (md) | text |
| -008 | hard | You found a data leak in a shared folder: steps (md) | text |
