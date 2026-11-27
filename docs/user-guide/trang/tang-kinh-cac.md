---
id: tang-kinh-cac
title: Trang Tàng Kinh Các (lịch sử báo cáo)
loai: trang
trang: Tàng Kinh Các
he_thong: chung
aliases: [lịch sử, lịch sử báo cáo, history, Thiên Đạo Ký Sơ, danh sách report, danh sách ảnh đã upload]
lien_quan: [tim-bao-cao, xem-chi-tiet-bao-cao, sua-so-lieu-ocr-sai, trang-thai, so-lieu-nao-duoc-hien-thi]
nguon_code: [frontend/html/history.html, frontend/js/history.js]
cap_nhat: 2026-11-20
---
# Trang Tàng Kinh Các (lịch sử báo cáo)

Còn gọi là: lịch sử, lịch sử báo cáo, "Thiên Đạo Ký Sơ", danh sách report.

Trang **Tàng Kinh Các** liệt kê mọi báo cáo đã đọc trong 35 ngày, kể cả báo cáo đã bị ảnh mới hơn thay thế. Từ đây mở chi tiết, xem ảnh gốc, hoặc sang trang sửa số liệu.

## Cách mở trang Tàng Kinh Các

- Bấm mục **"Tàng Kinh Các"** trên thanh menu.
- Bấm link "Tàng Kinh Các" ở cuối tab HT1 hoặc HT2 của trang Thiên Cơ Các.

Tiêu đề trang là **"Thiên Đạo Ký Sơ"**.

## Bố cục trang Tàng Kinh Các

Từ trên xuống:
1. Thanh tìm kiếm: ô **"Truy tìm bí pháp (chung cho cả HT1 và HT2)"**, ô **"Ngày báo cáo từ"**, ô **"đến"**, ô **"Trạng thái"**, nút **"Xóa bộ lọc"**.
2. Hai tab **"HT1 – SCADA"** và **"HT2 – DMWCS (CBS)"**, mỗi tab có số báo cáo bên cạnh.
3. Dòng tóm tắt kết quả tìm, ví dụ "Tìm thấy 5 báo cáo · HT1: 3 · HT2: 2".
4. Danh sách báo cáo, nhóm theo **"Ngày dd/mm/yyyy"**, ngày mới nhất ở trên.

## Các nút và ô nhập trên trang Tàng Kinh Các

| Phần tử | Vị trí | Dùng để | Khi bấm/nhập thì |
| --- | --- | --- | --- |
| Ô **"Truy tìm bí pháp"** | Thanh tìm kiếm, bên trái | Tìm theo một phần tên file ảnh | Tự tìm sau khi ngừng gõ; phần khớp tô vàng |
| Ô **"Ngày báo cáo từ"**, **"đến"** | Thanh tìm kiếm | Lọc theo ngày báo cáo | Tải lại danh sách |
| Ô **"Trạng thái"** | Thanh tìm kiếm | Chọn **"Tất cả"**, **"OK"**, **"Cần kiểm tra"**, **"Đã sửa tay"** | Tải lại danh sách |
| Nút **"Xóa bộ lọc"** | Cuối thanh tìm kiếm | Bỏ mọi điều kiện lọc | Hiện lại toàn bộ danh sách |
| Tab HT1 / HT2 | Dưới thanh tìm kiếm | Chọn hệ thống | Hiện danh sách của hệ thống đó |
| Một dòng báo cáo | Trong danh sách | Mở chi tiết | Hiện ảnh, thông tin, số liệu, cảnh báo |
| Nút **"Xem / sửa số liệu"** | Trong chi tiết, dưới ảnh | Sửa báo cáo | Mở trang Xem / sửa report |
| Ảnh nhỏ trong chi tiết | Bên trái chi tiết | Xem ảnh gốc | Mở ảnh gốc ở tab mới |
| Nút **"Tải thêm (còn N)"** | Cuối danh sách | Xem thêm báo cáo | Tải thêm 50 báo cáo |

## Dữ liệu hiển thị trên trang Tàng Kinh Các

Mỗi dòng báo cáo gồm: tiêu đề ("SCADA · <dây chuyền>", "Sorted parcels", "Capacity dd/mm → dd/mm", "Scanner (Hours&BcrRate)"), tên file, trạng thái, huy hiệu cảnh báo, huy hiệu **"Đã được thay"** nếu có, và giờ upload.

Chi tiết báo cáo gồm: ảnh đã upload, "Tên file", "Upload lúc", "Model", "Trên dashboard" ("Đang dùng" hoặc "Đã được thay bằng ảnh mới hơn"), số liệu theo loại báo cáo, và danh sách "Cảnh báo".

## Khi trang Tàng Kinh Các không có dữ liệu

- Chưa đăng nhập: hiện **"Chưa Nhập môn, không thể tra cứu Tàng Kinh Các."**
- Chưa có báo cáo nào: hiện **"Thiên Cơ trống rỗng. Hãy tiến hành Nạp Linh Ảnh để khai phá."**, có link sang trang Truyền Pháp Ảnh.
- Bộ lọc không khớp: hiện **"Không có báo cáo nào khớp bộ lọc. Thử bỏ bớt điều kiện hoặc bấm Xóa bộ lọc."**
- Lỗi tải: hiện **"Không tải được lịch sử: …"**.

## Việc thường làm trên trang Tàng Kinh Các

- [Tìm báo cáo](../tac-vu/tim-bao-cao.md)
- [Xem chi tiết một báo cáo và ảnh gốc](../tac-vu/xem-chi-tiet-bao-cao.md)
- [Sửa số liệu bị đọc sai](../tac-vu/sua-so-lieu-ocr-sai.md)
