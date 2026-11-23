"""Generate the Excel practice workbooks and their reference doc.

Reads CSVs from public/data/csv/<dataset>/<table>.csv and writes:
  public/data/excel/*.xlsx        (six practice workbooks, each with a README sheet first)
  docs/excel-workbooks.md         (exact sheet/column/row-count reference for content agents)

Deterministic: every random draw uses RANDOM_STATE = 42.
Run with: .venv/bin/python scripts/generate_data/excel_workbooks.py
"""
from __future__ import annotations

import datetime as dt
import math
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd
from openpyxl import Workbook, load_workbook
from openpyxl.styles import Alignment, Font
from openpyxl.utils import get_column_letter
from openpyxl.workbook.properties import CalcProperties
from openpyxl.worksheet.table import Table, TableStyleInfo

RANDOM_STATE = 42
ROOT = Path(__file__).resolve().parents[2]
CSV_DIR = ROOT / "public" / "data" / "csv"
OUT_DIR = ROOT / "public" / "data" / "excel"
DOC_PATH = ROOT / "docs" / "excel-workbooks.md"
MAX_BYTES = int(1.5 * 1024 * 1024)
AS_OF = pd.Timestamp("2024-12-31")
FIXED_TS = dt.datetime(2026, 1, 1)
DATE_FMT = "yyyy-mm-dd"
MONEY_FMT = "#,##0.00"
INR_FMT = '[>=10000000]"₹"##\\,##\\,##\\,##0;[>=100000]"₹"##\\,##\\,##0;"₹"##,##0'
PCT_FMT = "0.0%"


# --------------------------------------------------------------------------- helpers
def load(dataset: str, table: str) -> pd.DataFrame:
    """Read a source CSV with every column as text; callers convert types explicitly."""
    return pd.read_csv(CSV_DIR / dataset / f"{table}.csv", dtype=str)


def num(s: pd.Series) -> pd.Series:
    """Convert text such as '₹1,780.25' or '356.0' to float (NaN when blank)."""
    return pd.to_numeric(s.str.replace(r"[₹,\s]", "", regex=True), errors="coerce")


def whole(s: pd.Series) -> pd.Series:
    return num(s).round().astype("Int64")


def clean_text(s: pd.Series) -> pd.Series:
    return s.str.strip().str.replace(r"\s+", " ", regex=True)


def title_text(s: pd.Series) -> pd.Series:
    return clean_text(s).str.title()


def parse_iso(s: pd.Series) -> pd.Series:
    """Parse YYYY-MM-DD and DD-MM-YYYY / DD/MM/YYYY text (the source CSVs mix them)."""
    s = s.str.strip()
    out = pd.Series(pd.NaT, index=s.index, dtype="datetime64[ns]")
    iso = s.str.match(r"^\d{4}-\d{2}-\d{2}", na=False)
    dmy = s.str.match(r"^\d{2}[-/]\d{2}[-/]\d{4}", na=False)
    out[iso] = pd.to_datetime(s[iso].str[:10], format="%Y-%m-%d")
    out[dmy] = pd.to_datetime(s[dmy].str.replace("/", "-").str[:10], format="%d-%m-%Y")
    return out


def parse_mixed(s: pd.Series) -> pd.Series:
    """Parse YYYY-MM-DD and DD-MM-YYYY values (both occur in the ecommerce orders CSV)."""
    out = pd.Series(pd.NaT, index=s.index, dtype="datetime64[ns]")
    iso = s.str.match(r"^\d{4}-\d{2}-\d{2}$", na=False)
    dmy = s.str.match(r"^\d{2}-\d{2}-\d{4}$", na=False)
    out[iso] = pd.to_datetime(s[iso], format="%Y-%m-%d")
    out[dmy] = pd.to_datetime(s[dmy], format="%d-%m-%Y")
    return out


def pick(rng: np.random.Generator, options: list, probs: list[float]):
    return options[int(rng.choice(len(options), p=probs))]


def to_cell(v):
    if v is None or v is pd.NA or v is pd.NaT:
        return None
    if isinstance(v, pd.Timestamp):
        return v.to_pydatetime()
    if isinstance(v, (bool, np.bool_)):
        return bool(v)
    if isinstance(v, (int, np.integer)):
        return int(v)
    if isinstance(v, (float, np.floating)):
        return None if math.isnan(v) else float(v)
    return v


def write_header(ws, columns: list[str]) -> None:
    ws.append(columns)
    for c in range(1, len(columns) + 1):
        ws.cell(1, c).font = Font(bold=True)


def set_widths(ws, columns: list[str], values_by_col: list[list], overrides: dict | None = None) -> None:
    overrides = overrides or {}
    for j, name in enumerate(columns, start=1):
        if name in overrides:
            width = overrides[name]
        else:
            sample = [str(name)] + [str(v) for v in values_by_col[j - 1][:200] if v is not None]
            width = min(max(len(x) for x in sample) + 2, 60)
        ws.column_dimensions[get_column_letter(j)].width = max(width, 10)


@dataclass
class SheetInfo:
    name: str
    what: str
    rows: int
    columns: list[str]
    table: str | None


