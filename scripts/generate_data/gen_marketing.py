"""Dataset 6: marketing (fictional D2C retailer 'ShopSetu': campaigns, spend, clicks, conversions, A/B test)."""
import numpy as np
import pandas as pd
from common import *

SEED = 20230106

CH = {  # channel: cpc, cvr, aov, ctr
    "Google Search": (14.0, .055, 1450, .045), "Google Display": (6.0, .012, 1100, .008), "Meta Ads": (9.0, .028, 1250, .012),
    "YouTube": (5.5, .015, 1300, .006), "Influencer": (7.0, .02, 1200, .010), "Email": (1.2, .07, 1600, .03),
    "WhatsApp": (1.8, .06, 1500, .06), "Affiliate": (4.0, .035, 1350, .02)}
CAMPS = [  # name, channel, objective, start, days, clicks weight, cpc mult, cvr mult
    ("Republic Day Sale - Search", "Google Search", "Sales", "2023-01-18", 10, 1.0, 1, 1),
    ("Summer Cooler Meta Carousel", "Meta Ads", "Sales", "2023-04-10", 45, 1.2, 1, 1),
    ("IPL 2023 YouTube Brand Burst", "YouTube", "Awareness", "2023-04-01", 55, 1.3, 1, 0.7),
    ("IPL 2023 Search Always-On", "Google Search", "Sales", "2023-04-01", 55, 1.4, 1.05, 1),
    ("Monsoon Mania - Meta", "Meta Ads", "Sales", "2023-07-05", 40, 1.1, 1, 1.05),
    ("Independence Day Display Retarget", "Google Display", "Retargeting", "2023-08-01", 20, 0.6, 1, 1.4),
    ("Freedom Sale WhatsApp Blast", "WhatsApp", "Sales", "2023-08-05", 11, 0.5, 1, 1),
    ("Navratri Fashion Affiliates", "Affiliate", "Sales", "2023-10-08", 15, 0.8, 1, 1),
    ("Diwali Dhamaka 2023 - Search", "Google Search", "Sales", "2023-10-25", 22, 1.5, 1.2, 1.15),
    ("Diwali Dhamaka 2023 - Meta", "Meta Ads", "Sales", "2023-10-25", 22, 1.4, 1.15, 1.1),
    ("Diwali Dhamaka 2023 - Email", "Email", "Sales", "2023-10-28", 14, 0.6, 1, 1.1),
    ("Diwali Influencer Reels 2023", "Influencer", "Awareness", "2023-10-20", 25, 1.0, 1.1, 0.8),
    ("Year End Clearance - Search", "Google Search", "Sales", "2023-12-15", 17, 0.8, 1, 1),
    ("Winter Wardrobe Email Series", "Email", "Retention", "2023-12-01", 30, 0.5, 1, 1),
    ("Republic Day 2024 Meta", "Meta Ads", "Sales", "2024-01-15", 12, 0.8, 1, 1),
    ("Valentine Gifting Affiliates", "Affiliate", "Sales", "2024-02-01", 14, 0.5, 1, 1.05),
    ("IPL 2024 Search Always-On", "Google Search", "Sales", "2024-03-22", 66, 1.5, 1.05, 1),
    ("IPL 2024 YouTube Brand Burst", "YouTube", "Awareness", "2024-03-22", 60, 1.3, 1, 0.7),
    ("IPL 2024 Meta Reels", "Meta Ads", "Sales", "2024-04-01", 50, 1.2, 1, 0.95),
    ("Summer Sale WhatsApp", "WhatsApp", "Retention", "2024-05-01", 20, 0.6, 1, 1),
    ("Monsoon Mania 2024 - Display", "Google Display", "Awareness", "2024-06-25", 45, 0.9, 1, 0.9),
    ("Back To College Influencers", "Influencer", "Sales", "2024-07-10", 35, 0.9, 1, 1),
    ("Independence Day 2024 Search", "Google Search", "Sales", "2024-08-01", 15, 0.8, 1, 1),
    ("Festive Teaser 2024 - Meta", "Meta Ads", "Awareness", "2024-09-15", 12, 0.7, 1, 0.9),
    ("Influencer Mega Reach Oct-24", "Influencer", "Awareness", "2024-10-01", 40, 2.6, 2.3, 0.12),
    ("Diwali Dhamaka 2024 - Search", "Google Search", "Sales", "2024-10-20", 18, 1.5, 1.2, 1.15),
    ("Diwali Dhamaka 2024 - WhatsApp", "WhatsApp", "Sales", "2024-10-24", 10, 0.6, 1, 1.15),
    ("Winter Retarget 2024 - Display", "Google Display", "Retargeting", "2024-11-20", 30, 0.7, 1, 1.5)]


