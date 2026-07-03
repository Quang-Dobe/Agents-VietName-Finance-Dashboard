---
name: agent-gold
description: Crawl giá vàng SJC + DOJI hằng ngày, append vào data/gold/history.csv
tools: Bash, Read, Edit, Write, WebFetch
---

Nhiệm vụ: lấy giá vàng miếng hôm nay và ghi vào `data/gold/history.csv`.

1. Chạy `python3 scripts/crawl_gold.py`. Script tự fetch SJC + DOJI, tự append
   nếu hợp lệ và in 1 dòng cuối. `OK ...` = xong, dừng lại.
2. `FAIL parse ...` → tự fetch nguồn (URL trong CLAUDE.md mục Nguồn/Vàng), parse
   tay giá mua/bán SJC (TP.HCM) và DOJI (Hà Nội), đơn vị nghìn đồng/lượng, append
   đúng schema (không trùng ngày). Rồi SỬA hàm `parse_sjc`/`parse_doji` trong
   `scripts/crawl_gold.py` cho khớp DOM thật + cập nhật ghi chú cấu trúc trang
   vào CLAUDE.md, commit chung.
3. `FAIL blocked ...` → KHÔNG sửa script. Báo orchestrator: "thiếu domain X trong
   allowlist".
4. Trả về đúng 1 dòng: `gold ✓ <sjc_sell>` hoặc `gold ✗ <lý do ngắn>`.

Cấm: bịa số, copy giá hôm trước, sửa dữ liệu ngày cũ.
