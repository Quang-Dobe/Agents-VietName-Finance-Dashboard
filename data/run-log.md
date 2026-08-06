# Run log

Mỗi run append 1 mục, giữ ≤30 mục gần nhất. ✓ = có dữ liệu mới · – = check không có gì mới · ✗ = fail · skip = không đến lịch.

## 2026-08-06 (daily)
- gold ✓ 141.800 (SJC 138.800/141.800 qua crawl_gold.py, giavang.org, tăng ~0,93% so hôm qua 140.500, dưới ngưỡng flag 5%/ngày; DOJI không lấy được hôm nay — update.giavang.doji.vn tiếp tục không ổn định, để rỗng theo thiết kế, không self-heal)  fx ✓ 26.460 (VCB API: mua tiền mặt 26.050, mua CK 26.080, bán 26.460; SBV central rỗng; không đổi so hôm qua)  fuel – NO_CHANGE kỳ 30/07 (crawl_fuel.py --check → NO_CHANGE, chưa tới hạn kỳ mới)  gas skip (ngoài cửa sổ check 1-4, tháng 08/2026 đã có sẵn)  rates skip  electricity skip
- flags: (không có flag mới; validate.py: errors=0 flags=0)
- ghi chú: hôm nay thứ Năm nên rates & electricity skip theo lịch. Không self-heal, không domain thiếu. site-builder OK 5/5 module.

## 2026-08-05 (daily)
- gold ✓ 140.500 (SJC 137.500/140.500 qua crawl_gold.py, giavang.org, bán giảm ~0,35% so hôm qua 141.000, mua không đổi, dưới ngưỡng flag 5%/ngày; DOJI không lấy được hôm nay — update.giavang.doji.vn tiếp tục không ổn định, để rỗng theo thiết kế, không self-heal)  fx ✓ 26.460 (VCB API: mua tiền mặt 26.050, mua CK 26.080, bán 26.460; SBV central rỗng; giảm nhẹ ~0,08% so hôm qua)  fuel – NO_CHANGE kỳ 30/07 (crawl_fuel.py --check → NO_CHANGE, chưa tới hạn kỳ mới)  gas skip (tháng 08/2026 đã có sẵn, ngoài cửa sổ check 1-4)  rates skip  electricity skip
- flags: (không có flag mới; validate.py: errors=0 flags=0)
- ghi chú: hôm nay thứ Tư nên rates & electricity skip theo lịch. Không self-heal, không domain thiếu. site-builder OK 5/5 module.

## 2026-08-04 (daily)
- gold ✓ 141.000 (SJC 137.500/141.000 qua crawl_gold.py, giavang.org, mua tăng nhẹ ~0,4% so hôm qua 137.000, bán giữ nguyên, dưới ngưỡng flag 5%/ngày; DOJI không lấy được hôm nay — update.giavang.doji.vn tiếp tục không ổn định, để rỗng theo thiết kế, không self-heal)  fx – 26.480 (VCB API: mua tiền mặt 26.070, mua CK 26.100, bán 26.480; SBV central rỗng; giảm nhẹ ~0,04% so hôm qua)  fuel – NO_CHANGE kỳ 30/07 (crawl_fuel.py --check → NO_CHANGE, chưa tới hạn kỳ mới)  gas ✓ tháng 08/2026 (miền Bắc 518.400 / miền Trung 538.000 / miền Nam 552.000, nguồn vietnambiz.vn "Giá gas hôm nay 3/8", CP rỗng — ngày cuối cửa sổ 1-4/8, cuối cùng tìm được bài đủ tin cậy sau 3 ngày chưa có; tăng 3,2-11,4% so tháng 07, dưới ngưỡng flag 30%/tháng)  rates skip  electricity skip
- flags: (không có flag mới; validate.py: errors=0 flags=0)
- ghi chú: hôm nay thứ Ba nên rates & electricity skip theo lịch. Không self-heal, không domain thiếu. site-builder OK 5/5 module.

