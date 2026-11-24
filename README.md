# DA Launchpad (Data Analyst Launchpad)

> A modern, zero-to-hired learning platform and career accelerator designed specifically for aspiring data analysts targeting roles in the Indian tech, e-commerce, fintech, healthcare, and consulting ecosystems.

[![Astro](https://img.shields.io/badge/Astro-5.x-FF5D01.svg)](https://astro.build/)
[![React](https://img.shields.io/badge/React-19.x-61DAFB.svg)](https://react.dev/)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind-4.x-38B2AC.svg)](https://tailwindcss.com/)
[![SQLite WASM](https://img.shields.io/badge/SQLite-WASM-003B57.svg)](https://sqlite.org/)
[![Pyodide](https://img.shields.io/badge/Python-Pyodide_WASM-3776AB.svg)](https://pyodide.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 📌 Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [Tech Stack & Architecture](#tech-stack--architecture)
- [Curriculum & Module Map](#curriculum--module-map)
- [The 8 Portfolio Projects](#the-8-portfolio-projects)
- [Production Datasets](#production-datasets)
- [Interactive Client-Side Tools](#interactive-client-side-tools)
- [Content Targets vs Actuals](#content-targets-vs-actuals)
- [Local Setup & Installation](#local-setup--installation)
- [Quality Gates & Verification](#quality-gates--verification)
- [Deployment Guide](#deployment-guide)

---

## 🚀 Overview

**DA Launchpad** is a comprehensive, self-contained educational platform built from the ground up for aspiring Data Analysts. Unlike fragmented tutorials or generic video playlists, DA Launchpad provides:

1. **Empirically Rigorous Material**: Every metric, number, and case scenario is derived from real SQL execution against 7 production-grade SQLite datasets containing authentic Indian operational contexts (UPI payment failure spikes, COD return rates, monsoon delivery delays, and warehouse working capital).
2. **In-Browser Compute**: Practice SQL queries in SQLite via WebAssembly (`sql.js`) and execute Python (pandas, NumPy, Matplotlib) directly in the browser via Pyodide. No external server, account, or API keys required.
3. **End-to-End Interview Readiness**: 475 technical interview questions with model answers, 320 timed aptitude MCQs, 137 statistics MCQs, 11 timed 45-minute SQL screening tests, 35 industry and mock case studies, and a complete Job Search Toolkit with an ATS resume builder and application tracker.

---

## ✨ Key Features

- **Personalized 12-Week Study Plan**: Interactive daily task tracker, weekly study hour goal logger, streak counters, and weak-topic diagnostics.
- **SQL Playground & Interactive Exercises**: Practice 209 SQL questions and 130 Python pandas problems with live schema inspectors, instant execution, and automated diff checking against expected outputs.
- **11 Full-Length SQL Screening Tests**: 45-minute timed technical assessments mirroring entry-level screening tests at high-growth Indian tech firms.
- **Interactive Spaced Repetition (Leitner Box)**: 520+ flashcards across SQL, Python, Excel, Power BI, Statistics, Business, and Aptitude with a 5-box daily review queue.
- **Searchable Analytics Glossary**: 320+ terms across SQL, pandas, DAX, Excel, statistics, unit economics, and data engineering with instant search and A-Z filtering.
- **Printable Cheat Sheets**: One-page printable reference guides for SQL, Excel, pandas, Matplotlib/Seaborn, DAX, Statistics, A/B testing checklists, EDA checklists, and Business KPIs.
- **Offline PWA Support**: Full client-side caching powered by Service Workers and Workbox; search indexed locally with Pagefind.

---

## 🛠️ Tech Stack & Architecture

- **Framework**: [Astro 5](https://astro.build/) (Static Site Generation with partial hydration)
- **Component Islands**: [React 19](https://react.dev/) + TypeScript
- **Styling**: [Tailwind CSS v4](https://tailwindcss.com/)
- **In-Browser SQL Engine**: [sql.js / SQLite WASM](https://sql.js.org/)
- **In-Browser Python Engine**: [Pyodide WASM](https://pyodide.org/)
- **Search**: [Pagefind](https://pagefind.app/) (offline, zero-overhead static search index)
- **Diagrams**: [Mermaid.js](https://mermaid.js.org/) (for ER diagrams, metric trees, and data lineage)
- **Testing & Validation**: Node.js validation harness verifying 491 runnable SQL and Python solutions against source SQLite databases.

---

## 📚 Curriculum & Module Map

| Module | Name | Lessons | Practice Qs | Topics Covered |
| :--- | :--- | :---: | :---: | :--- |
| **00** | **Start Here** | 6 | 33 | Analytics career landscape, data analyst vs engineer vs scientist, 12-week roadmap, setup. |
| **01** | **Excel for Analytics** | 16 | 58 | Shortcuts, cleaning, XLOOKUP, INDEX MATCH, SUMIFS, Pivot Tables, Power Query, dynamic arrays. |
| **02** | **SQL Core & Advanced** | 42 | 209 | Filtering, joins, CTEs, window functions (ROW_NUMBER, RANK, LAG, LEAD), MoM growth, retention cohorts, query optimization. |
| **03** | **Power BI & DAX** | 19 | 83 | Star schema, relationships, calculated columns vs measures, CALCULATE, filter context, time intelligence, RLS. |
| **04** | **Python & Pandas** | 20 | 130 | NumPy, Series/DataFrames, indexing (`loc`/`iloc`), groupby transforms, data cleaning, Matplotlib & Seaborn, EDA. |
| **05** | **Statistics & Experimentation**| 17 | 170 | Summary stats, CLT, z-scores, confidence intervals, t-tests, ANOVA, Chi-Square, A/B testing design, SRM checks, OLS regression. |
| **06** | **Business Thinking** | 14 | 132 | Metric trees, funnels, cohort retention, churn, unit economics (LTV/CAC), guesstimates, RCA, data privacy (DPDP Act). |
| **07** | **Interview & Screening Hub** | 8 | 41 | Hiring mechanics, aptitude shortcuts, 10 mock cases, take-home projects, live SQL tests, salary negotiation, scam avoidance. |
| **08** | **Portfolio Projects** | 8 | — | 8 end-to-end industry portfolio projects with business problems, datasets, step-by-step guidance, and interview talking points. |
| **09** | **Job Search Toolkit** | 1 | — | ATS resume guide, 30 formula bullets, ResumeBuilder, ApplicationTracker, 4 Indian job channels, 90-day plan, 12-month AE roadmap. |
| **10** | **Cheat Sheets & Glossary** | 1 | — | 9 printable one-pagers, 320 glossary terms, 520 flashcards with Leitner spaced repetition. |

---

## 📂 The 8 Portfolio Projects

All projects live in `src/content/projects/` and follow a production-grade format (Business Problem, Dataset Description, Step-by-Step Analytical Execution, Deliverables, README Template, and Interview Talking Points):

1. **Food Delivery Operations: Delivery Delays & Customer Ratings** (`01-food-delivery-delays-and-ratings.mdx`)
   - *Dataset*: `food_delivery.sqlite` (15,000 orders)
   - *Skills*: SQL, Python, Linear Regression, Route Analytics
   - *Key Insight*: Monsoon rain triples late deliveries (15% to 53%); delivery duration penalizes ratings by -0.075 stars per delayed minute.
2. **E-commerce Operations: Returns Root Causes, COD Margins & RFM** (`02-ecommerce-sales-returns-rfm.mdx`)
   - *Dataset*: `ecommerce.sqlite` (10,000 orders)
   - *Skills*: SQL window functions, RFM segmentation, Return to Origin (RTO) diagnostics
   - *Key Insight*: Footwear returns reach 28.5% driven by size ambiguity; top 8% Champions drive 34% of GMV.
3. **Subscription Funnel Optimization & March 2024 Churn Anomaly** (`03-subscription-funnel-churn.mdx`)
   - *Dataset*: `subscription_churn.sqlite` (20,000 subscriptions)
   - *Skills*: Funnel conversion analysis, Cohort retention, Involuntary churn dunning
   - *Key Insight*: March 2024 cohort churn spiked to 62.2% due to failed recurring auto-debit triggers; automated dunning rescues 40% of dropouts.
4. **Workforce Analytics: Employee Attrition & Department Burnout** (`04-hr-attrition-workforce.mdx`)
   - *Dataset*: `hr_attrition.sqlite` (5,000 employees)
   - *Skills*: Python, Logistic Regression, Flight Risk Modeling, HR Metrics
   - *Key Insight*: Tech support experiences 31.4% attrition driven by unpaid overtime exceeding 15 hrs/week.
5. **Fintech UPI Payment Diagnostics & Anomaly Detection** (`05-fintech-upi-anomaly.mdx`)
   - *Dataset*: `fintech_upi.sqlite` (22,000 transactions)
   - *Skills*: Time-series SQL, Outlier detection, Fraud flag modeling
   - *Key Insight*: Kaveri Bank switch timeouts during 6 PM - 9 PM evening peak drove a 6.1% failure rate.
6. **Marketing A/B Testing & Channel ROAS Optimization** (`06-marketing-ab-campaign-roi.mdx`)
   - *Dataset*: `marketing_ab.sqlite` (12,000 experiment users + 250 campaigns)
   - *Skills*: Hypothesis testing, Chi-Square SRM verification, Attribution modeling
   - *Key Insight*: Checkout free-shipping banner lifted conversion by +1.15% (p=0.046) with confirmed 50/50 split (SRM p=0.73).
7. **Retail Store Operations & Inventory Bottlenecks** (`07-retail-inventory-store-ops.mdx`)
   - *Dataset*: `retail_inventory.sqlite` (100 stores, 25,000 inventory records)
   - *Skills*: Sales/SqFt analysis, Stockout frequency, Working capital turnover
   - *Key Insight*: Home Decor inventory coverage reaches 7.3 months of idle stock, trapping Rs 65 Lakhs in dead working capital.
8. **Omnichannel Analytics Capstone: Digital vs Brick-and-Mortar** (`08-omnichannel-analytics-capstone.mdx`)
   - *Dataset*: Cross-dataset synthesis (`ecommerce.sqlite` + `retail_inventory.sqlite`)
   - *Skills*: Multi-touch attribution, Customer lifetime value (LTV), Ship-from-Store fulfillment
   - *Key Insight*: Disproves channel cannibalization myth—hybrid omnichannel buyers spend 2.8x more annually than single-channel shoppers.

---

## 🗄️ Production Datasets

Located in `public/data/sqlite/`, these relational SQLite databases feature realistic operational nuances (case discrepancies, duplicate tracking IDs, and missing keys):

- **`ecommerce.sqlite`**: Customers, Orders (10,000 rows with duplicate order keys to teach deduplication), Order Items, Products, Shipments, Returns.
- **`food_delivery.sqlite`**: Restaurants, Delivery Partners, Customers, Orders (15,000 deliveries with monsoon weather indicators), Ratings, Order Items.
- **`subscription_churn.sqlite`**: Users, Subscriptions (20,000 subscription events), Payments, Usage Logs, Support Tickets.
- **`hr_attrition.sqlite`**: Employees (5,000 records), Departments, Performance Reviews, Salary History, Attrition Events.
- **`fintech_upi.sqlite`**: Users, Merchants, Transactions (22,000 UPI payments with bank switches, NPCI error codes, and fraud flags).
- **`marketing_ab.sqlite`**: Ad Campaigns, Impressions, Clicks, Conversions, A/B Test Variant Assignments (12,000 experiment records).
- **`retail_inventory.sqlite`**: Stores, Products, Daily Store Sales (25,000 records), Inventory Levels, Regional Targets.

---

## 🧰 Interactive Client-Side Tools

All tools are accessible via `/tools/<name>/` and operate completely client-side:

1. **SQL Tests** (`/tools/sql-tests/`): 11 timed, 45-minute screening assessments with automated query evaluation.
2. **Aptitude Practice** (`/tools/aptitude/`): 320 timed multiple-choice questions across Quant, Logical Reasoning, Data Interpretation, and Verbal Ability.
3. **Statistics MCQs** (`/tools/mcq/`): 137 timed conceptual questions with detailed statistical rationales and calculation shortcuts.
4. **Mock Interview** (`/tools/mock-interview/`): Category-specific technical question generator with countdown timers, candidate note pad, and self-rating history.
5. **Interview Question Banks** (`/interview/banks/`): 475 questions across 8 categories with togglable model answers, follow-up angles, and common traps.
6. **Spaced-Repetition Flashcards** (`/tools/flashcards/`): 520 flashcards with 5-box Leitner scheduling, keyboard navigation (`Space` to flip, `1` for review, `2` for mastered), and topic filtering.
7. **Analytics Glossary** (`/tools/glossary/`): 320 technical definitions with code examples, instant keyword search, and A-Z filtering.
8. **Application Tracker** (`/tools/tracker/`): Job hunt Kanban/list tracker with follow-up notifications, salary inputs, status stages, and CSV export.
9. **Resume Builder** (`/tools/resume/`): Single-page ATS resume creator with 30 pre-written Action + Task + Result + Number bullets and clean print-to-PDF output.

---

## 📊 Content Targets vs Actuals

| Metric | Master Prompt Target | Actual Verified Count | Status |
| :--- | :---: | :---: | :---: |
| **Total Lessons** | 130+ | **143** (142 published) | ✅ Exceeded |
| **SQL Practice Questions** | 200+ (70E / 80M / 50H) | **209** (71E / 81M / 57H) | ✅ Exceeded |
| **Total Practice Questions** | 700+ | **856** | ✅ Exceeded |
| **Runnable Solutions** | — | **491** (261 SQL, 230 Python) | ✅ 100% Pass |
| **Interview Q&A Bank** | 450+ | **475** | ✅ Exceeded |
| **Aptitude MCQs** | 300+ | **320** (100% blind validated) | ✅ Exceeded |
| **Statistics MCQs** | 100+ | **137** | ✅ Exceeded |
| **Timed SQL Screening Tests** | 10 | **11** | ✅ Exceeded |
| **Case Studies** | 35 (10 mock + 25 industry) | **35** | ✅ Met |
| **Portfolio Projects** | 8 | **8** | ✅ Met |
| **Flashcards** | 500+ | **520** | ✅ Exceeded |
| **Glossary Terms** | 300+ | **320** | ✅ Exceeded |
| **Astro Pages Built** | 200+ | **227** | ✅ Exceeded |
| **Pagefind Indexed Pages** | 150+ | **192** | ✅ Exceeded |

---

## 💻 Local Setup & Installation

### Prerequisites

- **Node.js**: v18.0.0 or higher
- **Python**: v3.10 or higher
- **npm**: v9.0.0 or higher

### 1. Clone & Install Dependencies

```bash
git clone https://github.com/lazinWolf/da-launchpad.git
cd da-launchpad

# Install Node dependencies
npm install

# Setup Python virtual environment (for solution validation)
python -m venv .venv

# On Linux/macOS:
source .venv/bin/activate
# On Windows (PowerShell):
.\.venv\Scripts\Activate.ps1

pip install -r requirements.txt
```

### 2. Start Local Development Server

```bash
npm run dev
```

Open `http://localhost:4321` in your browser.

---

## 🧪 Quality Gates & Verification

The project adheres to four mandatory quality gates before any commit:

```bash
# 1. MDX syntax & structure check
npm run check:mdx

# 2. Run all 491 runnable SQL & Python solutions against SQLite datasets
npm run validate

# 3. Collection integrity, cross-references, and broken internal links audit
npm run audit

# 4. Content quality & word-count linter
npm run lint:quality

# 5. Production build, Pagefind indexing & Service Worker generation
# (On Windows PowerShell, disable Astro telemetry first)
$env:ASTRO_TELEMETRY_DISABLED="1"; npm run build
```

---

## 🌐 Deployment Guide

### Deploy to GitHub Pages

1. In `astro.config.mjs`, the site base path is configurable via `SITE_BASE`:
   ```bash
   SITE_BASE=/da-launchpad/ npm run build
   ```
2. The output directory is `dist/`.
3. Set up a GitHub Actions workflow (`.github/workflows/deploy.yml`):
   ```yaml
   name: Deploy to GitHub Pages

   on:
     push:
       branches: [ master ]

   jobs:
     build-and-deploy:
       runs-on: ubuntu-latest
       steps:
         - uses: actions/checkout@v4
         - uses: actions/setup-node@v4
           with:
             node-version: 20
         - run: npm ci
         - run: SITE_BASE=/da-launchpad/ ASTRO_TELEMETRY_DISABLED=1 npm run build
         - uses: actions/upload-pages-artifact@v3
           with:
             path: dist
         - uses: actions/deploy-pages@v4
   ```

### Deploy to Vercel or Netlify

- Build Command: `ASTRO_TELEMETRY_DISABLED=1 npm run build`
- Output Directory: `dist`
- Install Command: `npm install`

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).
