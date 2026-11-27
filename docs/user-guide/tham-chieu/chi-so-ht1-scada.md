---
id: chi-so-ht1-scada
title: Chỉ số HT1 – SCADA
loai: tham-chieu
trang: Thiên Cơ Các
he_thong: HT1
aliases: [ALL HT1, REJECT HT1, CORRECT HT1, tỷ lệ REJECT SCADA, công suất MAX, thời gian sử dụng HT1, tỷ lệ bất thường, loại bất thường, số lượng đã quét]
lien_quan: [dashboard-tab-ht1, xem-thanh-phan-reject, so-sanh-cac-day-chuyen, thuat-ngu, sua-so-lieu-ocr-sai]
nguon_code: [frontend/js/dashboard.js, frontend/js/history.js]
cap_nhat: 2026-11-20
---
# Chỉ số HT1 – SCADA

Còn gọi là: chỉ số SCADA, "ALL HT1 là gì", "REJECT HT1 tính thế nào", công suất MAX.

Mỗi ảnh SCADA là báo cáo của **một dây chuyền trong một ngày**, chụp từ màn hình "Thống kê và phân tích dữ liệu". Đơn vị đếm là bưu kiện.

## Chỉ số chính trên tab HT1 – SCADA

| Tên trên giao diện | Ý nghĩa | Cách tính | Đơn vị |
| --- | --- | --- | --- |
| **ALL** | Tổng bưu kiện đi qua máy quét | = "Số lượng đã quét" trên ảnh | bưu kiện |
| **REJECT** | Bưu kiện lỗi | = Không có mã vạch + Yêu cầu ống dẫn thất bại | bưu kiện |
| **CORRECT** | Bưu kiện đúng | = ALL − REJECT | bưu kiện |
| **Tỷ lệ REJECT** | Phần trăm lỗi | = REJECT / ALL | % |
| Tỷ lệ CORRECT (trong ngoặc ở thẻ CORRECT) | Phần trăm đúng | = 100% − Tỷ lệ REJECT | % |
| **Công suất MAX** | Sản lượng lớn nhất trong 60 phút liên tục | = "Công suất cao nhất trong một giờ" trên ảnh | bưu kiện/giờ |
| **Khung giờ MAX** | Khoảng 1 giờ đạt Công suất MAX | Lấy từ dòng "Thời gian xảy ra" trên ảnh | giờ:phút |
| **Thời gian sử dụng** | Số giờ máy chạy, ước tính | = ALL / Công suất MAX | giờ (h) |

HT1 không có Công suất AVG.

## Hai thành phần của REJECT HT1

- **"Không có mã vạch"**: bưu kiện không đọc được mã vạch (loại "Không Có Mã Vạch" trên ảnh).
- **"Yêu cầu ống dẫn thất bại"**: hệ thống không yêu cầu được máng chia cho bưu kiện.

Các loại bất thường khác trên ảnh **không** tính vào REJECT: "Không có Báo cáo Phân loại", "Khóa Ô Phân Loại Quá Vòng", "Không Có Quy Tắc", "Không Có Nhiệm Vụ", "Khác", và các loại chữ Trung (thiết bị vật lý bất thường, thiết bị ô/máng bất thường).

## Số liệu tham khảo của HT1 ở Tàng Kinh Các

| Tên trên giao diện | Ý nghĩa | Đơn vị |
| --- | --- | --- |
| "Số lượng gói theo lưới" | Số gói có kết quả theo lưới; mẫu số của Tỷ lệ bất thường | bưu kiện |
| "Số lượng bưu kiện bất thường" | Số bưu kiện có ít nhất một bất thường | bưu kiện |
| "Tỷ lệ bất thường" | = bưu kiện bất thường / gói theo lưới | % |
| "Thời gian quét trung bình" | Thời gian quét trung bình mỗi bưu kiện | giây |
| Bảng loại bất thường | Từng loại: số lượng và tỷ lệ trên số bưu kiện bất thường | bưu kiện, % |

Tổng tỷ lệ các loại bất thường thường lớn hơn 100%, vì một bưu kiện có thể thuộc nhiều loại.

## Tên trường HT1 trên trang Xem / sửa report

| Tên trường | Ý nghĩa |
| --- | --- |
| `day_chuyen` | Tên dây chuyền |
| `thoi_gian_tu`, `thoi_gian_den` | Đầu và cuối kỳ báo cáo |
| `so_luong_da_quet` | Số lượng đã quét (ALL) |
| `so_luong_goi_theo_luoi` | Số lượng gói theo lưới |
| `so_buu_kien_bat_thuong`, `ty_le_bat_thuong` | Số và tỷ lệ bưu kiện bất thường |
| `thoi_gian_quet_trung_binh` | Thời gian quét trung bình (giây) |
| `cong_suat_cao_nhat_1h`, `cong_suat_max_tu`, `cong_suat_max_den` | Công suất MAX và khung giờ |
| `phan_bo_bat_thuong[n]`: `loai`, `so_luong`, `ty_le` | Từng loại bất thường |

## Ngày báo cáo của ảnh SCADA

Ngày báo cáo là ngày của mốc đầu ô "Thời gian quét" trên ảnh. Mỗi kỳ báo cáo là một ngày.
