---
id: dang-nhap
title: Đăng nhập (Nhập Môn)
loai: tac-vu
trang: Hộp thoại Nhập Môn
he_thong: chung
aliases: [đăng nhập, login, Nhập Môn, vào hệ thống, đăng nhập ở đâu]
lien_quan: [hop-dang-nhap, dang-xuat, sai-mat-khau, bi-khoa-dang-nhap, can-dang-nhap]
nguon_code: [frontend/js/api.js, backend/app/api/auth.py]
cap_nhat: 2026-11-20
---
# Đăng nhập (Nhập Môn)

Còn gọi là: login, vào hệ thống, "đăng nhập ở đâu", "làm sao để xem được số liệu".

**Kết quả:** trang tải lại, góc phải dưới hiện thông báo **"Nhập Môn thành công. Chào mừng đạo hữu!"**. Nút trên header đổi thành **"Xuất Môn"**. Số liệu, tải ảnh và chatbot dùng được.
**Cần có trước:** tài khoản và mật khẩu dùng chung của chi nhánh.

## Các bước đăng nhập

1. Mở trang bất kỳ của OCR Dashboard.
2. Bấm nút **"Nhập Môn"** ở góc trên bên phải, trên thanh màu đỏ. Hộp thoại **"Nhập Môn"** hiện giữa màn hình.
3. Gõ tên vào ô **"Tài khoản"**.
4. Gõ mật khẩu vào ô **"Mật khẩu"**.
5. Bấm nút **"Nhập Môn"** trong hộp thoại, hoặc nhấn Enter. Trang tải lại và hiện thông báo thành công.

Cách khác: khi popup chào mừng hiện ra, bấm **"Bắt đầu ngay"** để mở thẳng hộp thoại Nhập Môn.

## Nếu đăng nhập không thành công

| Hiện tượng | Nguyên nhân | Cách xử lý |
| --- | --- | --- |
| Dòng đỏ "Tư chất quá kém, tiên duyên chưa đủ, mời ngươi quay về đi!" | Sai tài khoản hoặc mật khẩu | Gõ lại; kiểm tra phím Caps Lock, bộ gõ tiếng Việt. Xem [lỗi sai mật khẩu](../loi/sai-mat-khau.md) |
| Bị chuyển sang trang "Thiên Đạo phong ấn" | Sai 8 lần trong 5 phút | Chờ hết 5 phút. Xem [bị khóa đăng nhập](../loi/bi-khoa-dang-nhap.md) |
| Hộp thoại hiện lỗi khác | Mất mạng hoặc máy chủ đang tắt | Kiểm tra mạng, thử lại sau; báo người hỗ trợ ở mục "Gặp Kiếp Nạn" cuối trang |
| Không thấy nút "Nhập Môn" | Đã đăng nhập rồi (nút ghi "Xuất Môn") | Không cần làm gì |

## Lưu ý khi đăng nhập

- Đăng nhập giữ được 7 ngày trên trình duyệt đó, rồi phải đăng nhập lại.
- Nhiều máy đăng nhập cùng lúc được.
- Muốn đổi mật khẩu: gửi email cho người viết code (Khoa) tại chiencodedao@gmail.com. Trang web không có chức năng tự đổi mật khẩu.
- Chưa đăng nhập vẫn mở được các trang, nhưng không thấy số liệu, không tải ảnh và không hỏi chatbot được.
- Hết phiên khi đang dùng thì có thể gặp lỗi "Cần đăng nhập". Xem [lỗi Cần đăng nhập](../loi/can-dang-nhap.md).
