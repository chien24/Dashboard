---
id: tinh-tong-thoi-gian-tu-file-excel
title: Tính tổng thời gian sử dụng từ file Excel
loai: tac-vu
trang: Đạo Vận Chi Lượng
he_thong: chung
aliases: [Đạo Vận Chi Lượng, cộng cột F, cộng giờ Excel, tính tổng 1h33m40s, tổng thời gian Inbound, so sánh giờ chạy các ngày, thay công thức LET SUMPRODUCT]
lien_quan: [thoi-gian-su-dung, xem-cong-suat-va-thoi-gian-su-dung]
nguon_code: [frontend/html/thoi-gian.html, frontend/js/thoi-gian.js]
cap_nhat: 2026-11-21
---
# Tính tổng thời gian sử dụng từ file Excel

Còn gọi là: cộng cột F, cộng giờ chạy máy, "tính tổng thời gian file IB".

**Kết quả:** biết tổng giờ của cột F (dạng 202h14m15s), giờ của từng thiết bị, và so sánh giữa các file. Không cần gõ công thức Excel.
**Cần có trước:** file .xlsx xuất từ máy chia chọn, cột A là thiết bị, cột F là thời lượng. Không cần đăng nhập.

## Các bước tính tổng thời gian từ file Excel

1. Bấm mục **"Đạo Vận Chi Lượng"** trên thanh menu.
2. Kéo thả file vào vùng **"Kéo thả file Excel vào đây"**, hoặc bấm vào vùng đó để chọn file. Chọn được nhiều file cùng lúc, ví dụ cả tuần "IB 16.xlsx" đến "IB 20.xlsx".
3. Xem thẻ **"Tổng thời gian sử dụng"**: tổng cột F của mọi file đã chọn.
4. Xem biểu đồ **"Thời gian theo thiết bị"** để biết thiết bị nào chạy lâu nhất.
5. Chọn từ 2 file trở lên thì xem thêm biểu đồ **"Tổng thời gian theo file"** để so các ngày.
6. Tổng của từng file nằm ở khung mang tên file, dòng **"Tổng:"**. Bấm **"Chi tiết theo thiết bị"** để xem bảng.

## Cách trang cộng thời gian

Giống công thức Excel thường dùng: ô thiếu giờ, phút hoặc giây thì phần thiếu tính là 0. Ví dụ "10s" = 0h0m10s, "2m9s" = 0h2m9s. Kết quả ghi dạng giờ-phút-giây, số giờ có thể lớn hơn 24 (ví dụ 202h14m15s).

Trang cộng **toàn bộ** cột F từ dòng 2 đến hết, không chọn được một khoảng dòng.

## Nếu kết quả không như mong muốn

| Hiện tượng | Nguyên nhân | Cách xử lý |
| --- | --- | --- |
| Kết quả mất sau khi tải lại trang | Trang không lưu file | Chọn lại file |
| "Không phải file .xlsx hợp lệ" | File .xls cũ, .csv hoặc file hỏng | Mở bằng Excel, lưu dạng .xlsx rồi chọn lại |
| Tổng khác số tính tay trong Excel | Công thức Excel chỉ cộng một khoảng (ví dụ F2:F34) | Trang cộng cả cột. So với công thức cộng cả cột |
| Hộp vàng "Bỏ qua N ô…" | Ô cột F không đúng dạng giờ-phút-giây | Sửa các dòng được liệt kê trong Excel |
| Kéo thả file mà không thấy gì | File không có đuôi .xlsx nên bị bỏ qua | Đổi sang .xlsx |

## Lưu ý khi tính tổng thời gian từ file Excel

- Số liệu ở trang này không vào dashboard Thiên Cơ Các và chatbot không hỏi được.
- Chọn hơn 7 file thì biểu đồ thiết bị gộp mọi file thành một màu.
