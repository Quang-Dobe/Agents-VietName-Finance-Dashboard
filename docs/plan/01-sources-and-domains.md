# 01 — Nguồn dữ liệu đã verify + allowed domains

> Verify bằng web search ngày **03/07/2026**. Môi trường cloud chặn mọi request tới domain ngoài allowlist (đã xác nhận trong session này — kể cả `example.com` cũng bị policy-denied), nên **bước đầu tiên của P0 là fetch thử từng URL dưới đây từ trong environment** để chốt allowlist.
>
> Ký hiệu: ✅ = đã thấy URL hoạt động qua search · 🔍 = ứng viên, cần verify trong environment

## Phát hiện quan trọng: webgia.com

`webgia.com` là nguồn backfill **một cửa cho 4/5 module** — có URL lịch sử theo ngày, cấu trúc ổn định:

| Module | URL pattern | Độ sâu lịch sử |
|---|---|---|
| Vàng SJC | `webgia.com/gia-vang/sjc/DD-MM-YYYY.html` ✅ | về tận 1996 |
| Vàng DOJI | `webgia.com/gia-vang/doji/` ✅ (verify pattern ngày) | 🔍 |
| Tỷ giá VCB | `webgia.com/ty-gia/vietcombank/DD-MM-YYYY.html` ✅ | nhiều năm |
| Xăng dầu Petrolimex | `webgia.com/gia-xang-dau/petrolimex/` ✅ (bảng lịch sử các kỳ) | nhiều năm |
| Lãi suất | `webgia.com/lai-suat/` ✅ (bảng hiện tại; lịch sử qua Wayback) | hiện tại |

→ Backfill ưu tiên crawl webgia (1 domain, cấu trúc đồng nhất, ~1.460 trang cho 2 năm × 2 module ngày). Nguồn chính thức (SJC, VCB…) dùng cho **daily** để số liệu là số "gốc".

## 1. Vàng

| Nguồn | URL | Ghi chú |
|---|---|---|
| SJC (chính thức) ✅ | `https://sjc.com.vn/gia-vang-online` | Bảng mua/bán theo khu vực; có trang biểu đồ `sjc.com.vn/bieu-do-gia-vang`. 🔍 kiểm tra endpoint XML/JSON cũ của SJC còn sống không |
| DOJI (chính thức) ✅ | `https://giavang.doji.vn/` | Bảng theo khu vực (HN/ĐN/HCM). 🔍 endpoint dữ liệu `update.giavang.doji.vn` xuất hiện trong search — có thể là feed JSON |
| PNJ 🔍 | `https://www.pnj.com.vn/site/gia-vang` | Dự phòng, chưa dùng v1 |
| Backfill ✅ | `webgia.com/gia-vang/sjc/…`, `giavang.org/trong-nuoc/sjc/` | webgia là chính; giavang.org dự phòng |
| Vàng thế giới (P3) 🔍 | `https://stooq.com/q/d/l/?s=xauusd&i=d` | CSV miễn phí không cần key — verify khi làm P3 |

**Lưu ý dữ liệu 2025-2026:** giá SJC đã ở vùng ~140-150 triệu đ/lượng. Sanity bound trong validator phải đặt theo vùng này, không hardcode vùng giá cũ.

## 2. Tỷ giá

| Nguồn | URL | Ghi chú |
|---|---|---|
| VCB tra cứu theo ngày (chính thức) ✅ | `https://www.vietcombank.com.vn/vi-VN/KHCN/Cong-cu-Tien-ich/Ty-gia` | Có date-picker → 🔍 tìm API JSON đứng sau (ứng viên: `vietcombank.com.vn/api/exchangerates?date=YYYY-MM-DD`) — nếu sống thì backfill FX **không cần** webgia |
| VCB XML cũ 🔍 | `portal.vietcombank.com.vn/Usercontrols/TVPortal.TyGia/pXML.aspx` | Endpoint lâu đời, chỉ tỷ giá hiện tại |
| SBV tỷ giá trung tâm ✅ | `https://dttktt.sbv.gov.vn/TyGia/faces/TyGiaTrungTam.jspx` | Trang JSF, chập chờn (khi verify có lỗi truy cập) → `sbv_central` cho phép null, fallback webgia/báo |
| Backfill ✅ | `webgia.com/ty-gia/vietcombank/DD-MM-YYYY.html` | Đã thấy hoạt động với nhiều ngày 2025-2026 |

