---
id: gioi-thieu
title: Giới thiệu trang web OCR Dashboard CNKT3
loai: tong-quan
trang: chung
he_thong: chung
aliases: [OCR Dashboard, dashboard CNKT3, hệ thống Thiên Đạo, trang web vận hành, web báo cáo chia chọn]
lien_quan: [bat-dau-nhanh, bo-cuc-giao-dien, thuat-ngu, chi-so-ht1-scada, chi-so-ht2-dmwcs]
nguon_code: [frontend/html/index.html, frontend/html/upload.html, frontend/html/history.html, frontend/html/chat.html, frontend/html/thoi-gian.html, frontend/js/api.js]
cap_nhat: 2026-11-21
---
# Giới thiệu trang web OCR Dashboard CNKT3

Còn gọi là: OCR Dashboard, hệ thống Thiên Đạo, web báo cáo vận hành, dashboard CNKT3.

**OCR Dashboard CNKT3** là trang web của Phòng Kỹ thuật, Chi nhánh Khai thác 3, Viettel Post. Trang web gom số liệu vận hành của hai hệ thống chia chọn bưu kiện vào một chỗ, vẽ thành biểu đồ và bảng.

## Trang web OCR Dashboard dùng để làm gì

Người dùng chụp màn hình báo cáo của máy chia chọn, rồi tải ảnh lên trang web. Hệ thống tự đọc số liệu từ ảnh. Số liệu đọc được hiện trên dashboard dưới dạng thẻ chỉ số, biểu đồ và bảng.

Trang web giúp:
- Xem sản lượng, số bưu kiện lỗi (REJECT), công suất theo ngày.
- So sánh các dây chuyền với nhau.
- Kiểm tra lại số liệu hệ thống đọc từ ảnh, sửa tay khi đọc sai.
- Hỏi đáp số liệu bằng tiếng Việt với chatbot.

## Hai hệ thống HT1 và HT2 trên OCR Dashboard

- **HT1 – SCADA**: hệ thống chia chọn có nhiều dây chuyền, ví dụ Outbound, Inbound, CBS1 2st layer, CBS2 1st layer. Mỗi ảnh SCADA là báo cáo của một dây chuyền trong một ngày.
- **HT2 – DMWCS (CBS)**: hệ thống của máy CBS, không chia dây chuyền. HT2 có ba loại ảnh báo cáo: Sorted (sản lượng), Capacity (công suất trung bình theo ngày) và BCR rate (tỷ lệ đọc mã vạch của từng Scanner).

## Các trang chính của OCR Dashboard

Thanh menu có năm trang:
- **"Thiên Cơ Các"**: dashboard, xem chỉ số và biểu đồ HT1, HT2.
- **"Truyền Pháp Ảnh"**: tải ảnh báo cáo lên để hệ thống đọc.
- **"Tàng Kinh Các"**: lịch sử các báo cáo trong 35 ngày, mở để xem chi tiết hoặc sửa.
- **"Vấn Đạo Đài"**: chatbot hỏi đáp số liệu.
- **"Đạo Vận Chi Lượng"**: cộng cột thời lượng của file Excel xuất từ máy, vẽ biểu đồ. Không cần đăng nhập, không lưu file.

Ngoài ra có trang **Xem / sửa report** để sửa số liệu của một báo cáo, và nút chat tròn ở góc phải dưới để hỏi nhanh.

## Ai dùng OCR Dashboard

Nhân viên vận hành và kỹ thuật của chi nhánh. Cả chi nhánh dùng chung một tài khoản. Phải **"Nhập Môn"** (đăng nhập) mới xem được số liệu, tải ảnh và hỏi chatbot.

## Tên gọi kiểu tiên hiệp trên OCR Dashboard

Trang web dùng tên kiểu tiên hiệp cho vui. Bảng đối chiếu:
- "Nhập Môn" = đăng nhập; "Xuất Môn" = đăng xuất.
- "Thiên Cơ Các" = Dashboard; "Truyền Pháp Ảnh" = tải ảnh lên; "Tàng Kinh Các" = lịch sử báo cáo; "Vấn Đạo Đài" = chatbot. "Đạo Vận Chi Lượng" = tính tổng thời gian sử dụng từ file Excel.
- "Khai Phá Thiên Cơ" = bắt đầu đọc ảnh; "Xóa Bỏ Phế Tích" = xóa danh sách ảnh trên màn hình.
- "Thần Niệm" = để hệ thống tự nhận diện loại ảnh.

Xem thêm [Thuật ngữ](../thuat-ngu.md).

## Dữ liệu được giữ bao lâu trên OCR Dashboard

Số liệu và ảnh chỉ được giữ **35 ngày** tính theo ngày báo cáo. Dữ liệu cũ hơn tự động bị xóa mỗi đêm. Xem [Giới hạn và quy tắc](../tham-chieu/gioi-han-va-quy-tac.md).
