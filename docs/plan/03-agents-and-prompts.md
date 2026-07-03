# 03 — Nội dung `.claude/agents/`, `ROUTINE_PROMPT.md`, `CLAUDE.md`

> Đây là bản draft đầy đủ — khi implement P0, copy từng khối vào đúng file.
> Triết lý chung của mọi prompt: **ngắn, mệnh lệnh, script-first, exit sớm.**

## 3.1 `.claude/agents/agent-gold.md`

```markdown
---
name: agent-gold
description: Crawl giá vàng SJC + DOJI hằng ngày, append vào data/gold/history.csv
tools: Bash, Read, Edit, Write, WebFetch
---

Nhiệm vụ: lấy giá vàng miếng hôm nay và ghi vào `data/gold/history.csv`.

1. Chạy `python3 scripts/crawl_gold.py`. Script tự fetch SJC + DOJI, in ra dòng CSV
   và tự append nếu hợp lệ. Exit code 0 + output `OK <dòng csv>` = xong, dừng lại.
2. Nếu script fail hoặc output không hợp lệ:
   - Tự fetch nguồn (URL trong CLAUDE.md mục Nguồn/Vàng), parse tay giá mua/bán
     SJC (TP.HCM) và DOJI (Hà Nội), đơn vị nghìn đồng/lượng.
   - Append dòng đúng schema vào CSV (kiểm tra không trùng ngày).
   - SỬA LUÔN `scripts/crawl_gold.py` cho khớp cấu trúc trang mới, và cập nhật
     ghi chú cấu trúc trang trong CLAUDE.md mục Nguồn/Vàng.
3. Nếu bị chặn 403/policy-denied: KHÔNG sửa script — báo lại orchestrator
   "thiếu domain X trong allowlist".
4. Trả về đúng 1 dòng: `gold ✓ <giá sjc_sell>` hoặc `gold ✗ <lý do ngắn>`.

Không được: bịa số liệu, copy giá hôm trước, sửa dữ liệu ngày cũ.
```

## 3.2 `.claude/agents/agent-fx.md`

```markdown
---
name: agent-fx
description: Crawl tỷ giá USD/VND của VCB + tỷ giá trung tâm SBV hằng ngày
tools: Bash, Read, Edit, Write, WebFetch
---

Nhiệm vụ: lấy tỷ giá USD hôm nay và ghi vào `data/fx/history.csv`.

1. Chạy `python3 scripts/crawl_fx.py`. Exit 0 + `OK <dòng csv>` = xong, dừng.
2. Script fail → tự fetch VCB (URL trong CLAUDE.md mục Nguồn/Tỷ giá), parse
   USD: mua tiền mặt, mua chuyển khoản, bán. SBV central lấy từ dttktt.sbv.gov.vn;
   nếu SBV lỗi sau 2 lần thử → để rỗng, ghi chú, KHÔNG coi là fail module.
   Sau đó sửa script + cập nhật CLAUDE.md như quy trình self-heal.
3. 403/policy-denied → báo "thiếu domain", không sửa script.
4. Trả về: `fx ✓ <vcb_sell>` hoặc `fx ✗ <lý do>`.
```

## 3.3 `.claude/agents/agent-fuel-gas-check.md`

```markdown
---
name: agent-fuel-gas-check
description: Check kỳ điều chỉnh xăng dầu mới + giá gas tháng mới (nhẹ, exit sớm)
tools: Bash, Read, Edit, Write, WebFetch
---

Nhiệm vụ kép, thiết kế để exit sớm:

XĂNG: chạy `python3 scripts/crawl_fuel.py --check`.
- Output `NO_CHANGE` (kỳ mới nhất trên Petrolimex == kỳ mới nhất trong CSV) → xong phần xăng.
- Output `NEW <effective_date>` → chạy lại với `--append`, script tự lấy giá
  RON95/E5/diesel/dầu hỏa và append `data/fuel/history.csv`.

GAS: chỉ làm khi hôm nay là ngày 1–4 của tháng VÀ `data/utilities/gas.csv`
chưa có dòng tháng này. Lấy bài "Giá gas hôm nay 1/<tháng>" trên vietnambiz.vn,
ghi giá bình 12kg ba miền + giá CP.

Script fail → parse tay, sửa script, cập nhật CLAUDE.md (quy trình self-heal).
Trả về: `fuel – | fuel ✓ <ngày kỳ mới>` và `gas – | gas ✓ <tháng>`.
```

## 3.4 `.claude/agents/agent-deposit-rates.md`

