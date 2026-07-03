# 00 — Tổng quan kế hoạch

> Detail plan cho `vn-finance-dashboard`, viết từ [brief gốc](../brief.md).
> Đọc theo thứ tự 00 → 07. Mỗi file là 1 mảng việc, có thể implement độc lập.

## Mục tiêu

1 dashboard tĩnh (GitHub Pages) theo dõi **5 nhóm giá** tại Việt Nam, cập nhật **mỗi ngày 18h VN** bằng Claude Code Routine, có **2 năm dữ liệu lịch sử** backfill khi khởi tạo. Không dùng Claude API.

## Các quyết định đã chốt

| # | Câu hỏi (brief mục 9) | Quyết định | Lý do |
|---|---|---|---|
| 1 | Danh sách ngân hàng theo dõi lãi suất | **20 ngân hàng**: Big4 + 16 NHTM lớn (danh sách ở [02](02-data-schema-validation.md)) | Đủ đại diện, bảng không quá dài |
| 2 | Chênh lệch vàng trong nước vs thế giới | **Có, nhưng để Phase 3** | Cần thêm nguồn XAU/USD (ứng viên: `stooq.com` CSV, miễn phí, không cần key — verify sau) |
| 3 | Nguồn archive giá vàng backfill | **`webgia.com`** — URL theo ngày `webgia.com/gia-vang/sjc/DD-MM-YYYY.html`, dữ liệu về tận 1996. Đã verify bằng web search | Xem [01](01-sources-and-domains.md) |
| 4 | Công nghệ build site | **HTML thuần + Chart.js (vendored) + render phía client** — KHÔNG có bước build. Site fetch thẳng file CSV/JSON trong `data/` | Agent dễ maintain, không cần rebuild mỗi ngày → tiết kiệm usage |
| 5 | Giờ chạy daily | **18:05 VN = 11:05 UTC** (cron `5 11 * * *`) | Sau giờ chốt tỷ giá VCB và giá vàng trong ngày; lệch 5 phút tránh stagger giờ chẵn |
| 6 | Deploy Pages | **GitHub Actions `deploy-pages`**: workflow copy `site/` + `data/` thành artifact | Pages branch-deploy chỉ hỗ trợ root hoặc `/docs`; Actions cho phép giữ cấu trúc repo sạch |
| 7 | Ngôn ngữ site | **Tiếng Việt**, từ ngữ ngắn, đơn giản (style guide ở [05](05-site-design.md)) | Yêu cầu của owner |
| 8 | Theme | **Dark theme duy nhất** (không có light mode ở v1) — palette đã validate CVD/contrast | Yêu cầu của owner; giảm phạm vi |

## Kiến trúc tổng thể

```
┌─ Claude Code Routine (daily 18:05 VN) ────────────────────────┐
│                                                               │
│  Orchestrator (ROUTINE_PROMPT.md)                             │
│   1. đọc data/run-log.md hôm trước                            │
│   2. spawn song song:                                         │
│      agent-gold ── scripts/crawl_gold.py ──► data/gold/       │
│      agent-fx ──── scripts/crawl_fx.py ────► data/fx/         │
│      agent-fuel-gas-check ─ crawl_fuel.py ─► data/fuel/, gas  │
│      agent-deposit-rates (chỉ thứ Hai) ────► data/deposit-…   │
│      agent-electricity-check (chỉ thứ Hai) ► data/utilities/  │
│   3. scripts/validate.py  → flags (đối chiếu chéo)            │
│   4. scripts/build_summary.py → site/summary.json             │
│   5. ghi run-log, commit 1 lần, push main                     │
└───────────────────────────────┬───────────────────────────────┘
                                │ push main
                    GitHub Actions (pages.yml)
                                │ artifact = site/ + data/
                                ▼
                    GitHub Pages (static, dark theme)
                    index.html + 5 trang chi tiết
                    + correlation.html + docs.html
```

