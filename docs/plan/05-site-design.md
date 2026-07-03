# 05 — Thiết kế site: dark theme, logo, wording

## Định vị

Tên site: **「Giá Việt」** — ngắn, dễ nhớ, nói đúng nội dung.
Tagline (dưới logo, 1 dòng): *Vàng · USD · Xăng · Lãi suất · Điện & Gas — cập nhật 18h mỗi ngày.*
Title tab trình duyệt: `Giá Việt — Vàng, USD, Xăng, Lãi suất` (trang con: `Vàng — Giá Việt`…).

## Design tokens (dark theme duy nhất)

Palette 5 series đã chạy qua validator dataviz trên nền `#111A2E`: **PASS cả 4 check** (band, chroma, CVD ΔE tệ nhất 27.6 ≥ 12, contrast ≥ 3:1). Không đổi màu tùy hứng — đổi thì phải validate lại.

```css
:root {
  /* nền */
  --page:        #0B1220;   /* nền trang */
  --surface:     #111A2E;   /* card, nền biểu đồ */
  --border:      rgba(255,255,255,.10);
  --grid:        #23304C;   /* gridline hairline */

  /* chữ — luôn dùng token chữ, không tô chữ bằng màu series */
  --ink:         #FFFFFF;
  --ink-2:       #A7B4CE;   /* phụ */
  --ink-3:       #6B7A99;   /* nhãn trục, muted */

  /* series — mỗi module 1 màu CỐ ĐỊNH, không xoay vòng */
  --c-gold:      #C98500;
  --c-fx:        #3987E5;
  --c-fuel:      #D95926;
  --c-rates:     #199E70;
  --c-utilities: #9085E9;

  /* trạng thái tăng/giảm (kèm mũi tên ▲▼, không chỉ dựa màu) */
  --up:          #0CA30C;
  --down:        #D03B3B;

  font-family: system-ui, -apple-system, "Segoe UI", Roboto, sans-serif;
}
```

Quy tắc chart (theo skill dataviz — ghi vào CLAUDE.md để agent giữ đúng khi sửa site):

- **1 trục y duy nhất**, không bao giờ dual-axis. Trang Tương quan: các chuỗi **index về 100** tại đầu khung thời gian thay vì 2 trục.
- Line 2px, marker hover ≥ 8px, grid hairline màu `--grid`, không viền chart.
- ≥ 2 series → có legend; số trên chart chỉ label chọn lọc (điểm cuối), không label mọi điểm.
- Số trong bảng/trục dùng `font-variant-numeric: tabular-nums`.
- Mỗi biểu đồ có nút "Bảng" (table view) — vừa accessibility vừa tiện copy số.

## Logo + favicon

Concept: **đồng xu vàng + đường giá đi lên** — 1 file SVG dùng cho cả logo header lẫn favicon (favicon SVG hiện được mọi trình duyệt lớn hỗ trợ; thêm PNG 180px cho `apple-touch-icon` ở P0).

`site/assets/logo.svg` (draft — tinh chỉnh khi implement):

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">
  <rect width="64" height="64" rx="14" fill="#0B1220"/>
  <circle cx="32" cy="32" r="22" fill="none" stroke="#C98500" stroke-width="3"/>
  <polyline points="18,40 27,33 34,37 46,24" fill="none"
            stroke="#C98500" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>
  <circle cx="46" cy="24" r="3.5" fill="#F5C451"/>
