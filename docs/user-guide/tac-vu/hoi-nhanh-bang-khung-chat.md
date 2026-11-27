---
id: hoi-nhanh-bang-khung-chat
title: Hỏi nhanh bằng khung chat góc phải dưới
loai: tac-vu
trang: Khung chat nhanh
he_thong: chung
aliases: [chat nhanh, nút chat góc phải, icon chatbot, hỏi bot không rời trang, bong bóng chat]
lien_quan: [khung-chat-nhanh, hoi-dap-so-lieu-voi-chatbot, xem-lich-su-hoi-dap, chatbot-hoi-duoc-gi]
nguon_code: [frontend/js/chat-widget.js]
cap_nhat: 2026-11-20
---
# Hỏi nhanh bằng khung chat góc phải dưới

Còn gọi là: chat nhanh, nút chat góc phải, "hỏi bot mà không rời trang dashboard".

**Kết quả:** câu trả lời ngắn hiện ngay trong khung nhỏ, không cần rời trang đang xem.
**Cần có trước:** đã đăng nhập; đang ở trang Thiên Cơ Các, Truyền Pháp Ảnh, Tàng Kinh Các hoặc Xem / sửa report.

## Các bước hỏi nhanh bằng khung chat

1. Bấm nút tròn màu đỏ hình bong bóng chat ở góc phải dưới màn hình. Khung chat nhỏ mở ra phía trên nút.
2. Gõ câu hỏi vào ô **"Nhập câu hỏi…"** ở đáy khung.
3. Nhấn Enter hoặc bấm **"Gửi"**. Khung hiện "Đang truy vấn…".
4. Đọc câu trả lời. Cảnh báo về dữ liệu hiện màu vàng dưới câu trả lời.
5. Chatbot hỏi lại thì bấm một nút lựa chọn bên dưới.
6. Câu trả lời có bảng: bấm **"Xem bảng kết quả"** để mở trang Vấn Đạo Đài.
7. Đóng khung: bấm **"✕"**, nhấn Esc, hoặc bấm lại nút tròn.

## Nếu hỏi nhanh bằng khung chat không được

| Hiện tượng | Nguyên nhân | Cách xử lý |
| --- | --- | --- |
| "Bạn cần Nhập Môn (nút ở góc trên bên phải) trước khi hỏi." | Chưa đăng nhập | Bấm "Nhập Môn" |
| "Phiên đăng nhập đã hết, hãy Nhập Môn lại." | Hết phiên 7 ngày | Đăng nhập lại |
| "Không gửi được câu hỏi: Hỏi nhanh quá, chờ … giây rồi hỏi tiếp" | Quá 10 câu/phút | Chờ đủ số giây |
| "Không gửi được câu hỏi: …" khác | Mất mạng hoặc lỗi máy chủ | Thử lại sau |
| Không thấy nút tròn | Đang ở trang Vấn Đạo Đài hoặc trang phong ấn | Ở Vấn Đạo Đài thì hỏi trực tiếp trên trang |

## Lưu ý khi hỏi nhanh bằng khung chat

- Khung chat chỉ để nhắn. Không hiện bảng, không hiện SQL, không tải lại tin nhắn cũ.
- Chuyển trang thì tin nhắn trong khung mất khỏi màn hình, nhưng vẫn lưu trong lịch sử. Xem ở trang Vấn Đạo Đài bằng link **"Xem lịch sử"**.
- Khung chat và trang Vấn Đạo Đài dùng chung cuộc trò chuyện. Hỏi nối tiếp được giữa hai nơi.
- Nếu cuộc trò chuyện cũ đã bị xóa theo hạn lưu trữ, khung chat tự bắt đầu cuộc trò chuyện mới.