class Book:
    """One practice workbook: a README sheet followed by data or formula sheets."""

    def __init__(self, filename: str, title: str, purpose: str):
        self.filename = filename
        self.title = title
        self.purpose = purpose
        self.wb = Workbook()
        self.wb.remove(self.wb.active)
        self.wb.create_sheet("README")
        self.infos: list[SheetInfo] = []
        self.notes: list[str] = []

    def add_df(self, name: str, df: pd.DataFrame, what: str, table: str | None = None,
               fmts: dict | None = None, widths: dict | None = None) -> None:
        fmts = fmts or {}
        ws = self.wb.create_sheet(name)
        columns = [str(c) for c in df.columns]
        write_header(ws, columns)
        for row in df.itertuples(index=False):
            ws.append([to_cell(v) for v in row])
        n = len(df)
        for j, col in enumerate(df.columns, start=1):
            fmt = fmts.get(col)
            if fmt is None and pd.api.types.is_datetime64_any_dtype(df[col]):
                fmt = DATE_FMT
            if fmt:
                for i in range(2, n + 2):
                    ws.cell(i, j).number_format = fmt
        values = [[to_cell(v) for v in df[c].tolist()] for c in df.columns]
        set_widths(ws, columns, values, widths)
        ws.freeze_panes = "A2"
        if table and n > 0:
            t = Table(displayName=table, ref=f"A1:{get_column_letter(len(columns))}{n + 1}")
            t.tableStyleInfo = TableStyleInfo(name="TableStyleMedium2", showRowStripes=True)
            ws.add_table(t)
        self.infos.append(SheetInfo(name, what, n, columns, table))

    def add_custom(self, name: str, what: str, columns: list[str], rows: int, fill, freeze: str | None = None,
                   table: str | None = None) -> None:
        """Sheet whose layout is written by `fill(ws)` (used for formula sheets)."""
        ws = self.wb.create_sheet(name)
        fill(ws)
        if freeze:
            ws.freeze_panes = freeze
        self.infos.append(SheetInfo(name, what, rows, columns, table))

    def save(self) -> Path:
        ws = self.wb["README"]
        ws["A1"] = self.title
        ws["A1"].font = Font(bold=True, size=14)
        ws["A2"] = self.purpose
        ws["A2"].alignment = Alignment(wrap_text=True, vertical="top")
        header_row = 4
        for j, label in enumerate(["Sheet", "What it contains", "Data rows"], start=1):
            ws.cell(header_row, j, label).font = Font(bold=True)
        r = header_row + 1
        for info in self.infos:
            ws.cell(r, 1, info.name)
            ws.cell(r, 2, info.what).alignment = Alignment(wrap_text=True, vertical="top")
            ws.cell(r, 3, info.rows)
            r += 1
        r += 1
        ws.cell(r, 1, "Notes").font = Font(bold=True)
        r += 1
        for note in self.notes:
            ws.cell(r, 1, "-")
            ws.cell(r, 2, note).alignment = Alignment(wrap_text=True, vertical="top")
            r += 1
        ws.column_dimensions["A"].width = 22
        ws.column_dimensions["B"].width = 100
        ws.column_dimensions["C"].width = 12
        ws.merge_cells("A2:C2")
        ws.row_dimensions[2].height = 45
        ws.freeze_panes = f"A{header_row + 1}"

        self.wb.properties.created = FIXED_TS
        self.wb.properties.modified = FIXED_TS
        self.wb.properties.creator = "da-launchpad"
        self.wb.calculation = CalcProperties(fullCalcOnLoad=True)
        path = OUT_DIR / self.filename
        self.wb.save(path)
        return path


# --------------------------------------------------------------------------- 1. cleaning
CUSTOMER_COLS = ["customer_id", "full_name", "email", "phone", "gender", "city", "state", "signup_date",
                 "acquisition_channel", "is_prime"]


def messy_customer(r: pd.Series, rng: np.random.Generator) -> dict:
    name = str(r["full_name"])
    name = pick(rng, [name, name.upper(), name.lower(), f"  {name}  ", name.replace(" ", "  ", 1)],
                [0.45, 0.15, 0.1, 0.15, 0.15])
    city = str(r["city"])
    city = pick(rng, [city, city.upper(), city.lower(), f" {city} ", f"{city} "], [0.5, 0.15, 0.15, 0.1, 0.1])
    email = str(r["email"])
    u = rng.random()
    if u < 0.08:
        email = email.upper()
    elif u < 0.13:
        email = f"{email} "
    if pd.isna(r["phone"]):
        phone = None
    else:
        d = str(int(float(r["phone"])))
        phone = pick(rng, [d, f"+91 {d[:5]} {d[5:]}", f"{d[:5]}-{d[5:]}", f"({d[:3]}) {d[3:6]} {d[6:]}",
                           f"0{d}", f"+91-{d}"], [0.3, 0.2, 0.15, 0.15, 0.1, 0.1])
    d = pd.Timestamp(r["signup_date"])
    signup = pick(rng, [d.strftime("%Y-%m-%d"), d.strftime("%d/%m/%Y"), f"{d:%b} {d.day}, {d.year}",
                        f"{d.day:02d}-{d:%b}-{d.year}", d.strftime("%d.%m.%Y")],
                  [0.3, 0.25, 0.2, 0.15, 0.1])
    return {
        "customer_id": int(r["customer_id"]), "full_name": name, "email": email, "phone": phone,
        "gender": r["gender"], "city": city, "state": r["state"], "signup_date": signup,
        "acquisition_channel": r["acquisition_channel"], "is_prime": int(r["is_prime"]),
    }


JUNK_PARTS = [
    ("prefix", "*** "), ("suffix", " ***"), ("nbsp", " "), ("tm", "™"), ("tab", "\t"),
    ("zwsp", "​"), ("hash", " ##"), ("dash", " - ")
]


def junk_name(name: str, rng: np.random.Generator) -> str:
    out = name
    if rng.random() < 0.3:
        out = "*** " + out
    if rng.random() < 0.3:
        out = out + " ***"
    if rng.random() < 0.2:
        out = out.replace(" ", " ", 1)
    if rng.random() < 0.2:
        out = out + "™"
    if rng.random() < 0.15:
        out = out + "\t"
    if rng.random() < 0.1:
        out = out.replace(" ", "​", 1)
    if rng.random() < 0.15:
        out = out + " ##"
    return out


