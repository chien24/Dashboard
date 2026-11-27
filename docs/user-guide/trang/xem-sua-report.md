---
id: xem-sua-report
title: Trang Xem / sửa report
loai: trang
trang: Xem / sửa report
he_thong: chung
aliases: [trang report, trang sửa số liệu, chi tiết report, sửa báo cáo, trang chỉnh sửa, OCR Version]
lien_quan: [sua-so-lieu-ocr-sai, them-xoa-dong-so-lieu, ocr-lai-bao-cao, quay-ve-phien-ban-ocr, xoa-bao-cao, canh-bao-so-lieu]
nguon_code: [frontend/html/report.html, frontend/js/report.js, backend/app/api/reports.py]
cap_nhat: 2026-11-20
---
# Trang Xem / sửa report

Còn gọi là: trang report, trang sửa số liệu, chi tiết báo cáo.

Trang **Xem / sửa report** hiện ảnh gốc cạnh số liệu hệ thống đã đọc của một báo cáo, để so và sửa tay. Trang Xem / sửa report còn dùng để thêm dòng, đọc lại ảnh, quay về một lần đọc cũ, hoặc xóa báo cáo.

## Cách mở trang Xem / sửa report

- Ở trang **"Tàng Kinh Các"**, bấm một dòng báo cáo, rồi bấm **"Xem / sửa số liệu"**.
- Ở trang **"Truyền Pháp Ảnh"**, khi ảnh đọc xong, bấm link **"Xem / Sửa"** hoặc **"xem kết quả cũ"**.

Trang Xem / sửa report không có mục trên thanh menu.

## Bố cục trang Xem / sửa report

1. Tiêu đề: tên loại báo cáo và tên file, ví dụ "SCADA · Screenshot 2026-11-16.png".
2. Dòng thông tin: **"Ngày báo cáo …"**, trạng thái, thông tin lần đọc.
3. Hộp **"Cảnh báo"** màu vàng (nếu có).
4. Bên trái: ảnh gốc. Bên phải: các ô số liệu, hàng nút **"Lưu"**, **"Thêm giá trị"**, **"OCR lại"**, rồi mục **"OCR Version"** và nút **"Xóa report"** ở cuối. Màn hình hẹp thì ảnh nằm trên, phần sửa nằm dưới.

## Các nút và ô nhập trên trang Xem / sửa report

| Phần tử | Vị trí | Dùng để | Khi bấm/nhập thì |
| --- | --- | --- | --- |
| Khung ảnh gốc | Bên trái | So với số liệu | Bấm để phóng to, bấm lần nữa để thu nhỏ |
| Các ô số liệu | Bên phải, nhóm theo khung | Sửa trực tiếp từng giá trị | Chưa lưu cho tới khi bấm "Lưu" |
| Nút **"Xóa dòng"** | Cạnh tên mỗi dòng của danh sách | Bỏ một dòng thừa | Dòng biến mất khỏi form, bấm "Lưu" để lưu |
| Nút **"Lưu"** | Dưới các ô số liệu | Lưu số đã sửa | "Đang lưu…" rồi "Đã lưu. Dashboard dùng số liệu mới." |
| Nút **"Thêm giá trị"** | Cạnh nút Lưu | Thêm một dòng vào danh sách của báo cáo | Hiện dòng mới để điền. Chỉ có ở báo cáo SCADA, Capacity, BCR rate |
| Nút **"OCR lại"** | Cạnh nút Thêm giá trị | Cho hệ thống đọc lại ảnh | Tự đọc lại, xong thì mở báo cáo mới |
| Mục **"OCR Version"** | Dưới hàng nút | Xem mọi lần đọc của ảnh | Mỗi lần có mục "Xem JSON" và nút **"Dùng bản này"** |
| Nút **"Xóa report"** | Cuối cột bên phải | Xóa báo cáo | Hỏi xác nhận rồi về Dashboard |

## Dữ liệu hiển thị trên trang Xem / sửa report

Mỗi trường dữ liệu có một ô, ghi tên trường kỹ thuật, ví dụ `so_luong_da_quet`, `total`, `reject_chute`. Trường dạng danh sách (loại bất thường, ngày công suất, Scanner) nhóm theo khung có số thứ tự, ví dụ `phan_bo_bat_thuong[0]`. Rê chuột lên tên ô để xem đường dẫn đầy đủ của trường.

Mục **"OCR Version"** liệt kê "OCR lần 1", "OCR lần 2"… kèm giờ đọc. Lần đang dùng có nhãn **"Đang dùng"**. Xem [Quay về một lần đọc cũ](../tac-vu/quay-ve-phien-ban-ocr.md).

Ý nghĩa từng trường: [Chỉ số HT1 – SCADA](../tham-chieu/chi-so-ht1-scada.md), [Chỉ số HT2 – DMWCS](../tham-chieu/chi-so-ht2-dmwcs.md).

## Khi trang Xem / sửa report không có dữ liệu

- Chưa đăng nhập: tiêu đề hiện **"Chưa nhập môn, không thể xem / sửa report"**, các nút bị mờ.
- Đường dẫn thiếu mã báo cáo: tiêu đề hiện **"Thiếu ?id= trên đường dẫn"**. Mở lại từ Tàng Kinh Các.
- Báo cáo đã bị xóa: tiêu đề hiện **"Không tải được report: Không có report này"**.
- Báo cáo nhập từ file dữ liệu, không có ảnh: khung ảnh hiện "Không có ảnh gốc (report import từ JSON).", nút "OCR lại" bị mờ, mục OCR Version ghi "Không có bản OCR nào (report import từ JSON)."

## Việc thường làm trên trang Xem / sửa report

- [Sửa số liệu bị đọc sai](../tac-vu/sua-so-lieu-ocr-sai.md)
- [Thêm hoặc xóa một dòng số liệu](../tac-vu/them-xoa-dong-so-lieu.md)
- [Đọc lại (OCR lại) ảnh của một báo cáo](../tac-vu/ocr-lai-bao-cao.md)
- [Quay về một lần đọc cũ (OCR Version)](../tac-vu/quay-ve-phien-ban-ocr.md)
- [Xóa một báo cáo](../tac-vu/xoa-bao-cao.md)
