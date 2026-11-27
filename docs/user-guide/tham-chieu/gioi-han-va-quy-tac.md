---
id: gioi-han-va-quy-tac
title: Giới hạn và quy tắc của hệ thống
loai: tham-chieu
trang: chung
he_thong: chung
aliases: [giới hạn, quy định, dung lượng ảnh tối đa, định dạng ảnh, lưu bao lâu, 35 ngày, ảnh trùng, số lần đọc, khóa đăng nhập, giới hạn chatbot]
lien_quan: [tai-anh-len, tai-lai-anh-da-tai-truoc-do, so-lieu-nao-duoc-hien-thi, chatbot-hoi-duoc-gi, dang-nhap]
nguon_code: [frontend/js/upload.js, frontend/js/dashboard.js, frontend/js/history.js, frontend/js/chat.js, backend/app/config.py, backend/app/api/upload.py, backend/app/api/auth.py, backend/app/services/retention.py, backend/app/chatbot/router.py]
cap_nhat: 2026-11-20
---
# Giới hạn và quy tắc của hệ thống

Còn gọi là: giới hạn, quy định, "ảnh tối đa bao nhiêu MB", "dữ liệu lưu bao lâu", "có tải nhiều ảnh cùng lúc được không".

## Giới hạn khi tải ảnh lên

- **Định dạng**: .jpg, .jpeg, .png, .webp. File khác bị bỏ qua. File đổi đuôi mà không phải ảnh thật bị từ chối.
- **Dung lượng**: tối đa 10 MB mỗi ảnh.
- **Số lượng**: chọn được nhiều ảnh cùng lúc. Ảnh được gửi và đọc lần lượt từng ảnh.
- **Ảnh trùng**: ảnh giống hệt nội dung ảnh đã tải (không xét tên file) thì không đọc lại, trừ khi bấm **"OCR lại"**.
- **Số lần đọc**: mỗi ảnh đọc 2 lần rồi so với nhau. Chọn "Thần Niệm (tự nhận diện)" thì thêm 1 lần để nhận diện loại.
- **Hàng đợi**: cả chi nhánh dùng chung một hàng đợi. Ảnh của người khác đang xử lý thì ảnh mới phải chờ.

## Thời gian lưu dữ liệu

- Báo cáo và ảnh được giữ **35 ngày**, tính theo **ngày báo cáo** ghi trên ảnh, không phải ngày tải lên.
- Mỗi ngày lúc 2 giờ sáng, hệ thống tự xóa báo cáo, ảnh và công suất của các ngày cũ hơn 35 ngày.
- Cuộc trò chuyện với chatbot không dùng quá **30 ngày** thì bị xóa.
- Dữ liệu đã xóa không khôi phục được.

## Quy tắc hiển thị trên dashboard

- Dashboard hiện tối đa 35 ngày cuối của khoảng ngày đã chọn.
- Một ngày không có ảnh hiện dấu "—", không phải số 0.
- Nhiều ảnh cùng kỳ báo cáo: chỉ một ảnh được dùng. Xem [Số nào được hiển thị](so-lieu-nao-duoc-hien-thi.md).
- Biểu đồ Scanner có màu riêng cho Scanner 1 tới 6; Scanner 7 trở lên màu xám.

## Quy tắc sửa số liệu

- Lưu số đã sửa thì trạng thái thành "Đã sửa tay".
- Hai người cùng mở một báo cáo: người lưu trước thành công. Người lưu sau nhận lỗi "Report này vừa được sửa ở máy khác…" và phải tải lại trang.
- Xóa báo cáo là vĩnh viễn.

## Quy tắc đăng nhập

- Cả chi nhánh dùng một tài khoản chung. Đăng nhập nhiều máy cùng lúc được.
- Một lần đăng nhập giữ 7 ngày trên trình duyệt đó.
- Sai mật khẩu 8 lần trong 5 phút thì máy đó bị khóa đăng nhập 5 phút, trình duyệt chuyển sang trang "Thiên Đạo phong ấn". Số lần sai tính riêng cho từng máy.
- Chỉ người viết code (Khoa) đổi được mật khẩu. Muốn đổi mật khẩu: gửi email tới chiencodedao@gmail.com.
- Chưa đăng nhập: các trang mở được nhưng không có số liệu, không tải ảnh, không hỏi chatbot.

## Giới hạn của chatbot

- Câu hỏi tối đa 1000 ký tự.
- Tối đa 10 câu hỏi mỗi phút từ một máy.
- Bảng kết quả hiện tối đa 200 dòng; lịch sử chỉ lưu 50 dòng đầu của mỗi bảng.
- Dịch vụ AI có giới hạn lượt dùng mỗi ngày. Hết lượt thì phải chờ.
- Chatbot chỉ đọc dữ liệu, không sửa, không xóa.
- Mỗi máy mở một cuộc trò chuyện riêng, nhưng danh sách lịch sử chung cho mọi máy (dùng chung tài khoản).

## Giới hạn của trang Tàng Kinh Các

Danh sách tải 50 báo cáo mỗi lần. Bấm **"Tải thêm (còn N)"** để xem tiếp. Tìm kiếm chỉ theo tên file ảnh.
