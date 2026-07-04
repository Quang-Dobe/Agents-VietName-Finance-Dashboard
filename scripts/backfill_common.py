"""Helpers cho backfill: vòng lặp ngày, checkpoint, commit theo lô.

Dùng chung cho backfill_gold.py, backfill_fx.py, ... Chỉ stdlib.
Backfill CHỈ chạy trong one-off run (xem BACKFILL_PROMPTS/), không phải daily.
"""
from __future__ import annotations

from datetime import date, timedelta

from common import DATA, dump_json, load_json

PROGRESS = DATA / "backfill-progress.json"


def daterange(start: date, end: date):
    """Sinh từng ngày [start, end] tăng dần."""
    d = start
    while d <= end:
        yield d
        d += timedelta(days=1)


def parse_iso(s: str) -> date:
    y, m, d = (int(x) for x in s.split("-"))
    return date(y, m, d)


def one_year_ago(today: date) -> date:
    """~1 năm trước (mặc định khoảng backfill khi user không nêu rõ)."""
    try:
        return today.replace(year=today.year - 1)
    except ValueError:  # 29/02
        return today.replace(year=today.year - 1, day=28)


def get_checkpoint(module: str) -> dict:
    prog = load_json(PROGRESS, {}) or {}
    return prog.get(module, {})


def set_checkpoint(module: str, **fields) -> None:
    prog = load_json(PROGRESS, {}) or {}
    prog.setdefault(module, {}).update(fields)
    dump_json(PROGRESS, prog)


def resume_start(module: str, default_start: date) -> date:
    """Điểm bắt đầu: sau ngày done_until trong checkpoint, nếu có."""
    cp = get_checkpoint(module)
    if cp.get("done_until"):
        return parse_iso(cp["done_until"]) + timedelta(days=1)
    return default_start
