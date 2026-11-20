-- 7 view chỉ đọc cho chatbot (request/DAC_TA_CHATBOT.md mục 5). Chạy trong init_db() sau create_all; sửa view thì DROP rồi tạo lại.
DROP VIEW IF EXISTS v_scada_summary;
CREATE VIEW v_scada_summary AS
SELECT r.id AS report_id, r.report_date AS ngay, r.status AS trang_thai,
       s.day_chuyen, s.day_chuyen_key, s.thoi_gian_tu, s.thoi_gian_den,
       s.so_luong_da_quet, s.so_luong_goi_theo_luoi, s.so_buu_kien_bat_thuong,
       s.ty_le_bat_thuong, s.thoi_gian_quet_trung_binh, s.cong_suat_cao_nhat_1h,
       s.cong_suat_max_tu, s.cong_suat_max_den
FROM scada_summary s JOIN reports r ON r.id = s.report_id;

DROP VIEW IF EXISTS v_scada_abnormal;
CREATE VIEW v_scada_abnormal AS
SELECT r.id AS report_id, r.report_date AS ngay, r.status AS trang_thai,
       s.day_chuyen, s.day_chuyen_key,
       a.loai_key, a.loai_vi, a.loai_raw, a.so_luong, a.ty_le
FROM scada_abnormal a
JOIN reports r ON r.id = a.report_id
LEFT JOIN scada_summary s ON s.report_id = a.report_id;

DROP VIEW IF EXISTS v_dmwcs_sorted;
CREATE VIEW v_dmwcs_sorted AS
SELECT r.id AS report_id, r.report_date AS ngay, r.status AS trang_thai,
       r.thoi_gian_tu, r.thoi_gian_den,
       d.total, d.correct_chute, d.pda, d.reject_chute, d.sort_failed,
       d.no_read_so_luong, d.no_read_ty_le,
       d.no_post_office_so_luong, d.no_post_office_ty_le,
       d.no_chute_so_luong, d.no_chute_ty_le,
       d.no_chute_danh_sach, d.no_chute_bi_cat,
       d.pie_correct_pct, d.pie_reject_pct
FROM dmwcs_sorted d JOIN reports r ON r.id = d.report_id;

DROP VIEW IF EXISTS v_dmwcs_no_chute;
CREATE VIEW v_dmwcs_no_chute AS
SELECT r.id AS report_id, r.report_date AS ngay, r.status AS trang_thai,
       n.chute_no, n.co_the_bi_cat
FROM dmwcs_no_chute_items n JOIN reports r ON r.id = n.report_id;

DROP VIEW IF EXISTS v_dmwcs_capacity;
CREATE VIEW v_dmwcs_capacity AS
SELECT c.ngay, c.cong_suat, r.id AS report_id, r.status AS trang_thai,
       r.report_date AS ngay_anh  -- den_ngay của ảnh cung cấp giá trị, KHÔNG dùng để lọc
FROM dmwcs_capacity_daily c JOIN reports r ON r.id = c.report_id;

DROP VIEW IF EXISTS v_dmwcs_bcr;
CREATE VIEW v_dmwcs_bcr AS
SELECT r.id AS report_id, r.report_date AS ngay, r.status AS trang_thai,
       b.bcr_no, b.total, b.success, b.failed, b.rate
FROM dmwcs_bcr b JOIN reports r ON r.id = b.report_id;

DROP VIEW IF EXISTS v_report_quality;
CREATE VIEW v_report_quality AS
SELECT r.id AS report_id, r.loai, r.report_date AS ngay, r.status AS trang_thai,
       r.source_name, r.canh_bao, r.provider, r.model, r.created_at, r.updated_at,
       CASE r.loai
         WHEN 'scada'          THEN EXISTS (SELECT 1 FROM scada_summary        x WHERE x.report_id = r.id)
         WHEN 'dmwcs_sorted'   THEN EXISTS (SELECT 1 FROM dmwcs_sorted         x WHERE x.report_id = r.id)
         WHEN 'dmwcs_capacity' THEN EXISTS (SELECT 1 FROM dmwcs_capacity_daily x WHERE x.report_id = r.id)
         WHEN 'dmwcs_bcr_rate' THEN EXISTS (SELECT 1 FROM dmwcs_bcr            x WHERE x.report_id = r.id)
       END AS dang_hien_thi   -- 0 = report đã bị report mới hơn chiếm khóa
FROM reports r;