def build_cleaning() -> Book:
    book = Book(
        "excel-cleaning.xlsx", "Excel cleaning practice: messy data",
        "Two sheets of deliberately messy data for practising TRIM, CLEAN, Text to Columns, Remove Duplicates, "
        "Find & Replace and Flash Fill. The data is synthetic and is based on the ecommerce customers and products tables.")
    rng = np.random.default_rng(RANDOM_STATE)

    cust = load("ecommerce", "customers").sample(n=1200, random_state=RANDOM_STATE).sort_values("customer_id")
    rows = [messy_customer(r, rng) for _, r in cust.iterrows()]
    df = pd.DataFrame(rows, columns=CUSTOMER_COLS)
    dupes = df.sample(n=72, random_state=RANDOM_STATE)
    df = pd.concat([df, dupes]).sample(frac=1, random_state=RANDOM_STATE).reset_index(drop=True)
    book.add_df(
        "customers_messy", df,
        "1,272 customer rows (1,200 unique customers plus 72 exact duplicate rows) with messy data: extra and "
        "missing spaces, mixed casing in city, email and full_name, phone numbers in six formats, and signup_date "
        "stored as text in five date formats. Columns: customer_id, full_name, email, phone, gender, city, state, "
        "signup_date, acquisition_channel, is_prime.",
        fmts={"phone": "@", "signup_date": "@"},
    )

    prod = load("ecommerce", "products").sort_values("product_id")
    prod_rng = np.random.default_rng(RANDOM_STATE)
    pdf = prod[["product_id", "sku", "product_name", "category", "sub_category", "brand", "mrp", "cost_price",
                "is_active"]].copy()
    pdf["product_name"] = [junk_name(str(n), prod_rng) for n in pdf["product_name"]]
    pdf["mrp"] = num(pdf["mrp"])
    pdf["cost_price"] = num(pdf["cost_price"])
    pdf["product_id"] = pdf["product_id"].astype(int)
    pdf["is_active"] = whole(pdf["is_active"])
    book.add_df(
        "products_messy", pdf,
        "420 product rows (every product in the catalogue) where product_name contains junk characters such as "
        "leading and trailing asterisks, non-breaking spaces, zero-width spaces, tabs, the trademark sign and "
        "trailing ' ##' markers. Columns: product_id, sku, product_name, category, sub_category, brand, mrp, "
        "cost_price, is_active.",
        fmts={"mrp": MONEY_FMT, "cost_price": MONEY_FMT},
    )
    book.notes = [
        "customers_messy: signup_date is text, not a real date. Slash dates are day/month/year (DD/MM/YYYY).",
        "customers_messy: 72 rows are exact copies of other rows (same customer_id). Use Remove Duplicates on customer_id.",
        "customers_messy: phone is text. Blank phone cells are genuinely missing.",
        "products_messy: product_name is the only column with junk characters. The other columns are clean numbers and codes.",
    ]
    return book


