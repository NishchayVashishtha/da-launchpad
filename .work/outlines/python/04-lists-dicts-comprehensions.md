# 04 Lists, dicts, sets, tuples and comprehensions
plan: title "Lists, dictionaries and comprehensions" | desc "Hold many values and transform them in one line." | order 4 | 35 min | tags python, list, dict, comprehension
objectives: use list/tuple/set/dict and pick the right one; index, slice, append, sort; count with dict; write list and dict comprehensions; read a list of dict records
## concept
- Analogy: list = queue at ATM; dict = phone contacts (name->number); set = unique ID badge box; tuple = fixed pair (lat,long).
- Methods: append, extend, sort vs sorted, `.get`, `.items()`, `in`, `set()` for unique, set ops.
- Slicing `x[-3:]`, `x[::2]`.
- Comprehension: `[f(x) for x in xs if cond]`, `{k:v for ...}`, set comp; readability limit (no nesting > 2).
- Records = list of dicts -> exactly how JSON/APIs and `pd.DataFrame(records)` look.
- Counting idiom: `d[k]=d.get(k,0)+1`; `collections.Counter` mention.
- FormulaCard: "[expr for item in iterable if condition]".
## worked examples
1. Failed-txn codes list -> Counter via dict get -> top code.
2. Comprehension: ₹ amounts >₹5,000 doubled? Better: GST-inclusive list for amounts above threshold.
3. Dict comp: {city: len(name)} no; use {payment_app: txn_count} from records.
4. Unique cities via set, sorted; list of dict -> DataFrame preview.
## common mistakes
- `list.sort()` returns None (`x = x.sort()`). | KeyError by d[key] vs `.get`. | copy by reference (`b=a` then change). | modifying dict during iteration. | set has no order/indexing. | too clever nested comprehension.
## quiz
1 `[x*2 for x in range(3)]` -> [0,2,4]. 2 `len(set([1,1,2]))` -> 2. 3 `d.get("z",0)` when missing -> 0. 4 `a=[1,2];b=a;b.append(3);a` -> [1,2,3]. 5 slicing `[10,20,30,40][-2:]` -> [30,40].
## interview Qs
- list vs tuple vs set vs dict. | Explain a list comprehension and when not to use. | How to count frequency without Counter. | shallow vs deep copy. | Time complexity of `in` list vs set (O(n) vs O(1) avg).
## takeaways: pick structure by need; dict for lookups; set for unique; comprehension = loop + filter in one line; list of dicts == table rows.
further reading: python-docs
## practice (comprehensions.json, topic "comprehensions", none)
| id | diff | lang | ds | ask | output | approach | mistake |
|---|---|---|---|---|---|---|---|
| python-comprehensions-001 | easy | python | none | amounts=[250,1200,80000,45,9100]; list of those >1000 | [1200,80000,9100] | list comp w/ if | filter condition placed before `for` |
| python-comprehensions-002 | medium | python | none | apps list of 8 payment_app strings (give in question); dict of counts | dict | loop with .get or Counter | KeyError on first sight |
| python-comprehensions-003 | medium | python | none | records list of 5 dicts (city, amount); dict city -> total amount | dict | accumulate with get | overwrite instead of add |
| python-comprehensions-004 | hard | python | none | Given list of 6 txn dicts with id, user, amount; return dict user -> max amount, only users with >=2 txns | dict | two-pass: group then dict comp | filtering count after taking max (wrong users) |
