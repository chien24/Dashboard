---
id: xem-chi-tiet-bao-cao
title: Xem chi tiết một báo cáo và ảnh gốc
loai: tac-vu
trang: Tàng Kinh Các
he_thong: chung
aliases: [xem ảnh gốc, chi tiết báo cáo, giá trị gốc, xem cảnh báo của báo cáo, mở report, xem ảnh đã upload]
lien_quan: [tang-kinh-cac, tim-bao-cao, xem-sua-report, canh-bao-so-lieu, so-lieu-nao-duoc-hien-thi]
nguon_code: [frontend/js/history.js, frontend/js/report.js]
cap_nhat: 2026-11-20
---
# Xem chi tiết một báo cáo và ảnh gốc

Còn gọi là: xem ảnh gốc, mở report, "xem giá trị gốc", "xem cảnh báo của báo cáo".

**Kết quả:** thấy ảnh đã tải lên, số liệu hệ thống đọc được, các cảnh báo, và báo cáo có đang được dùng trên dashboard hay không.
**Cần có trước:** đã đăng nhập.

## Các bước xem chi tiết một báo cáo

1. Mở trang **"Tàng Kinh Các"**. Tìm báo cáo nếu cần (xem [Tìm báo cáo](tim-bao-cao.md)).
2. Bấm vào dòng báo cáo. Dòng mở ra, hiện "Đang tải…" rồi hiện chi tiết.
3. Bên trái chi tiết: ảnh nhỏ, **"Tên file"**, **"Upload lúc"**, **"Model"**, **"Trên dashboard"**, nút **"Xem / sửa số liệu"**.
4. Bấm ảnh nhỏ để mở ảnh gốc kích thước đầy đủ ở tab mới.
5. Bên phải chi tiết: số liệu theo loại báo cáo và danh sách **"Cảnh báo"**.
6. Bấm lại vào dòng để thu gọn.

## Số liệu hiện trong chi tiết theo từng loại báo cáo

- **SCADA**: "Dây chuyền (giá trị gốc)", "Thời gian quét", "Số lượng đã quét", "Số lượng gói theo lưới", "Số lượng bưu kiện bất thường", "Tỷ lệ bất thường", "Thời gian quét trung bình", "Công suất cao nhất 1h", "Khung giờ công suất MAX", và bảng loại bất thường (tên hiển thị, nhãn OCR gốc, số lượng, tỷ lệ).
- **Sorted**: "Thời gian", Total, CorrectChute, PDA, RejectChute, NoRead, NoPostOffice, NoChute, SortFailed, "Biểu đồ tròn DMWCS", và danh sách **"Máng NoChute"**.
- **Capacity**: "Khoảng ngày truy vấn" và công suất từng ngày (bưu kiện/giờ).
- **BCR rate**: "Thời gian" và bảng Scanner, TOTAL, SUCCESS, FAILED, RATE.

## Nếu không xem được chi tiết báo cáo

| Hiện tượng | Nguyên nhân | Cách xử lý |
| --- | --- | --- |
| "Không tải được chi tiết: …" | Mất mạng, hết phiên, hoặc báo cáo vừa bị xóa | Bấm thu gọn rồi mở lại dòng; đăng nhập lại nếu cần |
| "Không có ảnh gốc (import từ JSON)" | Báo cáo được nhập từ file dữ liệu, không có ảnh | Bình thường |
| Ảnh không mở được | Ảnh đã bị xóa theo hạn 35 ngày | Không khôi phục được |

## Lưu ý khi xem chi tiết báo cáo

- **"Trên dashboard"** ghi "Đang dùng" hoặc "Đã được thay bằng ảnh mới hơn". Báo cáo đã được thay không còn hiện trên dashboard.
- Bảng loại bất thường SCADA: tỷ lệ tính trên số bưu kiện bất thường, tổng có thể lớn hơn 100% vì một bưu kiện có thể thuộc nhiều loại.
- Máng NoChute: ô trên màn hình DMWCS bị cắt ở mép phải, nên danh sách có thể thiếu, máng cuối có thể thiếu chữ số.
- Muốn sửa số: bấm **"Xem / sửa số liệu"**. Xem [Sửa số liệu bị đọc sai](sua-so-lieu-ocr-sai.md).
