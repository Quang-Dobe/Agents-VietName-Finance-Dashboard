# ROUTINE_PROMPT — daily run

> Prompt của routine daily (version-control tại đây). Cấu hình routine chỉ cần
> trỏ: *"Đọc và làm theo ROUTINE_PROMPT.md trong repo."*

Bạn là orchestrator của vn-finance-dashboard. Chạy quy trình daily, **tối ưu
token**: việc gì làm được bằng script thì chạy script, đừng reasoning lại.

1. `git pull origin main`. Đọc `CLAUDE.md`. Đọc mục mới nhất của
   `data/run-log.md` — nếu hôm qua có nguồn lỗi, lưu ý cho agent tương ứng.
2. Xác định thứ trong tuần theo giờ VN (UTC+7). Spawn **song song**:
   - `agent-gold`
   - `agent-fx`
   - `agent-fuel-gas-check`
   - `agent-deposit-rates`      ← CHỈ nếu hôm nay là **thứ Hai**
   - `agent-electricity-check`  ← CHỈ nếu hôm nay là **thứ Hai**

   Agent nào fail thì ghi nhận, **KHÔNG chặn** agent khác, KHÔNG chạy lại quá 1
   lần. Nếu agent báo "thiếu domain" → ghi rõ domain đó để báo owner ở bước 7.
3. Spawn `validator`. Đọc kết quả flags.
4. Spawn `site-builder`.
5. Append 1 mục mới vào `data/run-log.md` (format trong CLAUDE.md; giữ ≤30 mục,
   xóa mục cũ nhất nếu vượt).
6. Commit TẤT CẢ thay đổi trong **1 commit**:
   `daily: <YYYY-MM-DD> (gold ✓ fx ✓ fuel – rates skip electricity skip)`
   (✓ có dữ liệu mới · – check không có gì mới · ✗ fail · skip không đến lịch).
   Push branch của routine, retry 4 lần backoff 2s/4s/8s/16s nếu lỗi mạng.
7. Harness tự tạo PR sang `main` ở dạng **draft** sau khi push — luôn gọi
   `update_pull_request` với `draft: false` ngay sau khi PR được tạo để chuyển
   sang "ready for review". Đây là bước bắt buộc: workflow
   `.github/workflows/auto-merge.yml` chỉ merge PR không-draft, PR còn ở dạng
   draft sẽ đứng yên mãi mãi.
8. Kết thúc: nếu có agent ✗, flag, hoặc thiếu domain → mô tả ngắn gọn cho owner
   (nêu rõ domain nào cần thêm vào allowlist). Không có gì bất thường → 1 dòng
   xác nhận là đủ.

Cấm: chạy backfill, sửa dữ liệu lịch sử, đổi schema, force-push, bịa số liệu.
