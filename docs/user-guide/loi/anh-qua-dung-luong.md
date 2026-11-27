---
id: anh-qua-dung-luong
title: Lỗi "… lớn hơn 10.0 MB"
loai: loi
trang: Truyền Pháp Ảnh
he_thong: chung
aliases: [ảnh quá lớn, ảnh quá nặng, vượt dung lượng, file quá to, giới hạn 10 MB]
lien_quan: [tai-anh-len, gioi-han-va-quy-tac, ocr-that-bai]
nguon_code: [frontend/js/upload.js, backend/app/api/upload.py, backend/app/config.py]
cap_nhat: 2026-11-20
---
# Lỗi "… lớn hơn 10.0 MB"

Còn gọi là: ảnh quá lớn, ảnh quá nặng, vượt dung lượng.

**Xuất hiện ở:** trang **"Truyền Pháp Ảnh"**, sau khi bấm **"Khai Phá Thiên Cơ"**. Dòng ảnh hiện **"✕ Thất bại"**, khối lỗi ghi "Không đọc được ảnh này." kèm "<tên file> lớn hơn 10.0 MB". Góc phải dưới hiện thông báo đỏ "OCR thất bại: <tên file>".

**Nghĩa là:** ảnh nặng hơn 10 MB, hệ thống không nhận.

**Nguyên nhân thường gặp:**
- Chụp màn hình ở độ phân giải rất cao.
- Ảnh chụp bằng điện thoại, lưu ở chất lượng cao nhất.
- Lưu ảnh dạng PNG với màn hình lớn.

**Cách xử lý:**
1. Mở ảnh bằng Paint hoặc công cụ chỉnh ảnh.
2. Lưu lại dạng JPG, hoặc giảm kích thước ảnh. Chữ số trên ảnh vẫn phải đọc rõ.
3. Ở trang Truyền Pháp Ảnh, kéo thả ảnh mới vào và bấm **"Khai Phá Thiên Cơ"**.

Không nên cắt bớt ảnh, vì hệ thống cần đủ các ô số liệu và ô thời gian của báo cáo.

**Nếu vẫn lỗi:** báo người hỗ trợ ở mục **"Gặp Kiếp Nạn"** cuối trang. Giới hạn 10 MB là mặc định, người quản trị có thể đổi.
