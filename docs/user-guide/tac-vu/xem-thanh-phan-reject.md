---
id: xem-thanh-phan-reject
title: Xem thành phần REJECT
loai: tac-vu
trang: Thiên Cơ Các
he_thong: chung
aliases: [REJECT theo loại, thành phần lỗi, NoRead, NoPostOffice, NoChute, không có mã vạch, yêu cầu ống dẫn thất bại, lý do reject]
lien_quan: [dashboard-tab-ht1, dashboard-tab-ht2, chi-so-ht1-scada, chi-so-ht2-dmwcs, thuat-ngu]
nguon_code: [frontend/html/index.html, frontend/js/dashboard.js, frontend/js/history.js]
cap_nhat: 2026-11-20
---
# Xem thành phần REJECT

Còn gọi là: REJECT theo loại, lý do reject, "REJECT gồm những gì", NoRead, NoChute.

**Kết quả:** biết số bưu kiện REJECT mỗi ngày đến từ những nguyên nhân nào.
**Cần có trước:** đã đăng nhập, đã có ảnh SCADA (HT1) hoặc Sorted (HT2).

## Các bước xem thành phần REJECT của HT1

1. Mở trang **"Thiên Cơ Các"**, tab **"HT1 – SCADA"**.
2. Xem khung **"REJECT theo loại"**, bên phải khung "Sản lượng theo ngày".
3. Mỗi cột chồng hai phần: **"Không có mã vạch"** và **"Yêu cầu ống dẫn thất bại"**.
4. Thẻ **"REJECT"** ở đầu tab cũng ghi rõ hai số này của ngày đang chọn.

## Các bước xem thành phần REJECT của HT2

1. Mở trang **"Thiên Cơ Các"**, tab **"HT2 – DMWCS (CBS)"**.
2. Xem khung **"Thành phần REJECT"**, bên phải khung "Sản lượng theo ngày".
3. Mỗi cột chồng ba phần: **"NoRead"**, **"NoPostOffice"**, **"NoChute"**. Ba phần cộng lại bằng REJECT (RejectChute).
4. Muốn xem danh sách số máng NoChute: mở báo cáo Sorted của ngày đó ở trang **"Tàng Kinh Các"**, mục **"Máng NoChute"**.

## Nếu thành phần REJECT không khớp

| Hiện tượng | Nguyên nhân | Cách xử lý |
| --- | --- | --- |
| HT2: ba phần cộng lại khác REJECT | Hệ thống đọc sai một số trên ảnh | Báo cáo sẽ có cảnh báo; mở và sửa tay |
| HT1: REJECT nhỏ hơn số bưu kiện bất thường | Đúng thiết kế: REJECT chỉ tính 2 loại | Không cần làm gì |
| Danh sách máng NoChute thiếu máng cuối | Ô trên màn hình DMWCS bị cắt ở mép phải | Đối chiếu trực tiếp trên máy DMWCS |

## Lưu ý khi xem thành phần REJECT

- HT1: REJECT chỉ gồm "Không có mã vạch" và "Yêu cầu ống dẫn thất bại". Các loại bất thường khác (ví dụ "Không có Báo cáo Phân loại") không tính vào REJECT, chỉ xem ở Tàng Kinh Các.
- HT2: tỷ lệ NoRead, NoPostOffice, NoChute trên ảnh là % trên RejectChute, không phải trên Total.
- Định nghĩa đầy đủ: [Chỉ số HT1](../tham-chieu/chi-so-ht1-scada.md), [Chỉ số HT2](../tham-chieu/chi-so-ht2-dmwcs.md).
