---
id: ocr-that-bai
title: Lỗi "OCR thất bại" / "Không đọc được ảnh này."
loai: loi
trang: Truyền Pháp Ảnh
he_thong: chung
aliases: [OCR lỗi, đọc ảnh thất bại, Thất bại, Không đọc được ảnh này, Tất cả provider/model đều lỗi, upload xong không thấy số liệu]
lien_quan: [tai-anh-len, chon-loai-anh, khong-nhan-dien-duoc-loai-man-hinh, ocr-lai-bao-cao, anh-qua-dung-luong]
nguon_code: [frontend/js/upload.js, frontend/js/report.js, backend/app/ocr/router.py, backend/app/services/worker.py]
cap_nhat: 2026-11-20
---
# Lỗi "OCR thất bại" / "Không đọc được ảnh này."

Còn gọi là: đọc ảnh thất bại, OCR lỗi, "upload xong mà không thấy số liệu".

**Xuất hiện ở:** trang **"Truyền Pháp Ảnh"**: dòng ảnh hiện **"✕ Thất bại"**, khối đỏ ghi **"Không đọc được ảnh này."** kèm lý do; góc phải dưới hiện thông báo đỏ **"OCR thất bại: <tên file>"**. Ở trang **Xem / sửa report**, khi bấm nút "OCR lại", lý do hiện bằng chữ đỏ cạnh nút.

**Nghĩa là:** hệ thống không đọc được số liệu từ ảnh. Không có báo cáo mới nào được tạo, dashboard không đổi.

**Nguyên nhân thường gặp:**
- Lý do bắt đầu bằng **"Tất cả provider/model đều lỗi: …"**: mọi nguồn đọc ảnh đều lỗi, hết lượt dùng trong ngày, hoặc đang tạm nghỉ. Phần sau liệt kê lỗi của từng nguồn.
- Chọn sai loại ảnh, nên kết quả đọc không khớp mẫu báo cáo.
- "Không nhận diện được loại màn hình. Hãy chọn loại khi upload.": xem [lỗi này](khong-nhan-dien-duoc-loai-man-hinh.md).
- Ảnh mờ, bị che, hoặc không phải màn hình báo cáo.
- Ảnh quá lớn hoặc hỏng: xem [ảnh quá dung lượng](anh-qua-dung-luong.md), [file không phải ảnh](file-khong-phai-anh.md).

**Cách xử lý:**
1. Đọc lý do trong khối đỏ.
2. Nếu nghi sai loại: chọn đúng loại ở ô cạnh tên ảnh. Ô này mở lại được sau khi thất bại.
3. Bấm **"Thử lại"** trong khối đỏ.
4. Nếu lỗi "Tất cả provider/model đều lỗi": chờ vài phút tới vài giờ rồi thử lại, vì các nguồn đọc có giới hạn lượt dùng.

**Nếu vẫn lỗi:** chụp màn hình khối lỗi, báo người hỗ trợ ở mục **"Gặp Kiếp Nạn"** cuối trang.
