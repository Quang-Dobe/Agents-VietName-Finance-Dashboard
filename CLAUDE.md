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

> Trạng thái verify: **đã xác nhận live 2026-07-04** cho vàng (webgia) & tỷ giá
> (VCB API); **cập nhật lại 2026-07-08** cho vàng daily (SJC qua giavang.org, DOJI
> qua giavang.doji.vn) sau khi sjc.com.vn tiếp tục bị chặn. Ghi chú DOM cập nhật
> bên dưới. Lưu ý allowlist environment biến động: lúc verify, `sjc.com.vn` vẫn bị
> chặn; các domain khác (webgia, giavang.org, giavang.doji.vn, vietcombank,
> portal.vcb, petrolimex, evn, vietnambiz, web.archive) đã mở.

### Vàng — `scripts/crawl_gold.py` + `scripts/backfill_gold.py`
- SJC daily (`crawl_gold.get_sjc()`, xác nhận live 2026-07-08), `sjc.com.vn` **bị chặn
  allowlist (403)**, thử theo thứ tự:
  1. **webgia hôm nay** (`webgia.com/gia-vang/sjc/DD-MM-YYYY.html`, dòng cuối = giá
     chốt) — chỉ có dữ liệu sau ~18h VN khi ngày đã "chốt"/archive; trước đó (chạy
     sớm trong ngày) hoặc T7/CN/lễ trả bảng `Khu vực | Loại vàng | Mua vào | Bán ra`
     **rỗng** → rơi xuống bước 2.
  2. **`https://giavang.org/`** (đã whitelist, aggregator giá SJC toàn quốc
     real-time, cùng nguồn mà webgia credit "Nguồn: ... SJC, giavang.org"). DOM:
     khối `<h2>...Giá vàng Miếng SJC</h2>` rồi 2 `<span class="gold-price">146.500
     <small class="gold-unit">x1000đ/lượng</small>` (mua, bán theo thứ tự). Số hiển
     thị **đã là nghìn đồng/lượng**, không cần quy đổi — "146.500" -> 146500.
- SJC lịch sử (backfill, ĐÃ CHẠY): `https://webgia.com/gia-vang/sjc/DD-MM-YYYY.html` — server-rendered.
  DOM: bảng có header `Lần | Thời gian cập nhật | Mua vào | Bán ra`; **lấy DÒNG CUỐI**
  (giá chốt ngày). Số dạng `121.300 (+400)` → chỉ lấy `121.300`. SJC đồng giá toàn quốc.
  Cảnh báo: trang còn 1 widget sidebar "Tỷ giá Vietcombank" cũng có "Mua vào/Bán ra" →
  phải lọc bảng có cột `Lần/Thời gian` mới đúng bảng vàng. Ngày nghỉ (T7/CN/lễ) không có bảng → skip.
