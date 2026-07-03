---
name: agent-fuel-gas-check
description: Check kỳ điều chỉnh xăng dầu mới + giá gas tháng mới (nhẹ, exit sớm)
tools: Bash, Read, Edit, Write, WebFetch
---

Nhiệm vụ kép, thiết kế để EXIT SỚM khi không có gì mới.

XĂNG:
1. Chạy `python3 scripts/crawl_fuel.py --check`.
   - `NO_CHANGE` → phần xăng xong.
   - `NEW <effective_date>` → chạy `python3 scripts/crawl_fuel.py --append` để lấy
     giá vùng 1 (RON95/E5/diesel/dầu hỏa) và append `data/fuel/history.csv`.
   - `FAIL parse` → parse tay bài thông cáo Petrolimex mới nhất, append, sửa
     `latest_release_date`/`parse_prices` trong script + cập nhật CLAUDE.md.
   - `FAIL blocked` → báo thiếu domain, không sửa script.

GAS (chỉ khi hôm nay là ngày 1–4 của tháng VÀ `data/utilities/gas.csv` chưa có
dòng tháng này):
2. Fetch bài "Giá gas hôm nay 1/<tháng>" trên vietnambiz.vn (CLAUDE.md mục
   Nguồn/Gas). Ghi giá bình 12kg 3 miền (HN/ĐN/HCM) + giá CP (USD/tấn) vào
   `data/utilities/gas.csv` (cột: effective_month, mien_bac, mien_trung, mien_nam,
   cp_usd_ton). effective_month = `YYYY-MM`.

Trả về 2 dòng: `fuel – | fuel ✓ <ngày kỳ>` và `gas – | gas ✓ <tháng>`.
Cấm: bịa số, sửa kỳ/tháng cũ.
