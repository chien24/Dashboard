---
id: ocr-lai-bao-cao
title: Đọc lại (OCR lại) ảnh của một báo cáo
loai: tac-vu
trang: Xem / sửa report
he_thong: chung
aliases: [OCR lại, đọc lại ảnh, quét lại, chạy lại OCR, bắt hệ thống đọc lại]
lien_quan: [xem-sua-report, quay-ve-phien-ban-ocr, tai-lai-anh-da-tai-truoc-do, so-lieu-nao-duoc-hien-thi, ocr-that-bai]
nguon_code: [frontend/html/report.html, frontend/js/report.js, backend/app/api/reports.py]
cap_nhat: 2026-11-20
---
# Đọc lại (OCR lại) ảnh của một báo cáo

Còn gọi là: OCR lại, đọc lại ảnh, quét lại, "bắt hệ thống đọc lại".

**Kết quả:** hệ thống đọc lại ảnh gốc, tạo một báo cáo mới. Trang tự mở báo cáo mới khi xong. Báo cáo mới thay báo cáo cũ trên dashboard.
**Cần có trước:** đã đăng nhập; báo cáo có ảnh gốc.

## Các bước OCR lại ảnh của một báo cáo

1. Mở trang **Xem / sửa report** của báo cáo (từ Tàng Kinh Các, nút **"Xem / sửa số liệu"**).
2. Bấm nút **"OCR lại"**, cạnh nút "Thêm giá trị". Không cần chọn gì thêm.
3. Cạnh nút hiện "Đang OCR lại…", rồi "Đang OCR lại · …" kèm bước đang chạy. Nút "OCR lại" bị mờ trong lúc chờ.
4. Xong, trang tự chuyển sang báo cáo mới. Kiểm tra số và cảnh báo của báo cáo mới.

## Nếu OCR lại không thành công

| Hiện tượng | Nguyên nhân | Cách xử lý |
| --- | --- | --- |
| Nút "OCR lại" bị mờ | Báo cáo nhập từ file dữ liệu, không có ảnh; hoặc chưa đăng nhập | Tải ảnh gốc lên ở trang Truyền Pháp Ảnh |
| Chữ đỏ cạnh nút, bắt đầu "Tất cả provider/model đều lỗi" | Mọi nguồn đọc đều lỗi hoặc hết lượt | Thử lại sau. Xem [lỗi OCR thất bại](../loi/ocr-that-bai.md) |
| Chữ đỏ khác cạnh nút | Lỗi mạng hoặc hết phiên | Tải lại trang, đăng nhập lại nếu cần |

## Lưu ý khi OCR lại ảnh

- OCR lại dùng đúng loại báo cáo cũ, không nhận diện lại loại ảnh.
- Hệ thống tự chọn nguồn đọc ảnh, nguồn này lỗi thì tự chuyển sang nguồn khác.
- Báo cáo cũ không bị xóa. Ở Tàng Kinh Các báo cáo cũ có nhãn "Đã được thay".
- Các lần đọc cũ vẫn nằm trong mục **"OCR Version"** của báo cáo mới. Lần đọc mới sai thì quay về lần cũ được. Xem [Quay về một lần đọc cũ](quay-ve-phien-ban-ocr.md).
- Có thể rời trang khi đang OCR lại. Ảnh vẫn được đọc; kết quả xem ở Tàng Kinh Các.
- Mỗi lần OCR lại tốn 2 lượt đọc ảnh.
