---
id: sua-so-lieu-ocr-sai
title: Sửa số liệu bị đọc sai
loai: tac-vu
trang: Xem / sửa report
he_thong: chung
aliases: [sửa số, sửa tay, chỉnh số liệu, OCR đọc sai, sửa báo cáo, sửa report, đọc nhầm số]
lien_quan: [xem-sua-report, them-xoa-dong-so-lieu, quay-ve-phien-ban-ocr, trang-thai, report-vua-duoc-sua-o-may-khac, du-lieu-sua-khong-hop-le]
nguon_code: [frontend/js/report.js, backend/app/api/reports.py]
cap_nhat: 2026-11-20
---
# Sửa số liệu bị đọc sai

Còn gọi là: sửa tay, chỉnh số liệu, "OCR đọc sai thì sửa thế nào", "sửa số ở đâu".

**Kết quả:** cạnh nút "Lưu" hiện **"Đã lưu. Dashboard dùng số liệu mới."**. Trạng thái báo cáo đổi thành **"Đã sửa tay"** (da_sua_tay). Dashboard và chatbot dùng số mới.
**Cần có trước:** đã đăng nhập; biết báo cáo nào sai (thường là báo cáo "Cần kiểm tra").

## Các bước sửa số liệu bị đọc sai

1. Mở trang **"Tàng Kinh Các"**, bấm vào dòng báo cáo cần sửa.
2. Bấm nút **"Xem / sửa số liệu"**. Trang **Xem / sửa report** mở ra. (Từ trang Truyền Pháp Ảnh thì bấm link **"Xem / Sửa"**.)
3. Đọc hộp **"Cảnh báo"** màu vàng ở đầu trang để biết trường nào nghi sai.
4. So từng ô số liệu bên phải với ảnh gốc bên trái. Bấm vào ảnh để phóng to, bấm lần nữa để thu nhỏ.
5. Sửa số trong ô bị sai. Gõ số không có dấu chấm ngăn nghìn, dùng dấu chấm cho phần thập phân, ví dụ 83.23.
6. Bấm **"Lưu"**. Cạnh nút hiện "Đang lưu…" rồi "Đã lưu. Dashboard dùng số liệu mới.".
7. Đọc lại hộp "Cảnh báo": dòng đầu là "Đã sửa tay", các dòng sau là kết quả kiểm tra lại số học với số mới.

## Nếu sửa số liệu không lưu được

| Hiện tượng | Nguyên nhân | Cách xử lý |
| --- | --- | --- |
| "Report này vừa được sửa ở máy khác. Tải lại trang để xem bản mới rồi sửa lại." | Người khác đã lưu báo cáo này sau khi bạn mở | Tải lại trang, sửa lại. Xem [lỗi này](../loi/report-vua-duoc-sua-o-may-khac.md) |
| Lỗi đỏ có chữ "Sai schema" hoặc "không hợp lệ" | Ô số có chữ, hoặc ngày giờ sai định dạng | Xem [lỗi khi lưu số liệu](../loi/du-lieu-sua-khong-hop-le.md) |
| Nút "Lưu" bị mờ | Chưa đăng nhập | Bấm "Nhập Môn" rồi mở lại trang |
| Cần thêm hoặc bớt một dòng (loại bất thường, Scanner, ngày) | Hệ thống đọc thiếu hoặc thừa dòng | Bấm "Thêm giá trị" hoặc "Xóa dòng". Xem [Thêm hoặc xóa dòng](them-xoa-dong-so-lieu.md) |

## Lưu ý khi sửa số liệu

- Sau khi lưu, cảnh báo vẫn còn nếu số học vẫn không khớp. Đó là để nhắc kiểm tra, không chặn việc lưu.
- Mọi lần đọc gốc vẫn được giữ ở mục **"OCR Version"**. Lỡ sửa sai thì bấm "Dùng bản này" để quay về. Xem [Quay về một lần đọc cũ](quay-ve-phien-ban-ocr.md).
- Lưu một báo cáo đang ở trạng thái "Đã được thay" sẽ đưa nó trở lại dashboard, thay báo cáo đang dùng cùng kỳ.
- Sửa ngày giờ của báo cáo có thể đổi ngày báo cáo, và báo cáo chuyển sang ngày khác trên dashboard.
- Bấm "OCR lại" sau khi sửa tay sẽ tạo báo cáo mới thay số đã sửa.
