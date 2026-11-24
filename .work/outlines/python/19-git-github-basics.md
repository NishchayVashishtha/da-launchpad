# 19 Git and GitHub basics
plan: title "Git and GitHub basics for your portfolio" | desc "Save versions of your work and publish it for recruiters." | order 19 | 35 min | tags git, github, portfolio
objectives: explain repo/commit/branch; run init/add/commit/status/log; connect remote and push; write .gitignore and README; use branches and pull requests (basic)
## concept
- Analogy: Git = save-game with notes; GitHub = cloud storage + showcase.
- Core flow: working dir -> staging (`add`) -> commit -> remote (`push`).
- Commands: `git init`, `clone`, `status`, `add`, `commit -m`, `log --oneline`, `diff`, `branch`, `switch -c`, `merge`, `push/pull`, `restore`.
- Good commit messages; small commits.
- `.gitignore`: data files, `.env`, `.ipynb_checkpoints`, `__pycache__`; never commit secrets or personal data.
- README for a project: problem, data, method, findings, how to run; project folder structure (data/, notebooks/, src/, reports/).
- GitHub: create repo, Pages / README render, notebooks render; pull request basics; profile README.
- Link to Projects hub and Job Search module.
## worked examples
1. terminal session transcript (init -> add -> commit -> remote add -> push) shown as code block.
2. .gitignore example for analytics project.
3. branch -> change -> merge flow.
4. README template skeleton for an EDA project.
## common mistakes
- Committing large raw data / secrets. | commit message "update". | working on main without branches for bigger changes. | forgetting `git add` before commit. | merge conflict panic (resolve markers). | repo with no README.
## quiz
1 which command stages. 2 push vs commit. 3 what .gitignore does. 4 `git status` shows. 5 clone vs fork.
## interview Qs
- Git vs GitHub. | What is a branch. | How do you undo last commit (local). | merge vs rebase (one line). | what do you put in a README.
## takeaways: add then commit then push; small commits with clear messages; ignore data/secrets; README sells your project; branches for experiments.
further reading: git-docs, github-docs
## practice (git.json, topic "git", text, none)
| id | diff | lang | ds | ask | output | approach | mistake |
|---|---|---|---|---|---|---|---|
| python-git-001 | easy | text | none | Write the 3 commands to save a changed file `eda.ipynb` with message | add, commit | | skipping add |
| python-git-002 | easy | text | none | What is the difference between `git commit` and `git push`? | text | | |
| python-git-003 | easy | text | none | List 4 entries for a .gitignore of an analytics repo | list | | |
| python-git-004 | medium | text | none | You committed a CSV with customer phone numbers; what steps minimise harm? | text | remove, gitignore, rotate/history note | only deleting file |
| python-git-005 | medium | text | none | Write a good README outline for your UPI failure analysis repo | text | | |
