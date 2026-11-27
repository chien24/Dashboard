---
id: chatbot-hoi-duoc-gi
title: Chatbot hỏi được gì, không hỏi được gì
loai: tham-chieu
trang: Vấn Đạo Đài
he_thong: chung
aliases: [chatbot làm được gì, câu hỏi mẫu, hỏi chatbot thế nào, giới hạn chatbot, ngoài phạm vi, chatbot không trả lời]
lien_quan: [hoi-dap-so-lieu-voi-chatbot, van-dao-dai, canh-bao-cua-chatbot, chatbot-chua-tra-loi-duoc]
nguon_code: [frontend/js/chat.js, backend/app/chatbot/prompts/system_sql.md]
cap_nhat: 2026-11-20
---
# Chatbot hỏi được gì, không hỏi được gì

Còn gọi là: chatbot làm được gì, "hỏi bot câu gì", câu hỏi mẫu, ngoài phạm vi.

Chatbot ở trang **Vấn Đạo Đài** và khung chat nhanh trả lời câu hỏi về **số liệu đã có trên dashboard** của HT1 (SCADA) và HT2 (DMWCS).

## Chatbot hỏi được những gì

- Số liệu một ngày hoặc nhiều ngày: ALL, CORRECT, REJECT, tỷ lệ REJECT, công suất, thời gian sử dụng.
- So sánh: giữa các dây chuyền HT1, giữa các ngày, giữa HT1 và HT2.
- Xếp hạng: dây chuyền nào cao nhất, Scanner nào thấp nhất, máng NoChute nào xuất hiện nhiều nhất.
- Xu hướng theo ngày: "thế nào", "từng ngày" sẽ được trả về mỗi ngày một dòng.
- Tổng, trung bình trong một khoảng ngày.
- Chất lượng dữ liệu: báo cáo nào cần kiểm tra, ngày nào thiếu ảnh.
- Câu hỏi nối tiếp trong cùng cuộc trò chuyện, ví dụ "còn tuần trước?".

## Câu hỏi mẫu trên trang Vấn Đạo Đài

- "Hôm qua HT2 sorted tổng bao nhiêu kiện, tỷ lệ REJECT bao nhiêu %?"
- "Công suất AVG 7 ngày gần nhất thế nào?"
- "Dây chuyền nào có tỷ lệ bất thường cao nhất tuần này?"
- "BCR nào có rate thấp nhất hôm qua?"
- "Máng nào xuất hiện trong NoChute nhiều nhất 2 tuần qua?"
- "Tuần này có report nào cần kiểm tra không?"

## Chatbot không làm được những gì

- Sửa, xóa, thêm số liệu. Muốn sửa: trang Tàng Kinh Các → mở báo cáo → sửa tay.
- Dự báo tương lai, giải thích nguyên nhân vì sao số tăng giảm.
- Trả lời chủ đề ngoài số liệu vận hành.
- Xem dữ liệu cũ hơn 35 ngày (đã bị xóa).
- Đọc số liệu không có trong báo cáo, ví dụ biểu đồ theo giờ trên màn hình SCADA.

Câu hỏi ngoài phạm vi thì chatbot từ chối ngắn gọn và chỉ cách làm khác.

## Cách hỏi để chatbot trả lời đúng

- Nêu rõ hệ thống: HT1 (SCADA) hay HT2 (DMWCS). "Tỷ lệ lỗi" chung chung sẽ bị hỏi lại.
- Nêu rõ chỉ số: REJECT, NoRead, công suất AVG…
- Nêu rõ ngày: "hôm qua", "ngày 12/11", "7 ngày gần nhất", "tuần trước", "tháng này". Không nói ngày thì chatbot lấy ngày gần nhất có dữ liệu.
- Tên dây chuyền gọi tắt được, ví dụ "CBS2". Nếu khớp nhiều dây chuyền, chatbot hỏi lại.
- "Tỷ lệ NoRead" mặc định tính trên RejectChute. Muốn tính trên tổng thì hỏi "trên tổng".

## Kiểm tra câu trả lời của chatbot

Mỗi câu trả lời trên trang Vấn Đạo Đài có bảng kết quả. Đọc thêm danh sách cảnh báo nền vàng. Xem [Cảnh báo của chatbot](canh-bao-cua-chatbot.md).