## 2026-08-03 (daily)
- gold ✓ 141.000 (SJC 137.000/141.000 qua crawl_gold.py, giavang.org, không đổi so hôm qua, dưới ngưỡng flag 5%/ngày; DOJI không lấy được hôm nay — update.giavang.doji.vn tiếp tục không ổn định, để rỗng theo thiết kế, không self-heal)  fx – 26.490 (VCB API: mua tiền mặt 26.080, mua CK 26.110, bán 26.490; SBV central rỗng; không đổi so hôm qua)  fuel – NO_CHANGE kỳ 30/07 (crawl_fuel.py --check → NO_CHANGE, chưa tới hạn kỳ mới)  gas – trong cửa sổ ngày 1-4 nhưng vẫn chưa có bài giá gas tháng 08 đủ tin cậy (đã thử lại vietnambiz.vn, thoibaotaichinhvietnam.vn, alogas.vn; alogas chỉ có giá khuyến mãi giao hàng 1 đại lý tư nhân TPHCM, không phải giá bán lẻ vùng miền chính thức, giữ đánh giá không dùng như 2 ngày trước)  rates ✓ 2026-W32 (20/20 ngân hàng, 24hmoney, không ngân hàng nào đổi lãi suất so với 2026-W31 — có vẻ nguồn chưa cập nhật số liệu tuần này)  electricity – (QĐ 1279/QĐ-BCT vẫn hiện hành, không có biểu giá mới; ghi chú kỹ thuật: URL dự phòng cũ trong CLAUDE.md trả về trang chủ, URL đúng hiện tại là dạng `/d/vi-VN/news/...`, chưa cập nhật vào CLAUDE.md vì không có thay đổi biểu giá cần self-heal)
- flags: (không có flag mới; validate.py: errors=0 flags=0)
- ghi chú: hôm nay thứ Hai nên chạy đủ 5 module. Không self-heal, không domain thiếu. site-builder OK 5/5 module.

## 2026-08-02 (daily)
- gold ✓ 141.000 (SJC 137.000/141.000 qua crawl_gold.py, giavang.org, giảm ~0,65% so hôm qua 137.900/141.900, dưới ngưỡng flag 5%/ngày; DOJI không lấy được hôm nay — update.giavang.doji.vn tiếp tục không ổn định, để rỗng theo thiết kế, không self-heal)  fx – 26.490 (VCB API: mua tiền mặt 26.080, mua CK 26.110, bán 26.490; SBV central rỗng; không đổi so hôm qua)  fuel – NO_CHANGE kỳ 30/07 (crawl_fuel.py --check → NO_CHANGE, chưa tới hạn kỳ mới)  gas – trong cửa sổ ngày 1-4 nhưng chưa có bài giá gas tháng 08 (đã kiểm vietnambiz.vn, thoibaotaichinhvietnam.vn, thêm alogas.vn nhưng chỉ có giá TPHCM mơ hồ không đủ tin cậy theo schema 3 miền; sẽ thử lại các ngày tới trong cửa sổ 1-4/8)  rates skip  electricity skip
- flags: (không có flag mới; validate.py: errors=0 flags=0)
- ghi chú: hôm nay thứ Chủ nhật nên rates & electricity skip theo lịch. Không self-heal, không domain thiếu. site-builder OK 5/5 module.

## 2026-08-01 (daily)
- gold ✓ 141.900 (SJC 137.900/141.900 qua crawl_gold.py, giavang.org, tăng nhẹ ~0,14% so hôm qua 141.700, dưới ngưỡng flag 5%/ngày; DOJI không lấy được hôm nay — update.giavang.doji.vn tiếp tục không ổn định, để rỗng theo thiết kế, không self-heal)  fx ✓ 26.490 (VCB API: mua tiền mặt 26.080, mua CK 26.110, bán 26.490; SBV central rỗng; không đổi so hôm qua — VCF giữ giá cuối tuần theo giá đóng cửa thứ Sáu, `UpdatedDate` xác nhận đây là giá trả về đúng chứ không phải lỗi copy)  fuel – NO_CHANGE kỳ 30/07 (crawl_fuel.py --check → NO_CHANGE, kỳ mới vừa bắt đầu 2 ngày trước)  gas – trong cửa sổ ngày 1-4 nhưng chưa có bài giá gas tháng 08 (đã kiểm vietnambiz.vn/gia-gas/trang-1.html — bài mới nhất vẫn là 31/7; thoibaotaichinhvietnam.vn chưa có bài tháng 08 qua các URL thử; sẽ thử lại trong cửa sổ 1-4/8)  rates skip  electricity skip
- flags: (không có flag mới; validate.py: errors=0 flags=0)
- ghi chú: hôm nay thứ Bảy nên rates & electricity skip theo lịch. Không self-heal, không domain thiếu. site-builder OK 5/5 module. Lưu ý: một lần WebFetch AI-processed trên thoibaotaichinhvietnam.vn trả nội dung có vẻ hợp lý nhưng HTML gốc (curl) rỗng — nghi hallucination của WebFetch, đã bỏ qua và chỉ dùng dữ liệu từ HTML gốc; không ảnh hưởng đến dữ liệu commit (gas giữ nguyên).

