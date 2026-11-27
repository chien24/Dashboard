---
id: trang-phong-an
title: Trang Thiên Đạo phong ấn
loai: trang
trang: Thiên Đạo phong ấn
he_thong: chung
aliases: [trang phạt, bị nhốt, trang khóa, màn hình đếm ngược, jail, phong ấn]
lien_quan: [bi-khoa-dang-nhap, sai-mat-khau, dang-nhap, hop-dang-nhap]
nguon_code: [frontend/html/jail.html, frontend/js/api.js]
cap_nhat: 2026-11-20
---
# Trang Thiên Đạo phong ấn

Còn gọi là: trang phạt, trang khóa, bị nhốt, màn hình đếm ngược.

Trang **Thiên Đạo phong ấn** hiện ra khi nhập sai mật khẩu 8 lần. Trong thời gian phong ấn không dùng được trang web.

## Khi nào trang Thiên Đạo phong ấn hiện ra

Trong hộp thoại **"Nhập Môn"**, nhập sai tài khoản hoặc mật khẩu 8 lần trong 5 phút thì trình duyệt tự chuyển sang trang Thiên Đạo phong ấn. Máy chủ cũng khóa đăng nhập 5 phút cho máy đó.

## Bố cục trang Thiên Đạo phong ấn

- Nền là video toàn màn hình.
- Giữa màn hình: một lời phán chữ in hoa trong khung đỏ, hiện 10 giây rồi mờ dần.
- Phía dưới: chữ **"Thiên Đạo phong ấn"**, đồng hồ đếm ngược bắt đầu từ **"05:00"**, và dòng "Sai mật khẩu 8 lần. Hết thời gian phong ấn, ngươi sẽ được thả về."
- Góc trên bên phải: nút **"Bật âm thanh"** (hoặc **"Tắt âm thanh"** khi nhạc đang phát).

## Các nút trên trang Thiên Đạo phong ấn

| Phần tử | Vị trí | Dùng để | Khi bấm thì |
| --- | --- | --- | --- |
| Nút **"Bật âm thanh"** / **"Tắt âm thanh"** | Góc trên bên phải | Bật / tắt nhạc nền | Đổi chữ trên nút |

Trình duyệt có thể chặn tự phát nhạc. Khi đó nhạc phát ở lần bấm chuột hoặc gõ phím đầu tiên.

## Rời trang Thiên Đạo phong ấn

- Nút Back của trình duyệt không rời được trang Thiên Đạo phong ấn.
- Mở các trang khác của OCR Dashboard trên cùng trình duyệt cũng tự quay về trang phong ấn.
- Hết giờ đếm ngược, trang tự chuyển về **"Thiên Cơ Các"** (dashboard). Sau đó đăng nhập lại với đúng mật khẩu.

## Việc nên làm khi bị phong ấn

Chờ hết 5 phút. Trong lúc chờ, hỏi lại người quản lý tài khoản để có mật khẩu đúng. Xem [Bị chuyển sang trang Thiên Đạo phong ấn](../loi/bi-khoa-dang-nhap.md).
