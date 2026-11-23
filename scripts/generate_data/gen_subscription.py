"""Dataset 5: subscription (fictional streaming/learning app 'Kahani+' with trial -> paid -> renew/cancel)."""
import datetime as dt
import numpy as np
import pandas as pd
from common import *

SEED = 20230105
PLANS = {  # plan: (monthly price, annual price)
    "Basic": (149, 1299), "Standard": (299, 2499), "Premium": (499, 3999)}
END_TS = dt.datetime(2024, 12, 31, 23, 59, 59)


def build():
    rng = rng_for(SEED)
    n = 5200
    w = day_weights(growth=0.9, weekend=1.1, festive=1.35, sales=1.15, ipl=1.1)
    sday = np.sort(sample_days(rng, n, w))
    # keep last month signups out so most have time to be observed
    sts, _ = make_times(rng, sday, [.4, .2, .1, .1, .1, .2, .6, 1.2, 2, 2.5, 3, 3, 3.5, 3, 3, 3.5, 4, 5, 6, 7, 7.5, 6, 3, 1])
    platform = choice(rng, ["Android", "iOS", "Web"], n, p=[.62, .22, .16])
    source = choice(rng, ["Organic", "Google Ads", "Instagram", "Influencer", "Referral", "Play Store Feature"], n, p=[.28, .22, .18, .13, .12, .07])
    city = choice(rng, CITY_NAMES, n, p=CITY_W)
    names, _ = full_names(rng, n)
    users = pd.DataFrame({
        "user_id": np.arange(1, n + 1), "email": nullify(rng, emails(rng, names), 0.06), "signup_date": [t[:10] for t in sts],
        "signup_time": [t[11:] for t in sts], "city": nullify(rng, case_mess(rng, city, 0.1), 0.04), "platform": platform,
        "acquisition_source": source, "age_group": choice(rng, ["18-24", "25-34", "35-44", "45+"], n, p=[.34, .4, .18, .08])})
    events = []   # (user_id, datetime, name, plan)
    subs = []
    sid = 0
    for i in range(n):
        uid = i + 1
        s = dt.datetime.strptime(sts[i], "%Y-%m-%d %H:%M:%S")
        plat = platform[i]
        src = source[i]
        mon = (s.year, s.month)
        events.append((uid, s, "signup", None))
        p_trial = {"Android": 0.58, "iOS": 0.68, "Web": 0.55}[plat] + (0.2 if src == "Influencer" else 0) + (0.08 if src == "Referral" else 0)
        trial = rng.random() < p_trial
        k_early = rng.poisson(3.0 if trial else 1.1)
        end_active = s
        plan_name = None
        if trial:
            ts_ = s + dt.timedelta(minutes=int(rng.exponential(120)) if rng.random() < 0.6 else int(rng.integers(1, 48 * 60)))
            plan_name = rng.choice(["Basic", "Standard", "Premium"], p=[.3, .5, .2])
            events.append((uid, ts_, "trial_start", plan_name))
            if ts_ > END_TS:
                trial = False
            else:
                annual = rng.random() < 0.17
                p_conv = {"Android": 0.34, "iOS": 0.5, "Web": 0.42}[plat]
                if src == "Influencer":
                    p_conv *= 0.45
                if src == "Referral":
                    p_conv *= 1.25
                if mon in [(2023, 10), (2023, 11), (2024, 10), (2024, 11)]:
                    p_conv *= 1.2
                if plan_name == "Premium":
                    p_conv *= 0.9
                converted = rng.random() < min(p_conv, 0.9)
                paid_start = ts_ + dt.timedelta(days=7)
                price = PLANS[plan_name][1 if annual else 0]
                cycle = "Annual" if annual else "Monthly"
                if not converted or paid_start > END_TS:
                    subs.append([uid, plan_name, cycle, price, ts_.strftime("%Y-%m-%d"), None, (paid_start.strftime("%Y-%m-%d") if paid_start <= END_TS else None), "trial_expired" if paid_start <= END_TS else "trialing", None, 0, None])
                    if paid_start <= END_TS:
                        events.append((uid, paid_start, "trial_expired", plan_name))
                    end_active = min(ts_ + dt.timedelta(days=7), END_TS)
                else:
                    events.append((uid, paid_start, "payment_success", plan_name))
                    # renewals
                    period = 365 if annual else 30
                    hz1 = 0.30 if annual else 0.17
                    hz = 0.34 if annual else 0.075
                    mult = {"Basic": 1.35, "Standard": 1.0, "Premium": 0.8}[plan_name]
                    if mon == (2024, 3):
                        mult *= 2.7        # bad cohort (broken release / price change)
                    if plat == "Android":
                        mult *= 1.1
                    if src == "Influencer":
                        mult *= 1.3
                    renewals = 0
                    cur = paid_start
                    cancel_ts = None
                    while True:
                        nxt = cur + dt.timedelta(days=period)
                        # churn decision made sometime before next billing
                        h = (hz1 if renewals == 0 else hz) * mult
                        if rng.random() < min(h, 0.9):
                            cancel_ts = cur + dt.timedelta(days=int(rng.integers(max(2, period // 3), period)), minutes=int(rng.integers(0, 1440)))
                            if cancel_ts > END_TS:
                                cancel_ts = None
                                break
                            break
                        if nxt > END_TS:
                            break
                        if rng.random() < 0.035:
                            events.append((uid, nxt, "payment_failed", plan_name))
                            if rng.random() < 0.45:
                                cancel_ts = nxt + dt.timedelta(days=3)
                                events.append((uid, cancel_ts, "cancel_subscription", plan_name))
                                break
                            nxt = nxt + dt.timedelta(days=2)
                        events.append((uid, nxt, "renewal_success", plan_name))
                        renewals += 1
                        cur = nxt
                    if cancel_ts is not None and not any(e[0] == uid and e[2] == "cancel_subscription" for e in events[-3:]):
                        events.append((uid, cancel_ts, "cancel_subscription", plan_name))
                    end_dt = None
                    if cancel_ts is not None:
                        # service ends at end of paid period
                        end_dt = cur + dt.timedelta(days=period)
                        end_active = min(end_dt, END_TS)
                        status = "cancelled" if end_dt <= END_TS else "active"
                        end_date = end_dt.strftime("%Y-%m-%d") if end_dt <= END_TS else None
                    else:
                        status, end_date = "active", None
                        end_active = END_TS
                    subs.append([uid, plan_name, cycle, price, ts_.strftime("%Y-%m-%d"), paid_start.strftime("%Y-%m-%d"), end_date, status,
                                 cancel_ts.strftime("%Y-%m-%d") if cancel_ts else None, renewals, None])
        else:
            end_active = s + dt.timedelta(days=14)
        # engagement events
        k_early = min(k_early, 12)
        for _ in range(k_early):
            t = s + dt.timedelta(minutes=int(rng.integers(5, 14 * 24 * 60)))
            events.append((uid, t, rng.choice(["app_open", "content_view", "search"], p=[.5, .38, .12]), plan_name if trial else None))
        paid_days = max((min(end_active, END_TS) - (s + dt.timedelta(days=14))).days, 0)
        if trial and paid_days > 0:
            lam = min(paid_days / 7 * 0.28, 22)
            for _ in range(rng.poisson(lam)):
                t = s + dt.timedelta(days=14, minutes=int(rng.integers(0, paid_days * 1440)))
                events.append((uid, t, rng.choice(["app_open", "content_view", "search"], p=[.45, .43, .12]), plan_name))
    ev = pd.DataFrame(events, columns=["user_id", "event_time", "event_name", "plan"])
    ev = ev[ev["event_time"] <= END_TS].copy()
    ev["platform"] = platform[ev["user_id"].values - 1]
    ev = ev.sort_values(["event_time", "user_id"], kind="stable").reset_index(drop=True)
    ev["event_time"] = ev["event_time"].dt.strftime("%Y-%m-%d %H:%M:%S")
    ev.insert(0, "event_id", np.arange(1, len(ev) + 1))
    ev["event_name"] = case_mess(rng, ev["event_name"].values, 0.0)
    # mess: small share of event_name / platform casing
    m = rng.random(len(ev)) < 0.012
    ev.loc[m, "event_name"] = ev.loc[m, "event_name"].str.upper()
    m2 = rng.random(len(ev)) < 0.02
    ev.loc[m2, "platform"] = ev.loc[m2, "platform"].str.lower()
    # subscriptions table
    sb = pd.DataFrame(subs, columns=["user_id", "plan", "billing_cycle", "price_inr", "trial_start_date", "paid_start_date_tmp", "end_date_tmp", "status", "cancel_date", "renewal_count", "x"])
    # clean: for trial_expired rows tmp holds trial end; reorganise columns
    sb["paid_start_date"] = np.where(sb["status"].isin(["trial_expired", "trialing"]), None, sb["paid_start_date_tmp"])
    sb["end_date"] = np.where(sb["status"] == "trial_expired", sb["paid_start_date_tmp"], np.where(sb["status"] == "trialing", None, sb["end_date_tmp"]))
    sb = sb.sort_values("trial_start_date", kind="stable").reset_index(drop=True)
    sb.insert(0, "subscription_id", np.arange(1, len(sb) + 1))
    sb = sb[["subscription_id", "user_id", "plan", "billing_cycle", "price_inr", "trial_start_date", "paid_start_date", "end_date", "cancel_date", "status", "renewal_count"]]
    sb["price_inr"] = sb["price_inr"].astype(int)
    sb["renewal_count"] = sb["renewal_count"].astype(int)
    users = add_dups(rng, users, n=8)
    ev = add_dups(rng, ev, frac=0.005)

    def csv_users(df, r):
        df["signup_date"] = mix_dates(r, df["signup_date"], 0.15)
        return df

    def csv_subs(df, r):
        df["price_inr"] = rupee_text(r, df["price_inr"], 0.4, decimals=0)
        df["trial_start_date"] = mix_dates(r, df["trial_start_date"], 0.1)
        return df

    def csv_ev(df, r):
        df["event_time"] = mix_dates(r, df["event_time"], 0.1)
        return df

    spec = dict(
        id="subscription", title="Subscription App: Kahani+ Streaming", csv_seed=15,
        description=("Kahani+ is a fictional Indian streaming and learning app with a 7-day free trial and Basic, Standard and Premium plans (monthly or annual, priced in INR). "
                     "The data tracks 5,200 signups from 2023-2024 through trial, first payment, renewals and cancellation, along with a raw event log. "
                     "Use it for funnel conversion, retention curves, cohort analysis, churn drivers and plan mix."),
        tables=[
            dict(name="users", df=users, pk="user_id", desc="One row per signup (8 duplicate rows are deliberate).", csv=csv_users, cols="""
user_id - User identifier (duplicated for duplicate rows)
email - Email (NULL ~6%)
signup_date - Date the user signed up
signup_time - Time of day of signup
city - City (casing issues, ~4% NULL)
platform - Android, iOS or Web at signup
acquisition_source - Acquisition channel
age_group - Age band"""),
            dict(name="subscriptions", df=sb, pk="subscription_id", desc="One row per user who started a free trial; tracks conversion, renewal and end.", csv=csv_subs, cols="""
subscription_id - Subscription identifier (primary key)
user_id - FK to users.user_id
plan - Basic, Standard or Premium
billing_cycle - Monthly or Annual
price_inr - Price per billing period in INR
trial_start_date - Date the free trial started
paid_start_date - Date of first payment (NULL if never converted)
end_date - Trial expiry date (if not converted) or end of paid service (if cancelled); NULL while active/trialing
cancel_date - Date the user requested cancellation (NULL if not cancelled)
status - active, cancelled, trial_expired or trialing
renewal_count - Number of successful renewals after the first payment"""),
            dict(name="events", df=ev, pk="event_id", desc="Raw product and billing event log (~0.5% exact duplicates).", csv=csv_ev, cols="""
event_id - Event identifier (duplicated for duplicate rows)
user_id - FK to users.user_id
event_time - Timestamp of the event
event_name - signup, trial_start, trial_expired, payment_success, renewal_success, payment_failed, cancel_subscription, app_open, content_view, search (some UPPERCASE)
plan - Plan at the time of the event (NULL before a plan is chosen)
platform - Platform of the user (some lowercase values)"""),
        ],
        relationships=[("subscriptions.user_id", "users.user_id"), ("events.user_id", "users.user_id")],
        issues=[
            "events: ~0.5% (about 100) exact duplicate rows (same event_id); users: 8 exact duplicates. Neither table has a PRIMARY KEY constraint on its id.",
            "events.event_name: ~1.2% of values are UPPERCASE ('APP_OPEN'); events.platform: ~2% are lowercase ('android') - breaks naive GROUP BY.",
            "users.email ~6% NULL; users.city ~4% NULL and ~10% inconsistent casing/whitespace.",
            "events.plan is NULL for events before a plan is chosen (signup and most early engagement events); subscriptions.paid_start_date NULL for users who never paid; cancel_date/end_date NULL by design for active users.",
            "CSV only - users.signup_date ~15% and subscriptions.trial_start_date ~10%: DD-MM-YYYY; events.event_time ~10%: DD-MM-YYYY HH:MM:SS.",
            "CSV only - subscriptions.price_inr: ~40% of rows are text such as '₹299'."],
        signals=[
            "Funnel: signup -> trial_start (~63%) -> payment_success (~36% of trials) -> renewals; iOS converts trials noticeably better (~50%) than Android (~34%).",
            "The March 2024 signup cohort churns far faster (about 2.7x hazard) - month-1 and month-2 retention is visibly worse than neighbouring cohorts.",
            "Influencer-sourced users start trials often but convert at less than half the normal rate and churn faster; Referral users convert ~25% better.",
            "Basic plan churns more than Premium; annual plans have almost no churn in the first year but low renewal at month 12.",
            "Oct-Nov (Diwali) cohorts convert ~20% better; signups grow strongly through 2024.",
            "About 3.5% of renewal charges fail (payment_failed), and ~45% of those lead to involuntary cancellation.",
            "Engagement events (app_open, content_view) cluster in the first 14 days after signup and decay for churners."],
    )
    return spec


def run():
    return write_dataset(build())


if __name__ == "__main__":
    run()
