# 06-probability-basics  (topic: probability)
fm: title "Probability basics for analysts"; description "Events, rules, independence and conditional probability, with data you know."; order 6; estimatedMinutes 45; objectives: compute simple and compound probabilities; use AND/OR rules; understand independence; compute conditional probability from a table; use expected value; tags: statistics, probability, conditional
## Concept
- Analogy: weather forecast "70% rain" = out of 100 similar days, ~70 had rain. Probability 0..1; relative-frequency view with data.
- Complement P(not A)=1-P(A). OR: P(A or B)=P(A)+P(B)-P(A and B). AND independent: product. Mutually exclusive vs independent (frequent mix-up).
- Conditional P(A|B)=P(A and B)/P(B), computed from a cross-tab. Independence check: P(A|B)=P(A).
- Expected value = sum(value*prob): e.g. coupon expected cost.
- Permutations/combinations: one short example (n choose k) since aptitude rounds use it.
- FormulaCard: addition rule, FormulaCard: conditional probability.
## Worked examples
1. food_delivery: P(delay>10 min), P(Rain), P(delay>10 | Heavy Rain) vs overall -> not independent. (script-check)
2. subscription.subscriptions: P(status=...) from value_counts.
3. Expected value: a ₹50 cashback with 4% claim probability on 10 lakh orders.
4. Combinations: choose 3 of 8 stores for a pilot = 56.
## Common mistakes
- Adding probabilities for non-exclusive events (double count). | assuming independence. | confusing P(A|B) with P(B|A). | forgetting complement shortcut "at least one". | percent vs fraction mixing.
## Quiz: complement; independent AND; OR rule; conditional from counts; mutually exclusive vs independent.
## Interview Qs: P(at least one of 3 payments fails) | independence vs mutual exclusivity | conditional probability from a table | expected value of a promo.
## Takeaways 5. FurtherReading: khan-stats
## Practice (probability.json) 10 q
| statistics-probability-001 | easy | python | food_delivery | P(delivery late: delay_minutes>10) among delivered (4dp) | value | mean bool | including cancelled in denominator |
| -002 | easy | python | food_delivery | P(weather == 'Rain' or 'Heavy Rain') over all deliveries (4dp) | value | isin | |
| -003 | medium | python | food_delivery | P(late | Heavy Rain) (4dp) among delivered | value | filter then mean | P(HeavyRain|late) |
| -004 | medium | python | food_delivery | P(late | Clear) minus P(late | Heavy Rain) as value | value | | |
| -005 | medium | python | subscription | P(status == X) pick the most common status: return dict {status, prob 4dp} | dict | value_counts normalize | |
| -006 | hard | python | food_delivery | independence test: is P(late and Rain-or-HeavyRain) approx P(late)*P(Rain..)? return dict {joint, product} 4dp | dict | | |
| -007 | easy | text | none | P(at least one head) in 3 fair tosses | {value} 0.875 | 1-0.5^3 | 0.5*3 |
| -008 | medium | text | none | P(A)=0.4 P(B)=0.3 P(A and B)=0.12 independent? P(A or B) | {value} 0.58 | | 0.7 |
| -009 | medium | text | none | expected cashback cost: ₹40 with p=0.05 on 2,00,000 orders | {value} 400000 | | |
| -010 | hard | text | none | choose 3 of 10 analysts for a team: combinations | {value} 120 | nCk | 720 |
## MCQ bank (statistics-2.json, 8)
- range | P cannot be | 1.3 | 0
- complement | P(rain)=0.3, no rain | 0.7 | 0.3
- independent | two fair coins both heads | 0.25 | 0.5
- exclusive | P(A and B) for exclusive | 0 | P(A)P(B)
- or | 0.5+0.4-0.2 | 0.7 | 0.9
- conditional | 30 of 120 late were rain..: P(rain|late) | 0.25 | P(late|rain)
- ev | win ₹100 w.p. 0.1 | ₹10 | ₹100
- gambler | 5 tails in row, next head chance | still 0.5 | higher
