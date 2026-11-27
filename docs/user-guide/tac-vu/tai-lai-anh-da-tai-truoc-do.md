---
id: tai-lai-anh-da-tai-truoc-do
title: Tải lại ảnh đã tải trước đó (ảnh trùng)
loai: tac-vu
trang: Truyền Pháp Ảnh
he_thong: chung
aliases: [ảnh trùng, ảnh đã xử lý trước đó, upload lại, bắt đọc lại, OCR lại ảnh trùng, tải 2 lần cùng ảnh]
lien_quan: [tai-anh-len, ocr-lai-bao-cao, so-lieu-nao-duoc-hien-thi, gioi-han-va-quy-tac]
nguon_code: [frontend/js/upload.js, backend/app/api/upload.py]
cap_nhat: 2026-11-20
---
# Tải lại ảnh đã tải trước đó (ảnh trùng)

Còn gọi là: ảnh trùng, upload lại, "tải lại ảnh cũ thì sao", "muốn bắt đọc lại ảnh".

**Kết quả:** biết ảnh đã có kết quả cũ, hoặc bắt hệ thống đọc lại ảnh đó để có báo cáo mới.
**Cần có trước:** đã đăng nhập, đang ở trang **"Truyền Pháp Ảnh"**.

## Hệ thống nhận ra ảnh trùng thế nào

Ảnh trùng là ảnh có **nội dung giống hệt** ảnh đã tải trước đó, không xét tên file. Đổi tên file vẫn bị coi là trùng. Chụp lại màn hình thì là ảnh mới, không trùng.

Ảnh trùng không được đọc lại tự động, để tránh tốn lượt đọc.

## Các bước khi gặp ảnh trùng

1. Tải ảnh lên như bình thường và bấm **"Khai Phá Thiên Cơ"**.
2. Ảnh trùng hiện chữ vàng **"Ảnh đã được xử lý trước đó · xem kết quả cũ · OCR lại"**. Góc phải dưới hiện thông báo "Ảnh này đã OCR trước đó, đang hiện kết quả cũ."
3. Dưới ảnh hiện luôn kết quả cũ: loại báo cáo, trạng thái, cảnh báo, dữ liệu đã đọc.
4. Muốn xem hoặc sửa kết quả cũ: bấm link **"xem kết quả cũ"**.
5. Muốn bắt đọc lại: bấm nút **"OCR lại"**. Ảnh được gửi lại và đọc như ảnh mới.

## Nếu tải lại ảnh đã tải trước đó gặp vấn đề

| Hiện tượng | Nguyên nhân | Cách xử lý |
| --- | --- | --- |
| Ảnh trùng mà đang hiện tiến trình "Đang OCR" | Lần tải trước của ảnh này vẫn đang xử lý dở | Chờ; trang theo dõi tiếp lần xử lý đó |
| Hiện "✕ Thất bại" ngay, không có kết quả cũ | Lần đọc trước của ảnh này bị lỗi, chưa có báo cáo | Chọn loại ảnh đúng nếu cần, bấm **"Thử lại"** |
| Đọc lại xong mà dashboard vẫn số cũ | Báo cáo mới cũng ra số giống cũ | So với ảnh, sửa tay nếu cần |

## Lưu ý khi tải lại ảnh đã tải trước đó

- Đọc lại tạo ra **báo cáo mới**. Báo cáo cũ vẫn còn ở Tàng Kinh Các, gắn nhãn "Đã được thay".
- Báo cáo cũ đã sửa tay mà bấm "OCR lại" thì số sửa tay bị báo cáo mới thay trên dashboard.
- Ảnh đã bị xóa khỏi hệ thống thì tải lên lại được coi là ảnh mới. Ảnh bị xóa khi quá 35 ngày, hoặc khi mọi báo cáo của ảnh đã bị xóa.
- Cách khác để đọc lại: mở báo cáo ở trang Xem / sửa report và bấm nút "OCR lại". Xem [OCR lại báo cáo](ocr-lai-bao-cao.md).
