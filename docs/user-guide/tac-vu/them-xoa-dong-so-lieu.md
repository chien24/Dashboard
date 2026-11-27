---
id: them-xoa-dong-so-lieu
title: Thêm hoặc xóa một dòng số liệu
loai: tac-vu
trang: Xem / sửa report
he_thong: chung
aliases: [Thêm giá trị, thêm dòng, xóa dòng, thêm loại bất thường, thêm Scanner, thêm ngày công suất, hệ thống đọc thiếu dòng, đọc thừa dòng]
lien_quan: [sua-so-lieu-ocr-sai, xem-sua-report, du-lieu-sua-khong-hop-le, chi-so-ht1-scada, chi-so-ht2-dmwcs]
nguon_code: [frontend/html/report.html, frontend/js/report.js]
cap_nhat: 2026-11-20
---
# Thêm hoặc xóa một dòng số liệu

Còn gọi là: "Thêm giá trị", thêm dòng, xóa dòng, "hệ thống đọc thiếu một loại bất thường", "đọc thừa một Scanner".

**Kết quả:** báo cáo có thêm (hoặc bớt) một dòng trong danh sách. Bấm "Lưu" xong, cạnh nút hiện **"Đã lưu. Dashboard dùng số liệu mới."**, trạng thái thành **"Đã sửa tay"**.
**Cần có trước:** đã đăng nhập; báo cáo loại SCADA, Capacity hoặc BCR rate.

## Báo cáo nào thêm dòng được

| Loại báo cáo | Một dòng là | Các ô của dòng |
| --- | --- | --- |
| SCADA | Một loại bất thường | `loai` (tên loại), `so_luong`, `ty_le` |
| Capacity | Một ngày công suất | `ngay` (dạng 2026-11-16), `cong_suat` |
| BCR rate | Một Scanner | `bcr_no`, `total`, `success`, `failed`, `rate` |

Báo cáo Sorted không có danh sách, nên không có nút **"Thêm giá trị"**.

## Các bước thêm một dòng số liệu

1. Mở trang **Xem / sửa report** của báo cáo (từ Tàng Kinh Các, nút **"Xem / sửa số liệu"**).
2. Bấm nút **"Thêm giá trị"**, cạnh nút "Lưu". Một khung dòng mới hiện ở cuối danh sách, ô đầu tiên được chọn sẵn. Cạnh nút hiện "Đã thêm 1 dòng. Điền giá trị rồi bấm Lưu."
3. Điền các ô theo ảnh gốc. Ô số mặc định là 0, ô chữ để trống.
4. Bấm **"Lưu"**.

## Các bước xóa một dòng số liệu

1. Tìm dòng thừa trong form, ví dụ khung `bcr[3]`.
2. Bấm nút đỏ **"Xóa dòng"** cạnh tên khung. Dòng biến mất. Cạnh nút hiện "Đã bỏ 1 dòng. Bấm Lưu để lưu lại."
3. Bấm **"Lưu"**.

## Nếu thêm hoặc xóa dòng không lưu được

| Hiện tượng | Nguyên nhân | Cách xử lý |
| --- | --- | --- |
| Lỗi có chữ "Sai schema" | Ô số bị gõ chữ hoặc để trống | Xem [lỗi khi lưu số liệu](../loi/du-lieu-sua-khong-hop-le.md) |
| "Report này vừa được sửa ở máy khác…" | Người khác vừa lưu | Tải lại trang rồi làm lại |
| Lỡ thêm / xóa nhầm khi chưa lưu | Chưa bấm "Lưu" thì chưa có gì thay đổi | Tải lại trang (F5) để về như cũ |

## Lưu ý khi thêm hoặc xóa dòng số liệu

- Thêm hoặc xóa dòng chỉ thay đổi trên màn hình cho tới khi bấm **"Lưu"**.
- Sau khi lưu, hệ thống kiểm tra lại số học. Ví dụ SCADA: tổng tỷ lệ các loại bất thường nhỏ hơn 100% sẽ có cảnh báo.
- Lỡ lưu sai thì vẫn quay về được bản hệ thống đọc ban đầu. Xem [Quay về một lần đọc cũ](quay-ve-phien-ban-ocr.md).
