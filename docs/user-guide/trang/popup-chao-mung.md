---
id: popup-chao-mung
title: Popup chào mừng
loai: trang
trang: Popup chào mừng
he_thong: chung
aliases: [cửa sổ chào mừng, màn hình chào, welcome, popup Thiên Đạo, hộp chào mừng]
lien_quan: [hop-dang-nhap, dang-nhap, bo-cuc-giao-dien]
nguon_code: [frontend/js/api.js]
cap_nhat: 2026-11-20
---
# Popup chào mừng

Còn gọi là: cửa sổ chào mừng, màn hình chào, popup Thiên Đạo.

**Popup chào mừng** là cửa sổ hiện giữa màn hình khi mới mở trang web, có logo Thiên Đạo và lời chào.

## Khi nào popup chào mừng hiện ra

Popup chỉ hiện ở lần đầu mở trang web trong một phiên trình duyệt. Tải lại trang hay chuyển trang thì không hiện lại. Đóng hẳn trình duyệt rồi mở lại thì popup hiện lại.

Nếu trình duyệt chặn lưu dữ liệu trang web, popup không hiện.

## Bố cục popup chào mừng

Từ trên xuống: nút **"✕"** ở góc trên bên phải, logo Thiên Đạo, tiêu đề **"Chào mừng bạn đến với hệ thống Thiên Đạo"**, dòng "Chào mừng bạn đã gia nhập hệ thống giám sát và vận hành Thiên Đạo. Hãy cùng khám phá và tối ưu hóa hiệu suất ngay hôm nay!", nút **"Bắt đầu ngay"** và chữ **"Bỏ qua"**.

## Các nút trên popup chào mừng

| Phần tử | Vị trí | Dùng để | Khi bấm thì |
| --- | --- | --- | --- |
| Nút **"Bắt đầu ngay"** | Dưới lời chào | Bắt đầu dùng | Đóng popup. Chưa đăng nhập thì mở luôn hộp thoại "Nhập Môn" |
| Chữ **"Bỏ qua"** | Bên phải nút Bắt đầu ngay | Đóng popup | Chỉ đóng popup |
| Nút **"✕"** | Góc trên bên phải popup | Đóng popup | Chỉ đóng popup |
| Vùng nền tối bên ngoài popup | Quanh popup | Đóng nhanh | Bấm ra ngoài là đóng |

Phím Esc cũng đóng được popup.

## Việc thường làm sau popup chào mừng

- [Đăng nhập (Nhập Môn)](../tac-vu/dang-nhap.md)
- [Bắt đầu nhanh](../00-tong-quan/bat-dau-nhanh.md)
