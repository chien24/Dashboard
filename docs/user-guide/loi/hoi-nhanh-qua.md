---
id: hoi-nhanh-qua
title: Lỗi "Hỏi nhanh quá, chờ … giây rồi hỏi tiếp"
loai: loi
trang: Vấn Đạo Đài
he_thong: chung
aliases: [hỏi quá nhanh, giới hạn câu hỏi, chatbot bắt chờ, 10 câu một phút, rate limit]
lien_quan: [hoi-dap-so-lieu-voi-chatbot, hoi-nhanh-bang-khung-chat, gioi-han-va-quy-tac, het-luot-hoi-mien-phi]
nguon_code: [frontend/js/chat.js, frontend/js/chat-widget.js, backend/app/chatbot/router.py]
cap_nhat: 2026-11-20
---
# Lỗi "Hỏi nhanh quá, chờ … giây rồi hỏi tiếp"

Còn gọi là: chatbot bắt chờ, giới hạn số câu hỏi, rate limit.

**Xuất hiện ở:** trang **"Vấn Đạo Đài"** hoặc khung chat nhanh, sau khi gửi câu hỏi. Dạng: "Không gửi được câu hỏi: Hỏi nhanh quá, chờ 25 giây rồi hỏi tiếp".

**Nghĩa là:** máy này đã gửi 10 câu hỏi trong vòng 1 phút. Câu hỏi vừa gửi không được xử lý. Giới hạn tính riêng cho từng máy, các máy khác vẫn hỏi bình thường.

**Nguyên nhân thường gặp:**
- Bấm liên tục nhiều câu hỏi mẫu hoặc nút lựa chọn.
- Gửi lại cùng câu hỏi nhiều lần khi chờ lâu.

**Cách xử lý:**
1. Chờ đúng số giây ghi trong thông báo.
2. Gửi lại câu hỏi.
3. Gộp nhiều ý vào một câu hỏi, ví dụ "ALL, REJECT và tỷ lệ REJECT HT2 hôm qua" thay vì ba câu riêng.

**Nếu vẫn lỗi:** chờ đủ thời gian mà vẫn bị báo thì tải lại trang rồi thử lại sau vài phút. Vẫn không được thì báo người hỗ trợ ở mục **"Gặp Kiếp Nạn"** cuối trang.
