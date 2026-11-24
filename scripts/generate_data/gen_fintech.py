"""Dataset 4: fintech (fictional UPI-style payments: apps PayZippy, QuickPaisa, NammaPay, SabPay, RupeeRocket)."""
import numpy as np
import pandas as pd
from common import *

SEED = 20230104
OUTAGE_APP = "NammaPay"
# (date, start hour, end hour exclusive, extra retry attempts): four NammaPay outages
OUTAGE_WINDOWS = [("2023-03-14", 10, 13, 75), ("2023-09-21", 18, 22, 75), ("2024-02-06", 9, 12, 75), ("2024-07-16", 19, 22, 75)]

MCATS = {  # category: (weight, median ticket, sigma)
    "Grocery": (0.2, 320, 0.7), "Food & Beverage": (0.17, 260, 0.6), "Fuel": (0.07, 1300, 0.45), "Pharmacy": (0.07, 450, 0.7),
    "Telecom": (0.06, 299, 0.5), "Electronics": (0.04, 4800, 0.9), "Travel": (0.08, 2400, 0.9), "Entertainment": (0.07, 420, 0.6),
    "Utilities": (0.08, 1400, 0.7), "Fashion": (0.1, 1700, 0.8), "Education": (0.03, 5200, 0.8), "Healthcare": (0.03, 1800, 0.9)}


