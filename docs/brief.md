# Brief: `vn-finance-dashboard` — Dashboard thị trường & tài chính (chạy DAILY)

> **Cách dùng file này:** Paste toàn bộ nội dung vào một session Claude (Fable 5) mới và yêu cầu:
> *"Dựa trên brief này, hãy viết detail plan gồm: (1) nội dung file `.claude/agents/*.md` cho từng subagent, (2) bản `ROUTINE_PROMPT.md` hoàn chỉnh cho routine daily, (3) `CLAUDE.md` với schema + quy tắc validate chéo, (4) danh sách allowed domains đầy đủ cho cloud environment, (5) chuỗi one-off backfill prompts cho từng module (2 năm lịch sử), (6) code skeleton scripts và template dashboard HTML với biểu đồ tương tác. Trước khi viết code, hãy dùng web search verify lại URL nguồn: trang tỷ giá lịch sử Vietcombank, bảng giá vàng SJC/DOJI, lịch sử điều chỉnh giá xăng Petrolimex."*

---

## 1. Mục tiêu

Repo lớn nhất — tổng hợp **5 nhóm dữ liệu** (vàng, tỷ giá USD/VND, lãi suất tiết kiệm, xăng dầu, điện + gas) vào **1 dashboard**, mỗi nhóm có trang chi tiết với lịch sử đầy đủ. **Chạy DAILY** bằng Claude Code Routine. Backfill **2 năm** dữ liệu lịch sử khi khởi tạo bằng one-off routines. KHÔNG dùng Claude API.

## 2. Hạ tầng: Claude Code Routines — DAILY

- **1 Routine chính**, trigger: scheduled daily, **~18h VN** (sau giờ chốt tỷ giá/giá vàng trong ngày). Run có thể trễ vài phút do stagger — chấp nhận được với dữ liệu ngày
- Daily = 7 runs/tuần → nằm trong cap Pro (5 routine runs/NGÀY, đây chỉ 1 run/ngày), nhưng là run "nặng" nhất trong các repo → **tối ưu usage là ưu tiên thiết kế** (xem mục 6)
- **Custom cloud environment** — allowed domains dự kiến (verify khi implement):
  - `sjc.com.vn`, `giavang.doji.vn` (hoặc domain DOJI hiện hành), `pnj.com.vn`
  - `portal.vietcombank.com.vn`, `vietcombank.com.vn`, `sbv.gov.vn`
  - `petrolimex.com.vn`, `pvoil.com.vn`
  - `web.archive.org` (cho backfill lãi suất)
  - Các trang ngân hàng theo dõi lãi suất (liệt kê đầy đủ trong CLAUDE.md)
  - **Lỗi 403 do thiếu domain là lỗi phổ biến nhất sẽ gặp** — quy trình: thêm nguồn mới = cập nhật environment + CLAUDE.md cùng lúc
- **Deploy**: unrestricted branch push → commit `main` → GitHub Pages

## 3. Multi-agent orchestration mỗi run daily

**Orchestrator (routine chính):**
1. Đọc `data/run-log.md` hôm trước (biết nguồn nào đang lỗi)
2. Spawn **song song**:

| Agent | Nhiệm vụ | Tần suất |
|---|---|---|
| `agent-gold` | Giá vàng SJC, DOJI (mua/bán) | Daily |
| `agent-fx` | Tỷ giá VCB (mua/bán/chuyển khoản) + tỷ giá trung tâm SBV | Daily |
| `agent-fuel-gas-check` | Check "có kỳ điều chỉnh xăng/gas mới không" → có thì append | Daily (nhẹ) |
| `agent-deposit-rates` | Lãi suất tiết kiệm ~20-30 ngân hàng, kỳ hạn 1/3/6/12/24 tháng | **Chỉ thứ Hai** (orchestrator kiểm tra thứ trong tuần) |
| `agent-electricity-check` | Check thay đổi biểu giá điện EVN | Chỉ thứ Hai (thay đổi rất thưa) |

3. `validator`: đối chiếu chéo (SJC lệch bất thường so DOJI → flag; tỷ giá nhảy >2%/ngày → flag), **1 module fail KHÔNG chặn module khác** — ghi lỗi, tiếp tục
4. `site-builder`: rebuild dashboard + trang chi tiết, cập nhật sparkline/delta so hôm qua
5. Commit 1 lần cuối run, message chuẩn: `daily: 2026-07-04 (gold ✓ fx ✓ fuel – rates skip)`

## 4. Schema dữ liệu (chuẩn hóa theo module)

```
data/gold/history.csv          # date, sjc_buy, sjc_sell, doji_buy, doji_sell
data/fx/history.csv            # date, vcb_buy_cash, vcb_buy_transfer, vcb_sell, sbv_central
data/deposit-rates/2026-W27.json   # snapshot tuần: [{bank, term_months, rate, source_url}]
data/fuel/history.csv          # effective_date, ron95, e5ron92, diesel, dau_hoa
data/utilities/electricity.json    # mỗi lần thay đổi: effective_date + bảng giá bậc thang đầy đủ
data/utilities/gas.csv         # effective_month, gia_binh_12kg (theo khu vực nếu có)
data/provenance.md             # dòng nào từ backfill nguồn nào, dòng nào crawl trực tiếp
data/run-log.md
```

