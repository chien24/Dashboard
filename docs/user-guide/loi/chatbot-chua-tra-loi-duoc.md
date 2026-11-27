---
id: chatbot-chua-tra-loi-duoc
title: Lỗi "Mình chưa trả lời được câu này"
loai: loi
trang: Vấn Đạo Đài
he_thong: chung
aliases: [chatbot không hiểu, chatbot không trả lời được, diễn đạt lại, bot không hiểu câu hỏi]
lien_quan: [chatbot-hoi-duoc-gi, hoi-dap-so-lieu-voi-chatbot, canh-bao-cua-chatbot]
nguon_code: [frontend/js/chat.js, backend/app/chatbot/pipeline.py]
cap_nhat: 2026-11-20
---
# Lỗi "Mình chưa trả lời được câu này"

Còn gọi là: chatbot không hiểu, "bot không trả lời được".

**Xuất hiện ở:** trang **"Vấn Đạo Đài"** hoặc khung chat nhanh. Câu trả lời đầy đủ: "Mình chưa trả lời được câu này. Bạn thử diễn đạt lại cụ thể hơn: nêu hệ thống (HT1 SCADA hay HT2 DMWCS), chỉ số và ngày, ví dụ "Tỷ lệ REJECT HT2 ngày 12/11"."

**Nghĩa là:** chatbot đã thử vài lần nhưng không tạo được cách tính đúng cho câu hỏi.

**Nguyên nhân thường gặp:**
- Câu hỏi mơ hồ, thiếu hệ thống, chỉ số hoặc ngày.
- Câu hỏi về số liệu không có trong báo cáo, ví dụ số theo giờ.
- Câu hỏi quá phức tạp, gộp nhiều điều kiện.

**Cách xử lý:**
1. Viết lại câu hỏi đủ ba phần: hệ thống, chỉ số, ngày. Ví dụ "Tỷ lệ REJECT HT2 ngày 12/11".
2. Tách câu hỏi phức tạp thành nhiều câu nhỏ.
3. Thử một câu hỏi mẫu trong mục "Thử một câu hỏi:" để so cách hỏi.
4. Nếu chatbot đang hiểu nhầm theo câu trước, bấm **"+ Cuộc trò chuyện mới"** ở cột trái rồi hỏi lại.

Xem [Chatbot hỏi được gì](../tham-chieu/chatbot-hoi-duoc-gi.md).

**Nếu vẫn lỗi:** câu hỏi rõ ràng mà chatbot vẫn không trả lời được thì xem số trực tiếp trên dashboard, và báo câu hỏi đó cho người hỗ trợ ở mục **"Gặp Kiếp Nạn"** để cải thiện chatbot.
