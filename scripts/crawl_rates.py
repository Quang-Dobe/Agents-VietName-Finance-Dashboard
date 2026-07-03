#!/usr/bin/env python3
"""Lãi suất tiết kiệm ~20 ngân hàng -> data/deposit-rates/<YYYY-Www>.json

Chỉ chạy thứ Hai (orchestrator kiểm soát lịch). %/năm, gửi tại quầy, lãi cuối kỳ.
Kỳ hạn theo dõi: 1, 3, 6, 12, 24 tháng. 20 mã ngân hàng: xem BANKS bên dưới.

Nguồn: bảng tổng hợp webgia.com/lai-suat/. parse_table là bản đầu — sửa ở lần
chạy live đầu (self-heal). Ngân hàng thiếu trong nguồn -> bỏ qua, không fail.
"""
from __future__ import annotations

import re
from datetime import date

from common import (DATA, DomainBlocked, dump_json, emit, fetch, strip_tags,
                    vn_number)

SOURCE = "https://webgia.com/lai-suat/"
TERMS = [1, 3, 6, 12, 24]

# Mã ngân hàng -> các biến thể tên xuất hiện trong bảng nguồn (regex, không dấu OK).
BANKS = {
    "VCB": r"Vietcombank|VCB",
    "BIDV": r"BIDV",
    "VietinBank": r"VietinBank|Vietin",
    "Agribank": r"Agribank",
    "Techcombank": r"Techcombank|TCB",
    "VPBank": r"VPBank|VPB",
    "MB": r"\bMB\b|MBBank|MBB",
    "ACB": r"\bACB\b",
    "Sacombank": r"Sacombank|STB",
    "SHB": r"\bSHB\b",
    "HDBank": r"HDBank|HDB",
    "VIB": r"\bVIB\b",
    "TPBank": r"TPBank|TPB",
    "MSB": r"\bMSB\b|Maritime",
    "OCB": r"\bOCB\b",
    "Eximbank": r"Eximbank|EIB",
    "SeABank": r"SeABank|SeA",
    "LPBank": r"LPBank|LienViet|Lộc Phát",
    "NamABank": r"Nam A|NamABank",
    "BacABank": r"Bac A|BacABank|Bắc Á",
}


def parse_table(html: str) -> list[dict]:
    """Trả về [{bank, term_months, rate, source_url}] cho các ô đọc được.

    Heuristic: cắt HTML theo từng <tr>, dòng nào chứa tên 1 ngân hàng thì đọc
    dãy % trong dòng, gán lần lượt vào TERMS. Cấu trúc thật cần xác nhận lần
    chạy đầu — nếu số cột kỳ hạn khác, sửa mapping tại đây và ghi CLAUDE.md.
    """
    rows_html = re.split(r"(?i)<tr[ >]", html)
    out: list[dict] = []
    for rh in rows_html:
        text = strip_tags(rh)
        bank = next((code for code, pat in BANKS.items() if re.search(pat, text, re.I)), None)
        if not bank:
            continue
        pcts = re.findall(r"(\d{1,2}[.,]\d{1,2})\s*%", text)
        vals = [vn_number(p) for p in pcts]
        vals = [v for v in vals if 0.1 <= v <= 15]
        for term, rate in zip(TERMS, vals):
            out.append({"bank": bank, "term_months": term, "rate": rate, "source_url": SOURCE})
    return out


def iso_week(d: date) -> str:
    y, w, _ = d.isocalendar()
    return f"{y}-W{w:02d}"


def main() -> int:
    today = date.today()
    week = iso_week(today)
    out_path = DATA / "deposit-rates" / f"{week}.json"
    if out_path.exists():
        emit("OK", f"rates – (đã có {week})"); return 0
    try:
        rates = parse_table(fetch(SOURCE))
    except DomainBlocked as e:
        emit("FAIL", f"blocked: {e}"); return 2
    except Exception as e:  # noqa: BLE001
        emit("FAIL", f"parse rates: {e}"); return 1

    if not rates:
        emit("FAIL", "không đọc được ngân hàng nào"); return 1

    doc = {"week": week, "collected_at": today.isoformat(), "source_url": SOURCE, "rates": rates}
    dump_json(out_path, doc)
    dump_json(DATA / "deposit-rates" / "latest.json", doc)
    n_banks = len({r["bank"] for r in rates})
    emit("OK", f"rates ✓ {n_banks} ngân hàng ({week})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
