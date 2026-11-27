---
id: tim-bao-cao
title: Tìm báo cáo ở Tàng Kinh Các
loai: tac-vu
trang: Tàng Kinh Các
he_thong: chung
aliases: [tìm report, tìm ảnh đã upload, tra cứu báo cáo, lọc báo cáo, Truy tìm bí pháp, tìm theo tên file, báo cáo cần kiểm tra]
lien_quan: [tang-kinh-cac, xem-chi-tiet-bao-cao, trang-thai, sua-so-lieu-ocr-sai]
nguon_code: [frontend/html/history.html, frontend/js/history.js, backend/app/api/reports.py]
cap_nhat: 2026-11-20
---
# Tìm báo cáo ở Tàng Kinh Các

Còn gọi là: tìm report, tra cứu báo cáo, "tìm ảnh đã upload", "xem các báo cáo cần kiểm tra".

**Kết quả:** danh sách chỉ còn các báo cáo khớp điều kiện. Dòng tóm tắt ghi "Tìm thấy N báo cáo · HT1: a · HT2: b".
**Cần có trước:** đã đăng nhập.

## Các bước tìm báo cáo

1. Bấm menu **"Tàng Kinh Các"**.
2. Gõ một phần tên file ảnh vào ô **"Truy tìm bí pháp (chung cho cả HT1 và HT2)"**, ví dụ "Screenshot 2026-11-16" hoặc "3.jpg". Không phân biệt chữ hoa, chữ thường.
3. Danh sách tự cập nhật sau khi ngừng gõ. Phần tên file khớp được tô vàng.
4. Lọc thêm theo ngày báo cáo: chọn ô **"Ngày báo cáo từ"** và **"đến"**.
5. Lọc theo trạng thái: chọn ô **"Trạng thái"** là **"OK"**, **"Cần kiểm tra"** hoặc **"Đã sửa tay"**.
6. Xem kết quả ở tab **"HT1 – SCADA"** hoặc **"HT2 – DMWCS (CBS)"**. Số trên mỗi tab là số báo cáo khớp.
7. Bỏ mọi điều kiện: bấm **"Xóa bộ lọc"**.

## Nếu tìm báo cáo không ra

| Hiện tượng | Nguyên nhân | Cách xử lý |
| --- | --- | --- |
| "Không có báo cáo nào khớp bộ lọc. Thử bỏ bớt điều kiện hoặc bấm Xóa bộ lọc." | Điều kiện quá chặt | Bỏ bớt điều kiện, bấm "Xóa bộ lọc" |
| Tab đang xem trống, tab kia có kết quả | Báo cáo thuộc hệ thống kia | Trang tự chuyển sang tab có kết quả |
| Không tìm thấy ảnh cũ | Ngày báo cáo đã quá 35 ngày, đã bị xóa | Không khôi phục được |
| "Chưa Nhập môn, không thể tra cứu Tàng Kinh Các." | Chưa đăng nhập | Bấm "Nhập Môn" |

## Lưu ý khi tìm báo cáo

- Ô tìm kiếm chỉ tìm theo tên file ảnh, không tìm theo số liệu hay tên dây chuyền.
- Lọc ngày theo **ngày báo cáo** ghi trên ảnh, không phải ngày tải ảnh lên.
- Báo cáo Capacity có ngày báo cáo là ngày cuối của khoảng truy vấn trên ảnh.
- Danh sách tải 50 báo cáo mỗi lần. Bấm **"Tải thêm (còn N)"** ở cuối danh sách để xem tiếp.
- Danh sách gồm cả báo cáo đã bị ảnh mới hơn thay (nhãn "Đã được thay").
