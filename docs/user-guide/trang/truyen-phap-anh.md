---
id: truyen-phap-anh
title: Trang Truyền Pháp Ảnh (tải ảnh lên)
loai: trang
trang: Truyền Pháp Ảnh
he_thong: chung
aliases: [trang upload, tải ảnh, Truyền Tống Linh Ảnh, đẩy ảnh lên, trang OCR ảnh, Nạp Linh Ảnh]
lien_quan: [tai-anh-len, chon-loai-anh, theo-doi-tien-do-xu-ly-anh, tai-lai-anh-da-tai-truoc-do, gioi-han-va-quy-tac]
nguon_code: [frontend/html/upload.html, frontend/js/upload.js]
cap_nhat: 2026-11-20
---
# Trang Truyền Pháp Ảnh (tải ảnh lên)

Còn gọi là: trang upload, trang tải ảnh, "Truyền Tống Linh Ảnh", "Nạp Linh Ảnh".

Trang **Truyền Pháp Ảnh** dùng để tải ảnh chụp màn hình báo cáo SCADA hoặc DMWCS lên, để hệ thống đọc số liệu.

## Cách mở trang Truyền Pháp Ảnh

Bấm mục **"Truyền Pháp Ảnh"** trên thanh menu. Tiêu đề trang là **"Truyền Tống Linh Ảnh"**.

## Bố cục trang Truyền Pháp Ảnh

Từ trên xuống:
1. Tiêu đề và mô tả: hỗ trợ ảnh JPG / PNG, nhận nhiều ảnh cùng lúc.
2. Vùng viền nét đứt **"Kéo thả ảnh vào đây hoặc bấm để chọn"**.
3. Hàng điều khiển: ô **"Loại cho tất cả ảnh"**, nút **"Khai Phá Thiên Cơ"**, nút **"Xóa Bỏ Phế Tích"**, gợi ý "Dùng "Thần Niệm" sẽ tốn thêm 1 lần Thiên Cơ lệnh mỗi ảnh."
4. Danh sách ảnh đã chọn. Mỗi ảnh một dòng: ảnh nhỏ, tên file, ô chọn loại riêng, thanh tiến trình, chữ trạng thái, đồng hồ thời gian đã chạy.

## Các nút và ô nhập trên trang Truyền Pháp Ảnh

| Phần tử | Vị trí | Dùng để | Khi bấm/nhập thì |
| --- | --- | --- | --- |
| Vùng **"Kéo thả ảnh vào đây"** | Dưới tiêu đề | Thêm ảnh | Bấm mở hộp chọn file; kéo thả cũng được. Chọn được nhiều ảnh |
| Ô **"Loại cho tất cả ảnh"** | Hàng điều khiển, bên trái | Chọn loại chung | Áp cho mọi ảnh để "Theo lựa chọn chung" |
| Nút **"Khai Phá Thiên Cơ"** | Cạnh ô chọn loại | Bắt đầu gửi ảnh | Gửi lần lượt các ảnh chưa gửi. Mờ đi khi chưa có ảnh mới |
| Nút **"Xóa Bỏ Phế Tích"** | Cạnh nút Khai Phá Thiên Cơ | Dọn danh sách | Xóa danh sách ảnh trên màn hình. Ảnh đã gửi vẫn được xử lý tiếp |
| Ô chọn loại của từng ảnh | Cạnh tên file | Chọn loại riêng cho ảnh đó | Mặc định **"Theo lựa chọn chung"** |
| Link **"Xem / Sửa"** | Sau chữ trạng thái khi xong | Mở báo cáo | Mở trang Xem / sửa report |
| Nút **"OCR lại"** | Khi ảnh trùng | Bắt đọc lại ảnh | Gửi lại ảnh |
| Nút **"Thử lại"** | Khi đọc thất bại | Gửi lại ảnh | Gửi lại ảnh với loại đang chọn |

## Dữ liệu hiển thị trên trang Truyền Pháp Ảnh

Đọc xong, dưới mỗi ảnh hiện khối kết quả:
- Tên loại báo cáo và trạng thái (ok, can_kiem_tra).
- Hộp **"Cảnh báo"** màu vàng nếu có cảnh báo.
- Mục **"Dữ liệu đọc được (N trường lệch)"**: bảng mọi trường số liệu. Trường lệch giữa hai lần đọc tô đỏ. Có trường lệch thì mục này tự mở.

Mỗi ảnh xong còn hiện thông báo nổi ở góc phải dưới.

## Khi trang Truyền Pháp Ảnh không dùng được

Chưa đăng nhập: vùng kéo thả hiện **"Chưa nhập môn, chưa thể truyền ảnh. Hãy thực hiện Nhập Môn ở góc trên bên phải."**, các nút bị mờ. Bấm **"Nhập Môn"** để đăng nhập.

File không phải .jpg, .jpeg, .png, .webp bị bỏ qua, không hiện trong danh sách.

## Việc thường làm trên trang Truyền Pháp Ảnh

- [Tải ảnh báo cáo lên](../tac-vu/tai-anh-len.md)
- [Chọn loại ảnh khi tải lên](../tac-vu/chon-loai-anh.md)
- [Theo dõi tiến độ xử lý ảnh](../tac-vu/theo-doi-tien-do-xu-ly-anh.md)
- [Tải lại ảnh đã tải trước đó](../tac-vu/tai-lai-anh-da-tai-truoc-do.md)
