---
id: bo-cuc-giao-dien
title: Bố cục chung của các trang
loai: tong-quan
trang: chung
he_thong: chung
aliases: [menu, thanh menu, header, footer, chân trang, thanh trên cùng, thông báo nổi, toast]
lien_quan: [dang-nhap, dang-xuat, doi-che-do-sang-toi, khung-chat-nhanh, popup-chao-mung]
nguon_code: [frontend/html/index.html, frontend/js/api.js, frontend/css/base.css]
cap_nhat: 2026-11-21
---
# Bố cục chung của các trang

Còn gọi là: menu, header, footer, chân trang, thanh trên cùng, thông báo góc màn hình.

Mọi trang của OCR Dashboard (trừ trang phong ấn) có chung thanh trên cùng, thanh menu, chân trang và khu vực thông báo.

## Thanh trên cùng màu đỏ (header)

Từ trái sang phải:
- **Logo Viettel Post**: bấm để về trang **"Thiên Cơ Các"** (dashboard).
- Chữ **"OCR Dashboard CNKT3"**. Trên điện thoại màn hình hẹp, chữ này bị ẩn.
- Nút **"Nhập Môn"** khi chưa đăng nhập, hoặc **"Xuất Môn"** khi đã đăng nhập. Nằm ở góc trên bên phải.
- Nút tròn hình mặt trăng hoặc mặt trời ở góc trên bên phải: đổi giao diện sáng / tối.

## Thanh menu dưới header

Thanh menu có năm mục: **"Thiên Cơ Các"**, **"Truyền Pháp Ảnh"**, **"Tàng Kinh Các"**, **"Vấn Đạo Đài"**, **"Đạo Vận Chi Lượng"**. Mục của trang đang mở có màu đỏ và gạch chân. Trang **Xem / sửa report** không có mục riêng trên menu.

## Chân trang (footer)

Chân trang nền tối, ở cuối mỗi trang, gồm:
- Tên đơn vị "Viettel Post CNKT 3" và link **"Xem địa chỉ trên Google Maps"**.
- Mục **"Gặp Kiếp Nạn"**: người cần liên hệ và email hỗ trợ khi hệ thống gặp sự cố.
- Mục **"Dẫn Lộ Bàn"**: link tới năm trang chính.
- Nút mũi tên lên **"Lên đầu trang"** ở góc phải dưới cùng của chân trang.

## Thông báo nổi ở góc phải dưới

Một số việc hiện thông báo nổi ở góc phải dưới màn hình, ví dụ đăng nhập thành công, đọc ảnh xong. Thông báo màu xanh hoặc vàng tự ẩn sau 8 giây. Thông báo lỗi màu đỏ giữ nguyên tới khi bấm **"×"**. Cùng lúc hiện tối đa 4 thông báo.

## Nút chat tròn ở góc phải dưới

Trên các trang Thiên Cơ Các, Truyền Pháp Ảnh, Tàng Kinh Các, Đạo Vận Chi Lượng và Xem / sửa report có nút tròn màu đỏ, hình bong bóng chat, ở góc phải dưới. Bấm để mở khung hỏi nhanh chatbot. Xem [Khung chat nhanh](../trang/khung-chat-nhanh.md).

## Popup chào mừng khi mở trang web

Lần đầu mở trang web trong một phiên trình duyệt, popup **"Chào mừng bạn đến với hệ thống Thiên Đạo"** hiện giữa màn hình. Xem [Popup chào mừng](../trang/popup-chao-mung.md).

## Khi chưa đăng nhập

Chưa đăng nhập thì các trang vẫn mở được nhưng không có số liệu: dashboard trống, không tải ảnh được, không hỏi chatbot được. Bấm **"Nhập Môn"** để đăng nhập.
