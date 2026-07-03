# 07 — Checklist triển khai

Làm theo thứ tự. Mỗi mục là 1 lần commit/PR gọn, verify được trước khi sang mục sau.

## P0 — Skeleton (1–2 session)

- [ ] **P0.1 — Verify allowlist trong environment**: tạo custom environment với danh sách domain ở [01](01-sources-and-domains.md); từ trong environment fetch thử từng URL ✅/🔍, ghi kết quả (URL cuối cùng + render type + ghi chú cấu trúc trang) vào CLAUDE.md mục Nguồn. Chốt các mục 🔍: API JSON của VCB theo ngày, pattern lịch sử DOJI trên webgia, endpoint `update.giavang.doji.vn`, `gia.petrolimex.com.vn`.
- [ ] **P0.2 — CLAUDE.md + agents + prompts**: tạo `CLAUDE.md`, 7 file `.claude/agents/`, `ROUTINE_PROMPT.md`, `BACKFILL_PROMPTS/` từ draft ở [03](03-agents-and-prompts.md)/[04](04-backfill.md) (điền ghi chú cấu trúc trang thật từ P0.1).
- [ ] **P0.3 — Scripts**: `common.py`, 4 crawler daily, `validate.py`, `build_summary.py` theo [06](06-scripts-and-site-skeleton.md). Chạy tay từng crawler trong environment → mỗi cái phải in `OK …` với số liệu thật hôm đó.
- [ ] **P0.4 — Site**: 8 trang + style.css + app.js + logo.svg + logo-180.png + vendor Chart.js theo [05](05-site-design.md)/[06](06-scripts-and-site-skeleton.md). Có `summary.json` thật từ P0.3 → mở local xem card render đúng. **Check favicon hiện trên tab.** Chạy validator palette nếu có chỉnh màu.
- [ ] **P0.5 — Pages**: `pages.yml`, bật GitHub Pages (Source: GitHub Actions), push main → site live. Check `docs.html` được link từ index (header + footer).

**Definition of done P0**: site live trên Pages, dashboard hiển thị số liệu thật của ngày hôm đó (dữ liệu 1 ngày), favicon + logo hiển thị, docs.html đọc được.

## P1 — Backfill (5–6 one-off runs, xem [04](04-backfill.md))

- [ ] P1.1 — Viết `backfill_*.py` (khuôn giống crawler daily + vòng lặp ngày + checkpoint).
- [ ] P1.2 — Run 1 fx → check chart fx.html vẽ đủ 2 năm.
- [ ] P1.3 — Run 2 fuel → check stepped chart.
- [ ] P1.4 — Run 3 + 3b gold.
- [ ] P1.5 — Run 4 gas + điện.
- [ ] P1.6 — Run 5 rates (chấp nhận partial, độ phân giải tháng).
- [ ] P1.7 — `validate.py --full` toàn bộ; sửa ERROR; cập nhật `provenance.md`; xóa `backfill-progress.json`; tag `backfill-complete`.

## P2 — Daily routine

- [ ] P2.1 — Tạo routine: cron `5 11 * * *` UTC, prompt = "Đọc và làm theo ROUTINE_PROMPT.md", environment custom, fresh session, unrestricted push main.
- [ ] P2.2 — Chạy tay 1 lần (fire ngoài lịch) → check commit message chuẩn, run-log, site cập nhật.
- [ ] P2.3 — Theo dõi 7 ngày đầu: mỗi sáng xem run-log; script gãy → để cơ chế self-heal xử lý, chỉ can thiệp khi agent báo thiếu domain (thêm allowlist + CLAUDE.md).
- [ ] P2.4 — Sau 1 tuần ổn: kiểm tra thứ Hai có rates + electricity chạy; kỳ điều hành xăng (thường thứ Năm) được bắt đúng.

## P3 — Nâng cao

- [ ] P3.1 — `correlation.html`: vàng vs USD vs lãi suất, index = 100.
- [ ] P3.2 — Chênh lệch vàng VN vs thế giới: verify `stooq.com` (thêm allowlist), cột mới `xau_usd` + đường premium trên gold.html.
- [ ] P3.3 — (tùy chọn) Open Graph tags + ảnh share; light mode nếu có nhu cầu thật.

## Nhắc lại 3 quy tắc vận hành

1. Thêm nguồn = thêm domain vào environment **và** CLAUDE.md cùng commit.
2. Script gãy = self-heal (parse tay → sửa script → ghi chú CLAUDE.md) trong chính run đó.
3. Không sửa dữ liệu lịch sử bằng tay — mọi sửa đổi đi qua script + provenance.
