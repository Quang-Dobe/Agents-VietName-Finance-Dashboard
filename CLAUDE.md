# vn-finance-dashboard — hướng dẫn cho agent

Dashboard giá cả Việt Nam (vàng, USD, xăng dầu, lãi suất, điện & gas), cập nhật
daily ~18:05 VN bằng Claude Code Routine. Site tĩnh trên GitHub Pages, render
phía client từ `data/*.csv` + `site/summary.json`. Không dùng Claude API.

## Nguyên tắc (đọc trước khi làm bất cứ gì)

1. **Script-first.** Việc lặp hằng ngày là chạy `scripts/`. Chỉ dùng reasoning
   khi script in `FAIL`. Đừng tự parse lại khi script đã in `OK`.
2. **Self-heal.** Script gãy vì trang đổi cấu trúc → tự fetch trang, parse tay để
   có dữ liệu hôm nay, rồi **SỬA hàm `parse_*` trong script + cập nhật ghi chú
   cấu trúc trang ở mục "Nguồn" dưới đây**, commit chung. Hệ thống tự vá dần.
3. **403/blocked = thiếu domain, KHÔNG phải lỗi parse.** Script in `FAIL blocked:`
   khi bị proxy chặn. Đừng sửa script — báo domain cần thêm vào allowlist. Danh
   sách allowlist hiện tại ở cuối file; thêm nguồn mới = thêm ở đó **và** trong
   environment settings cùng lúc.
4. **Dữ liệu thật > dữ liệu đẹp.** Không bịa, không copy giá hôm trước, không sửa
   dòng lịch sử bằng tay. Trường lấy không được → để rỗng (CSV) / null (JSON).
5. **1 commit / run.** Không force-push. Không đổi schema khi chưa được yêu cầu.
   Không chạy backfill trong run daily.

## Quy trình daily (chi tiết trong ROUTINE_PROMPT.md)

Orchestrator đọc run-log → spawn song song các agent crawl (deposit-rates &
electricity-check chỉ thứ Hai) → validator → site-builder → ghi run-log → commit
1 lần, push `main`. 1 module fail không chặn module khác.

## Schema dữ liệu

Ngày ISO `YYYY-MM-DD`. Số dùng dấu chấm thập phân, KHÔNG phân tách nghìn (định
dạng VN là việc của frontend). CSV append-only, sort tăng theo ngày, 1 dòng/ngày.

| File | Cột | Đơn vị |
|---|---|---|
| `data/gold/history.csv` | `date, sjc_buy, sjc_sell, doji_buy, doji_sell` | nghìn đ/lượng · SJC tại TP.HCM, DOJI tại HN, vàng miếng |
| `data/fx/history.csv` | `date, vcb_buy_cash, vcb_buy_transfer, vcb_sell, sbv_central` | VND/USD · sbv_central cho phép rỗng |
| `data/fuel/history.csv` | `effective_date, ron95, e5ron92, diesel, dau_hoa` | đồng/lít · vùng 1 Petrolimex · 1 dòng/kỳ điều hành |
| `data/utilities/gas.csv` | `effective_month, mien_bac, mien_trung, mien_nam, cp_usd_ton` | đ/bình 12kg · cp_usd_ton cho phép rỗng |
| `data/utilities/electricity.json` | `changes[]: {effective_date, decision, unit, tiers[]}` | đ/kWh chưa VAT · 1 phần tử/lần đổi biểu giá |
| `data/deposit-rates/YYYY-Www.json` | `{week, collected_at, source_url, rates[]}` · `rates[]: {bank, term_months, rate, source_url}` | %/năm · gửi tại quầy, lãi cuối kỳ |

Kỳ hạn lãi suất theo dõi: **1, 3, 6, 12, 24 tháng**.

**20 mã ngân hàng** (dùng đúng mã này ở trường `bank`):
`VCB, BIDV, VietinBank, Agribank` (Big4) ·
`Techcombank, VPBank, MB, ACB, Sacombank, SHB, HDBank, VIB, TPBank, MSB, OCB, Eximbank, SeABank, LPBank, NamABank, BacABank`.
Ngân hàng thiếu trong nguồn tuần đó → bỏ qua, không fail cả module.

## Quy tắc validate (`scripts/validate.py`)

- **ERROR** (loại/sửa): gold 30.000–500.000 & sell>buy · fx 15.000–50.000 &
  buy_transfer≤sell · rate 0,1–15 · fuel 5.000–60.000 · gas 200.000–1.200.000.
- **FLAG** (giữ, site hiện ⚠): SJC lệch DOJI >3% · vàng nhảy >5%/ngày · tỷ giá
  nhảy >2%/ngày · VCB lệch SBV >5% · xăng nhảy >20% · gas nhảy >30% · lãi suất
  1 ngân hàng đổi >2 điểm %/tuần.

## Nguồn (cập nhật ghi chú cấu trúc trang khi self-heal)

> Trạng thái verify: URL lấy từ web search 2026-07-03; **cấu trúc DOM chưa xác nhận
> live** (môi trường verify chặn fetch khi soạn plan). Lần chạy live đầu tiên:
> xác nhận DOM, sửa `parse_*` nếu cần, ghi chú lại tại đây.

