# 16 Visualisation with matplotlib and seaborn
plan: title "Charts with matplotlib and seaborn" | desc "Pick the right chart and draw it in a few lines." | order 16 | 45 min | tags python, matplotlib, seaborn, visualization
objectives: choose chart type by question; draw line/bar/hist/box/scatter/heatmap; label titles, axes, units; use seaborn for grouped views; avoid misleading charts
## concept
- Analogy: chart = a sentence; every chart should answer one question.
- Chart chooser: trend -> line; compare -> bar; distribution -> histogram/box; relationship -> scatter; correlation matrix -> heatmap; part-to-whole sparingly.
- matplotlib: `fig, ax = plt.subplots()`, `ax.plot/bar/hist`, `set_title/xlabel/ylabel`, `plt.tight_layout()`, `savefig`.
- seaborn: `sns.barplot`, `histplot`, `boxplot`, `scatterplot`, `heatmap(df.corr())`, `hue`.
- Prepare data first (groupby) then plot; sort bars; format ₹ with lakh.
- Good practice: start y axis at 0 for bars, no 3-D, ≤5 colours, title states the insight.
- NOTE: the browser Python runner on this site cannot render charts; code is shown for you to run in Jupyter/Colab locally. Practice here checks the data you would plot or answers in text.
## worked examples (code shown; output described as image caption)
1. line: daily txn count (fintech) -> Diwali spikes.
2. bar: failure rate by bank sorted.
3. hist + box: amount (log-scale idea) with outliers.
4. heatmap: corr of delivery numeric columns.
## common mistakes
- Truncated bar axis. | unsorted bars. | too many colours / pie with 10 slices. | no labels/units. | plotting raw dirty data. | forgetting plt.show() / overlapping figures in notebook.
## quiz
1 chart for trend -> line. 2 `hue` purpose. 3 hist vs bar. 4 corr heatmap input. 5 why not pie for 10 categories.
## interview Qs
- Chart choice for a question. | How to show distribution & outliers. | Misleading chart examples. | matplotlib vs seaborn. | How to show 3 variables.
## takeaways: one question per chart; shape data first; sort and label; bars start at zero; seaborn for grouped stats.
further reading: matplotlib-docs, seaborn-docs
## practice (viz.json, topic "viz")
| id | diff | lang | ds | ask | output | approach | mistake |
|---|---|---|---|---|---|---|---|
| python-viz-001 | easy | text | none | Which chart for "monthly orders over 2 years"? Why? (solution md) | text | line | pie/bar without time order |
| python-viz-002 | easy | text | none | Write the matplotlib lines to draw a sorted bar chart with title and axis labels for dict `d` | text | ax.bar | missing labels |
| python-viz-003 | medium | python | fintech | Prepare the data for a bar chart: txn failure rate % by payment_app sorted desc, 2dp (dedupe) -> Series | Series | groupby | unsorted |
| python-viz-004 | medium | text | none | Review description of a bar chart with axis starting at 90 (given); list 3 problems and the fix | text | | |
| python-viz-005 | hard | python | ecommerce | Data prep for a heatmap: order_items joined to products; rows = top 3 categories by item count, cols = quantity capped at 5 (5 means 5+); cell = item count | pivot 3x5 | clip(upper=5), crosstab | forgetting to cap, giving 7 columns |
| python-viz-006 | hard | text | marketing | Design 3 charts for a campaign ROI review: for each give chart type, data prep, key message | text | | too many charts |
