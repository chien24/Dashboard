---
id: loc-theo-day-chuyen
title: Lọc số liệu HT1 theo dây chuyền
loai: tac-vu
trang: Thiên Cơ Các
he_thong: HT1
aliases: [chọn dây chuyền, lọc dây chuyền, xem riêng Outbound, xem riêng Inbound, xem riêng CBS, line]
lien_quan: [dashboard-tab-ht1, so-sanh-cac-day-chuyen, loc-dashboard-theo-ngay, chi-so-ht1-scada]
nguon_code: [frontend/html/index.html, frontend/js/dashboard.js]
cap_nhat: 2026-11-20
---
# Lọc số liệu HT1 theo dây chuyền

Còn gọi là: chọn dây chuyền, xem riêng một line, "xem riêng Outbound", "xem riêng CBS2".

**Kết quả:** thẻ chỉ số, biểu đồ "Sản lượng theo ngày", "REJECT theo loại" và "Bảng chi tiết" chỉ còn số của một dây chuyền.
**Cần có trước:** đã đăng nhập, đã có ảnh SCADA của dây chuyền đó.

## Các bước lọc số liệu HT1 theo dây chuyền

1. Mở trang **"Thiên Cơ Các"**, tab **"HT1 – SCADA"**.
2. Ở hàng lọc đầu tab, bấm ô **"Dây chuyền"** (bên phải hai ô ngày).
3. Chọn tên dây chuyền. Chọn **"Tất cả"** để xem tổng mọi dây chuyền.
4. Dòng "Chỉ số ngày …" đổi thành tên dây chuyền đã chọn. Thẻ và biểu đồ vẽ lại.

## Nếu lọc theo dây chuyền không như mong muốn

| Hiện tượng | Nguyên nhân | Cách xử lý |
| --- | --- | --- |
| Không thấy dây chuyền cần tìm trong danh sách | Chưa có ảnh SCADA nào của dây chuyền đó | Tải ảnh của dây chuyền đó lên |
| Thấy hai tên gần giống nhau | Tên trên ảnh khác nhau (ví dụ thêm khoảng trắng) | Báo người quản trị. Chữ hoa/thường khác nhau thì đã được gộp làm một |
| Biểu đồ "So sánh 4 dây chuyền" vẫn hiện mọi dây chuyền | Biểu đồ này luôn so sánh tất cả | Đúng thiết kế |

## Lưu ý khi lọc theo dây chuyền

- Tên dây chuyền hiển thị đúng như hệ thống đọc được trên ảnh. "CBs2" và "CBS2" được coi là cùng một dây chuyền.
- Chọn **"Tất cả"**: thẻ "Công suất MAX" và "Thời gian sử dụng" là tổng các dây chuyền, kèm danh sách từng dây chuyền.
- Chọn một dây chuyền: thẻ "Công suất MAX" ghi khung giờ đạt MAX.
- Tab HT2 không có lọc dây chuyền, vì máy CBS không chia dây chuyền.
