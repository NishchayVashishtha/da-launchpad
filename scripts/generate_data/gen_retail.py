"""Dataset 7: retail (fictional Indian grocery and lifestyle chain 'Vasudha Retail', 24 stores)."""
import numpy as np
import pandas as pd
from common import *

SEED = 20240707
HOUR_P = [0.2] * 8 + [1.0] * 4 + [1.4] * 3 + [1.2] * 4 + [1.8] * 3 + [0.4] * 2
FORMAT_AREA = {"Hypermarket": (60000, 90000), "Supermarket": (15000, 30000), "Express": (2500, 5000)}
FORMAT_W = {"Hypermarket": 3.0, "Supermarket": 1.6, "Express": 0.9}
PRONE_LOCALITIES = {"Velachery", "Adajan", "Gomti Nagar", "Kharadi"}   # frequent stockouts, lower sales
REGION = {"Maharashtra": "West", "Gujarat": "West", "Madhya Pradesh": "West", "Delhi": "North", "Rajasthan": "North",
          "Uttar Pradesh": "North", "Chandigarh": "North", "Karnataka": "South", "Telangana": "South",
          "Tamil Nadu": "South", "Kerala": "South", "Andhra Pradesh": "South", "West Bengal": "East",
          "Bihar": "East", "Assam": "East"}

# city, store format, locality
STORES = [("Mumbai", "Hypermarket", "Andheri"), ("Mumbai", "Supermarket", "Thane"),
          ("Delhi", "Hypermarket", "Dwarka"), ("Delhi", "Express", "Rohini"),
          ("Bengaluru", "Hypermarket", "Whitefield"), ("Bengaluru", "Supermarket", "Jayanagar"),
          ("Hyderabad", "Supermarket", "Kukatpally"), ("Chennai", "Supermarket", "Velachery"),
          ("Kolkata", "Supermarket", "Salt Lake"), ("Pune", "Supermarket", "Aundh"),
          ("Pune", "Express", "Kharadi"), ("Ahmedabad", "Hypermarket", "Satellite"),
          ("Jaipur", "Supermarket", "Malviya Nagar"), ("Lucknow", "Supermarket", "Gomti Nagar"),
          ("Chandigarh", "Express", "Sector 17"), ("Indore", "Supermarket", "Vijay Nagar"),
          ("Kochi", "Express", "Kakkanad"), ("Nagpur", "Supermarket", "Dharampeth"),
          ("Surat", "Express", "Adajan"), ("Bhopal", "Supermarket", "MP Nagar"),
          ("Patna", "Express", "Boring Road"), ("Coimbatore", "Supermarket", "RS Puram"),
          ("Visakhapatnam", "Express", "MVP Colony"), ("Guwahati", "Supermarket", "Six Mile")]

# code, category, sales share, products (name, base price INR)
CATEGORIES = [
    ("GRC", "Grocery & Staples", 0.30, [("Basmati Rice 5kg", 480), ("Toor Dal 1kg", 160), ("Atta 10kg", 520), ("Cold-Pressed Mustard Oil 1L", 290)]),
    ("PRC", "Personal Care", 0.20, [("Neem Face Wash 100ml", 140), ("Herbal Shampoo 340ml", 380), ("Sandal Soap 3-pack", 210), ("Coconut Hair Oil 200ml", 260)]),
    ("APP", "Apparel", 0.15, [("Cotton Kurta", 650), ("Men's Denim Jeans", 1200), ("Women's Leggings", 540), ("Kids T-Shirt 2-pack", 399)]),
    ("HNK", "Home & Kitchen", 0.15, [("Steel Pressure Cooker 5L", 1850), ("Non-stick Tawa 26cm", 420), ("Insulated Water Bottle 1L", 550), ("Mixer Grinder Jar Set", 620)]),
    ("ELC", "Electronics Accessories", 0.10, [("USB-C Cable 1m", 199), ("Power Bank 10000mAh", 899), ("Wired Earphones", 449), ("Phone Stand", 299)]),
    ("DCR", "Home Decor", 0.05, [("Brass Diya Set", 350), ("Jute Wall Hanging", 480), ("Ceramic Planter", 320), ("Canvas Wall Art 30x40", 899)]),
]
SKUS = []  # (sku_id, category, base price, sales share)
for code, cat, share, prods in CATEGORIES:
    for j, (_pname, price) in enumerate(prods):
        SKUS.append((f"{code}-{j + 1:02d}", cat, price, share / len(prods)))
