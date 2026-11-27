---
id: so-lieu-nao-duoc-hien-thi
title: Nhiều ảnh cùng kỳ báo cáo thì số nào được hiển thị
loai: tham-chieu
trang: Thiên Cơ Các
he_thong: chung
aliases: [ảnh trùng kỳ, ghi đè, ảnh mới thay ảnh cũ, Đã được thay, hai ảnh cùng ngày, số nào được dùng, capacity trùng ngày]
lien_quan: [trang-thai, tai-lai-anh-da-tai-truoc-do, ocr-lai-bao-cao, xoa-bao-cao, xem-cong-suat-va-thoi-gian-su-dung]
nguon_code: [frontend/js/history.js, backend/app/services/ingest.py, backend/app/api/reports.py]
cap_nhat: 2026-11-20
---
# Nhiều ảnh cùng kỳ báo cáo thì số nào được hiển thị

Còn gọi là: ghi đè, ảnh mới thay ảnh cũ, "hai ảnh cùng ngày thì lấy số nào", "Đã được thay".

Dashboard không bao giờ cộng hai ảnh của cùng một kỳ báo cáo. Mỗi kỳ chỉ dùng **một** báo cáo. Báo cáo không được dùng vẫn còn ở Tàng Kinh Các, có nhãn **"Đã được thay"**.

## Quy tắc với ảnh SCADA (HT1)

Hai ảnh SCADA **cùng dây chuyền** và **cùng khoảng "Thời gian quét"** là cùng kỳ. Ảnh đọc xong **sau cùng** được dùng, thay ảnh trước.

Hai ảnh cùng ngày nhưng khác dây chuyền là hai báo cáo riêng, cùng hiện trên dashboard.

## Quy tắc với ảnh Sorted và BCR rate (HT2)

Hai ảnh Sorted (hoặc hai ảnh BCR rate) có **cùng khoảng thời gian** trên ảnh là cùng kỳ. Ảnh đọc xong sau cùng được dùng.

## Quy tắc với ảnh Capacity (HT2)

Một ảnh Capacity chứa nhiều ngày. Mỗi ngày chỉ có **một** giá trị Công suất AVG:
- Nhiều ảnh cùng có một ngày: dùng ảnh có **ngày cuối khoảng truy vấn muộn hơn**.
- Hai ảnh có ngày cuối bằng nhau: dùng ảnh đọc xong sau.
- Ảnh mới thay ảnh cũ mà số khác nhau thì ảnh mới có cảnh báo "Công suất AVG ngày dd/mm khác ảnh trước …".

Ví dụ: ảnh A truy vấn 05/11–10/11, ảnh B truy vấn 08/11–12/11. Ngày 08/11–10/11 dùng số của ảnh B. Ngày 05/11–07/11 vẫn dùng ảnh A.

## Sửa tay, OCR lại và xóa ảnh hưởng thế nào

- **Lưu** (sửa tay) một báo cáo SCADA, Sorted hoặc BCR rate: báo cáo đó trở thành báo cáo được dùng cho kỳ của nó, kể cả khi trước đó nó "Đã được thay". Với Capacity: chỉ những ngày mà ảnh đang dùng không có ngày cuối khoảng truy vấn muộn hơn mới lấy số của báo cáo vừa lưu.
- **OCR lại**: tạo báo cáo mới, thay báo cáo cũ trên dashboard.
- **Xóa** báo cáo đang dùng: báo cáo cũ hơn **không** tự quay lại. Ngày đó trống trên dashboard cho tới khi mở báo cáo cũ và bấm "Lưu", hoặc tải ảnh mới.

## Cách biết báo cáo nào đang được dùng

Ở trang **"Tàng Kinh Các"**, bấm vào dòng báo cáo. Dòng **"Trên dashboard"** ghi:
- "Đang dùng": số của báo cáo này đang hiện trên dashboard.
- "Đã được thay bằng ảnh mới hơn": số của báo cáo này không hiện trên dashboard.