Dữ liệu daily có độ phân giải **theo ngày** → biểu đồ 2 năm rất giá trị. Lãi suất giữ độ phân giải tuần (thay đổi chậm).

## 5. Migration lần đầu — backfill 2 NĂM (chuỗi one-off routines)

One-off routine chạy 1 lần rồi tự disable, **không tính vào daily cap**. Chia theo module, thứ tự từ dễ đến khó:

| Run | Module | Nguồn backfill | Độ khả thi |
|---|---|---|---|
| 1 | Tỷ giá VCB | Trang tra cứu tỷ giá lịch sử theo ngày của Vietcombank (chính thức) | Cao nhất |
| 2 | Xăng dầu | Lịch sử kỳ điều chỉnh Petrolimex (10 ngày/kỳ ≈ 73 kỳ/2 năm) | Cao |
| 3-4 | Vàng | Nguồn archive bảng giá vàng (trang thống kê của báo tài chính / webgia / tygia — **verify nguồn khi implement**); có thể cần 2 run | Trung bình |
| 5 | Gas + Điện | Gas: crawl tin điều chỉnh đầu tháng (24 mốc); Điện: vài mốc thay đổi biểu giá EVN | Trung bình |
| 6 | Lãi suất | Wayback Machine cho các trang tổng hợp lãi suất — **chấp nhận partial**; thiếu thì bắt đầu từ hiện tại | Thấp |

Quy tắc chung cho mọi run backfill:
- Checkpoint qua `data/backfill-progress.json`, commit sau mỗi run → run sau resume được
- Nếu 1 module quá lớn cho 1 session cloud: chia nhỏ thêm one-off runs, hoặc chạy phần còn lại bằng Claude Code local
- Rate limit lịch sự; ghi provenance đầy đủ vào `data/provenance.md`

## 6. Tối ưu usage (quan trọng vì chạy daily)

- Prompt hướng agent **chạy script có sẵn trong `scripts/` trước** cho các nguồn ổn định (rẻ, nhanh, ít token)
- Chỉ dùng reasoning khi script fail: *"Chạy `scripts/crawl_gold.py`; nếu output không hợp lệ, tự fetch trang và parse, sau đó SỬA LUÔN SCRIPT và commit bản sửa kèm ghi chú vào CLAUDE.md"* → hệ thống **tự vá crawler** theo thời gian
- Các agent check (fuel/gas/điện) thiết kế "exit sớm nếu không có gì mới"
- Site-builder chỉ rebuild trang có dữ liệu thay đổi

## 7. Static site (GitHub Pages)

- **Trang chủ dashboard:** card cho mỗi chỉ số — giá hiện tại + delta so hôm qua/tuần trước + sparkline mini
- **5 trang chi tiết:** biểu đồ tương tác (Chart.js hoặc ECharts) với chọn khung thời gian **1M / 6M / 1Y / 2Y / All**, bảng dữ liệu, nút download CSV
- **Trang "Tương quan":** biểu đồ overlay vàng vs USD vs lãi suất — điểm nhấn phân tích của dashboard
- Trang lãi suất: bảng so sánh ~20-30 ngân hàng theo kỳ hạn, highlight ngân hàng tăng/giảm so tuần trước

## 8. Cấu trúc repo

```
.claude/agents/        # agent-gold.md, agent-fx.md, agent-fuel-gas-check.md,
                       # agent-deposit-rates.md, agent-electricity-check.md,
                       # validator.md, site-builder.md
CLAUDE.md              # schema, quy tắc validate chéo, danh sách nguồn + allowed domains,
                       # ghi chú cấu trúc từng trang nguồn (cập nhật khi self-heal)
ROUTINE_PROMPT.md      # prompt routine daily (version control)
BACKFILL_PROMPTS/      # run-1-fx.md ... run-6-rates.md (chuỗi one-off)
scripts/               # crawl_gold.py, crawl_fx.py, crawl_fuel.py, ...
data/
site/
```

## 9. Các quyết định cần chốt trong detail plan

1. Danh sách ngân hàng theo dõi lãi suất (đề xuất: 4 Big4 + ~15-20 NHTM cổ phần lớn)
2. Có thêm chênh lệch giá vàng trong nước vs thế giới không (cần thêm nguồn giá quốc tế + tỷ giá quy đổi → thêm allowed domain)
3. Nguồn archive giá vàng cụ thể cho backfill (verify bằng web search)
4. Build site: HTML thuần + JS hay static site generator (khuyên: HTML thuần + Chart.js, đơn giản để agent maintain)
5. Giờ chạy daily chính xác (18h VN? cần sau giờ VCB chốt tỷ giá cuối ngày)
