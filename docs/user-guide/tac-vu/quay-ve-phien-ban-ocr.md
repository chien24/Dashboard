---
id: quay-ve-phien-ban-ocr
title: Quay về một lần đọc cũ (OCR Version)
loai: tac-vu
trang: Xem / sửa report
he_thong: chung
aliases: [OCR Version, phiên bản OCR, quay về bản cũ, khôi phục số liệu, fallback, Dùng bản này, xem JSON từng lần đọc, so sánh 2 lần OCR]
lien_quan: [xem-sua-report, ocr-lai-bao-cao, sua-so-lieu-ocr-sai, canh-bao-so-lieu, trang-thai]
nguon_code: [frontend/html/report.html, frontend/js/report.js, backend/app/api/reports.py]
cap_nhat: 2026-11-20
---
# Quay về một lần đọc cũ (OCR Version)

Còn gọi là: OCR Version, phiên bản OCR, khôi phục số liệu, "quay về bản đọc lần 2", "lỡ sửa sai muốn lấy lại số cũ".

**Kết quả:** số liệu đang dùng của báo cáo được thay bằng đúng kết quả của lần đọc đã chọn. Cạnh nút hiện **"Đã quay về OCR lần N. Dashboard dùng số liệu này."**, lần đọc đó có nhãn **"Đang dùng"**.
**Cần có trước:** đã đăng nhập; báo cáo có ảnh gốc.

## OCR Version là gì

Mỗi ảnh được hệ thống đọc 2 lần. Mỗi lần bấm "OCR lại" lại có thêm 2 lần đọc nữa. Mục **"OCR Version"** trên trang Xem / sửa report liệt kê **mọi lần đọc của cùng ảnh**, cũ trước mới sau: "OCR lần 1", "OCR lần 2", "OCR lần 3"… Mỗi lần ghi giờ đọc. Lần thuộc báo cáo khác (trước khi OCR lại) ghi thêm "report #…".

Luôn chỉ có **một** lần đọc mang nhãn **"Đang dùng"**, kể cả khi hai lần đọc ra số giống hệt nhau:
- Báo cáo vừa đọc xong: lần 1 của báo cáo đó đang được dùng.
- Sau khi bấm "Dùng bản này": lần vừa chọn được đánh dấu.
- Sau khi sửa tay một số rồi bấm "Lưu": không lần nào được đánh dấu. Đầu mục hiện dòng "Đang dùng: bản sửa tay (số đã được sửa, không trùng lần OCR nào bên dưới)." Bấm "Lưu" mà không đổi số nào thì giữ nguyên đánh dấu cũ.

## Các bước xem và quay về một lần đọc

1. Mở trang **Xem / sửa report** của báo cáo.
2. Cuộn xuống mục **"OCR Version"**, dưới hàng nút "Lưu", "Thêm giá trị", "OCR lại".
3. Bấm **"Xem JSON"** ở một lần đọc để xem toàn bộ số liệu của lần đó.
4. So với ảnh gốc. Thấy lần nào đúng thì bấm **"Dùng bản này"** ở lần đó.
5. Trình duyệt hỏi "Thay số liệu đang dùng bằng OCR lần N? Số đang có (kể cả phần đã sửa tay) sẽ bị thay." Bấm OK.
6. Form hiện số của lần đã chọn, trạng thái báo cáo thành **"Đã sửa tay"**, dashboard dùng số này.

## Nếu quay về một lần đọc không được

| Hiện tượng | Nguyên nhân | Cách xử lý |
| --- | --- | --- |
| "Không có bản OCR nào (report import từ JSON)." | Báo cáo nhập từ file dữ liệu, không có lần đọc nào | Không quay về được |
| Chỉ có "OCR lần 1" | Lần đọc thứ hai bị lỗi | Bấm "OCR lại" để có thêm lần đọc |
| "Report này vừa được sửa ở máy khác…" | Người khác vừa lưu | Tải lại trang rồi làm lại |
| Lỗi có chữ "Sai schema" | Lần đọc đó thiếu hoặc sai trường | Chọn lần khác, hoặc sửa tay từng ô |

## Lưu ý khi quay về một lần đọc

- Quay về sẽ thay cả phần đã sửa tay. Số sửa tay cũ không được giữ lại.
- Hai lần đọc khác nhau ở trường nào thì hộp "Cảnh báo" đã ghi "Lệch giữa lần 1 và lần 2…". So hai lần trong OCR Version để chọn lần đúng.
- Sau khi quay về, cảnh báo được kiểm tra lại với số mới; dòng đầu là "Đã sửa tay".
