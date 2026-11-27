---
id: du-lieu-sua-khong-hop-le
title: Lỗi khi lưu số liệu đã sửa ("Sai schema", "không hợp lệ")
loai: loi
trang: Xem / sửa report
he_thong: chung
aliases: [Sai schema, không hợp lệ, lưu không được, số không hợp lệ, thoi_gian_tu không hợp lệ, den_ngay không hợp lệ, lỗi kiểu dữ liệu]
lien_quan: [sua-so-lieu-ocr-sai, them-xoa-dong-so-lieu, quay-ve-phien-ban-ocr, chi-so-ht1-scada, chi-so-ht2-dmwcs]
nguon_code: [frontend/js/report.js, backend/app/api/reports.py, backend/app/services/normalize.py]
cap_nhat: 2026-11-20
---
# Lỗi khi lưu số liệu đã sửa ("Sai schema", "không hợp lệ")

Còn gọi là: lưu không được, số không hợp lệ, lỗi kiểu dữ liệu.

**Xuất hiện ở:** trang **Xem / sửa report**, chữ đỏ cạnh nút **"Lưu"**, sau khi bấm **"Lưu"** hoặc **"Dùng bản này"** (mục OCR Version). Thường có dạng:
- "Sai schema: N lỗi, ví dụ <tên trường>: <mô tả>"
- "thoi_gian_tu không hợp lệ: '…'"
- "den_ngay không hợp lệ: '…'"

**Nghĩa là:** dữ liệu vừa sửa sai kiểu hoặc thiếu trường, nên hệ thống không lưu. Báo cáo giữ nguyên như trước khi sửa.

**Nguyên nhân thường gặp:**
- Gõ chữ hoặc ký tự lạ vào ô số, ví dụ "75.469" (dấu chấm ngăn nghìn), "12%", "1 368".
- Để trống ô số.
- Ngày giờ sai dạng. Dạng đúng: 2026-11-16 00:00 (năm-tháng-ngày giờ:phút); ngày Capacity: 2026-11-16.
- Bấm "Thêm giá trị" rồi để trống ô chữ hoặc ô ngày của dòng mới.

**Cách xử lý:**
1. Đọc tên trường trong thông báo lỗi.
2. Tìm ô có tên đó trong form. Rê chuột lên tên ô để xem đường dẫn đầy đủ.
3. Sửa giá trị: số viết liền, không dấu chấm ngăn nghìn, không dấu %; phần thập phân dùng dấu chấm, ví dụ 83.23.
4. Bấm **"Lưu"** lại.

**Nếu vẫn lỗi:** tải lại trang (F5) để về dữ liệu gốc rồi sửa lại từng ô. Vẫn không được thì chụp màn hình thông báo lỗi, báo người hỗ trợ ở mục **"Gặp Kiếp Nạn"** cuối trang.
