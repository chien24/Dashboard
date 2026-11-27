---
id: can-dang-nhap
title: Lỗi "Cần đăng nhập"
loai: loi
trang: chung
he_thong: chung
aliases: [hết phiên, phiên đăng nhập hết hạn, Cần đăng nhập, bị đăng xuất, mất đăng nhập, Phiên đăng nhập đã hết]
lien_quan: [dang-nhap, khong-tai-duoc-du-lieu, gioi-han-va-quy-tac]
nguon_code: [frontend/js/api.js, frontend/js/chat.js, frontend/js/chat-widget.js, backend/app/main.py]
cap_nhat: 2026-11-20
---
# Lỗi "Cần đăng nhập"

Còn gọi là: hết phiên, bị đăng xuất, "Phiên đăng nhập đã hết, hãy Nhập Môn lại.", "Bạn cần Nhập Môn (đăng nhập) trước khi hỏi."

**Xuất hiện ở:** mọi trang có tải số liệu. Thường nằm sau một câu khác, ví dụ "Không tải được dữ liệu: Cần đăng nhập", "Không tải được lịch sử: Cần đăng nhập", "OCR thất bại … Cần đăng nhập". Trang Vấn Đạo Đài hiện "Bạn cần Nhập Môn (đăng nhập) trước khi hỏi."; khung chat nhanh hiện "Phiên đăng nhập đã hết, hãy Nhập Môn lại."

**Nghĩa là:** trình duyệt chưa đăng nhập, hoặc phiên đăng nhập đã hết trong lúc đang dùng trang.

**Nguyên nhân thường gặp:**
- Đã quá 7 ngày từ lần đăng nhập trước.
- Đã bấm "Xuất Môn" ở một tab khác của cùng trình duyệt.
- Mật khẩu chung vừa được đổi. Hỏi mật khẩu mới từ người viết code (Khoa), email chiencodedao@gmail.com.
- Đã xóa dữ liệu duyệt web (cookie).

**Cách xử lý:**
1. Bấm nút **"Nhập Môn"** ở góc trên bên phải.
2. Đăng nhập lại.
3. Làm lại thao tác vừa bị lỗi. Ảnh đã chọn ở trang Truyền Pháp Ảnh mà chưa gửi thì phải chọn lại sau khi trang tải lại.

**Nếu vẫn lỗi:** đăng nhập xong vẫn báo "Cần đăng nhập" thì trình duyệt có thể đang chặn cookie. Cho phép cookie với trang web này, hoặc thử trình duyệt khác. Vẫn không được thì báo người hỗ trợ ở mục **"Gặp Kiếp Nạn"** cuối trang.
