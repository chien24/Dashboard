---
id: xem-ty-le-doc-cua-scanner
title: Xem tỷ lệ đọc thành công của từng Scanner
loai: tac-vu
trang: Thiên Cơ Các
he_thong: HT2
aliases: [BCR rate, tỷ lệ đọc mã vạch, Scanner, đầu đọc, BCR_NO, Hours&BcrRate, scanner nào đọc kém]
lien_quan: [dashboard-tab-ht2, chi-so-ht2-dmwcs, chon-loai-anh, canh-bao-so-lieu]
nguon_code: [frontend/js/dashboard.js]
cap_nhat: 2026-11-20
---
# Xem tỷ lệ đọc thành công của từng Scanner

Còn gọi là: BCR rate, tỷ lệ đọc mã vạch, đầu đọc, "Scanner nào đọc kém nhất".

**Kết quả:** thấy tỷ lệ đọc thành công (RATE) của từng Scanner trong một ngày, kèm số lượt đọc.
**Cần có trước:** đã đăng nhập, đã tải ảnh loại **"DMWCS BCR rate"** (màn hình Hours&BcrRate) của ngày đó.

## Các bước xem tỷ lệ đọc của Scanner

1. Mở trang **"Thiên Cơ Các"**, tab **"HT2 – DMWCS (CBS)"**.
2. Tìm khung **"Tỷ lệ đọc thành công của từng Scanner ngày dd/mm/yyyy"**.
3. Mỗi cột là một Scanner ("Scanner 1", "Scanner 2"…). Chiều cao cột là RATE, trục dọc từ 0% tới 100%.
4. Rê chuột lên cột để xem RATE, TOTAL, SUCCESS, FAILED.
5. Dưới biểu đồ có bảng: **BCR_NO**, **TOTAL**, **SUCCESS**, **FAILED**, **RATE**.
6. Muốn xem ngày khác: bấm vào ngày đó trên một biểu đồ theo ngày của tab HT2.

## Nếu không xem được tỷ lệ đọc của Scanner

| Hiện tượng | Nguyên nhân | Cách xử lý |
| --- | --- | --- |
| "Chưa có dữ liệu Scanner ngày …" | Không có ảnh BCR rate nào trong khoảng ngày | Tải ảnh BCR rate lên |
| "Ngày … chưa có dữ liệu Scanner, đang hiện ngày gần nhất có dữ liệu." | Ngày đang chọn chưa có ảnh BCR rate | Tải ảnh BCR rate của ngày đó lên |
| Thiếu một Scanner (ví dụ không có Scanner 4) | Bảng trên màn hình máy không có Scanner đó | Bình thường, không điền 0 |
| Cột có dấu "⚠" trên đầu | Số của Scanner đó không khớp nhau | Rê chuột xem cảnh báo, mở báo cáo để sửa |

## Lưu ý khi xem tỷ lệ đọc của Scanner

- RATE = SUCCESS / TOTAL. TOTAL, SUCCESS, FAILED tính bằng lượt quét.
- Dưới biểu đồ ghi "Thông tin tham khảo · báo cáo …" kèm khoảng thời gian của báo cáo.
- Mỗi Scanner có màu cố định. Từ Scanner 7 trở đi dùng màu xám.
