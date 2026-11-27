---
id: xoa-bao-cao
title: Xóa một báo cáo
loai: tac-vu
trang: Xem / sửa report
he_thong: chung
aliases: [xóa report, xóa báo cáo, xóa ảnh đã upload, gỡ số liệu sai, Xóa report]
lien_quan: [xem-sua-report, so-lieu-nao-duoc-hien-thi, sua-so-lieu-ocr-sai, tang-kinh-cac]
nguon_code: [frontend/html/report.html, frontend/js/report.js, backend/app/api/reports.py]
cap_nhat: 2026-11-20
---
# Xóa một báo cáo

Còn gọi là: xóa report, gỡ số liệu sai, "xóa ảnh tải nhầm".

**Kết quả:** báo cáo bị xóa hẳn, số liệu của nó biến mất khỏi dashboard và Tàng Kinh Các. Trang chuyển về **"Thiên Cơ Các"**.
**Cần có trước:** đã đăng nhập.

## Các bước xóa một báo cáo

1. Mở trang **"Tàng Kinh Các"**, bấm dòng báo cáo, bấm **"Xem / sửa số liệu"**.
2. Kiểm tra tiêu đề trang đúng là báo cáo cần xóa (loại báo cáo, tên file, ngày báo cáo).
3. Cuộn xuống cuối cột bên phải, bấm nút **"Xóa report"**.
4. Trình duyệt hỏi **"Xóa report này? Số liệu của nó sẽ biến mất khỏi dashboard."**. Bấm OK để xóa, Hủy để thôi.
5. Xóa xong, trang tự chuyển về Thiên Cơ Các.

## Nếu xóa báo cáo không như mong muốn

| Hiện tượng | Nguyên nhân | Cách xử lý |
| --- | --- | --- |
| Nút "Xóa report" bị mờ | Chưa đăng nhập | Bấm "Nhập Môn" |
| Xóa xong, ngày đó trên dashboard trống thay vì hiện báo cáo cũ hơn | Báo cáo cũ đã bị thay không tự quay lại | Mở báo cáo cũ ở Tàng Kinh Các, bấm "Xem / sửa số liệu", bấm "Lưu" để đưa nó lên dashboard |
| Lỡ xóa nhầm | Xóa không hoàn tác được | Ảnh đó còn báo cáo khác (nhãn "Đã được thay") thì mở báo cáo đó và bấm "Lưu". Nếu không còn: tải lại ảnh gốc ở trang Truyền Pháp Ảnh, ảnh được đọc như ảnh mới |

## Lưu ý khi xóa báo cáo

- Xóa là vĩnh viễn, không có thùng rác, không hoàn tác.
- Ảnh không còn báo cáo nào khác thì bị xóa luôn khỏi hệ thống cùng báo cáo. Tải lại đúng ảnh đó sau này được đọc như ảnh mới, không bị báo trùng.
- Ảnh còn báo cáo khác (ví dụ báo cáo cũ trước lần "OCR lại") thì ảnh được giữ. Tải lại ảnh đó sẽ bị báo "Ảnh đã được xử lý trước đó" và hiện báo cáo còn lại.
- Chỉ cần sửa vài số thì nên sửa tay thay vì xóa. Xem [Sửa số liệu bị đọc sai](sua-so-lieu-ocr-sai.md).
- Báo cáo cũ hơn 35 ngày tự bị xóa, không cần xóa tay.
