---
name: agent-electricity-check
description: Check thay đổi biểu giá điện EVN, CHỈ chạy thứ Hai (thay đổi rất thưa)
tools: Bash, Read, Write, WebFetch
---

Nhiệm vụ: phát hiện biểu giá điện sinh hoạt mới. Chỉ spawn vào thứ Hai.

1. Đọc `effective_date` mới nhất trong `data/utilities/electricity.json`.
2. Fetch trang biểu giá EVN (URL trong CLAUDE.md mục Nguồn/Điện). So số bậc +
   giá từng bậc với bản mới nhất trong file.
3. Không đổi (trường hợp thường gặp) → trả về `electricity –`, dừng ngay.
4. Có biểu giá mới → append 1 phần tử vào mảng `changes` (đủ: effective_date,
   decision, unit, bảng `tiers[]` đầy đủ 6 bậc). Trả về `electricity ✓ <ngày hiệu lực>`.

Không cần script riêng — thay đổi quá thưa, đọc trực tiếp trang là đủ.
Cấm: sửa các mốc biểu giá cũ trong file.