## 2026-07-31 (daily)
- gold ✓ 141.700 (SJC 137.700/141.700 qua crawl_gold.py, giavang.org, tăng nhẹ +0,14% so hôm qua 141.500, dưới ngưỡng flag 5%/ngày; DOJI không lấy được hôm nay — update.giavang.doji.vn tiếp tục không ổn định, để rỗng theo thiết kế, không self-heal)  fx ✓ 26.490 (VCB API: mua tiền mặt 26.080, mua CK 26.110, bán 26.490; SBV central rỗng; giảm ~0,09% so hôm qua 26.515)  fuel ✓ kỳ mới 2026-07-30 (hiệu lực 15h00 30/7, sớm hơn 1 ngày so ước tính ~31/07; RON95 E10-III 22.850, E5RON92 22.380, Diesel 0.05S-II 27.620, Dầu hỏa 27.400 — tăng ~6,6-7,2% so kỳ 23/07, dưới ngưỡng flag 20%; bảng Petrolimex vẫn là ảnh, tuoitre vẫn chưa có bài dùng được nên đọc tay giabanle.jpg theo quy trình fallback đã ghi trong CLAUDE.md)  gas – ngoài cửa sổ ngày 1-4 nên bỏ qua check tháng 08 (07/2026 đã có sẵn)  rates skip  electricity skip
- flags: (không có flag mới; validate.py: errors=0 flags=0)
- ghi chú: hôm nay thứ Sáu nên rates & electricity skip theo lịch. Không self-heal, không domain thiếu. site-builder OK 5/5 module.

## 2026-07-30 (daily)
- gold ✓ 141.500 (SJC 137.500/141.500 qua crawl_gold.py, giavang.org, không đổi so hôm qua 2026-07-29, dưới ngưỡng flag 5%/ngày; DOJI không lấy được hôm nay — update.giavang.doji.vn vẫn không ổn định, để rỗng theo thiết kế, không self-heal)  fx ✓ 26.515 (VCB API: mua tiền mặt 26.105, mua CK 26.135, bán 26.515; SBV central rỗng; giảm ~0,04% so hôm qua 26.525)  fuel – NO_CHANGE kỳ 23/07 (crawl_fuel.py --check → NO_CHANGE, chưa tới hạn kỳ mới, dự kiến ~31/07)  gas – ngoài cửa sổ ngày 1-4 nên bỏ qua check tháng 08 (07/2026 đã có sẵn)  rates skip  electricity skip
- flags: (không có flag mới; validate.py: errors=0 flags=0)
- ghi chú: hôm nay thứ Năm nên rates & electricity skip theo lịch. Không self-heal, không domain thiếu. site-builder OK 5/5 module.

## 2026-07-29 (daily)
- gold ✓ 141.500 (SJC 137.500/141.500 qua crawl_gold.py, giavang.org, giảm ~1,0% so hôm qua 139.000/143.000, dưới ngưỡng flag 5%/ngày; DOJI không lấy được hôm nay — update.giavang.doji.vn vẫn không ổn định, để rỗng theo thiết kế, không self-heal)  fx ✓ 26.525 (VCB API: mua tiền mặt 26.115, mua CK 26.145, bán 26.525; SBV central rỗng; tăng ~0,02% so hôm qua 26.520)  fuel – NO_CHANGE kỳ 23/07 (crawl_fuel.py --check → NO_CHANGE, chưa tới hạn kỳ mới, dự kiến ~31/07)  gas – ngoài cửa sổ ngày 1-4 nên bỏ qua check tháng 08 (07/2026 đã có sẵn)  rates skip  electricity skip
- flags: (không có flag mới; validate.py: errors=0 flags=0)
- ghi chú: hôm nay thứ Tư nên rates & electricity skip theo lịch. Không self-heal, không domain thiếu. site-builder OK 5/5 module.

