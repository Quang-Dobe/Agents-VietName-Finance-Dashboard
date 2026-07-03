# Backfill run 2 — Xăng dầu Petrolimex

Đọc `CLAUDE.md` và `BACKFILL_PROMPTS/README.md` trước.

Nhiệm vụ: backfill `data/fuel/history.csv` từ **2024-07-04** đến kỳ mới nhất bằng
`scripts/backfill_fuel.py`.

Nguồn: bảng lịch sử `webgia.com/gia-xang-dau/petrolimex/` (ít trang, mỗi trang
nhiều kỳ điều hành) → ~73 kỳ/2 năm. Cột: `effective_date, ron95, e5ron92, diesel,
dau_hoa` (đồng/lít, vùng 1). `effective_date` = ngày **hiệu lực**, không phải ngày đăng.

Lưu ý chuyển đổi: xăng khoáng RON95 bị thay bằng E10 RON95 từ 06/2026 — cột
`ron95` chứa loại RON95 hiện hành theo từng kỳ; ghi mốc chuyển đổi vào provenance.

Đối chiếu: chọn ngẫu nhiên 3 kỳ, so với bài thông cáo tương ứng trên
`petrolimex.com.vn`. Checkpoint + commit theo lô. Xong: cập nhật provenance +
checkpoint, báo số kỳ.