- DOJI daily — **self-heal 2026-07-16:** `https://giavang.doji.vn/` giờ **redirect 301
  sang `https://banggia.doji.vn/`**, một Angular SPA (`<app-root>`, bundle JS
  `main-*.js`/`chunk-*.js`, HTML tĩnh chỉ ~3.8KB không có số) → không đọc được bằng
  fetch tĩnh nữa (DOM cũ `#bang-gia-theo-vung-mien` / `table.goldprice-view` mô tả bên
  dưới KHÔNG còn áp dụng cho domain này). WebFetch trên `banggia.doji.vn` cũng gặp 503.
  Không tìm thấy endpoint API JSON nào lộ trong các bundle JS đã kiểm tra.
  **Nguồn thay thế:** subdomain legacy `https://update.giavang.doji.vn/` (Drupal cũ,
  vẫn server-rendered, KHÔNG bị redirect) — bảng đầu trang là "Giá vàng trong nước",
  dòng `<td class="first"><span class="title...">SJC -Bán Lẻ</span>...</td><td
  class="goldprice-td..."><div class="item-relative">14,550</div></td><td...><div
  class="item-relative">14,850</div></td>` (mua, bán). Đơn vị **nghìn đồng/CHỈ** →
  **nhân 10** ra nghìn đồng/lượng. **Cảnh báo quan trọng:** subdomain này có dấu hiệu
  ĐÃ NGỪNG cập nhật real-time — khi crawl lúc 2026-07-16 (~07h VN) trang vẫn hiện mốc
  "Cập nhập lúc: 08:50 15/07/2026" (dữ liệu của NGÀY HÔM TRƯỚC, đơ ít nhất >22h). Vì
  vậy `parse_doji` bắt buộc parse mốc "Cập nhập lúc: HH:MM DD/MM/YYYY" và so với ngày
  hôm nay — không khớp thì raise (bỏ trống DOJI) thay vì lặp giá cũ. Bảng cũng không
  còn ghi rõ "Hà Nội" trong tiêu đề (chỉ "Giá vàng trong nước", có thể là bảng chung/
  toàn quốc chứ không riêng Hà Nội — cần xác nhận lại nếu/khi trang cập nhật lại).
  webgia DOJI (`https://webgia.com/gia-vang/doji/`) cũng đã thử: trả 200 nhưng bảng
  `<tbody></tbody>` RỖNG (giá được JS widget `doji.js` chèn vào, không có trong HTML
  thô) → không dùng được. Nếu subdomain `update.giavang.doji.vn` ngừng hẳn, cần tìm
  nguồn DOJI khác (chưa có phương án).
  **2026-07-17: subdomain còn hỏng nặng hơn** — `fetch()` giờ raise `FetchError`
  (`SSL: CERTIFICATE_VERIFY_FAILED ... unable to get local issuer certificate`)
  TRƯỚC CẢ KHI đọc được HTML để check mốc "Cập nhập lúc". Đã xác minh bằng tay đây
  KHÔNG PHẢI lỗi allowlist/proxy: CONNECT tunnel tới `update.giavang.doji.vn:443`
  trả `200 Connection Established` bình thường (giống domain khác trong allowlist,
  ví dụ `giavang.org`, `banggia.doji.vn` verify TLS OK qua cùng proxy), và
  `openssl s_client -proxy ... -connect update.giavang.doji.vn:443 -showcerts` cho
  thấy origin server có cert lá hợp lệ (CN đúng, GlobalSign, hết hạn 2026-12-02)
  nhưng **không gửi kèm chứng chỉ trung gian** "GlobalSign GCC R6 AlphaSSL CA 2025"
  → client không dựng được chain, lỗi `unable to get local issuer certificate`. Đây
  là lỗi cấu hình TLS phía server nguồn (thiếu chain cert), không sửa được từ phía
  agent (không được tắt xác minh TLS). `parse_doji`/`get sjc` không cần sửa — luồng
  try/except hiện tại ở `main()` đã đúng: DOJI fail (bất kỳ lý do gì, kể cả
  `FetchError`) → để trống, không chặn phần SJC. Ghi nhận thêm bằng chứng subdomain
  này đang bị bỏ bê (2 ngày liên tiếp 07-16, 07-17 đều không lấy được DOJI, hai lý
  do khác nhau) — nên coi là nguồn không ổn định, ưu tiên tìm nguồn DOJI thay thế
  khi có thời gian rà soát kỹ hơn (chưa có phương án).
- DOJI lịch sử: webgia **404** (`/gia-vang/doji/DD-MM-YYYY.html` không tồn tại) → backfill để DOJI rỗng.

### Tỷ giá — `scripts/crawl_fx.py` + `scripts/backfill_fx.py`
- **VCB API JSON (TỐT NHẤT, có tham số ngày — dùng cho cả daily lẫn backfill):**
  `https://www.vietcombank.com.vn/api/exchangerates?date=YYYY-MM-DD`
  → `{"Date","Data":[{"currencyCode":"USD","cash","transfer","sell"}...]}`. Trả rate mọi
  ngày (cả cuối tuần). Đây là nguồn chính hiện tại.
- VCB XML (dự phòng): `https://portal.vietcombank.com.vn/Usercontrols/TVPortal.TyGia/pXML.aspx`
  — **chỉ tỷ giá hiện tại, BỎ QUA tham số date, giới hạn 1 request/5 phút**. Không dùng cho backfill.
- webgia FX: bảng lịch sử **JS-load, không có số trong HTML thô** → không parse bằng fetch, đừng dùng.
- SBV trung tâm: `https://dttktt.sbv.gov.vn/TyGia/faces/TyGiaTrungTam.jspx` — chập chờn, cho phép null.

### Xăng dầu — `scripts/crawl_fuel.py` + `scripts/backfill_fuel.py`
- **Backfill (xác nhận live 2026-07-04): `tuoitre.vn`** — bài điều hành giá, giá TEXT sạch,
  KHÔNG lẫn giá nước ngoài. `backfill_fuel.py` nhận danh sách URL bài (thu bằng web search vì
  tuoitre dùng timeline JS, không walk được). Bẫy: (1) tiêu đề nêu số TRÒN ("vượt mốc 20.000")
  → ưu tiên giá không tròn nghìn; RON95 chỉ nhận số chính xác, không thì để trống. (2) `effective_date`
  = NGÀY ĐĂNG (meta `article:published_time`) vì ngày trong thân bài hay dính kỳ trước. (3) lọc 14.000–26.000.
  **E5RON92 là chuỗi đầy đủ nhất** → site + summary lấy E5 làm giá chính (RON95/diesel thưa).
- Daily `crawl_fuel.py` hiện dùng Petrolimex (bảng giá là **ẢNH** → parse_prices không đọc được).
  **TODO daily:** chuyển sang tuoitre như backfill. webgia fuel = JS-load, bỏ.