## 2026-07-28 (daily)
- gold ✓ 143.000 (SJC 139.000/143.000 qua crawl_gold.py, giavang.org, tăng ~1,06%/~1,09% so hôm qua 137.500/141.500, dưới ngưỡng flag 5%/ngày; DOJI không lấy được hôm nay — update.giavang.doji.vn vẫn không ổn định, để rỗng theo thiết kế, không self-heal)  fx ✓ 26.520 (VCB API: mua tiền mặt 26.110, mua CK 26.140, bán 26.520; SBV central rỗng; tăng ~0,04% so hôm qua 26.510)  fuel – NO_CHANGE kỳ 23/07 (crawl_fuel.py --check → NO_CHANGE, chưa tới hạn kỳ mới, dự kiến ~31/07)  gas – ngoài cửa sổ ngày 1-4 nên bỏ qua check tháng 08 (07/2026 đã có sẵn)  rates skip  electricity skip
- flags: (không có flag mới; validate.py: errors=0 flags=0)
- ghi chú: hôm nay thứ Ba nên rates & electricity skip theo lịch. Không self-heal, không domain thiếu. site-builder OK 5/5 module.

## 2026-07-27 (daily)
- gold ✓ 141.500 (SJC 137.500/141.500 qua crawl_gold.py, giavang.org, không đổi so hôm qua 2026-07-26, dưới ngưỡng flag 5%/ngày; DOJI không lấy được hôm nay — update.giavang.doji.vn vẫn không ổn định, để rỗng theo thiết kế, không self-heal)  fx ✓ 26.510 (VCB API: mua tiền mặt 26.100, mua CK 26.130, bán 26.510; SBV central rỗng; không đổi so hôm qua)  fuel – NO_CHANGE kỳ 23/07 (crawl_fuel.py --check → NO_CHANGE, chưa tới hạn kỳ mới, dự kiến ~31/07)  gas – ngoài cửa sổ ngày 1-4 nên bỏ qua check tháng 08 (07/2026 đã có sẵn)  rates ✓ 20 ngân hàng (2026-W31, 24hmoney, kỳ hạn 1/3/6/12, 24 tháng để trống; đối chiếu tay 80 cặp với 2026-W30 không có ngân hàng nào đổi >2 điểm%/tuần)  electricity – (QĐ 1279/QĐ-BCT 09/5/2025 vẫn hiện hành; 2 tin liên quan gần đây (NĐ 278/2026/NĐ-CP, VBHN 17/07/2026) chỉ đổi cơ chế điều chỉnh giá, không đổi biểu giá bậc thang)
- flags: (không có flag mới; validate.py: errors=0 flags=0)
- ghi chú: hôm nay thứ Hai nên chạy đủ 5 module. Không self-heal, không domain thiếu. site-builder OK 5/5 module. Nhắc lại (chưa sửa): `check_rates()` trong `scripts/validate.py` vẫn chưa tự động hoá so sánh tuần-qua-tuần cho FLAG "lãi suất đổi >2 điểm%/tuần" (biến `JUMP["rate_pts"]` khai báo nhưng chưa dùng) — đối chiếu tay tuần này không phát hiện bất thường.

## 2026-07-26 (daily)
- gold ✓ 141.500 (SJC 137.500/141.500 qua crawl_gold.py, giavang.org, tăng ~1,48%/~0,71% so hôm qua 135.500/140.500, dưới ngưỡng flag 5%/ngày; DOJI không lấy được hôm nay — update.giavang.doji.vn vẫn không ổn định, để rỗng theo thiết kế, không self-heal)  fx ✓ 26.510 (VCB API: mua tiền mặt 26.100, mua CK 26.130, bán 26.510; SBV central rỗng; không đổi so hôm qua)  fuel – NO_CHANGE kỳ 23/07 (crawl_fuel.py --check → NO_CHANGE, chưa tới hạn kỳ mới, dự kiến ~31/07)  gas – ngoài cửa sổ ngày 1-4 nên bỏ qua check tháng 08  rates skip  electricity skip
- flags: (không có flag mới; validate.py: errors=0 flags=0)
- ghi chú: hôm nay Chủ nhật nên rates & electricity skip theo lịch. Không self-heal script, không domain thiếu. site-builder OK 5/5 module.