# --------------------------------------------------------------------------- 2. functions
def build_functions() -> Book:
    book = Book(
        "excel-functions.xlsx", "Excel functions practice",
        "Ecommerce, HR and target data for practising IF/IFS/AND/OR, VLOOKUP, HLOOKUP, XLOOKUP, INDEX-MATCH, "
        "SUMIFS/COUNTIFS/AVERAGEIFS, text and date functions, and FILTER/UNIQUE/SORT. Sheets are joined by ID "
        "(order.customer_id to customers.customer_id, order.main_product_id to products.product_id).")
    orders_all = load("ecommerce", "orders")
    orders_all["order_date_p"] = parse_mixed(orders_all["order_date"])
    orders_all["total"] = num(orders_all["total_amount"])
    orders = orders_all.sample(n=2000, random_state=RANDOM_STATE).sort_values("order_id")

    items = load("ecommerce", "order_items")
    items["order_id"] = items["order_id"].astype(int)
    items["line_total_n"] = num(items["line_total"])
    items["product_id_n"] = items["product_id"].astype(int)
    item_count = items.groupby("order_id").size()
    main_item = (items.sort_values(["order_id", "line_total_n"], ascending=[True, False])
                 .drop_duplicates("order_id").set_index("order_id")["product_id_n"])

    o = pd.DataFrame({
        "order_id": orders["order_id"].astype(int),
        "customer_id": orders["customer_id"].astype(int),
        "order_date": orders["order_date_p"],
        "order_time": orders["order_time"],
        "order_status": clean_text(orders["order_status"]),
        "sales_channel": clean_text(orders["sales_channel"]),
        "coupon_code": clean_text(orders["coupon_code"]),
        "discount_amount": num(orders["discount_amount"]),
        "shipping_fee": num(orders["shipping_fee"]),
        "total_amount": num(orders["total_amount"]),
        "delivery_date": parse_iso(orders["delivery_date"]),
    })
    o["items_count"] = o["order_id"].map(item_count).fillna(0).astype(int)
    o["main_product_id"] = o["order_id"].map(main_item).astype("Int64")
    book.add_df(
        "orders", o,
        "2,000 ecommerce orders (random sample, sorted by order_id). One row per order. Columns: order_id, "
        "customer_id, order_date, order_time, order_status, sales_channel, coupon_code, discount_amount, "
        "shipping_fee, total_amount, delivery_date, items_count (number of order lines), main_product_id (product "
        "on the order's highest-value line).",
        table="tbl_orders",
        fmts={"discount_amount": MONEY_FMT, "shipping_fee": MONEY_FMT, "total_amount": MONEY_FMT},
    )

    cust = load("ecommerce", "customers")
    cust = cust[cust["customer_id"].astype(int).isin(set(o["customer_id"]))].copy()
    c = pd.DataFrame({
        "customer_id": cust["customer_id"].astype(int),
        "full_name": clean_text(cust["full_name"]),
        "city": title_text(cust["city"]),
        "state": clean_text(cust["state"]),
        "gender": clean_text(cust["gender"]),
        "signup_date": parse_iso(cust["signup_date"]),
        "acquisition_channel": clean_text(cust["acquisition_channel"]),
        "is_prime": whole(cust["is_prime"]),
    }).sort_values("customer_id").reset_index(drop=True)
    book.add_df(
        "customers", c,
        f"{len(c):,} customers who placed at least one order in the orders sheet, with cleaned city casing and "
        "real dates. Columns: customer_id, full_name, city, state, gender, signup_date, acquisition_channel, is_prime "
        "(1 = Prime member, 0 = not).",
        table="tbl_customers", fmts={"signup_date": DATE_FMT},
    )

    prod = load("ecommerce", "products").sort_values("product_id")
    p = pd.DataFrame({
        "product_id": prod["product_id"].astype(int),
        "sku": clean_text(prod["sku"]),
        "product_name": clean_text(prod["product_name"]),
        "category": title_text(prod["category"]),
        "sub_category": title_text(prod["sub_category"]),
        "brand": clean_text(prod["brand"]),
        "mrp": num(prod["mrp"]),
        "cost_price": num(prod["cost_price"]),
        "is_active": whole(prod["is_active"]),
    }).reset_index(drop=True)
    book.add_df(
        "products", p,
        f"{len(p):,} products from the catalogue (all of them), with cleaned category casing. Columns: product_id, "
        "sku, product_name, category, sub_category, brand, mrp, cost_price, is_active (1 = active).",
        table="tbl_products", fmts={"mrp": MONEY_FMT, "cost_price": MONEY_FMT},
    )

    emp = load("hr", "employees").drop_duplicates("employee_id", keep="first")
    dep = load("hr", "departments")
    dep_names = dict(zip(dep["department_id"].astype(int), clean_text(dep["department_name"])))
    h = pd.DataFrame({
        "employee_id": emp["employee_id"].astype(int),
        "full_name": clean_text(emp["full_name"]),
        "gender": clean_text(emp["gender"]),
        "date_of_birth": parse_iso(emp["date_of_birth"]),
        "hire_date": parse_iso(emp["hire_date"]),
        "department_id": emp["department_id"].astype(int),
        "department_name": emp["department_id"].astype(int).map(dep_names),
        "job_title": clean_text(emp["job_title"]),
        "job_level": clean_text(emp["job_level"]),
        "manager_id": whole(emp["manager_id"]),
        "city": clean_text(emp["city"]),
        "employment_type": clean_text(emp["employment_type"]),
        "work_mode": clean_text(emp["work_mode"]),
        "employment_status": clean_text(emp["employment_status"]),
    })
    book.add_df(
        "hr_employees", h,
        f"{len(h):,} employees (one row per employee_id) with the department name looked up from the "
        "departments table. Columns: employee_id, full_name, gender, date_of_birth, hire_date, department_id, "
        "department_name, job_title, job_level, manager_id, city, employment_type, work_mode, employment_status.",
        table="tbl_hr_employees", fmts={"date_of_birth": DATE_FMT, "hire_date": DATE_FMT},
    )

    months = pd.period_range("2023-01", "2023-12", freq="M")
    by_month = orders_all.assign(m=orders_all["order_date_p"].dt.to_period("M"))
    by_month = by_month[by_month["m"].isin(months)].groupby("m").agg(n=("order_id", "count"), rev=("total", "sum"))
    by_month = by_month.reindex(months, fill_value=0)
    trng = np.random.default_rng(RANDOM_STATE)
    t_orders = [int(round(by_month.loc[m, "n"] * trng.uniform(0.95, 1.15))) for m in months]
    t_rev = [round(float(by_month.loc[m, "rev"]) * trng.uniform(0.95, 1.15), -2) for m in months]

    def fill_targets(ws):
        ws.cell(1, 1, "Metric").font = Font(bold=True)
        for j, m in enumerate(months, start=2):
            cell = ws.cell(1, j, m.to_timestamp().to_pydatetime())
            cell.number_format = "mmm-yyyy"
            cell.font = Font(bold=True)
        ws.cell(2, 1, "Target orders")
        ws.cell(3, 1, "Target revenue (INR)")
        for j, (to, tr) in enumerate(zip(t_orders, t_rev), start=2):
            ws.cell(2, j, to)
            ws.cell(3, j, tr).number_format = MONEY_FMT
        ws.column_dimensions["A"].width = 24
        for j in range(2, len(months) + 2):
            ws.column_dimensions[get_column_letter(j)].width = 14
        ws.freeze_panes = "B2"

    book.add_custom(
        "monthly_targets", "Small horizontal table for HLOOKUP practice. Row 1 holds the 12 month start dates of "
        "2023 (Jan-2023 to Dec-2023) across columns B to M. Row 2 is the target order count per month and row 3 is "
        "the target revenue in INR per month. Column A holds the row labels.",
        ["Metric", "Jan-2023 ... Dec-2023 (columns B to M)"], 2, fill_targets, freeze="B2")
    book.notes = [
        "orders: order_date is a real date. The source mixed YYYY-MM-DD and DD-MM-YYYY text, which was converted.",
        "orders: coupon_code and delivery_date are blank where the order had no coupon or was not delivered.",
        "customers: only customers who appear in the orders sheet are included, so every customer_id in orders can be looked up.",
        "hr_employees: department_name comes from the department lookup. Use it to practise INDEX-MATCH or XLOOKUP.",
        "monthly_targets: targets were set as 2023 actuals multiplied by a random factor between 0.95 and 1.15. "
        "Actuals come from the full ecommerce order table, so the targets do not match the 2,000-row orders sheet.",
    ]
    return book


