# 03 Functions
plan: title "Functions: write reusable analysis steps" | desc "Package logic so you can reuse and test it." | order 3 | 30 min | tags python, functions
objectives: define functions with params, defaults, return; know return vs print; use keyword args; write docstrings; understand scope; use lambda for tiny rules
## concept
- Analogy: a pressure-cooker recipe card: same steps, different ingredients.
- def, params, return; default args; `*args/**kwargs` brief; return multiple values (tuple).
- print vs return (a function returning None is the classic bug).
- Scope: local vs global; mutable default argument pitfall.
- lambda + sorted(key=...), map/filter mention; why analysts use functions: `clean_amount()`, then `df.apply`.
- Docstring + small test with assert.
## worked examples
1. `gst(amount, rate=0.18)` with default and keyword override.
2. `clean_rupee(text)` returns float; handle None; used on 4 strings.
3. `summary(values)` returns (min,max,mean) tuple; unpack.
4. sorted list of dicts by amount using lambda.
## common mistakes
- print instead of return -> result None. | mutable default `def f(x, acc=[])` shares state. | forgetting parentheses to call. | modifying global inside function without `global` -> UnboundLocalError. | positional args order swapped. | no return in some branch -> None.
## quiz
1 function with no return gives -> None. 2 `def f(a,b=2)`; `f(1)` -> uses 2. 3 `lambda x: x*2` calling -> ... 4 mutable default bug identify output of two calls. 5 `sorted(d, key=lambda r:r["amt"], reverse=True)` orders high to low.
## interview Qs
- return vs print. | *args/**kwargs. | what is a lambda & when not to use. | mutable default arguments. | write a function to clean currency strings.
## takeaways: functions name a step; return gives value; defaults make calls short; avoid mutable defaults; lambdas for one-liners.
further reading: python-docs
## practice (functions.json, topic "functions", none)
| id | diff | lang | ds | ask | output | approach | mistake |
|---|---|---|---|---|---|---|---|
| python-functions-001 | easy | python | none | Define `emi_simple(principal, rate_pct, months)` = principal*(1+rate_pct/100*months/12)/months; call for 120000, 12, 12 | 11200.0 | def+return | print instead of return |
| python-functions-002 | easy | python | none | Define `to_float(s)` stripping ₹ and commas; apply to "₹3,450.50" | 3450.5 | replace chain | float() on raw string |
| python-functions-003 | medium | python | none | Function `bucket(amount)` returning "S","M","L" (<1000, <10000, else); apply to list [500,1000,9999,15000] | ['S','M','M','L'] | if/elif in list comp | boundary using `<=` |
| python-functions-004 | medium | python | none | Given list of dicts (name, score), return names sorted by score desc then name asc (ties) | list of names | sorted key tuple `(-score,name)` | sorting only by score loses tie rule |
