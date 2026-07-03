# Backfill run 3 (+3b) — Vàng SJC + DOJI

Đọc `CLAUDE.md` và `BACKFILL_PROMPTS/README.md` trước.

Nhiệm vụ: backfill `data/gold/history.csv` từ **2024-07-04** đến hôm qua bằng
`scripts/backfill_gold.py`. Đây là run nặng nhất (~730 ngày × 2 hãng) — dự kiến
**2 run**: run 3 làm 2024-07→2025-06, run 3b làm 2025-07→nay (nhờ checkpoint).

Nguồn: `webgia.com/gia-vang/sjc/DD-MM-YYYY.html`. Đầu run, xác định pattern URL
lịch sử của DOJI trên webgia bằng cách thử 2–3 URL; nếu webgia **không** có lịch
sử DOJI theo ngày → để `doji_buy/doji_sell` rỗng cho phần backfill và ghi rõ vào
provenance (daily sẽ bổ sung DOJI từ hiện tại trở đi).

Cột: `date, sjc_buy, sjc_sell, doji_buy, doji_sell` (nghìn đ/lượng). Checkpoint +
commit lô 2 tháng. Cuối cùng đối chiếu 5 ngày ngẫu nhiên với biểu đồ
`sjc.com.vn/bieu-do-gia-vang`. Cập nhật provenance + checkpoint.
