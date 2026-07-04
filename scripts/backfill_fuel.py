#!/usr/bin/env python3
"""Backfill giá xăng dầu theo kỳ điều hành từ tuoitre.vn -> data/fuel/history.csv

Chỉ chạy trong one-off run (BACKFILL_PROMPTS/run-2-fuel.md).
Nguồn (xác nhận live 2026-07-04): bài điều hành giá của **tuoitre.vn** — giá dạng
TEXT sạch, đủ RON95/E5/diesel/dầu hỏa, KHÔNG lẫn giá nước ngoài (khác vietnambiz).
Petrolimex = ẢNH, webgia fuel = JS → cả hai không parse được bằng fetch.

Discovery: tuoitre dùng timeline JS (không walk được như vietnambiz) → truyền
danh sách URL bài điều hành (thu bằng web search) làm tham số. Mỗi bài 1 kỳ.

  backfill_fuel.py <url1> <url2> ...

Bẫy đã xử lý:
- Tiêu đề hay nêu số TRÒN ("vượt mốc 20.000") → ưu tiên giá KHÔNG tròn nghìn (giá thật).
- Năm lấy từ meta article:published_time (ID trên URL không nhất quán).
- Lọc sanity 14.000–26.000 đ/lít (giữ đỉnh sốc 3/2026 ~25.575, loại số parse sai).
"""
from __future__ import annotations

import re
import sys

from common import (DATA, DomainBlocked, FetchError, append_csv_row, fetch,
                    strip_tags, vn_number)

FIELDS = ["effective_date", "ron95", "e5ron92", "diesel", "dau_hoa"]
PATH = DATA / "fuel" / "history.csv"
LO, HI = 14_000, 26_000

NAMES = {
    "ron95": r"E10\s*RON\s*95|RON\s*95|RON95",
    "e5ron92": r"E5\s*RON\s*92|E5RON92|xăng E5",
    "diesel": r"[Dd]iesel",
    "dau_hoa": r"[Dd]ầu hỏa|[Dd]ầu hoả",
}


def parse_article(html: str) -> tuple[str | None, dict]:
    """-> (effective_date_iso hoặc None, {ron95,e5ron92,diesel,dau_hoa}).

    effective_date = NGÀY ĐĂNG bài (điều hành công bố & hiệu lực cùng ngày) — lấy từ
    meta cho chắc; parse ngày trong thân bài hay dính ngày kỳ trước nên không dùng.
    """
    pm = re.search(r'article:published_time"\s*content="(\d{4}-\d{2}-\d{2})', html) or \
        re.search(r'"datePublished":"(\d{4}-\d{2}-\d{2})', html)
    eff = pm.group(1) if pm else None
    txt = strip_tags(html)
    cut = re.search(r"các nước lân cận|nước láng giềng", txt)
    if cut:
        txt = txt[:cut.start()]

    prices = {}
    for col, name in NAMES.items():
        cands = []
        for m in re.finditer(name, txt):
            for pm in re.finditer(r"([\d.]{5,7})\s*đồng/l[íi]t", txt[m.end(): m.end() + 90]):
                try:
                    v = vn_number(pm.group(1))
                except ValueError:
                    continue
                if LO < v < HI:
                    cands.append(v)
        nonround = [v for v in cands if v % 1000 != 0]  # giá thật hiếm khi tròn nghìn
        if col == "ron95":
            # RON95 hay bị tiêu đề nêu số tròn ("vượt mốc 20.000") → chỉ nhận giá
            # chính xác (không tròn nghìn); nếu chỉ có số tròn → để trống, không bịa.
            prices[col] = nonround[0] if nonround else ""
        else:
            prices[col] = (nonround[0] if nonround else (cands[0] if cands else ""))

    return eff, prices


def main() -> int:
    urls = [a for a in sys.argv[1:] if a.startswith("http")]
    if not urls:
        print("Cách dùng: backfill_fuel.py <url tuoitre> ..."); return 1
    n_ok = n_skip = 0
    for url in urls:
        try:
            eff, prices = parse_article(fetch(url, retries=1))
        except DomainBlocked as e:
            print(f"FAIL blocked: {e}"); return 2
        except FetchError:
            n_skip += 1; continue
        if not eff or not any(isinstance(prices[k], float) for k in ("ron95", "e5ron92")):
            print(f"SKIP {url.split('/')[-1][:40]} eff={eff} {prices}"); n_skip += 1; continue
        append_csv_row(PATH, {"effective_date": eff, **prices}, FIELDS, key="effective_date")
        print(f"OK {eff}: ron95={prices['ron95']} e5={prices['e5ron92']} diesel={prices['diesel']}")
        n_ok += 1
    print(f"DONE fuel: {n_ok} kỳ ghi, {n_skip} bỏ qua")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
