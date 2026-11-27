---
id: dashboard-tab-ht1
title: Tab HT1 – SCADA trên trang Thiên Cơ Các
loai: trang
trang: Thiên Cơ Các
he_thong: HT1
aliases: [tab HT1, tab SCADA, dashboard SCADA, biểu đồ HT1, bảng chi tiết HT1]
lien_quan: [dashboard-thien-co-cac, chi-so-ht1-scada, loc-theo-day-chuyen, so-sanh-cac-day-chuyen, xem-thanh-phan-reject]
nguon_code: [frontend/html/index.html, frontend/js/dashboard.js]
cap_nhat: 2026-11-20
---
# Tab HT1 – SCADA trên trang Thiên Cơ Các

Còn gọi là: tab SCADA, dashboard HT1, biểu đồ dây chuyền.

Tab **"HT1 – SCADA"** trên trang **Thiên Cơ Các** hiện số liệu của hệ thống SCADA, theo từng dây chuyền và từng ngày.

## Cách mở tab HT1 – SCADA

Mở trang **"Thiên Cơ Các"**. Tab **"HT1 – SCADA"** được mở sẵn. Đang ở tab HT2 thì bấm **"HT1 – SCADA"** dưới tiêu đề trang.

## Bố cục tab HT1 – SCADA

Từ trên xuống:
1. Hàng lọc: **"Từ ngày"**, **"Đến ngày"**, **"Dây chuyền"**, và gợi ý "Bấm vào một ngày trên biểu đồ để xem chỉ số của ngày đó."
2. Dòng **"Chỉ số ngày dd/mm/yyyy · Tất cả dây chuyền"** (hoặc tên dây chuyền đang lọc).
3. Năm thẻ chỉ số: **"ALL"**, **"CORRECT"**, **"REJECT"**, **"Công suất MAX"**, **"Thời gian sử dụng"**.
4. Hai biểu đồ cạnh nhau: **"Sản lượng theo ngày"** và **"REJECT theo loại"**.
5. Biểu đồ **"So sánh 4 dây chuyền"** có ô chọn chỉ số ở góc trên bên phải.
6. **"Bảng chi tiết"** có nút **"Xuất CSV"**.

## Các nút và ô nhập trên tab HT1 – SCADA

| Phần tử | Vị trí | Dùng để | Khi bấm/nhập thì |
| --- | --- | --- | --- |
| Ô **"Từ ngày"**, **"Đến ngày"** | Hàng lọc đầu tab | Chọn khoảng ngày | Vẽ lại toàn bộ tab |
| Ô chọn **"Dây chuyền"** | Hàng lọc, bên phải ô ngày | Lọc một dây chuyền, hoặc **"Tất cả"** | Thẻ, biểu đồ, bảng chỉ còn dây chuyền đó |
| Ô chọn chỉ số | Góc trên bên phải biểu đồ "So sánh 4 dây chuyền" | Chọn **"Sản lượng ALL"**, **"REJECT"**, **"Tỷ lệ REJECT (%)"**, **"Công suất MAX"**, **"Thời gian sử dụng (h)"** | Vẽ lại biểu đồ so sánh |
| Cột một ngày trên biểu đồ | Các biểu đồ | Chọn ngày | Thẻ chỉ số chuyển sang ngày đó |
| Nút **"Xuất CSV"** | Góc trên bên phải "Bảng chi tiết" | Tải bảng | Tải file h1-table.csv |

## Dữ liệu hiển thị trên tab HT1 – SCADA

- **Thẻ chỉ số**: số của ngày đang chọn, cộng các dây chuyền đang lọc. Thẻ "CORRECT" và "REJECT" kèm tỷ lệ % trong ngoặc. Thẻ "REJECT" ghi rõ số "Không có mã vạch" và "Yêu cầu ống dẫn thất bại".
- Nhiều dây chuyền: thẻ "Công suất MAX" và "Thời gian sử dụng" là tổng các dây chuyền, kèm danh sách từng dây chuyền. Một dây chuyền: thẻ "Công suất MAX" ghi khung giờ đạt MAX.
- **"Sản lượng theo ngày"**: cột chồng CORRECT và REJECT mỗi ngày.
- **"REJECT theo loại"**: cột chồng "Không có mã vạch" và "Yêu cầu ống dẫn thất bại".
- **"So sánh 4 dây chuyền"**: mỗi ngày một nhóm cột, mỗi dây chuyền một màu cố định.
- **"Bảng chi tiết"**: mỗi dòng là một dây chuyền trong một ngày, ngày mới nhất ở trên. Các cột: Ngày, Dây chuyền, ALL, CORRECT, REJECT, Không có mã vạch, Yêu cầu ống dẫn thất bại, Tỷ lệ REJECT, Công suất MAX, Khung giờ MAX, Thời gian sử dụng, Cảnh báo.
- Cột "Cảnh báo" có huy hiệu "⚠ n" (rê chuột để đọc cảnh báo) hoặc "✓ 0".
- Ghi chú dưới bảng: "Thời gian sử dụng = ALL / Công suất MAX: ước tính, thời gian thực tế ≥ giá trị này."

Ý nghĩa từng chỉ số: [Chỉ số HT1 – SCADA](../tham-chieu/chi-so-ht1-scada.md).

## Khi tab HT1 – SCADA không có dữ liệu

Bảng hiện **"Không có dữ liệu trong khoảng ngày đã chọn"**, thẻ hiện "—". Nguyên nhân: chưa đăng nhập, chưa tải ảnh SCADA của các ngày đó, hoặc ngày đã quá 35 ngày nên bị xóa. Ô **"Dây chuyền"** chỉ liệt kê dây chuyền đã có ảnh.

## Việc thường làm trên tab HT1 – SCADA

- [Lọc số liệu HT1 theo dây chuyền](../tac-vu/loc-theo-day-chuyen.md)
- [So sánh các dây chuyền HT1](../tac-vu/so-sanh-cac-day-chuyen.md)
- [Xem thành phần REJECT](../tac-vu/xem-thanh-phan-reject.md)
