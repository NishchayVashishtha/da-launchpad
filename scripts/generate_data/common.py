"""Shared helpers for the DA Launchpad dataset generators (stdlib + pandas + numpy only)."""
import datetime as dt
import json
import re
import sqlite3
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
PUB = ROOT / "public" / "data"
META_DIR = Path(__file__).resolve().parent / "_meta"

START = dt.date(2023, 1, 1)
END = dt.date(2024, 12, 31)
DAYS = pd.date_range(START, END)            # 731 days
N_DAYS = len(DAYS)
DAY_STR = np.array([d.strftime("%Y-%m-%d") for d in DAYS], dtype=object)
DOW = np.array(DAYS.dayofweek)              # 0=Mon
MONTH = np.array(DAYS.month)

# ---------------------------------------------------------------- reference data
FIRST_M = ["Aarav", "Vivaan", "Aditya", "Arjun", "Rohan", "Karan", "Rahul", "Amit", "Suresh", "Ramesh", "Vikram", "Sanjay",
           "Manoj", "Deepak", "Nikhil", "Siddharth", "Harsh", "Pranav", "Kunal", "Ishaan", "Ravi", "Mohit", "Gaurav", "Tarun",
           "Abhishek", "Yash", "Varun", "Naveen", "Prakash", "Sandeep", "Imran", "Faisal", "Gurpreet", "Harpreet", "Arun", "Karthik",
           "Venkat", "Sunil", "Anil", "Dinesh"]
FIRST_F = ["Aanya", "Diya", "Isha", "Priya", "Neha", "Pooja", "Sneha", "Anjali", "Kavya", "Meera", "Riya", "Shreya", "Divya",
           "Nisha", "Swati", "Ritu", "Ananya", "Aditi", "Sakshi", "Tanvi", "Lakshmi", "Sunita", "Rekha", "Geeta", "Pallavi",
           "Shruti", "Komal", "Nandini", "Zoya", "Fatima", "Simran", "Jasleen", "Deepika", "Madhuri", "Bhavna", "Radhika",
           "Aishwarya", "Padma", "Usha", "Vaishnavi"]
LAST = ["Sharma", "Verma", "Gupta", "Singh", "Patel", "Shah", "Mehta", "Joshi", "Iyer", "Nair", "Reddy", "Rao", "Kulkarni",
        "Deshmukh", "Patil", "Chopra", "Kapoor", "Malhotra", "Bansal", "Agarwal", "Jain", "Mishra", "Pandey", "Tiwari", "Yadav",
        "Das", "Banerjee", "Chatterjee", "Ghosh", "Sen", "Bose", "Menon", "Pillai", "Kurup", "Naidu", "Chowdhury", "Khan",
        "Ansari", "Sheikh", "Qureshi", "Gill", "Sandhu", "Bhatia", "Saxena", "Trivedi", "Desai", "Thakur", "Rathore", "Shetty", "Hegde"]

# city, state, tier, population weight
CITIES = [("Mumbai", "Maharashtra", 1, 14), ("Delhi", "Delhi", 1, 14), ("Bengaluru", "Karnataka", 1, 12),
          ("Hyderabad", "Telangana", 1, 9), ("Chennai", "Tamil Nadu", 1, 8), ("Kolkata", "West Bengal", 1, 7),
          ("Pune", "Maharashtra", 1, 6), ("Ahmedabad", "Gujarat", 1, 5), ("Jaipur", "Rajasthan", 2, 3.5),
          ("Lucknow", "Uttar Pradesh", 2, 3.5), ("Chandigarh", "Chandigarh", 2, 2.5), ("Indore", "Madhya Pradesh", 2, 3),
          ("Kochi", "Kerala", 2, 2.5), ("Nagpur", "Maharashtra", 2, 2.5), ("Surat", "Gujarat", 2, 3),
          ("Bhopal", "Madhya Pradesh", 2, 2), ("Patna", "Bihar", 2, 2), ("Coimbatore", "Tamil Nadu", 2, 2),
          ("Visakhapatnam", "Andhra Pradesh", 2, 2), ("Guwahati", "Assam", 2, 1.5)]
CITY_NAMES = [c[0] for c in CITIES]
CITY_STATE = {c[0]: c[1] for c in CITIES}
CITY_TIER = {c[0]: c[2] for c in CITIES}
CITY_W = np.array([c[3] for c in CITIES], dtype=float)
CITY_W = CITY_W / CITY_W.sum()

# fictional UPI banks / apps
BANKS = ["Bharat Union Bank", "Sundaram Bank", "Kaveri Co-op Bank", "Himalaya Trust Bank", "Rajdhani National Bank",
         "Coromandel Bank", "Malabar Savings Bank", "PayNova Small Finance Bank"]