## 2026-07-25 (daily)
- gold ✓ 140.500 (SJC 135.500/140.500 qua crawl_gold.py, giavang.org, tăng ~0,37% so hôm qua 135.000/140.000, dưới ngưỡng flag 5%/ngày; DOJI không lấy được hôm nay — update.giavang.doji.vn vẫn không ổn định, để rỗng theo thiết kế, không self-heal)  fx ✓ 26.510 (VCB API: mua tiền mặt 26.100, mua CK 26.130, bán 26.510; SBV central rỗng; tăng 10đ so hôm qua 26.500, ~0,04%)  fuel – NO_CHANGE kỳ 23/07 (crawl_fuel.py --check → NO_CHANGE, chưa tới hạn kỳ mới, dự kiến ~31/07)  gas – ngoài cửa sổ ngày 1-4 nên bỏ qua check tháng 08  rates skip  electricity skip
- flags: (không có flag mới; validate.py: errors=0 flags=0)
- ghi chú: hôm nay thứ Bảy nên rates & electricity skip theo lịch. Không self-heal script, không domain thiếu. site-builder OK 5/5 module.

## 2026-07-24 (daily)
- gold ✓ 140.000 (SJC 135.000/140.000 qua crawl_gold.py, giavang.org, giảm ~4,9%/~4,1% so hôm qua 142.000/146.000, dưới ngưỡng flag 5%/ngày; DOJI không lấy được hôm nay — update.giavang.doji.vn vẫn không ổn định, để rỗng theo thiết kế, không self-heal)  fx ✓ 26.500 (VCB API: mua tiền mặt 26.090, mua CK 26.120, bán 26.500; SBV central rỗng; không đổi so hôm qua)  fuel ✓ kỳ 23/07 (crawl_fuel.py --check báo NEW 2026-07-23 sớm hơn dự kiến 31/07; Petrolimex daily vẫn bảng ảnh nên --append FAIL sanity như dự kiến; lấy tay từ tuoitre.vn bài "Giá xăng dầu đồng loạt tăng từ 15h hôm nay 23-7": E10 RON95-III 21.435, E5RON92-II 20.888, diesel 0,05S-II 25.768, dầu hỏa không có trong bài → để trống; tăng lần lượt +4,3%/+5,4%/+10,5% so kỳ 16/07, dưới ngưỡng flag 20%)  gas – ngoài cửa sổ ngày 1-4 nên bỏ qua check tháng 08  rates skip  electricity skip
- flags: (không có flag mới; validate.py: errors=0 flags=0)
- ghi chú: hôm nay thứ Sáu nên rates & electricity skip theo lịch. Không self-heal script, không domain thiếu. site-builder OK 5/5 module.

## 2026-07-23 (daily)
- gold ✓ 146.000 (SJC 142.000/146.000 qua crawl_gold.py, giavang.org, giảm ~1,0%/~0,3% so hôm qua 143.400/146.400; DOJI không lấy được hôm nay — update.giavang.doji.vn vẫn không ổn định, để rỗng theo thiết kế, không self-heal)  fx ✓ 26.500 (VCB API: mua tiền mặt 26.090, mua CK 26.120, bán 26.500; SBV central rỗng; giảm ~0,04% so hôm qua 26.510)  fuel – kỳ 16/07 không đổi (crawl_fuel.py --check → NO_CHANGE, chưa tới hạn kỳ mới, dự kiến ~31/07)  gas – ngoài cửa sổ ngày 1-4 nên bỏ qua check tháng 08  rates skip  electricity skip
- flags: (không có flag mới; validate.py: errors=0 flags=0)
- ghi chú: hôm nay thứ Năm nên rates & electricity skip theo lịch. Không self-heal, không domain thiếu. site-builder OK 5/5 module.

## 2026-07-22 (daily)
- gold ✓ 146.400 (SJC 143.400/146.400 qua crawl_gold.py, giavang.org, tăng ~0,27% so hôm qua 146.000; DOJI không lấy được hôm nay — update.giavang.doji.vn vẫn không ổn định, để rỗng theo thiết kế, không self-heal)  fx ✓ 26.510 (VCB API: mua tiền mặt 26.100, mua CK 26.130, bán 26.510; SBV central rỗng; tăng ~0,08% so hôm qua 26.490)  fuel – kỳ 16/07 không đổi (crawl_fuel.py --check → NO_CHANGE, chưa tới hạn kỳ mới, dự kiến ~31/07)  gas – ngoài cửa sổ ngày 1-4 nên bỏ qua check tháng 08  rates skip  electricity skip
- flags: (không có flag mới; validate.py: errors=0 flags=0)
- ghi chú: hôm nay thứ Tư nên rates & electricity skip theo lịch. Không self-heal, không domain thiếu. site-builder OK 5/5 module.