# --------------------------------------------------------------------------- 3. sales analysis
def build_sales() -> Book:
    book = Book(
        "excel-sales-analysis.xlsx", "Excel sales analysis practice",
        "Retail sales joined to store details, plus store monthly targets. Built for pivot tables, pivot charts, "
        "slicers, conditional formatting, charts and dashboards.")
    sales = load("retail", "sales").sample(n=3000, random_state=RANDOM_STATE)
    stores = load("retail", "stores")
    st = pd.DataFrame({
        "store_id": stores["store_id"].astype(int),
        "store_name": clean_text(stores["store_name"]),
        "store_city": title_text(stores["city"]),
        "store_region": title_text(stores["region"]),
        "store_format": title_text(stores["store_format"]),
    }).set_index("store_id")

    raw_dt = sales["sale_datetime"].str.strip()
    dtime = pd.Series(pd.NaT, index=raw_dt.index, dtype="datetime64[ns]")
    iso_dt = raw_dt.str.match(r"^\d{4}-", na=False)
    dtime[iso_dt] = pd.to_datetime(raw_dt[iso_dt], format="%Y-%m-%d %H:%M:%S")
    dtime[~iso_dt] = pd.to_datetime(raw_dt[~iso_dt], format="%d-%m-%Y %H:%M:%S")
    method = clean_text(sales["payment_mode"]).str.lower()
    method = method.map({"upi": "UPI", "card": "Card", "cash": "Cash", "wallet": "Wallet"}).fillna("Not Recorded")
    s = pd.DataFrame({
        "sale_id": sales["sale_id"].astype(int),
        "sale_date": dtime.dt.normalize(),
        "sale_month": dtime.dt.strftime("%Y-%m"),
        "sale_hour": dtime.dt.hour.astype(int),
        "store_id": sales["store_id"].astype(int),
    })
    s = s.join(st, on="store_id")
    s["sku_id"] = clean_text(sales["sku_id"])
    s["category"] = clean_text(sales["category"])
    s["quantity"] = whole(sales["quantity"])
    s["unit_price_inr"] = num(sales["unit_price_inr"])
    s["discount_pct"] = num(sales["discount_pct"])
    s["net_amount_inr"] = num(sales["net_amount_inr"])
    s["payment_mode"] = method.values
    s = s.sort_values(["sale_date", "sale_id"]).reset_index(drop=True)
    cols = ["sale_id", "sale_date", "sale_month", "sale_hour", "store_id", "store_name", "store_city",
            "store_region", "store_format", "sku_id", "category", "quantity", "unit_price_inr", "discount_pct",
            "net_amount_inr", "payment_mode"]
    s = s[cols]
    book.add_df(
        "sales", s,
        "3,000 retail sales transactions (random sample, sorted by date) with store name, city, region and store "
        "format looked up from the stores table. Columns: sale_id, sale_date, sale_month (text YYYY-MM), sale_hour, "
        "store_id, store_name, store_city, store_region, store_format, sku_id, category, quantity, unit_price_inr, "
        "discount_pct, net_amount_inr, payment_mode.",
        table="tbl_sales",
        fmts={"unit_price_inr": MONEY_FMT, "net_amount_inr": MONEY_FMT, "discount_pct": "0.0"},
    )

    targets = load("retail", "targets")
    tg = pd.DataFrame({
        "target_id": targets["target_id"].astype(int),
        "store_id": targets["store_id"].astype(int),
    })
    tg = tg.join(st, on="store_id")
    tg["target_month"] = clean_text(targets["target_month"])
    tg["target_net_sales_inr"] = num(targets["target_net_sales_inr"])
    tg["target_units"] = whole(targets["target_units"])
    tg = tg[["target_id", "store_id", "store_name", "store_city", "store_region", "target_month",
             "target_net_sales_inr", "target_units"]].sort_values(["store_id", "target_month"]).reset_index(drop=True)
    book.add_df(
        "targets", tg,
        f"{len(tg):,} monthly net sales targets, one row per store per month (Jan-2023 to Dec-2024). Columns: "
        "target_id, store_id, store_name, store_city, store_region, target_month (text YYYY-MM), "
        "target_net_sales_inr, target_units.",
        table="tbl_targets", fmts={"target_net_sales_inr": MONEY_FMT},
    )
    book.notes = [
        "sales: category is the product category (the retail data has no separate product table).",
        "sales: payment_mode was cleaned to UPI, Card, Cash or Wallet. Blank values are 'Not Recorded'.",
        "sales: the sample is 3,000 of 24,350 transactions, so monthly totals will not match the full retail data.",
        "targets: stores with no target rows for a month have no row for that month.",
    ]
    return book


