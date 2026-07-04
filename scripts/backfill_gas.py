#!/usr/bin/env python3
"""Backfill giá gas bình 12kg theo tháng từ vietnambiz -> data/utilities/gas.csv

Chỉ chạy trong one-off run (BACKFILL_PROMPTS/run-4-gas-dien.md). ~12 tháng.
Nguồn: bài "Giá gas hôm nay 1/M ..." của vietnambiz (kỳ điều chỉnh đầu tháng),
báo giá bình 12kg 3 miền dạng text + giá CP thế giới (USD/tấn).

Cách dùng: truyền danh sách URL bài đầu-tháng (mỗi tháng 1 bài) + effective_month:
  backfill_gas.py 2025-08=<url> 2025-09=<url> ...
URL bài lấy bằng web search / trang listing vietnambiz.vn/gia-gas.html.

DOM xác nhận live 2026-07-04: giá dạng "bình gas 12kg ... còn 502.200 đồng".
"""
from __future__ import annotations

import re
import sys

from common import DATA, DomainBlocked, append_csv_row, fetch, strip_tags, vn_number

FIELDS = ["effective_month", "mien_bac", "mien_trung", "mien_nam", "cp_usd_ton"]
PATH = DATA / "utilities" / "gas.csv"
LO, HI = 200_000, 1_200_000  # đ/bình 12kg

# Mỗi miền: danh sách từ khóa neo, THỬ THEO THỨ TỰ (thành phố cụ thể trước —
# vì câu có giá luôn gắn với thành phố; tên miền chỉ để dự phòng).
REGIONS = {
    "mien_bac": [r"Hà Nội", r"miền Bắc"],
    "mien_trung": [r"Đà Nẵng", r"miền Trung"],
    "mien_nam": [r"TP HCM", r"TP\.HCM", r"TP Hồ Chí Minh", r"miền Nam"],
}

# Giá bình 12kg xuất hiện nhiều kiểu:
#   a) '... còn/ở mức/niêm yết/giữ/lên/là/có giá <PRICE> đồng ...'
#   b) '<PRICE> đồng/bình [dân dụng] 12 kg'
_PAT_A = re.compile(r"(?:còn|ở mức|mức|niêm yết|giữ|lên|là|có giá)\s+([\d.]{5,})\s*đồng", re.I)
_PAT_B = re.compile(r"([\d.]{5,})\s*đồng\s*/?\s*bình\s*(?:dân dụng\s*)?12\s*kg", re.I)


def _price_near(text: str, anchor: str) -> float | str:
    """Lấy giá bình 12kg (200k–700k) gần `anchor`. Duyệt MỌI vị trí xuất hiện của
    anchor (bỏ qua widget thời tiết 'Hà Nội 31°C' ở đầu trang — nó không có giá)."""
    for m in re.finditer(anchor, text, re.I):
        window = text[m.start(): m.start() + 200]
        for pat in (_PAT_B, _PAT_A):  # ưu tiên '<giá> đồng/bình 12kg'
            for mm in pat.finditer(window):
                try:
                    v = vn_number(mm.group(1))
                except ValueError:
                    continue
                if LO < v < 700_000:
                    return v
    return ""


def _price_12kg_after(text: str, anchors: list[str]) -> float | str:
    for a in anchors:
        v = _price_near(text, a)
        if v != "":
            return v
    return ""


def parse_gas_article(html: str) -> dict:
    text = strip_tags(html)
    out = {r: _price_12kg_after(text, anchor) for r, anchor in REGIONS.items()}
    # giá CP thế giới (USD/tấn): lấy MỨC (300–900), không phải delta ('giảm 55 USD/tấn').
    cp = ""
    for mm in re.finditer(r"([\d.,]{3,5})\s*USD/tấn", text, re.I):
        try:
            v = vn_number(mm.group(1))
        except ValueError:
            continue
        if 300 <= v <= 900:  # mức CP hợp lý; loại delta nhỏ & số khác
            cp = v
            break
    out["cp_usd_ton"] = cp
    return out


def main() -> int:
    # args: effective_month=url ...
    items = [a.split("=", 1) for a in sys.argv[1:] if "=" in a]
    if not items:
        print("Cách dùng: backfill_gas.py 2025-08=<url> 2025-09=<url> ...")
        return 1
    n_ok = n_fail = 0
    for month, url in items:
        try:
            prices = parse_gas_article(fetch(url))
        except DomainBlocked as e:
            print(f"FAIL blocked: {e}"); return 2
        except Exception as e:  # noqa: BLE001
            print(f"SKIP {month}: {e}"); n_fail += 1; continue
        if not any(isinstance(prices[k], float) for k in ("mien_bac", "mien_trung", "mien_nam")):
            print(f"SKIP {month}: không đọc được giá miền nào ({prices})"); n_fail += 1; continue
        append_csv_row(PATH, {"effective_month": month, **prices}, FIELDS, key="effective_month")
        print(f"OK {month}: bac={prices['mien_bac']} trung={prices['mien_trung']} nam={prices['mien_nam']} cp={prices['cp_usd_ton']}")
        n_ok += 1
    print(f"DONE gas: ok={n_ok} fail={n_fail}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