</svg>
```

Khai báo trong `<head>` mọi trang:

```html
<link rel="icon" type="image/svg+xml" href="assets/logo.svg">
<link rel="apple-touch-icon" href="assets/logo-180.png">
```

Header: logo 28px + chữ "Giá Việt" (`--ink`, 600) + tagline (`--ink-2`) — không thêm hiệu ứng.

## Wording — quy tắc viết chữ trên site

1. **Ngắn nhất có thể.** Nhãn ≤ 3 từ: "Vàng SJC", "USD / VND", "Xăng RON95", "Lãi suất 12T", "Điện & Gas".
2. **Không thuật ngữ khó.** "Bán ra" thay vì "niêm yết chiều bán"; "so hôm qua" thay vì "biến động theo phiên liền trước".
3. Delta luôn kèm mũi tên + dấu: `▲ +0,4% so hôm qua` / `▼ −1,2% so tuần trước`.
4. Số theo định dạng VN: `151.400.000 ₫/lượng`, `26.480 ₫/USD`, `4,7%/năm`.
5. Mỗi trang chi tiết có 1 dòng giải thích đơn vị ở đầu, ví dụ: *"Giá vàng miếng, triệu đồng mỗi lượng. SJC lấy tại TP.HCM, DOJI tại Hà Nội."*
6. Thời điểm cập nhật ghi kiểu thân thiện: `Cập nhật: 18:07 · 04/07/2026`.

## Các trang

### `index.html` — Dashboard

- **Header**: logo + tên + tagline; phải có link `Cách hoạt động` (docs.html).
- **Hàng cảnh báo** (chỉ hiện khi `flags.json` có mục): 1 dòng nền `--surface`, icon ⚠ + mô tả ngắn.
- **Lưới card 2×3** (mobile: 1 cột), mỗi card 1 module, viền trái 3px màu series của module:
  - Tên module · giá trị chính hiện tại (số to, `--ink`) · delta 1 ngày + 7 ngày · sparkline 30 ngày (màu series) · link "Chi tiết →".
  - Card Lãi suất: hiển thị "cao nhất 12T: 6,9% — BacABank" + trung vị.
  - Card Điện & Gas: giá bậc 1 + giá gas miền Nam tháng này.
  - Card thứ 6: **Tương quan** (P3 — trước đó hiển thị "sắp có").
- **Footer**: `Cập nhật 18h mỗi ngày · Cách hoạt động · Dữ liệu trên GitHub` (link repo) · dòng miễn trừ: *"Số liệu tổng hợp từ nguồn công khai, chỉ để tham khảo."*

### 5 trang chi tiết (`gold.html`, `fx.html`, `fuel.html`, `rates.html`, `utilities.html`)

Khung chung:
- Tiêu đề + dòng giải thích đơn vị.
- **Bộ chọn khung thời gian**: `1T · 6T · 1N · 2N · Tất cả` (một hàng nút, nút active nền series-color 15% + chữ `--ink`).
- Biểu đồ line chính (Chart.js, màu series module; gold/fx vẽ 2 đường mua–bán cùng hue đậm/nhạt + legend).
- Nút `Tải CSV` (link thẳng file trong `data/`) + nút `Bảng` (toggle table view 30 dòng gần nhất).
- `rates.html` khác khung: bảng so sánh 20 ngân hàng × 5 kỳ hạn là nội dung chính; ô tăng/giảm so tuần trước có ▲▼ màu `--up/--down`; trên bảng có biểu đồ line "cao nhất/trung vị/thấp nhất 12T theo tuần".
- `utilities.html`: biểu đồ bậc thang điện (stepped line) + line giá gas theo tháng, 2 chart riêng (không dual-axis).
- `fuel.html`: stepped line (giá giữ nguyên giữa các kỳ điều hành).

### `correlation.html` — Tương quan (P3)

Vàng vs USD vs lãi suất 12T trung vị, **index = 100** tại đầu khung, 3 series 3 màu module, legend + direct label điểm cuối. Ghi chú phương pháp 1 câu ở dưới.

### `docs.html` — "Cách hoạt động" (yêu cầu của owner)

Trang tĩnh, giọng đơn giản, là **URL tham chiếu được link từ index.html**. Nội dung:

1. **Dữ liệu này là gì** — 5 nhóm, nguồn nào (bảng: module → nguồn → tần suất).
2. **Cập nhật thế nào** — sơ đồ 4 bước: `18:05 mỗi ngày → robot đọc nguồn → kiểm tra chéo → đăng lên trang này`. Nói rõ chạy bằng Claude Code Routine, mã nguồn mở trên GitHub (link repo).
3. **Đọc số thế nào** — giải thích mua/bán, tỷ giá trung tâm, kỳ điều hành xăng, bậc thang điện. Mỗi khái niệm ≤ 2 câu.
4. **Độ tin cậy** — dữ liệu backfill lấy từ đâu (link `data/provenance.md` trên GitHub), dấu ⚠ nghĩa là gì, miễn trừ trách nhiệm.
5. **Câu hỏi thường gặp** — 4-5 mục (vì sao thiếu ngày X, vì sao lãi suất chỉ cập nhật thứ Hai…).

## Accessibility

- Mọi thông tin tăng/giảm: màu + mũi tên + dấu (không màu-alone).
- Sparkline có `aria-label` dạng "Vàng 30 ngày, từ 148,1 đến 151,4 triệu".
- Table view cho mọi chart. Contrast chữ: `--ink-2` trên `--surface` ≈ 6,7:1 — đạt AA.
- Không animation trừ transition hover ≤ 150ms; tôn trọng `prefers-reduced-motion`.
