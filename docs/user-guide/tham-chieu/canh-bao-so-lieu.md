---
id: canh-bao-so-lieu
title: Ý nghĩa các cảnh báo số liệu của báo cáo
loai: tham-chieu
trang: chung
he_thong: chung
aliases: [cảnh báo, warning, hộp cảnh báo, Lệch giữa lần 1 và lần 2, sai số học, vì sao cần kiểm tra, cảnh báo màu vàng]
lien_quan: [trang-thai, sua-so-lieu-ocr-sai, chi-so-ht1-scada, chi-so-ht2-dmwcs, so-lieu-nao-duoc-hien-thi]
nguon_code: [frontend/js/upload.js, frontend/js/report.js, backend/app/services/validate.py, backend/app/ocr/pipeline.py, backend/app/services/ingest.py]
cap_nhat: 2026-11-20
---
# Ý nghĩa các cảnh báo số liệu của báo cáo

Còn gọi là: cảnh báo, warning, "vì sao báo cáo bị cần kiểm tra", hộp cảnh báo màu vàng.

Sau khi đọc ảnh, hệ thống tự kiểm tra số liệu và ghi cảnh báo. Cảnh báo hiện ở hộp **"Cảnh báo"** (trang Truyền Pháp Ảnh, trang Xem / sửa report, chi tiết ở Tàng Kinh Các) và ở huy hiệu "⚠ n" trong bảng dashboard. Cảnh báo chỉ nhắc kiểm tra, hệ thống không tự sửa số.

## Cảnh báo lệch giữa hai lần đọc

Dạng: **"Lệch giữa lần 1 và lần 2 (lần 1 / lần 2) <tên trường>: <số lần 1> / <số lần 2>"**.
**Nghĩa là:** hai lần đọc cùng một ảnh ra số khác nhau. Hệ thống dùng số của lần 1. Báo cáo bị "Cần kiểm tra".
**Nên làm:** nhìn ảnh gốc, xem số nào đúng, sửa ô đó ở trang Xem / sửa report. Trên trang Truyền Pháp Ảnh, trường lệch được tô đỏ.

Dạng: **"Không đọc được lần 2 nên chưa đối chiếu: …"**. Lần đọc thứ hai lỗi, nên chưa so được. Báo cáo bị "Cần kiểm tra".

## Cảnh báo sai số học của ảnh SCADA

- "Số lượng bưu kiện bất thường / Số lượng gói theo lưới = … khác Tỷ lệ bất thường …%"
- "Số lượng gói theo lưới … > Số lượng đã quét …"
- "'<loại>': … khác tỷ lệ …% trên chú thích": tỷ lệ một loại bất thường không khớp.
- "Tổng tỷ lệ chú thích 'Phân bổ loại bất thường' = …% < 100%: thiếu loại hoặc đọc sai"
- "Nghi ngờ: tổng tỷ lệ chú thích đúng 100,00% …": tổng thường lớn hơn 100%, đúng 100% là đáng ngờ.
- "Khung giờ công suất MAX … không phải 59 phút"
- "Thời gian quét sai định dạng" hoặc "mốc đầu … không nhỏ hơn mốc cuối …"

## Cảnh báo sai số học của ảnh Sorted

- "CorrectChute + PDA + RejectChute = …, khác Total …"
- "NoRead + NoPostOffice + NoChute (dòng 1) = …, khác RejectChute …"
- "no_read: … / RejectChute = …%, khác …%" (tương tự cho no_post_office, no_chute)
- "(CorrectChute + PDA) / Total = …%, khác nhãn 'Correct' …%"
- "Correct …% + Reject …% khác 100%"
- "Ô thời gian sai định dạng" hoặc mốc đầu không nhỏ hơn mốc cuối.

## Cảnh báo của ảnh Capacity

- "Ô ngày sai định dạng", "Ngày thứ nhất … sau ngày thứ hai …"
- "Có N điểm có nhãn số nhưng từ … đến … có M ngày", "Thiếu nhãn số cho ngày: …"
- "Ngày sai định dạng hoặc ngoài khoảng đã chọn: …", "Ngày bị trùng: …", "Công suất <= 0 ở ngày: …"
- "Công suất AVG ngày dd/mm khác ảnh trước (… ở report #N): dùng … của ảnh này": hai ảnh Capacity cho cùng ngày ra số khác nhau; dashboard dùng số của ảnh này.

## Cảnh báo của ảnh BCR rate

- "Không đọc được dòng BCR nào: ảnh có đúng màn hình Hours&BcrRate không?"
- "BCR_NO bị trùng: …"
- "BCR n: SUCCESS + FAILED = …, khác TOTAL …", "BCR n: RATE …% ngoài khoảng 0–100", "BCR n: SUCCESS / TOTAL = …%, khác RATE …%". Trên biểu đồ Scanner, cột đó có dấu "⚠".

## Cảnh báo khác

- **"OCR lần 1: …"** hoặc **"OCR lần 2: …"**: ghi chú của hệ thống đọc ảnh, ví dụ chữ bị che hoặc danh sách NoChute bị cắt. Chỉ là ghi chú, không tự làm báo cáo "Cần kiểm tra".
- **"Loại bất thường chưa có trong …: '<tên>'"**: hệ thống chưa nhận ra tên loại bất thường SCADA này. Báo người quản trị để bổ sung.
- **"Đã sửa tay"**: báo cáo đã được người dùng lưu bằng tay.
