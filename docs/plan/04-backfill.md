# 04 — Backfill 2 năm (chuỗi one-off runs)

Khoảng backfill: **04/07/2024 → 03/07/2026** (điều chỉnh theo ngày chạy thật).
One-off routine chạy 1 lần rồi tự disable, không tính vào daily cap.

## Quy tắc chung cho MỌI run backfill

1. **Checkpoint**: đọc `data/backfill-progress.json` khi bắt đầu, cập nhật sau mỗi lô, commit theo lô → run sau (hoặc chạy lại sau khi đứt session) resume đúng chỗ.

```json
{"fx": {"done_until": "2025-03-14", "status": "in_progress"},
 "gold": {"status": "pending"}}
```

2. **Commit theo lô ~2 tháng dữ liệu/commit**, message: `backfill(fx): 2024-07 → 2024-08`.
3. **Lịch sự với nguồn**: tuần tự, delay 1–2s giữa request, không song song hóa request vào cùng domain.
4. **Provenance**: xong mỗi run, append vào `data/provenance.md`: khoảng ngày, nguồn, ngày chạy.
5. Session hết giờ/limit giữa chừng → không sao: checkpoint + commit lô đã đảm bảo resume. Phần còn lại chạy tiếp bằng một one-off run nữa hoặc Claude Code local.
6. Backfill dùng script `scripts/backfill_<module>.py` (viết ở P0, cùng kiểu với script daily): script nhận `--from --to`, tự đọc checkpoint.
7. Sau khi module xong: chạy `scripts/validate.py --module <m> --full` quét toàn bộ lịch sử, sửa các dòng ERROR bằng cách crawl lại đúng ngày đó.

## Run 1 — Tỷ giá VCB (dễ nhất, làm trước để dò quy trình)

- **Prompt one-off:**
  > Đọc CLAUDE.md và docs/plan/04-backfill.md. Backfill module fx từ 2024-07-04 đến hôm qua bằng `scripts/backfill_fx.py`. Thứ tự nguồn: (1) thử API/tra cứu theo ngày của Vietcombank — nếu lấy được JSON theo ngày thì dùng; (2) fallback `webgia.com/ty-gia/vietcombank/DD-MM-YYYY.html`. Cột: vcb_buy_cash, vcb_buy_transfer, vcb_sell; sbv_central để rỗng cho giai đoạn backfill. Checkpoint + commit theo lô 2 tháng. Xong thì cập nhật provenance.md và backfill-progress.json, báo cáo số dòng.
- ~730 trang nếu đi đường webgia. Nếu 1 session không đủ → run 1b resume.

## Run 2 — Xăng dầu (nguồn gọn nhất)

- **Prompt:** tương tự run 1, module fuel. Nguồn: bảng lịch sử `webgia.com/gia-xang-dau/petrolimex/` (ít trang, mỗi trang nhiều kỳ) → ~73 kỳ. Đối chiếu xác suất: chọn ngẫu nhiên 3 kỳ, so với bài thông cáo tương ứng trên petrolimex.com.vn.
- Ghi `effective_date` theo ngày hiệu lực trong nguồn, không phải ngày đăng bài.

## Run 3 + 3b — Vàng (nặng nhất về số trang)

- **Prompt:** module gold, nguồn `webgia.com/gia-vang/sjc/DD-MM-YYYY.html` và pattern tương ứng cho DOJI (xác định pattern DOJI ngay đầu run bằng cách thử 2-3 URL; nếu webgia không có lịch sử DOJI theo ngày thì DOJI để rỗng cho phần backfill và ghi rõ vào provenance).
- ~730 ngày × 2 hãng. Dự kiến **2 run** (3: năm 2024-07→2025-06; 3b: 2025-07→nay). Cuối cùng đối chiếu 5 ngày ngẫu nhiên với biểu đồ `sjc.com.vn/bieu-do-gia-vang`.

## Run 4 — Gas + Điện (ít mốc)

- **Gas:** 24 mốc tháng. Nguồn: bài "Giá gas hôm nay 1/M" của vietnambiz.vn (search nội bộ site hoặc URL pattern từ CLAUDE.md). Thiếu tháng nào → thử tuoitre.vn / thoibaotaichinhvietnam.vn; vẫn thiếu thì để trống và ghi chú.
- **Điện:** chỉ vài mốc thay đổi biểu giá từ 07/2024 (đã biết: QĐ 2699/QĐ-BCT hiệu lực 11/10/2024, QĐ 1279/QĐ-BCT hiệu lực 10/05/2025 — verify + lấy đủ bảng bậc trong run). Ghi thẳng vào `electricity.json`.

## Run 5 — Lãi suất (khó nhất, chấp nhận partial)

- **Prompt:** module deposit-rates. Nguồn: snapshot Wayback Machine của `webgia.com/lai-suat/` (API: `web.archive.org/cdx/search/cdx?url=webgia.com/lai-suat/&from=20240701&to=20260703&output=json`), lấy **1 snapshot/tháng** (không cần tuần cho quá khứ — ghi rõ trong provenance là độ phân giải tháng). Parse bảng như crawl_rates.py. Snapshot hỏng/thiếu → bỏ qua tháng đó.
- Kỳ vọng thực tế: có được 50–80% số tháng là thành công. Chuỗi tuần đầy đủ bắt đầu từ khi daily routine chạy.

## Thứ tự & điều kiện dừng

```
Run 1 (fx) → Run 2 (fuel) → Run 3, 3b (gold) → Run 4 (gas+điện) → Run 5 (rates)
```

Sau mỗi run: mở site local (hoặc Pages) xem trang chi tiết module đó vẽ được biểu đồ 2 năm chưa. Toàn bộ xong → xóa `backfill-progress.json`, gắn tag `backfill-complete`.

## File `BACKFILL_PROMPTS/`

Khi implement P0, tạo `BACKFILL_PROMPTS/run-1-fx.md` … `run-5-rates.md`, mỗi file = prompt ở trên + nhắc quy tắc chung (mục đầu file này). One-off routine chỉ cần trỏ: "Đọc và làm theo BACKFILL_PROMPTS/run-N-<module>.md".
