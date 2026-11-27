---
id: file-khong-phai-anh
title: Lỗi "File không phải ảnh hợp lệ"
loai: loi
trang: Truyền Pháp Ảnh
he_thong: chung
aliases: [file hỏng, ảnh hỏng, sai định dạng, Chỉ nhận ảnh, không phải ảnh, file không hợp lệ, không chọn được file]
lien_quan: [tai-anh-len, gioi-han-va-quy-tac, anh-qua-dung-luong]
nguon_code: [frontend/js/upload.js, backend/app/api/upload.py]
cap_nhat: 2026-11-20
---
# Lỗi "File không phải ảnh hợp lệ"

Còn gọi là: ảnh hỏng, sai định dạng, "Chỉ nhận ảnh .jpg, .jpeg, .png, .webp".

**Xuất hiện ở:** trang **"Truyền Pháp Ảnh"**, sau khi bấm **"Khai Phá Thiên Cơ"**. Dòng ảnh hiện **"✕ Thất bại"** kèm "File không phải ảnh hợp lệ: <tên file>" hoặc "Chỉ nhận ảnh .jpg, .jpeg, .png, .webp: <tên file>".

**Nghĩa là:** file có đuôi giống ảnh nhưng nội dung không phải ảnh, hoặc ảnh bị hỏng, nên hệ thống không mở được.

**Nguyên nhân thường gặp:**
- File tải về chưa xong, hoặc bị lỗi khi chép.
- File thật ra là PDF, Word hay ảnh HEIC, nhưng bị đổi đuôi thành .jpg.
- Ảnh được dán vào file khác rồi lưu sai.

**Cách xử lý:**
1. Mở thử file bằng trình xem ảnh của Windows. Không mở được thì file đã hỏng.
2. Chụp lại màn hình báo cáo, lưu dạng PNG hoặc JPG.
3. Tải ảnh mới lên và bấm **"Khai Phá Thiên Cơ"**.

**Lưu ý:** file có đuôi khác .jpg, .jpeg, .png, .webp (ví dụ .pdf, .heic, .bmp) không báo lỗi mà bị bỏ qua: không hiện trong danh sách ảnh. Đổi sang JPG hoặc PNG trước khi tải lên.

**Nếu vẫn lỗi:** báo người hỗ trợ ở mục **"Gặp Kiếp Nạn"** cuối trang, gửi kèm file ảnh.