- **Lưu ý:** từ 06/2026 xăng khoáng RON95 được thay bằng E10 RON95 (sinh học); cột `ron95` chứa giá loại RON95 hiện hành.
- vietnambiz fuel: **KHÔNG dùng** — lẫn giá tham chiếu nước ngoài (Thái/Lào/TQ) làm parser lấy sai; RON95 hay vắng.
- **Fallback thủ công khi tuoitre chưa đăng bài kỳ mới (đã dùng 2026-07-09):** nếu
  `crawl_fuel.py --check` báo `NEW` nhưng tuoitre chưa có bài (kiểm `tuoitre.vn/gia-xang-dau.html`,
  danh sách bài gắn tag, không phải trang search — search dùng JS không fetch được), agent có thể
  fetch trực tiếp ảnh `giabanle.jpg` từ bài thông cáo Petrolimex (`<img src=".../giabanle.jpg">`
  trong HTML bài) rồi **đọc bằng Read tool (vision)** — bảng ảnh có cột "Vùng 1"/"Vùng 2", đơn vị
  đồng/lít đã gồm VAT. Đây là parse tay một lần, KHÔNG tự động hoá được trong script (regex không
  đọc ảnh) nên không sửa `parse_prices`. Chọn đúng dòng:
  - `ron95` = "Xăng sinh học E10 RON 95-**III**" (loại phổ thông, khớp lịch sử trước 06/2026),
    KHÔNG lấy dòng "-V" (loại cao cấp, giá luôn cao hơn ~1.000-1.200đ, ít trạm bán).
  - `diesel` = "Điêzen 0,05S-**II**" (phổ thông, khớp range lịch sử ~21.000-22.000), KHÔNG lấy
    "0,001S-V" (cao cấp, ~23.000-24.000).
  - `dau_hoa` = "Dầu hỏa 2-K".
  - Vùng 1 = cột đầu tiên sau "Đơn vị tính".

### Lãi suất — `scripts/crawl_rates.py`
- **`https://24hmoney.vn/lai-suat-gui-ngan-hang` (CHÍNH, xác nhận live 2026-07-04):**
  bảng server-rendered `Ngân hàng | 01 | 03 | 06 | 09 | 12 tháng`, số text, ~38 NH →
  lọc 20 mã. **Không có cột 24 tháng** → term 24 để trống.
- webgia.com/lai-suat: **JS-load số** (tên NH có trong HTML nhưng lãi suất do JS chèn)
  → KHÔNG parse được bằng fetch, đừng dùng. Dự phòng: `laisuattietkiem.vn`.

### Điện & Gas
- EVN biểu giá: bài "Biểu giá bán lẻ điện" trên `evn.com.vn` (hiện hành QĐ 1279/QĐ-BCT, hiệu lực 10/05/2025). Dự phòng `evnhanoi.vn/cskh/gia-ban-dien`.
- Gas (backfill xác nhận live 2026-07-04): **`thoibaotaichinhvietnam.vn`** — bài THEO THÁNG
  "Giá gas bán lẻ ... tháng M/YYYY", server-rendered, giá text. Cột `mien_bac` (Petrolimex
  Hà Nội, gồm VAT) đầy đủ nhất; `mien_trung`/`mien_nam` thưa (nhiều bài chỉ chi tiết HN).
  CP lấy số "ở mức <X> USD/tấn" (300–900), tránh delta. Parser: `scripts/backfill_gas.py`.
  **Bẫy đã gặp:** trang có widget thời tiết "Hà Nội 31°C..." ở đầu → phải duyệt MỌI vị trí
  khớp tên thành phố, chọn chỗ có giá. Nguồn thay thế theo NGÀY: `vietnambiz.vn` bài
  "Giá gas hôm nay 1/<tháng>" (listing phân trang `/gia-gas/trang-N.html`; lẫn bài giá thế
  giới USD/mmBTU — lọc bỏ; chỉ có domestic gần đây). Dự phòng thêm `tuoitre.vn`.

### Backfill (chỉ dùng trong one-off runs, xem `BACKFILL_PROMPTS/`)
- `webgia.com/gia-vang/sjc/DD-MM-YYYY.html`, `webgia.com/ty-gia/vietcombank/DD-MM-YYYY.html`,
  `webgia.com/gia-xang-dau/petrolimex/`, `web.archive.org` (lãi suất).

## Allowlist environment hiện tại (cập nhật cùng lúc với environment settings)

Bắt buộc (daily): `sjc.com.vn` (hiện bị chặn — vàng daily dùng `giavang.org` thay thế),
`giavang.org`, `giavang.doji.vn`, `update.giavang.doji.vn`,
`vietcombank.com.vn`, `portal.vietcombank.com.vn`, `sbv.gov.vn`,
`dttktt.sbv.gov.vn`, `petrolimex.com.vn`, `evn.com.vn`, `evnhanoi.vn`,
`webgia.com`, `vietnambiz.vn`, `24hmoney.vn` (lãi suất),
`thoibaotaichinhvietnam.vn` (gas).

Backfill/dự phòng: `web.archive.org`,
`laisuattietkiem.vn`, `tuoitre.vn`, `alogas.vn`,
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
