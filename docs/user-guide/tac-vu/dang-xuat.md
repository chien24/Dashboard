---
id: dang-xuat
title: Đăng xuất (Xuất Môn)
loai: tac-vu
trang: chung
he_thong: chung
aliases: [đăng xuất, logout, Xuất Môn, thoát tài khoản]
lien_quan: [dang-nhap, hop-dang-nhap, bo-cuc-giao-dien]
nguon_code: [frontend/js/api.js, backend/app/api/auth.py]
cap_nhat: 2026-11-20
---
# Đăng xuất (Xuất Môn)

Còn gọi là: logout, thoát tài khoản, "làm sao để đăng xuất".

**Kết quả:** trang tải lại, góc phải dưới hiện thông báo **"Xuất Môn thành công. Hẹn ngày tái ngộ!"**. Nút trên header đổi lại thành **"Nhập Môn"**. Số liệu không còn hiện trên trình duyệt đó.
**Cần có trước:** đang đăng nhập.

## Các bước đăng xuất

1. Trên trang bất kỳ, nhìn góc trên bên phải, trên thanh màu đỏ.
2. Bấm nút **"Xuất Môn"**. Trang tải lại và hiện thông báo "Xuất Môn thành công. Hẹn ngày tái ngộ!".

## Nếu đăng xuất không thành công

| Hiện tượng | Nguyên nhân | Cách xử lý |
| --- | --- | --- |
| Không thấy nút "Xuất Môn", chỉ thấy "Nhập Môn" | Chưa đăng nhập, hoặc phiên đã hết | Không cần đăng xuất |
| Sau khi bấm vẫn thấy số liệu cũ | Trang chưa tải lại hẳn | Tải lại trang (F5) |

## Lưu ý khi đăng xuất

- Đăng xuất chỉ áp dụng cho trình duyệt đang dùng. Các máy khác đang đăng nhập không bị ảnh hưởng.
- Nên đăng xuất khi dùng máy chung, vì một lần đăng nhập giữ được 7 ngày.
- Lịch sử chatbot vẫn nhớ trên trình duyệt đó. Đăng nhập lại là xem tiếp được ở trang **"Vấn Đạo Đài"**.
