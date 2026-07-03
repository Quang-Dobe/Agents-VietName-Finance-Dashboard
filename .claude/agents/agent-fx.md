---
name: agent-fx
description: Crawl tỷ giá USD/VND của VCB + tỷ giá trung tâm SBV hằng ngày
tools: Bash, Read, Edit, Write, WebFetch
---

Nhiệm vụ: lấy tỷ giá USD hôm nay và ghi vào `data/fx/history.csv`.

1. Chạy `python3 scripts/crawl_fx.py`. `OK ...` = xong, dừng.
2. `FAIL parse ...` → tự fetch VCB (URL trong CLAUDE.md mục Nguồn/Tỷ giá), parse
   USD: mua tiền mặt, mua chuyển khoản, bán. SBV central lấy từ dttktt.sbv.gov.vn;
   SBV lỗi sau 2 lần thử → để rỗng, KHÔNG coi là fail module. Sửa hàm parse
   trong script + cập nhật CLAUDE.md (self-heal), commit chung.
   Nếu tìm được API JSON tỷ giá theo ngày của VCB, ghi URL đó vào CLAUDE.md để
   dùng cho backfill.
3. `FAIL blocked ...` → báo "thiếu domain", không sửa script.
4. Trả về: `fx ✓ <vcb_sell>` hoặc `fx ✗ <lý do>`.

Cấm: bịa số, copy hôm trước, sửa dữ liệu cũ.
