# Run log

Mỗi run append 1 mục, giữ ≤30 mục gần nhất. ✓ = có dữ liệu mới · – = check không có gì mới · ✗ = fail · skip = không đến lịch.

## 2026-07-18 (daily)
- gold ✓ 146.600 (SJC 143.600/146.600 qua crawl_gold.py, giavang.org, giảm ~1,1% so hôm qua 148.200; DOJI không lấy được hôm nay — update.giavang.doji.vn chưa có mốc cập nhật khớp ngày, để rỗng theo thiết kế, không self-heal)  fx ✓ 26.490 (VCB API: mua tiền mặt 26.080, mua CK 26.110, bán 26.490; SBV central rỗng; tăng ~0,15% so hôm qua 26.450)  fuel – kỳ 16/07 không đổi (crawl_fuel.py --check → NO_CHANGE, chưa tới hạn kỳ mới)  gas – ngoài cửa sổ ngày 1-4 nên bỏ qua check tháng 08  rates skip  electricity skip
- flags: (không có flag mới; validate.py: errors=0 flags=0; 2 flag lịch sử gold 2026-02-03/2026-06-12 giữ nguyên trong flags.json, không liên quan run này)
- ghi chú: hôm nay thứ Bảy nên rates & electricity skip theo lịch. Không self-heal, không domain thiếu. site-builder OK 5/5 module.

## 2026-07-17 (daily)
- gold ✓ 148.200 (SJC 145.200/148.200 qua crawl_gold.py, giavang.org, giảm ~0,2% so hôm qua 148.500; DOJI không lấy được hôm nay — nguồn update.giavang.doji.vn chưa có mốc cập nhật khớp ngày, script tự để rỗng theo thiết kế, không self-heal)  fx ✓ 26.450 (VCB API: mua tiền mặt 26.040, mua CK 26.070, bán 26.450; SBV central rỗng; không đổi so hôm qua)  fuel ✓ kỳ 16/07 (E10 RON95-III 20.550, E5RON92-II 19.820, diesel 0,05S-II 23.320, dầu hỏa 2-K 24.590 — tăng lần lượt +2,75%/+3,3%/+7,3%/+13,8% so kỳ 09/07, dưới ngưỡng flag 20%; Petrolimex daily vẫn bảng ảnh nên đọc tay từ giaban.jpg thông cáo PLX theo đúng fallback đã ghi trong CLAUDE.md, tuoitre chưa đăng bài kỳ mới nên không self-heal crawl_fuel.py)  gas – (07/2026 đã có, chưa tới hạn tháng 08, hôm nay ngoài khung ngày 1-4 nên bỏ qua check)  rates skip  electricity skip
- flags: (không có flag mới; validate.py: errors=0 flags=0)
- ghi chú: hôm nay thứ Sáu nên rates & electricity skip theo lịch. Không self-heal script, không domain thiếu. site-builder OK 5/5 module.

## 2026-07-16 (daily)
- gold ✓ 148.500 (SJC 145.500/148.500 qua crawl_gold.py, giavang.org, tăng ~0,68% so hôm qua 147.500; DOJI không lấy được hôm nay, để rỗng, không self-heal)  fx ✓ 26.450 (VCB API: mua tiền mặt 26.040, mua CK 26.070, bán 26.450; SBV central rỗng; không đổi so hôm qua)  fuel – kỳ 09/07 không đổi (chưa tới hạn kỳ mới, dự kiến ~19-20/07)  gas – (07/2026 đã có, chưa tới hạn tháng 08)  rates skip  electricity skip
- flags: (không có flag mới; validate.py: errors=0 flags=0)
- ghi chú: hôm nay thứ Năm nên rates & electricity skip theo lịch. Không self-heal, không domain thiếu. site-builder OK 5/5 module.

## 2026-07-15 (daily)
- gold ✓ 147.500 (SJC/DOJI cùng 144.500/147.500, giavang.org+giavang.doji.vn qua crawl_gold.py, giảm ~0,6% so hôm qua 148.400, không self-heal)  fx ✓ 26.450 (VCB API: mua tiền mặt 26.040, mua CK 26.070, bán 26.450; SBV central rỗng; giảm ~0,04% so hôm qua)  fuel – kỳ 09/07 không đổi (chưa tới hạn kỳ mới, dự kiến ~19-20/07)  gas – (07/2026 đã có, chưa tới hạn tháng 08)  rates skip  electricity skip
- flags: (không có flag mới; validate.py: errors=0 flags=0)
- ghi chú: hôm nay thứ Tư nên rates & electricity skip theo lịch. Không self-heal, không domain thiếu. site-builder OK 5/5 module.

## 2026-07-14 (daily)
- gold ✓ 148.400 (SJC/DOJI cùng 145.400/148.400, giavang.org+giavang.doji.vn qua crawl_gold.py, giảm ~1% so hôm qua 149.900, không self-heal)  fx ✓ 26.460 (VCB API: mua tiền mặt 26.050, mua CK 26.080, bán 26.460; SBV central rỗng; giảm ~0,04% so hôm qua)  fuel – kỳ 09/07 không đổi (chưa tới hạn kỳ mới, dự kiến ~19-20/07)  gas – (07/2026 đã có, chưa tới hạn tháng 08)  rates skip  electricity skip
- flags: (không có flag mới; validate.py: errors=0 flags=0)
- ghi chú: hôm nay thứ Ba nên rates & electricity skip theo lịch. Không self-heal, không domain thiếu. site-builder OK 5/5 module.

