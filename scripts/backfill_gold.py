#!/usr/bin/env python3
"""Backfill giá vàng SJC theo ngày từ webgia -> data/gold/history.csv

Chỉ chạy trong one-off run (BACKFILL_PROMPTS/run-3-gold.md). Mặc định ~1 năm.
Nguồn: webgia.com/gia-vang/sjc/DD-MM-YYYY.html (URL theo ngày, về tận 1996).

  backfill_gold.py                    # 1 năm gần nhất (mặc định)
  backfill_gold.py --from 2025-07-04 --to 2026-07-03
  backfill_gold.py --batch 60         # commit-checkpoint mỗi 60 ngày

DOM webgia CHƯA xác nhận (env verify bị chặn). parse_webgia_sjc là bản đầu — ở
lần chạy live đầu, sửa cho khớp DOM thật + ghi chú vào CLAUDE.md (self-heal).
DOJI lịch sử theo ngày trên webgia chưa chắc có → để rỗng nếu không thấy.
"""
from __future__ import annotations

import re
import sys
from datetime import date

from backfill_common import (daterange, one_year_ago, parse_iso, resume_start,
                             set_checkpoint)
from common import (DATA, DomainBlocked, FetchError, append_csv_row, fetch,
                    strip_tags, vn_number)

FIELDS = ["date", "sjc_buy", "sjc_sell", "doji_buy", "doji_sell"]
PATH = DATA / "gold" / "history.csv"
LO, HI = 30_000, 500_000


def url_for(d: date) -> str:
    return f"https://webgia.com/gia-vang/sjc/{d:%d-%m-%Y}.html"


def parse_webgia_sjc(html: str) -> tuple[float, float]:
    """Lấy (mua, bán) vàng miếng SJC tại TP.HCM từ trang lịch sử webgia."""
    text = strip_tags(html)
    m = re.search(r"(SJC|Hồ Chí Minh|TPHCM)", text, re.I)
    if not m:
        raise ValueError("không thấy nhãn SJC/HCM")
    nums = [vn_number(x) for x in re.findall(r"\d[\d.,]{4,}", text[m.end(): m.end() + 400])]
    good = [n for n in nums if LO < n < HI]
    if len(good) < 2:
        raise ValueError(f"không đủ 2 giá: {good}")
    return good[0], good[1]


def main() -> int:
    args = sys.argv[1:]
    def opt(name, default=None):
        return args[args.index(name) + 1] if name in args else default

    today = date.today()
    start = parse_iso(opt("--from")) if "--from" in args else resume_start("gold", one_year_ago(today))
    end = parse_iso(opt("--to")) if "--to" in args else today
    batch = int(opt("--batch", "60"))

    n_ok = n_skip = n_fail = 0
    since_commit = 0
    for d in daterange(start, end):
        iso = d.isoformat()
        try:
            buy, sell = parse_webgia_sjc(fetch(url_for(d)))
        except DomainBlocked as e:
            print(f"FAIL blocked: {e} — thêm webgia.com vào allowlist rồi chạy lại")
            return 2
        except (FetchError, ValueError):
            n_skip += 1  # ngày nghỉ / trang thiếu -> bỏ qua, không bịa
            continue
        if not (LO < sell < HI) or sell <= buy:
            n_fail += 1
            continue
        append_csv_row(PATH, {"date": iso, "sjc_buy": buy, "sjc_sell": sell,
                              "doji_buy": "", "doji_sell": ""}, FIELDS)
        n_ok += 1
        since_commit += 1
        if since_commit >= batch:
            set_checkpoint("gold", done_until=iso, status="in_progress")
            print(f"CHECKPOINT gold done_until={iso} (ok={n_ok} skip={n_skip})")
            since_commit = 0

    set_checkpoint("gold", done_until=end.isoformat(), status="done")
    print(f"OK gold backfill {start}→{end}: ok={n_ok} skip={n_skip} fail={n_fail}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