UPI_APPS = ["PayZippy", "QuickPaisa", "NammaPay", "SabPay", "RupeeRocket"]


def rng_for(seed):
    return np.random.default_rng(seed)


# ---------------------------------------------------------------- generic helpers
def choice(rng, options, n, p=None):
    options = list(options)
    idx = rng.choice(len(options), size=n, p=p)
    return np.array(options, dtype=object)[idx]


def full_names(rng, n, genders=None):
    if genders is None:
        genders = choice(rng, ["Male", "Female"], n, p=[0.55, 0.45])
    first = np.where(genders == "Male", choice(rng, FIRST_M, n), choice(rng, FIRST_F, n))
    last = choice(rng, LAST, n)
    return np.array([f"{a} {b}" for a, b in zip(first, last)], dtype=object), genders


def phones(rng, n):
    first = rng.choice([6, 7, 8, 9], size=n, p=[0.05, 0.2, 0.25, 0.5])
    rest = rng.integers(0, 10**9, size=n)
    return np.array([f"{a}{b:09d}" for a, b in zip(first, rest)], dtype=object)


def emails(rng, names, domain_choices=("gmail.com", "yahoo.in", "outlook.com", "rediffmail.com", "hotmail.com"), ids=None):
    doms = choice(rng, domain_choices, len(names), p=[0.6, 0.15, 0.12, 0.08, 0.05] if len(domain_choices) == 5 else None)
    out = []
    for i, (nm, d) in enumerate(zip(names, doms)):
        base = nm.lower().replace(" ", ".")
        out.append(f"{base}{rng.integers(1, 999) if rng.random() < 0.7 else ''}@{d}")
    return np.array(out, dtype=object)


def nullify(rng, arr, frac):
    a = np.array(arr, dtype=object)
    mask = rng.random(len(a)) < frac
    a[mask] = None
    return a


def case_mess(rng, arr, frac):
    """Inconsistent casing / stray whitespace on a fraction of non-null text values."""
    a = np.array(arr, dtype=object)
    for i in np.where(rng.random(len(a)) < frac)[0]:
        v = a[i]
        if v is None or (isinstance(v, float) and np.isnan(v)):
            continue
        k = rng.integers(0, 5)
        a[i] = [v.lower(), v.upper(), " " + v, v + " ", " " + v.lower() + "  "][k]
    return a


def add_dups(rng, df, frac=None, n=None):
    """Insert exact duplicate rows right after their originals."""
    k = n if n is not None else int(round(len(df) * frac))
    pick = rng.choice(len(df), size=k, replace=False)
    pos = np.arange(len(df), dtype=float)
    d = df.iloc[pick].copy()
    full = pd.concat([df, d], ignore_index=True)
    full["_pos"] = np.concatenate([pos, pick + 0.5])
    full = full.sort_values("_pos", kind="stable").drop(columns="_pos").reset_index(drop=True)
    return full


def day_weights(growth=0.4, weekend=1.15, festive=1.0, ipl=1.0, monsoon=1.0, monthend=1.0, sales=1.0):
    """Daily volume weights over 2023-2024 with growth, weekend, festive, IPL, monsoon patterns."""
    t = np.arange(N_DAYS) / (N_DAYS - 1)
    w = 1 + growth * t
    w = w * np.where(DOW >= 5, weekend, 1.0)
    f = np.ones(N_DAYS)

    def bump(a, b, m):
        s = (DAYS >= pd.Timestamp(a)) & (DAYS <= pd.Timestamp(b))
        f[np.array(s)] *= m
    # festive: Diwali 2023-11-12, 2024-11-01; Navratri/Dussehra sale windows; Republic Day, Independence Day sales
    bump("2023-10-08", "2023-10-16", 1 + 0.6 * (festive - 1))
    bump("2023-11-06", "2023-11-14", festive)
    bump("2024-09-27", "2024-10-06", 1 + 0.6 * (festive - 1))
    bump("2024-10-24", "2024-11-03", festive)
    bump("2023-01-18", "2023-01-26", sales)
    bump("2024-01-18", "2024-01-26", sales)
    bump("2023-08-05", "2023-08-15", sales)
    bump("2024-08-05", "2024-08-15", sales)
    bump("2023-12-24", "2024-01-01", 1 + (sales - 1) * 0.6)
    bump("2023-03-31", "2023-05-28", ipl)     # IPL 2023
    bump("2024-03-22", "2024-05-26", ipl)     # IPL 2024
    bump("2023-06-10", "2023-09-25", monsoon)
    bump("2024-06-10", "2024-09-25", monsoon)
    w = w * f
    # salary days / month-end bump
    dom = np.array(DAYS.day)
    w = w * np.where((dom <= 3) | (dom >= 28), monthend, 1.0)
    return w / w.sum()


def sample_days(rng, n, weights):
    return rng.choice(N_DAYS, size=n, p=weights)


