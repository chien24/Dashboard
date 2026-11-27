---
id: dashboard-tab-ht2
title: Tab HT2 – DMWCS (CBS) trên trang Thiên Cơ Các
loai: trang
trang: Thiên Cơ Các
he_thong: HT2
aliases: [tab HT2, tab DMWCS, tab CBS, dashboard DMWCS, biểu đồ HT2, bảng chi tiết theo ngày]
lien_quan: [dashboard-thien-co-cac, chi-so-ht2-dmwcs, xem-ty-le-doc-cua-scanner, xem-cong-suat-va-thoi-gian-su-dung, xem-thanh-phan-reject]
nguon_code: [frontend/html/index.html, frontend/js/dashboard.js]
cap_nhat: 2026-11-20
---
# Tab HT2 – DMWCS (CBS) trên trang Thiên Cơ Các

Còn gọi là: tab DMWCS, tab CBS, dashboard HT2.

Tab **"HT2 – DMWCS (CBS)"** trên trang **Thiên Cơ Các** hiện số liệu của máy CBS: sản lượng, thành phần REJECT, công suất AVG, tỷ lệ đọc của Scanner và thời gian sử dụng.

## Cách mở tab HT2 – DMWCS (CBS)

Mở trang **"Thiên Cơ Các"**, bấm tab **"HT2 – DMWCS (CBS)"** dưới tiêu đề trang. Link "Tàng Kinh Các" ở cuối tab HT2 mở thẳng tab HT2 của trang Tàng Kinh Các.

## Bố cục tab HT2 – DMWCS (CBS)

Từ trên xuống:
1. Hàng lọc: **"Từ ngày"**, **"Đến ngày"** và gợi ý "Bấm vào một ngày trên biểu đồ để xem chỉ số của ngày đó." Tab HT2 không có ô lọc dây chuyền.
2. Dòng **"Chỉ số ngày dd/mm/yyyy · máy CBS"**.
3. Năm thẻ: **"ALL"**, **"CORRECT"**, **"REJECT"**, **"Công suất AVG"**, **"Thời gian sử dụng"**.
4. Năm biểu đồ: **"Sản lượng theo ngày"**, **"Thành phần REJECT"**, **"Công suất AVG theo ngày"**, **"Tỷ lệ đọc thành công của từng Scanner"**, **"Thời gian sử dụng (h)"**.
5. **"Bảng chi tiết theo ngày"** có nút **"Xuất CSV"**.

## Các nút và ô nhập trên tab HT2 – DMWCS (CBS)

| Phần tử | Vị trí | Dùng để | Khi bấm/nhập thì |
| --- | --- | --- | --- |
| Ô **"Từ ngày"**, **"Đến ngày"** | Hàng lọc đầu tab | Chọn khoảng ngày | Vẽ lại toàn bộ tab HT2 |
| Cột một ngày trên biểu đồ | Các biểu đồ theo ngày | Chọn ngày | Thẻ chỉ số và biểu đồ Scanner chuyển sang ngày đó |
| Nút **"Xuất CSV"** | Góc trên bên phải "Bảng chi tiết theo ngày" | Tải bảng | Tải file h2-table.csv |

## Dữ liệu hiển thị trên tab HT2 – DMWCS (CBS)

- **Thẻ chỉ số**: số của ngày đang chọn. Mặc định là ngày gần nhất có báo cáo Sorted. Thẻ "CORRECT" ghi "CorrectChute … + PDA …"; thẻ "REJECT" ghi "RejectChute"; thẻ "Công suất AVG" ghi "bưu kiện/giờ · báo cáo Capacity"; thẻ "Thời gian sử dụng" ghi "ALL / AVG".
- **"Sản lượng theo ngày"**: cột chồng "CORRECT – CorrectChute", "CORRECT – PDA", "REJECT".
- **"Thành phần REJECT"**: cột chồng NoRead, NoPostOffice, NoChute.
- **"Công suất AVG theo ngày"**: đường nối các ngày. Ghi chú: "Mỗi ngày đúng 1 giá trị. Nhiều ảnh capacity cùng có 1 ngày thì không cộng: lấy ảnh có khoảng truy vấn mới nhất, giá trị khác nhau thì gắn cảnh báo."
- **"Tỷ lệ đọc thành công của từng Scanner"**: cột RATE của từng Scanner trong ngày đang chọn, kèm bảng BCR_NO, TOTAL, SUCCESS, FAILED, RATE.
- **"Thời gian sử dụng (h)"**: cột số giờ mỗi ngày, có in số trên đầu cột.
- **"Bảng chi tiết theo ngày"**: cột Ngày, Nguồn, ALL, CORRECT, trong đó PDA, REJECT, Tỷ lệ CORRECT, Tỷ lệ REJECT, Công suất AVG (bưu kiện/giờ), Thời gian sử dụng, Cảnh báo. Cột "Nguồn" ghi "Sorted + Capacity" hoặc "Chỉ Capacity".
- Ghi chú dưới bảng: "CORRECT = CorrectChute + PDA, nên CORRECT + REJECT = ALL. Cột PDA là phần PDA nằm trong CORRECT."

Ý nghĩa chỉ số: [Chỉ số HT2 – DMWCS](../tham-chieu/chi-so-ht2-dmwcs.md).

## Khi tab HT2 – DMWCS (CBS) không có dữ liệu

- Ngày chỉ có ảnh Capacity: thẻ ALL, CORRECT, REJECT hiện "—", cột "Nguồn" ghi "Chỉ Capacity". Tải ảnh Sorted của ngày đó lên.
- Ngày không có ảnh Capacity: "Công suất AVG" và "Thời gian sử dụng" hiện "—".
- Không có ảnh BCR rate: biểu đồ Scanner hiện **"Chưa có dữ liệu Scanner ngày …"**.
- Khoảng ngày trống: bảng hiện **"Không có dữ liệu trong khoảng ngày đã chọn"**.

## Việc thường làm trên tab HT2 – DMWCS (CBS)

- [Xem tỷ lệ đọc thành công của từng Scanner](../tac-vu/xem-ty-le-doc-cua-scanner.md)
- [Xem công suất và thời gian sử dụng](../tac-vu/xem-cong-suat-va-thoi-gian-su-dung.md)
- [Xem thành phần REJECT](../tac-vu/xem-thanh-phan-reject.md)
