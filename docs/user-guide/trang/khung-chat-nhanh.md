---
id: khung-chat-nhanh
title: Khung chat nhanh ở góc phải dưới
loai: trang
trang: Khung chat nhanh
he_thong: chung
aliases: [nút chat, icon chatbot, bong bóng chat, chat nổi, khung hỏi nhanh, widget chat]
lien_quan: [hoi-nhanh-bang-khung-chat, van-dao-dai, xem-lich-su-hoi-dap, chatbot-hoi-duoc-gi]
nguon_code: [frontend/js/chat-widget.js, frontend/css/base.css]
cap_nhat: 2026-11-20
---
# Khung chat nhanh ở góc phải dưới

Còn gọi là: nút chat, icon chatbot, chat nổi, khung hỏi nhanh.

**Khung chat nhanh** là cửa sổ nhỏ để hỏi chatbot mà không cần rời trang đang xem. Khung chỉ để nhắn câu hỏi và đọc câu trả lời ngắn. Lịch sử đầy đủ và bảng kết quả xem ở trang **"Vấn Đạo Đài"**.

## Cách mở khung chat nhanh

Bấm nút tròn màu đỏ, hình bong bóng chat có ngôi sao, ở góc phải dưới màn hình. Rê chuột lên nút thấy chữ "Hỏi đáp dữ liệu".

Nút có trên các trang Thiên Cơ Các, Truyền Pháp Ảnh, Tàng Kinh Các và Xem / sửa report. Trang Vấn Đạo Đài không có nút tròn hình bong bóng chat vì đã là trang chat.

## Bố cục khung chat nhanh

Khung mở ngay phía trên nút tròn, rộng khoảng 360 điểm ảnh, cao khoảng 480 điểm ảnh. Trên điện thoại, khung tự thu nhỏ cho vừa màn hình.
1. Thanh tiêu đề: chữ **"Vấn Đạo Đài"**, link **"Xem lịch sử"**, nút **"✕"** để đóng.
2. Khu tin nhắn: lời chào "Hỏi nhanh số liệu HT1 (SCADA) và HT2 (DMWCS). VD: "Tỷ lệ REJECT HT2 hôm qua?"", rồi các câu hỏi và trả lời.
3. Ô nhập **"Nhập câu hỏi…"** và nút **"Gửi"** ở đáy khung.

## Các nút và ô nhập trong khung chat nhanh

| Phần tử | Vị trí | Dùng để | Khi bấm/nhập thì |
| --- | --- | --- | --- |
| Nút tròn hình bong bóng chat | Góc phải dưới màn hình | Mở / đóng khung | Bấm lần nữa để đóng |
| Ô **"Nhập câu hỏi…"** | Đáy khung | Gõ câu hỏi | Enter gửi; Shift+Enter xuống dòng |
| Nút **"Gửi"** | Bên phải ô nhập | Gửi câu hỏi | Hiện "Đang truy vấn…" rồi câu trả lời |
| Link **"Xem lịch sử"** | Thanh tiêu đề | Xem lịch sử đầy đủ | Mở trang Vấn Đạo Đài |
| Nút **"✕"** | Góc phải thanh tiêu đề | Đóng khung | Phím Esc cũng đóng được |
| Nút lựa chọn | Dưới câu chatbot hỏi lại | Chọn câu trả lời | Gửi lựa chọn đó |
| Link **"Xem bảng kết quả"** | Dưới câu trả lời có bảng | Xem bảng đầy đủ | Mở trang Vấn Đạo Đài |

## Dữ liệu hiển thị trong khung chat nhanh

Khung chỉ hiện chữ trả lời, cảnh báo màu vàng và nút lựa chọn. Bảng kết quả không hiện trong khung.

Khung không tải lại tin nhắn cũ. Chuyển sang trang khác thì các tin trong khung mất khỏi màn hình. Câu hỏi vẫn được lưu vào cuộc trò chuyện đang mở của máy này, xem lại ở cột trái trang Vấn Đạo Đài trên trình duyệt đó.

## Khi khung chat nhanh không dùng được

- Chưa đăng nhập: gửi câu hỏi thì hiện "Bạn cần Nhập Môn (nút ở góc trên bên phải) trước khi hỏi."
- Hết phiên đăng nhập: hiện "Phiên đăng nhập đã hết, hãy Nhập Môn lại."
- Lỗi khác: hiện "Không gửi được câu hỏi: …" kèm lý do. Xem [Lỗi "Hỏi nhanh quá"](../loi/hoi-nhanh-qua.md) và [Lỗi "Đã hết lượt hỏi miễn phí"](../loi/het-luot-hoi-mien-phi.md).

## Việc thường làm với khung chat nhanh

- [Hỏi nhanh bằng khung chat góc phải dưới](../tac-vu/hoi-nhanh-bang-khung-chat.md)
- [Xem lại lịch sử hỏi đáp](../tac-vu/xem-lich-su-hoi-dap.md)