## 2026-07-13 (daily)
- gold ✓ 149.900 (SJC/DOJI cùng 146.900/149.900, giavang.org+giavang.doji.vn qua crawl_gold.py, không self-heal)  fx ✓ 26.470 (VCB API: mua tiền mặt 26.060, mua CK 26.090, bán 26.470; SBV central rỗng)  fuel – kỳ 09/07 không đổi (chưa tới hạn kỳ mới, dự kiến ~19-20/07)  gas – (07/2026 đã có, chưa tới hạn tháng 08)  rates ✓ 20 ngân hàng (2026-W29, 24hmoney, kỳ hạn 1/3/6/12, 24 tháng để trống)  electricity – (QĐ 1279/QĐ-BCT vẫn hiện hành; NĐ 278/2026/NĐ-CP mới chỉ đổi thẩm quyền điều chỉnh giá bình quân, không đổi biểu giá bậc thang)
- flags: (không có flag mới; validate.py: errors=0 flags=0)
- ghi chú: thứ Hai nên chạy đủ 5 module. Không self-heal, không domain thiếu. site-builder OK 5/5 module.

## 2026-07-12 (daily)
- gold ✓ 149.900 (SJC/DOJI, giavang.org+giavang.doji.vn qua crawl_gold.py, không đổi so hôm qua — giá cuối tuần giữ nguyên, không self-heal)  fx ✓ 26.470 (VCB API, vcb_buy_cash 26.060/vcb_buy_transfer 26.090, không đổi so hôm qua, SBV central rỗng)  fuel – kỳ 09/07 không đổi (chưa tới hạn kỳ mới, dự kiến ~19-20/07)  gas – (07/2026 đã có, chưa tới hạn tháng 08)  rates skip  electricity skip
- flags: (không có flag mới; validate.py: errors=0 flags=0)
- ghi chú: không self-heal, không domain thiếu. Giá vàng/tỷ giá trùng với 2026-07-11 do cuối tuần thị trường không cập nhật — xác nhận là dữ liệu thật từ 2 lần crawl độc lập, không phải copy tay.

## 2026-07-11 (daily)
- gold ✓ 149.900 (SJC/DOJI, giavang.org+giavang.doji.vn qua crawl_gold.py, tăng 900 so hôm qua 149.000, không self-heal)  fx ✓ 26.470 (VCB API, buy_cash 26.060/buy_transfer 26.090/sell 26.470, SBV central rỗng)  fuel – kỳ 09/07 không đổi (crawl_fuel.py --check → NO_CHANGE, chưa tới hạn kỳ mới ~19-20/07)  gas – (07/2026 đã có, ngoài cửa sổ ngày 1-4 nên chưa check tháng 08)  rates skip  electricity skip
- flags: (không có flag mới; validate.py: errors=0 flags=0)
- ghi chú: không self-heal, không domain thiếu. Hôm nay Thứ Bảy nên rates & electricity skip theo lịch.

## 2026-07-10 (daily)
- gold ✓ 149.000 (SJC/DOJI, giavang.org+giavang.doji.vn qua crawl_gold.py, không đổi so với hôm qua, không self-heal)  fx – 26.471 (VCB API, giá VCB chưa cập nhật trong ngày, SBV central rỗng)  fuel – kỳ 09/07 không đổi (chưa tới hạn kỳ mới, dự kiến ~19-20/07)  gas – (07/2026 đã có, chưa tới hạn tháng 08)  rates skip  electricity skip
- flags: (không có flag mới; validate.py: errors=0 flags=0)
- ghi chú: không self-heal, không domain thiếu. Build trên nhánh nối tiếp PR #3 (2026-07-09) vì PR đó chưa merge vào lúc chạy, giữ đúng thứ tự ngày trong CSV.

## 2026-07-09 (daily)
- gold ✓ 149.000 (SJC/DOJI, giavang.org+giavang.doji.vn, không self-heal)  fx ✓ 26.471 (VCB, SBV central rỗng)  fuel ✓ kỳ 09/07 (20.000/19.190/21.740/21.610 — tuoitre chưa đăng bài kỳ mới nên đọc tay ảnh giabanle.jpg từ thông cáo Petrolimex 40/2026/PLX-TCBC, chọn đúng dòng III/II phổ thông, ghi fallback vào CLAUDE.md)  gas – (07/2026 đã có, chưa tới hạn tháng 08)  rates skip  electricity skip
- flags: (không có flag mới; validate.py: errors=0 flags=0)
- ghi chú: không domain thiếu. Cập nhật CLAUDE.md mục Xăng dầu với quy trình fallback đọc ảnh tay khi tuoitre chưa đăng bài kỳ mới (không sửa `parse_prices` vì regex không đọc được ảnh).

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
