#!/usr/bin/env python3
"""Validate + đối chiếu chéo dữ liệu -> in ERROR/FLAG, ghi data/flags.json.

ERROR = dữ liệu vi phạm sanity (nên loại/sửa). FLAG = bất thường nhưng giữ lại,
site hiển thị dấu ⚠. KHÔNG tự sửa số liệu — số thật > số đẹp.

  validate.py                 # kiểm tra dữ liệu mới nhất mỗi module
  validate.py --full          # quét toàn bộ lịch sử (dùng sau backfill)
"""
from __future__ import annotations

import sys

from common import DATA, dump_json, emit, load_json, read_csv

# Ngưỡng đặt tập trung để dễ sửa.
SANITY = {
    "gold": (30_000, 500_000),   # nghìn đ/lượng
    "fx": (15_000, 50_000),      # VND/USD
    "rate": (0.1, 15.0),         # %/năm
    "fuel": (5_000, 60_000),     # đ/lít
    "gas": (200_000, 1_200_000), # đ/bình 12kg
}
JUMP = {  # ngưỡng FLAG khi nhảy so kỳ trước (tỷ lệ)
    "gold": 0.05, "fx": 0.02, "fuel": 0.20, "gas": 0.30, "rate_pts": 2.0,
    "sjc_vs_doji": 0.03, "vcb_vs_sbv": 0.05,
}


def _f(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


def check_gold(rows, full, errs, flags):
    rows = rows if full else rows[-2:]
    prev = None
    for r in rows:
        b, s = _f(r.get("sjc_buy")), _f(r.get("sjc_sell"))
        lo, hi = SANITY["gold"]
        if s is None or not (lo < s < hi) or (b is not None and s <= b):
            errs.append(("gold", r["date"], f"sanity sjc buy={b} sell={s}"))
        ds = _f(r.get("doji_sell"))
        if s and ds and abs(s - ds) / s > JUMP["sjc_vs_doji"]:
            flags.append(("gold", r["date"], f"SJC lệch DOJI {abs(s-ds)/s*100:.1f}%"))
        if prev and s and _f(prev.get("sjc_sell")):
            ps = _f(prev["sjc_sell"])
            if abs(s - ps) / ps > JUMP["gold"]:
                flags.append(("gold", r["date"], f"vàng nhảy {(s-ps)/ps*100:+.1f}% so hôm trước"))
        prev = r


def check_fx(rows, full, errs, flags):
    rows = rows if full else rows[-2:]
    prev = None
    for r in rows:
        bt, s = _f(r.get("vcb_buy_transfer")), _f(r.get("vcb_sell"))
        lo, hi = SANITY["fx"]
        if s is None or not (lo < s < hi) or (bt is not None and bt > s):
            errs.append(("fx", r["date"], f"sanity buy_transfer={bt} sell={s}"))
        cen = _f(r.get("sbv_central"))
        if s and cen and abs(s - cen) / cen > JUMP["vcb_vs_sbv"]:
            flags.append(("fx", r["date"], f"VCB lệch SBV {abs(s-cen)/cen*100:.1f}%"))
        if prev and s and _f(prev.get("vcb_sell")):
            ps = _f(prev["vcb_sell"])
            if abs(s - ps) / ps > JUMP["fx"]:
                flags.append(("fx", r["date"], f"tỷ giá nhảy {(s-ps)/ps*100:+.1f}% so hôm trước"))
        prev = r


def check_fuel(rows, full, errs, flags):
    rows = rows if full else rows[-2:]
    prev = None
    for r in rows:
        v = _f(r.get("ron95"))
        lo, hi = SANITY["fuel"]
        if v is None or not (lo < v < hi):
            errs.append(("fuel", r["effective_date"], f"sanity ron95={v}"))
        if prev and v and _f(prev.get("ron95")):
            pv = _f(prev["ron95"])
            if abs(v - pv) / pv > JUMP["fuel"]:
                flags.append(("fuel", r["effective_date"], f"xăng nhảy {(v-pv)/pv*100:+.1f}% so kỳ trước"))
        prev = r


def check_gas(rows, full, errs, flags):
    rows = rows if full else rows[-2:]
    prev = None
    for r in rows:
        v = _f(r.get("mien_nam"))
        lo, hi = SANITY["gas"]
        if v is None or not (lo < v < hi):
            errs.append(("gas", r["effective_month"], f"sanity mien_nam={v}"))
        if prev and v and _f(prev.get("mien_nam")):
            pv = _f(prev["mien_nam"])
            if abs(v - pv) / pv > JUMP["gas"]:
                flags.append(("gas", r["effective_month"], f"gas nhảy {(v-pv)/pv*100:+.1f}% so tháng trước"))
        prev = r


def check_rates(errs, flags):
    doc = load_json(DATA / "deposit-rates" / "latest.json")
    if not doc:
        return
    lo, hi = SANITY["rate"]
    for r in doc.get("rates", []):
        v = _f(r.get("rate"))
        if v is None or not (lo <= v <= hi):
            errs.append(("rates", doc.get("week", "?"), f"{r.get('bank')} {r.get('term_months')}m rate={v}"))


def main() -> int:
    full = "--full" in sys.argv
    errs: list = []
    flags: list = []
    check_gold(read_csv(DATA / "gold" / "history.csv"), full, errs, flags)
    check_fx(read_csv(DATA / "fx" / "history.csv"), full, errs, flags)
    check_fuel(read_csv(DATA / "fuel" / "history.csv"), full, errs, flags)
    check_gas(read_csv(DATA / "utilities" / "gas.csv"), full, errs, flags)
    check_rates(errs, flags)

    for kind, (mod, when, msg) in [("ERROR", e) for e in errs] + [("FLAG", f) for f in flags]:
        print(f"{kind} {mod} {when} — {msg}")

    dump_json(DATA / "flags.json", {
        "flags": [{"module": m, "when": w, "msg": msg} for m, w, msg in flags],
    })
    emit("SUMMARY", f"errors={len(errs)} flags={len(flags)}")
    return 1 if errs else 0


if __name__ == "__main__":
    raise SystemExit(main())
