# 07-bayes-theorem  (topic: bayes)
fm: title "Bayes theorem: updating beliefs with evidence"; description "Why a positive fraud alert may still be wrong, explained step by step."; order 7; estimatedMinutes 40; objectives: state Bayes rule; solve with a natural-frequency table; explain base rate neglect; apply to fraud/spam alerts; tags: statistics, bayes, probability
## Concept
- Analogy: UPI fraud alarm that is "95% accurate" but fraud is 1 in 1000: most alarms are false.
- P(A|B)=P(B|A)P(A)/P(B), with P(B)=P(B|A)P(A)+P(B|not A)P(not A). Terms: prior, likelihood, posterior, sensitivity, false-positive rate, base rate.
- Teach with natural frequencies: imagine 100,000 transactions -> table of fraud/not fraud x flagged/not flagged. Precision = posterior.
- Link: precision vs recall in alerts; why analysts tune thresholds.
- FormulaCard: Bayes theorem.
## Worked examples
1. Fraud: base 0.1%, sensitivity 90%, false-alarm 2% -> posterior 4.3% (script-check); table of 100,000.
2. fintech.transactions: is_flagged vs status (CSV amount is text - avoid); compute P(FAILED | flagged) and P(flagged|FAILED) via crosstab. (script-check)
3. Spam/disease alternative with 1% prevalence for contrast; show sensitivity change vs base rate change.
4. Update twice (two independent alerts) briefly.
## Common mistakes
- Base-rate neglect. | swapping P(A|B) and P(B|A) (prosecutor fallacy). | forgetting to total P(B) over both branches. | using percentages inconsistently. | assuming independence of two tests.
## Quiz: prior definition; compute posterior simple; P(B|A) vs P(A|B); effect of lower base rate; what the 'table' shows.
## Interview Qs: explain Bayes with fraud example | why accurate test has many false positives | precision vs recall link.
## Takeaways 5. FurtherReading: khan-stats
## Practice (bayes.json) 10 q
| statistics-bayes-001 | easy | python | fintech | P(is_flagged=1) over all txns (4dp) | value | mean | |
| -002 | medium | python | fintech | P(status=='FAILED' | is_flagged==1) (4dp) | value | filter | reverse conditional |
| -003 | medium | python | fintech | P(is_flagged==1 | status=='FAILED') (4dp) | value | | |
| -004 | medium | python | fintech | crosstab counts is_flagged x (status=='FAILED'): return dict of 4 counts | dict | | |
| -005 | hard | python | fintech | apply Bayes formula from -002's inputs to recompute P(FAILED|flagged) and confirm equal: return dict{direct,bayes} 4dp | dict | | |
| -006 | hard | python | food_delivery | P(Heavy Rain | late) using Bayes from P(late|HR), P(HR), P(late) among delivered 4dp | value | | |
| -007 | easy | text | none | prior 2%; likelihood.. direct: out of 1000 users 20 churn, 18 of churners were flagged, 98 of 980 non-churn flagged: P(churn|flagged) as % 1dp | {value} 15.5 | 18/116 | 18/20 |
| -008 | medium | text | none | base 0.1%, sens 90%, fpr 2%: posterior % 1dp | {value} 4.3 | script | |
| -009 | medium | text | none | same but base rate 1%: posterior % 1dp | {value} 31.3 | script | |
| -010 | hard | text | none | out of 100,000 txns 0.1% fraud, flagger catches 90% fraud, flags 2% genuine: how many flags are genuine? | {value} 1998 | 99,900*0.02 | |
## MCQ bank (statistics-2.json, 8)
- prior | meaning | belief before evidence | after
- posterior | meaning | updated probability | likelihood
- base rate | neglect leads to | too many false alarms trusted | missing evidence
- swap | P(A|B)=P(B|A)? | not generally | always
- fpr | higher false pos rate does | lowers posterior | raises
- rare | rarer event, same test | lower posterior | higher
- denominator | P(B) is | total chance of evidence | prior
- precision | flagged that are truly fraud | precision | recall
