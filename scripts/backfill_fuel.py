#!/usr/bin/env python3
"""Backfill giá xăng dầu theo kỳ điều hành từ vietnambiz -> data/fuel/history.csv

Chỉ chạy trong one-off run (BACKFILL_PROMPTS/run-2-fuel.md). ~1 năm (~40 kỳ).
Nguồn (xác nhận live 2026-07-04): bài "Giá xăng dầu đồng loạt tăng/giảm..." của
vietnambiz — mỗi kỳ điều hành 1 bài, giá dạng TEXT: "Xăng E5RON92 19.730 đồng/lít".
(Petrolimex đăng bảng giá là ẢNH; webgia fuel JS-load → cả hai không parse được.)

Duyệt listing gia-xang-dau (phân trang /trang-N.html), lọc bài có "đồng loạt"
(bài điều hành trong nước; các bài "hôm nay X/Y" là giá dầu thế giới → bỏ).

  backfill_fuel.py                 # ~1 năm gần nhất
  backfill_fuel.py --pages 60 --sleep 0.3
"""
from __future__ import annotations

import re
import sys
import time
from datetime import date

from common import (DATA, DomainBlocked, FetchError, append_csv_row, fetch,
                    strip_tags, vn_number)

FIELDS = ["effective_date", "ron95", "e5ron92", "diesel", "dau_hoa"]
PATH = DATA / "fuel" / "history.csv"
LIST = "https://vietnambiz.vn/gia-xang-dau.html"
LIST_N = "https://vietnambiz.vn/gia-xang-dau/trang-{n}.html"

# tên nhiên liệu trong bài (E10RON95-III, E5RON92, diesel 0.05S, dầu hỏa)
NAMES = {
    "ron95": r"E10\s*RON\s*95|RON\s*95",
    "e5ron92": r"E5\s*RON\s*92",
    "diesel": r"[Dd]iesel|Điêzen|Đi[eê]zen",
    "dau_hoa": r"[Dd]ầu hỏa|[Dd]ầu hoả",
}
LO, HI = 14_000, 35_000  # đ/lít cho vùng giá hiện hành (loại delta nhỏ)


def parse_prices(html: str) -> dict:
    txt = strip_tags(html)
    out = {}
    for col, name in NAMES.items():
        val = ""
        for m in re.finditer(name, txt):
            for pm in re.finditer(r"([\d.]{5,7})\s*đồng/lít", txt[m.end(): m.end() + 80]):
                v = vn_number(pm.group(1))
                if LO < v < HI:
                    val = v
                    break
            if val != "":
                break
        out[col] = val
    return out


def discover(pages: int, sleep_s: float, start: date):
    """Trả về list (effective_date_iso, url) các bài điều hành trong nước, mới→cũ."""
    seen = {}
    for page in range(1, pages + 1):
        url = LIST if page == 1 else LIST_N.format(n=page)
        try:
            h = fetch(url, retries=1)
        except (DomainBlocked, FetchError):
            break
        for m in re.finditer(r'<a[^>]*href="(/gia-xang-dau[^"]*?(\d{4})\d{6,}\.htm)"\s+title="([^"]*)"', h):
            href, year, title = m.group(1), m.group(2), m.group(3)
            if "đồng loạt" not in title.lower() and "điều chỉnh" not in title.lower():
                continue
            dm = re.search(r"(\d{1,2})/(\d{1,2})", title)
            if not dm:
                continue
            d, mo = int(dm.group(1)), int(dm.group(2))
            if not (1 <= mo <= 12 and 1 <= d <= 31):
                continue
            iso = f"{year}-{mo:02d}-{d:02d}"
            seen.setdefault(iso, "https://vietnambiz.vn" + href)
        oldest = min(seen) if seen else None
        if oldest and oldest < start.isoformat():
            break
        time.sleep(sleep_s)
    return sorted(seen.items())


def main() -> int:
    args = sys.argv[1:]
    def opt(name, d=None):
        return args[args.index(name) + 1] if name in args else d
    pages = int(opt("--pages", "60"))
    sleep_s = float(opt("--sleep", "0.3"))
    start = date.today().replace(year=date.today().year - 1)

    items = discover(pages, sleep_s, start)
    n_ok = n_skip = 0
    for iso, url in items:
        if iso < start.isoformat():
            continue
        time.sleep(sleep_s)
        try:
            prices = parse_prices(fetch(url))
        except DomainBlocked as e:
            print(f"FAIL blocked: {e}"); return 2
        except FetchError:
            n_skip += 1; continue
        if not (isinstance(prices.get("ron95"), float) or isinstance(prices.get("e5ron92"), float)):
            n_skip += 1; continue
        append_csv_row(PATH, {"effective_date": iso, **prices}, FIELDS, key="effective_date")
        n_ok += 1
    print(f"OK fuel backfill: {n_ok} kỳ ghi, {n_skip} bỏ qua (từ {start})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
