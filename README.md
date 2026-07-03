# vn-finance-dashboard

Dashboard thị trường & tài chính Việt Nam, cập nhật **mỗi ngày** bằng Claude Code Routine.

Theo dõi 5 nhóm dữ liệu:

| Nhóm | Nội dung | Tần suất |
|---|---|---|
| 🥇 Vàng | Giá SJC, DOJI (mua/bán) | Hằng ngày |
| 💵 Tỷ giá | USD/VND tại VCB + tỷ giá trung tâm SBV | Hằng ngày |
| ⛽ Xăng dầu | RON95, E5 RON92, dầu diesel, dầu hỏa | Theo kỳ điều hành (~10 ngày) |
| 🏦 Lãi suất | Tiết kiệm ~20 ngân hàng, kỳ hạn 1–24 tháng | Hằng tuần (thứ Hai) |
| ⚡ Điện & Gas | Biểu giá điện EVN + gas bình 12kg | Khi có thay đổi |

## Trạng thái

- [x] Detail plan — xem [`docs/plan/`](docs/plan/00-overview.md)
- [ ] Skeleton repo (scripts, site, CLAUDE.md, agents)
- [ ] Backfill 2 năm dữ liệu lịch sử (6 one-off runs)
- [ ] Bật routine daily 18h VN
- [ ] GitHub Pages live

## Tài liệu

- **Kế hoạch chi tiết**: [`docs/plan/00-overview.md`](docs/plan/00-overview.md)
- **Brief gốc**: [`docs/brief.md`](docs/brief.md)
- **Cách hoạt động** (dành cho người xem dashboard): sẽ có tại `site/docs.html`
