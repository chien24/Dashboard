---
id: hoi-dap-so-lieu-voi-chatbot
title: Hỏi đáp số liệu với chatbot ở Vấn Đạo Đài
loai: tac-vu
trang: Vấn Đạo Đài
he_thong: chung
aliases: [hỏi chatbot, hỏi bot, chat hỏi số liệu, hỏi đáp dữ liệu, câu hỏi nối tiếp, bot hỏi lại]
lien_quan: [van-dao-dai, chatbot-hoi-duoc-gi, canh-bao-cua-chatbot, hoi-nhanh-bang-khung-chat, xem-lich-su-hoi-dap]
nguon_code: [frontend/html/chat.html, frontend/js/chat.js, backend/app/chatbot/router.py, backend/app/chatbot/pipeline.py]
cap_nhat: 2026-11-20
---
# Hỏi đáp số liệu với chatbot ở Vấn Đạo Đài

Còn gọi là: hỏi chatbot, hỏi bot, "hỏi số liệu bằng tiếng Việt".

**Kết quả:** chatbot trả lời bằng chữ, kèm bảng kết quả và cảnh báo về dữ liệu (nếu có).
**Cần có trước:** đã đăng nhập.

## Các bước hỏi đáp số liệu với chatbot

1. Bấm menu **"Vấn Đạo Đài"**.
2. Gõ câu hỏi vào ô ở cuối trang (gợi ý "VD: Tỷ lệ REJECT HT2 hôm qua?"). Hoặc bấm một câu trong mục **"Thử một câu hỏi:"**.
3. Nhấn Enter hoặc bấm **"Gửi câu hỏi"**. Shift+Enter để xuống dòng.
4. Câu trả lời hiện "Đang truy vấn…" trong lúc chờ. Muốn thôi chờ thì bấm **"Hủy"**.
5. Đọc câu trả lời. Nếu có danh sách nền vàng, đó là cảnh báo về dữ liệu, ví dụ ngày còn thiếu ảnh.
6. Xem bảng kết quả dưới câu trả lời. Bảng hiện tối đa 200 dòng.
7. Hỏi tiếp câu nối tiếp được, ví dụ "còn HT1 thì sao?". Chatbot nhớ vài lượt hỏi gần nhất trong cùng cuộc trò chuyện.

## Khi chatbot hỏi lại

Câu hỏi thiếu thông tin (ví dụ "tỷ lệ lỗi hôm qua" mà không nói HT1 hay HT2), chatbot hỏi lại và hiện các nút lựa chọn. Bấm một nút để trả lời, hoặc gõ câu hỏi đầy đủ hơn.

## Nếu hỏi chatbot không được

| Hiện tượng | Nguyên nhân | Cách xử lý |
| --- | --- | --- |
| "Bạn cần Nhập Môn (nút ở góc trên bên phải) để hỏi đáp dữ liệu." | Chưa đăng nhập | Bấm "Nhập Môn" |
| "Hỏi nhanh quá, chờ … giây rồi hỏi tiếp" | Quá 10 câu trong 1 phút | Chờ đủ số giây. Xem [lỗi này](../loi/hoi-nhanh-qua.md) |
| "Đã hết lượt hỏi miễn phí…" | Dịch vụ AI hết lượt dùng | Thử lại sau. Xem [lỗi này](../loi/het-luot-hoi-mien-phi.md) |
| "Mình chưa trả lời được câu này…" | Chatbot không hiểu câu hỏi | Hỏi cụ thể hơn. Xem [lỗi này](../loi/chatbot-chua-tra-loi-duoc.md) |
| "Không gửi được câu hỏi: …" | Mất mạng hoặc lỗi máy chủ | Thử lại; đọc lý do sau dấu hai chấm |
| "Đã hủy chờ. Câu hỏi vẫn có thể đang chạy ở máy chủ." | Đã bấm "Hủy" | Gửi lại câu hỏi nếu vẫn cần |

## Lưu ý khi hỏi đáp số liệu với chatbot

- Chatbot chỉ đọc dữ liệu. Không sửa, không xóa được. Muốn sửa số: dùng trang Tàng Kinh Các.
- Ngày không có dữ liệu được báo là "chưa có dữ liệu", không bao giờ tính là 0.
- Câu hỏi dài tối đa 1000 ký tự.
- Câu trả lời dựa trên số đang dùng trên dashboard. Số đọc sai mà chưa sửa thì câu trả lời cũng sai.
- Hỏi được gì: [Chatbot hỏi được gì, không hỏi được gì](../tham-chieu/chatbot-hoi-duoc-gi.md).
