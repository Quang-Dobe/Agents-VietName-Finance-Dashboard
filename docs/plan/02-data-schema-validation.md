# 02 — Schema dữ liệu + quy tắc validate

## Nguyên tắc chung

- CSV **append-only**, sort tăng dần theo ngày, **1 dòng/ngày** (dedupe theo cột ngày — chạy lại trong ngày thì ghi đè dòng của ngày đó).
- Ngày dạng ISO `YYYY-MM-DD`. Số dùng dấu chấm thập phân, **không** phân tách hàng nghìn (định dạng hiển thị kiểu VN là việc của frontend).
- Đơn vị cố định ghi ở header comment dòng 1 của mỗi file và trong CLAUDE.md.
- Trường không lấy được → để **rỗng** (CSV) / `null` (JSON), KHÔNG bịa, KHÔNG copy giá hôm trước.

## Cấu trúc `data/`

```
data/
  gold/history.csv
  fx/history.csv
  deposit-rates/2026-W27.json      # 1 file / tuần ISO
  deposit-rates/latest.json        # symlink logic: bản mới nhất (copy)
  fuel/history.csv
  utilities/electricity.json
  utilities/gas.csv
  provenance.md
  run-log.md
  backfill-progress.json           # chỉ tồn tại trong P1
```

## Schema từng file

### `data/gold/history.csv` — đơn vị: nghìn đồng/lượng

```csv
date,sjc_buy,sjc_sell,doji_buy,doji_sell
2026-07-03,148400,151400,148400,151400
```

Lấy giá **TP.HCM với SJC, Hà Nội với DOJI** (khu vực niêm yết chính của mỗi hãng), loại vàng miếng.

### `data/fx/history.csv` — đơn vị: VND/USD

```csv
date,vcb_buy_cash,vcb_buy_transfer,vcb_sell,sbv_central
2026-07-03,26120,26150,26480,25150
```

`sbv_central` cho phép rỗng (SBV chập chờn, không công bố cuối tuần).

### `data/deposit-rates/YYYY-Www.json` — %/năm, lãi cuối kỳ, gửi tại quầy

```json
{
  "week": "2026-W27",
  "collected_at": "2026-07-06",
  "source_url": "https://webgia.com/lai-suat/",
  "rates": [
    {"bank": "VCB", "term_months": 12, "rate": 4.7}
  ]
}
```

`term_months` ∈ {1, 3, 6, 12, 24}. **20 ngân hàng theo dõi** (mã dùng trong `bank`):

> Big4: `VCB`, `BIDV`, `VietinBank`, `Agribank`
> NHTM: `Techcombank`, `VPBank`, `MB`, `ACB`, `Sacombank`, `SHB`, `HDBank`, `VIB`, `TPBank`, `MSB`, `OCB`, `Eximbank`, `SeABank`, `LPBank`, `NamABank`, `BacABank`

Ngân hàng thiếu trong nguồn tuần đó → bỏ qua ngân hàng đó, ghi chú run-log (không fail cả module).

### `data/fuel/history.csv` — đơn vị: đồng/lít, 1 dòng/kỳ điều hành

```csv
effective_date,ron95,e5ron92,diesel,dau_hoa
2026-07-01,21580,20120,19340,19010
```

Giá vùng 1 của Petrolimex. `effective_date` = ngày hiệu lực (không phải ngày crawl).

### `data/utilities/electricity.json` — 1 phần tử/lần thay đổi biểu giá

```json
{
  "changes": [
    {
      "effective_date": "2025-05-10",
      "decision": "1279/QĐ-BCT",
      "unit": "đồng/kWh, chưa VAT",
      "tiers": [
        {"from_kwh": 0,   "to_kwh": 50,   "price": 1984},
        {"from_kwh": 51,  "to_kwh": 100,  "price": 2050},
        {"from_kwh": 101, "to_kwh": 200,  "price": 2380},
        {"from_kwh": 201, "to_kwh": 300,  "price": 2998},
        {"from_kwh": 301, "to_kwh": 400,  "price": 3350},
        {"from_kwh": 401, "to_kwh": null, "price": 3460}
      ]
    }
  ]
}
```

