# BACKFILL_PROMPTS — chuỗi one-off backfill 2 năm

Mỗi file là 1 one-off routine (chạy 1 lần rồi tự disable, không tính daily cap).
Cấu hình routine chỉ cần trỏ: *"Đọc và làm theo BACKFILL_PROMPTS/run-N-<module>.md"*.

Thứ tự (dễ → khó): `run-1-fx` → `run-2-fuel` → `run-3-gold` → `run-4-gas-dien`
→ `run-5-rates`.

## Quy tắc chung cho MỌI run backfill

1. **Checkpoint** `data/backfill-progress.json`: đọc khi bắt đầu, cập nhật + commit
   sau mỗi lô → run sau (hoặc chạy lại sau khi đứt session) resume đúng chỗ.
2. **Commit theo lô ~2 tháng dữ liệu**, message `backfill(<module>): <từ> → <đến>`.
3. **Lịch sự với nguồn**: tuần tự, delay 1–2s/request, không song song cùng domain.
4. **Provenance**: xong mỗi run, append `data/provenance.md` (khoảng ngày, nguồn, cách lấy).
5. Session hết giờ giữa chừng → không sao, checkpoint đảm bảo resume.
6. Dùng `scripts/backfill_<module>.py` (viết ở P1.1, khuôn giống crawler daily +
   vòng lặp ngày + đọc checkpoint; nhận `--from --to`).
7. Xong module → `python3 scripts/validate.py --full` quét toàn bộ; sửa ERROR bằng
   cách crawl lại đúng ngày đó.

Khoảng backfill mặc định: **2024-07-04 → hôm qua** (điều chỉnh theo ngày chạy).

Cấm: bịa số cho ngày thiếu (để trống + ghi provenance), sửa số đã đúng.