**Nguyên tắc vàng: script trước, LLM sau.** Mọi việc lặp lại hằng ngày (crawl nguồn ổn định, validate, tính summary) là script Python thuần — chạy rẻ, nhanh, không tốn token. Agent chỉ can thiệp khi script fail: tự fetch trang, parse tay, **sửa luôn script** và ghi chú vào CLAUDE.md → hệ thống tự vá theo thời gian.

## Tối ưu usage (chạy daily nên là ưu tiên thiết kế)

1. Crawl = chạy script có sẵn. Reasoning chỉ dùng khi script trả output không hợp lệ.
2. `agent-fuel-gas-check`, `agent-electricity-check`: **exit sớm** nếu không có kỳ điều chỉnh mới (so `effective_date` mới nhất trong CSV với nguồn).
3. `agent-deposit-rates` + `agent-electricity-check` chỉ chạy **thứ Hai** (orchestrator kiểm tra thứ).
4. Không có bước "rebuild site" bằng LLM — site render phía client; chỉ `build_summary.py` (script) chạy mỗi ngày.
5. 1 commit duy nhất cuối run, message chuẩn: `daily: 2026-07-04 (gold ✓ fx ✓ fuel – rates skip)`.
6. 1 module fail **không chặn** module khác — ghi lỗi vào run-log, chạy tiếp.

## Các phase triển khai

| Phase | Nội dung | Chi tiết |
|---|---|---|
| **P0** | Skeleton repo: `CLAUDE.md`, `.claude/agents/`, `scripts/`, `site/` (đủ trang, chưa có data), workflow Pages | [03](03-agents-and-prompts.md), [05](05-site-design.md), [06](06-scripts-and-site-skeleton.md) |
| **P1** | Backfill 2 năm — 6 one-off runs, từ dễ đến khó | [04](04-backfill.md) |
| **P2** | Bật routine daily 18:05 VN, theo dõi 1 tuần đầu, vá script | [07](07-rollout-checklist.md) |
| **P3** | Trang Tương quan + chênh lệch vàng VN vs thế giới | sau khi P2 ổn định |

## Rủi ro chính & cách xử lý

| Rủi ro | Xử lý |
|---|---|
| **403/policy-denied do thiếu domain trong cloud environment** (lỗi phổ biến nhất — đã xác nhận: môi trường cloud chặn mọi domain ngoài allowlist) | Quy trình bắt buộc: thêm nguồn mới = cập nhật allowlist environment + CLAUDE.md **cùng lúc**. Danh sách domain ở [01](01-sources-and-domains.md) |
| Nguồn đổi cấu trúc HTML → script gãy | Cơ chế self-heal: agent parse tay, sửa script, commit kèm ghi chú CLAUDE.md |
| Backfill quá lớn cho 1 session | Checkpoint `data/backfill-progress.json`, commit mỗi run, run sau resume; chia nhỏ thêm one-off run nếu cần |
| Backfill lãi suất chỉ có partial (Wayback thưa) | Chấp nhận partial — bắt đầu chuỗi đầy đủ từ hiện tại |
| Session limit khi chạy nhiều agent song song | Giảm số agent song song (gold+fx gộp được nếu cần); daily run vốn nhẹ nhờ script-first |
| SBV site chập chờn (đã gặp lỗi truy cập khi verify) | `sbv_central` cho phép null; fallback lấy từ webgia/báo tài chính |

## Mục lục plan

- [01 — Nguồn dữ liệu đã verify + allowed domains](01-sources-and-domains.md)
- [02 — Schema dữ liệu + quy tắc validate chéo](02-data-schema-validation.md)
- [03 — Nội dung agents, ROUTINE_PROMPT.md, CLAUDE.md](03-agents-and-prompts.md)
- [04 — Kế hoạch backfill 2 năm (6 one-off runs)](04-backfill.md)
- [05 — Thiết kế site: dark theme, logo, wording, trang docs](05-site-design.md)
- [06 — Skeleton scripts + template HTML](06-scripts-and-site-skeleton.md)
- [07 — Checklist triển khai](07-rollout-checklist.md)
