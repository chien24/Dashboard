---
id: xem-bieu-do-san-luong
title: Xem biểu đồ sản lượng theo ngày
loai: tac-vu
trang: Thiên Cơ Các
he_thong: chung
aliases: [biểu đồ sản lượng, chart sản lượng, đồ thị CORRECT REJECT, sản lượng theo ngày, tổng kiện mỗi ngày]
lien_quan: [dashboard-tab-ht1, dashboard-tab-ht2, xem-chi-so-cua-mot-ngay, xem-thanh-phan-reject]
nguon_code: [frontend/html/index.html, frontend/js/dashboard.js]
cap_nhat: 2026-11-20
---
# Xem biểu đồ sản lượng theo ngày

Còn gọi là: biểu đồ sản lượng, chart sản lượng, "xem tổng kiện mỗi ngày", đồ thị CORRECT REJECT.

**Kết quả:** thấy sản lượng từng ngày, chia phần đúng (CORRECT) và phần lỗi (REJECT).
**Cần có trước:** đã đăng nhập, đã có ảnh SCADA (HT1) hoặc ảnh Sorted (HT2).

## Các bước xem biểu đồ sản lượng theo ngày

1. Mở trang **"Thiên Cơ Các"**.
2. Chọn tab **"HT1 – SCADA"** hoặc **"HT2 – DMWCS (CBS)"**.
3. Tìm khung **"Sản lượng theo ngày"**, khung đầu tiên bên trái dưới các thẻ chỉ số.
4. Mỗi ngày là một cột chồng. Chú thích màu ở trên biểu đồ.
5. Rê chuột lên một cột: ô nhỏ hiện số từng phần và dòng **"Tổng"**.
6. Bấm vào cột để thẻ chỉ số chuyển sang ngày đó.

## Biểu đồ sản lượng của HT1 và HT2 khác nhau thế nào

- **HT1**: hai phần **"CORRECT"** và **"REJECT"**. Tổng cột = ALL (số lượng đã quét), cộng các dây chuyền đang lọc.
- **HT2**: ba phần **"CORRECT – CorrectChute"**, **"CORRECT – PDA"**, **"REJECT"**. Tổng cột = ALL (Total) của máy CBS.

## Nếu biểu đồ sản lượng không hiện đúng

| Hiện tượng | Nguyên nhân | Cách xử lý |
| --- | --- | --- |
| Ngày chỉ có dấu "—" | Ngày đó chưa có ảnh | Tải ảnh lên |
| HT2 có công suất nhưng không có cột sản lượng | Ngày đó thiếu ảnh Sorted | Tải ảnh Sorted lên |
| Cột HT1 thấp bất thường | Thiếu ảnh của vài dây chuyền ngày đó | Kiểm tra ở Bảng chi tiết, tải đủ ảnh |

## Lưu ý khi xem biểu đồ sản lượng

- Nhãn trục ngang ghi ngày dạng dd/mm. Khoảng ngày dài thì chỉ ghi cách quãng.
- Trục dọc tự co giãn theo số lớn nhất trong khoảng.
- Số chính xác xem ở "Bảng chi tiết" cuối tab, hoặc rê chuột lên cột.
