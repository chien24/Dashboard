# 7 view (SQLite)
Cột chung: report_id; ngay DATE 'YYYY-MM-DD' (ngày báo cáo, LỌC ngày bằng cột này); trang_thai ok|can_kiem_tra (số có thể sai)|da_sua_tay.
Mỗi kỳ báo cáo = 1 ngày. % lưu dạng 0–100.

## HT1 SCADA (theo dây chuyền)
v_scada_summary — 1 dòng/dây chuyền/ngày: day_chuyen (hiển thị), day_chuyen_key (lọc), thoi_gian_tu, thoi_gian_den,
so_luong_da_quet (kiện, = ALL), so_luong_goi_theo_luoi (kiện), so_buu_kien_bat_thuong (kiện),
ty_le_bat_thuong (% = bat_thuong/goi_theo_luoi), thoi_gian_quet_trung_binh (giây),
cong_suat_cao_nhat_1h (kiện/giờ, = Công suất MAX), cong_suat_max_tu, cong_suat_max_den (khung giờ MAX).
v_scada_abnormal — 1 dòng/loại bất thường/dây chuyền/ngày: day_chuyen, day_chuyen_key, loai_key (lọc/GROUP BY; UNKNOWN = chưa phân loại),
loai_vi (hiển thị), loai_raw (KHÔNG dùng), so_luong (kiện), ty_le (% = so_luong/so_buu_kien_bat_thuong; tổng các loại > 100% là bình thường).
Loại vắng mặt trong ngày dây chuyền đã có dữ liệu = 0.
Chỉ số HT1: ALL = so_luong_da_quet; REJECT = so_luong của NO_BARCODE + CHUTE_REQUEST_FAILED (loại khác không tính);
CORRECT = ALL − REJECT; tỷ lệ REJECT = REJECT/ALL; thời gian sử dụng (giờ, ước tính) = ALL / cong_suat_cao_nhat_1h. HT1 không có Công suất AVG.

## HT2 DMWCS (máy CBS, không chia dây chuyền)
v_dmwcs_sorted — 1 dòng/ngày: thoi_gian_tu, thoi_gian_den, total (kiện, = ALL), correct_chute, pda, reject_chute (= REJECT; total = correct_chute + pda + reject_chute),
sort_failed (không dùng cho chỉ số), no_read_so_luong/no_read_ty_le, no_post_office_so_luong/no_post_office_ty_le, no_chute_so_luong/no_chute_ty_le
(3 tỷ lệ này = so_luong/reject_chute; 3 số lượng cộng lại = reject_chute), no_chute_danh_sach (text '/'), no_chute_bi_cat (0/1),
pie_correct_pct (= (correct_chute+pda)/total), pie_reject_pct (= reject_chute/total).
Chỉ số HT2: CORRECT = correct_chute + pda; tỷ lệ REJECT = reject_chute/total; thời gian sử dụng (giờ) = total / Công suất AVG cùng ngày.
v_dmwcs_no_chute — 1 dòng/máng NoChute/ngày: chute_no, co_the_bi_cat (0/1: danh sách bị cắt, có thể thiếu).
v_dmwcs_capacity — 1 dòng/ngày: ngay (lọc), cong_suat (kiện/giờ, = Công suất AVG), ngay_anh (KHÔNG lọc).
v_dmwcs_bcr — 1 dòng/Scanner/ngày: bcr_no (INTEGER: "BCR 1" → bcr_no = 1), total (lượt), success, failed, rate (% = success/total). Ngày thiếu BCR nào đó là bình thường.

## Chất lượng
v_report_quality — 1 dòng/report: loai (scada | dmwcs_sorted | dmwcs_capacity | dmwcs_bcr_rate), ngay, trang_thai, source_name (tên ảnh),
canh_bao (JSON), provider, model, created_at, updated_at, dang_hien_thi (0 = đã bị ảnh mới hơn thay, hỏi số hiện tại thì lọc = 1).
