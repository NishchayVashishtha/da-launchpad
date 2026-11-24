# 06 NumPy basics
plan: title "NumPy: fast arrays for numbers" | desc "Do maths on whole columns at once." | order 6 | 35 min | tags python, numpy, arrays
objectives: create arrays; use vectorised maths and broadcasting; slice and boolean-mask; use sum/mean/std/percentile/where; understand why NumPy beats loops
## concept
- Analogy: spreadsheet column - apply one formula to the whole column instead of cell by cell.
- np.array, arange, linspace, zeros; shape, dtype, ndim; reshape.
- Vectorised ops, broadcasting (array*1.18); boolean masks `a[a>5000]`.
- Aggregates: sum mean median(np.median) std var min max percentile; axis=0/1 for 2-D.
- np.where (if-else column), np.nan, np.isnan, nansum/nanmean; np.round; np.cumsum, np.diff.
- Random with seed (np.random.default_rng(42)) to simulate.
- Link: pandas columns are NumPy arrays under the hood.
- FormulaCard: "z = (x - mean) / std" in NumPy.
## worked examples
1. Amounts array [250, 1200, 80000, 45, 9100]: add 18% GST, mean, max.
2. Mask: amounts above 5000; count with `.sum()` on boolean.
3. np.where label High/Normal; np.nanmean with a NaN.
4. 2-D: 3 months x 4 apps matrix of volumes; axis sums, share of total.
## common mistakes
- Python list * 2 vs array * 2. | shape mismatch in broadcasting. | `np.mean` with NaN -> nan. | using `and` instead of `&` for masks (needs parentheses). | integer dtype overflow/truncation. | view vs copy when slicing.
## quiz
1 `np.array([1,2,3])*2` -> [2,4,6]. 2 `[1,2,3]*2` -> list repeated. 3 `a[(a>1)&(a<5)]` correct syntax. 4 `np.mean([1,np.nan,3])` -> nan. 5 `np.arange(0,10,3)` -> [0,3,6,9].
## interview Qs
- Why is NumPy faster than lists. | broadcasting explained. | view vs copy. | how to replace outliers using np.where / clip. | difference np.std ddof.
## takeaways: arrays are typed and fixed; operations apply to all elements; masks filter; where is the vector if-else; NaN poisons plain mean.
further reading: numpy-docs
## practice (numpy.json, topic "numpy", none unless noted)
| id | diff | lang | ds | ask | output | approach | mistake |
|---|---|---|---|---|---|---|---|
| python-numpy-001 | easy | python | none | amounts=[250,1200,80000,45,9100]; mean (float, round 2) | 18119.0 | np.mean | median confusion |
| python-numpy-002 | easy | python | none | Apply 18% GST to array; return list rounded 2 dp | list | arr*1.18, round | list*1.18 TypeError |
| python-numpy-003 | easy | python | fintech | Fraud desk: how many transactions are flagged (is_flagged==1, raw rows)? | int | df.is_flagged.sum() | counting rows instead of flags |
| python-numpy-004 | medium | python | none | rng seed array of 1..20: number of values divisible by 3 and >6 | int | mask with & | `and` ValueError |
| python-numpy-005 | medium | python | none | amounts with a np.nan: mean ignoring NaN, round 2 | float | np.nanmean | np.mean -> nan |
| python-numpy-006 | medium | python | none | 3x4 volumes matrix (give in question): return list of share-of-total % per column rounded 1 dp | list of 4 floats | sum axis=0 / total*100 | wrong axis |
| python-numpy-007 | hard | python | none | z-score array of 8 given values; return count with abs(z)>1.5 (population std, ddof=0) | int | np.std default ddof=0 | using sample std changes count |