## 3. Xăng dầu

| Nguồn | URL | Ghi chú |
|---|---|---|
| Petrolimex thông cáo báo chí ✅ | `https://www.petrolimex.com.vn/ndi/thong-cao-bao-chi.html` | Mỗi kỳ điều hành 1 bài, URL đoán được: `…/petrolimex-dieu-chinh-gia-xang-dau-tu-15-gio-00-phut-ngay-DD.M.YYYY.html`. Daily check: đọc trang danh sách, so ngày mới nhất |
| Bảng giá hiện hành 🔍 | `gia.petrolimex.com.vn` | Subdomain bảng giá bán lẻ — verify trong environment |
| Backfill ✅ | `webgia.com/gia-xang-dau/petrolimex/` | Bảng lịch sử đầy đủ các kỳ (RON95, E5 RON92, DO, dầu hỏa) — đủ ~73 kỳ/2 năm trong ít trang |
| Dự phòng 🔍 | `pvoil.com.vn`, `moit.gov.vn` | Không dùng v1 |

## 4. Lãi suất tiết kiệm

| Nguồn | URL | Ghi chú |
|---|---|---|
| Tổng hợp (chính cho daily) ✅ | `https://webgia.com/lai-suat/` | Bảng ~40 ngân hàng × kỳ hạn, cập nhật thường xuyên |
| Tổng hợp dự phòng ✅ | `https://24hmoney.vn/lai-suat-gui-ngan-hang`, `https://laisuattietkiem.vn/` | Đối chiếu chéo khi số liệu bất thường |
| Backfill ✅ | `web.archive.org` snapshot của `webgia.com/lai-suat/` | Chấp nhận partial (xem [04](04-backfill.md)) |

Chiến lược: **crawl 1 trang tổng hợp** thay vì 20 trang ngân hàng (20 domain + 20 cấu trúc khác nhau = quá đắt để maintain). Trang ngân hàng gốc chỉ dùng khi validator flag số liệu bất thường.

## 5. Điện & Gas

| Nguồn | URL | Ghi chú |
|---|---|---|
| EVN biểu giá ✅ | `https://evn.com.vn` — bài "Biểu giá bán lẻ điện" (hiện hành: QĐ 1279/QĐ-BCT, hiệu lực 10/05/2025, 6 bậc: 1.984 / 2.050 / 2.380 / 2.998 / 3.350 / 3.460 đ/kWh chưa VAT) | Daily check thứ Hai: so số bậc + giá bậc 1 với `electricity.json` |
| EVN Hà Nội (dự phòng) ✅ | `https://evnhanoi.vn/cskh/gia-ban-dien` | Cấu trúc đơn giản hơn |
| Gas hằng tháng ✅ | `vietnambiz.vn` — bài "Giá gas hôm nay 1/M" mỗi đầu tháng, có giá bình 12kg theo miền + hãng + giá CP (USD/tấn) | Nguồn nhất quán nhất cho cả daily check lẫn backfill 24 mốc |
| Gas dự phòng ✅ | `tuoitre.vn`, `thoibaotaichinhvietnam.vn`, `alogas.vn` | |

## Allowed domains cho cloud environment

**Nhóm bắt buộc (daily):**

```
sjc.com.vn            www.sjc.com.vn
giavang.doji.vn       update.giavang.doji.vn
vietcombank.com.vn    www.vietcombank.com.vn    portal.vietcombank.com.vn
sbv.gov.vn            dttktt.sbv.gov.vn
petrolimex.com.vn     www.petrolimex.com.vn     gia.petrolimex.com.vn
evn.com.vn            www.evn.com.vn            evnhanoi.vn
webgia.com
vietnambiz.vn
```

**Nhóm backfill / dự phòng:**

```
web.archive.org
giavang.org
24hmoney.vn
laisuattietkiem.vn
tuoitre.vn
thoibaotaichinhvietnam.vn
alogas.vn
pnj.com.vn            www.pnj.com.vn
```

**Nhóm P3 (thêm khi làm):** `stooq.com`

Quy tắc vận hành: **mỗi lần thêm nguồn mới = thêm domain vào environment + ghi vào mục "Nguồn" của CLAUDE.md trong cùng 1 commit.** Lỗi fetch bị chặn sẽ hiện là 403/policy-denied — gặp lỗi này, việc đầu tiên là kiểm tra allowlist, không phải sửa script.