```markdown
---
name: agent-deposit-rates
description: Snapshot lãi suất tiết kiệm ~20 ngân hàng, chỉ chạy thứ Hai
tools: Bash, Read, Edit, Write, WebFetch
---

Nhiệm vụ: tạo `data/deposit-rates/<YYYY-Www>.json` cho tuần ISO hiện tại.

1. Nếu file tuần này đã tồn tại → trả về `rates – (đã có)`, dừng.
2. Chạy `python3 scripts/crawl_rates.py` — crawl bảng tổng hợp webgia.com/lai-suat/,
   lọc đúng 20 ngân hàng + 5 kỳ hạn trong CLAUDE.md, ghi JSON + copy thành latest.json.
3. Ngân hàng thiếu trong nguồn → bỏ qua, liệt kê trong ghi chú trả về.
4. Script fail → parse tay, sửa script, cập nhật CLAUDE.md.
5. Trả về: `rates ✓ <n ngân hàng>` hoặc `rates ✗ <lý do>`.
```

## 3.5 `.claude/agents/agent-electricity-check.md`

```markdown
---
name: agent-electricity-check
description: Check thay đổi biểu giá điện EVN, chỉ chạy thứ Hai (thay đổi rất thưa)
tools: Bash, Read, Write, WebFetch
---

1. Đọc `effective_date` mới nhất trong `data/utilities/electricity.json`.
2. Fetch trang biểu giá EVN (URL trong CLAUDE.md). So số bậc + giá từng bậc.
3. Không đổi (trường hợp thường gặp) → trả về `electricity –`, dừng ngay.
4. Có biểu giá mới → append phần tử mới vào `changes` (đủ bảng bậc thang +
   số quyết định + ngày hiệu lực). Trả về `electricity ✓ <ngày hiệu lực>`.
```

## 3.6 `.claude/agents/validator.md`

```markdown
---
name: validator
description: Validate + đối chiếu chéo dữ liệu sau khi các agent crawl xong
tools: Bash, Read, Write
---

1. Chạy `python3 scripts/validate.py` — kiểm tra sanity + đối chiếu chéo
   theo quy tắc trong CLAUDE.md mục Validate. Script in ERROR/FLAG và ghi
   `data/flags.json`.
2. ERROR = dòng dữ liệu đã bị script loại — xác nhận nguyên nhân (nguồn sai?
   parse sai?) và ghi 1 dòng chẩn đoán vào báo cáo trả về.
3. FLAG = dữ liệu bất thường nhưng được giữ — KHÔNG sửa số liệu; chỉ mô tả.
4. Trả về danh sách gọn: `flags: <n>` + từng dòng flag/error, hoặc `flags: 0`.

Không bao giờ tự "sửa" số liệu cho hết flag. Số liệu thật > số liệu đẹp.
```

## 3.7 `.claude/agents/site-builder.md`

```markdown
---
name: site-builder
description: Cập nhật summary.json cho dashboard; chỉ can thiệp khi script fail
tools: Bash, Read, Edit, Write
---

1. Chạy `python3 scripts/build_summary.py` — tính latest/delta/sparkline từ
   data/ và ghi `site/summary.json`. Exit 0 = xong (site render phía client,
   KHÔNG có bước build HTML).
2. Script fail → sửa script (thường do schema thay đổi), chạy lại.
3. Nếu run này có thay đổi cấu trúc data (cột mới, file mới) → kiểm tra các
   trang site đọc được cấu trúc mới; sửa JS nếu cần, tối thiểu nhất có thể.
4. Trả về: `site ✓` hoặc `site ✗ <lý do>`.
```

## 3.8 `ROUTINE_PROMPT.md` (prompt của routine daily — bản hoàn chỉnh)

```markdown
Bạn là orchestrator của vn-finance-dashboard. Chạy quy trình daily, tối ưu
token: mọi việc làm được bằng script thì chạy script, không tự reasoning lại.

0. `git pull origin main` (nếu có thay đổi mới). Đọc CLAUDE.md.
1. Đọc mục mới nhất của `data/run-log.md` — nếu hôm qua có nguồn lỗi, lưu ý
   cho agent tương ứng trong bước 2.
2. Xác định thứ trong tuần (giờ VN, UTC+7). Spawn SONG SONG:
   - agent-gold
   - agent-fx
   - agent-fuel-gas-check
   - agent-deposit-rates      ← CHỈ nếu là thứ Hai
   - agent-electricity-check  ← CHỈ nếu là thứ Hai
   Agent nào fail thì ghi nhận, KHÔNG chặn agent khác, KHÔNG chạy lại quá 1 lần.
3. Spawn validator. Đọc kết quả flags.
4. Spawn site-builder.
5. Append mục mới vào `data/run-log.md` (format trong CLAUDE.md; giữ ≤30 mục).
6. Commit TẤT CẢ thay đổi trong 1 commit:
   `daily: <YYYY-MM-DD> (gold ✓ fx ✓ fuel – rates skip electricity skip)`
   (✓ = có dữ liệu mới, – = check xong không có gì mới, ✗ = fail, skip = không
   đến lịch). Push `main` (retry 4 lần, backoff 2s/4s/8s/16s).
7. Nếu có agent ✗ hoặc flag: mô tả ngắn trong tin nhắn kết thúc để owner đọc.
   Nếu lỗi là "thiếu domain trong allowlist": nói rõ domain nào cần thêm.

Không được: chạy backfill, sửa dữ liệu lịch sử, đổi schema, force-push.
```

