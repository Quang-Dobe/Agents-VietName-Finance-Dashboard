#!/usr/bin/env python3
"""Backfill tỷ giá VCB theo ngày từ webgia -> data/fx/history.csv

Chỉ chạy trong one-off run (BACKFILL_PROMPTS/run-1-fx.md). Mặc định ~1 năm.
Nguồn: webgia.com/ty-gia/vietcombank/DD-MM-YYYY.html.
sbv_central để rỗng cho backfill (chỉ daily mới lấy SBV).

  backfill_fx.py                      # 1 năm gần nhất
  backfill_fx.py --from 2025-07-04 --to 2026-07-03 --batch 60

DOM webgia CHƯA xác nhận. parse_webgia_vcb là bản đầu — sửa ở lần chạy live đầu.
Nếu tìm được API JSON tỷ giá theo ngày của VCB thì ưu tiên dùng (ghi vào CLAUDE.md).
"""
from __future__ import annotations

import re
import sys
from datetime import date

from backfill_common import (daterange, one_year_ago, parse_iso, resume_start,
                             set_checkpoint)
from common import (DATA, DomainBlocked, FetchError, append_csv_row, fetch,
                    strip_tags, vn_number)

FIELDS = ["date", "vcb_buy_cash", "vcb_buy_transfer", "vcb_sell", "sbv_central"]
PATH = DATA / "fx" / "history.csv"
LO, HI = 15_000, 50_000


def url_for(d: date) -> str:
    return f"https://webgia.com/ty-gia/vietcombank/{d:%d-%m-%Y}.html"


def parse_webgia_vcb(html: str) -> tuple[float, float, float]:
    """Lấy USD (mua tiền mặt, mua CK, bán) từ trang lịch sử webgia."""
    text = strip_tags(html)
    m = re.search(r"US\s*Dollar|USD", text, re.I)
    if not m:
        raise ValueError("không thấy hàng USD")
    nums = [vn_number(x) for x in re.findall(r"\d[\d.,]{4,}", text[m.end(): m.end() + 300])]
    good = [n for n in nums if LO < n < HI]
    if len(good) < 3:
        raise ValueError(f"không đủ 3 tỷ giá: {good}")
    return good[0], good[1], good[2]


def main() -> int:
    args = sys.argv[1:]
    def opt(name, default=None):
        return args[args.index(name) + 1] if name in args else default

    today = date.today()
    start = parse_iso(opt("--from")) if "--from" in args else resume_start("fx", one_year_ago(today))
    end = parse_iso(opt("--to")) if "--to" in args else today
    batch = int(opt("--batch", "60"))

    n_ok = n_skip = n_fail = 0
    since_commit = 0
    for d in daterange(start, end):
        iso = d.isoformat()
        try:
            cash, transfer, sell = parse_webgia_vcb(fetch(url_for(d)))
        except DomainBlocked as e:
            print(f"FAIL blocked: {e} — thêm webgia.com vào allowlist rồi chạy lại")
            return 2
        except (FetchError, ValueError):
            n_skip += 1
            continue
        if not (LO < sell < HI) or transfer > sell:
            n_fail += 1
            continue
        append_csv_row(PATH, {"date": iso, "vcb_buy_cash": cash, "vcb_buy_transfer": transfer,
                              "vcb_sell": sell, "sbv_central": ""}, FIELDS)
        n_ok += 1
        since_commit += 1
        if since_commit >= batch:
            set_checkpoint("fx", done_until=iso, status="in_progress")
            print(f"CHECKPOINT fx done_until={iso} (ok={n_ok} skip={n_skip})")
            since_commit = 0

    set_checkpoint("fx", done_until=end.isoformat(), status="done")
    print(f"OK fx backfill {start}→{end}: ok={n_ok} skip={n_skip} fail={n_fail}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