### `data/utilities/gas.csv` — đơn vị: đồng/bình 12kg

```csv
effective_month,mien_bac,mien_trung,mien_nam,cp_usd_ton
2026-07,502200,483000,522000,590
```

Giá đại diện mỗi miền (HN / ĐN / TP.HCM, hãng phổ biến trong bài nguồn). `cp_usd_ton` = giá hợp đồng thế giới, cho phép rỗng.

### `data/provenance.md`

Bảng: khoảng ngày → nguồn (backfill webgia / crawl trực tiếp SJC…) → run tạo ra nó. Backfill ghi 1 dòng/run; daily ghi 1 dòng/tháng (gộp).

### `data/run-log.md`

Mỗi run append 1 mục, **giữ 30 mục gần nhất** (cũ hơn thì xóa để file không phình):

```markdown
## 2026-07-04 (daily)
- gold ✓  fx ✓  fuel – (không có kỳ mới)  rates skip (không phải thứ Hai)  electricity skip
- flags: (không)
- lỗi: sbv_central null — dttktt.sbv.gov.vn timeout, đã thử 2 lần
```

## Quy tắc validate (scripts/validate.py — chạy mỗi run)

Hai mức: **ERROR** = không ghi dòng đó vào CSV, báo run-log; **FLAG** = vẫn ghi, đánh dấu để người xem/agent chú ý.

### Sanity (ERROR)

| Trường | Điều kiện hợp lệ |
|---|---|
| gold buy/sell | 30.000 – 500.000 (nghìn đ/lượng) và `sell > buy` |
| fx | 15.000 – 50.000 VND/USD và `sell > buy_transfer ≥ buy_cash` |
| rate | 0,1 – 15 %/năm |
| fuel | 5.000 – 60.000 đ/lít |
| gas | 200.000 – 1.200.000 đ/bình |
| date | không ở tương lai, đúng ISO |

### Đối chiếu chéo (FLAG)

| Quy tắc | Ngưỡng |
|---|---|
| SJC lệch bất thường so DOJI (cùng ngày, giá bán) | > 3% |
| Vàng nhảy so hôm trước | > 5%/ngày |
| Tỷ giá VCB nhảy so hôm trước | > 2%/ngày |
| VCB sell lệch so SBV central | > 5% (biên độ cho phép ±5%) |
| Xăng kỳ mới lệch so kỳ trước | > 20% |
| Lãi suất 1 ngân hàng đổi so tuần trước | > 2 điểm % |
| Gas tháng mới lệch so tháng trước | > 30% |

Flag ghi vào run-log + file `data/flags.json` (site hiển thị dấu ⚠ trên card tương ứng). **1 module fail không chặn module khác.**

## `site/summary.json` (build_summary.py sinh ra mỗi run)

Frontend đọc file này để vẽ card tức thì, không phải parse CSV lớn:

```json
{
  "generated_at": "2026-07-04T11:08:00Z",
  "gold":  {"latest": {"date": "2026-07-04", "sjc_sell": 151400},
            "delta_1d": 0.4, "delta_7d": 1.2, "spark_30d": [148.1, 148.9]},
  "fx":    {"latest": {"date": "2026-07-04", "vcb_sell": 26480},
            "delta_1d": -0.1, "delta_7d": 0.2, "spark_30d": []},
  "fuel":  {"latest": {"effective_date": "2026-07-01", "ron95": 21580},
            "delta_period": -2.1, "spark_30d": []},
  "rates": {"latest_week": "2026-W27", "top12m": {"bank": "BacABank", "rate": 6.9},
            "median_12m": 5.1},
  "utilities": {"electricity_effective": "2025-05-10", "tier1_price": 1984,
                "gas_month": "2026-07", "gas_mien_nam": 522000,
                "gas_delta": -11.8},
  "flags": []
}
```
