---
id: xem-chi-so-cua-mot-ngay
title: Xem chỉ số của một ngày cụ thể
loai: tac-vu
trang: Thiên Cơ Các
he_thong: chung
aliases: [thẻ chỉ số, KPI, xem số ngày hôm qua, chọn ngày trên biểu đồ, bấm vào cột, chỉ số ngày]
lien_quan: [dashboard-tab-ht1, dashboard-tab-ht2, loc-dashboard-theo-ngay, chi-so-ht1-scada, chi-so-ht2-dmwcs]
nguon_code: [frontend/js/dashboard.js]
cap_nhat: 2026-11-20
---
# Xem chỉ số của một ngày cụ thể

Còn gọi là: thẻ chỉ số, KPI, "xem số của hôm qua", "bấm vào cột trên biểu đồ".

**Kết quả:** năm thẻ chỉ số ở đầu tab hiện số của ngày đã chọn. Dòng "Chỉ số ngày dd/mm/yyyy" ghi rõ ngày.
**Cần có trước:** đã đăng nhập, ngày đó có dữ liệu.

## Các bước xem chỉ số của một ngày

1. Mở trang **"Thiên Cơ Các"**, chọn tab **"HT1 – SCADA"** hoặc **"HT2 – DMWCS (CBS)"**.
2. Nếu ngày cần xem nằm ngoài khoảng đang hiện, chỉnh ô **"Từ ngày"**, **"Đến ngày"** cho chứa ngày đó.
3. Bấm vào cột (hoặc điểm) của ngày đó trên một biểu đồ theo ngày bất kỳ, ví dụ "Sản lượng theo ngày".
4. Cột ngày đó được tô nền xám trên mọi biểu đồ. Dòng **"Chỉ số ngày …"** và năm thẻ chỉ số đổi sang ngày đó.
5. Rê chuột lên cột để xem nhanh số của ngày mà không cần bấm.

## Thẻ chỉ số của từng tab

- Tab HT1: **"ALL"**, **"CORRECT"**, **"REJECT"**, **"Công suất MAX"**, **"Thời gian sử dụng"**.
- Tab HT2: **"ALL"**, **"CORRECT"**, **"REJECT"**, **"Công suất AVG"**, **"Thời gian sử dụng"**. Biểu đồ Scanner cũng đổi theo ngày đã chọn.

## Nếu xem chỉ số của một ngày không được

| Hiện tượng | Nguyên nhân | Cách xử lý |
| --- | --- | --- |
| Thẻ hiện "—" | Ngày đó chưa có ảnh | Tải ảnh của ngày đó lên |
| HT2: ALL, CORRECT, REJECT là "—" nhưng có Công suất AVG | Ngày đó chỉ có ảnh Capacity, chưa có ảnh Sorted | Tải ảnh Sorted lên |
| Đổi khoảng ngày thì thẻ nhảy về ngày khác | Đổi ngày lọc thì thẻ về ngày mới nhất có dữ liệu | Bấm lại vào ngày cần xem |

## Lưu ý khi xem chỉ số của một ngày

- Mặc định thẻ hiện ngày mới nhất có dữ liệu trong khoảng đang lọc. Tab HT2 ưu tiên ngày mới nhất có ảnh Sorted.
- Tab HT1 đang lọc "Tất cả" thì thẻ là tổng các dây chuyền có ảnh trong ngày đó.
- Ý nghĩa từng thẻ: [Chỉ số HT1](../tham-chieu/chi-so-ht1-scada.md), [Chỉ số HT2](../tham-chieu/chi-so-ht2-dmwcs.md).
