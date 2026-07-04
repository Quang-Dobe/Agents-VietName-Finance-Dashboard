#!/usr/bin/env python3
"""Tính latest/delta/sparkline từ data/ -> site/summary.json (frontend đọc file này).

Thuần số học, KHÔNG fetch mạng. Chạy mỗi run sau khi crawl + validate xong.
"""
from __future__ import annotations

from datetime import datetime, timezone

from common import DATA, ROOT, dump_json, load_json, read_csv

SITE = ROOT / "site"


def _f(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


def pct(cur, prev):
    if cur is None or prev in (None, 0):
        return None
    return round((cur - prev) / prev * 100, 1)


def series(rows, col, n=30):
    vals = [_f(r.get(col)) for r in rows][-n:]
    return [v for v in vals if v is not None]


def at(rows, col, back=0):
    """Giá trị cột `col` ở dòng cách cuối `back` bước (có bỏ dòng rỗng)."""
    vals = [(_f(r.get(col))) for r in rows]
    vals = [v for v in vals if v is not None]
    if len(vals) <= back:
        return None
    return vals[-1 - back]


def gold_block():
    rows = read_csv(DATA / "gold" / "history.csv")
    if not rows:
        return None
    cur = at(rows, "sjc_sell")
    return {
        "latest": {"date": rows[-1]["date"], "sjc_sell": cur, "sjc_buy": at(rows, "sjc_buy")},
        "delta_1d": pct(cur, at(rows, "sjc_sell", 1)),
        "delta_7d": pct(cur, at(rows, "sjc_sell", 7)),
        "spark_30d": series(rows, "sjc_sell"),
    }


def fx_block():
    rows = read_csv(DATA / "fx" / "history.csv")
    if not rows:
        return None
    cur = at(rows, "vcb_sell")
    return {
        "latest": {"date": rows[-1]["date"], "vcb_sell": cur, "vcb_buy_transfer": at(rows, "vcb_buy_transfer")},
        "delta_1d": pct(cur, at(rows, "vcb_sell", 1)),
        "delta_7d": pct(cur, at(rows, "vcb_sell", 7)),
        "spark_30d": series(rows, "vcb_sell"),
    }


def fuel_block():
    rows = read_csv(DATA / "fuel" / "history.csv")
    if not rows:
        return None
    # E5 RON92 là chuỗi đầy đủ nhất (backfill tuoitre) → dùng làm giá đại diện.
    cur = at(rows, "e5ron92")
    return {
        "latest": {"effective_date": rows[-1]["effective_date"], "e5ron92": cur,
                   "ron95": at(rows, "ron95"), "diesel": at(rows, "diesel")},
        "primary": "e5ron92",
        "delta_period": pct(cur, at(rows, "e5ron92", 1)),
        "spark_30d": series(rows, "e5ron92"),
    }


def rates_block():
    doc = load_json(DATA / "deposit-rates" / "latest.json")
    if not doc or not doc.get("rates"):
        return None
    r12 = [r for r in doc["rates"] if r.get("term_months") == 12 and _f(r.get("rate"))]
    if not r12:
        return {"latest_week": doc.get("week"), "top12m": None, "median_12m": None}
    top = max(r12, key=lambda r: r["rate"])
    vals = sorted(_f(r["rate"]) for r in r12)
    median = vals[len(vals) // 2]
    return {
        "latest_week": doc.get("week"),
        "top12m": {"bank": top["bank"], "rate": top["rate"]},
        "median_12m": round(median, 2),
        "n_banks": len({r["bank"] for r in doc["rates"]}),
    }


def utilities_block():
    elec = load_json(DATA / "utilities" / "electricity.json", {"changes": []})
    gas = read_csv(DATA / "utilities" / "gas.csv")
    out = {}
    if elec.get("changes"):
        last = elec["changes"][-1]
        out["electricity_effective"] = last.get("effective_date")
        out["tier1_price"] = last["tiers"][0]["price"] if last.get("tiers") else None
    if gas:
        out["gas_month"] = gas[-1]["effective_month"]
        # miền Bắc (Hà Nội) là chuỗi đầy đủ nhất → dùng làm giá đại diện trên card
        out["gas_region"] = "Hà Nội"
        out["gas_price"] = _f(gas[-1].get("mien_bac"))
        out["gas_delta"] = pct(_f(gas[-1].get("mien_bac")),
                               _f(gas[-2].get("mien_bac")) if len(gas) > 1 else None)
    return out or None


def main() -> int:
    summary = {
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "gold": gold_block(),
        "fx": fx_block(),
        "fuel": fuel_block(),
        "rates": rates_block(),
        "utilities": utilities_block(),
        "flags": load_json(DATA / "flags.json", {"flags": []}).get("flags", []),
    }
    dump_json(SITE / "summary.json", summary)
    print(f"OK summary.json ({sum(1 for k in ('gold','fx','fuel','rates','utilities') if summary[k])}/5 module)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
