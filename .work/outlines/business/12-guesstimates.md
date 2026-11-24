# 12-guesstimates  (topic: guess; 10 practice, text with {value})
fm: title "Estimation and guesstimate basics"; description "Make a sensible number from nothing using simple assumptions."; order 12; estimatedMinutes 45; objectives: use a top-down and bottom-up approach; state assumptions clearly; sanity-check; do Indian-context estimates (UPI, clinics, chai); tags: business, guesstimate, estimation, interview
## Concept
- Purpose: show structure, not exact answer. Steps: clarify (scope, region, unit, time), choose approach (top-down: population x share; bottom-up: supply side, e.g. clinics x patients), split into easy parts, round numbers, compute, sanity check against known facts, state range.
- Round-number toolkit: India ~140 crore people (1.4 billion), ~35% urban, household ~4.5 persons, 1 crore = 100 lakh. Work in powers of 10. Segmenting population (age bands, urban/rural, income).
- Analogy: counting steps to a destination using average stride, not measuring every step.
- Avoid: false precision, hidden assumptions, forgetting units/time period. Cross-check with a second method.
- FormulaCard: market size = people x % buying x frequency x price.
## Worked examples (pure arithmetic; show assumptions table)
1. Cups of chai sold per day in a city of 20 lakh: 40% drink, 2 cups => 16,00,000 cups (value 1,600,000).
2. UPI transactions per day in India: 30 crore users x 40% daily x 3 txns = 36 crore (360,000,000) - sanity check with a known magnitude; call assumption fictional.
3. Monthly revenue of a clinic: 6 doctors x 25 patients/day x 26 days x Rs 400 = 1,560,000.
4. Hospital beds needed in a city of 20 lakh at 1.5 beds per 1,000 = 3,000.
## Common mistakes
- No assumptions stated | unit mix-ups (lakh/crore) | forgetting frequency | double counting | single-method answer | not sanity checking | going too deep on one branch.
## Quiz: top-down vs bottom-up; lakh to crore; sanity check; segmentation; ratio choice.
## Interview Qs: estimate the number of UPI transactions per day in Pune | how many diagnostic labs in Bengaluru | how many doctors consult via telehealth | size the market for a pharmacy delivery app | how would you validate your estimate.
## Takeaways 5. FurtherReading: alex-the-analyst.
## Practice (guess.json) language text; each {value} computed exactly (writers compute with python, round as stated)
| business-guess-001 | easy | City of 20 lakh adults, 40% drink chai, 2 cups each per day: cups per day | {value} 1600000 | forgetting 40% |
| -002 | easy | 1 crore = ? lakh | {value} 100 | |
| -003 | medium | 30 crore users x 40% active daily x 3 txns: txns/day | {value} 360000000 | lakh/crore slip |
| -004 | medium | Clinic: 6 doctors x 25 patients x 26 days x Rs 400: monthly revenue | {value} 1560000 | |
| -005 | medium | Beds for 20 lakh people at 1.5 per 1,000 | {value} 3000 | |
| -006 | medium | Pharmacies: 20 lakh people, 1 per 1,500: number (round to nearest) | {value} 1333 | |
| -007 | hard | Telehealth market: 4 crore urban households x 25% willing x Rs 600 per year: market size in Rs crore | {value} 600 | crore conversion |
| -008 | hard | Bottom-up: 400 labs x 60 samples per day x 300 days x Rs 500: yearly revenue in Rs crore | {value} 360 | |
| -009 | medium | List the steps and assumptions to estimate daily orders for a FoodKart in one city (md) | text | |
| -010 | hard | Two methods for number of UPI merchants in a city of 50 lakh: write both and compare (md) | text | |
