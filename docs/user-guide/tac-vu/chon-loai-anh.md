---
id: chon-loai-anh
title: Chọn loại ảnh khi tải lên
loai: tac-vu
trang: Truyền Pháp Ảnh
he_thong: chung
aliases: [loại ảnh, Thần Niệm, tự nhận diện, chọn SCADA, chọn DMWCS, chọn sai loại, Loại cho tất cả ảnh]
lien_quan: [tai-anh-len, truyen-phap-anh, khong-nhan-dien-duoc-loai-man-hinh, ocr-that-bai]
nguon_code: [frontend/html/upload.html, frontend/js/upload.js, backend/app/ocr/pipeline.py]
cap_nhat: 2026-11-20
---
# Chọn loại ảnh khi tải lên

Còn gọi là: chọn loại báo cáo, Thần Niệm, tự nhận diện loại ảnh, "hệ thống có tự nhận loại ảnh không".

**Kết quả:** hệ thống đọc ảnh theo đúng mẫu báo cáo đã chọn, ít lỗi hơn và nhanh hơn.
**Cần có trước:** đang ở trang **"Truyền Pháp Ảnh"**, đã thêm ảnh vào danh sách.

## Các loại ảnh trên trang Truyền Pháp Ảnh

| Lựa chọn | Dùng cho ảnh |
| --- | --- |
| **"Thần Niệm (tự nhận diện)"** | Để hệ thống tự đoán loại |
| **"SCADA"** | Màn hình "Thống kê và phân tích dữ liệu" của HT1, một dây chuyền |
| **"DMWCS Sorted"** | Màn hình "The Report of Sorted parcels" của HT2 |
| **"DMWCS Capacity"** | Màn hình "The Report of Capacity" của HT2 (công suất theo ngày) |
| **"DMWCS BCR rate"** | Màn hình Hours&BcrRate của HT2 (bảng tỷ lệ đọc của Scanner) |

## Các bước chọn loại ảnh

1. Chọn loại chung ở ô **"Loại cho tất cả ảnh"**, bên trái nút "Khai Phá Thiên Cơ".
2. Ảnh nào khác loại: chọn loại riêng ở ô cạnh tên ảnh đó. Ô riêng mặc định là **"Theo lựa chọn chung"**.
3. Bấm **"Khai Phá Thiên Cơ"**. Sau khi gửi, ô loại của ảnh đó bị khóa.

## Nếu chọn loại ảnh sai

| Hiện tượng | Nguyên nhân | Cách xử lý |
| --- | --- | --- |
| "✕ Thất bại" với lỗi kiểu dữ liệu | Chọn loại không đúng màn hình trong ảnh | Chọn lại loại đúng ở ô cạnh tên ảnh, bấm **"Thử lại"** |
| "Không nhận diện được loại màn hình. Hãy chọn loại khi upload." | "Thần Niệm" không đoán được | Chọn loại cụ thể rồi bấm "Thử lại". Xem [lỗi này](../loi/khong-nhan-dien-duoc-loai-man-hinh.md) |
| Đọc xong nhưng số vô lý, nhiều cảnh báo | Có thể sai loại | Thêm lại ảnh đó vào danh sách, chọn loại đúng ở ô cạnh tên ảnh, bấm "Khai Phá Thiên Cơ". Ảnh bị báo trùng thì bấm **"OCR lại"** ngay trên dòng đó. Sau đó xóa báo cáo sai ở Tàng Kinh Các |

## Lưu ý khi chọn loại ảnh

- Gợi ý trên trang: "Dùng "Thần Niệm" sẽ tốn thêm 1 lần Thiên Cơ lệnh mỗi ảnh." Nghĩa là tự nhận diện tốn thêm một lượt đọc, chậm hơn một chút.
- Chọn sẵn loại đúng giúp nhanh hơn và tránh đoán nhầm.
- Khi bấm "OCR lại" ở trang Xem / sửa report, hệ thống dùng lại loại của báo cáo cũ, không cần chọn.
