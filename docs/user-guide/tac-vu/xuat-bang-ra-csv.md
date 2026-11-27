---
id: xuat-bang-ra-csv
title: Xuất bảng chi tiết ra file CSV
loai: tac-vu
trang: Thiên Cơ Các
he_thong: chung
aliases: [xuất Excel, tải bảng về, export CSV, download số liệu, Xuất CSV, lấy số liệu ra Excel]
lien_quan: [dashboard-tab-ht1, dashboard-tab-ht2, loc-dashboard-theo-ngay, loc-theo-day-chuyen]
nguon_code: [frontend/html/index.html, frontend/js/dashboard.js]
cap_nhat: 2026-11-20
---
# Xuất bảng chi tiết ra file CSV

Còn gọi là: xuất Excel, export, tải số liệu về máy, "lấy số liệu ra Excel".

**Kết quả:** máy tải về file CSV có đúng các dòng và cột của bảng đang hiện. Mở được bằng Excel, tiếng Việt không lỗi font.
**Cần có trước:** đã đăng nhập, bảng có dữ liệu.

## Các bước xuất bảng chi tiết ra CSV

1. Mở trang **"Thiên Cơ Các"**, chọn tab **"HT1 – SCADA"** hoặc **"HT2 – DMWCS (CBS)"**.
2. Chọn khoảng ngày (và dây chuyền với HT1) cần xuất.
3. Cuộn xuống **"Bảng chi tiết"** (HT1) hoặc **"Bảng chi tiết theo ngày"** (HT2).
4. Bấm nút **"Xuất CSV"** ở góc trên bên phải khung bảng.
5. Trình duyệt tải về file **h1-table.csv** (HT1) hoặc **h2-table.csv** (HT2).

## Nếu xuất bảng ra CSV không như mong muốn

| Hiện tượng | Nguyên nhân | Cách xử lý |
| --- | --- | --- |
| File chỉ có dòng "Không có dữ liệu trong khoảng ngày đã chọn" | Bảng đang trống | Đổi khoảng ngày rồi xuất lại |
| Số trong Excel có dấu chấm ngăn nghìn, không cộng được | File giữ đúng định dạng hiển thị (ví dụ 75.469) | Dùng Tìm và thay thế trong Excel để bỏ dấu chấm |
| Cột Cảnh báo chỉ có "⚠ 2" hoặc "✓ 0" | File giữ chữ hiển thị, không gồm nội dung cảnh báo | Xem nội dung ở Tàng Kinh Các |
| Không thấy file | Trình duyệt chặn tải xuống | Cho phép tải xuống ở thanh địa chỉ |

## Lưu ý khi xuất bảng ra CSV

- File xuất đúng như bảng đang hiện, kể cả bộ lọc ngày và dây chuyền.
- Tên file luôn cố định. Xuất nhiều lần thì trình duyệt tự thêm số vào tên.
- Biểu đồ không xuất được, chỉ bảng.
