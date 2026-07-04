# Run log

Mỗi run append 1 mục, giữ ≤30 mục gần nhất. ✓ = có dữ liệu mới · – = check không có gì mới · ✗ = fail · skip = không đến lịch.

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