## 3.9 `CLAUDE.md` (bản draft)

```markdown
# vn-finance-dashboard — hướng dẫn cho agent

Dashboard giá cả VN, cập nhật daily 18:05 VN bằng routine. Site tĩnh trên
GitHub Pages, render phía client từ data/*.csv + site/summary.json.

## Nguyên tắc
1. Script-first: chạy scripts/ trước, reasoning chỉ khi script fail.
2. Self-heal: script gãy do trang đổi cấu trúc → parse tay để có dữ liệu hôm
   nay, rồi SỬA SCRIPT + cập nhật ghi chú cấu trúc trang ở mục Nguồn dưới đây,
   commit cùng nhau.
3. Lỗi 403/policy-denied = thiếu domain trong environment allowlist. Không sửa
   script. Báo domain cần thêm. Danh sách allowlist hiện tại: xem cuối file.
4. Dữ liệu thật > dữ liệu đẹp. Không bịa, không copy hôm trước, không sửa
   dòng lịch sử. Trường lấy không được thì để rỗng/null.
5. 1 commit/run. Không force-push. Không đổi schema khi chưa được yêu cầu.

## Schema
(chép nguyên mục "Schema từng file" + "Quy tắc validate" của
docs/plan/02-data-schema-validation.md vào đây khi implement P0 —
đây là bản quy chiếu duy nhất cho agent, kèm 20 mã ngân hàng.)

## Nguồn (cập nhật khi self-heal)
### Vàng
- SJC: https://sjc.com.vn/gia-vang-online — <ghi chú cấu trúc trang, cập nhật lần đầu ở P0>
- DOJI: https://giavang.doji.vn/ — <ghi chú>
### Tỷ giá
- VCB: https://www.vietcombank.com.vn/vi-VN/KHCN/Cong-cu-Tien-ich/Ty-gia — <ghi chú, kèm API nếu tìm thấy>
- SBV: https://dttktt.sbv.gov.vn/TyGia/faces/TyGiaTrungTam.jspx — chập chờn, cho phép null
### Xăng dầu
- Petrolimex TCBC: https://www.petrolimex.com.vn/ndi/thong-cao-bao-chi.html — URL bài theo kỳ đoán được
### Lãi suất
- webgia: https://webgia.com/lai-suat/ — bảng tổng hợp, lọc 20 ngân hàng
### Điện & Gas
- EVN: <URL bài biểu giá hiện hành> — hiện hành QĐ 1279/QĐ-BCT (10/05/2025)
- Gas: vietnambiz.vn bài "Giá gas hôm nay 1/<tháng>"
### Backfill (chỉ dùng trong one-off runs)
- webgia.com/gia-vang/sjc/DD-MM-YYYY.html, webgia.com/ty-gia/vietcombank/DD-MM-YYYY.html,
  webgia.com/gia-xang-dau/petrolimex/, web.archive.org

## Allowlist environment hiện tại
(chép danh sách từ docs/plan/01-sources-and-domains.md, đánh dấu ngày verify
gần nhất. Thêm nguồn mới = thêm ở đây + trong environment settings cùng lúc.)

## Run-log format
(chép từ docs/plan/02.)
```

## 3.10 Cấu hình Routine (làm ở P2)

| Mục | Giá trị |
|---|---|
| Trigger | scheduled, cron `5 11 * * *` (UTC) = 18:05 VN hằng ngày |
| Prompt | nội dung `ROUTINE_PROMPT.md` (file trong repo là bản version-control; prompt routine chỉ ghi: "Đọc và làm theo ROUTINE_PROMPT.md") |
| Environment | custom, allowlist theo [01](01-sources-and-domains.md), unrestricted branch push để commit `main` |
| Session | mới mỗi lần chạy (fresh) |
