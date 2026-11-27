---
id: tai-anh-len
title: Tải ảnh báo cáo lên để hệ thống đọc số liệu
loai: tac-vu
trang: Truyền Pháp Ảnh
he_thong: chung
aliases: [upload ảnh, tải ảnh, đẩy ảnh lên, nạp ảnh, OCR ảnh, gửi ảnh báo cáo, Khai Phá Thiên Cơ]
lien_quan: [truyen-phap-anh, chon-loai-anh, theo-doi-tien-do-xu-ly-anh, tai-lai-anh-da-tai-truoc-do, gioi-han-va-quy-tac]
nguon_code: [frontend/html/upload.html, frontend/js/upload.js, backend/app/api/upload.py]
cap_nhat: 2026-11-20
---
# Tải ảnh báo cáo lên để hệ thống đọc số liệu

Còn gọi là: upload ảnh, đẩy ảnh lên, nạp ảnh, OCR ảnh, "chỗ nào để tải ảnh".

**Kết quả:** mỗi ảnh có dòng trạng thái **"✓ Thành công"** hoặc **"✓ Xong, cần kiểm tra"**. Số liệu đọc được hiện trên trang **Thiên Cơ Các** và **Tàng Kinh Các**.
**Cần có trước:** đã đăng nhập; ảnh chụp màn hình báo cáo SCADA hoặc DMWCS (Sorted, Capacity, BCR rate), định dạng .jpg, .jpeg, .png hoặc .webp, mỗi ảnh tối đa 10 MB.

## Các bước tải ảnh lên

1. Bấm menu **"Truyền Pháp Ảnh"**.
2. Kéo thả ảnh vào vùng **"Kéo thả ảnh vào đây hoặc bấm để chọn"**. Hoặc bấm vào vùng đó rồi chọn ảnh. Chọn được nhiều ảnh một lúc.
3. Mỗi ảnh hiện một dòng: ảnh nhỏ, tên file, chữ **"Chưa gửi"**.
4. (Nên làm) Chọn loại ảnh ở ô **"Loại cho tất cả ảnh"**, hoặc ở ô cạnh tên từng ảnh. Để **"Thần Niệm (tự nhận diện)"** thì hệ thống tự đoán loại. Xem [Chọn loại ảnh](chon-loai-anh.md).
5. Bấm **"Khai Phá Thiên Cơ"**. Các ảnh được gửi lần lượt, mỗi ảnh có thanh tiến trình và đồng hồ chạy.
6. Chờ tới khi mỗi ảnh hiện **"✓ Thành công · Xem / Sửa"** hoặc **"✓ Xong, cần kiểm tra · Xem / Sửa"**. Góc phải dưới cũng hiện thông báo cho từng ảnh.
7. Ảnh "cần kiểm tra": bấm **"Xem / Sửa"** để so số với ảnh và sửa nếu sai.

Muốn thêm ảnh sau khi đã gửi: kéo thả thêm ảnh rồi bấm lại **"Khai Phá Thiên Cơ"**. Chỉ ảnh chưa gửi mới được gửi.

## Nếu tải ảnh lên không thành công

| Hiện tượng | Nguyên nhân | Cách xử lý |
| --- | --- | --- |
| Vùng kéo thả ghi "Chưa nhập môn, chưa thể truyền ảnh…" | Chưa đăng nhập | Bấm "Nhập Môn" ở góc trên bên phải |
| Chọn file mà không hiện trong danh sách | File không phải .jpg, .jpeg, .png, .webp | Chụp lại / lưu lại ảnh đúng định dạng |
| "Ảnh đã được xử lý trước đó" | Ảnh này đã tải lên rồi | Xem [Tải lại ảnh đã tải trước đó](tai-lai-anh-da-tai-truoc-do.md) |
| "✕ Thất bại" | Ảnh quá lớn, hỏng, hoặc không đọc được | Xem [lỗi OCR thất bại](../loi/ocr-that-bai.md) |
| Nút "Khai Phá Thiên Cơ" bị mờ | Chưa có ảnh mới chưa gửi | Thêm ảnh trước |

## Lưu ý khi tải ảnh lên

- Mỗi ảnh được đọc 2 lần rồi so với nhau. Lệch nhau thì báo cáo bị đánh dấu "cần kiểm tra".
- Ảnh được xử lý lần lượt theo hàng đợi chung của cả chi nhánh. Nhiều người cùng tải thì phải chờ lâu hơn.
- Bấm **"Xóa Bỏ Phế Tích"** chỉ xóa danh sách trên màn hình. Ảnh đã gửi vẫn được đọc tiếp, kết quả xem ở Tàng Kinh Các.
- Tải ảnh mới cùng dây chuyền, cùng kỳ báo cáo thì ảnh mới thay ảnh cũ trên dashboard. Xem [Số nào được hiển thị](../tham-chieu/so-lieu-nao-duoc-hien-thi.md).
- Dữ liệu chỉ giữ 35 ngày. Ảnh của ngày báo cáo cũ hơn 35 ngày sẽ bị xóa trong lần dọn dẹp ban đêm.
