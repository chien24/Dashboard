---
id: khong-nhan-dien-duoc-loai-man-hinh
title: Lỗi "Không nhận diện được loại màn hình. Hãy chọn loại khi upload."
loai: loi
trang: Truyền Pháp Ảnh
he_thong: chung
aliases: [không nhận diện được loại ảnh, Thần Niệm lỗi, tự nhận diện thất bại, không biết loại ảnh]
lien_quan: [chon-loai-anh, tai-anh-len, ocr-that-bai]
nguon_code: [frontend/js/upload.js, backend/app/ocr/classify.py]
cap_nhat: 2026-11-20
---
# Lỗi "Không nhận diện được loại màn hình. Hãy chọn loại khi upload."

Còn gọi là: tự nhận diện thất bại, Thần Niệm lỗi, "không biết ảnh loại gì".

**Xuất hiện ở:** trang **"Truyền Pháp Ảnh"**, khi để loại ảnh là **"Thần Niệm (tự nhận diện)"**. Dòng ảnh hiện **"✕ Thất bại"**, khối đỏ ghi "Không đọc được ảnh này. Không nhận diện được loại màn hình. Hãy chọn loại khi upload."

**Nghĩa là:** hệ thống không đoán được ảnh là SCADA, DMWCS Sorted, DMWCS Capacity hay DMWCS BCR rate.

**Nguyên nhân thường gặp:**
- Ảnh chụp thiếu phần tiêu đề của màn hình báo cáo.
- Ảnh không phải một trong bốn loại màn hình báo cáo.
- Ảnh mờ, nhỏ, hoặc bị che.

**Cách xử lý:**
1. Ở dòng ảnh bị lỗi, bấm ô chọn loại cạnh tên ảnh. Ô này mở lại được sau khi thất bại.
2. Chọn đúng loại: **"SCADA"**, **"DMWCS Sorted"**, **"DMWCS Capacity"** hoặc **"DMWCS BCR rate"**.
3. Bấm **"Thử lại"** trong khối đỏ.

Lần sau, chọn loại sẵn ở ô **"Loại cho tất cả ảnh"** trước khi bấm "Khai Phá Thiên Cơ". Cách này còn tiết kiệm một lượt đọc mỗi ảnh. Xem [Chọn loại ảnh](../tac-vu/chon-loai-anh.md).

**Nếu vẫn lỗi:** chọn đúng loại mà vẫn thất bại thì xem [lỗi OCR thất bại](ocr-that-bai.md), hoặc báo người hỗ trợ ở mục **"Gặp Kiếp Nạn"** cuối trang.
