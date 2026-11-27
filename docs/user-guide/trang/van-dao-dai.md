---
id: van-dao-dai
title: Trang Vấn Đạo Đài (chatbot hỏi đáp số liệu)
loai: trang
trang: Vấn Đạo Đài
he_thong: chung
aliases: [chatbot, trang chat, hỏi đáp dữ liệu, trợ lý số liệu, Vấn Đạo Đài, bot, lịch sử trò chuyện]
lien_quan: [hoi-dap-so-lieu-voi-chatbot, xem-lich-su-hoi-dap, bat-dau-cuoc-tro-chuyen-moi, chatbot-hoi-duoc-gi, canh-bao-cua-chatbot]
nguon_code: [frontend/html/chat.html, frontend/js/chat.js, frontend/css/chat.css]
cap_nhat: 2026-11-20
---
# Trang Vấn Đạo Đài (chatbot hỏi đáp số liệu)

Còn gọi là: chatbot, trang chat, hỏi đáp dữ liệu, trợ lý số liệu.

Trang **Vấn Đạo Đài** là chatbot trả lời câu hỏi tiếng Việt về số liệu HT1 (SCADA) và HT2 (DMWCS). Bố cục giống các ứng dụng chat phổ biến: danh sách cuộc trò chuyện bên trái, cuộc trò chuyện đang mở bên phải. Chatbot chỉ đọc dữ liệu, không sửa được.

## Cách mở trang Vấn Đạo Đài

- Bấm mục **"Vấn Đạo Đài"** trên thanh menu.
- Trong khung chat nhanh ở góc phải dưới, bấm link **"Xem lịch sử"**.

## Bố cục trang Vấn Đạo Đài

**Cột trái (lịch sử trò chuyện):**
1. Nút **"+ Cuộc trò chuyện mới"** trên cùng.
2. Danh sách cuộc trò chuyện của **mọi máy**, chia nhóm "Hôm nay", "Hôm qua", "7 ngày qua", "30 ngày qua". Mỗi cuộc ghi câu hỏi đầu tiên. Cuộc đang mở được tô đỏ.
3. Dòng ghi chú "Lịch sử chung của mọi máy. Cuộc trò chuyện không dùng 30 ngày sẽ tự xóa."

**Cột phải (cuộc trò chuyện đang mở):**
1. Tiêu đề **"Vấn Đạo Đài"** và dòng mô tả.
2. Khu hội thoại: câu hỏi bên phải, câu trả lời bên trái.
3. Mục **"Thử một câu hỏi:"** với 6 câu hỏi mẫu (khi cuộc trò chuyện còn trống).
4. Ô nhập câu hỏi và nút **"Gửi câu hỏi"**, luôn dính ở đáy màn hình khi cuộn.
5. Dòng **"Enter để gửi, Shift+Enter để xuống dòng."** và dòng thống kê lượt hỏi trong ngày.

Trên điện thoại hoặc màn hình hẹp, cột trái được ẩn. Bấm nút **"Lịch sử trò chuyện"** trên tiêu đề để mở hoặc đóng danh sách.

## Các nút và ô nhập trên trang Vấn Đạo Đài

| Phần tử | Vị trí | Dùng để | Khi bấm/nhập thì |
| --- | --- | --- | --- |
| Nút **"+ Cuộc trò chuyện mới"** | Trên cùng cột trái | Bắt đầu cuộc mới | Cột phải trống, hiện câu hỏi mẫu |
| Một dòng trong danh sách | Cột trái | Mở cuộc trò chuyện đó | Cột phải hiện toàn bộ cuộc đó; hỏi tiếp được |
| Nút **"Lịch sử trò chuyện"** | Trên tiêu đề, chỉ có ở màn hình hẹp | Mở / đóng cột trái | Danh sách hiện phía trên |
| Ô nhập (gợi ý "VD: Tỷ lệ REJECT HT2 hôm qua?") | Cuối cột phải | Gõ câu hỏi, tối đa 1000 ký tự | Enter gửi; Shift+Enter xuống dòng |
| Nút **"Gửi câu hỏi"** | Bên phải ô nhập | Gửi câu hỏi | Hiện "Đang truy vấn…" rồi câu trả lời |
| Nút **"Hủy"** | Cạnh nút Gửi, chỉ hiện khi đang chờ | Thôi chờ câu trả lời | Hiện "Đã hủy chờ. Câu hỏi vẫn có thể đang chạy ở máy chủ." |
| Nút câu hỏi mẫu | Mục "Thử một câu hỏi:" | Hỏi nhanh câu mẫu | Gửi đúng câu đó |
| Nút lựa chọn trong câu trả lời | Dưới câu chatbot hỏi lại | Trả lời câu hỏi lại | Gửi lựa chọn đó như một câu hỏi |

## Dữ liệu hiển thị trên trang Vấn Đạo Đài

Mỗi câu trả lời của chatbot có thể gồm: câu trả lời bằng chữ, danh sách cảnh báo nền vàng, nút lựa chọn khi chatbot hỏi lại, bảng kết quả (tối đa 200 dòng) và dòng nhỏ ghi model đã dùng cùng số giây trả lời. Xem [Cảnh báo của chatbot](../tham-chieu/canh-bao-cua-chatbot.md).

Dòng thống kê dưới ô nhập có dạng "Hôm nay: N câu hỏi, N lượt gọi model, …", là tổng của cả chi nhánh trong ngày.

## Khi trang Vấn Đạo Đài không dùng được

- Chưa đăng nhập: khu hội thoại hiện **"Bạn cần Nhập Môn (nút ở góc trên bên phải) để hỏi đáp dữ liệu."**, nút gửi bị mờ, danh sách bên trái trống.
- Hết phiên khi đang hỏi: hiện **"Bạn cần Nhập Môn (đăng nhập) trước khi hỏi."**
- Các lỗi khác: xem [Hỏi đáp số liệu với chatbot](../tac-vu/hoi-dap-so-lieu-voi-chatbot.md).

## Việc thường làm trên trang Vấn Đạo Đài

- [Hỏi đáp số liệu với chatbot](../tac-vu/hoi-dap-so-lieu-voi-chatbot.md)
- [Xem lại lịch sử hỏi đáp](../tac-vu/xem-lich-su-hoi-dap.md)
- [Bắt đầu cuộc trò chuyện mới](../tac-vu/bat-dau-cuoc-tro-chuyen-moi.md)
