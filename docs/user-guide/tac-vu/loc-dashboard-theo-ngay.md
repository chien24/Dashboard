---
id: loc-dashboard-theo-ngay
title: Lọc dashboard theo khoảng ngày
loai: tac-vu
trang: Thiên Cơ Các
he_thong: chung
aliases: [lọc theo ngày, chọn ngày, khoảng ngày, Từ ngày Đến ngày, xem tuần trước, xem nhiều ngày]
lien_quan: [dashboard-thien-co-cac, xem-chi-so-cua-mot-ngay, loc-theo-day-chuyen, gioi-han-va-quy-tac]
nguon_code: [frontend/html/index.html, frontend/js/dashboard.js]
cap_nhat: 2026-11-20
---
# Lọc dashboard theo khoảng ngày

Còn gọi là: chọn ngày, khoảng ngày, "xem số liệu tuần trước", "xem từ ngày này tới ngày kia".

**Kết quả:** biểu đồ và bảng chi tiết của tab đang xem chỉ hiện các ngày trong khoảng đã chọn.
**Cần có trước:** đã đăng nhập, đang ở trang **"Thiên Cơ Các"**.

## Các bước lọc dashboard theo khoảng ngày

1. Mở trang **"Thiên Cơ Các"**, chọn tab **"HT1 – SCADA"** hoặc **"HT2 – DMWCS (CBS)"**.
2. Ở hàng lọc đầu tab, bấm ô **"Từ ngày"** và chọn ngày bắt đầu.
3. Bấm ô **"Đến ngày"** và chọn ngày kết thúc.
4. Biểu đồ, bảng và thẻ chỉ số vẽ lại ngay. Thẻ chỉ số chuyển về ngày mới nhất có dữ liệu trong khoảng.

## Nếu lọc dashboard theo khoảng ngày không như mong muốn

| Hiện tượng | Nguyên nhân | Cách xử lý |
| --- | --- | --- |
| Bảng ghi "Không có dữ liệu trong khoảng ngày đã chọn" | Chưa có ảnh của các ngày đó | Đổi khoảng ngày, hoặc tải ảnh lên |
| Chọn 2 tháng mà chỉ thấy khoảng 35 ngày | Biểu đồ chỉ hiện tối đa 35 ngày cuối của khoảng | Thu hẹp khoảng ngày |
| Ngày cũ không còn số liệu | Dữ liệu chỉ giữ 35 ngày | Không khôi phục được |
| Một ngày trên biểu đồ chỉ có dấu "—" | Ngày đó chưa có ảnh | Tải ảnh của ngày đó lên |
| Chọn "Từ ngày" sau "Đến ngày" | Trang tự đảo lại hai ngày | Không cần làm gì |

## Lưu ý khi lọc dashboard theo khoảng ngày

- Khoảng ngày mặc định khi mở trang: kết thúc ở ngày mới nhất có dữ liệu, lùi lại 7 ngày. Nếu có báo cáo cũ hơn thì lùi tới báo cáo cũ nhất, nhưng không quá 35 ngày.
- Tab HT1 và tab HT2 có ô ngày riêng, lọc độc lập với nhau.
- Khoảng ngày không được nhớ: tải lại trang thì về mặc định.
- Ngày được tính theo ngày báo cáo ghi trên ảnh, không phải ngày tải ảnh lên.
