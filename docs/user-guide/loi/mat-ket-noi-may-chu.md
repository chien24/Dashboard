---
id: mat-ket-noi-may-chu
title: Lỗi "Mất kết nối tới server"
loai: loi
trang: Truyền Pháp Ảnh
he_thong: chung
aliases: [mất mạng, không kết nối được, Failed to fetch, server không phản hồi, rớt mạng khi upload]
lien_quan: [theo-doi-tien-do-xu-ly-anh, khong-tai-duoc-du-lieu, tim-bao-cao]
nguon_code: [frontend/js/upload.js]
cap_nhat: 2026-11-20
---
# Lỗi "Mất kết nối tới server"

Còn gọi là: mất mạng, rớt mạng khi tải ảnh, server không phản hồi.

**Xuất hiện ở:** trang **"Truyền Pháp Ảnh"**, trong lúc theo dõi tiến độ đọc ảnh. Dòng ảnh hiện **"✕ Thất bại"**, khối đỏ ghi "Không đọc được ảnh này. Mất kết nối tới server: …".

**Nghĩa là:** trình duyệt không hỏi được máy chủ về tiến độ của ảnh. Ảnh **có thể vẫn đang được đọc** trên máy chủ, chỉ là trang không theo dõi tiếp được.

**Nguyên nhân thường gặp:**
- Mạng của máy bị ngắt hoặc chập chờn.
- Máy chủ đang khởi động lại.
- Đường truyền tới máy chủ bị gián đoạn.

**Cách xử lý:**
1. Kiểm tra mạng của máy.
2. Chờ vài phút, mở trang **"Tàng Kinh Các"** và tìm theo tên file ảnh. Có báo cáo thì ảnh đã đọc xong.
3. Không thấy báo cáo: quay lại trang Truyền Pháp Ảnh, tải lại ảnh. Nếu bị báo trùng mà đang xử lý dở, trang tự theo dõi tiếp. Nếu bị báo trùng với kết quả cũ, xem kết quả cũ.

Không nên bấm "Thử lại" ngay, vì có thể tạo thêm một lượt đọc thừa cho cùng ảnh.

**Nếu vẫn lỗi:** mạng ổn mà vẫn mất kết nối, máy chủ có thể đang tắt. Báo người hỗ trợ ở mục **"Gặp Kiếp Nạn"** cuối trang.
