"""Dataset 3: hr (fictional mid-size Indian IT/services company 'Nirmaan Technologies')."""
import numpy as np
import pandas as pd
from common import *

SEED = 20230103

DEPTS = [  # name, head, location, budget (cr INR), headcount weight, base ctc multiplier, ot mean, attr effect
    ("Engineering", "Rajiv Menon", "Bengaluru", 42, 0.34, 1.25, 7, 0.0),
    ("Sales", "Anita Kapoor", "Mumbai", 18, 0.14, 1.0, 9, 0.55),
    ("Marketing", "Sameer Joshi", "Mumbai", 9, 0.06, 0.95, 5, 0.1),
    ("Customer Support", "Lata Pillai", "Chennai", 12, 0.18, 0.6, 10, 0.7),
    ("Finance", "Harish Iyer", "Pune", 6, 0.05, 1.05, 5, -0.2),
    ("Human Resources", "Neelam Gupta", "Pune", 4, 0.04, 0.9, 4, -0.1),
    ("Operations", "Vikas Rathore", "Hyderabad", 14, 0.12, 0.8, 8, 0.25),
    ("Product", "Ishita Banerjee", "Bengaluru", 8, 0.07, 1.3, 6, -0.1)]
TITLES = {
    "Engineering": ["Software Engineer", "Data Engineer", "QA Engineer", "DevOps Engineer", "Backend Developer"],
    "Sales": ["Sales Executive", "Account Manager", "Business Development Associate", "Inside Sales Rep"],
    "Marketing": ["Marketing Executive", "Content Specialist", "Performance Marketer", "Brand Associate"],
    "Customer Support": ["Support Associate", "Customer Success Associate", "Technical Support Engineer", "Team Lead Support"],
    "Finance": ["Accountant", "Financial Analyst", "Payroll Specialist", "Audit Associate"],
    "Human Resources": ["HR Executive", "Talent Acquisition Specialist", "HR Business Partner"],
    "Operations": ["Operations Executive", "Logistics Coordinator", "Process Associate", "Vendor Manager"],
    "Product": ["Product Analyst", "Product Manager", "UX Designer", "Business Analyst"]}
LEVELS = ["Junior", "Mid", "Senior", "Lead", "Manager"]
LEVEL_CTC = {"Junior": (3.0, 6.0), "Mid": (6.0, 12.0), "Senior": (12.0, 22.0), "Lead": (20.0, 34.0), "Manager": (30.0, 60.0)}