# --------------------------------------------------------------------------- 4. HR attrition
def build_hr() -> Book:
    book = Book(
        "excel-hr-attrition.xlsx", "Excel HR attrition practice",
        "One row per employee with department, tenure, latest review, latest salary and an attrition flag. Built for "
        "attrition analysis and dashboard tasks.")
    emp = load("hr", "employees").drop_duplicates("employee_id", keep="first")
    dep = load("hr", "departments")
    dep_names = dict(zip(dep["department_id"].astype(int), clean_text(dep["department_name"])))
    dob = parse_iso(emp["date_of_birth"])
    hire = parse_iso(emp["hire_date"])

    perf = load("hr", "performance_reviews")
    perf["employee_id"] = perf["employee_id"].astype(int)
    perf["d"] = parse_iso(perf["review_date"])
    perf["rating"] = num(perf["manager_rating"])
    latest_review = (perf.sort_values(["employee_id", "d"]).groupby("employee_id")
                     .agg(latest_review_period=("review_period", "last"),
                          latest_manager_rating=("rating", "last")))

    sal = load("hr", "salaries")
    sal["employee_id"] = sal["employee_id"].astype(int)
    sal["d"] = parse_iso(sal["effective_date"])
    sal["ctc"] = num(sal["annual_ctc"])
    latest_sal = (sal.sort_values(["employee_id", "d"]).groupby("employee_id")
                  .agg(latest_annual_ctc_inr=("ctc", "last"), latest_salary_effective_date=("d", "last")))

    attr = load("hr", "attrition")
    attr_idx = attr.assign(eid=attr["employee_id"].astype(int)).set_index("eid")

    eid = emp["employee_id"].astype(int)
    df = pd.DataFrame({
        "employee_id": eid,
        "gender": clean_text(emp["gender"]),
        "age": ((AS_OF - dob).dt.days / 365.25).floordiv(1).astype("Int64"),
        "hire_date": hire,
        "tenure_years": ((AS_OF - hire).dt.days / 365.25).round(1),
        "department_name": emp["department_id"].astype(int).map(dep_names),
        "job_title": clean_text(emp["job_title"]),
        "job_level": clean_text(emp["job_level"]),
        "city": clean_text(emp["city"]),
        "employment_type": clean_text(emp["employment_type"]),
        "work_mode": clean_text(emp["work_mode"]),
        "employment_status": clean_text(emp["employment_status"]),
    })
    df = df.join(latest_review, on="employee_id").join(latest_sal, on="employee_id")
    df["latest_manager_rating"] = df["latest_manager_rating"].round().astype("Int64")
    df["attrition_flag"] = eid.isin(attr_idx.index).astype(int)
    for src, dst in [("exit_date", "exit_date"), ("exit_type", "exit_type"), ("exit_reason", "exit_reason"),
                     ("regretted_loss", "regretted_loss"), ("exit_interview_score", "exit_interview_score")]:
        vals = attr_idx[src]
        if src == "exit_date":
            df[dst] = parse_iso(eid.map(vals))
        elif src in ("regretted_loss", "exit_interview_score"):
            df[dst] = eid.map(num(vals)).round().astype("Int64")
        else:
            df[dst] = eid.map(clean_text(vals))
    df = df.reset_index(drop=True)
    book.add_df(
        "employees", df,
        f"{len(df):,} employees (one row per employee_id). attrition_flag is 1 when the employee has a row in "
        "the attrition table (exit_date, exit_type, exit_reason, regretted_loss, exit_interview_score are filled "
        "only for leavers). latest_review_period and latest_manager_rating come from the most recent performance "
        "review. latest_annual_ctc_inr and latest_salary_effective_date come from the most recent salary row. "
        "Columns: employee_id, gender, age (at 2024-12-31), hire_date, tenure_years (at 2024-12-31), "
        "department_name, job_title, job_level, city, employment_type, work_mode, employment_status, "
        "latest_review_period, latest_manager_rating, latest_annual_ctc_inr, latest_salary_effective_date, "
        "attrition_flag, exit_date, exit_type, exit_reason, regretted_loss, exit_interview_score.",
        table="tbl_employees",
        fmts={"latest_annual_ctc_inr": MONEY_FMT},
    )
    book.notes = [
        "age and tenure_years are calculated as of 2024-12-31, the end of the data period, not today.",
        "The source employee list had 12 employee IDs listed twice (same person, dates in a different format). Only the first copy of each ID is kept.",
        "employment_status and attrition_flag do not always agree in the source data. attrition_flag comes from the attrition table.",
        "regretted_loss is 1 for a regretted leaver and 0 for a non-regretted leaver. Blank for employees who stayed.",
    ]
    return book


