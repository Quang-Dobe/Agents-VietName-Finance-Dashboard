#!/usr/bin/env python3
"""Tỷ giá USD/VND của Vietcombank + tỷ giá trung tâm SBV -> data/fx/history.csv

Đơn vị: VND/USD. Cột: vcb_buy_cash, vcb_buy_transfer, vcb_sell, sbv_central.
SBV chập chờn / không công bố cuối tuần -> cho phép rỗng, KHÔNG coi là fail.

CẤU TRÚC NGUỒN: xem CLAUDE.md mục "Nguồn / Tỷ giá". VCB có endpoint XML lâu đời
(portal.vietcombank.com.vn/.../pXML.aspx) — thử endpoint này trước vì rẻ & ổn định;
fail thì parse trang HTML. parse_* là bản đầu, sửa ở lần chạy live đầu (self-heal).
"""
from __future__ import annotations

import re
from datetime import date

from common import (DATA, DomainBlocked, append_csv_row, emit, fetch,
                    strip_tags, vn_number)

FIELDS = ["date", "vcb_buy_cash", "vcb_buy_transfer", "vcb_sell", "sbv_central"]
PATH = DATA / "fx" / "history.csv"

VCB_XML = "https://portal.vietcombank.com.vn/Usercontrols/TVPortal.TyGia/pXML.aspx"
VCB_HTML = "https://www.vietcombank.com.vn/vi-VN/KHCN/Cong-cu-Tien-ich/Ty-gia"
SBV_URL = "https://dttktt.sbv.gov.vn/TyGia/faces/TyGiaTrungTam.jspx"

LO, HI = 15_000, 50_000


def parse_vcb_xml(xml: str) -> tuple[float, float, float]:
    """<Exrate CurrencyCode="USD" Buy="..." Transfer="..." Sell="..."/>."""
    m = re.search(r'CurrencyCode="USD"[^>]*', xml, re.I)
    if not m:
        raise ValueError("XML không có dòng USD")
    seg = m.group(0)
    def attr(name: str) -> float:
        a = re.search(rf'{name}="([\d.,]+)"', seg, re.I)
        if not a:
            raise ValueError(f"XML USD thiếu {name}")
        return vn_number(a.group(1))
    return attr("Buy"), attr("Transfer"), attr("Sell")


def parse_vcb_html(html: str) -> tuple[float, float, float]:
    """Fallback: tìm hàng USD trong bảng tỷ giá, lấy 3 số hợp lệ đầu tiên."""
    text = strip_tags(html)
    m = re.search(r"US\s*Dollar|USD", text, re.I)
    if not m:
        raise ValueError("HTML không thấy hàng USD")
    nums = [vn_number(x) for x in re.findall(r"\d[\d.,]{4,}", text[m.end(): m.end() + 300])]
    good = [n for n in nums if LO < n < HI]
    if len(good) < 3:
        raise ValueError(f"không đủ 3 tỷ giá USD: {good}")
    return good[0], good[1], good[2]


def get_vcb() -> tuple[float, float, float]:
    try:
        return parse_vcb_xml(fetch(VCB_XML))
    except DomainBlocked:
        raise
    except Exception:
        return parse_vcb_html(fetch(VCB_HTML))


def get_sbv() -> float | str:
    """Tỷ giá trung tâm USD. Lỗi -> trả '' (rỗng), không raise."""
    try:
        text = strip_tags(fetch(SBV_URL))
        m = re.search(r"USD", text)
        if not m:
            return ""
        for x in re.findall(r"\d[\d.,]{4,}", text[m.end(): m.end() + 200]):
            n = vn_number(x)
            if LO < n < HI:
                return n
    except Exception:
        pass
    return ""


def main() -> int:
    row = {"date": date.today().isoformat()}
    try:
        row["vcb_buy_cash"], row["vcb_buy_transfer"], row["vcb_sell"] = get_vcb()
    except DomainBlocked as e:
        emit("FAIL", f"blocked: {e}"); return 2
    except Exception as e:  # noqa: BLE001
        emit("FAIL", f"parse vcb: {e}"); return 1

    row["sbv_central"] = get_sbv()

    if not (LO < row["vcb_sell"] < HI) or not (row["vcb_buy_transfer"] <= row["vcb_sell"]):
        emit("FAIL", f"sanity vcb: {row}"); return 1

    changed = append_csv_row(PATH, row, FIELDS)
    sbv = "" if row["sbv_central"] == "" else " (sbv null)" if not row["sbv_central"] else ""
    emit("OK", f"vcb_sell={row['vcb_sell']:.0f}{'' if changed else ' (không đổi)'}{sbv}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
