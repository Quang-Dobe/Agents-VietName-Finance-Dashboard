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
import time
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
    """Lấy (mua, bán) vàng miếng SJC từ trang lịch sử webgia.

    DOM (xác nhận live 2026-07-04): bảng có header 'Mua vào'/'Bán ra', mỗi dòng
    là 1 lần cập nhật trong ngày [Lần, Thời gian, Mua vào, Bán ra]. Lấy DÒNG CUỐI
    (giá chốt ngày). Số dạng '121.300 (+400)' → chỉ lấy '121.300'. SJC đồng giá
    toàn quốc nên không cần chọn khu vực.
    """
    tables = re.findall(r"(?is)<table.*?</table>", html)
    for t in tables:
        if not re.search(r"Mua vào", t, re.I) or not re.search(r"Bán ra", t, re.I):
            continue
        # Phân biệt bảng vàng với widget "Tỷ giá Vietcombank" ở sidebar (cũng có
        # Mua vào/Bán ra): bảng vàng có cột 'Lần'/'Thời gian cập nhật'.
        if not re.search(r"Thời gian|Lần", t, re.I):
            continue
        last = None
        for rh in re.split(r"(?i)<tr[ >]", t):
            cells = [strip_tags(c) for c in re.findall(r"(?is)<t[dh][^>]*>(.*?)</t[dh]>", rh)]
            cells = [c for c in cells if c != ""]
            prices = [vn_number(c) for c in cells if re.match(r"\s*\d[\d.,]{4,}", c)]
            good = [p for p in prices if LO < p < HI]
            if len(good) >= 2:
                last = (good[-2], good[-1])  # 2 số cuối dòng = mua, bán
        if last:
            return last
    raise ValueError("không thấy bảng giá SJC (Mua vào/Bán ra)")


def main() -> int:
    args = sys.argv[1:]
    def opt(name, default=None):
        return args[args.index(name) + 1] if name in args else default

    today = date.today()
    start = parse_iso(opt("--from")) if "--from" in args else resume_start("gold", one_year_ago(today))
    end = parse_iso(opt("--to")) if "--to" in args else today
    batch = int(opt("--batch", "60"))

    sleep_s = float(opt("--sleep", "0.4"))
    n_ok = n_skip = n_fail = 0
    since_commit = 0
    for d in daterange(start, end):
        iso = d.isoformat()
        time.sleep(sleep_s)  # lịch sự với nguồn
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
