# Outline brief (Sonnet outliner)
You DESIGN; Haiku agents will WRITE the final lessons and question JSON from your outlines, seeing only your outline file + one dataset schema file (.work/schema/<id>.md) + CLAUDE.md + .briefs/content-common.md. So every decision that needs judgment goes in the outline. Be terse (bullets, no prose paragraphs), but specific.

Read: CLAUDE.md, .briefs/content-common.md, your module's section of master_prompt.md (§5 Module N) plus §2/§3 only, and .work/schema/*.md for datasets (small files). Check ideas against data with `sqlite3 public/data/sqlite/<id>.sqlite` when needed. Look at scripts/py_harness.py to know what Python solutions can do (pandas via `load(dataset, table)`, assign `result`).

Write one file per lesson: .work/outlines/<module>/<NN-slug>.md containing:
- frontmatter plan: title, description, order, estimatedMinutes, objectives (3–5), tags
- concept: key points in teaching order; the analogy to use; terms to define; FormulaCard(s) if any
- worked examples (2–4): dataset+table, the business ask, the approach/code sketch, what the output shows
- common mistakes (4–6): mistake → consequence
- quiz: 5 MCQ ideas with the correct answer and the trap in each wrong option
- interview Qs (3–5): question + key points of a model answer
- takeaways (5); further-reading ids from src/data/links.json (or new official links to append, listed explicitly)
- practice questions: a table, one row each: id, difficulty, language, dataset, business ask (who/why), exact output spec (columns/order or value), solution approach (1 line), the realistic common mistake. Ids: `<module>-<topic>-NNN`, globally unique (grep src/content/practice to avoid clashes). Practice file path: src/content/practice/<module>/<topic>.json.
Also write .work/outlines/<module>/_plan.md: lesson list, question counts by difficulty and file, any extra assets (notebooks, checklists) with their spec, and the suggested split into Haiku writer tasks (each task = 1–2 lessons + their practice files, ~10–20 questions).

Difficulty must be honest (hard = multi-step, really hard). Don't write final content. Don't edit anything outside .work/outlines/<module>/. Final reply ≤100 words: lessons outlined, questions planned by difficulty, task split count, open questions.
