---
id: sai-mat-khau
title: Lỗi "Tư chất quá kém, tiên duyên chưa đủ, mời ngươi quay về đi!"
loai: loi
trang: Hộp thoại Nhập Môn
he_thong: chung
aliases: [sai mật khẩu, sai tài khoản, đăng nhập sai, không đăng nhập được, tư chất quá kém, login failed]
lien_quan: [dang-nhap, hop-dang-nhap, bi-khoa-dang-nhap]
nguon_code: [frontend/js/api.js, backend/app/api/auth.py]
cap_nhat: 2026-11-20
---
# Lỗi "Tư chất quá kém, tiên duyên chưa đủ, mời ngươi quay về đi!"

Còn gọi là: sai mật khẩu, sai tài khoản, đăng nhập không được.

**Xuất hiện ở:** hộp thoại **"Nhập Môn"**, sau khi bấm nút **"Nhập Môn"** để đăng nhập.

**Nghĩa là:** tài khoản hoặc mật khẩu không đúng. Dòng chữ vàng bên dưới cho biết đã sai mấy lần, ví dụ lần đầu: "Nghịch thiên cải mệnh? Ta cho ngươi 7 lần giãy giụa nữa!". Lần thứ 7: "Thiên uy khó phạm, ngươi chỉ còn duy nhất một lần cuối!".

**Nguyên nhân thường gặp:**
- Gõ sai mật khẩu, hoặc mật khẩu đã được đổi.
- Đang bật Caps Lock.
- Bộ gõ tiếng Việt (Unikey, EVKey) tự đổi chữ khi gõ mật khẩu.
- Thừa khoảng trắng ở đầu hoặc cuối tài khoản. Hệ thống tự bỏ khoảng trắng ở tài khoản, nhưng không bỏ ở mật khẩu.

**Cách xử lý:**
1. Tắt Caps Lock, tắt bộ gõ tiếng Việt.
2. Gõ lại mật khẩu. Ô mật khẩu được bôi đen sẵn sau mỗi lần sai, gõ đè là được.
3. Bấm **"Nhập Môn"**.

**Nếu vẫn lỗi:** dừng lại trước khi sai đủ 8 lần trong 5 phút, vì lần thứ 8 sẽ bị khóa 5 phút. Hỏi lại mật khẩu đúng từ người viết code (Khoa), email chiencodedao@gmail.com, cũng ghi ở mục **"Gặp Kiếp Nạn"** cuối trang. Xem [Bị chuyển sang trang Thiên Đạo phong ấn](bi-khoa-dang-nhap.md).
