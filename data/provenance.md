# Provenance dữ liệu

Ghi lại dòng nào từ đâu: seed ban đầu, backfill, hay crawl trực tiếp daily.

| Khoảng | Module | Nguồn | Cách lấy | Ghi chú |
|---|---|---|---|---|
| 2026-07-03 | gold | search sjc.com.vn / giavang.doji.vn | seed P0 | SJC & DOJI (vàng miếng, TP.HCM/HN); xác nhận lại ở lần crawl live đầu |
| 2026-07-03 | fx | search vietcombank.com.vn | seed P0 | mới có `vcb_sell`; buy_cash/buy_transfer/sbv_central chờ crawl đầu |
| 2026-07-01 | fuel | search petrolimex.com.vn (kỳ 01/07/2026) | seed P0 | `ron95` = E10 RON95-III (xăng khoáng đã bỏ từ 06/2026), e5ron92 xác nhận; diesel & dầu hỏa để trống (số search nghi ngờ) → chờ crawl live |
| 2026-07 | gas | search vietnambiz.vn (kỳ 01/07/2026) | seed P0 | giá bình 12kg 3 miền + CP 590 USD/tấn |
| 2025-05-10 | electricity | search evn.com.vn (QĐ 1279/QĐ-BCT) | seed P0 | biểu giá 6 bậc hiện hành |

> Seed P0 = giá trị thật thu từ web search ngày 2026-07-03, dùng để dashboard có
> "1 ngày dữ liệu" khi khởi tạo. Sẽ được bổ sung/đối chiếu bởi backfill (P1) và
> crawl daily (P2). Backfill ghi 1 dòng/run; daily gộp 1 dòng/tháng.

## Backfill 1 năm (2026-07-04, one-off)

| Module | Khoảng | Nguồn | Kết quả |
|---|---|---|---|
| gold (SJC) | 2025-07-04 → 2026-07-03 | `webgia.com/gia-vang/sjc/DD-MM-YYYY.html` (server-rendered, giá chốt ngày) | 265 ngày giao dịch, skip 101 ngày nghỉ, 0 fail. DOJI để trống (webgia không có lịch sử DOJI). Giá trị 2026-07-03 khớp seed. |
| fx (VCB) | 2025-07-03 → 2026-07-04 | VCB API `?date=YYYY-MM-DD` (cash/transfer/sell) | 364 ngày, 0 skip, 0 fail. `sbv_central` trống cho giai đoạn backfill. |
| gas | 2025-07 → 2026-07 | `thoibaotaichinhvietnam.vn` (bài theo tháng, giá text) | 10 tháng, cột `mien_bac` (HN, Petrolimex gồm VAT) đầy đủ nhất + CP; `mien_trung`/`mien_nam` thưa. Thiếu 2026-01/02/05 (bài không nêu giá tuyệt đối / không tìm được URL). 2026-07 khớp seed (502.200). |
| fuel | — | (chặn) petrolimex bảng giá là ẢNH; webgia fuel JS-load | Chưa backfill được từ môi trường này — xem CLAUDE.md. |
| rates | — | Wayback webgia/lai-suat | Chưa làm; follow-up. |

> FLAG hợp lệ sau backfill: vàng nhảy >5% ngày 2026-02-03 (+6,3%) và 2026-06-12
> (+5,1%) — biến động thật trong đợt vàng tăng mạnh đầu 2026, giữ nguyên, site hiện ⚠.
