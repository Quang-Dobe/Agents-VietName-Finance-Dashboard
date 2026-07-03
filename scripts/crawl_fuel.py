#!/usr/bin/env python3
"""Giá bán lẻ xăng dầu Petrolimex (vùng 1) -> data/fuel/history.csv

1 dòng / kỳ điều hành. Cột: effective_date, ron95, e5ron92, diesel, dau_hoa (đồng/lít).

Thiết kế EXIT SỚM:
  crawl_fuel.py --check    -> in NO_CHANGE hoặc NEW <effective_date> (không ghi)
  crawl_fuel.py --append   -> lấy giá kỳ mới nhất và append nếu chưa có

LƯU Ý THỰC TẾ: từ 06/2026 xăng khoáng RON95-III/V được thay bằng xăng sinh học
E10 RON95. Cột 'ron95' giữ nguyên tên nhưng chứa giá E10 RON95 hiện hành — ghi rõ
trong provenance khi có chuyển đổi. Xem CLAUDE.md mục "Nguồn / Xăng dầu".
"""
from __future__ import annotations

import re
import sys
from datetime import date

from common import (DATA, DomainBlocked, append_csv_row, emit, fetch,
                    read_csv, strip_tags, vn_number)

FIELDS = ["effective_date", "ron95", "e5ron92", "diesel", "dau_hoa"]
PATH = DATA / "fuel" / "history.csv"

LIST_URL = "https://www.petrolimex.com.vn/ndi/thong-cao-bao-chi.html"
LO, HI = 5_000, 60_000

# Nhãn -> cột. Regex nới lỏng để bắt biến thể tên (E10 RON95, RON95-III...).
LABELS = {
    "ron95": r"RON\s*95",
    "e5ron92": r"E5\s*RON\s*92",
    "diesel": r"(Diesel|DO\b|dầu DO)",
    "dau_hoa": r"(dầu hỏa|dầu hoả|Kerosene|KO\b)",
}


def latest_release_date(list_html: str) -> tuple[str, str]:
    """Tìm bài điều chỉnh mới nhất -> (effective_date ISO, url bài)."""
    m = re.search(
        r'href="([^"]*dieu-chinh-gia-xang-dau[^"]*ngay-(\d{1,2})[.-](\d{1,2})[.-](\d{4})[^"]*)"',
        list_html, re.I)
    if not m:
        raise ValueError("không thấy bài điều chỉnh trong trang thông cáo")
    url, d, mo, y = m.group(1), int(m.group(2)), int(m.group(3)), int(m.group(4))
    if url.startswith("/"):
        url = "https://www.petrolimex.com.vn" + url
    return f"{y:04d}-{mo:02d}-{d:02d}", url


def parse_prices(article_html: str) -> dict:
    """Lấy giá vùng 1 từ bài thông cáo. Vùng 1 là cột giá đầu tiên."""
    text = strip_tags(article_html)
    out: dict[str, object] = {}
    for col, lbl in LABELS.items():
        m = re.search(lbl, text, re.I)
        if not m:
            out[col] = ""
            continue
        vals = [vn_number(x) for x in re.findall(r"\d[\d.,]{3,}", text[m.end(): m.end() + 120])]
        good = [v for v in vals if LO < v < HI]
        out[col] = good[0] if good else ""
    return out


def main() -> int:
    mode = "--append" if "--append" in sys.argv else "--check"
    try:
        eff, url = latest_release_date(fetch(LIST_URL))
    except DomainBlocked as e:
        emit("FAIL", f"blocked: {e}"); return 2
    except Exception as e:  # noqa: BLE001
        emit("FAIL", f"parse list: {e}"); return 1

    have = {r["effective_date"] for r in read_csv(PATH)}
    if eff in have:
        emit("NO_CHANGE", eff); return 0
    if mode == "--check":
        emit("NEW", eff); return 0

    try:
        prices = parse_prices(fetch(url))
    except DomainBlocked as e:
        emit("FAIL", f"blocked: {e}"); return 2
    except Exception as e:  # noqa: BLE001
        emit("FAIL", f"parse article: {e}"); return 1

    row = {"effective_date": eff, **prices}
    if not (isinstance(row["ron95"], float) and LO < row["ron95"] < HI):
        emit("FAIL", f"sanity fuel: {row}"); return 1
    append_csv_row(PATH, row, FIELDS, key="effective_date")
    emit("OK", f"{eff} ron95={row['ron95']:.0f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
