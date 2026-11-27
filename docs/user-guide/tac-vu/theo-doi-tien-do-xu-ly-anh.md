---
id: theo-doi-tien-do-xu-ly-anh
title: Theo dõi tiến độ xử lý ảnh và xem kết quả
loai: tac-vu
trang: Truyền Pháp Ảnh
he_thong: chung
aliases: [tiến độ OCR, thanh tiến trình, ảnh đang xử lý, chờ bao lâu, trạng thái ảnh, xem kết quả đọc ảnh]
lien_quan: [tai-anh-len, trang-thai, canh-bao-so-lieu, ocr-that-bai, mat-ket-noi-may-chu]
nguon_code: [frontend/js/upload.js, backend/app/services/worker.py, backend/app/ocr/pipeline.py]
cap_nhat: 2026-11-20
---
# Theo dõi tiến độ xử lý ảnh và xem kết quả

Còn gọi là: tiến độ OCR, thanh tiến trình, "upload xong phải chờ bao lâu", "xem tiến độ ở đâu".

**Kết quả:** biết mỗi ảnh đang ở bước nào, xong thì xem được số liệu đọc được và cảnh báo.
**Cần có trước:** đã bấm **"Khai Phá Thiên Cơ"** trên trang **"Truyền Pháp Ảnh"**.

## Các bước theo dõi tiến độ xử lý ảnh

1. Giữ trang **"Truyền Pháp Ảnh"** mở. Mỗi ảnh có thanh tiến trình, chữ trạng thái và đồng hồ phút:giây.
2. Chữ trạng thái đổi lần lượt: **"Đang gửi ảnh…"** → **"Đang chờ tới lượt"** → **"Đang OCR · …"**. Phần sau dấu chấm cho biết bước đang chạy, ví dụ "đang nhận diện loại ảnh" hoặc "lần 1/2", "lần 2/2".
3. Xong, thanh tiến trình đầy và đổi màu. Chữ trạng thái thành một trong các kết quả ở bảng dưới.
4. Dưới ảnh hiện khối kết quả: tên loại báo cáo, trạng thái, hộp **"Cảnh báo"** (nếu có), mục **"Dữ liệu đọc được (N trường lệch)"**.
5. Bấm **"Xem / Sửa"** để mở trang sửa số liệu của báo cáo.

## Ý nghĩa kết quả trên trang Truyền Pháp Ảnh

| Chữ trạng thái | Nghĩa là |
| --- | --- |
| **"✓ Thành công · Xem / Sửa"** | Hai lần đọc khớp, số học đúng. Thanh màu xanh |
| **"✓ Xong, cần kiểm tra · Xem / Sửa"** | Đọc xong nhưng có cảnh báo, nên so lại với ảnh. Thanh màu vàng |
| **"Ảnh đã được xử lý trước đó"** | Ảnh trùng, đang hiện kết quả cũ |
| **"✕ Thất bại"** | Không đọc được ảnh. Thanh màu đỏ |

Trong mục "Dữ liệu đọc được", dòng tô đỏ là trường lệch giữa hai lần đọc. Có trường lệch thì mục này tự mở.

## Nếu theo dõi tiến độ gặp vấn đề

| Hiện tượng | Nguyên nhân | Cách xử lý |
| --- | --- | --- |
| Đứng lâu ở "Đang chờ tới lượt" | Đang có ảnh khác trong hàng đợi | Chờ thêm; ảnh xử lý lần lượt từng cái |
| "Mất kết nối tới server: …" | Mạng chập chờn khi đang theo dõi | Xem kết quả ở Tàng Kinh Các sau ít phút. Xem [lỗi mất kết nối](../loi/mat-ket-noi-may-chu.md) |
| Lỡ đóng trang khi đang chờ | Trang không theo dõi được nữa | Ảnh vẫn được xử lý; mở Tàng Kinh Các để xem |

## Lưu ý khi theo dõi tiến độ xử lý ảnh

- Thời gian xử lý mỗi ảnh không cố định: tùy tốc độ mạng, dịch vụ đọc ảnh và số ảnh đang chờ trước đó.
- Mỗi ảnh đọc 2 lần, nên "lần 1/2" rồi "lần 2/2". Dùng "Thần Niệm" thì có thêm bước nhận diện loại.
- Thanh tiến trình là ước lượng, không phải thời gian chính xác.
- Máy chủ khởi động lại khi đang xử lý thì ảnh dở dang được chạy lại từ đầu.
