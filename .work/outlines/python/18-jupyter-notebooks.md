# 18 Jupyter notebooks
plan: title "Jupyter notebooks for analysts" | desc "Work in cells, document as you go, share clean notebooks." | order 18 | 30 min | tags python, jupyter, notebook
objectives: install and launch Jupyter / use Colab / VS Code; use code and markdown cells; run in order; use shortcuts and magics; structure a portfolio-grade notebook; export
## concept
- Analogy: a lab notebook where code, results and notes live together.
- Setup: Anaconda or `pip install jupyter`; VS Code Jupyter extension; Google Colab.
- Cells: code/markdown, Shift+Enter, kernel restart & run all (hidden state bug), `%timeit`, `%matplotlib inline`, `!pip install`, `df.head()` display.
- Notebook structure: title, question, data, cleaning, EDA, insights, next steps; headers, TOC.
- Habits: restart-and-run-all before sharing; no secrets/keys; small outputs; clear names; relative paths; requirements.txt.
- Export: HTML, PDF, `.py`; commit `.ipynb` to Git (clear outputs or keep for portfolio).
- Starter notebooks provided on this site (see _plan assets).
## worked examples
1. Notebook skeleton listing (markdown headings) - describe.
2. Hidden state bug: cell run out of order, fix with Restart & Run All.
3. magics demo.
4. Convert notebook to HTML command `jupyter nbconvert --to html`.
## common mistakes
- Running cells out of order. | giant outputs. | no markdown story. | hard-coded local paths. | committing data/secrets. | never restarting kernel.
## quiz
1 run cell shortcut. 2 what kernel is. 3 hidden state. 4 magic prefix. 5 nbconvert.
## interview Qs
- Jupyter vs script. | Problems with notebooks. | How do you make a notebook reproducible. | Colab vs local. | How to share.
## takeaways: tell a story; run top to bottom; restart before sharing; no secrets; export clean.
further reading: jupyter, anaconda, vscode
## practice (jupyter.json, topic "jupyter", all text, dataset none)
| id | diff | lang | ds | ask | output | approach | mistake |
|---|---|---|---|---|---|---|---|
| python-jupyter-001 | easy | text | none | Keyboard shortcut and menu to run a cell and move on | Shift+Enter | | Ctrl+Enter does not advance |
| python-jupyter-002 | easy | text | none | Name 4 markdown sections a portfolio notebook must have | list | | |
| python-jupyter-003 | easy | text | none | Which magic times one line of code? | %timeit | | |
| python-jupyter-004 | medium | text | none | A notebook works on your laptop but fails for a recruiter; give 4 likely causes and fixes | list | | |
