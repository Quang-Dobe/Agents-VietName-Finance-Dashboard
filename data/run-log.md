# Run log

Mỗi run append 1 mục, giữ ≤30 mục gần nhất. ✓ = có dữ liệu mới · – = check không có gì mới · ✗ = fail · skip = không đến lịch.

## 2026-07-08 (daily, chạy lại)
- gold ✓ 148.500 (SJC/DOJI cùng giavang.org+giavang.doji.vn, giá real-time giảm so lần chạy trước cùng ngày 149.500 → 148.500)  fx – 26.466 (không đổi)  fuel – (kỳ 02/07 chưa đổi, chưa tới hạn kỳ mới ~11-12/07)  gas – (07/2026 đã có, chưa tới tháng 08)  rates skip  electricity skip
- flags: (không có flag mới; validate.py không --full chỉ quét 2 dòng gần nhất nên 2 flag lịch sử gold 2026-02-03/2026-06-12 không còn xuất hiện trong flags.json — đây là hành vi thiết kế của script, không phải mất dữ liệu, số liệu CSV gốc không đổi)
- ghi chú: không self-heal, không domain thiếu. Đây là lần chạy thứ 2 trong ngày (giờ ~18:05 VN theo lịch daily); giá vàng biến động trong ngày là bình thường.

## 2026-07-08 (daily)
- gold ✓ 149.500 (SJC, tự self-heal: webgia trống bảng hôm nay → chuyển sang giavang.org + giavang.doji.vn)  fx ✓ 26.466  fuel – (kỳ 02/07 chưa đổi)  gas – (07/2026 đã có)  rates skip  electricity skip
- flags: (không có flag mới hôm nay; 2 flag lịch sử gold 2026-02-03/2026-06-12 giữ nguyên)
- ghi chú: sjc.com.vn vẫn 403 → sửa `crawl_gold.py` (parse_sjc dùng giavang.org, parse_doji dùng giavang.doji.vn, cả hai đã có sẵn allowlist, không cần thêm domain mới). Cập nhật ghi chú DOM trong CLAUDE.md.

## 2026-07-04 (backfill fuel + rates, one-off)
- fuel ✓ (8 kỳ 2025-08→2026-07, nguồn tuoitre; E5 đầy đủ, RON95 thưa)  rates ✓ (20 NH, 24hmoney, tuần 2026-W27)
- ghi chú: E5 làm chuỗi chính (RON95 hay bị số tròn/thiếu). Sửa validate cho cột khuyết; fetch chịu IncompleteRead.

## 2026-07-04 (backfill gas, one-off)
- gas ✓ (10 tháng 2025-07→2026-07, nguồn thoibaotaichinhvietnam.vn; miền Bắc/HN đầy đủ, CP có)
- ghi chú: thiếu 2026-01/02/05; miền Trung/Nam thưa. Sửa validate.check_gas cho dữ liệu miền khuyết.

## 2026-07-04 (backfill 1 năm, one-off)
- gold ✓ (265 ngày, 2025-07-04→2026-07-03, nguồn webgia)  fx ✓ (364 ngày, VCB API)
- fuel skip (nguồn ảnh)  gas skip  rates skip  electricity skip
- flags: gold nhảy >5% ngày 2026-02-03 (+6,3%), 2026-06-12 (+5,1%) — biến động thật, giữ.
- ghi chú: allowlist đã mở cho webgia/vietcombank; sjc.com.vn còn chặn. DOJI lịch sử không có.

## 2026-07-03 (seed P0)
- gold ✓  fx ✓ (chỉ sell)  fuel ✓ (kỳ 01/07)  gas ✓ (07/2026)  electricity ✓ (QĐ 1279)  rates skip
- flags: (không)
- ghi chú: seed thủ công từ web search để khởi tạo dashboard; chưa bật routine daily.
