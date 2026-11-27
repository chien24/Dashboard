---
id: het-luot-hoi-mien-phi
title: Lỗi "Đã hết lượt hỏi miễn phí"
loai: loi
trang: Vấn Đạo Đài
he_thong: chung
aliases: [hết lượt hỏi, hết quota, chatbot hết lượt, thử lại sau khoảng phút, chatbot không trả lời nữa]
lien_quan: [hoi-dap-so-lieu-voi-chatbot, hoi-nhanh-qua, chatbot-chua-goi-duoc-model, gioi-han-va-quy-tac]
nguon_code: [frontend/js/chat.js, backend/app/chatbot/pipeline.py]
cap_nhat: 2026-11-20
---
# Lỗi "Đã hết lượt hỏi miễn phí"

Còn gọi là: hết lượt hỏi, hết quota, "chatbot không trả lời nữa".

**Xuất hiện ở:** trang **"Vấn Đạo Đài"** hoặc khung chat nhanh, là câu trả lời của chatbot (chữ đỏ ở trang Vấn Đạo Đài). Dạng: "Đã hết lượt hỏi miễn phí, thử lại sau khoảng N phút." hoặc "Đã hết lượt hỏi miễn phí, thử lại sau ít phút."

**Nghĩa là:** dịch vụ AI mà chatbot dùng đã hết lượt cho phép, ở mọi lựa chọn dự phòng. Giới hạn này tính chung cho cả chi nhánh, không riêng một người.

**Nguyên nhân thường gặp:**
- Cả chi nhánh đã hỏi nhiều trong ngày, hết lượt dùng theo ngày.
- Nhiều câu hỏi dồn trong vài phút, hết lượt theo phút.

**Cách xử lý:**
1. Chờ số phút ghi trong thông báo, rồi hỏi lại.
2. Trong lúc chờ, xem số liệu trực tiếp ở trang **"Thiên Cơ Các"** hoặc **"Tàng Kinh Các"**.
3. Hỏi gọn: gộp nhiều ý vào một câu để tiết kiệm lượt.

Dòng thống kê "Hôm nay: … câu hỏi, … lượt gọi model" dưới ô nhập ở trang Vấn Đạo Đài cho biết cả chi nhánh đã hỏi bao nhiêu trong ngày.

**Nếu vẫn lỗi:** sang ngày hôm sau vẫn báo hết lượt thì báo người hỗ trợ ở mục **"Gặp Kiếp Nạn"** cuối trang.
