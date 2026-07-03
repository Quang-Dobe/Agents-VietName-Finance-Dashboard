# Backfill run 5 — Lãi suất tiết kiệm (chấp nhận partial)

Đọc `CLAUDE.md` và `BACKFILL_PROMPTS/README.md` trước. Đây là run khó nhất —
**chấp nhận partial**, không cố cho đủ.

Nhiệm vụ: tạo các snapshot `data/deposit-rates/<YYYY-Www>.json` cho quá khứ, độ
phân giải **tháng** (1 snapshot/tháng là đủ cho quá khứ — ghi rõ trong provenance).

Nguồn: Wayback Machine của `webgia.com/lai-suat/`:
```
https://web.archive.org/cdx/search/cdx?url=webgia.com/lai-suat/&from=20240701&to=<hôm nay>&output=json
```
Với mỗi tháng, chọn 1 snapshot gần đầu tháng, fetch bản archive, parse bảng như
`scripts/crawl_rates.py` (lọc 20 mã ngân hàng + 5 kỳ hạn). Dùng
`scripts/backfill_rates.py`.

- Snapshot hỏng/thiếu tháng → bỏ qua tháng đó, ghi vào provenance.
- Kỳ vọng thực tế: lấy được 50–80% số tháng là thành công. Chuỗi **tuần** đầy đủ
  bắt đầu từ khi routine daily chạy (thứ Hai hằng tuần).

Checkpoint + commit theo lô. Cập nhật provenance. Xong toàn bộ backfill (run 1–5):
chạy `validate.py --full`, xóa `backfill-progress.json`, gắn tag `backfill-complete`.
