#!/bin/sh
# Chạy 1 LẦN khi volume DB còn trống (docker-entrypoint-initdb.d). Đổi mật khẩu trong .env sau đó KHÔNG có tác dụng
# (xem HUONG_DAN_DOCKER.md mục "Đổi mật khẩu database").
#   ocr    : chủ database ocr, BE đọc/ghi bằng role này (không phải superuser)
#   ocr_ro : chatbot chạy SQL do LLM viết bằng role này; BE cấp SELECT trên 7 view lúc khởi động (views_postgres.sql)
set -eu

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" \
     -v app_pw="$DB_PASSWORD" -v ro_pw="$DB_RO_PASSWORD" <<'SQL'
CREATE ROLE ocr LOGIN PASSWORD :'app_pw';
CREATE ROLE ocr_ro LOGIN PASSWORD :'ro_pw';
CREATE DATABASE ocr OWNER ocr;
SQL

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname ocr <<'SQL'
REVOKE ALL ON DATABASE ocr FROM PUBLIC;
GRANT CONNECT ON DATABASE ocr TO ocr, ocr_ro;
REVOKE CREATE ON SCHEMA public FROM PUBLIC;
GRANT USAGE ON SCHEMA public TO ocr_ro;
SQL
