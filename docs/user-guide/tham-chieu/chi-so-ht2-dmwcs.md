---
id: chi-so-ht2-dmwcs
title: Chỉ số HT2 – DMWCS
loai: tham-chieu
trang: Thiên Cơ Các
he_thong: HT2
aliases: [ALL HT2, Total, CorrectChute, PDA, RejectChute, NoRead, NoPostOffice, NoChute, SortFailed, công suất AVG, BCR rate, RATE, chỉ số DMWCS]
lien_quan: [dashboard-tab-ht2, xem-ty-le-doc-cua-scanner, xem-cong-suat-va-thoi-gian-su-dung, xem-thanh-phan-reject, thuat-ngu]
nguon_code: [frontend/js/dashboard.js, frontend/js/history.js]
cap_nhat: 2026-11-20
---
# Chỉ số HT2 – DMWCS

Còn gọi là: chỉ số DMWCS, chỉ số CBS, "CORRECT HT2 có tính PDA không", công suất AVG.

HT2 là máy CBS, không chia dây chuyền. Số liệu HT2 đến từ ba loại ảnh: **Sorted**, **Capacity** và **BCR rate**.

## Chỉ số từ ảnh Sorted ("The Report of Sorted parcels")

| Tên trên giao diện | Ý nghĩa | Cách tính | Đơn vị |
| --- | --- | --- | --- |
| **ALL** | Tổng bưu kiện | = Total trên ảnh | bưu kiện |
| **CORRECT** | Bưu kiện đúng | = CorrectChute + PDA | bưu kiện |
| CorrectChute | Vào đúng máng | Từ ảnh | bưu kiện |
| PDA ("trong đó PDA") | Xử lý qua PDA (chia tay), nằm trong CORRECT | Từ ảnh | bưu kiện |
| **REJECT** | Rơi vào máng lỗi | = RejectChute trên ảnh | bưu kiện |
| **Tỷ lệ REJECT** | Phần trăm lỗi | = REJECT / ALL | % |
| **Tỷ lệ CORRECT** | Phần trăm đúng | = 100% − Tỷ lệ REJECT | % |

CORRECT + REJECT = ALL.

## Thành phần REJECT của HT2

| Tên | Ý nghĩa | Tỷ lệ tính trên |
| --- | --- | --- |
| **NoRead** | Không đọc được mã | RejectChute |
| **NoPostOffice** | Không có bưu cục phát | RejectChute |
| **NoChute** | Không có máng | RejectChute |

NoRead + NoPostOffice + NoChute = RejectChute. Ở Tàng Kinh Các còn có danh sách **"Máng NoChute"** (số máng) và **SortFailed** (chia chọn thất bại, chỉ để tham khảo, không dùng tính chỉ số). "Biểu đồ tròn DMWCS" ghi % Correct và % Reject đọc từ ảnh.

## Chỉ số từ ảnh Capacity ("The Report of Capacity")

| Tên trên giao diện | Ý nghĩa | Đơn vị |
| --- | --- | --- |
| **Công suất AVG** | Công suất trung bình trong ngày | bưu kiện/giờ |
| **Thời gian sử dụng** | = ALL / Công suất AVG cùng ngày | giờ (h) |

Một ảnh Capacity chứa nhiều ngày (khoảng ngày truy vấn). Mỗi ngày chỉ dùng một giá trị.

## Chỉ số từ ảnh BCR rate (Hours&BcrRate)

| Tên trên giao diện | Ý nghĩa | Đơn vị |
| --- | --- | --- |
| Scanner n (**BCR_NO**) | Số hiệu đầu đọc mã vạch | số |
| **RATE** | Tỷ lệ đọc thành công = SUCCESS / TOTAL | % |
| **TOTAL** | Số lượt quét | lượt |
| **SUCCESS** | Số lượt đọc được | lượt |
| **FAILED** | Số lượt không đọc được | lượt |

## Tên trường HT2 trên trang Xem / sửa report

| Tên trường | Ý nghĩa |
| --- | --- |
| `thoi_gian_tu`, `thoi_gian_den` | Đầu và cuối kỳ báo cáo (Sorted, BCR rate) |
| `total`, `correct_chute`, `pda`, `reject_chute`, `sort_failed` | Total, CorrectChute, PDA, RejectChute, SortFailed |
| `no_read`, `no_post_office`, `no_chute`: `so_luong`, `ty_le` | Số lượng và % của NoRead, NoPostOffice, NoChute |
| `no_chute_danh_sach` | Danh sách máng NoChute, ngăn bằng dấu / |
| `pie_correct_pct`, `pie_reject_pct` | % Correct và % Reject trên biểu đồ tròn |
| `tu_ngay`, `den_ngay` | Khoảng ngày truy vấn (Capacity) |
| `cong_suat_theo_ngay[n]`: `ngay`, `cong_suat` | Công suất từng ngày (Capacity) |
| `bcr[n]`: `bcr_no`, `total`, `success`, `failed`, `rate` | Từng Scanner (BCR rate) |

## Ngày báo cáo của ảnh HT2

Sorted và BCR rate: ngày của mốc đầu ô thời gian trên ảnh. Capacity: mỗi điểm trên biểu đồ là một ngày; ngày báo cáo của cả ảnh là ngày cuối khoảng truy vấn.
