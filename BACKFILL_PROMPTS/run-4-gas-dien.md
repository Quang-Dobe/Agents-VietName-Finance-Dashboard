# Backfill run 4 — Gas + Điện

Đọc `CLAUDE.md` và `BACKFILL_PROMPTS/README.md` trước.

## Gas → `data/utilities/gas.csv` (24 mốc tháng)

Nguồn: bài "Giá gas hôm nay 1/M" của `vietnambiz.vn` mỗi đầu tháng từ 2024-07.
Cột: `effective_month (YYYY-MM), mien_bac, mien_trung, mien_nam, cp_usd_ton`
(đ/bình 12kg). Thiếu tháng nào → thử `tuoitre.vn` / `thoibaotaichinhvietnam.vn`;
vẫn thiếu → để trống + ghi provenance. Dùng `scripts/backfill_gas.py`.

## Điện → `data/utilities/electricity.json` (vài mốc)

Chỉ vài lần đổi biểu giá từ 2024-07. Đã biết: **QĐ 2699/QĐ-BCT** (hiệu lực
~11/10/2024) và **QĐ 1279/QĐ-BCT** (hiệu lực 10/05/2025 — đã có trong file).
Verify + lấy đủ bảng bậc thang cho mốc còn thiếu (2699), thêm phần tử vào mảng
`changes`, giữ sort theo `effective_date`.

Checkpoint + commit. Cập nhật provenance.
