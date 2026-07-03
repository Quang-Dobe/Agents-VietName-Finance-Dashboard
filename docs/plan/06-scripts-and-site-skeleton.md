# 06 — Skeleton `scripts/` + template site

## 6.1 Cấu trúc repo đích (sau P0)

```
.claude/agents/            # 7 file — nội dung ở docs/plan/03
CLAUDE.md
ROUTINE_PROMPT.md
BACKFILL_PROMPTS/          # run-1-fx.md … run-5-rates.md
.github/workflows/pages.yml
scripts/
  common.py                # fetch + retry + parse helpers dùng chung
  crawl_gold.py  crawl_fx.py  crawl_fuel.py  crawl_rates.py
  backfill_fx.py backfill_gold.py backfill_fuel.py backfill_gas.py backfill_rates.py
  validate.py    build_summary.py
data/                      # schema ở docs/plan/02
site/
  index.html  gold.html  fx.html  fuel.html  rates.html  utilities.html
  correlation.html  docs.html
  summary.json             # build_summary.py sinh ra
  assets/  style.css  app.js  logo.svg  logo-180.png
           vendor/chart.umd.js        # Chart.js vendored, không CDN
```

Chỉ dùng **stdlib Python** (`urllib`, `html.parser`, `csv`, `json`) — không dependency để môi trường nào cũng chạy được. Nếu buộc phải thêm lib (khó xảy ra), ghi vào CLAUDE.md.

## 6.2 `scripts/common.py`

```python
"""Helpers dùng chung. Mọi crawler import từ đây."""
import urllib.request, time, csv, json, sys, re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
UA = "Mozilla/5.0 (vn-finance-dashboard; +https://github.com/<owner>/<repo>)"

def fetch(url: str, retries: int = 2, delay: float = 1.5) -> str:
    """GET với retry. Lỗi 403 → raise DomainBlocked để agent báo thiếu allowlist."""
    ...

def append_csv_row(path: Path, row: dict, key: str = "date") -> bool:
    """Append 1 dòng; nếu key đã tồn tại thì thay dòng đó. Giữ sort theo key.
    Trả về True nếu file thay đổi."""
    ...

def vn_number(s: str) -> float:
    """'151.400' / '151,400' / '4,7%' → float. Chuẩn hóa mọi kiểu số VN."""
    ...

class DomainBlocked(Exception): ...
```

## 6.3 Crawler daily — khuôn chung (ví dụ `crawl_gold.py`)

Mọi crawler in đúng **1 dòng cuối**: `OK <csv-row>` / `NO_CHANGE` / `FAIL <lý do>` — agent chỉ nhìn dòng này.

```python
#!/usr/bin/env python3
"""Giá vàng SJC + DOJI hôm nay → data/gold/history.csv
Cấu trúc trang nguồn: xem CLAUDE.md mục Nguồn/Vàng (cập nhật khi self-heal)."""
from common import fetch, append_csv_row, vn_number, ROOT, DomainBlocked
from datetime import date

SJC_URL  = "https://sjc.com.vn/gia-vang-online"
DOJI_URL = "https://giavang.doji.vn/"

def parse_sjc(html: str) -> tuple[float, float]:
    """→ (buy, sell) nghìn đ/lượng, vàng miếng TP.HCM. Raise nếu không tìm thấy."""
    ...

def parse_doji(html: str) -> tuple[float, float]: ...

def main() -> int:
    row = {"date": date.today().isoformat()}
    try:
        row["sjc_buy"], row["sjc_sell"] = parse_sjc(fetch(SJC_URL))
        row["doji_buy"], row["doji_sell"] = parse_doji(fetch(DOJI_URL))
    except DomainBlocked as e:
        print(f"FAIL blocked: {e}"); return 2
    except Exception as e:
        print(f"FAIL parse: {e}"); return 1
    # sanity tối thiểu ngay tại crawler (validator sẽ kiểm kỹ hơn)
    if not (30_000 < row["sjc_sell"] < 500_000) or row["sjc_sell"] <= row["sjc_buy"]:
        print(f"FAIL sanity: {row}"); return 1
    append_csv_row(ROOT / "data/gold/history.csv", row)
    print(f"OK {row}"); return 0

if __name__ == "__main__":
    raise SystemExit(main())
```

