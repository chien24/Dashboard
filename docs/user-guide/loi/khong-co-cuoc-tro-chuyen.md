---
id: khong-co-cuoc-tro-chuyen
title: Lỗi "Không có cuộc trò chuyện này"
loai: loi
trang: Vấn Đạo Đài
he_thong: chung
aliases: [mất cuộc trò chuyện, lịch sử chat bị xóa, cuộc trò chuyện đã bị xóa, không thấy lịch sử]
lien_quan: [xem-lich-su-hoi-dap, bat-dau-cuoc-tro-chuyen-moi, gioi-han-va-quy-tac]
nguon_code: [frontend/js/chat.js, frontend/js/chat-widget.js, backend/app/chatbot/router.py]
cap_nhat: 2026-11-20
---
# Lỗi "Không có cuộc trò chuyện này"

Còn gọi là: mất cuộc trò chuyện, lịch sử chat bị xóa.

**Xuất hiện ở:** trang **"Vấn Đạo Đài"**, khi gửi câu hỏi. Dạng: "Không gửi được câu hỏi: Không có cuộc trò chuyện này (có thể đã bị xóa theo chính sách lưu trữ)".

**Nghĩa là:** trình duyệt còn nhớ một cuộc trò chuyện cũ, nhưng cuộc trò chuyện đó đã bị xóa khỏi hệ thống.

**Nguyên nhân thường gặp:**
- Cuộc trò chuyện không được dùng quá 30 ngày nên bị xóa tự động.
- Trang Vấn Đạo Đài để mở qua đêm, đúng lúc hệ thống dọn dữ liệu cũ.

**Cách xử lý:**
1. Bấm nút **"+ Cuộc trò chuyện mới"** trên cùng cột trái trang Vấn Đạo Đài, hoặc mở một cuộc khác trong danh sách.
2. Gửi lại câu hỏi.

Thường mở lại trang Vấn Đạo Đài thì trang tự bỏ cuộc trò chuyện đã bị xóa và hiện câu hỏi mẫu, nên ít gặp lỗi này. Khung chat nhanh ở góc phải dưới cũng tự bắt đầu cuộc trò chuyện mới, không báo lỗi.

**Nếu vẫn lỗi:** tải lại trang (F5). Vẫn lỗi thì báo người hỗ trợ ở mục **"Gặp Kiếp Nạn"** cuối trang.