def build():
    rng = rng_for(SEED)
    nd = len(DEPTS)
    departments = pd.DataFrame({"department_id": np.arange(1, nd + 1), "department_name": [d[0] for d in DEPTS], "department_head": [d[1] for d in DEPTS],
                                "location": [d[2] for d in DEPTS], "annual_budget_inr": [d[3] * 10_000_000 for d in DEPTS],
                                "cost_center_code": [f"CC{100 + i * 10}" for i in range(nd)]})
    n = 2400
    dept = rng.choice(nd, n, p=np.array([d[4] for d in DEPTS]))
    level_i = rng.choice(5, n, p=[.3, .32, .24, .09, .05])
    level = np.array(LEVELS, dtype=object)[level_i]
    # hire date: 40% 2014-2021, 60% 2022-2024-11 (ramping up)
    old = rng.random(n) < 0.4
    hire_off = np.where(old, rng.integers(0, 8 * 365, n), 8 * 365 + rng.integers(0, 3 * 365 - 30, n))
    hire = pd.to_datetime("2014-01-01") + pd.to_timedelta(hire_off, unit="D")
    hire = hire.where(hire <= pd.Timestamp("2024-11-30"), pd.Timestamp("2024-11-30"))
    order = np.argsort(hire.values, kind="stable")
    hire, dept, level_i, level = hire[order], dept[order], level_i[order], level[order]
    ids = np.arange(1, n + 1)
    genders = choice(rng, ["Male", "Female"], n, p=[.62, .38])
    names, _ = full_names(rng, n, genders)
    age = np.clip(rng.normal(27, 4, n) + level_i * 3.5 + (hire.year.values < 2022) * 2, 21, 60)
    dob = (hire - pd.to_timedelta(age * 365.25, unit="D")).strftime("%Y-%m-%d")
    city_p = {"Bengaluru": .3, "Mumbai": .17, "Pune": .17, "Hyderabad": .13, "Chennai": .12, "Delhi": .11}
    city = choice(rng, list(city_p), n, p=list(city_p.values()))
    etype = choice(rng, ["Full-time", "Contract", "Intern"], n, p=[.88, .09, .03])
    wmode = choice(rng, ["Hybrid", "Office", "Remote"], n, p=[.55, .3, .15])
    # latent factors
    perf = rng.normal(0, 1, n)
    ot_mean = np.array([DEPTS[d][6] for d in dept]) + rng.normal(0, 3, n)
    ot_mean = np.clip(ot_mean, 0, 40)
    # manager assignment: someone of higher level in same dept
    mgr = np.full(n, 0)
    for d in range(nd):
        for lv in range(4):
            cand = ids[(dept == d) & (level_i == lv + 1)] if lv < 4 else []
            cand2 = ids[(dept == d) & (level_i > lv)]
            m = (dept == d) & (level_i == lv)
            if len(cand2) and m.sum():
                mgr[m] = rng.choice(cand2, m.sum())
    mgr = np.where(mgr == 0, 0, mgr)
    # salaries: baseline CTC
    lo = np.array([LEVEL_CTC[l][0] for l in level])
    hi = np.array([LEVEL_CTC[l][1] for l in level])
    dm = np.array([DEPTS[d][5] for d in dept])
    base_ctc = np.round((lo + (hi - lo) * rng.beta(2, 2.2, n)) * dm * 100000 / 1000) * 1000
    hike23 = np.clip(np.round(4 + 3.0 * perf + rng.normal(0, 2.0, n) + (dept == 1) * -1.0, 1), 0, 28)
    hike24 = np.clip(np.round(4 + 3.0 * perf + rng.normal(0, 2.0, n) + (dept == 1) * -1.0, 1), 0, 28)
    # attrition model
    avg_hike = np.where(hire < pd.Timestamp("2023-10-01"), (hike23 + hike24) / 2, hike24)
    tenure_short = (hire > pd.Timestamp("2022-01-01")).astype(float)
    z = (-2.35 - 0.75 * perf + 0.09 * (ot_mean - 7) - 0.16 * (avg_hike - 6) + 0.5 * tenure_short +
         np.array([DEPTS[d][7] for d in dept]) + 0.25 * (wmode == "Office") * 0 + 0.2 * (etype == "Contract"))
    p = 1 / (1 + np.exp(-z))
    left = rng.random(n) < p
    aw = np.ones(N_DAYS)
    aw[(MONTH >= 4) & (MONTH <= 6)] *= 1.7
    aw[(MONTH == 11) | (MONTH == 12)] *= 1.3
    aw[(MONTH == 1)] *= 1.2
    aw = aw * (1 + 0.3 * np.arange(N_DAYS) / N_DAYS)
    aw /= aw.sum()
    exit_idx = rng.choice(N_DAYS, n, p=aw)
    exit_ts = DAYS[exit_idx]
    min_exit = hire + pd.Timedelta(days=120)
    exit_ts = pd.DatetimeIndex(np.maximum(exit_ts.values, min_exit.values))
    exit_ts = exit_ts + pd.to_timedelta(rng.integers(0, 60, n) * (exit_ts.values == min_exit.values).astype(int), unit="D")
    left = left & (exit_ts <= pd.Timestamp("2024-12-31"))
    exit_ts = exit_ts.where(left, pd.NaT)
    # ---------------- employees
    employees = pd.DataFrame({
        "employee_id": ids, "full_name": names, "gender": np.where(rng.random(n) < 0.06, np.where(genders == "Male", "M", "F"), genders),
        "date_of_birth": np.array(dob, dtype=object), "email": nullify(rng, emails(rng, names, ("nirmaan-tech.in",)), 0.04),
        "hire_date": np.array(hire.strftime("%Y-%m-%d"), dtype=object), "department_id": dept + 1,
        "job_title": [TITLES[DEPTS[d][0]][rng.integers(len(TITLES[DEPTS[d][0]]))] for d in dept], "job_level": level,
        "manager_id": pd.array(np.where(mgr == 0, -1, mgr)).astype("Int64"), "city": case_mess(rng, city, 0.09),
        "employment_type": etype, "work_mode": wmode, "employment_status": np.where(left, "Exited", "Active")})
    employees.loc[employees["manager_id"] == -1, "manager_id"] = pd.NA
    employees["city"] = nullify(rng, employees["city"].values, 0.02)
    # ---------------- salaries
    rows = []
    sid = 0
    cur = base_ctc.copy()
    for i in range(n):
        h = hire[i]
        e = exit_ts[i]
        end = e if not pd.isna(e) else pd.Timestamp("2024-12-31")
        if h < pd.Timestamp("2023-01-01"):
            rows.append((i + 1, "2023-01-01", cur[i], None, "Opening balance"))
        else:
            rows.append((i + 1, h.strftime("%Y-%m-%d"), cur[i], None, "Joining"))
        for yr, hk in ((2023, hike23[i]), (2024, hike24[i])):
            eff = pd.Timestamp(f"{yr}-04-01")
            if h <= eff - pd.Timedelta(days=180) and end > eff:
                promo = hk >= 14
                cur[i] = np.round(cur[i] * (1 + hk / 100) / 1000) * 1000
                rows.append((i + 1, eff.strftime("%Y-%m-%d"), cur[i], hk, "Promotion" if promo else "Annual Appraisal"))
    salaries = pd.DataFrame(rows, columns=["employee_id", "effective_date", "annual_ctc", "hike_pct", "change_reason"])
    salaries.insert(0, "salary_id", np.arange(1, len(salaries) + 1))
    oi = rng.choice(len(salaries), 5, replace=False)
    salaries.loc[oi, "annual_ctc"] = salaries.loc[oi, "annual_ctc"] * 100
    salaries["annual_ctc"] = salaries["annual_ctc"].astype(float)
    # ---------------- reviews
    periods = [("2023-H1", "2023-07-15"), ("2023-H2", "2024-01-15"), ("2024-H1", "2024-07-15")]
    rv = []
    for lab, rd in periods:
        rdt = pd.Timestamp(rd)
        start = rdt - pd.Timedelta(days=180)
        ok = (hire <= start + pd.Timedelta(days=60))
        ok = ok & np.array([pd.isna(e) or e > rdt - pd.Timedelta(days=10) for e in exit_ts])
        idx = np.where(ok)[0]
        r = np.clip(np.round(3.1 + 0.8 * perf[idx] + rng.normal(0, 0.55, len(idx))), 1, 5).astype(int)
        ot = np.round(np.clip(ot_mean[idx] + rng.normal(0, 2.5, len(idx)), 0, 60), 1)
        goals = np.clip(np.round(70 + 9 * (r - 3) + rng.normal(0, 8, len(idx))), 20, 130).astype(int)
        selfr = np.clip(r + np.round(rng.normal(0.5, 0.7, len(idx))), 1, 5).astype(int)
        promo_rec = ((r >= 4) & (rng.random(len(idx)) < 0.3)).astype(int)
        jitter = rng.integers(0, 15, len(idx))
        for j, k in enumerate(idx):
            rv.append((k + 1, lab, (rdt + pd.Timedelta(days=int(jitter[j]))).strftime("%Y-%m-%d"), int(r[j]), int(selfr[j]), int(goals[j]), float(ot[j]), int(promo_rec[j])))
    reviews = pd.DataFrame(rv, columns=["employee_id", "review_period", "review_date", "manager_rating", "self_rating", "goals_met_pct", "avg_monthly_overtime_hours", "promotion_recommended"])
    reviews.insert(0, "review_id", np.arange(1, len(reviews) + 1))
    # ---------------- attrition
    li = np.where(left)[0]
    et = choice(rng, ["Resignation", "Termination", "Retirement", "End of Contract"], len(li), p=[.82, .09, .01, .08])
    et = np.where(np.array(etype)[li] == "Contract", np.where(rng.random(len(li)) < 0.5, "End of Contract", "Resignation"), np.where(et == "End of Contract", "Resignation", et))
    reasons = np.array([choice(rng, ["Better compensation", "Career growth", "Work-life balance / overtime", "Higher studies", "Relocation", "Manager issues", "Personal reasons"], 1,
                               p=([.28, .2, .2, .05, .05, .12, .1] if ot_mean[i] > 9 else [.25, .25, .06, .1, .1, .12, .12]))[0] for i in li], dtype=object)
    reasons = np.where(et == "Termination", "Performance / conduct", np.where(et == "End of Contract", "Contract ended", np.where(et == "Retirement", "Retirement", reasons)))
    notice = np.where(et == "Resignation", rng.choice([30, 60, 90], len(li), p=[.3, .4, .3]), np.where(et == "Termination", 0, 15))
    attrition = pd.DataFrame({"attrition_id": np.arange(1, len(li) + 1), "employee_id": li + 1,
                              "exit_date": np.array(exit_ts[li].strftime("%Y-%m-%d"), dtype=object), "exit_type": et, "exit_reason": reasons,
                              "notice_period_days": notice.astype(int), "regretted_loss": ((perf[li] > 0.3) & (et == "Resignation")).astype(int),
                              "exit_interview_score": nullify(rng, np.clip(np.round(3 - 0.4 * (ot_mean[li] > 9) + rng.normal(0, 1, len(li))), 1, 5).astype(int).astype(object), 0.3)})
    attrition = attrition.sort_values("exit_date", kind="stable").reset_index(drop=True)
    attrition["attrition_id"] = np.arange(1, len(attrition) + 1)
    attrition["exit_interview_score"] = attrition["exit_interview_score"].astype("Int64")
    employees = add_dups(rng, employees, n=12)
    reviews = add_dups(rng, reviews, n=10)

    def csv_emp(df, r):
        df["hire_date"] = mix_dates(r, df["hire_date"], 0.2)
        df["date_of_birth"] = mix_dates(r, df["date_of_birth"], 0.2)
        return df

    def csv_sal(df, r):
        df["annual_ctc"] = rupee_text(r, df["annual_ctc"], 0.3, decimals=0, indian=True)
        return df

    def csv_rev(df, r):
        df["review_date"] = mix_dates(r, df["review_date"], 0.15)
        return df

    spec = dict(
        id="hr", title="HR Analytics: Nirmaan Technologies", csv_seed=13,
        description=("Nirmaan Technologies is a fictional 2,400-person Indian tech and services company with eight departments across Bengaluru, Mumbai, Pune, Hyderabad, Chennai and Delhi. "
                     "The dataset links employees to appraisal-cycle salary changes, half-yearly performance reviews and exits during 2023-2024. "
                     "Use it to analyse attrition drivers, pay equity, hike policy and workforce planning."),
        tables=[
            dict(name="departments", df=departments, pk="department_id", desc="Eight departments with budget and head.", cols="""
department_id - Department identifier (primary key)
department_name - Department name
department_head - Name of the department head
location - Main office location
annual_budget_inr - Annual budget in INR
cost_center_code - Finance cost-centre code"""),
            dict(name="employees", df=employees, pk="employee_id", desc="One row per employee ever employed 2023-2024 (12 duplicate rows are deliberate).", csv=csv_emp, cols="""
employee_id - Employee identifier (duplicated for the duplicate rows)
full_name - Employee name
gender - Male/Female with some abbreviated 'M'/'F' values
date_of_birth - Date of birth
email - Work email (NULL for ~4%)
hire_date - Date of joining (2014 to Nov 2024)
department_id - FK to departments.department_id
job_title - Job title
job_level - Junior, Mid, Senior, Lead or Manager
manager_id - FK to employees.employee_id (NULL for top managers)
city - Work city (casing/whitespace issues, ~2% NULL)
employment_type - Full-time, Contract or Intern
work_mode - Hybrid, Office or Remote
employment_status - Active or Exited (matches the attrition table)"""),
            dict(name="salaries", df=salaries, pk="salary_id", desc="Salary history: opening/joining CTC and April appraisal revisions.", csv=csv_sal, cols="""
salary_id - Salary record identifier (primary key)
employee_id - FK to employees.employee_id
effective_date - Date the CTC became effective
annual_ctc - Annual cost-to-company in INR (5 rows are 100x outliers)
hike_pct - Percentage hike versus the previous CTC (NULL for opening/joining rows)
change_reason - Opening balance, Joining, Annual Appraisal or Promotion"""),
            dict(name="attrition", df=attrition, pk="attrition_id", desc="One row per employee who left in 2023-2024.", cols="""
attrition_id - Attrition record identifier (primary key)
employee_id - FK to employees.employee_id
exit_date - Last working date
exit_type - Resignation, Termination, Retirement or End of Contract
exit_reason - Recorded reason
notice_period_days - Notice period served in days
regretted_loss - 1 if a high performer resigned
exit_interview_score - 1-5 exit interview score (NULL for ~30%)"""),
            dict(name="performance_reviews", df=reviews, pk="review_id", desc="Half-yearly reviews 2023-H1 to 2024-H1 (10 duplicate rows are deliberate).", csv=csv_rev, cols="""
review_id - Review identifier (duplicated for duplicate rows)
employee_id - FK to employees.employee_id
review_period - Period label such as 2023-H1
review_date - Date the review was recorded
manager_rating - Manager rating 1-5
self_rating - Self-assessment rating 1-5
goals_met_pct - Percentage of goals met
avg_monthly_overtime_hours - Average monthly overtime hours in the period
promotion_recommended - 1 if manager recommended promotion"""),
        ],
        relationships=[("employees.department_id", "departments.department_id"), ("employees.manager_id", "employees.employee_id"),
                       ("salaries.employee_id", "employees.employee_id"), ("attrition.employee_id", "employees.employee_id"),
                       ("performance_reviews.employee_id", "employees.employee_id")],
        issues=[
            "employees: 12 exact duplicate rows (same employee_id twice), so employee_id has no PRIMARY KEY constraint; performance_reviews: 10 exact duplicate rows.",
            "employees.gender: ~6% of rows use 'M'/'F' instead of 'Male'/'Female'.",
            "employees.city: ~9% have inconsistent casing/whitespace ('pune', ' Pune'), ~2% NULL; employees.email ~4% NULL.",
            "employees.manager_id is NULL for top-level managers (~5% of employees).",
            "salaries.annual_ctc: 5 rows are 100x outliers (e.g. 120,000,000 instead of 1,200,000).",
            "salaries.hike_pct is NULL for opening-balance and joining rows (about 45% of salary rows).",
            "attrition.exit_interview_score is NULL for ~30% of exits.",
            "CSV only - employees.hire_date and employees.date_of_birth: ~20% of rows are DD-MM-YYYY.",
            "CSV only - salaries.annual_ctc: ~30% of rows are text with rupee symbol and Indian grouping (e.g. '₹12,50,000').",
            "CSV only - performance_reviews.review_date: ~15% of rows are DD-MM-YYYY."],
        signals=[
            "Attrition is driven by (a) low manager ratings, (b) high average overtime (> ~10 h/month), and (c) low appraisal hikes (< ~4%); employees with all three leave at several times the base rate.",
            "Customer Support, Sales and Operations have the highest attrition; Finance and HR the lowest; employees with < 2 years tenure leave more.",
            "Exits spike in April-June (post-appraisal) and Nov-Jan (post-bonus).",
            "Hike % tracks performance (about +3 points per rating step) while Sales gets ~1 point lower hikes.",
            "Customer Support has the lowest CTC but the highest overtime; Engineering and Product pay ~25-30% more than average.",
            "Overtime-heavy exits cite 'Work-life balance / overtime' far more often in exit_reason.",
            "5 salary outliers (100x) distort average CTC unless excluded."],
    )
    return spec


def run():
    return write_dataset(build())


if __name__ == "__main__":
    run()
