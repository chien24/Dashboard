---
id: so-sanh-cac-day-chuyen
title: So sánh các dây chuyền HT1
loai: tac-vu
trang: Thiên Cơ Các
he_thong: HT1
aliases: [so sánh dây chuyền, so sánh 4 dây chuyền, dây chuyền nào cao nhất, xếp hạng dây chuyền, compare line]
lien_quan: [dashboard-tab-ht1, loc-theo-day-chuyen, chi-so-ht1-scada, xem-cong-suat-va-thoi-gian-su-dung]
nguon_code: [frontend/html/index.html, frontend/js/dashboard.js]
cap_nhat: 2026-11-20
---
# So sánh các dây chuyền HT1

Còn gọi là: so sánh 4 dây chuyền, "dây chuyền nào REJECT cao nhất", xếp hạng dây chuyền.

**Kết quả:** thấy cùng một chỉ số của mọi dây chuyền HT1 đặt cạnh nhau theo từng ngày.
**Cần có trước:** đã đăng nhập, đã có ảnh SCADA của các dây chuyền.

## Các bước so sánh các dây chuyền HT1

1. Mở trang **"Thiên Cơ Các"**, tab **"HT1 – SCADA"**.
2. Cuộn xuống khung **"So sánh 4 dây chuyền"**, dưới hai biểu đồ "Sản lượng theo ngày" và "REJECT theo loại".
3. Bấm ô chọn ở góc trên bên phải khung, chọn chỉ số:
   - **"Sản lượng ALL"**
   - **"REJECT"**
   - **"Tỷ lệ REJECT (%)"**
   - **"Công suất MAX"**
   - **"Thời gian sử dụng (h)"**
4. Mỗi ngày là một nhóm cột, mỗi dây chuyền một màu. Chú thích tên dây chuyền ở trên biểu đồ.
5. Rê chuột lên nhóm cột để xem số của từng dây chuyền trong ngày.

## Nếu so sánh các dây chuyền không như mong muốn

| Hiện tượng | Nguyên nhân | Cách xử lý |
| --- | --- | --- |
| Một dây chuyền thiếu cột ở vài ngày | Chưa có ảnh của dây chuyền đó ngày đó | Tải ảnh lên |
| Có nhiều hơn 4 dây chuyền | Ảnh có tên dây chuyền mới hoặc đọc sai tên | Dây chuyền ngoài 4 dây chuyền chính có màu xám; kiểm tra tên ở Tàng Kinh Các |

## Lưu ý khi so sánh các dây chuyền

- Biểu đồ so sánh luôn hiện mọi dây chuyền, không theo ô lọc "Dây chuyền".
- Mỗi dây chuyền giữ màu cố định: Outbound, Inbound, CBS2 1st layer, CBS1 2st layer lần lượt có màu riêng.
- So sánh số chính xác: xem "Bảng chi tiết" cuối tab, mỗi dòng là một dây chuyền trong một ngày.
