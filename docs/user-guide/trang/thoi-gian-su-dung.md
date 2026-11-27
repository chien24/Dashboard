---
id: thoi-gian-su-dung
title: Trang Đạo Vận Chi Lượng (cộng giờ từ file Excel)
loai: trang
trang: Đạo Vận Chi Lượng
he_thong: chung
aliases: [trang thời gian sử dụng, Đạo vận chi lượng, tính giờ Excel, cộng cột F, tổng thời gian file IB, file Inbound, 持续时长, cộng 1h33m40s, tính thời gian chạy máy từ Excel]
lien_quan: [tinh-tong-thoi-gian-tu-file-excel, xem-cong-suat-va-thoi-gian-su-dung, bo-cuc-giao-dien]
nguon_code: [frontend/html/thoi-gian.html, frontend/js/thoi-gian.js]
cap_nhat: 2026-11-21
---
# Trang Đạo Vận Chi Lượng (cộng giờ từ file Excel)

Còn gọi là: trang thời gian sử dụng, trang tính giờ Excel, trang cộng cột F, "tính tổng thời gian file IB".

Trang **Đạo Vận Chi Lượng** cộng cột thời lượng (cột F) của file Excel xuất từ máy chia chọn, ví dụ file "IB 16.xlsx". Kết quả giống công thức Excel cộng các ô dạng "1h33m40s", "2m9s", "10s".

Trang này khác thẻ **"Thời gian sử dụng"** trên trang Thiên Cơ Các. Thẻ trên dashboard tính từ ảnh đã OCR (ALL / Công suất). Trang Đạo Vận Chi Lượng chỉ cộng giờ trong file Excel bạn chọn. Xem [Xem công suất và thời gian sử dụng](../tac-vu/xem-cong-suat-va-thoi-gian-su-dung.md).

## Cách mở trang Đạo Vận Chi Lượng

Bấm mục **"Đạo Vận Chi Lượng"** trên thanh menu, mục cuối cùng. Không cần đăng nhập.

## File Excel dùng được trên trang Đạo Vận Chi Lượng

- Định dạng **.xlsx**. File .xls đời cũ không đọc được.
- Dữ liệu nằm ở sheet đầu tiên, dòng 1 là tiêu đề.
- Cột A là tên thiết bị (ví dụ Inbound-1). Cột F là thời lượng (ví dụ 37m40s, 1h33m40s).
- Ô cột F trống thì bỏ qua.

## Bố cục trang Đạo Vận Chi Lượng

Từ trên xuống:
1. Tiêu đề và mô tả.
2. Vùng viền nét đứt **"Kéo thả file Excel vào đây hoặc bấm để chọn"**.
3. Sau khi chọn file, hiện bốn thẻ chỉ số: **"Tổng thời gian sử dụng"**, **"Số lần chạy"**, **"Số thiết bị"**, **"Trung bình mỗi thiết bị"**.
4. Biểu đồ **"Thời gian theo thiết bị"**: mỗi thiết bị một thanh ngang, số giờ ghi ở cuối thanh. Chọn nhiều file thì thanh chia màu theo từng file, có chú thích màu ở trên.
5. Biểu đồ **"Tổng thời gian theo file"**: mỗi file một cột. Chỉ hiện khi chọn từ 2 file trở lên.
6. Mỗi file một khung: tên file, **"Tổng:"** dạng 202h14m15s và số dòng đã cộng. Bấm **"Chi tiết theo thiết bị"** để mở bảng: thiết bị, số lần, thời gian.

Đưa chuột lên thanh hoặc cột của biểu đồ để xem số giờ chính xác đến giây.

## Dữ liệu trên trang Đạo Vận Chi Lượng có được lưu không

Không. File chỉ đọc trên máy, không gửi lên server, không vào dashboard hay chatbot. Tải lại trang (F5) hoặc chuyển trang là mất kết quả. Muốn xem lại thì chọn file lần nữa. Chọn file mới thì kết quả cũ được thay.

## Thông báo trên trang Đạo Vận Chi Lượng

| Thông báo | Nghĩa | Cách xử lý |
| --- | --- | --- |
| "Đang đọc N file…" | Đang đọc file | Chờ vài giây |
| "Không phải file .xlsx hợp lệ" | File không phải .xlsx, hoặc file hỏng | Mở file bằng Excel, lưu lại dạng .xlsx |
| "Không tìm thấy sheet1 trong file" | File không có sheet dữ liệu | Kiểm tra file có đúng là file xuất từ máy |
| Hộp vàng "Bỏ qua N ô không đúng dạng thời gian" | Có ô cột F không theo dạng giờ-phút-giây | Xem số dòng được liệt kê, sửa trong Excel nếu cần |

## Việc thường làm trên trang Đạo Vận Chi Lượng

- [Tính tổng thời gian sử dụng từ file Excel](../tac-vu/tinh-tong-thoi-gian-tu-file-excel.md)