def make_times(rng, day_idx, hour_p):
    hour_p = np.array(hour_p, dtype=float)
    hour_p = hour_p / hour_p.sum()
    hrs = rng.choice(24, size=len(day_idx), p=hour_p)
    secs = hrs * 3600 + rng.integers(0, 3600, size=len(day_idx))
    ts = DAYS[day_idx] + pd.to_timedelta(secs, unit="s")
    return np.array(ts.strftime("%Y-%m-%d %H:%M:%S"), dtype=object), hrs


def add_days(date_strs, offsets):
    """date_strs: ISO strings (date or datetime); offsets: array of days (can be float, minutes via fractions)."""
    ts = pd.to_datetime(pd.Series(date_strs)) + pd.to_timedelta(np.asarray(offsets, dtype=float), unit="D")
    return ts


def fmt_date(ts):
    return np.array(ts.dt.strftime("%Y-%m-%d"), dtype=object)


def fmt_dt(ts):
    return np.array(ts.dt.strftime("%Y-%m-%d %H:%M:%S"), dtype=object)


def pick_by_signup(rng, day_idx, signup_idx_sorted, cumw):
    """Pick customer indexes (into the signup-sorted array) who had signed up on/before each day, weighted by activity."""
    cutoff = np.searchsorted(signup_idx_sorted, day_idx, side="right")   # count signed up
    cutoff = np.maximum(cutoff, 1)
    u = rng.random(len(day_idx)) * cumw[cutoff - 1]
    return np.minimum(np.searchsorted(cumw, u, side="right"), cutoff - 1)


# ---------------------------------------------------------------- CSV-only messiness
def indian_fmt(x, decimals=0):
    neg = x < 0
    x = abs(x)
    s = f"{x:.{decimals}f}"
    ip, _, fp = s.partition(".")
    if len(ip) > 3:
        head, tail = ip[:-3], ip[-3:]
        parts = []
        while len(head) > 2:
            parts.insert(0, head[-2:])
            head = head[:-2]
        if head:
            parts.insert(0, head)
        ip = ",".join(parts) + "," + tail
    out = ip + ("." + fp if fp else "")
    return ("-" if neg else "") + out


def rupee_text(rng, series, frac, decimals=2, indian=False, symbol=True):
    """CSV only: turn a fraction of numeric values into text like '₹1,234.50' (rest stay plain numbers)."""
    s = pd.Series(series)
    out = s.astype(object).copy()
    mask = rng.random(len(s)) < frac
    for i in np.where(mask & s.notna().values)[0]:
        v = float(s.iloc[i])
        body = indian_fmt(v, decimals) if indian else f"{v:,.{decimals}f}"
        out.iloc[i] = ("₹" if symbol else "") + body
    return out


def mix_dates(rng, series, frac):
    """CSV only: convert a fraction of ISO date/datetime strings to DD-MM-YYYY[ HH:MM[:SS]]."""
    s = pd.Series(series).astype(object).copy()
    mask = rng.random(len(s)) < frac
    for i in np.where(mask & s.notna().values)[0]:
        v = s.iloc[i]
        d = v[:10]
        y, m, dd = d.split("-")
        s.iloc[i] = f"{dd}-{m}-{y}" + v[10:]
    return s


# ---------------------------------------------------------------- writer
def _sqltype(dtype):
    k = str(dtype)
    if k.startswith(("int", "Int", "uint", "bool")):
        return "INTEGER"
    if k.startswith(("float", "Float")):
        return "REAL"
    return "TEXT"


