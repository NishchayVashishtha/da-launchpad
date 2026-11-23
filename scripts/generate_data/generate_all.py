"""Regenerate all 7 DA Launchpad datasets, rebuild zips and assemble src/data/datasets.json.

Usage: .venv/bin/python scripts/generate_data/generate_all.py
"""
import json
import sqlite3
import sys
import zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from common import META_DIR, PUB, ROOT  # noqa: E402
import gen_ecommerce, gen_food_delivery, gen_hr, gen_fintech, gen_subscription, gen_marketing, gen_retail  # noqa: E402

GENERATORS = [gen_ecommerce, gen_food_delivery, gen_hr, gen_fintech, gen_subscription, gen_marketing, gen_retail]
ORDER = ["ecommerce", "food_delivery", "hr", "fintech", "subscription", "marketing", "retail"]
REQUIRED = ["id", "title", "description", "tables", "relationships", "qualityIssues", "er", "downloads", "signals"]


def build_zip(did):
    """Zip every CSV of a dataset with fixed timestamps so the archive is deterministic."""
    csv_dir = PUB / "csv" / did
    zp = PUB / "zip" / f"{did}.zip"
    zp.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(zp, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for fp in sorted(csv_dir.glob("*.csv")):
            zi = zipfile.ZipInfo(f"{did}/{fp.name}", date_time=(2024, 1, 1, 0, 0, 0))
            zi.compress_type = zipfile.ZIP_DEFLATED
            z.writestr(zi, fp.read_bytes())


def check_meta(meta):
    did = meta["id"]
    missing = [k for k in REQUIRED if k not in meta]
    assert not missing, f"{did}: missing keys {missing}"
    con = sqlite3.connect(PUB / "sqlite" / f"{did}.sqlite")
    try:
        for t in meta["tables"]:
            real = con.execute(f'SELECT COUNT(*) FROM "{t["name"]}"').fetchone()[0]
            assert real == t["rowCount"], f"{did}.{t['name']}: rowCount {t['rowCount']} != {real}"
    finally:
        con.close()


def main():
    for g in GENERATORS:
        g.run()
    datasets = []
    for did in ORDER:
        build_zip(did)
        meta = json.loads((META_DIR / f"{did}.json").read_text(encoding="utf-8"))
        check_meta(meta)
        datasets.append(meta)
    out = ROOT / "src" / "data" / "datasets.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(datasets, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {out} ({len(datasets)} datasets)")


if __name__ == "__main__":
    main()
