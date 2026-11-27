---
id: hop-dang-nhap
title: Hộp thoại Nhập Môn (đăng nhập)
loai: trang
trang: Hộp thoại Nhập Môn
he_thong: chung
aliases: [hộp đăng nhập, form đăng nhập, login, Nhập Môn, cửa sổ đăng nhập]
lien_quan: [dang-nhap, dang-xuat, sai-mat-khau, bi-khoa-dang-nhap, trang-phong-an]
nguon_code: [frontend/js/api.js]
cap_nhat: 2026-11-20
---
# Hộp thoại Nhập Môn (đăng nhập)

Còn gọi là: hộp đăng nhập, form đăng nhập, login.

Hộp thoại **Nhập Môn** là cửa sổ đăng nhập của OCR Dashboard. Cả chi nhánh dùng chung một tài khoản.

## Cách mở hộp thoại Nhập Môn

- Bấm nút **"Nhập Môn"** ở góc trên bên phải, trên thanh màu đỏ. Nút "Nhập Môn" chỉ hiện khi chưa đăng nhập.
- Trong popup chào mừng, bấm **"Bắt đầu ngay"** khi chưa đăng nhập.

## Bố cục hộp thoại Nhập Môn

Hộp thoại nằm giữa màn hình, nền phía sau tối đi. Từ trên xuống: tiêu đề **"Nhập Môn"**, ô **"Tài khoản"**, ô **"Mật khẩu"**, chỗ hiện lỗi, và hai nút **"Hủy"**, **"Nhập Môn"** ở góc dưới bên phải.

## Các nút và ô nhập trong hộp thoại Nhập Môn

| Phần tử | Vị trí | Dùng để | Khi bấm/nhập thì |
| --- | --- | --- | --- |
| Ô **"Tài khoản"** | Dưới tiêu đề | Nhập tên tài khoản | Bắt buộc |
| Ô **"Mật khẩu"** | Dưới ô Tài khoản | Nhập mật khẩu (ẩn ký tự) | Bắt buộc |
| Nút **"Hủy"** | Góc dưới, bên trái nút Nhập Môn | Đóng hộp thoại | Không đăng nhập |
| Nút **"Nhập Môn"** | Góc dưới bên phải | Đăng nhập | Đúng: trang tải lại, báo "Nhập Môn thành công. Chào mừng đạo hữu!" |

## Thông báo trong hộp thoại Nhập Môn

Sai tài khoản hoặc mật khẩu, hộp thoại hiện dòng đỏ **"Tư chất quá kém, tiên duyên chưa đủ, mời ngươi quay về đi!"**. Dòng vàng bên dưới đổi theo số lần sai:
- Lần 1: "Nghịch thiên cải mệnh? Ta cho ngươi 7 lần giãy giụa nữa!"
- Lần 2 tới lần 6: các câu răn đe khác nhau, càng về sau càng nặng lời.
- Lần 7: "Thiên uy khó phạm, ngươi chỉ còn duy nhất một lần cuối!"
- Lần 8: chuyển sang trang **"Thiên Đạo phong ấn"**, khóa đăng nhập 5 phút.

Sau mỗi lần sai, ô mật khẩu được bôi đen để gõ lại ngay. Lỗi mạng hoặc máy chủ thì hiện nội dung lỗi thay cho câu trên.

## Lưu ý về đăng nhập

- Một lần đăng nhập giữ được 7 ngày trên trình duyệt đó.
- Đăng nhập được trên nhiều máy cùng lúc.
- Số lần sai được đếm trong 5 phút gần nhất, riêng cho từng máy.

## Việc thường làm với hộp thoại Nhập Môn

- [Đăng nhập (Nhập Môn)](../tac-vu/dang-nhap.md)
- [Lỗi sai mật khẩu](../loi/sai-mat-khau.md)
- [Bị chuyển sang trang Thiên Đạo phong ấn](../loi/bi-khoa-dang-nhap.md)