_ISO_D = re.compile(r"^\d{4}-\d{2}-\d{2}$")
_ISO_DT = re.compile(r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$")


def _coltype_label(series, sqltype):
    if sqltype != "TEXT":
        return sqltype
    nn = series.dropna()
    if len(nn) and all(_ISO_D.match(str(v)) for v in nn.iloc[:200]):
        return "DATE"
    if len(nn) and all(_ISO_DT.match(str(v)) for v in nn.iloc[:200]):
        return "DATETIME"
    return "TEXT"


def _example(series):
    nn = series.dropna()
    if not len(nn):
        return ""
    v = nn.iloc[min(2, len(nn) - 1)]
    if isinstance(v, (float, np.floating)):
        return str(round(float(v), 2))
    return str(v).strip() if isinstance(v, str) else str(v)


def parse_cols(text):
    out = {}
    for line in text.strip().splitlines():
        if "-" in line:
            k, v = line.split(" - ", 1)
            out[k.strip()] = v.strip()
    return out


def write_dataset(spec):
    """spec: id,title,description,tables(list of dict name,df,desc,cols,pk,csv(optional fn(df,rng)->df)),
    relationships(list of (from,to)), issues, signals, csv_seed."""
    did = spec["id"]
    (PUB / "sqlite").mkdir(parents=True, exist_ok=True)
    (PUB / "csv" / did).mkdir(parents=True, exist_ok=True)
    (PUB / "zip").mkdir(parents=True, exist_ok=True)
    META_DIR.mkdir(parents=True, exist_ok=True)
    dbp = PUB / "sqlite" / f"{did}.sqlite"
    if dbp.exists():
        dbp.unlink()
    con = sqlite3.connect(dbp)
    meta_tables = []
    fks = {}
    for a, _b in spec["relationships"]:
        t, c = a.split(".")
        fks.setdefault(t, []).append(c)
    csv_rng = np.random.default_rng(spec.get("csv_seed", 7))
    csv_files = []
    for t in spec["tables"]:
        name, df = t["name"], t["df"].reset_index(drop=True)
        descs = parse_cols(t["cols"])
        missing = [c for c in df.columns if c not in descs]
        assert not missing, f"{name}: no description for {missing}"
        pk = t.get("pk")
        pk_ok = pk is not None and df[pk].is_unique
        defs = []
        for c in df.columns:
            ty = _sqltype(df[c].dtype)
            defs.append(f'"{c}" {ty}' + (" PRIMARY KEY" if (c == pk and pk_ok) else ""))
        con.execute(f'CREATE TABLE "{name}" ({", ".join(defs)})')
        rows = df.astype(object).where(df.notna(), None).values.tolist()
        con.executemany(f'INSERT INTO "{name}" VALUES ({",".join("?" * len(df.columns))})', rows)
        for c in fks.get(name, []):
            con.execute(f'CREATE INDEX "idx_{name}_{c}" ON "{name}"("{c}")')
        if pk and not pk_ok:
            con.execute(f'CREATE INDEX "idx_{name}_{pk}" ON "{name}"("{pk}")')
        for c in t.get("index", []):
            con.execute(f'CREATE INDEX "idx_{name}_{c}" ON "{name}"("{c}")')
        # csv (with optional CSV-only messiness)
        out = df.copy()
        if t.get("csv"):
            out = t["csv"](out, csv_rng)
        fp = PUB / "csv" / did / f"{name}.csv"
        out.to_csv(fp, index=False, encoding="utf-8", lineterminator="\n")
        csv_files.append(fp)
        cols = []
        for c in df.columns:
            ty = _sqltype(df[c].dtype)
            cols.append({"name": c, "type": _coltype_label(df[c], ty), "description": descs[c],
                         "nullable": bool(df[c].isna().any()) or c in t.get("nullable", []),
                         "example": _example(df[c])})
        meta_tables.append({"name": name, "rowCount": int(len(df)), "description": t["desc"], "columns": cols})
    con.commit()
    con.close()
    # zip (fixed timestamps for determinism)
    zp = PUB / "zip" / f"{did}.zip"
    with zipfile.ZipFile(zp, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for fp in csv_files:
            zi = zipfile.ZipInfo(f"{did}/{fp.name}", date_time=(2024, 1, 1, 0, 0, 0))
            zi.compress_type = zipfile.ZIP_DEFLATED
            z.writestr(zi, fp.read_bytes())
    # ER diagram
    pkmap = {t["name"]: t.get("pk") for t in spec["tables"]}
    fkcols = {(a.split(".")[0], a.split(".")[1]) for a, _ in spec["relationships"]}
    er = ["erDiagram"]
    for mt in meta_tables:
        er.append(f"  {mt['name']} {{")
        for c in mt["columns"]:
            ty = "TEXT" if c["type"] in ("DATE", "DATETIME") else c["type"]
            key = " PK" if pkmap[mt["name"]] == c["name"] else (" FK" if (mt["name"], c["name"]) in fkcols else "")
            er.append(f"    {ty} {c['name']}{key}")
        er.append("  }")
    for a, b in spec["relationships"]:
        ft, _ = a.split(".")
        tt, _ = b.split(".")
        er.append(f'  {tt} ||--o{{ {ft} : "{a.split(".")[1]}"')
    meta = {
        "id": did, "title": spec["title"], "description": spec["description"], "tables": meta_tables,
        "relationships": [{"from": a, "to": b, "type": "many-to-one"} for a, b in spec["relationships"]],
        "qualityIssues": spec["issues"], "er": "\n".join(er),
        "downloads": {"sqlite": f"data/sqlite/{did}.sqlite", "zip": f"data/zip/{did}.zip",
                      "csv": [f"data/csv/{did}/{t['name']}.csv" for t in spec["tables"]]},
        "signals": ["[Instructor note] " + s for s in spec["signals"]],
    }
    (META_DIR / f"{did}.json").write_text(json.dumps(meta, indent=2, ensure_ascii=False), encoding="utf-8")
    return meta
