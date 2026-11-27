---
id: dashboard-thien-co-cac
title: Trang Thiên Cơ Các (Dashboard)
loai: trang
trang: Thiên Cơ Các
he_thong: chung
aliases: [dashboard, trang chủ, Thiên Cơ Các, Dashboard vận hành CNKT3, trang biểu đồ, màn hình chỉ số]
lien_quan: [dashboard-tab-ht1, dashboard-tab-ht2, loc-dashboard-theo-ngay, xem-chi-so-cua-mot-ngay, xuat-bang-ra-csv]
nguon_code: [frontend/html/index.html, frontend/js/dashboard.js]
cap_nhat: 2026-11-20
---
# Trang Thiên Cơ Các (Dashboard)

Còn gọi là: dashboard, trang chủ, trang biểu đồ, "Dashboard vận hành CNKT3".

Trang **Thiên Cơ Các** hiện chỉ số, biểu đồ và bảng số liệu của HT1 – SCADA và HT2 – DMWCS, lấy từ các ảnh báo cáo đã tải lên.

## Cách mở trang Thiên Cơ Các

- Bấm mục **"Thiên Cơ Các"** trên thanh menu, hoặc bấm logo Viettel Post ở góc trên bên trái.
- Mở địa chỉ gốc của trang web cũng tự chuyển tới trang Thiên Cơ Các.

## Bố cục trang Thiên Cơ Các

Từ trên xuống:
1. Tiêu đề **"Dashboard vận hành CNKT3"** và dòng "Phòng Kỹ thuật · Chi nhánh Khai thác 3 · HT1 SCADA và HT2 DMWCS".
2. Hai tab **"HT1 – SCADA"** và **"HT2 – DMWCS (CBS)"**. Mặc định mở tab HT1.
3. Nội dung của tab đang chọn: ô lọc ngày, dòng "Chỉ số ngày …", các thẻ chỉ số, biểu đồ, bảng chi tiết.
4. Cuối mỗi tab có dòng "Chi tiết từng báo cáo (giá trị gốc, cảnh báo, ảnh đã upload) xem ở trang **Tàng Kinh Các**", có link sang trang Tàng Kinh Các.

Mỗi tab có mô tả riêng: [Tab HT1 – SCADA](dashboard-tab-ht1.md) và [Tab HT2 – DMWCS (CBS)](dashboard-tab-ht2.md).

## Các nút và ô nhập chung trên trang Thiên Cơ Các

| Phần tử | Vị trí | Dùng để | Khi bấm/nhập thì |
| --- | --- | --- | --- |
| Tab **"HT1 – SCADA"**, **"HT2 – DMWCS (CBS)"** | Dưới tiêu đề trang | Chọn hệ thống | Hiện nội dung của hệ thống đó |
| Ô **"Từ ngày"**, **"Đến ngày"** | Đầu mỗi tab | Chọn khoảng ngày | Vẽ lại thẻ, biểu đồ, bảng |
| Cột ngày trên biểu đồ | Trong các biểu đồ theo ngày | Chọn ngày xem chỉ số | Thẻ chỉ số chuyển sang ngày đó |
| Nút **"Xuất CSV"** | Góc trên bên phải khung bảng chi tiết | Tải bảng về máy | Tải file CSV mở được bằng Excel |

## Dữ liệu hiển thị trên trang Thiên Cơ Các

- Mặc định, khoảng ngày kết thúc ở ngày mới nhất có dữ liệu và lùi lại 7 ngày. Nếu có báo cáo cũ hơn trong 35 ngày, khoảng ngày lùi tới báo cáo cũ nhất.
- Biểu đồ và bảng chỉ hiện tối đa 35 ngày cuối của khoảng đã chọn.
- Rê chuột lên biểu đồ để xem số chính xác của từng ngày.
- Chỉ hiện báo cáo đang được dùng. Báo cáo đã bị ảnh mới hơn thay thì không hiện. Xem [Nhiều ảnh cùng kỳ báo cáo thì số nào được hiển thị](../tham-chieu/so-lieu-nao-duoc-hien-thi.md).

## Khi trang Thiên Cơ Các không có dữ liệu

- Chưa đăng nhập: thẻ chỉ số hiện dấu "—", biểu đồ trống. Bấm **"Nhập Môn"** để đăng nhập.
- Khoảng ngày không có ảnh nào: bảng hiện **"Không có dữ liệu trong khoảng ngày đã chọn"**. Đổi khoảng ngày, hoặc tải ảnh của các ngày đó lên.
- Một ngày trên biểu đồ chỉ có dấu "—": ngày đó chưa có ảnh, không phải số 0.
- Lỗi tải: đầu trang hiện **"Không tải được dữ liệu: …"**. Xem [Lỗi "Không tải được …"](../loi/khong-tai-duoc-du-lieu.md).

## Việc thường làm trên trang Thiên Cơ Các

- [Lọc dashboard theo khoảng ngày](../tac-vu/loc-dashboard-theo-ngay.md)
- [Xem chỉ số của một ngày cụ thể](../tac-vu/xem-chi-so-cua-mot-ngay.md)
- [Xem biểu đồ sản lượng theo ngày](../tac-vu/xem-bieu-do-san-luong.md)
- [Xuất bảng chi tiết ra file CSV](../tac-vu/xuat-bang-ra-csv.md)
