---
id: canh-bao-cua-chatbot
title: Ý nghĩa các cảnh báo trong câu trả lời của chatbot
loai: tham-chieu
trang: Vấn Đạo Đài
he_thong: chung
aliases: [cảnh báo chatbot, chatbot báo thiếu dữ liệu, chưa có dữ liệu, dữ liệu đã bị xóa, ảnh đang được OCR, kết quả rỗng]
lien_quan: [hoi-dap-so-lieu-voi-chatbot, chatbot-hoi-duoc-gi, trang-thai, gioi-han-va-quy-tac]
nguon_code: [frontend/js/chat.js, backend/app/chatbot/checks.py]
cap_nhat: 2026-11-20
---
# Ý nghĩa các cảnh báo trong câu trả lời của chatbot

Còn gọi là: chatbot báo thiếu dữ liệu, "chatbot nói chưa có dữ liệu là sao", danh sách vàng dưới câu trả lời.

Hệ thống tự kiểm tra dữ liệu quanh mỗi câu hỏi và ghi cảnh báo thành danh sách nền vàng dưới câu trả lời của chatbot (ở trang **Vấn Đạo Đài** và khung chat nhanh). Các cảnh báo này không do chatbot tự đoán.

## Cảnh báo về dữ liệu đã bị xóa

- **"Dữ liệu trước dd/mm/yyyy đã bị xóa theo chính sách lưu 35 ngày; kết quả chỉ tính từ dd/mm."**: một phần khoảng ngày hỏi đã quá 35 ngày.
- **"Dữ liệu trước … đã bị xóa theo chính sách lưu 35 ngày, nên không còn số liệu cho …"**: cả khoảng ngày hỏi đã bị xóa; chatbot không tra cứu.

## Cảnh báo về ngày chưa có dữ liệu

- **"Các ngày sau hôm nay (dd/mm) chưa có dữ liệu."**: câu hỏi có ngày tương lai.
- **"Chưa có dữ liệu <loại> các ngày: dd/mm, dd/mm…"**: các ngày chưa có ảnh của loại đó, ví dụ "SCADA (HT1)", "Sorted (HT2)", "Capacity (HT2)", "BCR rate (HT2)". Kết quả chỉ tính trên các ngày có dữ liệu. Nên tải ảnh của các ngày còn thiếu.

## Cảnh báo về chất lượng số liệu

- **"Report ngày dd/mm (<tên ảnh>) cần kiểm tra: số có thể sai do lệch giữa 2 lần OCR."**: kết quả dùng một báo cáo có trạng thái "Cần kiểm tra". Mở báo cáo đó ở Tàng Kinh Các để kiểm tra.
- **"Có N dòng loại bất thường chưa phân loại được (UNKNOWN) trong khoảng này."**: có loại bất thường SCADA hệ thống chưa nhận ra tên. Báo người quản trị.
- **"Danh sách máng NoChute ngày … bị cắt trên ảnh, có thể thiếu máng."**: danh sách máng NoChute trên ảnh Sorted bị cắt ở mép.
- **"Có N ảnh đang được OCR, số liệu có thể thay đổi sau ít phút."**: đang có ảnh trong hàng đợi. Hỏi lại sau ít phút để có số mới nhất.

## Câu trả lời khi không có kết quả

- **"Chưa có dữ liệu … cho dd/mm–dd/mm (chưa có ảnh được OCR cho khoảng này). Ngày gần nhất có dữ liệu: …"**: chưa có ảnh nào trong khoảng hỏi. Chatbot gợi ý ngày gần nhất có dữ liệu.
- **"Không có dòng nào khớp điều kiện của câu hỏi (đã có dữ liệu trong khoảng ngày này)."**: có dữ liệu nhưng điều kiện không khớp, ví dụ tên dây chuyền sai. Câu trả lời có thể kèm "Tên dây chuyền đang có: …".

Chatbot không bao giờ coi ngày thiếu dữ liệu là bằng 0.

## Câu trả lời mặc định "Đây là kết quả truy vấn."

Chatbot không viết được lời tóm tắt thì hiện câu "Đây là kết quả truy vấn." kèm bảng kết quả. Đọc số trực tiếp trong bảng.