def build():
    rng = rng_for(SEED)
    TOTAL_CLICKS = 21500
    wsum = sum(c[5] * (c[4] ** 0.5) for c in CAMPS)
    camp_rows = []
    click_parts = []
    cid_click = 0
    conv_rows = []
    for k, (name, ch, obj, start, days, cw, cpcm, cvrm) in enumerate(CAMPS):
        cid = k + 1
        cpc, cvr, aov, ctr = CH[ch]
        cpc *= cpcm
        cvr *= cvrm
        nclk = int(TOTAL_CLICKS * cw * (days ** 0.5) / wsum)
        start_i = int(np.where(DAY_STR == start)[0][0])
        di = np.arange(start_i, min(start_i + days, N_DAYS))
        wt = np.where(DOW[di] >= 5, 1.1, 1.0) * (1 + 0.5 * np.exp(-((np.arange(len(di)) - len(di) * 0.35) ** 2) / (2 * (len(di) / 5) ** 2)))
        if ch in ("Email", "WhatsApp"):
            wt = wt * np.where(np.arange(len(di)) < 3, 5, 0.8)
        if ch == "Influencer":
            wt = wt * (1 + 2 * np.exp(-np.arange(len(di)) / 5))
        wt = wt / wt.sum()
        day = rng.choice(di, nclk, p=wt)
        ts, hrs = make_times(rng, day, [.5, .3, .2, .1, .1, .2, .5, 1, 2, 3, 3.5, 4, 4, 3.5, 3, 3.5, 4, 5, 6, 8, 8, 7, 4, 1.5])
        dev = choice(rng, ["Mobile", "Desktop", "Tablet"], nclk, p=[.72, .24, .04] if ch not in ("Email",) else [.6, .36, .04])
        city = choice(rng, CITY_NAMES, nclk, p=CITY_W)
        cost = np.round(cpc * rng.lognormal(-0.045, 0.3, nclk), 2)
        lp = choice(rng, ["/home", "/sale", "/category/fashion", "/category/electronics", "/product", "/festive-offers"], nclk, p=[.15, .3, .2, .1, .15, .1])
        click_parts.append(pd.DataFrame({"campaign_id": cid, "click_time": ts, "device": dev, "city": city, "landing_page": lp, "cost_inr": cost, "_day": day}))
        camp_rows.append((cid, name, ch, obj, start, DAY_STR[di[-1]], nclk * cpc * rng.uniform(1.04, 1.3), cpc, cvr, aov, ctr))
    clicks = pd.concat(click_parts, ignore_index=True)
    clicks = clicks.sort_values("click_time", kind="stable").reset_index(drop=True)
    clicks.insert(0, "click_id", np.arange(1, len(clicks) + 1))
    nclk = len(clicks)
    clicks["visitor_id"] = rng.integers(1, int(nclk * 0.7), nclk) + 500000
    clicks["city_tier"] = np.where(clicks["city"].map(CITY_TIER) == 1, "Metro", "Tier-2")
    # conversions
    prm = {c[0]: (c[8], c[9]) for c in camp_rows}
    objm = {c[0]: c[3] for c in camp_rows}
    cvr_c = clicks["campaign_id"].map({k: v[0] for k, v in prm.items()}).values
    aov_c = clicks["campaign_id"].map({k: v[1] for k, v in prm.items()}).values
    f = np.where(clicks["device"] == "Desktop", 1.35, np.where(clicks["device"] == "Mobile", 0.9, 0.8)) * np.where(clicks["city_tier"] == "Metro", 1.1, 0.9)
    f = f * np.where(clicks["_day"].map(lambda d: d in set()) if False else 1, 1, 1)
    dayw = pd.Series(clicks["_day"]).map(lambda d: 1.0).values
    festive = pd.Series(clicks["click_time"].str[:10]).between("2023-10-25", "2023-11-14") | pd.Series(clicks["click_time"].str[:10]).between("2024-10-20", "2024-11-03")
    f = f * np.where(festive.values, 1.25, 1.0)
    conv_mask = rng.random(nclk) < cvr_c * f
    ci = np.where(conv_mask)[0]
    objs = clicks["campaign_id"].map(objm).values[ci]
    ctype = np.array([choice(rng, ["Purchase", "Signup", "Lead"], 1, p=([.9, .08, .02] if o in ("Sales", "Retargeting", "Retention") else [.3, .5, .2]))[0] for o in objs], dtype=object)
    rev = np.round(aov_c[ci] * rng.lognormal(-0.18, 0.6, len(ci)), 2)
    rev = np.where(ctype == "Purchase", rev, np.nan)
    ctime = pd.to_datetime(clicks["click_time"].iloc[ci].reset_index(drop=True)) + pd.to_timedelta(np.minimum(rng.exponential(300, len(ci)), 4000).astype(int) + 1, unit="m")
    ctime = ctime.where(ctime <= pd.Timestamp("2024-12-31 23:59:59"), pd.Timestamp("2024-12-31 23:59:59"))
    conversions = pd.DataFrame({"conversion_id": np.arange(1, len(ci) + 1), "click_id": clicks["click_id"].values[ci], "campaign_id": clicks["campaign_id"].values[ci],
                                "conversion_time": np.array(ctime.dt.strftime("%Y-%m-%d %H:%M:%S"), dtype=object), "conversion_type": ctype, "revenue_inr": rev})
    conversions = conversions.sort_values("conversion_time", kind="stable").reset_index(drop=True)
    conversions["conversion_id"] = np.arange(1, len(conversions) + 1)
    # ad spend aggregated from clicks
    g = clicks.assign(spend_date=clicks["click_time"].str[:10]).groupby(["campaign_id", "spend_date", "device"], sort=True).agg(clicks=("click_id", "count"), spend_inr=("cost_inr", "sum")).reset_index()
    ctr_c = g["campaign_id"].map({c[0]: c[10] for c in camp_rows}).values
    g["impressions"] = np.maximum(g["clicks"], (g["clicks"] / (ctr_c * rng.uniform(0.8, 1.25, len(g)))).astype(int))
    g["spend_inr"] = np.round(g["spend_inr"], 2)
    oi = rng.choice(len(g), 3, replace=False)
    g.loc[oi, "spend_inr"] = g.loc[oi, "spend_inr"] * 100
    ad = g[["campaign_id", "spend_date", "device", "impressions", "clicks", "spend_inr"]].copy()
    ad.insert(0, "ad_spend_id", np.arange(1, len(ad) + 1))
    ad = add_dups(rng, ad, n=6)
    campaigns = pd.DataFrame(camp_rows, columns=["campaign_id", "campaign_name", "channel", "objective", "start_date", "end_date", "budget_inr", "_a", "_b", "_c", "_d"]).drop(columns=["_a", "_b", "_c", "_d"])
    campaigns["budget_inr"] = (np.round(campaigns["budget_inr"] / 1000) * 1000).astype(float)
    campaigns["owner_team"] = choice(rng, ["Performance", "Brand", "CRM", "Growth"], len(campaigns))
    campaigns["status"] = np.where(campaigns["end_date"] < "2024-12-31", "Completed", "Running")
    clicks_out = clicks[["click_id", "campaign_id", "click_time", "visitor_id", "device", "city", "city_tier", "landing_page", "cost_inr"]].copy()
    clicks_out["city"] = nullify(rng, case_mess(rng, clicks_out["city"].values, 0.07), 0.03)
    clicks_out["device"] = case_mess(rng, clicks_out["device"].values, 0.02)
    clicks_out = add_dups(rng, clicks_out, n=30)
    # A/B test
    n = 12000
    uid = np.arange(1, n + 1) + 100000
    var = np.where(rng.random(n) < 0.5, "control", "treatment")
    dev = choice(rng, ["Mobile", "Desktop"], n, p=[.7, .3])
    tier = choice(rng, ["Metro", "Tier-2"], n, p=[.6, .4])
    base = np.where(dev == "Mobile", 0.085, 0.125) * np.where(tier == "Metro", 1.08, 0.9)
    lift = np.where(var == "treatment", np.where(dev == "Mobile", 0.018, 0.003) * np.where(tier == "Metro", 1.0, 1.1), 0.0)
    conv = rng.random(n) < base + lift
    atime = pd.Timestamp("2024-09-02") + pd.to_timedelta(rng.integers(0, 28 * 86400, n), unit="s")
    revv = np.round(np.exp(rng.normal(np.log(950), 0.55, n)) * np.where(var == "treatment", 0.96, 1.0), 2)
    ab = pd.DataFrame({"user_id": uid, "test_name": "checkout_free_shipping_banner", "variant": var, "assigned_at": np.array(atime.strftime("%Y-%m-%d %H:%M:%S"), dtype=object),
                       "device_type": dev, "city_tier": tier, "converted": conv.astype(int), "revenue_inr": np.where(conv, revv, 0.0)})
    ab = ab.sort_values("assigned_at", kind="stable").reset_index(drop=True)
    ab.insert(0, "ab_id", np.arange(1, len(ab) + 1))
    # contamination: 10 users appear in the other arm too (as a new row, same user)
    ci2 = rng.choice(n, 10, replace=False)
    extra = ab.iloc[ci2].copy()
    extra["variant"] = np.where(extra["variant"] == "control", "treatment", "control")
    extra["ab_id"] = np.arange(len(ab) + 1, len(ab) + 11)
    ab = pd.concat([ab, extra], ignore_index=True)
    ab = add_dups(rng, ab, n=20)

    def csv_camp(df, r):
        df["start_date"] = mix_dates(r, df["start_date"], 0.15)
        df["budget_inr"] = rupee_text(r, df["budget_inr"], 0.3, decimals=0, indian=True)
        return df

    def csv_ad(df, r):
        df["spend_inr"] = rupee_text(r, df["spend_inr"], 0.1)
        return df

    def csv_clicks(df, r):
        df["click_time"] = mix_dates(r, df["click_time"], 0.12)
        return df

    def csv_conv(df, r):
        df["revenue_inr"] = rupee_text(r, df["revenue_inr"], 0.25, indian=True)
        return df

    spec = dict(
        id="marketing", title="Marketing Analytics: ShopSetu Campaigns and A/B Test", csv_seed=16,
        description=("ShopSetu is a fictional Indian direct-to-consumer fashion and lifestyle brand running 28 paid and owned campaigns across Google, Meta, YouTube, influencers, email, WhatsApp and affiliates. "
                     "The data links campaign budgets and daily spend to clicks and conversions, plus a separate 12,000-user checkout A/B test (free-shipping banner). "
                     "Use it for ROAS and CAC analysis, channel comparison, attribution-style funnels and A/B test significance testing."),
        tables=[
            dict(name="campaigns", df=campaigns, pk="campaign_id", desc="Campaign master (28 campaigns).", csv=csv_camp, cols="""
campaign_id - Campaign identifier (primary key)
campaign_name - Campaign name
channel - Marketing channel
objective - Sales, Awareness, Retargeting or Retention
start_date - Campaign start date
end_date - Campaign end date
budget_inr - Planned budget in INR
owner_team - Owning team
status - Completed or Running"""),
            dict(name="ad_spend", df=ad, pk="ad_spend_id", desc="Daily spend, impressions and clicks per campaign and device (6 duplicate rows are deliberate).", csv=csv_ad, cols="""
ad_spend_id - Row identifier (duplicated for duplicate rows)
campaign_id - FK to campaigns.campaign_id
spend_date - Date of spend
device - Mobile, Desktop or Tablet
impressions - Impressions served
clicks - Clicks recorded (matches rows in the clicks table)
spend_inr - Spend in INR (3 rows are 100x outliers)"""),
            dict(name="clicks", df=clicks_out, pk="click_id", desc="Individual ad clicks (30 duplicate rows are deliberate).", csv=csv_clicks, cols="""
click_id - Click identifier (duplicated for duplicate rows)
campaign_id - FK to campaigns.campaign_id
click_time - Timestamp of the click
visitor_id - Anonymous visitor identifier
device - Mobile, Desktop or Tablet (a few casing issues)
city - City (casing issues, ~3% NULL)
city_tier - Metro or Tier-2
landing_page - Landing page path
cost_inr - Cost of this click in INR"""),
            dict(name="conversions", df=conversions, pk="conversion_id", desc="Conversions attributed to a click (last-click).", csv=csv_conv, cols="""
conversion_id - Conversion identifier (primary key)
click_id - FK to clicks.click_id
campaign_id - FK to campaigns.campaign_id
conversion_time - Timestamp of conversion
conversion_type - Purchase, Signup or Lead
revenue_inr - Order revenue in INR (NULL for Signup and Lead)"""),
            dict(name="ab_test_results", df=ab, pk="ab_id", desc="User-level A/B test of a free-shipping banner at checkout (Sep 2024).", cols="""
ab_id - Row identifier (duplicated for duplicate rows)
user_id - Experiment unit (visitor), assigned once to a variant
test_name - Name of the experiment
variant - control or treatment
assigned_at - Timestamp of assignment
device_type - Mobile or Desktop
city_tier - Metro or Tier-2
converted - 1 if the user purchased
revenue_inr - Revenue in INR (0 when not converted)"""),
        ],
        relationships=[("ad_spend.campaign_id", "campaigns.campaign_id"), ("clicks.campaign_id", "campaigns.campaign_id"),
                       ("conversions.click_id", "clicks.click_id"), ("conversions.campaign_id", "campaigns.campaign_id")],
        issues=[
            "clicks: 30 exact duplicate rows (same click_id); ad_spend: 6 exact duplicates; ab_test_results: 20 exact duplicate rows - so these ids carry no PRIMARY KEY constraint.",
            "ab_test_results: 10 users appear in both variants (contaminated assignment) - should be removed before analysis.",
            "ad_spend.spend_inr: 3 rows are 100x outliers.",
            "clicks.city: ~3% NULL and ~7% inconsistent casing/whitespace; clicks.device: ~2% casing issues ('mobile', 'DESKTOP').",
            "conversions.revenue_inr is NULL for Signup and Lead conversions (~10%) by design.",
            "ab_test_results has no foreign key; it is independent of the campaign tables.",
            "CSV only - campaigns.start_date ~15% DD-MM-YYYY; campaigns.budget_inr ~30% text like '₹12,50,000'.",
            "CSV only - ad_spend.spend_inr ~10% text with rupee symbol; clicks.click_time ~12% DD-MM-YYYY HH:MM:SS; conversions.revenue_inr ~25% text with rupee symbol and Indian grouping."],
        signals=[
            "Campaign 'Influencer Mega Reach Oct-24' burns the largest budget at ~2.3x normal CPC with a conversion rate ~1/8 of a normal influencer campaign - by far the worst ROAS/CAC among revenue-driving campaigns (ROAS about 0.07 vs 5-8 for Search).",
            "Email and WhatsApp have the lowest CPC and the highest conversion rate (best ROAS); Google Search is the best large-scale paid channel.",
            "Diwali windows (Oct 25-Nov 14 2023, Oct 20-Nov 3 2024) lift conversion rate by ~25%; Search/Meta Diwali campaigns are the top revenue campaigns.",
            "Awareness-objective campaigns (YouTube, Display) convert to Signup/Lead mostly and look weak on last-click revenue.",
            "Desktop converts ~35% better than mobile; Metro converts better than Tier-2.",
            "A/B test: treatment lifts conversion from ~9.5% to ~11% overall (about +1.5pp, p roughly 0.01-0.03), driven by Mobile (about +1.8pp) while Desktop shows an insignificant +0.3pp; treatment AOV is ~4% lower (free shipping cost), so revenue per user lift is smaller than conversion lift.",
            "Contaminated users, duplicates and 100x spend outliers must be cleaned before computing cost metrics or test statistics."],
    )
    return spec


def run():
    return write_dataset(build())


if __name__ == "__main__":
    run()
