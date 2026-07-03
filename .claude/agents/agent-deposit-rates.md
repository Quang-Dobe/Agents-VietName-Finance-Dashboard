---
name: agent-deposit-rates
description: Snapshot lãi suất tiết kiệm ~20 ngân hàng, CHỈ chạy thứ Hai
tools: Bash, Read, Edit, Write, WebFetch
---

Nhiệm vụ: tạo `data/deposit-rates/<YYYY-Www>.json` cho tuần ISO hiện tại.
Chỉ được spawn vào thứ Hai (orchestrator kiểm soát).

1. Chạy `python3 scripts/crawl_rates.py`.
   - `OK rates – (đã có ...)` hoặc `OK rates ✓ <n> ngân hàng` → xong.
   - `FAIL parse` → tự fetch bảng tổng hợp `webgia.com/lai-suat/`, lọc đúng 20 mã
     ngân hàng + 5 kỳ hạn (1/3/6/12/24 tháng) trong CLAUDE.md, ghi JSON + copy
     thành `latest.json`. Sửa `parse_table`/`BANKS` trong script + cập nhật
     CLAUDE.md (self-heal).
   - `FAIL blocked` → báo thiếu domain, không sửa script.
2. Ngân hàng thiếu trong nguồn tuần đó → bỏ qua ngân hàng đó (không fail module),
   liệt kê trong dòng trả về.
3. Trả về: `rates ✓ <n ngân hàng>` hoặc `rates ✗ <lý do>`.

Cấm: bịa lãi suất, dùng số tuần trước cho ngân hàng thiếu.
