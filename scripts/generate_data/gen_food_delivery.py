"""Dataset 2: food_delivery (fictional 'ThaliDash' food delivery platform)."""
import numpy as np
import pandas as pd
from common import *

SEED = 20230102
FD_CITIES = CITY_NAMES[:10]


def rain_prob(city, month):
    m = {"Mumbai": {6: .5, 7: .75, 8: .65, 9: .45}, "Kolkata": {6: .4, 7: .55, 8: .55, 9: .45}, "Pune": {6: .3, 7: .5, 8: .4, 9: .3},
         "Chennai": {10: .4, 11: .55, 12: .3}, "Bengaluru": {5: .2, 6: .25, 7: .3, 8: .3, 9: .35, 10: .3}, "Delhi": {7: .3, 8: .3, 9: .15},
         "Hyderabad": {7: .25, 8: .3, 9: .3}, "Ahmedabad": {7: .25, 8: .25}, "Jaipur": {7: .2, 8: .25}, "Lucknow": {7: .25, 8: .25}}
    return m.get(city, {}).get(month, 0.03)


def build():
    rng = rng_for(SEED)
    cw = CITY_W[:10] / CITY_W[:10].sum()
    # --- restaurants
    n_r = 600
    rcity = choice(rng, FD_CITIES, n_r, p=cw)
    cuis = choice(rng, ["North Indian", "South Indian", "Biryani", "Chinese", "Pizza", "Burgers", "Street Food", "Desserts", "Healthy", "Mughlai", "Gujarati Thali", "Bengali"], n_r,
                  p=[.2, .13, .13, .1, .07, .06, .08, .06, .05, .05, .04, .03])
    pre = ["Spice", "Tandoor", "Masala", "Dilli", "Annapoorna", "Royal", "Madras", "Kolkata", "Zaika", "Punjabi", "Saffron", "Curry", "Dosa", "Chaat", "Biryani"]
    suf = ["Junction", "Express", "Kitchen", "House", "Darbar", "Corner", "Point", "Rasoi", "Hub", "Villa", "Magic", "Bhavan"]
    rname = np.array([f"{pre[rng.integers(len(pre))]} {suf[rng.integers(len(suf))]}" for _ in range(n_r)], dtype=object)
    band = choice(rng, ["Budget", "Mid", "Premium"], n_r, p=[.4, .45, .15])
    quality = np.clip(rng.normal(0, 0.55, n_r), -1.3, 1.3)       # latent food quality
    prep = np.round(np.clip(rng.normal(16, 4, n_r) + np.where(band == "Premium", 4, 0), 7, 35)).astype(int)
    restaurants = pd.DataFrame({
        "restaurant_id": np.arange(1, n_r + 1), "restaurant_name": rname, "cuisine": cuis, "city": case_mess(rng, rcity, 0.08),
        "price_band": band, "avg_prep_minutes": prep, "is_cloud_kitchen": (rng.random(n_r) < 0.2).astype(int),
        "onboarded_date": fmt_date(add_days(["2021-01-01"] * n_r, rng.integers(0, 1400, n_r)))})
    restaurants["city"] = nullify(rng, restaurants["city"].values, 0.02)
    # --- partners
    n_p = 900
    pcity = choice(rng, FD_CITIES, n_p, p=cw)
    pn, _ = full_names(rng, n_p, np.array(["Male"] * n_p, dtype=object))
    joined = fmt_date(add_days(["2021-06-01"] * n_p, rng.integers(0, 1300, n_p)))
    speed = np.clip(rng.normal(0, 1, n_p), -2, 2)
    partners = pd.DataFrame({
        "partner_id": np.arange(1, n_p + 1), "partner_name": pn, "city": pcity,
        "vehicle_type": choice(rng, ["Bike", "EV Scooter", "Bicycle"], n_p, p=[.82, .12, .06]), "joined_date": joined,
        "phone": nullify(rng, phones(rng, n_p), 0.05), "is_active": (rng.random(n_p) < 0.88).astype(int)})
    partners["city"] = case_mess(rng, partners["city"].values, 0.06)
    partners = add_dups(rng, partners, n=8)
    joined_idx = pd.to_datetime(pd.Series(joined))
    # --- deliveries
    n = 15000
    w = day_weights(growth=0.55, weekend=1.25, festive=1.15, ipl=1.3, monsoon=1.08, monthend=1.05, sales=1.05)
    day = np.sort(sample_days(rng, n, w))
    ts, hrs = make_times(rng, day, [.3, .1, .05, .02, .02, .05, .2, .6, 1.2, 1.2, 1.5, 3.5, 5, 4, 2.5, 2, 2.5, 3, 4.5, 7, 9, 8, 4.5, 1.5])
    rpop = rng.pareto(1.5, n_r) + 1
    rest = np.zeros(n, dtype=int)
    part = np.zeros(n, dtype=int)
    rc = np.array(rcity)
    pc = np.array(pcity)
    cust_city = choice(rng, FD_CITIES, n, p=cw)
    for c in FD_CITIES:
        m = cust_city == c
        ri = np.where(rc == c)[0]
        pi = np.where(pc == c)[0]
        rest[m] = rng.choice(ri, m.sum(), p=rpop[ri] / rpop[ri].sum())
        part[m] = rng.choice(pi, m.sum())
    month = DAYS.month.values[day]
    dist = np.round(np.clip(rng.gamma(3.0, 1.2, n) + 0.5, 0.4, 14), 1)
    # weather
    rp = np.array([rain_prob(c, mo) for c, mo in zip(cust_city, month)])
    u = rng.random(n)
    weather = np.where(u < rp * 0.35, "Heavy Rain", np.where(u < rp, "Rain", np.where(rng.random(n) < 0.2, "Cloudy", "Clear"))).astype(object)
    peak = np.isin(hrs, [12, 13, 20, 21])
    wx_pen = np.where(weather == "Heavy Rain", 13, np.where(weather == "Rain", 6, 0))
    join_days = (pd.to_datetime(pd.Series(DAY_STR[day])).values - joined_idx.values[part]) / np.timedelta64(1, "D")
    newp = np.where(join_days < 60, 5.0, 0.0)
    pprep = prep[rest] + rng.normal(0, 4, n) + np.where(peak, 3, 0)
    travel = dist * (4.4 - 0.25 * speed[part]) + np.where(peak, 3, 0) + wx_pen * 0.5
    wait = np.clip(rng.exponential(3.0, n) + wx_pen * 0.3 + np.where(peak, 3, 0), 0, 30)
    actual = np.round(np.clip(pprep + travel + wait + newp + np.where(rng.random(n) < 0.04, rng.uniform(10, 30, n), 0), 12, 120)).astype(int)
    promised = (np.ceil((18 + dist * 3.6 + prep[rest] * 0.4) / 5) * 5).astype(int)
    delay = actual - promised
    pcancel = 0.035 + 0.04 * (weather == "Heavy Rain") + 0.015 * (weather == "Rain") + 0.002 * np.clip(delay, 0, 30)
    cancelled = rng.random(n) < pcancel
    band_mult = pd.Series(band[rest]).map({"Budget": 260, "Mid": 420, "Premium": 700}).values
    value = np.round(np.clip(rng.lognormal(0, 0.45, n) * band_mult * np.where(day_weights() is not None, 1, 1), 79, 4000))
    out_i = rng.choice(n, 8, replace=False)
    value[out_i] = value[out_i] * 100
    fee = np.where(value >= 599, 0, np.round(15 + dist * 4 + np.where(weather != "Clear", 10, 0))).astype(float)
    odt = pd.to_datetime(pd.Series(ts))
    deliv = odt + pd.to_timedelta(actual, unit="m")
    status = np.where(cancelled, "Cancelled", "Delivered").astype(object)
    reason = np.where(cancelled, choice(rng, ["Restaurant delay", "Customer cancelled", "No partner available", "Restaurant closed", "Payment issue"], n, p=[.28, .3, .22, .1, .1]), None)
    deliveries = pd.DataFrame({
        "delivery_id": np.arange(1, n + 1), "restaurant_id": rest + 1, "partner_id": part + 1, "customer_id": rng.integers(1, 9001, n),
        "city": cust_city, "order_date": DAY_STR[day], "order_time": ts,
        "delivered_time": np.where(cancelled, None, np.array(deliv.dt.strftime("%Y-%m-%d %H:%M:%S"), dtype=object)),
        "distance_km": dist, "promised_minutes": promised, "actual_minutes": pd.array(np.where(cancelled, -1, actual)).astype("Int64"),
        "delay_minutes": pd.array(np.where(cancelled, -999, delay)).astype("Int64"),
        "order_value": value, "delivery_fee": fee, "payment_mode": choice(rng, ["UPI", "Card", "Cash on Delivery", "Wallet"], n, p=[.58, .18, .17, .07]),
        "weather": weather, "delivery_status": status, "cancel_reason": reason})
    deliveries.loc[cancelled, ["actual_minutes", "delay_minutes"]] = pd.NA
    deliveries["city"] = case_mess(rng, deliveries["city"].values, 0.03)
    # --- ratings
    deliv_ok = np.where(~cancelled)[0]
    bad = np.clip(delay[deliv_ok], 0, 60)
    p_rate = np.clip(0.55 + 0.01 * bad, 0.4, 0.9)
    rated = deliv_ok[rng.random(len(deliv_ok)) < p_rate]
    d_r = np.clip(np.round(4.6 - 0.075 * np.clip(delay[rated], -5, 60) + rng.normal(0, 0.6, len(rated))), 1, 5).astype(int)
    f_r = np.clip(np.round(4.0 + quality[rest[rated]] + rng.normal(0, 0.6, len(rated))), 1, 5).astype(int)
    overall = np.clip(np.round(0.6 * d_r + 0.4 * f_r + rng.normal(0, 0.25, len(rated))), 1, 5).astype(int)
    texts_pos = ["Great food, on time", "Loved it", "Hot and fresh", "Value for money", "Delivery was quick", "Tasty!"]
    texts_neg = ["Very late delivery", "Food was cold", "Took forever", "Order delayed again", "Partner was rude", "Missing items", "Packaging spilled"]
    txt = np.array([rng.choice(texts_pos if o >= 4 else texts_neg) if o != 3 else rng.choice(["Okay", "Average", "Could be better"]) for o in overall], dtype=object)
    txt = np.where(rng.random(len(rated)) < 0.55, None, txt)
    rated_at = odt.iloc[rated].reset_index(drop=True) + pd.to_timedelta(actual[rated] + rng.integers(2, 600, len(rated)), unit="m")
    ratings = pd.DataFrame({"rating_id": np.arange(1, len(rated) + 1), "delivery_id": rated + 1, "restaurant_id": rest[rated] + 1, "partner_id": part[rated] + 1,
                            "food_rating": f_r, "delivery_rating": d_r, "overall_rating": overall, "review_text": txt,
                            "rated_at": np.array(rated_at.dt.strftime("%Y-%m-%d %H:%M:%S"), dtype=object)})
    ratings = ratings.sort_values("rated_at", kind="stable").reset_index(drop=True)
    ratings["rating_id"] = np.arange(1, len(ratings) + 1)
    # --- promo usage
    ipl = pd.Series(DAY_STR[day]).between("2023-03-31", "2023-05-28") | pd.Series(DAY_STR[day]).between("2024-03-22", "2024-05-26")
    monsoon = pd.Series(month).between(6, 9)
    p_use = 0.28 + 0.08 * ipl.values + 0.05 * monsoon.values + 0.05 * (~peak) + 0.1 * (value < 250)
    used = np.where(rng.random(n) < p_use)[0]
    codes = []
    disc = []
    for i in used:
        v = value[i]
        ops = ["WELCOME50", "FREEDEL", "FLAT75", "BIGSAVER", "IPLFEAST", "MONSOON20"]
        pr = np.array([.2, .22, .2, .14, .12 if ipl.iloc[i] else 0.0, .12 if monsoon.iloc[i] else 0.0])
        c = ops[rng.choice(6, p=pr / pr.sum())]
        codes.append(c)
        if c == "WELCOME50":
            d = min(v * 0.5, 100)
        elif c == "FREEDEL":
            d = fee[i] if fee[i] > 0 else 25
        elif c == "FLAT75":
            d = 75 if v >= 120 else v * 0.5
        elif c == "BIGSAVER":
            d = min(v * 0.2, 150)
        elif c == "IPLFEAST":
            d = min(v * 0.25, 125)
        else:
            d = min(v * 0.2, 80)
        disc.append(round(float(d), 2))
    promo = pd.DataFrame({"usage_id": np.arange(1, len(used) + 1), "delivery_id": used + 1, "promo_code": codes, "discount_amount": disc,
                          "is_new_user": ((np.array(codes) == "WELCOME50") | (rng.random(len(used)) < 0.08)).astype(int),
                          "used_at": ts[used]})
    promo["promo_code"] = case_mess(rng, promo["promo_code"].values, 0.04)
    deliveries = add_dups(rng, deliveries, frac=0.008)

    def csv_del(df, r):
        df["order_time"] = mix_dates(r, df["order_time"], 0.15)
        df["order_value"] = rupee_text(r, df["order_value"], 0.15, decimals=0, indian=True)
        return df

    def csv_rat(df, r):
        df["rated_at"] = mix_dates(r, df["rated_at"], 0.25)
        return df

    def csv_promo(df, r):
        df["discount_amount"] = rupee_text(r, df["discount_amount"], 0.2, decimals=2)
        return df

    spec = dict(
        id="food_delivery", title="Food Delivery: ThaliDash", csv_seed=12,
        description=("ThaliDash is a fictional Indian food-delivery platform operating in 10 cities with 600 partner restaurants and 900 delivery partners. "
                     "Two years of deliveries, ratings and promo redemptions capture lunch and dinner peaks, IPL-season surges and monsoon disruption. "
                     "Use it to study delivery time, SLA breaches, customer ratings, partner performance and promo ROI."),
        tables=[
            dict(name="restaurants", df=restaurants, pk="restaurant_id", desc="Partner restaurants.", cols="""
restaurant_id - Restaurant identifier (primary key)
restaurant_name - Restaurant display name (not unique)
cuisine - Main cuisine
city - City (inconsistent casing/whitespace, ~2% NULL)
price_band - Budget, Mid or Premium
avg_prep_minutes - Typical kitchen preparation time
is_cloud_kitchen - 1 if delivery-only kitchen
onboarded_date - Date the restaurant joined the platform"""),
            dict(name="delivery_partners", df=partners, pk="partner_id", desc="Delivery riders (a few duplicate rows are deliberate).", cols="""
partner_id - Partner identifier
partner_name - Rider name
city - Operating city (inconsistent casing)
vehicle_type - Bike, EV Scooter or Bicycle
joined_date - Date the rider joined
phone - Mobile number (NULL for ~5%)
is_active - 1 if currently active"""),
            dict(name="deliveries", df=deliveries, pk="delivery_id", desc="One row per order/delivery (~0.8% exact duplicate rows are deliberate).", csv=csv_del, cols="""
delivery_id - Delivery identifier (duplicated for duplicate rows)
restaurant_id - FK to restaurants.restaurant_id
partner_id - FK to delivery_partners.partner_id
customer_id - Anonymous customer id (no customer table)
city - Customer city (a few casing issues)
order_date - Date the order was placed
order_time - Timestamp the order was placed
delivered_time - Timestamp of delivery (NULL if cancelled)
distance_km - Restaurant to customer distance
promised_minutes - ETA promised to the customer
actual_minutes - Actual minutes from order to delivery (NULL if cancelled)
delay_minutes - actual_minutes minus promised_minutes (NULL if cancelled; negative = early)
order_value - Food order value in INR (8 rows are 100x outliers)
delivery_fee - Delivery fee in INR
payment_mode - UPI, Card, Cash on Delivery or Wallet
weather - Clear, Cloudy, Rain or Heavy Rain at delivery
delivery_status - Delivered or Cancelled
cancel_reason - Reason when cancelled, else NULL"""),
            dict(name="ratings", df=ratings, pk="rating_id", desc="Customer ratings for ~60-70% of delivered orders.", csv=csv_rat, cols="""
rating_id - Rating identifier (primary key)
delivery_id - FK to deliveries.delivery_id
restaurant_id - FK to restaurants.restaurant_id
partner_id - FK to delivery_partners.partner_id
food_rating - 1-5 food rating
delivery_rating - 1-5 delivery rating
overall_rating - 1-5 overall rating
review_text - Free-text review (NULL for ~55%)
rated_at - Timestamp the rating was left"""),
            dict(name="promo_usage", df=promo, pk="usage_id", desc="Promo code redemptions on deliveries.", csv=csv_promo, cols="""
usage_id - Redemption identifier (primary key)
delivery_id - FK to deliveries.delivery_id
promo_code - Promo code (a few casing inconsistencies)
discount_amount - Discount given in INR
is_new_user - 1 if redemption by a first-time user
used_at - Timestamp of redemption (equals order time)"""),
        ],
        relationships=[("deliveries.restaurant_id", "restaurants.restaurant_id"), ("deliveries.partner_id", "delivery_partners.partner_id"),
                       ("ratings.delivery_id", "deliveries.delivery_id"), ("ratings.restaurant_id", "restaurants.restaurant_id"),
                       ("ratings.partner_id", "delivery_partners.partner_id"), ("promo_usage.delivery_id", "deliveries.delivery_id")],
        issues=[
            "deliveries: ~0.8% of rows (about 120) are exact duplicates by delivery_id, so delivery_id has no PRIMARY KEY constraint.",
            "delivery_partners: 8 exact duplicate partner rows.",
            "deliveries.actual_minutes, delay_minutes, delivered_time and cancel_reason are NULL by design for cancelled orders (~5-6% of rows).",
            "deliveries.order_value: 8 rows are 100x outliers (e.g. 41,200 instead of 412).",
            "restaurants.city ~8% and delivery_partners.city ~6% (and deliveries.city ~3%) have inconsistent casing or whitespace; restaurants.city ~2% NULL; delivery_partners.phone ~5% NULL.",
            "promo_usage.promo_code: ~4% of values have inconsistent casing/whitespace.",
            "CSV only - deliveries.order_time: ~15% of rows are DD-MM-YYYY HH:MM:SS instead of ISO.",
            "CSV only - deliveries.order_value: ~15% of rows are text with rupee symbol and Indian grouping (e.g. '₹1,250').",
            "CSV only - ratings.rated_at: ~25% of rows in DD-MM-YYYY format.",
            "CSV only - promo_usage.discount_amount: ~20% of rows are text like '₹75.00'."],
        signals=[
            "Delivery delay drives ratings: delivery_rating falls ~0.075 per minute of delay; late (delay > 10 min) orders average roughly 1-1.5 points lower than on-time orders; unhappy customers are also more likely to rate.",
            "Heavy Rain and Rain days (Mumbai/Kolkata/Pune Jun-Sep, Chennai Oct-Dec) add 6-13 minutes and raise cancellation rates (~3.5% base up to ~8%).",
            "Lunch (12-13h) and dinner (20-21h) peaks have longer waits; weekends are ~25% busier; order volume rises ~1.3x during IPL months (Mar 22-May 26 2024, Mar 31-May 28 2023).",
            "Partners in their first ~60 days are ~5 minutes slower; a skill factor per partner creates a spread in partner performance.",
            "FLAT75 is applied heavily to low-value orders (discount is a large share of order value), making it the worst-ROI promo; WELCOME50 drives new-user orders; IPLFEAST and MONSOON20 only appear in their seasons.",
            "Restaurant food quality varies independently of delivery speed (food_rating vs delivery_rating can be separated by analysts).",
            "8 outlier order_values (100x) distort average order value."],
    )
    return spec


def run():
    return write_dataset(build())


if __name__ == "__main__":
    run()