def build():
    rng = rng_for(SEED)
    # ---- users
    nu = 4000
    pre = rng.random(nu) < 0.35
    sig = np.where(pre, -1, sample_days(rng, nu, day_weights(growth=1.0, festive=1.2)))
    sig = np.sort(sig)
    pre = sig < 0
    pre_dates = np.array((pd.to_datetime("2022-01-01") + pd.to_timedelta(rng.integers(0, 365, nu), unit="D")).strftime("%Y-%m-%d"), dtype=object)
    sdate = np.where(pre, pre_dates, DAY_STR[np.maximum(sig, 0)]).astype(object)
    sdate = np.sort(sdate.astype(str)).astype(object)
    names, _ = full_names(rng, nu)
    city = choice(rng, CITY_NAMES, nu, p=CITY_W)
    bank = choice(rng, BANKS, nu, p=[.25, .2, .09, .12, .16, .1, .05, .03])
    app = choice(rng, UPI_APPS, nu, p=[.34, .26, .16, .14, .10])
    handles = {"Bharat Union Bank": "bub", "Sundaram Bank": "sdm", "Kaveri Co-op Bank": "kcb", "Himalaya Trust Bank": "htb",
               "Rajdhani National Bank": "rnb", "Coromandel Bank": "cor", "Malabar Savings Bank": "mal", "PayNova Small Finance Bank": "pnv"}
    ph = phones(rng, nu)
    upi = np.array([f"{p}@{handles[b]}" for p, b in zip(ph, bank)], dtype=object)
    users = pd.DataFrame({
        "user_id": np.arange(1, nu + 1), "full_name": names, "phone": nullify(rng, ph, 0.02), "city": nullify(rng, case_mess(rng, city, 0.1), 0.03),
        "state": [CITY_STATE[c] for c in city], "age_group": choice(rng, ["18-24", "25-34", "35-44", "45-60", "60+"], nu, p=[.22, .38, .22, .14, .04]),
        "kyc_status": choice(rng, ["Full KYC", "Min KYC", "Pending"], nu, p=[.72, .22, .06]), "primary_bank": bank, "preferred_app": app,
        "upi_id": nullify(rng, upi, 0.05), "signup_date": sdate})
    sig_idx = np.where(sdate < "2023-01-01", -1, pd.Series(sdate).map({d: i for i, d in enumerate(DAY_STR)}).fillna(-1)).astype(int)
    act = rng.gamma(0.7, 1.0, nu)
    cumw = np.cumsum(act)
    # ---- merchants
    nm = 400
    cats = list(MCATS)
    mcat = choice(rng, cats, nm, p=np.array([MCATS[c][0] for c in cats]) / sum(MCATS[c][0] for c in cats))
    mcity = choice(rng, CITY_NAMES, nm, p=CITY_W)
    suffix = {"Grocery": ["Kirana Store", "Fresh Mart", "Bazaar"], "Food & Beverage": ["Chai Point", "Biryani House", "Cafe", "Sweets"],
              "Fuel": ["Petro Pump", "Fuel Station"], "Pharmacy": ["Medico", "Chemist", "Pharmacy"], "Telecom": ["Recharge Hub", "Mobile Care"],
              "Electronics": ["Electronics", "Mobile World"], "Travel": ["Travels", "Cabs", "Tours"], "Entertainment": ["Cinemas", "Gaming Zone", "OTT Pack"],
              "Utilities": ["Power Board", "Gas Agency", "Water Works"], "Fashion": ["Fashions", "Boutique", "Textiles"], "Education": ["Academy", "Classes"],
              "Healthcare": ["Clinic", "Diagnostics"]}
    pre_n = ["Sri", "Shree", "Lakshmi", "New", "Royal", "Ganesh", "Balaji", "Krishna", "Metro", "City", "Super", "Anand", "Om", "Sai", "Annapurna"]
    mname = np.array([f"{pre_n[rng.integers(len(pre_n))]} {suffix[c][rng.integers(len(suffix[c]))]}" for c in mcat], dtype=object)
    merchants = pd.DataFrame({
        "merchant_id": np.arange(1, nm + 1), "merchant_name": mname, "category": mcat,
        "city": case_mess(rng, mcity, 0.08), "onboarding_date": fmt_date(add_days(["2021-01-01"] * nm, rng.integers(0, 1700, nm))),
        "is_verified": (rng.random(nm) < 0.88).astype(int)})
    merchants["mcc_code"] = pd.Series(mcat).map({"Grocery": 5411, "Food & Beverage": 5812, "Fuel": 5541, "Pharmacy": 5912, "Telecom": 4814, "Electronics": 5732,
                                                 "Travel": 4722, "Entertainment": 7832, "Utilities": 4900, "Fashion": 5651, "Education": 8299, "Healthcare": 8099}).values
    mpop = rng.pareto(1.3, nm) + 1
    # ---- transactions
    nb = 22000
    w = day_weights(growth=0.7, weekend=1.1, festive=1.45, monthend=1.18, sales=1.15)
    day = np.sort(sample_days(rng, nb, w))
    ts, hrs = make_times(rng, day, [.4, .2, .1, .1, .1, .3, .8, 2, 4, 5, 5, 4, 4.5, 4, 3.5, 3.5, 4, 5, 6.5, 6.5, 5, 3.5, 2, 1])
    # outage windows: NammaPay retry-storm attempts added on top of the base volume (about 300 rows across 4 windows of 3-4 hours)
    xd, xh = [], []
    for d, h0, h1, k in OUTAGE_WINDOWS:
        xd += [int((pd.Timestamp(d) - DAYS[0]).days)] * k
        xh += list(rng.integers(h0, h1, k))
    xd, xh = np.array(xd), np.array(xh)
    xts = np.array((DAYS[xd] + pd.to_timedelta(xh * 3600 + rng.integers(0, 3600, len(xd)), unit="s")).strftime("%Y-%m-%d %H:%M:%S"), dtype=object)
    day = np.concatenate([day, xd])
    ts = np.concatenate([ts, xts])
    hrs = np.concatenate([hrs, xh])
    isx = np.concatenate([np.zeros(nb, bool), np.ones(len(xd), bool)])
    o = np.argsort(ts, kind="stable")
    day, ts, hrs, isx = day[o], ts[o], hrs[o], isx[o]
    n = len(day)
    uidx = pick_by_signup(rng, day, sig_idx, cumw)
    ttype = choice(rng, ["P2M", "P2P", "Bill Pay", "Recharge"], n, p=[.55, .24, .13, .08])
    amount = np.zeros(n)
    mid = np.full(n, 0)
    rid = np.full(n, 0)
    for t in ["P2M", "Bill Pay", "Recharge", "P2P"]:
        m = np.where(ttype == t)[0]
        if t == "P2P":
            rid[m] = rng.integers(1, nu + 1, len(m))
            amount[m] = np.exp(rng.normal(np.log(700), 1.0, len(m)))
            continue
        allowed = {"P2M": cats, "Bill Pay": ["Utilities", "Education", "Healthcare", "Entertainment"], "Recharge": ["Telecom"]}[t]
        mi = np.where(np.isin(mcat, allowed))[0]
        mid[m] = rng.choice(mi, len(m), p=mpop[mi] / mpop[mi].sum()) + 1
        for j in m:
            c = mcat[mid[j] - 1]
            amount[j] = np.exp(rng.normal(np.log(MCATS[c][1]), MCATS[c][2]))
    amount = np.round(np.clip(amount, 1, 100000), 2)
    # outliers: 6 rows x100 (entry/decimal errors)
    oi = rng.choice(np.where(amount < 3000)[0], 6, replace=False)
    amount[oi] = np.round(amount[oi] * 100, 2)
    ubank = bank[uidx]
    uapp = app[uidx]
    appx = np.where(rng.random(n) < 0.9, uapp, choice(rng, UPI_APPS, n))
    appx = np.where(isx, OUTAGE_APP, appx)
    in_win = np.zeros(n, bool)
    for d, h0, h1, _k in OUTAGE_WINDOWS:
        in_win |= (day == int((pd.Timestamp(d) - DAYS[0]).days)) & (hrs >= h0) & (hrs < h1)
    outage = in_win & (appx == OUTAGE_APP)
    os_ = np.where(rng.random(n) < 0.83, "Android", "iOS")
    peak = np.isin(hrs, [9, 10, 18, 19, 20])
    dom = DAYS.day.values[day]
    pf = 0.022 * np.ones(n)
    kc = ubank == "Kaveri Co-op Bank"
    pf = pf + np.where(kc, 0.02, 0) + np.where(kc & peak, 0.085, 0)
    pf = pf * np.where(dom <= 3, 1.35, 1.0) * np.where(amount > 50000, 2.5, 1.0) * np.where(os_ == "iOS", 0.9, 1.0)
    pf = pf + np.where(ubank == "PayNova Small Finance Bank", 0.012, 0)
    pf = np.where(outage, 0.42, pf * 0.85)   # 0.85 keeps total failed rows close to the earlier volume
    failed = rng.random(n) < pf
    pend = (~failed) & (rng.random(n) < 0.003)
    status = np.where(failed, "FAILED", np.where(pend, "PENDING", "SUCCESS")).astype(object)
    # fraud flag: several learnable risk factors (about 1.5% of rows overall)
    night = np.isin(hrs, [23, 0, 1, 2, 3, 4])
    age_days = (pd.to_datetime(pd.Series(DAY_STR[day])) - pd.to_datetime(pd.Series(sdate[uidx]))).dt.days.values
    new_acct = age_days < 30
    med_amt = pd.Series(amount).groupby(uidx).transform("median").values
    big_vs_median = amount > 3 * med_amt
    tcat = np.array(["none"] + list(mcat), dtype=object)[mid]
    risky_cat = np.isin(tcat, ["Electronics", "Travel", "Entertainment"])
    flag_p = 0.006 * np.where(night, 3.5, 1.0) * np.where(new_acct, 5.0, 1.0) * np.where(big_vs_median, 4.0, 1.0) * np.where(risky_cat, 2.5, 1.0)
    flag_p = np.where((ttype == "P2P") & night & (amount > 8000), 0.3, flag_p)
    flagged = ((rng.random(n) < np.clip(flag_p, 0, 0.9)) & (~failed)).astype(int)
    txn = pd.DataFrame({
        "txn_id": np.arange(1, n + 1), "user_id": uidx + 1, "merchant_id": pd.array(np.where(mid == 0, -1, mid)).astype("Int64"),
        "receiver_user_id": pd.array(np.where(rid == 0, -1, rid)).astype("Int64"), "txn_type": ttype, "txn_datetime": ts, "amount": amount,
        "payment_app": appx, "bank": ubank, "device_os": os_, "status": status, "is_flagged": flagged})
    txn.loc[txn["merchant_id"] == -1, "merchant_id"] = pd.NA
    txn.loc[txn["receiver_user_id"] == -1, "receiver_user_id"] = pd.NA
    # ---- failed transactions
    fi = np.where(failed)[0]
    codes = []
    for i in fi:
        if outage[i]:
            c = "UPI_SYSTEM_DOWN"
        elif kc[i] and peak[i] and rng.random() < 0.7:
            c = "BANK_SERVER_TIMEOUT"
        else:
            pr = [.30, .18, .14, .16, .22] if amount[i] <= 50000 else [.1, .05, .65, .1, .1]
            c = ["INSUFFICIENT_FUNDS", "INCORRECT_PIN", "LIMIT_EXCEEDED", "NETWORK_ERROR", "BANK_DECLINED"][rng.choice(5, p=pr)]
        codes.append(c)
    reason = {"INSUFFICIENT_FUNDS": "Insufficient balance in account", "INCORRECT_PIN": "Wrong UPI PIN entered", "LIMIT_EXCEEDED": "Daily/transaction limit exceeded",
              "NETWORK_ERROR": "Network error during authorisation", "BANK_DECLINED": "Declined by remitter bank", "BANK_SERVER_TIMEOUT": "Remitter bank server timed out",
              "UPI_SYSTEM_DOWN": "UPI switch unavailable"}
    codes = np.array(codes, dtype=object)
    retried = (rng.random(len(fi)) < np.where(np.isin(codes, ["BANK_SERVER_TIMEOUT", "NETWORK_ERROR", "UPI_SYSTEM_DOWN"]), 0.7, 0.4)).astype(int)
    retry_ok = np.where(retried == 1, (rng.random(len(fi)) < np.where(codes == "INCORRECT_PIN", 0.85, np.where(codes == "INSUFFICIENT_FUNDS", 0.2, 0.65))).astype(int), -1)
    failed_at = pd.to_datetime(pd.Series(ts[fi])) + pd.to_timedelta(rng.integers(3, 90, len(fi)), unit="s")
    ft = pd.DataFrame({"failed_txn_id": np.arange(1, len(fi) + 1), "txn_id": fi + 1, "failure_code": codes, "failure_reason": [reason[c] for c in codes],
                       "failed_at": np.array(failed_at.dt.strftime("%Y-%m-%d %H:%M:%S"), dtype=object), "retried": retried,
                       "retry_succeeded": pd.array(retry_ok).astype("Int64")})
    ft.loc[ft["retry_succeeded"] == -1, "retry_succeeded"] = pd.NA
    txn = add_dups(rng, txn, frac=0.004)
    ft = add_dups(rng, ft, n=6)
    users = add_dups(rng, users, n=10)

    def csv_users(df, r):
        df["signup_date"] = mix_dates(r, df["signup_date"], 0.15)
        return df

    def csv_txn(df, r):
        df["txn_datetime"] = mix_dates(r, df["txn_datetime"], 0.15)
        df["amount"] = rupee_text(r, df["amount"], 0.12, indian=True)
        return df

    def csv_ft(df, r):
        df["failed_at"] = mix_dates(r, df["failed_at"], 0.2)
        return df

    spec = dict(
        id="fintech", title="Fintech: UPI-style Payments (PayZippy and friends)", csv_seed=14,
        description=("A fictional UPI-style digital payments ecosystem with five payment apps, eight banks and 400 merchants across India. "
                     "Transactions cover P2P transfers, merchant payments, bill payments and recharges over two years, with salary-day, festive and evening peaks plus four NammaPay outages. "
                     "Use it for failure-rate analysis, peak-hour load, merchant category insights and simple fraud-flag exploration."),
        tables=[
            dict(name="users", df=users, pk="user_id", desc="App users (10 duplicate rows are deliberate).", csv=csv_users, cols="""
user_id - User identifier (duplicated for duplicate rows)
full_name - User name
phone - Mobile number (NULL ~2%)
city - City (casing/whitespace issues, ~3% NULL)
state - State of the city
age_group - Age band
kyc_status - Full KYC, Min KYC or Pending
primary_bank - Linked bank (fictional)
preferred_app - UPI app the user mostly uses
upi_id - Virtual payment address (NULL ~5%)
signup_date - Registration date"""),
            dict(name="merchants", df=merchants, pk="merchant_id", desc="Merchants accepting UPI.", cols="""
merchant_id - Merchant identifier (primary key)
merchant_name - Merchant name
category - Business category
city - City (casing issues)
onboarding_date - Date merchant was onboarded
is_verified - 1 if KYB verified
mcc_code - Merchant category code"""),
            dict(name="transactions", df=txn, pk="txn_id", desc="All payment attempts, successful or not (~0.4% exact duplicates).", csv=csv_txn, cols="""
txn_id - Transaction identifier (duplicated for duplicate rows)
user_id - FK to users.user_id (payer)
merchant_id - FK to merchants.merchant_id (NULL for P2P)
receiver_user_id - FK to users.user_id for P2P (NULL otherwise)
txn_type - P2M, P2P, Bill Pay or Recharge
txn_datetime - Timestamp of the attempt
amount - Amount in INR (6 rows are 100x outliers)
payment_app - App used
bank - Payer's bank
device_os - Android or iOS
status - SUCCESS, FAILED or PENDING
is_flagged - 1 if flagged by risk rules"""),
            dict(name="failed_transactions", df=ft, pk="failed_txn_id", desc="Details for transactions with status FAILED (6 duplicate rows are deliberate).", csv=csv_ft, cols="""
failed_txn_id - Failure record identifier (duplicated for duplicate rows)
txn_id - FK to transactions.txn_id
failure_code - Machine failure code
failure_reason - Human readable reason
failed_at - Timestamp of failure
retried - 1 if the user retried
retry_succeeded - 1/0 result of retry (NULL if not retried)"""),
        ],
        relationships=[("transactions.user_id", "users.user_id"), ("transactions.merchant_id", "merchants.merchant_id"),
                       ("transactions.receiver_user_id", "users.user_id"), ("failed_transactions.txn_id", "transactions.txn_id")],
        issues=[
            "transactions: ~0.4% (about 90) rows are exact duplicates (same txn_id), so txn_id has no PRIMARY KEY constraint; users: 10 exact duplicate rows; failed_transactions: 6 exact duplicates.",
            "transactions.amount: 6 rows are 100x outliers.",
            "transactions.merchant_id is NULL for P2P rows (~24%) and receiver_user_id is NULL for non-P2P rows - by design, not an error.",
            "users.city ~10% inconsistent casing/whitespace and ~3% NULL; users.phone ~2% NULL; users.upi_id ~5% NULL; merchants.city ~8% inconsistent casing.",
            "failed_transactions.retry_succeeded is NULL when retried = 0 (~40% of rows).",
            "CSV only - users.signup_date: ~15% of rows are DD-MM-YYYY.",
            "CSV only - transactions.txn_datetime: ~15% DD-MM-YYYY HH:MM:SS; transactions.amount: ~12% text with rupee symbol and Indian grouping.",
            "CSV only - failed_transactions.failed_at: ~20% DD-MM-YYYY."],
        signals=[
            "Kaveri Co-op Bank has a much higher failure rate than other banks, concentrated in peak hours (9-10h and 18-20h) with code BANK_SERVER_TIMEOUT (about 15% at peak vs ~2% elsewhere).",
            "NammaPay had four outage windows (2023-03-14 10-13h, 2023-09-21 18-22h, 2024-02-06 9-12h, 2024-07-16 19-22h). Inside them about 42% of NammaPay attempts fail with UPI_SYSTEM_DOWN, vs ~2-3% normally.",
            "Failures are ~35% higher on the 1st-3rd of the month (salary days) and amounts above 50,000 fail 2.5x more (LIMIT_EXCEEDED).",
            "Volume spikes around Diwali windows and month-end; weekends are ~10% higher; evening 18-20h is the busiest slot.",
            "Network/timeouts are retried and succeed far more often than insufficient-funds failures.",
            "About 1.5% of transactions are flagged (is_flagged = 1). Flags cluster in late-night hours (23h-4h), in accounts less than 30 days old, when an amount is more than 3x the payer's usual median, and for Electronics, Travel and Entertainment merchants. Large late-night P2P transfers (> 8,000) are the strongest signal (~30% flagged).",
            "Customer activity is heavy-tailed; merchant volume is power-law distributed; Fuel/Travel/Electronics have high ticket sizes."],
    )
    return spec


def run():
    return write_dataset(build())


if __name__ == "__main__":
    run()
