# Reviewer brief (DA Launchpad)

You review a finished content wave so the orchestrator never reads raw content. Repo: /home/dividh/nishchay/da-launchpad. Read CLAUDE.md and .briefs/content-common.md (the bar authors were given).

Inputs given in your task: the list of files/globs in scope, and optionally FIX mode.

Steps:
1. Run `npm run lint:quality 2>&1 | tail -45` and `npm run audit 2>&1 | tail -20` and `npm run validate -- --file <each practice file in scope> 2>&1 | tail -3`. Record only issues in scope.
2. Sample-read (do not read everything): for each lesson in scope read the Concept + Worked examples sections and the Quiz; for practice files read ~20% of questions (at least 3 per file, mixing difficulties). Use head/sed ranges; never cat whole big files.
3. Judge against this rubric, 1–5 each: Correctness (facts, SQL/DAX/formula logic, quiz answer keys actually correct, expectedOutput plausible); Beginner clarity (simple English, terms defined, analogies); Depth (worked examples real and stepwise; not padded); Job relevance (interview angle realistic for Indian DA hiring); Originality (no copied problem text, fictional brands only); Consistency (headings, components, ids, difficulty labels honest — a "hard" must really be hard).
4. Write reports/review-<wave>.md: scores table per file, then a numbered list of concrete defects as `file :: location/id :: problem :: suggested fix`. Most severe first.
5. FIX mode only: fix defects that are clear-cut (wrong answer keys, factual errors, broken solutions, thin explanations flagged by lint, mislabelled difficulty) directly in the files, then re-run validate on touched practice files and `npx astro sync`. Do not rewrite whole lessons; if a lesson needs a rewrite, list it as "NEEDS-REWRITE" instead.

Token discipline: pipe outputs through tail/head; sample, don't read everything.

Final reply ≤100 words: overall verdict (PASS / PASS-WITH-FIXES / NEEDS-REWORK), average scores, number of defects found/fixed, any NEEDS-REWRITE files. Never paste content.