# --------------------------------------------------------------------------- 5. what-if
def build_whatif() -> Book:
    book = Book(
        "excel-whatif.xlsx", "Excel what-if analysis practice",
        "Two models with live formulas for Goal Seek, Data Tables and Scenario Manager. Change the blue input cells "
        "and the rest of the sheet recalculates.")
    loan_cols = ["Month", "Opening balance", "EMI", "Interest", "Principal", "Closing balance"]

    def fill_loan(ws):
        ws["A1"] = "EMI calculator"
        ws["A1"].font = Font(bold=True, size=13)
        labels = {3: "Loan amount (principal)", 4: "Annual interest rate", 5: "Tenure (months)",
                  7: "Monthly interest rate", 8: "Monthly EMI", 9: "Total amount payable", 10: "Total interest"}
        for r, text in labels.items():
            ws.cell(r, 1, text)
        ws["B3"] = 500000
        ws["B3"].number_format = INR_FMT
        ws["B4"] = 0.105
        ws["B4"].number_format = "0.00%"
        ws["B5"] = 36
        ws["B7"] = "=B4/12"
        ws["B7"].number_format = "0.0000%"
        ws["B8"] = "=B3*B7*(1+B7)^B5/((1+B7)^B5-1)"
        ws["B9"] = "=B8*B5"
        ws["B10"] = "=B9-B3"
        for ref in ("B8", "B9", "B10"):
            ws[ref].number_format = '"₹"#,##0.00'
        for j, label in enumerate(loan_cols, start=1):
            ws.cell(12, j, label).font = Font(bold=True)
        for k in range(1, 37):
            r = 12 + k
            ws.cell(r, 1, k)
            ws.cell(r, 2, "=B3" if k == 1 else f"=F{r - 1}")
            ws.cell(r, 3, "=$B$8")
            ws.cell(r, 4, f"=B{r}*$B$7")
            ws.cell(r, 5, f"=C{r}-D{r}")
            ws.cell(r, 6, f"=B{r}-E{r}")
            for c in range(2, 7):
                ws.cell(r, c).number_format = MONEY_FMT
        ws.column_dimensions["A"].width = 28
        for col in "BCDEF":
            ws.column_dimensions[col].width = 18

    book.add_custom(
        "loan_emi", "EMI calculator. Inputs are in B3 (loan amount, Rs 5,00,000), B4 (annual rate, 10.5%) and "
        "B5 (tenure, 36 months). B7 to B10 are formulas for the monthly rate, monthly EMI, total payable and total "
        "interest. Rows 13 to 48 hold a 36-month amortisation schedule built with formulas (columns A to F).",
        loan_cols, 36, fill_loan)

    prod = load("ecommerce", "products")
    prod = prod[prod["is_active"].astype(int) == 1]
    picks = prod.sample(n=8, random_state=RANDOM_STATE).sort_values("product_id")
    rng = np.random.default_rng(RANDOM_STATE)
    units = [int(u) for u in rng.integers(40, 400, size=8)]

    def fill_pricing(ws):
        ws["A1"] = "Pricing model"
        ws["A1"].font = Font(bold=True, size=13)
        ws["A3"] = "Price change %"
        ws["B3"] = 0
        ws["B3"].number_format = PCT_FMT
        ws["A4"] = "Unit cost change %"
        ws["B4"] = 0
        ws["B4"].number_format = PCT_FMT
        ws["A5"] = "Fixed costs (INR)"
        ws["B5"] = 250000
        ws["B5"].number_format = INR_FMT
        head = ["Product", "Units sold", "Base price (INR)", "Base unit cost (INR)", "Adjusted price (INR)",
                "Adjusted unit cost (INR)", "Revenue (INR)", "Variable cost (INR)", "Gross profit (INR)", "Margin %"]
        for j, label in enumerate(head, start=1):
            ws.cell(7, j, label).font = Font(bold=True)
        for i, (_, p) in enumerate(picks.iterrows()):
            r = 8 + i
            ws.cell(r, 1, clean_text(pd.Series([p["product_name"]])).iloc[0])
            ws.cell(r, 2, units[i])
            ws.cell(r, 3, float(p["mrp"])).number_format = MONEY_FMT
            ws.cell(r, 4, float(p["cost_price"])).number_format = MONEY_FMT
            ws.cell(r, 5, f"=C{r}*(1+$B$3)").number_format = MONEY_FMT
            ws.cell(r, 6, f"=D{r}*(1+$B$4)").number_format = MONEY_FMT
            ws.cell(r, 7, f"=B{r}*E{r}").number_format = MONEY_FMT
            ws.cell(r, 8, f"=B{r}*F{r}").number_format = MONEY_FMT
            ws.cell(r, 9, f"=G{r}-H{r}").number_format = MONEY_FMT
            ws.cell(r, 10, f"=IF(G{r}=0,0,I{r}/G{r})").number_format = PCT_FMT
        ws.cell(16, 1, "Total").font = Font(bold=True)
        for col in "BGHI":
            ws[f"{col}16"] = f"=SUM({col}8:{col}15)"
            ws[f"{col}16"].number_format = MONEY_FMT if col != "B" else "#,##0"
        ws["J16"] = "=IF(G16=0,0,I16/G16)"
        ws["J16"].number_format = PCT_FMT
        ws["A18"] = "Net profit after fixed costs (INR)"
        ws["A18"].font = Font(bold=True)
        ws["B18"] = "=I16-B5"
        ws["B18"].number_format = INR_FMT
        ws.column_dimensions["A"].width = 36
        for j in range(2, 11):
            ws.column_dimensions[get_column_letter(j)].width = 18

    book.add_custom(
        "pricing_model", "Pricing model for 8 active catalogue products. Units sold (column B) are typed inputs and "
        "base price and cost come from the catalogue MRP and cost price. Global inputs: B3 price change %, B4 unit "
        "cost change %, B5 fixed costs. Columns E to J and the totals in row 16 are formulas. B18 is net profit "
        "after fixed costs.",
        ["Product", "Units sold", "Base price (INR)", "Base unit cost (INR)", "Adjusted price (INR)",
         "Adjusted unit cost (INR)", "Revenue (INR)", "Variable cost (INR)", "Gross profit (INR)", "Margin %"],
        8, fill_pricing, freeze="A8")
    book.notes = [
        "Formulas are not pre-calculated. Excel calculates them when the file opens.",
        "loan_emi: the schedule has 36 rows. If you change the tenure to a value above 36, copy the last row down.",
        "pricing_model: change B3 and B4 to test price and cost scenarios, or use Goal Seek on B18 by changing B3.",
    ]
    return book


# --------------------------------------------------------------------------- 6. test practice
INSTRUCTIONS = [
    "Find the total order_value_inr for each restaurant_city using SUMIFS. List the cities in column H and put the totals in column I.",
    "Count the cancelled deliveries (delivery_status = \"Cancelled\") for each cuisine using COUNTIFS.",
    "Find the average delay_minutes for Delivered orders in each weather type using AVERAGEIFS.",
    "Count how many orders have delay_minutes greater than 15 using COUNTIF. Then add a new column late_flag that shows \"Late\" when delay_minutes is above 15 and \"On time\" otherwise, using IF.",
    "Add a new column distance_band that uses IFS to label distance_km: \"Short\" when under 3 km, \"Medium\" from 3 to 6 km, and \"Long\" above 6 km.",
    "Type any delivery_id from the sheet in cell K2. Then use INDEX and MATCH to return the order_value_inr for that delivery_id.",
    "Use UNIQUE to list the distinct cuisine values, then wrap it in SORT so the list is in A to Z order.",
    "Use FILTER to list every row where delivery_status is \"Cancelled\" and weather is \"Heavy Rain\".",
    "Add a column weekday_name using TEXT(order_date, \"dddd\"). Then count the deliveries on each weekday using COUNTIF.",
    "For each restaurant_city, find the on-time rate among Delivered orders: the count of delay_minutes <= 0 divided by the count of Delivered orders, using COUNTIFS.",
]


