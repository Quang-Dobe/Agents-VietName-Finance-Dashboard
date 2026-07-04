#!/usr/bin/env python3
"""Lãi suất tiết kiệm ~20 ngân hàng -> data/deposit-rates/<YYYY-Www>.json

Chỉ chạy thứ Hai (orchestrator kiểm soát lịch). %/năm, gửi tại quầy, lãi cuối kỳ.
Kỳ hạn theo dõi: 1, 3, 6, 12, 24 tháng. 20 mã ngân hàng: xem BANKS bên dưới.

Nguồn (xác nhận live 2026-07-04): **24hmoney.vn/lai-suat-gui-ngan-hang** —
bảng server-rendered `Ngân hàng | 01 | 03 | 06 | 09 | 12 tháng`, số dạng text.
(webgia.com/lai-suat JS-load số → KHÔNG parse được bằng fetch; đừng dùng.)
24hmoney không có cột 24 tháng → term 24 để trống.
"""
from __future__ import annotations

import re
from datetime import date

from common import (DATA, DomainBlocked, dump_json, emit, fetch, strip_tags,
                    vn_number)

SOURCE = "https://24hmoney.vn/lai-suat-gui-ngan-hang"
TERMS = [1, 3, 6, 12, 24]

# Mã ngân hàng -> chuỗi tên xuất hiện trong bảng 24hmoney (khớp không phân biệt hoa/thường).
BANKS = {
    "VCB": "Vietcombank",
    "BIDV": "BIDV",
    "VietinBank": "VietinBank",
    "Agribank": "Agribank",
    "Techcombank": "Techcombank",
    "VPBank": "VPBank",
    "MB": "MBBank",
    "ACB": "ACB",
    "Sacombank": "Sacombank",
    "SHB": "SHB",
    "HDBank": "HDBank",
    "VIB": "VIB",
    "TPBank": "TPBank",
    "MSB": "MSB",
    "OCB": "OCB",
    "Eximbank": "Eximbank",
    "SeABank": "SeABank",
    "LPBank": "LPBank",
    "NamABank": "Nam Á Bank",
    "BacABank": "Bắc Á Bank",
}


def _term_from_header(cell: str) -> int | None:
    m = re.search(r"(\d{1,2})\s*tháng", cell, re.I)
    return int(m.group(1)) if m else None


def _match_bank(name: str) -> str | None:
    """Khớp tên ô đầu dòng với 1 trong 20 mã (chọn chuỗi khớp dài nhất để tránh nhầm)."""
    hits = [(code, sub) for code, sub in BANKS.items() if sub.lower() in name.lower()]
    if not hits:
        return None
    return max(hits, key=lambda x: len(x[1]))[0]


def parse_table(html: str) -> list[dict]:
    """Trả về [{bank, term_months, rate, source_url}] cho 20 ngân hàng theo dõi.

    Bảng: dòng đầu là header (map cột -> kỳ hạn), các dòng sau: [tên NH, r1, r3, r6, r9, r12].
    Ô '-' (thiếu) -> bỏ qua. Chỉ giữ kỳ hạn trong TERMS.
    """
    for t in re.findall(r"(?is)<table.*?</table>", html):
        rows = []
        for rh in re.split(r"(?i)<tr[ >]", t):
            cells = [strip_tags(c) for c in re.findall(r"(?is)<t[dh][^>]*>(.*?)</t[dh]>", rh)]
            cells = [c for c in cells if c != ""]
            if cells:
                rows.append(cells)
        if not rows or not re.search(r"Ngân hàng", rows[0][0] if rows[0] else "", re.I):
            continue
        # map chỉ số cột -> kỳ hạn (cột 0 là tên NH)
        col_term = {i: _term_from_header(h) for i, h in enumerate(rows[0]) if i > 0}
        out: list[dict] = []
        for r in rows[1:]:
            code = _match_bank(r[0])
            if not code:
                continue
            for i, term in col_term.items():
                if term not in TERMS or i >= len(r):
                    continue
                cell = r[i].strip()
                if cell in ("", "-"):
                    continue
                try:
                    rate = vn_number(cell)
                except ValueError:
                    continue
                if 0.1 <= rate <= 15:
                    out.append({"bank": code, "term_months": term, "rate": rate, "source_url": SOURCE})
        if out:
            return out
    return []


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
