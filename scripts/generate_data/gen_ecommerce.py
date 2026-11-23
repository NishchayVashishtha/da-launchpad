"""Dataset 1: ecommerce (fictional online marketplace 'BazaarKart-like' -> 'DesiCart')."""
import numpy as np
import pandas as pd
from common import *

SEED = 20230101


def build():
    rng = rng_for(SEED)
    # ------------------------------------------------ products
    cats = {  # category: (weight, price lo, price hi, [brands], [sub categories])
        "Electronics": (0.17, 499, 45000, ["VoltEdge", "Zenix", "Technova", "Gadgetry", "Orbita"], ["Mobiles", "Headphones", "Smartwatches", "Chargers", "Speakers"]),
        "Fashion": (0.25, 299, 4500, ["Rangrez", "UrbanKurta", "Threadly", "Vastra Co", "Denim Dukaan"], ["Kurtas", "T-Shirts", "Jeans", "Sarees", "Dresses"]),
        "Footwear": (0.08, 399, 5000, ["StrideWell", "Padukas", "Kolhapuri Kraft", "RunMate"], ["Sports Shoes", "Sandals", "Formal Shoes", "Sneakers"]),
        "Home & Kitchen": (0.17, 199, 12000, ["GharSaaj", "Rasoi Plus", "NestWell", "Lakshmi Home"], ["Cookware", "Decor", "Bedding", "Storage", "Appliances"]),
        "Beauty": (0.10, 99, 2500, ["GlowVeda", "Ayurmitra", "Kesar Naturals", "PureNeem"], ["Skincare", "Haircare", "Makeup", "Fragrance"]),
        "Grocery": (0.15, 49, 1500, ["Annapurna", "Desi Dhara", "FreshKhet", "Masala Mandi"], ["Staples", "Snacks", "Beverages", "Spices", "Dry Fruits"]),
        "Books": (0.08, 99, 1200, ["Pustak Ghar", "Kitaab Press", "Sahitya Hub"], ["Fiction", "Exam Prep", "Self Help", "Kids"]),
    }
    n_prod = 420
    cat_names = list(cats)
    pcat = choice(rng, cat_names, n_prod, p=[cats[c][0] for c in cat_names])
    prods = []
    for i, c in enumerate(pcat):
        _, lo, hi, brands, subs = cats[c]
        mrp = float(np.round(np.exp(rng.uniform(np.log(lo), np.log(hi))) / 10) * 10 - 1)
        mrp = max(mrp, 49.0)
        b = brands[rng.integers(len(brands))]
        s = subs[rng.integers(len(subs))]
        prods.append((i + 1, f"{b} {s[:-1] if s.endswith('s') else s} {rng.integers(100, 999)}", c, s, b, mrp,
                      round(mrp * rng.uniform(0.55, 0.8), 2), int(rng.random() > 0.05)))
    products = pd.DataFrame(prods, columns=["product_id", "product_name", "category", "sub_category", "brand", "mrp", "cost_price", "is_active"])
    products["sku"] = ["SKU" + str(100000 + i * 7) for i in range(n_prod)]
    products = products[["product_id", "sku", "product_name", "category", "sub_category", "brand", "mrp", "cost_price", "is_active"]]
    products["category"] = case_mess(rng, products["category"].values, 0.02)

    # ------------------------------------------------ customers
    n_cust = 4500
    pre = rng.random(n_cust) < 0.30
    sw = day_weights(growth=1.2, festive=1.3)
    sig_idx = np.where(pre, -1, sample_days(rng, n_cust, sw))
    order = np.argsort(sig_idx, kind="stable")
    sig_idx = sig_idx[order]
    pre = pre[order]
    pre_dates = pd.to_datetime("2022-07-01") + pd.to_timedelta(rng.integers(0, 184, n_cust), unit="D")
    signup = np.where(pre, np.array(pre_dates.strftime("%Y-%m-%d"), dtype=object), DAY_STR[np.maximum(sig_idx, 0)])
    signup = np.sort(signup.astype(str)).astype(object)  # keep ids chronological
    names, gender = full_names(rng, n_cust)
    city = choice(rng, CITY_NAMES, n_cust, p=CITY_W)
    state = np.array([CITY_STATE[c] for c in city], dtype=object)
    is_prime = (rng.random(n_cust) < 0.22).astype(int)
    channel = choice(rng, ["Organic Search", "Instagram Ads", "Google Ads", "Referral", "Influencer", "Direct"], n_cust,
                     p=[0.25, 0.2, 0.22, 0.12, 0.09, 0.12])
    # raw messy signup string
    raw = []
    for s in signup:
        y, m, d = s.split("-")
        mon = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"][int(m) - 1]
        k = rng.random()
        raw.append(s if k < 0.5 else f"{d}/{m}/{y}" if k < 0.72 else f"{int(d)} {mon} {y}" if k < 0.88 else f"{mon} {int(d)}, {y}" if k < 0.97 else "")
    raw = np.array([r if r else None for r in raw], dtype=object)
    customers = pd.DataFrame({
        "customer_id": np.arange(1, n_cust + 1), "full_name": names, "email": nullify(rng, emails(rng, names), 0.08),
        "phone": nullify(rng, phones(rng, n_cust), 0.03), "gender": nullify(rng, gender, 0.04),
        "city": nullify(rng, case_mess(rng, city, 0.10), 0.03), "state": state,
        "signup_date": signup, "signup_date_raw": raw, "acquisition_channel": channel, "is_prime": is_prime})
    # a few customers with unknown state when city null
    customers.loc[customers["city"].isna(), "state"] = None
    sig_sorted = np.where(customers["signup_date"] < "2023-01-01", -1,
                          pd.Series(customers["signup_date"]).map({d: i for i, d in enumerate(DAY_STR)}).fillna(-1)).astype(int)
    tier = np.array([CITY_TIER[c] for c in city])
    act = rng.gamma(0.55, 1.0, n_cust) * np.where(is_prime == 1, 2.2, 1.0) * np.where(tier == 1, 1.15, 1.0)
    cumw = np.cumsum(act)

    # ------------------------------------------------ orders
    n_ord = 10000
    ow = day_weights(growth=0.45, weekend=1.18, festive=1.9, sales=1.4, monthend=1.12)
    oday = sample_days(rng, n_ord, ow)
    oday.sort()
    cidx = pick_by_signup(rng, oday, sig_sorted, cumw)
    otimes, _ = make_times(rng, oday, [1, .6, .4, .3, .3, .5, 1, 2, 3, 4, 4.5, 5, 5, 5, 5, 5, 5.5, 6, 6.5, 7.5, 9, 9.5, 7, 3])
    otime = np.array([t[11:] for t in otimes], dtype=object)
    odate = DAY_STR[oday]
    ctier = tier[cidx]
    cprime = is_prime[cidx]
    pm_p = lambda t: [0.43, 0.17, 0.12, 0.18, 0.05, 0.05] if t == 1 else [0.32, 0.12, 0.09, 0.34, 0.07, 0.06]
    methods = ["UPI", "Credit Card", "Debit Card", "COD", "Netbanking", "Wallet"]
    pay = np.empty(n_ord, dtype=object)
    for t in (1, 2):
        m = ctier == t
        pay[m] = choice(rng, methods, m.sum(), p=pm_p(t))
    cod = pay == "COD"
    u = rng.random(n_ord)
    status = np.where(u < np.where(cod, 0.11, 0.035), "Cancelled",
                      np.where((u > 0.11) & (u < 0.11 + 0.07) & cod, "RTO", "Delivered"))
    status = np.where((status == "Delivered") & (rng.random(n_ord) < 0.005), "Cancelled", status).astype(object)
    discount_pct_sale = np.where(pd.Series(odate).isin(DAY_STR[[i for i in range(N_DAYS) if ow[i] > ow.mean() * 1.7]]).values, 0.25, 0.08)

    # ------------------------------------------------ order items
    k = np.clip(1 + rng.poisson(0.9, n_ord), 1, 5)
    k = np.where(cprime == 1, np.minimum(k + (rng.random(n_ord) < 0.3), 5), k)
    oid_rep = np.repeat(np.arange(1, n_ord + 1), k)
    n_items = len(oid_rep)
    pw = products["is_active"].values * np.array([cats[c if c in cats else c.strip().title()][0] if (c in cats) else 0.1 for c in products["category"]])
    pw = pw / pw.sum()
    # per-product popularity (long tail)
    pop = rng.pareto(1.6, n_prod) + 1
    pw = pw * pop
    pw = pw / pw.sum()
    pid = rng.choice(n_prod, size=n_items, p=pw)
    cat_real = np.array([c.strip().title() if c.strip().title() in cats else ("Home & Kitchen" if "home" in c.lower() else c) for c in products["category"]], dtype=object)
    qty = np.where(np.isin(cat_real[pid], ["Grocery", "Books"]), 1 + rng.poisson(0.9, n_items), 1 + (rng.random(n_items) < 0.12))
    disc = np.clip(rng.normal(discount_pct_sale[oid_rep - 1] + 0.12, 0.07, n_items), 0, 0.6)
    disc = np.round(disc, 2)
    unit = np.round(products["mrp"].values[pid] * (1 - disc), 2)
    # outliers: ~12 unit_price entry errors x100
    out_idx = rng.choice(n_items, size=12, replace=False)
    unit[out_idx] = np.round(unit[out_idx] * 100, 2)
    line_total = np.round(unit * qty, 2)
    items = pd.DataFrame({"order_item_id": np.arange(1, n_items + 1), "order_id": oid_rep, "product_id": pid + 1,
                          "quantity": qty.astype(int), "unit_price": unit, "discount_pct": np.round(disc * 100, 0).astype(int), "line_total": line_total})
    sub = items.groupby("order_id")["line_total"].sum().reindex(np.arange(1, n_ord + 1)).values
    ship = np.where(sub >= 499, 0.0, 49.0)
    coupon_used = rng.random(n_ord) < 0.18
    coupon_amt = np.where(coupon_used, np.round(np.minimum(sub * rng.choice([0.05, 0.1, 0.15], n_ord), 300), 2), 0.0)
    coupon_code = np.where(coupon_used, choice(rng, ["WELCOME10", "FESTIVE15", "SAVE5", "PRIME100", "DIWALI20"], n_ord), None)
    total = np.round(sub - coupon_amt + ship, 2)
    dlv_off = np.where(ctier == 1, rng.integers(1, 5, n_ord), rng.integers(2, 8, n_ord))
    delivery = fmt_date(add_days(odate, dlv_off))
    delivery = np.where((status == "Delivered") & (delivery <= "2024-12-31"), delivery, None)
    app = choice(rng, ["Android App", "iOS App", "Website", "Mobile Web"], n_ord, p=[0.5, 0.17, 0.2, 0.13])
    orders = pd.DataFrame({"order_id": np.arange(1, n_ord + 1), "customer_id": customers["customer_id"].values[cidx], "order_date": odate,
                           "order_time": otime, "order_status": status, "sales_channel": app, "coupon_code": coupon_code,
                           "discount_amount": coupon_amt, "shipping_fee": ship, "total_amount": total, "delivery_date": delivery})
    orders["delivery_date"] = orders["delivery_date"].astype(object)
    orders = add_dups(rng, orders, frac=0.01)

    # ------------------------------------------------ payments
    ptype = pd.Series(pay)
    p_status = np.where(status == "Delivered", "Success", np.where(cod, "Failed", "Refunded"))
    pdate = np.where(cod & (delivery != None), delivery, odate)
    ref = np.array([("TXN%010d" % rng.integers(0, 10**10)) for _ in range(n_ord)], dtype=object)
    ref = np.where(cod, None, ref)
    payments = pd.DataFrame({"order_id": np.arange(1, n_ord + 1), "payment_method": pay, "amount": total,
                             "payment_status": p_status, "payment_date": pdate, "transaction_ref": ref})
    # failed first attempts for ~5% of online-paid delivered orders
    retry = np.where((~cod) & (rng.random(n_ord) < 0.05))[0]
    fa = payments.iloc[retry].copy()
    fa["payment_status"] = "Failed"
    fa["payment_method"] = choice(rng, ["UPI", "Credit Card", "Netbanking"], len(fa), p=[0.5, 0.2, 0.3])
    fa["transaction_ref"] = [("TXN%010d" % rng.integers(0, 10**10)) for _ in range(len(fa))]
    payments = pd.concat([fa, payments], ignore_index=True)
    payments = payments.sort_values(["order_id", "payment_status"], kind="stable").reset_index(drop=True)
    payments.insert(0, "payment_id", np.arange(1, len(payments) + 1))

    # ------------------------------------------------ returns
    rate = {"Fashion": 0.21, "Footwear": 0.15, "Electronics": 0.07, "Home & Kitchen": 0.05, "Beauty": 0.04, "Grocery": 0.01, "Books": 0.02}
    ord_status = pd.Series(status, index=np.arange(1, n_ord + 1))
    it = items.copy()
    it["cat"] = cat_real[it["product_id"].values - 1]
    it = it[ord_status.loc[it["order_id"]].values == "Delivered"]
    it = it[rng.random(len(it)) < it["cat"].map(rate).values * np.where(cod[it["order_id"].values - 1], 1.25, 1.0)]
    rdel = pd.Series(delivery, index=np.arange(1, n_ord + 1)).loc[it["order_id"]].values
    rdate = add_days(rdel, rng.integers(2, 13, len(it)))
    keep = (rdate <= pd.Timestamp("2024-12-31")).values
    it, rdate = it[keep], rdate[keep]
    reasons = {"Fashion": (["Size / fit issue", "Not as described", "Changed mind", "Damaged"], [.52, .2, .18, .1]),
               "Footwear": (["Size / fit issue", "Not as described", "Changed mind", "Damaged"], [.5, .2, .2, .1]),
               "Electronics": (["Defective product", "Not as described", "Changed mind", "Wrong item sent"], [.4, .25, .2, .15]),
               "Home & Kitchen": (["Damaged", "Not as described", "Changed mind", "Wrong item sent"], [.35, .3, .2, .15]),
               "Beauty": (["Allergic / skin reaction", "Not as described", "Damaged", "Changed mind"], [.3, .3, .2, .2]),
               "Grocery": (["Damaged", "Expired / near expiry", "Wrong item sent", "Changed mind"], [.4, .3, .2, .1]),
               "Books": (["Damaged", "Wrong item sent", "Changed mind", "Not as described"], [.4, .3, .2, .1])}
    rr = np.array([choice(rng, reasons[c][0], 1, p=reasons[c][1])[0] for c in it["cat"]], dtype=object)
    rs = choice(rng, ["Refunded", "Rejected", "Pickup Pending"], len(it), p=[0.86, 0.09, 0.05])
    refund = np.where(rs == "Rejected", np.nan, np.round(it["line_total"].values * np.where(rng.random(len(it)) < 0.1, 0.9, 1.0), 2))
    returns = pd.DataFrame({"return_id": np.arange(1, len(it) + 1), "order_item_id": it["order_item_id"].values, "order_id": it["order_id"].values,
                            "return_date": fmt_date(rdate.reset_index(drop=True)), "return_reason": rr, "return_status": rs, "refund_amount": refund})
    returns = returns.sort_values("return_date", kind="stable").reset_index(drop=True)
    returns["return_id"] = np.arange(1, len(returns) + 1)

    customers = add_dups(rng, customers, n=20)

    def csv_customers(df, r):
        return df

    def csv_orders(df, r):
        df["order_date"] = mix_dates(r, df["order_date"], 0.18)
        df["total_amount"] = rupee_text(r, df["total_amount"], 0.12)
        return df

    def csv_returns(df, r):
        df["refund_amount"] = rupee_text(r, df["refund_amount"], 0.5, indian=True)
        return df

    spec = dict(
        id="ecommerce", title="E-commerce: DesiCart Marketplace", csv_seed=11,
        description=("DesiCart is a fictional Indian online marketplace selling electronics, fashion, home goods, beauty, grocery and books across 20 cities. "
                     "The data covers two years of customers, orders, line items, payments and returns (Jan 2023 to Dec 2024), including festive-season sale spikes around Diwali and "
                     "the usual messiness of a real order database. Use it for revenue analysis, cohort and repeat-purchase analysis, return analysis and cleaning practice."),
        tables=[
            dict(name="customers", df=customers, pk="customer_id", desc="One row per registered customer (a few duplicated rows are deliberate).", csv=csv_customers, cols="""
customer_id - Customer identifier (primary key, chronological by signup)
full_name - Customer name
email - Email address (NULL for some customers)
phone - 10-digit Indian mobile number as text
gender - Male / Female (NULL for some)
city - Home city (inconsistent casing/whitespace, NULL for some)
state - Indian state of the city (NULL when city is NULL)
signup_date - Account creation date (clean ISO date)
signup_date_raw - Signup date as typed in a legacy form: mixed formats, some NULL (for cleaning lessons)
acquisition_channel - Marketing channel that brought the customer
is_prime - 1 if customer holds the paid DesiCart Prime membership"""),
            dict(name="products", df=products, pk="product_id", desc="Product catalogue (~420 SKUs).", cols="""
product_id - Product identifier (primary key)
sku - Stock keeping unit code
product_name - Display name
category - Top-level category (a few rows have inconsistent casing/whitespace)
sub_category - Sub-category
brand - Fictional brand name
mrp - Maximum retail price in INR
cost_price - Landing cost in INR
is_active - 1 if currently listed"""),
            dict(name="orders", df=orders, pk="order_id", desc="One row per order (about 1% exact duplicate rows are deliberate).", csv=csv_orders, cols="""
order_id - Order identifier (duplicated for duplicate rows)
customer_id - FK to customers.customer_id
order_date - Date the order was placed (clean ISO in SQLite)
order_time - Time of day the order was placed (HH:MM:SS)
order_status - Delivered, Cancelled or RTO (return to origin, mostly COD)
sales_channel - Android App, iOS App, Website or Mobile Web
coupon_code - Coupon applied (NULL if none)
discount_amount - Coupon discount in INR
shipping_fee - Shipping fee in INR (free above 499)
total_amount - Order value in INR after discount and shipping
delivery_date - Delivery date (NULL unless delivered)"""),
            dict(name="order_items", df=items, pk="order_item_id", desc="Line items of each order.", cols="""
order_item_id - Line item identifier (primary key)
order_id - FK to orders.order_id
product_id - FK to products.product_id
quantity - Units ordered
unit_price - Selling price per unit in INR after discount (a few 100x outliers)
discount_pct - Percentage discount applied on MRP
line_total - unit_price x quantity in INR"""),
            dict(name="payments", df=payments, pk="payment_id", desc="Payment attempts (some orders have a failed attempt followed by a success).", cols="""
payment_id - Payment identifier (primary key)
order_id - FK to orders.order_id
payment_method - UPI, Credit Card, Debit Card, COD, Netbanking or Wallet
amount - Amount in INR
payment_status - Success, Failed or Refunded
payment_date - Date of payment (delivery date for COD)
transaction_ref - Gateway reference (NULL for COD)"""),
            dict(name="returns", df=returns, pk="return_id", desc="Returned line items.", csv=csv_returns, cols="""
return_id - Return identifier (primary key)
order_item_id - FK to order_items.order_item_id
order_id - FK to orders.order_id
return_date - Date the return was raised
return_reason - Customer reason
return_status - Refunded, Rejected or Pickup Pending
refund_amount - Refund in INR (NULL when rejected)"""),
        ],
        relationships=[("orders.customer_id", "customers.customer_id"), ("order_items.order_id", "orders.order_id"),
                       ("order_items.product_id", "products.product_id"), ("payments.order_id", "orders.order_id"),
                       ("returns.order_item_id", "order_items.order_item_id"), ("returns.order_id", "orders.order_id")],
        issues=[
            "orders: ~1% of rows (about 100) are exact duplicates (same order_id repeated); so orders.order_id has no PRIMARY KEY constraint.",
            "customers: 20 exact duplicate customer rows; customers.customer_id is therefore not unique.",
            "customers.email is NULL for ~8% of rows, phone ~3%, gender ~4%, city ~3% (state is NULL whenever city is NULL).",
            "customers.city: ~10% of values have inconsistent casing or stray whitespace ('mumbai', ' Mumbai', 'DELHI ').",
            "customers.signup_date_raw: free-text dates in four formats (YYYY-MM-DD, DD/MM/YYYY, '5 Mar 2023', 'Mar 5, 2023') and ~3% NULL; signup_date holds the clean value.",
            "products.category: ~2% of values have inconsistent casing or whitespace.",
            "order_items.unit_price: 12 rows are 100x too high (entry errors) which inflates order totals for those orders.",
            "CSV only - orders.order_date: ~18% of rows are written as DD-MM-YYYY instead of YYYY-MM-DD.",
            "CSV only - orders.total_amount: ~12% of rows are text like '₹1,234.50' (symbol and thousands commas).",
            "CSV only - returns.refund_amount: ~50% of rows are text with rupee symbol and Indian digit grouping (e.g. '₹1,23,456.00').",
            "payments: ~5% of online-paid orders have an extra earlier 'Failed' attempt row, so order_id is not unique in payments."],
        signals=[
            "Festive spikes: order volume rises ~1.5-1.9x in the Diwali windows (Oct 8-16 2023, Nov 6-14 2023, Sep 27-Oct 6 2024, Oct 24-Nov 3 2024); weekends are ~18% higher; steady growth through 2024.",
            "Fashion and Footwear have return rates of ~21% and ~15% (mostly 'Size / fit issue'), versus ~1% for Grocery.",
            "COD orders are cancelled ~11% of the time and RTO another ~7%, versus ~3.5% cancellation for prepaid.",
            "Tier-2 cities use COD far more (~34% vs ~18%) and have longer delivery times.",
            "Prime members (22% of customers) place roughly twice the orders; customer activity is heavy-tailed (a minority of customers drive most orders).",
            "Data-entry outliers (12 order_items with 100x unit_price) distort average order value unless handled."],
    )
    return spec


def run():
    return write_dataset(build())


if __name__ == "__main__":
    run()
