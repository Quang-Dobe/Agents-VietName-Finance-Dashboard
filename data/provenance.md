# Provenance dữ liệu

Ghi lại dòng nào từ đâu: seed ban đầu, backfill, hay crawl trực tiếp daily.

| Khoảng | Module | Nguồn | Cách lấy | Ghi chú |
|---|---|---|---|---|
| 2026-07-03 | gold | search sjc.com.vn / giavang.doji.vn | seed P0 | SJC & DOJI (vàng miếng, TP.HCM/HN); xác nhận lại ở lần crawl live đầu |
| 2026-07-03 | fx | search vietcombank.com.vn | seed P0 | mới có `vcb_sell`; buy_cash/buy_transfer/sbv_central chờ crawl đầu |
| 2026-07-01 | fuel | search petrolimex.com.vn (kỳ 01/07/2026) | seed P0 | `ron95` E10 RON95-III, e5ron92; diesel/dầu hỏa trống |
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
| fuel | 2025-08 → 2026-07 | `tuoitre.vn` (bài điều hành, URL thu bằng web search) | 8 kỳ + seed. **E5RON92 đầy đủ** (site lấy làm giá chính) + diesel; RON95 thưa (chỉ nhận số chính xác, số tròn tiêu đề bỏ; nhiều bài chỉ nêu "vượt mốc 20.000"). `effective_date` = ngày đăng. Thưa (gaps 09-12/2025, 01-02/2026) do search index; daily dựng tiếp. Trước đó thử vietnambiz — bỏ vì lẫn giá nước ngoài làm parser sai. |
| rates | tuần 2026-W27 | `24hmoney.vn/lai-suat-gui-ngan-hang` (server-rendered) | 20/20 NH, kỳ hạn 1/3/6/12 (24hmoney không có 24 tháng). Tuần hiện tại; chuỗi tuần tích lũy từ đây qua routine thứ Hai. |

> FLAG hợp lệ sau backfill: vàng nhảy >5% ngày 2026-02-03 (+6,3%) và 2026-06-12
> (+5,1%) — biến động thật trong đợt vàng tăng mạnh đầu 2026, giữ nguyên, site hiện ⚠.

## Gap catch-up 2026-08-11 (one-off, không phải daily)

Session daily bị gián đoạn 4 ngày (08-07→08-10, không có run nào — xem
`data/run-log.md` mục 2026-08-11). Chạy `backfill_gold.py`/`backfill_fx.py`
một lần cho đúng khoảng thiếu để lấp đầy CSV.

| Module | Khoảng | Nguồn | Kết quả |
|---|---|---|---|
| gold (SJC) | 2026-08-07 → 2026-08-10 | `webgia.com/gia-vang/sjc/DD-MM-YYYY.html` | ok=3 (07,08,10), skip=1 (09 CN không có bảng chốt, đúng theo quy tắc ngày nghỉ), 0 fail. DOJI trống (webgia không có lịch sử DOJI). |
| fx (VCB) | 2026-08-07 → 2026-08-10 | VCB API `?date=YYYY-MM-DD` | 4/4 ngày, 0 fail. `sbv_central` trống (backfill không lấy SBV). |
| rates | tuần 2026-W33 (lẽ ra thu thứ Hai 08-10, bị lỡ) | `24hmoney.vn/lai-suat-gui-ngan-hang` (live, thu muộn 08-11) | Không phải backfill lịch sử thật — hôm thu (08-11, thứ Ba) vẫn nằm trong cùng tuần ISO 2026-W33 nên là snapshot hợp lệ của tuần đó, chỉ trễ 1 ngày so với lịch thứ Hai. Không tìm được snapshot Wayback nào của 24hmoney gần 08-10 (CDX chỉ có bản 2026-08-05, thuộc tuần W32) nên không cần dùng web.archive. |
| electricity | 08-07 → 08-11 | evn.com.vn | Check catch-up cho thứ Hai bị lỡ — xem kết quả trong `run-log.md`. |

Không backfill rates/electricity cho các ngày TRƯỚC 08-10 (không thuộc lịch
thu thập — chỉ thu thứ Hai hằng tuần) — không có gì để lấp cho những ngày đó.