### Vàng — `scripts/crawl_gold.py`
- SJC: `https://sjc.com.vn/gia-vang-online` — bảng mua/bán theo khu vực; lấy TP.HCM, vàng miếng SJC. (DOM: _chưa xác nhận_)
- DOJI: `https://giavang.doji.vn/` — bảng theo khu vực HN/ĐN/HCM; endpoint dữ liệu khả nghi `update.giavang.doji.vn` (thử nếu HTML khó parse). (DOM: _chưa xác nhận_)

### Tỷ giá — `scripts/crawl_fx.py`
- VCB XML (thử trước): `https://portal.vietcombank.com.vn/Usercontrols/TVPortal.TyGia/pXML.aspx` — chỉ tỷ giá hiện tại, `<Exrate CurrencyCode="USD" Buy Transfer Sell>`.
- VCB HTML (fallback + tra cứu theo ngày): `https://www.vietcombank.com.vn/vi-VN/KHCN/Cong-cu-Tien-ich/Ty-gia` — có date-picker; tìm API JSON theo ngày ở lần chạy đầu (nếu có thì dùng cho cả backfill).
- SBV trung tâm: `https://dttktt.sbv.gov.vn/TyGia/faces/TyGiaTrungTam.jspx` — chập chờn, cho phép null.

### Xăng dầu — `scripts/crawl_fuel.py`
- Petrolimex thông cáo: `https://www.petrolimex.com.vn/ndi/thong-cao-bao-chi.html` — mỗi kỳ 1 bài, URL: `.../petrolimex-dieu-chinh-gia-xang-dau-tu-...-ngay-DD.M.YYYY.html`. Giá vùng 1 = cột đầu.
- **Lưu ý:** từ 06/2026 xăng khoáng RON95 được thay bằng E10 RON95 (sinh học); cột `ron95` chứa giá loại RON95 hiện hành, ghi provenance khi có chuyển đổi.

### Lãi suất — `scripts/crawl_rates.py`
- Tổng hợp: `https://webgia.com/lai-suat/` — bảng ~40 ngân hàng × kỳ hạn; lọc 20 mã trên. Dự phòng đối chiếu: `24hmoney.vn/lai-suat-gui-ngan-hang`, `laisuattietkiem.vn`.

### Điện & Gas
- EVN biểu giá: bài "Biểu giá bán lẻ điện" trên `evn.com.vn` (hiện hành QĐ 1279/QĐ-BCT, hiệu lực 10/05/2025). Dự phòng `evnhanoi.vn/cskh/gia-ban-dien`.
- Gas: `vietnambiz.vn` bài "Giá gas hôm nay 1/<tháng>" đầu mỗi tháng — bình 12kg 3 miền + giá CP. Dự phòng `tuoitre.vn`, `thoibaotaichinhvietnam.vn`.

### Backfill (chỉ dùng trong one-off runs, xem `BACKFILL_PROMPTS/`)
- `webgia.com/gia-vang/sjc/DD-MM-YYYY.html`, `webgia.com/ty-gia/vietcombank/DD-MM-YYYY.html`,
  `webgia.com/gia-xang-dau/petrolimex/`, `web.archive.org` (lãi suất).

## Allowlist environment hiện tại (cập nhật cùng lúc với environment settings)

Bắt buộc (daily): `sjc.com.vn`, `giavang.doji.vn`, `update.giavang.doji.vn`,
`vietcombank.com.vn`, `portal.vietcombank.com.vn`, `sbv.gov.vn`,
`dttktt.sbv.gov.vn`, `petrolimex.com.vn`, `evn.com.vn`, `evnhanoi.vn`,
`webgia.com`, `vietnambiz.vn`.

Backfill/dự phòng: `web.archive.org`, `giavang.org`, `24hmoney.vn`,
`laisuattietkiem.vn`, `tuoitre.vn`, `thoibaotaichinhvietnam.vn`, `alogas.vn`,
`pnj.com.vn`. P3 (thêm khi làm): `stooq.com`.

## Định dạng run-log (`data/run-log.md`, giữ ≤30 mục)

```
## YYYY-MM-DD (daily)
- gold ✓  fx ✓  fuel –  rates skip  electricity skip
- flags: <mô tả hoặc "(không)">
- lỗi: <mô tả hoặc bỏ dòng này>
```
✓ = có dữ liệu mới · – = check xong không có gì mới · ✗ = fail · skip = không đến lịch.

## Commit message chuẩn (daily)

`daily: YYYY-MM-DD (gold ✓ fx ✓ fuel – rates skip electricity skip)`

## Chạy site local

Site fetch `data/...` theo đường dẫn tương đối so với trang (khớp với layout
Pages, nơi workflow copy `data/` nằm cạnh `index.html`). Để preview local, tạo
symlink 1 lần rồi phục vụ từ trong `site/`:

```
ln -s ../data site/data          # đã gitignore, chỉ dùng local
cd site && python3 -m http.server # mở http://localhost:8000
```

Workflow Pages KHÔNG dùng symlink này — nó copy `data/` thật vào artifact.
