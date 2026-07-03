#!/usr/bin/env python3
"""Giá vàng miếng SJC + DOJI hôm nay -> data/gold/history.csv

Đơn vị: nghìn đồng/lượng. SJC lấy tại TP.HCM, DOJI lấy tại Hà Nội (vàng miếng).

CẤU TRÚC TRANG NGUỒN: xem CLAUDE.md mục "Nguồn / Vàng". Hàm parse_* dưới đây
là bản heuristic ĐẦU TIÊN — phải xác nhận/sửa ở lần chạy live đầu tiên (self-heal):
nếu parse fail, agent tự đọc trang, sửa parse_sjc/parse_doji cho khớp DOM thật,
rồi cập nhật ghi chú cấu trúc trang vào CLAUDE.md.
"""
from __future__ import annotations

import re
from datetime import date

from common import (DATA, DomainBlocked, append_csv_row, emit, fetch,
                    strip_tags, vn_number)

FIELDS = ["date", "sjc_buy", "sjc_sell", "doji_buy", "doji_sell"]
PATH = DATA / "gold" / "history.csv"

SJC_URL = "https://sjc.com.vn/gia-vang-online"
DOJI_URL = "https://giavang.doji.vn/"

# Ngưỡng sanity (nghìn đ/lượng) — vùng giá 2025-2026 ~140-160 triệu/lượng.
LO, HI = 30_000, 500_000


def _two_prices_near(text: str, label_regex: str) -> tuple[float, float]:
    """Tìm cặp (mua, bán) là hai số lớn đầu tiên xuất hiện sau nhãn `label_regex`."""
    m = re.search(label_regex, text, re.I)
    if not m:
        raise ValueError(f"không thấy nhãn {label_regex!r}")
    tail = text[m.end(): m.end() + 400]
    nums = [vn_number(x) for x in re.findall(r"\d[\d.,]{4,}", tail)]
    big = [n for n in nums if LO < n < HI]
    if len(big) < 2:
        raise ValueError(f"không đủ 2 giá sau {label_regex!r}: {big}")
    return big[0], big[1]


def parse_sjc(html: str) -> tuple[float, float]:
    """SJC TP.HCM, vàng miếng SJC. -> (buy, sell)."""
    return _two_prices_near(strip_tags(html), r"(Hồ Chí Minh|TPHCM|HCM|Vàng SJC)")


def parse_doji(html: str) -> tuple[float, float]:
    """DOJI Hà Nội, vàng miếng (SJC bar tại DOJI). -> (buy, sell)."""
    return _two_prices_near(strip_tags(html), r"(Hà Nội|SJC)")


def main() -> int:
    row = {"date": date.today().isoformat()}
    try:
        row["sjc_buy"], row["sjc_sell"] = parse_sjc(fetch(SJC_URL))
    except DomainBlocked as e:
        emit("FAIL", f"blocked: {e}"); return 2
    except Exception as e:  # noqa: BLE001 - self-heal đọc lý do
        emit("FAIL", f"parse sjc: {e}"); return 1
    try:
        row["doji_buy"], row["doji_sell"] = parse_doji(fetch(DOJI_URL))
    except DomainBlocked as e:
        emit("FAIL", f"blocked: {e}"); return 2
    except Exception as e:  # noqa: BLE001
        # DOJI fail không chặn SJC — ghi SJC, để DOJI rỗng, vẫn coi là OK phần SJC
        row["doji_buy"] = row["doji_sell"] = ""

    if not (LO < row["sjc_sell"] < HI) or row["sjc_sell"] <= row["sjc_buy"]:
        emit("FAIL", f"sanity sjc: {row}"); return 1

    changed = append_csv_row(PATH, row, FIELDS)
    emit("OK", f"sjc_sell={row['sjc_sell']:.0f}{'' if changed else ' (không đổi)'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
