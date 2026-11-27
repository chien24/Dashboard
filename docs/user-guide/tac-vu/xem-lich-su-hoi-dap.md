---
id: xem-lich-su-hoi-dap
title: Xem lại lịch sử hỏi đáp
loai: tac-vu
trang: Vấn Đạo Đài
he_thong: chung
aliases: [lịch sử chat, xem lại câu hỏi cũ, tin nhắn cũ, lịch sử nhắn, hội thoại cũ, Xem lịch sử, xem chat của máy khác, chat của người khác]
lien_quan: [van-dao-dai, khung-chat-nhanh, bat-dau-cuoc-tro-chuyen-moi, khong-co-cuoc-tro-chuyen]
nguon_code: [frontend/js/chat.js, frontend/js/chat-widget.js, backend/app/chatbot/router.py, backend/app/services/retention.py]
cap_nhat: 2026-11-20
---
# Xem lại lịch sử hỏi đáp

Còn gọi là: lịch sử chat, tin nhắn cũ, "xem lại câu đã hỏi bot", "xem chat của máy khác".

**Kết quả:** thấy danh sách mọi cuộc trò chuyện với chatbot của cả chi nhánh, mở lại cuộc nào cũng được.
**Cần có trước:** đã đăng nhập.

## Lịch sử hỏi đáp được chia theo máy thế nào

- Mỗi máy đang mở một cuộc trò chuyện riêng. Máy A hỏi không lẫn vào cuộc trò chuyện của máy B.
- Cả chi nhánh dùng chung tài khoản, nên **danh sách lịch sử chung cho mọi máy**. Máy A thấy được cuộc trò chuyện của máy B, và ngược lại.
- Câu hỏi gửi từ khung chat nhanh ở góc phải dưới cũng nằm trong lịch sử này.

## Các bước xem lại lịch sử hỏi đáp

1. Bấm menu **"Vấn Đạo Đài"**. Hoặc trong khung chat nhanh, bấm link **"Xem lịch sử"**.
2. Cột phải tự mở cuộc trò chuyện gần nhất của máy đang dùng.
3. Cột trái liệt kê mọi cuộc trò chuyện, mới dùng gần nhất ở trên, chia nhóm "Hôm nay", "Hôm qua", "7 ngày qua", "30 ngày qua". Mỗi dòng ghi câu hỏi đầu tiên; rê chuột để đọc đủ câu.
4. Bấm một dòng để mở cuộc trò chuyện đó ở cột phải. Mỗi câu trả lời cũ vẫn có cảnh báo và bảng kết quả.
5. Gõ câu hỏi mới để hỏi tiếp trong cuộc trò chuyện đang mở, kể cả cuộc do máy khác bắt đầu.

Muốn thấy cuộc trò chuyện máy khác vừa tạo: tải lại trang (F5).

## Nếu không thấy lịch sử hỏi đáp

| Hiện tượng | Nguyên nhân | Cách xử lý |
| --- | --- | --- |
| Danh sách bên trái trống | Chưa đăng nhập, hoặc chưa ai hỏi trong 30 ngày | Bấm "Nhập Môn" |
| Không thấy cột trái | Màn hình hẹp | Bấm nút "Lịch sử trò chuyện" trên tiêu đề |
| Không thấy cuộc máy khác vừa hỏi | Danh sách chỉ tải khi mở trang hoặc sau khi gửi câu hỏi | Tải lại trang |
| Cuộc trò chuyện cũ biến mất | Không dùng quá 30 ngày nên bị xóa | Không khôi phục được |
| Bảng cũ ghi "Đang hiển thị a/b dòng đã lưu." | Mỗi câu trả lời chỉ lưu tối đa 50 dòng bảng | Hỏi lại câu đó để xem đủ dòng |

## Lưu ý khi xem lại lịch sử hỏi đáp

- Cuộc trò chuyện không ai dùng 30 ngày sẽ tự xóa. Hỏi tiếp trong một cuộc thì cuộc đó được tính lại từ đầu 30 ngày.
- Mọi người dùng tài khoản chung đều đọc được lịch sử. Không hỏi nội dung riêng tư trong chatbot.
- Chưa xóa hoặc đổi tên cuộc trò chuyện được trên giao diện.