def build_test() -> Book:
    book = Book(
        "excel-test-practice.xlsx", "Excel screening test practice",
        "A simulated Excel screening test. The food_orders sheet holds the data and the instructions sheet lists "
        "10 numbered tasks to complete within the test time.")
    deliveries = load("food_delivery", "deliveries").sample(n=2000, random_state=RANDOM_STATE).sort_values("delivery_id")
    rest = load("food_delivery", "restaurants")
    rest_df = pd.DataFrame({
        "restaurant_id": rest["restaurant_id"].astype(int),
        "restaurant_name": clean_text(rest["restaurant_name"]),
        "restaurant_city": title_text(rest["city"]),
        "cuisine": clean_text(rest["cuisine"]),
    }).set_index("restaurant_id")
    method = clean_text(deliveries["payment_mode"]).str.lower()
    method = method.map({"upi": "UPI", "card": "Card", "cash": "Cash", "wallet": "Wallet"}).fillna(
        clean_text(deliveries["payment_mode"]).str.title())
    f = pd.DataFrame({
        "delivery_id": deliveries["delivery_id"].astype(int),
        "order_date": parse_iso(deliveries["order_date"]),
        "restaurant_id": deliveries["restaurant_id"].astype(int),
    })
    f = f.join(rest_df, on="restaurant_id")
    f["distance_km"] = num(deliveries["distance_km"])
    f["promised_minutes"] = whole(deliveries["promised_minutes"])
    f["actual_minutes"] = whole(deliveries["actual_minutes"])
    f["delay_minutes"] = whole(deliveries["delay_minutes"])
    f["order_value_inr"] = num(deliveries["order_value"])
    f["delivery_fee_inr"] = num(deliveries["delivery_fee"])
    f["payment_mode"] = method.values
    f["weather"] = clean_text(deliveries["weather"])
    f["delivery_status"] = clean_text(deliveries["delivery_status"])
    f["cancel_reason"] = clean_text(deliveries["cancel_reason"])
    cols = ["delivery_id", "order_date", "restaurant_id", "restaurant_name", "restaurant_city", "cuisine",
            "distance_km", "promised_minutes", "actual_minutes", "delay_minutes", "order_value_inr",
            "delivery_fee_inr", "payment_mode", "weather", "delivery_status", "cancel_reason"]
    f = f[cols].reset_index(drop=True)
    book.add_df(
        "food_orders", f,
        "2,000 food delivery orders (random sample, sorted by delivery_id) with restaurant_name, restaurant_city and "
        "cuisine looked up from the restaurants table. Columns: delivery_id, order_date, restaurant_id, "
        "restaurant_name, restaurant_city, cuisine, distance_km, promised_minutes, actual_minutes, delay_minutes, "
        "order_value_inr, delivery_fee_inr, payment_mode, weather, delivery_status, cancel_reason.",
        table="tbl_food_orders",
        fmts={"order_value_inr": MONEY_FMT, "delivery_fee_inr": MONEY_FMT, "distance_km": "0.0"},
    )
    instr = pd.DataFrame({"No.": range(1, len(INSTRUCTIONS) + 1), "Task": INSTRUCTIONS})
    book.add_df(
        "instructions", instr,
        "The 10 numbered test tasks, in plain text. Each task refers to columns in food_orders.",
        widths={"No.": 8, "Task": 120},
    )
    book.notes = [
        "food_orders: delay_minutes is blank for cancelled orders. cancel_reason is blank for delivered orders.",
        "food_orders: restaurant_city and cuisine come from the restaurants table. The restaurant_id is the join key.",
        "food_orders: this is a 2,000-row sample of 15,120 deliveries.",
        "food_orders: restaurant_city is blank for restaurants that have no city in the source restaurants table.",
    ]
    return book


# --------------------------------------------------------------------------- output
def verify(path: Path, expected_sheets: list[str]) -> int:
    wb = load_workbook(path)
    names = wb.sheetnames
    assert names[0] == "README", f"{path.name}: README must be first, got {names}"
    assert names == expected_sheets, f"{path.name}: sheets {names} != {expected_sheets}"
    return path.stat().st_size


def render_doc(books: list[Book]) -> str:
    lines = [
        "# Excel practice workbooks",
        "",
        "Generated by `scripts/generate_data/excel_workbooks.py`. Do not edit by hand; rerun the script instead.",
        "",
        "Files are in `public/data/excel/`. Every workbook starts with a `README` sheet that lists the other sheets. "
        "Row counts below exclude the header row. Column names are exact and match the header cells.",
        "",
        "Sample data comes from the CSVs in `public/data/csv/` with `random_state=42`. A blank cell means the value was missing in the source CSV or does not apply to that row.",
        "",
    ]
    for book in books:
        lines += [f"## {book.filename}", "", f"Path: `public/data/excel/{book.filename}`", "", book.purpose, "",
                  "| Sheet | Data rows | Excel Table | Columns (in order) |", "|---|---|---|---|"]
        lines.append("| README | (index) | no | Sheet, What it contains, Data rows |")
        for info in book.infos:
            cols = ", ".join(f"`{c}`" for c in info.columns)
            table = info.table or "no"
            lines.append(f"| `{info.name}` | {info.rows:,} | {table} | {cols} |")
        lines.append("")
        lines.append("Sheet descriptions:")
        lines.append("")
        for info in book.infos:
            lines.append(f"- `{info.name}`: {info.what}")
        if book.notes:
            lines += ["", "Notes:", ""]
            lines += [f"- {n}" for n in book.notes]
        lines.append("")
    return "\n".join(lines)


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    DOC_PATH.parent.mkdir(parents=True, exist_ok=True)
    builders = [build_cleaning, build_functions, build_sales, build_hr, build_whatif, build_test]
    books = []
    for build in builders:
        book = build()
        path = book.save()
        size = path.stat().st_size
        if size > MAX_BYTES:
            raise SystemExit(f"{path.name} is {size} bytes, over the 1.5 MB limit")
        books.append(book)
    for book, build in zip(books, builders):
        expected = ["README"] + [i.name for i in book.infos]
        size = verify(OUT_DIR / book.filename, expected)
        print(f"{book.filename}: {size / 1024:.1f} KB, sheets={expected}")
    DOC_PATH.write_text(render_doc(books), encoding="utf-8")
    print(f"wrote {DOC_PATH.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