`crawl_fx.py` cùng khuôn (SBV lỗi → để rỗng, vẫn `OK`). `crawl_fuel.py` thêm cờ `--check` (chỉ so ngày kỳ mới nhất, không ghi) và `--append`. `crawl_rates.py` ghi JSON tuần thay vì CSV.

## 6.4 `validate.py` & `build_summary.py`

- `validate.py [--module m] [--full]`: đọc data/, áp bảng quy tắc ở [02](02-data-schema-validation.md) (ngưỡng đặt trong `RULES` dict ngay đầu file để dễ sửa), in từng vi phạm `ERROR|FLAG <module> <ngày> <mô tả>`, ghi `data/flags.json`. Exit 0 nếu không ERROR.
- `build_summary.py`: đọc data/ → tính latest, delta 1d/7d, sparkline 30 điểm/module → ghi `site/summary.json` (schema ở [02](02-data-schema-validation.md)). Thuần số học, không fetch mạng.

## 6.5 `.github/workflows/pages.yml`

```yaml
name: pages
on:
  push: { branches: [main], paths: [site/**, data/**] }
  workflow_dispatch:
permissions: { pages: write, id-token: write }
jobs:
  deploy:
    runs-on: ubuntu-latest
    environment: { name: github-pages, url: "${{ steps.d.outputs.page_url }}" }
    steps:
      - uses: actions/checkout@v4
      - run: |
          mkdir -p _pub && cp -r site/* _pub/ && cp -r data _pub/data
      - uses: actions/upload-pages-artifact@v3
        with: { path: _pub }
      - id: d
        uses: actions/deploy-pages@v4
```

Site fetch dữ liệu bằng đường dẫn tương đối `data/...` — chạy được cả local (`python3 -m http.server` từ `_pub/` hoặc từ root repo với symlink) lẫn trên Pages.

## 6.6 Template site

### `site/app.js` — helpers chung (không framework)

```js
// parse CSV đơn giản (dữ liệu mình kiểm soát, không cần lib)
async function loadCSV(path) {
  const text = await (await fetch(path)).text();
  const [head, ...rows] = text.trim().split("\n").map(l => l.split(","));
  return rows.map(r => Object.fromEntries(head.map((h, i) => [h, r[i]])));
}
const fmtVN = n => new Intl.NumberFormat("vi-VN").format(n);
const deltaHTML = d => d == null ? "" :
  `<span class="${d >= 0 ? "up" : "down"}">${d >= 0 ? "▲ +" : "▼ −"}${Math.abs(d).toFixed(1)}%</span>`;
// lọc theo khung thời gian 1T/6T/1N/2N/Tất cả
function sliceRange(rows, months) { ... }
// vẽ line chart Chart.js với defaults dark theme (grid #23304C, ink #A7B4CE,
// tooltip crosshair, 1 trục y) — mọi trang gọi hàm này thay vì tự cấu hình
function makeLineChart(canvas, series, opts) { ... }
function sparkline(canvas, values, color) { ... }  // chart trần: không trục, không grid
```

### `site/index.html` — khung

