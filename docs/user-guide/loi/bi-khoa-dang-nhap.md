---
id: bi-khoa-dang-nhap
title: Bị chuyển sang trang "Thiên Đạo phong ấn"
loai: loi
trang: Thiên Đạo phong ấn
he_thong: chung
aliases: [bị khóa đăng nhập, bị nhốt, sai 8 lần, đếm ngược 5 phút, Sai quá 8 lần khóa đăng nhập, không thoát được trang]
lien_quan: [trang-phong-an, sai-mat-khau, dang-nhap]
nguon_code: [frontend/html/jail.html, frontend/js/api.js, backend/app/api/auth.py]
cap_nhat: 2026-11-20
---
# Bị chuyển sang trang "Thiên Đạo phong ấn"

Còn gọi là: bị khóa đăng nhập, bị nhốt, "Sai quá 8 lần, khóa đăng nhập … giây".

**Xuất hiện ở:** sau khi bấm **"Nhập Môn"** trong hộp thoại đăng nhập. Trình duyệt chuyển sang trang có đồng hồ đếm ngược **"05:00"** và dòng "Sai mật khẩu 8 lần. Hết thời gian phong ấn, ngươi sẽ được thả về."

**Nghĩa là:** máy này đã nhập sai tài khoản hoặc mật khẩu 8 lần trong 5 phút. Đăng nhập trên máy này bị khóa 5 phút. Số lần sai tính riêng cho từng máy, các máy khác vẫn đăng nhập bình thường. Trong thời gian này, mở trang nào của OCR Dashboard trên trình duyệt đó cũng quay về trang phong ấn.

**Nguyên nhân thường gặp:**
- Quên mật khẩu, thử nhiều lần.
- Mật khẩu đã được đổi mà chưa được báo.

**Cách xử lý:**
1. Chờ đồng hồ đếm ngược về 00:00. Nút Back không thoát được trang.
2. Hết giờ, trang tự chuyển về **"Thiên Cơ Các"**.
3. Bấm **"Nhập Môn"**, gõ đúng tài khoản và mật khẩu.

**Nếu vẫn lỗi:** hỏi mật khẩu đúng từ người quản lý tài khoản, hoặc người hỗ trợ ở mục **"Gặp Kiếp Nạn"** cuối trang. Đừng thử tiếp khi chưa chắc mật khẩu, vì sai thêm 8 lần sẽ bị khóa lại.
