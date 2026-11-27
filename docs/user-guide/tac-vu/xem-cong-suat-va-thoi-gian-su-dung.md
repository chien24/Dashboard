---
id: xem-cong-suat-va-thoi-gian-su-dung
title: Xem công suất và thời gian sử dụng
loai: tac-vu
trang: Thiên Cơ Các
he_thong: chung
aliases: [công suất MAX, công suất AVG, capacity, biểu đồ công suất, thời gian sử dụng, số giờ chạy máy, giờ vận hành]
lien_quan: [tinh-tong-thoi-gian-tu-file-excel, dashboard-tab-ht1, dashboard-tab-ht2, chi-so-ht1-scada, chi-so-ht2-dmwcs, so-lieu-nao-duoc-hien-thi]
nguon_code: [frontend/html/index.html, frontend/js/dashboard.js]
cap_nhat: 2026-11-20
---
# Xem công suất và thời gian sử dụng

Còn gọi là: biểu đồ công suất, capacity, công suất AVG, công suất MAX, số giờ chạy máy.

**Kết quả:** biết công suất (bưu kiện/giờ) và số giờ máy chạy ước tính mỗi ngày.
**Cần có trước:** đã đăng nhập. HT1 cần ảnh SCADA. HT2 cần ảnh Capacity, và cả ảnh Sorted để tính thời gian sử dụng.

## Các bước xem công suất và thời gian sử dụng của HT1

1. Mở trang **"Thiên Cơ Các"**, tab **"HT1 – SCADA"**.
2. Xem thẻ **"Công suất MAX"** và **"Thời gian sử dụng"** ở đầu tab, cho ngày đang chọn.
3. Muốn xem theo ngày và theo dây chuyền: ở khung **"So sánh 4 dây chuyền"**, chọn **"Công suất MAX"** hoặc **"Thời gian sử dụng (h)"**.
4. "Bảng chi tiết" có cột Công suất MAX, Khung giờ MAX, Thời gian sử dụng cho từng dây chuyền.

## Các bước xem công suất và thời gian sử dụng của HT2

1. Mở trang **"Thiên Cơ Các"**, tab **"HT2 – DMWCS (CBS)"**.
2. Xem thẻ **"Công suất AVG"** và **"Thời gian sử dụng"** ở đầu tab.
3. Xem khung **"Công suất AVG theo ngày"**: đường nối công suất trung bình mỗi ngày.
4. Xem khung **"Thời gian sử dụng (h)"**: cột số giờ mỗi ngày, có in số trên đầu cột.

## Nếu không thấy công suất hoặc thời gian sử dụng

| Hiện tượng | Nguyên nhân | Cách xử lý |
| --- | --- | --- |
| HT2 "Công suất AVG" là "—" | Chưa có ảnh Capacity chứa ngày đó | Tải ảnh Capacity lên |
| HT2 có công suất nhưng "Thời gian sử dụng" là "—" | Ngày đó thiếu ảnh Sorted (cần ALL) | Tải ảnh Sorted lên |
| HT1 không có Công suất AVG | Màn hình SCADA không có chỉ số này | Đúng thiết kế |

## Lưu ý khi xem công suất và thời gian sử dụng

- HT1: Thời gian sử dụng = ALL / Công suất MAX. Đây là ước tính, thời gian thực tế lớn hơn hoặc bằng số này.
- HT1 lọc "Tất cả": thẻ là tổng các dây chuyền, vì mỗi dây chuyền đạt MAX ở khung giờ khác nhau.
- HT2: Thời gian sử dụng = ALL / Công suất AVG cùng ngày.
- Cần cộng giờ thật từ file Excel xuất từ máy (cột dạng 1h33m40s) thì dùng trang "Đạo Vận Chi Lượng". Xem [Tính tổng thời gian từ file Excel](tinh-tong-thoi-gian-tu-file-excel.md).
- Một ảnh Capacity chứa nhiều ngày. Nhiều ảnh cùng có một ngày thì không cộng, chỉ lấy một giá trị. Xem [Số nào được hiển thị](../tham-chieu/so-lieu-nao-duoc-hien-thi.md).
