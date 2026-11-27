---
id: thuat-ngu
title: Thuật ngữ
loai: thuat-ngu
trang: chung
he_thong: chung
aliases: [từ điển, giải thích từ, nghĩa là gì, NoRead là gì, PDA là gì, BCR là gì, thuật ngữ tiên hiệp]
lien_quan: [gioi-thieu, chi-so-ht1-scada, chi-so-ht2-dmwcs, trang-thai]
nguon_code: [frontend/html/index.html, frontend/js/dashboard.js, frontend/js/api.js]
cap_nhat: 2026-11-20
---
# Thuật ngữ

Còn gọi là: từ điển, "… là gì", giải thích từ ngữ trên OCR Dashboard.

## Thuật ngữ về hệ thống và báo cáo

- **HT1 – SCADA**: hệ thống chia chọn có nhiều dây chuyền. Ảnh báo cáo là màn hình "Thống kê và phân tích dữ liệu".
- **HT2 – DMWCS (CBS)**: hệ thống của máy CBS, không chia dây chuyền. Có ba loại ảnh báo cáo: Sorted, Capacity, BCR rate.
- **Dây chuyền**: một line chia chọn của HT1, ví dụ Outbound, Inbound, CBS1 2st layer, CBS2 1st layer.
- **Báo cáo (report)**: kết quả đọc một ảnh. Mỗi ảnh tải lên tạo một báo cáo.
- **Kỳ báo cáo**: khoảng thời gian một báo cáo thống kê, thường là một ngày (00:00 tới hết ngày).
- **Ngày báo cáo**: ngày của kỳ báo cáo, lấy từ ô thời gian trên ảnh. Không phải ngày tải ảnh lên.
- **OCR**: việc hệ thống tự đọc chữ và số trên ảnh.
- **Sorted**: ảnh "The Report of Sorted parcels" của HT2, có Total, CorrectChute, PDA, RejectChute.
- **Capacity**: ảnh "The Report of Capacity" của HT2, có công suất trung bình từng ngày.
- **BCR rate / Hours&BcrRate**: ảnh bảng tỷ lệ đọc mã vạch của từng Scanner (HT2).

## Thuật ngữ về chỉ số

- **ALL**: tổng bưu kiện. HT1 là "Số lượng đã quét"; HT2 là Total.
- **CORRECT**: bưu kiện chia đúng. HT1 = ALL − REJECT; HT2 = CorrectChute + PDA.
- **REJECT**: bưu kiện lỗi. HT1 = Không có mã vạch + Yêu cầu ống dẫn thất bại; HT2 = RejectChute.
- **CorrectChute**: bưu kiện vào đúng máng (HT2).
- **PDA**: bưu kiện xử lý qua máy PDA (chia tay), tính vào CORRECT (HT2).
- **RejectChute**: bưu kiện rơi vào máng lỗi (HT2).
- **NoRead**: không đọc được mã vạch (thành phần REJECT HT2).
- **NoPostOffice**: không có bưu cục phát (thành phần REJECT HT2).
- **NoChute**: không có máng cho bưu kiện (thành phần REJECT HT2). "Máng NoChute" là danh sách số máng.
- **SortFailed**: chia chọn thất bại. Chỉ để tham khảo, không dùng tính chỉ số.
- **Công suất MAX**: sản lượng lớn nhất trong 60 phút liên tục (HT1), bưu kiện/giờ.
- **Công suất AVG**: công suất trung bình trong ngày (HT2), bưu kiện/giờ.
- **Thời gian sử dụng**: số giờ máy chạy ước tính. HT1 = ALL / Công suất MAX; HT2 = ALL / Công suất AVG.
- **Scanner / BCR / BCR_NO**: đầu đọc mã vạch và số hiệu của nó.
- **RATE**: tỷ lệ đọc thành công của Scanner = SUCCESS / TOTAL.
- **Bất thường (HT1)**: bưu kiện gặp ít nhất một sự cố, chia thành nhiều loại. Chỉ 2 loại tính vào REJECT.

## Thuật ngữ về trạng thái

- **OK / ok**: số liệu khớp, không cần kiểm tra.
- **Cần kiểm tra / can_kiem_tra**: số có thể sai, nên so với ảnh.
- **Đã sửa tay / da_sua_tay**: người dùng đã lưu số bằng tay.
- **Đã được thay**: báo cáo cũ, đã có ảnh mới hơn cùng kỳ thay trên dashboard.
- **Ảnh trùng**: ảnh có nội dung giống hệt ảnh đã tải trước đó.
- **Lệch giữa lần 1 và lần 2**: hai lần đọc cùng một ảnh ra số khác nhau.

## Tên gọi kiểu tiên hiệp trên giao diện

| Tên trên giao diện | Nghĩa thường |
| --- | --- |
| Nhập Môn / Xuất Môn | Đăng nhập / Đăng xuất |
| Thiên Cơ Các | Trang Dashboard |
| Truyền Pháp Ảnh / Truyền Tống Linh Ảnh / Nạp Linh Ảnh | Trang tải ảnh lên |
| Tàng Kinh Các / Thiên Đạo Ký Sơ | Trang lịch sử báo cáo |
| Vấn Đạo Đài | Trang chatbot |
| Khai Phá Thiên Cơ | Bắt đầu đọc ảnh |
| Xóa Bỏ Phế Tích | Xóa danh sách ảnh trên màn hình |
| Thần Niệm | Tự nhận diện loại ảnh |
| Thiên Cơ lệnh | Một lượt đọc ảnh |
| Truy tìm bí pháp | Tìm kiếm báo cáo |
| Thiên Đạo phong ấn | Trang khóa khi sai mật khẩu 8 lần |
| Gặp Kiếp Nạn | Mục liên hệ hỗ trợ ở chân trang |
| Dẫn Lộ Bàn | Mục link nhanh ở chân trang |
| Đạo hữu | Người dùng |
