---
id: khong-tai-duoc-du-lieu
title: Lỗi "Không tải được …" (dữ liệu, lịch sử, chi tiết, report)
loai: loi
trang: chung
he_thong: chung
aliases: [Không tải được dữ liệu, Không tải được lịch sử, Không tải được chi tiết, Không tải được report, Không có report này, "Thiếu ?id= trên đường dẫn", trang trắng không có số]
lien_quan: [can-dang-nhap, mat-ket-noi-may-chu, dashboard-thien-co-cac, tang-kinh-cac, xem-sua-report]
nguon_code: [frontend/js/dashboard.js, frontend/js/history.js, frontend/js/report.js, backend/app/api/reports.py]
cap_nhat: 2026-11-20
---
# Lỗi "Không tải được …" (dữ liệu, lịch sử, chi tiết, report)

Còn gọi là: trang không có số, lỗi tải trang, "Không có report này".

**Xuất hiện ở:**
- Trang **"Thiên Cơ Các"**: dòng đỏ đầu trang "Không tải được dữ liệu: …".
- Trang **"Tàng Kinh Các"**: "Không tải được lịch sử: …" dưới tab, hoặc "Không tải được chi tiết: …" trong một dòng báo cáo đã mở.
- Trang **Xem / sửa report**: tiêu đề thành "Không tải được report: …", hoặc "Thiếu ?id= trên đường dẫn".

**Nghĩa là:** trang không lấy được số liệu từ máy chủ. Phần sau dấu hai chấm là lý do.

**Nguyên nhân thường gặp:**
- "Cần đăng nhập": phiên đăng nhập đã hết. Xem [lỗi Cần đăng nhập](can-dang-nhap.md).
- "Không có report này": báo cáo đã bị xóa (bằng tay hoặc do quá 35 ngày).
- "Thiếu ?id= trên đường dẫn": mở trang Xem / sửa report trực tiếp mà không qua link.
- "Failed to fetch" hoặc lỗi mạng: mất mạng, máy chủ đang tắt hoặc khởi động lại.

**Cách xử lý:**
1. Đọc lý do sau dấu hai chấm.
2. Hết phiên: bấm **"Nhập Môn"** và đăng nhập lại.
3. Lỗi mạng: kiểm tra mạng, chờ vài phút rồi tải lại trang (F5).
4. Báo cáo không còn: quay về **"Tàng Kinh Các"** để tìm báo cáo khác.
5. Chi tiết một dòng ở Tàng Kinh Các lỗi: bấm thu gọn dòng rồi mở lại để thử lại.

**Nếu vẫn lỗi:** báo người hỗ trợ ở mục **"Gặp Kiếp Nạn"** cuối trang, kèm ảnh chụp màn hình thông báo lỗi.
