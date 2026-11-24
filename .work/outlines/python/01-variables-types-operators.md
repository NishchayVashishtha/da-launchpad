# 01 Variables, types and operators
plan: title "Python basics: variables, types and operators" | desc "Store values, know their types and do arithmetic and comparisons." | order 1 | 30 min | tags python, basics, types
objectives: create variables and pick sensible names; tell int/float/str/bool/None apart; use arithmetic, comparison, logical operators; format numbers (f-strings, rounding) for reports; convert types safely
## concept (teaching order)
- Analogy: variable = labelled steel tiffin box; label points to contents, content has a type.
- Types: int, float, str, bool, None. `type()`. Why `"100"` is not `100`.
- Operators: + - * / // % **; `/` always float; `//` floor; `%` remainder (use: even/odd, paise). Comparison == != < >; and/or/not. `in`.
- Strings: quotes, f-strings `f"₹{x:,.2f}"`, len, upper/lower/strip, slicing `s[0:3]`, `.replace`, `.split`.
- Type conversion int()/float()/str(); `int("1,200")` fails -> motivates cleaning later.
- Float noise: `0.1+0.2`; use round(); money in paise or Decimal idea (mention only).
- Naming: snake_case, no keywords, meaningful (`gmv_inr`). Truthy/falsy short.
- FormulaCard: "Percentage change = (new - old) / old * 100" (Python form).
## worked examples
1. No dataset. UPI txn: amount=2499.5, fee_pct=0.9 -> fee, net; f-string print. Output: fee 22.4955 -> round 22.5.
2. Types trap: amount_text = "₹1,250"; strip symbol/comma with replace; float(); show error on raw conversion.
3. Flag logic: is_high_value = amount > 50000 and kyc == "FULL"; show bool outputs for 3 sample txns.
4. Integer vs float division: 7 txns / 2 batches with / // %.
## common mistakes
- `=` vs `==` -> SyntaxError or silent wrong. | `"5" + 5` TypeError. | int division belief (`/` returns float). | comparing floats with == after arithmetic. | variable named `list`/`sum` shadows builtin -> later calls crash. | forgetting strings are immutable (`s[0]="x"`).
## quiz
1 `10/4` -> 2.5 (traps: 2, 2.0, 3). 2 `type("42")` -> str (int, float, bool). 3 `7 % 3` -> 1 (2, 0, 2.33). 4 `not (5>3 and 2>4)` -> True (False, error, None). 5 f-string `f"{1234567.891:,.1f}"` -> `1,234,567.9` (1234567.9; 1,234,567.89; 1,234,568).
## interview Qs
- Mutable vs immutable (str/int/tuple vs list/dict/set) with an example. | `is` vs `==`. | What does `/` vs `//` return; where did you use `%`? | Why does `0.1+0.2 != 0.3` and what do you do for money?
## takeaways: variables are labels; every value has a type; `/` is float division; f-strings format reports; convert and check types before maths.
further reading: python-docs, kaggle-learn
## practice (file basics.json, topic "basics", dataset none)
| id | diff | lang | ds | ask | output | approach | mistake |
|---|---|---|---|---|---|---|---|
| python-basics-001 | easy | python | none | Ops team: 18% GST on a ₹2,499 plan; give GST amount | `result` = 449.82 (float, round 2) | `round(2499*0.18,2)` | integer `18/100` typed as `18//100` = 0 |
| python-basics-002 | easy | python | none | Convert string "₹1,25,000" salary to int | `result`=125000 | replace ₹ and , then int | `int("₹1,25,000")` ValueError |
| python-basics-003 | easy | python | none | Given amounts a=1250.0 and b=480.5 return their average rounded to 2 dp | 865.25 | (a+b)/2 | rounding too early / integer ops |
| python-basics-004 | medium | python | none | Given `name="  asha VERMA "`, return cleaned title-case name | "Asha Verma" | strip().title() | forgetting strip leaves spaces |
