#!/usr/bin/env python3
"""Backfill tỷ giá VCB theo ngày -> data/fx/history.csv

Chỉ chạy trong one-off run (BACKFILL_PROMPTS/run-1-fx.md). Mặc định ~1 năm.
Nguồn (xác nhận live 2026-07-04): API JSON của Vietcombank có tham số ngày:
  https://www.vietcombank.com.vn/api/exchangerates?date=YYYY-MM-DD
Trả về {"Date","Data":[{"currencyCode":"USD","cash","transfer","sell"},...]}.
API trả rate cho MỌI ngày (kể cả cuối tuần VCB vẫn niêm yết) → không skip.
sbv_central để rỗng cho backfill (chỉ daily mới lấy SBV).

  backfill_fx.py                       # 1 năm gần nhất
  backfill_fx.py --from 2025-07-04 --to 2026-07-03 --batch 60 --sleep 0.3
"""
from __future__ import annotations

import json
import sys
import time
from datetime import date

from backfill_common import (daterange, one_year_ago, parse_iso, resume_start,
                             set_checkpoint)
from common import DATA, DomainBlocked, FetchError, append_csv_row, fetch, vn_number

FIELDS = ["date", "vcb_buy_cash", "vcb_buy_transfer", "vcb_sell", "sbv_central"]
PATH = DATA / "fx" / "history.csv"
API = "https://www.vietcombank.com.vn/api/exchangerates?date={d}"
LO, HI = 15_000, 50_000


def fetch_usd(d: date) -> tuple[float, float, float]:
    """-> (cash, transfer, sell) USD của VCB cho ngày d. Raise nếu không có."""
    doc = json.loads(fetch(API.format(d=d.isoformat())))
    row = next((x for x in doc.get("Data", []) if x.get("currencyCode") == "USD"), None)
    if not row:
        raise ValueError("JSON không có USD")
    return vn_number(row["cash"]), vn_number(row["transfer"]), vn_number(row["sell"])


def main() -> int:
    args = sys.argv[1:]
    def opt(name, default=None):
        return args[args.index(name) + 1] if name in args else default

    today = date.today()
    start = parse_iso(opt("--from")) if "--from" in args else resume_start("fx", one_year_ago(today))
    end = parse_iso(opt("--to")) if "--to" in args else today
    batch = int(opt("--batch", "60"))
    sleep_s = float(opt("--sleep", "0.3"))

    n_ok = n_skip = n_fail = 0
    since_commit = 0
    for d in daterange(start, end):
        iso = d.isoformat()
        time.sleep(sleep_s)
        try:
            cash, transfer, sell = fetch_usd(d)
        except DomainBlocked as e:
            print(f"FAIL blocked: {e} — thêm vietcombank.com.vn vào allowlist rồi chạy lại")
            return 2
        except (FetchError, ValueError, KeyError, json.JSONDecodeError):
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