NS, NK, NM = len(STORES), len(SKUS), 24   # stores, SKUs, months (2023-01..2024-12)


def build():
    rng = rng_for(SEED)
    sku_id = np.array([s[0] for s in SKUS], dtype=object)
    sku_cat = np.array([s[1] for s in SKUS], dtype=object)
    sku_price = np.array([s[2] for s in SKUS], dtype=float)
    sku_w = np.array([s[3] for s in SKUS])
    sku_w = sku_w / sku_w.sum()
    fmt = [f for _, f, _ in STORES]
    prone = np.array([loc in PRONE_LOCALITIES for _, _, loc in STORES])
    store_w = np.array([FORMAT_W[f] for f in fmt]) * np.where(prone, 0.7, 1.0)
    store_w = store_w / store_w.sum()
    states = [CITY_STATE[c] for c, _, _ in STORES]
    regions = np.array([REGION[s] for s in states], dtype=object)

    # ---------------- stores
    opened = pd.to_datetime("2008-01-01") + pd.to_timedelta(rng.integers(0, 15 * 365, NS), unit="D")
    area = np.array([round(rng.uniform(*FORMAT_AREA[f]) / 100) * 100 for f in fmt], dtype=int)
    stores = pd.DataFrame({
        "store_id": np.arange(1, NS + 1),
        "store_code": [f"VSD-{i:03d}" for i in range(1, NS + 1)],
        "store_name": [f"Vasudha {f} - {loc}" for _, f, loc in STORES],
        "city": case_mess(rng, [c for c, _, _ in STORES], 0.08),
        "state": states,
        "region": regions,
        "store_format": fmt,
        "opened_on": list(opened.strftime("%Y-%m-%d")),
        "carpet_area_sqft": area,
    })

    # ---------------- sales (sampled transaction lines, clean values first)
    n = 24000
    dw = day_weights(growth=0.35, weekend=1.2, festive=1.9, sales=1.5, monsoon=0.92, monthend=1.1)
    day_idx = sample_days(rng, n, dw)
    ts, _ = make_times(rng, day_idx, HOUR_P)
    st = rng.choice(NS, n, p=store_w)
    sk = rng.choice(NK, n, p=sku_w)
    qty = rng.poisson(1.6, n) + 1
    yr_f = np.where(day_idx >= 365, 1.06, 1.0)            # 2024 price revision
    unit = np.round(sku_price[sk] * yr_f * rng.normal(1.0, 0.03, n), 2)
    disc = rng.choice([0, 5, 10, 15, 20], n, p=[.55, .2, .12, .08, .05]).astype(float)
    net = np.round(qty * unit * (1 - disc / 100), 2)
    pay = choice(rng, ["UPI", "Card", "Cash", "Wallet"], n, p=[.5, .25, .18, .07])
    order = np.argsort(ts.astype(str), kind="stable")
    ts, st, sk, qty, unit, disc, net, pay = ts[order], st[order], sk[order], qty[order], unit[order], disc[order], net[order], pay[order]
    mon = np.array([(int(x[:4]) - 2023) * 12 + int(x[5:7]) - 1 for x in ts])

    # clean aggregates used for inventory and targets
    NET = np.zeros((NM, NS))
    np.add.at(NET, (mon, st), net)
    UNITS = np.zeros((NM, NS, NK))
    np.add.at(UNITS, (mon, st, sk), qty)

    sales = pd.DataFrame({
        "sale_id": np.arange(1, n + 1), "sale_datetime": ts, "store_id": st + 1, "sku_id": sku_id[sk],
        "category": sku_cat[sk], "quantity": qty, "unit_price_inr": unit, "discount_pct": disc,
        "net_amount_inr": net, "payment_mode": pay})
    dp = sales["discount_pct"].values.copy()
    dp[rng.random(n) < 0.04] = np.nan
    sales["discount_pct"] = dp
    sales["payment_mode"] = nullify(rng, case_mess(rng, sales["payment_mode"].values, 0.08), 0.01)
    big = rng.choice(n, 6, replace=False)
    sales.loc[big, "net_amount_inr"] *= 100
    sales = add_dups(rng, sales, n=350)

    # ---------------- inventory (month-end snapshot per store x SKU)
    month_ends = list(pd.date_range("2023-01-31", "2024-12-31", freq="ME").strftime("%Y-%m-%d"))
    inv = []
    for mi in range(NM):
        for s in range(NS):
            for k in range(NK):
                d = UNITS[mi, s, k]
                reorder = max(2, int(round(UNITS[:, s, k].mean() * 0.5)))
                if sku_cat[k] == "Home Decor":
                    cover = rng.uniform(6, 10)               # overstock: many months of cover
                else:
                    cover = rng.lognormal(0.0, 0.35)
                if (prone[s] and rng.random() < 0.4) or rng.random() < 0.02:
                    stock, days_out = 0, int(rng.integers(3, 22))
                else:
                    stock, days_out = int(round(d * cover * (0.5 if prone[s] else 1.0))), 0
                inv.append((month_ends[mi], s + 1, sku_id[k], sku_cat[k], stock, reorder, int(d), days_out))
    inventory = pd.DataFrame(inv, columns=["snapshot_date", "store_id", "sku_id", "category", "stock_on_hand",
                                           "reorder_level", "units_sold_in_month", "days_out_of_stock"])
    inventory.insert(0, "inventory_id", np.arange(1, len(inventory) + 1))
    soh = inventory["stock_on_hand"].astype(float).values.copy()
    soh[rng.random(len(soh)) < 0.01] = np.nan
    inventory["stock_on_hand"] = pd.Series(soh).astype("Int64")

    # ---------------- targets (no rows for the East region)
    tg = []
    for mi in range(NM):
        for s in range(NS):
            if regions[s] == "East":
                continue
            tg.append((mi, s))
    raw = np.array([NET[mi, s] * rng.uniform(0.9, 1.15) for mi, s in tg])
    tgt = np.round(raw / 1000) * 1000
    tval = tgt.astype(float).copy()
    tval[rng.random(len(tval)) < 0.03] = np.nan
    targets = pd.DataFrame({
        "target_id": np.arange(1, len(tg) + 1),
        "store_id": [s + 1 for _, s in tg],
        "target_month": [f"{2023 + mi // 12}-{mi % 12 + 1:02d}" for mi, _ in tg],
        "target_net_sales_inr": tval,
        "target_units": np.round(raw / 850).astype(int),
    })

    # ---------------- CSV-only messiness
    def csv_sales(df, r):
        df["sale_datetime"] = mix_dates(r, df["sale_datetime"], 0.15)
        df["net_amount_inr"] = rupee_text(r, df["net_amount_inr"], 0.25, decimals=2, indian=True)
        return df

    def csv_inv(df, r):
        df["snapshot_date"] = mix_dates(r, df["snapshot_date"], 0.12)
        return df

    def csv_tgt(df, r):
        df["target_net_sales_inr"] = rupee_text(r, df["target_net_sales_inr"], 0.15, decimals=0, indian=True)
        return df

    spec = dict(
        id="retail", title="Retail Sales: Vasudha Retail", csv_seed=17,
        description=("Vasudha Retail is a fictional chain of 24 grocery and lifestyle stores (hypermarkets, supermarkets and express stores) "
                     "across 15 Indian states and union territories. The dataset covers 2023-2024 with sampled transaction lines, "
                     "month-end inventory snapshots per store and SKU, and monthly sales targets. "
                     "Use it for monthly sales trends, festive seasonality, stockout impact, overstock and target attainment."),
        tables=[
            dict(name="stores", df=stores, pk="store_id", desc="24 stores with city, region, format and carpet area.", cols="""
store_id - Store identifier (primary key)
store_code - Short store code such as VSD-001
store_name - Store name (format and locality)
city - City (casing/whitespace issues on ~8% of rows)
state - State or union territory
region - North, South, East or West
store_format - Hypermarket, Supermarket or Express
opened_on - Opening date
carpet_area_sqft - Carpet area in square feet"""),
            dict(name="sales", df=sales, pk="sale_id", desc="Sampled sales transaction lines, about one line per store per day (350 exact duplicate rows are deliberate).", csv=csv_sales, index=["sku_id"], cols="""
sale_id - Sale line identifier (duplicated for duplicate rows)
sale_datetime - Date and time of the sale
store_id - FK to stores.store_id
sku_id - SKU code (no product master table; see category)
category - Product category for the SKU
quantity - Units sold on the line
unit_price_inr - Unit selling price in INR
discount_pct - Discount percentage applied (NULL for ~4%)
net_amount_inr - Net line amount in INR after discount (6 rows are 100x outliers)
payment_mode - UPI, Card, Cash or Wallet (casing issues, ~1% NULL)"""),
            dict(name="inventory", df=inventory, pk="inventory_id", desc="Month-end stock snapshot for every store and SKU, 2023-01 to 2024-12.", csv=csv_inv, index=["sku_id"], cols="""
inventory_id - Inventory record identifier (primary key)
snapshot_date - Month-end snapshot date
store_id - FK to stores.store_id
sku_id - SKU code
category - Product category for the SKU
stock_on_hand - Units on hand at month end (NULL for ~1%)
reorder_level - Suggested reorder level in units
units_sold_in_month - Units sold during the month
days_out_of_stock - Days during the month the SKU was out of stock"""),
            dict(name="targets", df=targets, pk="target_id", desc="Monthly net sales targets per store; the East region (Kolkata, Patna, Guwahati) has no targets.", csv=csv_tgt, cols="""
target_id - Target identifier (primary key)
store_id - FK to stores.store_id
target_month - Target month as YYYY-MM
target_net_sales_inr - Target net sales in INR (NULL for ~3%)
target_units - Target units derived from the sales target"""),
        ],
        relationships=[("sales.store_id", "stores.store_id"), ("inventory.store_id", "stores.store_id"),
                       ("targets.store_id", "stores.store_id")],
        issues=[
            "sales: 350 exact duplicate rows (same sale_id twice), so sale_id has no PRIMARY KEY constraint.",
            "sales.discount_pct: NULL for ~4% of rows; net_amount_inr already reflects the discount, so it is still populated.",
            "sales.payment_mode: ~8% inconsistent casing/whitespace ('upi', ' Card'), ~1% NULL.",
            "sales.net_amount_inr: 6 rows are 100x outliers.",
            "stores.city: ~8% casing/whitespace issues.",
            "inventory.stock_on_hand: ~1% NULL.",
            "targets.target_net_sales_inr: ~3% NULL; no targets exist for the East region stores.",
            "CSV only - sales.sale_datetime: ~15% of rows use DD-MM-YYYY; sales.net_amount_inr: ~25% are rupee text with Indian grouping.",
            "CSV only - inventory.snapshot_date: ~12% of rows use DD-MM-YYYY; targets.target_net_sales_inr: ~15% are rupee text.",
            "No product master table: sku_id and category are denormalised codes."],
        signals=[
            "Stockouts: Velachery (Chennai), Adajan (Surat), Gomti Nagar (Lucknow) and Kharadi (Pune) stores have frequent stockouts (days_out_of_stock > 0 for many SKUs) and roughly 30% lower sales volume than peers.",
            "Diwali (Oct-Nov) and the 2024 Navratri window spike sales; Republic Day and Independence Day sale weeks give smaller spikes.",
            "Home Decor is slow-moving: about 5% of sales volume, but stock covers 6-10 months of demand, so it is overstocked.",
            "East region stores (Kolkata, Patna, Guwahati) have no targets, so target attainment can only be compared for the other regions.",
            "Targets are set at 90-115% of actual sales, so attainment clusters near 100% with a few misses.",
            "2024 prices are about 6% higher than 2023 for every SKU, so compare volume and value separately.",
            "Sales are a sampled extract of about one transaction line per store per day, so use rates and shares rather than absolute totals.",
            "6 net_amount outliers (100x) distort totals unless excluded."],
    )
    return spec


def run():
    return write_dataset(build())


if __name__ == "__main__":
    run()