## 2026-07-21 (daily)
- gold ✓ 146.000 (SJC 143.000/146.000 qua crawl_gold.py, giavang.org, giảm ~1,0% so hôm qua 147.500; DOJI không lấy được hôm nay — update.giavang.doji.vn vẫn không ổn định, để rỗng theo thiết kế, không self-heal)  fx ✓ 26.490 (VCB API: mua tiền mặt 26.080, mua CK 26.110, bán 26.490; SBV central rỗng; không đổi so hôm qua)  fuel – kỳ 16/07 không đổi (crawl_fuel.py --check → NO_CHANGE, chưa tới hạn kỳ mới)  gas – ngoài cửa sổ ngày 1-4 nên bỏ qua check tháng 08  rates skip  electricity skip
- flags: (không có flag mới; validate.py: errors=0 flags=0)
- ghi chú: hôm nay thứ Ba nên rates & electricity skip theo lịch. Không self-heal, không domain thiếu. site-builder OK 5/5 module.

## 2026-07-20 (daily)
- gold ✓ 147.500 (SJC 144.500/147.500 qua crawl_gold.py, giavang.org, không đổi so hôm qua; DOJI không lấy được hôm nay — update.giavang.doji.vn vẫn chưa có mốc cập nhật khớp ngày, để rỗng theo thiết kế, không self-heal)  fx ✓ 26.490 (VCB API: mua tiền mặt 26.080, mua CK 26.110, bán 26.490; SBV central rỗng; không đổi so hôm qua)  fuel – kỳ 16/07 không đổi (crawl_fuel.py --check → NO_CHANGE, chưa tới hạn kỳ mới)  gas – ngoài cửa sổ ngày 1-4 nên bỏ qua check tháng 08  rates ✓ 20 ngân hàng (2026-W30, 24hmoney, kỳ hạn 1/3/6/12, 24 tháng để trống; đối chiếu tay với 2026-W29 không có ngân hàng nào đổi >2 điểm%/tuần)  electricity – (QĐ 1279/QĐ-BCT 09/5/2025 vẫn hiện hành; NĐ 278/2026/NĐ-CP + VBHN 68/2026/VBHN-BCT chỉ đổi cơ chế điều chỉnh giá bình quân, không đổi biểu giá bậc thang)
- flags: (không có flag mới; validate.py: errors=0 flags=0)
- ghi chú: hôm nay thứ Hai nên chạy đủ 5 module. Không self-heal, không domain thiếu. site-builder OK 5/5 module. Ghi nhận (không sửa): `check_rates()` trong `scripts/validate.py` chưa tự động hoá so sánh tuần-qua-tuần cho quy tắc FLAG "lãi suất đổi >2 điểm%/tuần" — hiện chỉ sanity range; đối chiếu tay tuần này không phát hiện gì bất thường.

## 2026-07-19 (daily)
- gold ✓ 147.500 (SJC 144.500/147.500 qua crawl_gold.py, giavang.org, tăng ~0,6% so hôm qua 146.600; DOJI không lấy được hôm nay — update.giavang.doji.vn chưa có mốc cập nhật khớp ngày, để rỗng theo thiết kế, không self-heal)  fx ✓ 26.490 (VCB API: mua tiền mặt 26.080, mua CK 26.110, bán 26.490; SBV central rỗng; không đổi so hôm qua)  fuel – kỳ 16/07 không đổi (crawl_fuel.py --check → NO_CHANGE, chưa tới hạn kỳ mới)  gas – ngoài cửa sổ ngày 1-4 nên bỏ qua check tháng 08  rates skip  electricity skip
- flags: (không có flag mới; validate.py: errors=0 flags=0; flags.json bị ghi đè rỗng do chạy không `--full` — chỉ quét 2 dòng gần nhất, hành vi thiết kế đã ghi nhận từ 2026-07-08, không phải mất dữ liệu CSV gốc)
- ghi chú: hôm nay Chủ Nhật nên rates & electricity skip theo lịch. Không self-heal, không domain thiếu. site-builder OK 5/5 module.

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
