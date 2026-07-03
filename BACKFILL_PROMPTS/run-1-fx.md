# Backfill run 1 — Tỷ giá VCB

Đọc `CLAUDE.md` và `BACKFILL_PROMPTS/README.md` (quy tắc chung) trước.

Nhiệm vụ: backfill `data/fx/history.csv` từ **2024-07-04** đến **hôm qua** bằng
`scripts/backfill_fx.py`.

Thứ tự nguồn:
1. Thử API / trang tra cứu tỷ giá **theo ngày** của Vietcombank — nếu lấy được
   JSON/HTML theo ngày thì dùng (rẻ, chính thức). Ghi URL API vào CLAUDE.md nếu tìm ra.
2. Fallback: `webgia.com/ty-gia/vietcombank/DD-MM-YYYY.html`.

Cột: `vcb_buy_cash, vcb_buy_transfer, vcb_sell`. Để `sbv_central` **rỗng** cho
giai đoạn backfill (chỉ crawl daily mới lấy SBV).

Checkpoint + commit theo lô 2 tháng. Xong: cập nhật `provenance.md`,
`backfill-progress.json`, báo cáo tổng số dòng + số ngày thiếu (nếu có).

Đây là run dễ nhất — dùng để dò lại quy trình. Nếu 1 session không đủ, cứ dừng;
run sau resume nhờ checkpoint.
