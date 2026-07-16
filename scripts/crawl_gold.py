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

# sjc.com.vn bị chặn allowlist (2026-07) -> dùng giavang.org (đã whitelist,
# aggregator giá SJC toàn quốc, cập nhật real-time, cùng nguồn dữ liệu mà
# webgia.com credit "Nguồn: ... SJC, giavang.org"). Xem ghi chú DOM ở CLAUDE.md.
SJC_URL = "https://giavang.org/"
# giavang.doji.vn từ ~2026-07-16 redirect 301 sang banggia.doji.vn (Angular SPA,
# JS-render, không có số trong HTML tĩnh) -> dùng subdomain cũ update.giavang.doji.vn
# (vẫn server-rendered kiểu Drupal) làm nguồn chính. Xem ghi chú DOM ở CLAUDE.md.
DOJI_URL = "https://update.giavang.doji.vn/"

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
    """SJC (giá vàng miếng toàn quốc, giavang.org). -> (buy, sell).

    DOM: khối `<h2>...Giá vàng Miếng SJC</h2>` rồi tới 2 khối
    `<span class="gold-price-label">Mua vào</span> ... <span class="gold-price">146.500 <small class="gold-unit">x1000đ/lượng</small>`.
    Số hiển thị ĐÃ là nghìn đồng/lượng (không cần quy đổi) — "146.500" -> 146500.
    """
    m = re.search(r"Giá vàng\s*Miếng SJC", html, re.I)
    if not m:
        raise ValueError("không thấy khối 'Giá vàng Miếng SJC'")
    block = html[m.end(): m.end() + 1500]
    prices = re.findall(r'class="gold-price">\s*([\d.,]+)\s*<small class="gold-unit">x1000', block)
    if len(prices) < 2:
        raise ValueError(f"không đủ 2 giá trong khối SJC: {prices}")
    buy, sell = vn_number(prices[0]), vn_number(prices[1])
    return buy, sell


def parse_doji(html: str) -> tuple[float, float]:
    """DOJI (giá vàng trong nước, quầy DOJI), qua subdomain cũ update.giavang.doji.vn
    (giavang.doji.vn nay redirect 301 sang banggia.doji.vn — Angular SPA, JS-render,
    không đọc được bằng fetch tĩnh). -> (buy, sell).

    DOM: bảng `table.goldprice-view` đầu tiên trong trang (khối "Giá vàng trong
    nước"), dòng `<td class="first"><span class="title...">SJC -Bán Lẻ</span>...`
    kèm 2 `<td class="goldprice-td..."><div class="item-relative">14,550</div></td>`
    (mua, bán). Đơn vị NGHÌN ĐỒNG/CHỈ (ghi chú "(nghìn/chỉ)" cạnh nhãn) -> nhân 10
    ra nghìn đồng/lượng.

    Subdomain này là trang legacy, có dấu hiệu đứng cập nhật (thấy đơ ở
    2026-07-15 08:50 khi chạy ngày 2026-07-16) -> BẮT BUỘC kiểm tra mốc
    "Cập nhập lúc: HH:MM DD/MM/YYYY" khớp NGÀY HÔM NAY, không thì coi là dữ liệu
    cũ và raise (để DOJI trống thay vì lặp lại giá hôm qua).
    """
    fresh_m = re.search(r"Cập nhập lúc:\s*\d{2}:\d{2}\s*(\d{2})/(\d{2})/(\d{4})", html)
    if not fresh_m:
        raise ValueError("không thấy mốc 'Cập nhập lúc'")
    dd, mm, yyyy = fresh_m.groups()
    page_date = f"{yyyy}-{mm}-{dd}"
    if page_date != date.today().isoformat():
        raise ValueError(f"dữ liệu DOJI cũ (trang ghi {page_date}, hôm nay {date.today().isoformat()})")
    row_m = re.search(
        r'<td class="first"><span class="title[^>]*>SJC\s*-\s*Bán\s*Lẻ</span>.*?</td>'
        r'\s*<td[^>]*><div class="item-relative">([\d.,]+)</div></td>'
        r'\s*<td[^>]*><div class="item-relative">([\d.,]+)</div></td>',
        html, re.S)
    if not row_m:
        raise ValueError("không thấy dòng 'SJC -Bán Lẻ' trong bảng giá trong nước")
    buy = vn_number(row_m.group(1)) * 10
    sell = vn_number(row_m.group(2)) * 10
    return buy, sell


def get_sjc() -> tuple[float, float]:
    """SJC hôm nay. Thử webgia (giá chốt trong ngày, chỉ có sau ~18h VN) TRƯỚC;
    nếu webgia lỗi/chưa có bảng (chạy sớm trong ngày, hoặc T7/CN/lễ) thì thử
    giavang.org (giá real-time, luôn có, dùng thay sjc.com.vn đang bị chặn)."""
    from backfill_gold import parse_webgia_sjc, url_for  # bảng lịch sử = giá trong ngày
    try:
        return parse_webgia_sjc(fetch(url_for(date.today())))
    except DomainBlocked:
        pass  # webgia chặn → thử nguồn dự phòng
    except Exception:
        pass  # webgia chưa có bảng hôm nay → thử nguồn dự phòng
    return parse_sjc(fetch(SJC_URL))


def main() -> int:
    row = {"date": date.today().isoformat()}
    try:
        row["sjc_buy"], row["sjc_sell"] = get_sjc()
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
