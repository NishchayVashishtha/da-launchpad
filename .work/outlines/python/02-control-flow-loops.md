# 02 Control flow and loops
plan: title "Decisions and loops: if, for, while" | desc "Make Python choose and repeat." | order 2 | 30 min | tags python, loops, if
objectives: write if/elif/else for business rules; loop with for and range; use while with a stop condition; use break/continue; accumulate totals and counts in loops
## concept
- Analogy: bank counter token system: loop = serve each token; if = route by account type.
- Indentation = block. if/elif/else order matters (first true wins).
- for over list, range(start, stop, step) (stop exclusive), enumerate, zip. while + break; infinite-loop danger.
- Accumulator pattern: total=0; for x: total+=x. Counter dict preview.
- break / continue; for-else skip.
- Why analysts still prefer vectorised pandas (loops slow on 1 lakh rows) — foreshadow.
## worked examples
1. Fee slab: amount list [120, 5400, 62000]; label "Low/Mid/High" with if/elif.
2. Sum and count successful txns from list of dicts (status/amount); average.
3. First txn above ₹10,000 using for + break; show index via enumerate.
4. FizzBuzz-style: flag every 5th invoice id for audit using `%`.
## common mistakes
- Off-by-one with range stop. | modifying list while looping. | wrong indentation under if. | while without update -> infinite loop. | elif order (`>1000` before `>10000`) mislabels. | dividing by len(list)=0.
## quiz
1 `list(range(2,8,2))` -> [2,4,6]. 2 which prints for i in range(3): -> 0 1 2. 3 `break` vs `continue`. 4 if/elif order result for amount 70000 with checks >1000 first -> "Mid" (trap: "High"). 5 `zip([1,2,3],"ab")` -> 2 pairs.
## interview Qs
- FizzBuzz or count vowels live. | Difference between for and while, when use each. | How do you find the second largest number without sort? | Why avoid loops in pandas? | What does enumerate do?
## takeaways: indentation is syntax; first true branch wins; range stop is exclusive; accumulate with +=; prefer vectorised pandas later.
further reading: python-docs, kaggle-learn
## practice (loops.json, topic "loops", none)
| id | diff | lang | ds | ask | output | approach | mistake |
|---|---|---|---|---|---|---|---|
| python-loops-001 | easy | python | none | Sum of squares of 1..10 | 385 | loop or sum(range) | range(1,10) stops at 9 -> 285 |
| python-loops-002 | easy | python | none | txns=[250,1200,80000,45,9100]; count above 5000 | 2 | loop counter | `>=`/wrong threshold |
| python-loops-003 | easy | python | none | Given list of amounts return a list of labels "High" if >=50000 else "Normal" | list of 5 strings (specify list) | for + if | mutating list in place |
| python-loops-004 | medium | python | none | Collatz-like: starting 27 count steps while n!=1 (even n/2 else 3n+1) | 111 | while loop | infinite loop / off by one count |