```html
<!doctype html><html lang="vi"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Giá Việt — Vàng, USD, Xăng, Lãi suất</title>
<link rel="icon" type="image/svg+xml" href="assets/logo.svg">
<link rel="apple-touch-icon" href="assets/logo-180.png">
<link rel="stylesheet" href="assets/style.css">
</head><body>
<header>
  <img src="assets/logo.svg" alt="" width="28" height="28">
  <div><h1>Giá Việt</h1>
    <p class="tagline">Vàng · USD · Xăng · Lãi suất · Điện &amp; Gas — cập nhật 18h mỗi ngày</p></div>
  <nav><a href="docs.html">Cách hoạt động</a></nav>
</header>
<div id="flags" hidden></div>            <!-- hiện khi flags.json có mục -->
<main class="grid">
  <a class="card" href="gold.html" style="--c:var(--c-gold)">
    <h2>Vàng SJC</h2>
    <p class="big" id="gold-price">…</p>  <!-- 151.400.000 ₫/lượng -->
    <p class="deltas" id="gold-delta"></p><!-- ▲ +0,4% hôm qua · +1,2% 7 ngày -->
    <canvas class="spark" id="gold-spark" aria-label=""></canvas>
    <span class="more">Chi tiết →</span>
  </a>
  <!-- fx, fuel, rates, utilities: cùng khuôn; card 6 = correlation (P3) -->
</main>
<footer>
  <span id="updated"></span> ·
  <a href="docs.html">Cách hoạt động</a> ·
  <a href="https://github.com/<owner>/<repo>">Dữ liệu trên GitHub</a>
  <p class="disclaimer">Số liệu tổng hợp từ nguồn công khai, chỉ để tham khảo.</p>
</footer>
<script src="assets/vendor/chart.umd.js"></script>
<script src="assets/app.js"></script>
<script>
  // index chỉ đọc summary.json — nhẹ và tức thì
  fetch("summary.json").then(r => r.json()).then(renderCards);
</script>
</body></html>
```

### Trang chi tiết — khuôn (`gold.html`)

```html
<main>
  <h1>Vàng miếng</h1>
  <p class="unit">Triệu đồng mỗi lượng. SJC tại TP.HCM, DOJI tại Hà Nội.</p>
  <div class="ranges" role="tablist">
    <button data-m="1">1T</button><button data-m="6">6T</button>
    <button data-m="12" class="active">1N</button><button data-m="24">2N</button>
    <button data-m="0">Tất cả</button>
  </div>
  <canvas id="chart"></canvas>           <!-- 2 đường: bán (đậm) / mua (nhạt) + legend -->
  <div class="actions">
    <a href="data/gold/history.csv" download>Tải CSV</a>
    <button id="toggle-table">Bảng</button>
  </div>
  <table id="table" hidden></table>      <!-- 30 dòng gần nhất -->
</main>
<script>
  loadCSV("data/gold/history.csv").then(rows => initDetailPage(rows, {
    series: [
      { key: "sjc_sell", label: "SJC bán", color: css("--c-gold") },
      { key: "sjc_buy",  label: "SJC mua", color: css("--c-gold"), dim: true },
    ],
    scale: 1000,   // nghìn đ/lượng → triệu đ/lượng khi hiển thị
  }));
</script>
```

`fuel.html`/`utilities.html` truyền `stepped: true`. `rates.html` dùng khuôn riêng (bảng chính + chart phụ) như mô tả ở [05](05-site-design.md).

### `site/assets/style.css`

Токens từ [05](05-site-design.md) trong `:root`; layout: header flex, `.grid` = `grid-template-columns: repeat(auto-fit, minmax(300px, 1fr))`, card nền `--surface` bo 12px viền trái 3px `var(--c)`, hover nhấc nhẹ `translateY(-2px)`; `@media (prefers-reduced-motion: reduce)` tắt transition. ~150 dòng, không framework.

## 6.7 Chart.js

- Vendor bản UMD mới nhất 4.x vào `site/assets/vendor/chart.umd.js` (1 file, ~200KB) — **không CDN** để trang tự chứa và không phụ thuộc mạng ngoài.
- Defaults dark cấu hình 1 lần trong `makeLineChart` (không copy config từng trang).
- Sparkline cũng dùng Chart.js (chart trần) — không thêm lib thứ hai.
