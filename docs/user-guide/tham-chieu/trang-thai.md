---
id: trang-thai
title: Các trạng thái của báo cáo và của ảnh đang xử lý
loai: tham-chieu
trang: chung
he_thong: chung
aliases: [trạng thái, status, can_kiem_tra, cần kiểm tra, da_sua_tay, đã sửa tay, ok, Đã được thay, huy hiệu cảnh báo]
lien_quan: [canh-bao-so-lieu, sua-so-lieu-ocr-sai, theo-doi-tien-do-xu-ly-anh, so-lieu-nao-duoc-hien-thi, tim-bao-cao]
nguon_code: [frontend/js/history.js, frontend/js/upload.js, frontend/js/dashboard.js, backend/app/ocr/pipeline.py, backend/app/api/reports.py]
cap_nhat: 2026-11-20
---
# Các trạng thái của báo cáo và của ảnh đang xử lý

Còn gọi là: status, "can_kiem_tra nghĩa là gì", "Đã được thay là sao", huy hiệu ⚠.

Trang **Tàng Kinh Các** ghi trạng thái bằng chữ tiếng Việt ("OK", "Cần kiểm tra", "Đã sửa tay"). Trang **Truyền Pháp Ảnh** và trang **Xem / sửa report** ghi bằng mã: `ok`, `can_kiem_tra`, `da_sua_tay`. Hai cách ghi là cùng một trạng thái.

## Trạng thái "OK" (ok) của báo cáo

**Nghĩa là:** hai lần đọc ảnh cho cùng kết quả, và các con số khớp nhau về số học.
**Khi nào xuất hiện:** ngay sau khi đọc ảnh xong, nếu không có lỗi.
**Nên làm gì:** không cần làm gì. Báo cáo "OK" vẫn có thể có vài ghi chú cảnh báo nhẹ, rê chuột lên huy hiệu "⚠" để đọc.

## Trạng thái "Cần kiểm tra" (can_kiem_tra) của báo cáo

**Nghĩa là:** số liệu có thể sai. Hai lần đọc ra số khác nhau, hoặc các số không khớp nhau (ví dụ CorrectChute + PDA + RejectChute khác Total), hoặc lần đọc thứ hai bị lỗi nên chưa đối chiếu được.
**Khi nào xuất hiện:** ngay sau khi đọc ảnh. Trang Truyền Pháp Ảnh hiện "✓ Xong, cần kiểm tra".
**Nên làm gì:**
1. Mở báo cáo ở trang **Xem / sửa report**.
2. Đọc hộp **"Cảnh báo"** để biết trường nào nghi sai.
3. So với ảnh gốc, sửa nếu sai, bấm **"Lưu"**. Trạng thái đổi thành "Đã sửa tay".

Xem ý nghĩa từng cảnh báo: [Cảnh báo số liệu](canh-bao-so-lieu.md).

## Trạng thái "Đã sửa tay" (da_sua_tay) của báo cáo

**Nghĩa là:** một người đã kiểm tra và lưu số liệu bằng tay.
**Khi nào xuất hiện:** sau khi bấm **"Lưu"**, hoặc **"Dùng bản này"** ở mục OCR Version, trên trang Xem / sửa report, dù có sửa số hay không.
**Nên làm gì:** không cần làm gì. Cảnh báo đầu tiên của báo cáo là "Đã sửa tay". Các cảnh báo sau là kết quả kiểm tra lại số học với số mới.

## Nhãn "Đã được thay" của báo cáo

**Nghĩa là:** đã có ảnh mới hơn cho cùng kỳ báo cáo (cùng dây chuyền, cùng ngày), nên báo cáo này không còn hiện trên dashboard. Báo cáo vẫn được giữ để xem lại.
**Nơi xuất hiện:** trang Tàng Kinh Các. Trong chi tiết, dòng "Trên dashboard" ghi "Đã được thay bằng ảnh mới hơn". Báo cáo đang dùng thì ghi "Đang dùng".
**Nên làm gì:** muốn đưa báo cáo này trở lại dashboard thì mở nó và bấm "Lưu". Xem [Số nào được hiển thị](so-lieu-nao-duoc-hien-thi.md).

## Huy hiệu cảnh báo "⚠ n" và "✓ 0"

Có ở bảng chi tiết của dashboard và ở Tàng Kinh Các. "⚠ 3" nghĩa là báo cáo có 3 cảnh báo; rê chuột lên huy hiệu để đọc (ở dashboard). "✓ 0" nghĩa là không có cảnh báo.

## Trạng thái của ảnh trên trang Truyền Pháp Ảnh

| Chữ hiển thị | Nghĩa là |
| --- | --- |
| "Chưa gửi" | Ảnh đã chọn, chưa bấm "Khai Phá Thiên Cơ" |
| "Đang gửi ảnh…" | Đang chuyển ảnh lên máy chủ |
| "Đang chờ tới lượt" | Ảnh đang trong hàng đợi |
| "Đang OCR · …" | Đang đọc ảnh; phần sau dấu chấm là bước đang chạy |
| "✓ Thành công" | Đọc xong, trạng thái ok |
| "✓ Xong, cần kiểm tra" | Đọc xong, trạng thái can_kiem_tra |
| "Ảnh đã được xử lý trước đó" | Ảnh trùng, hiện kết quả cũ |
| "✕ Thất bại" | Không đọc được ảnh |
