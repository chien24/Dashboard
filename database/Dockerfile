# Database: PostgreSQL + script tạo role cho BE (ocr) và chatbot (ocr_ro). Build:  docker build -t ocr-dashboard-db database
FROM postgres:17.12-alpine

RUN apk upgrade --no-cache  # vá gói Alpine (zlib, openssl...)
COPY init-roles.sh /docker-entrypoint-initdb.d/10-init-roles.sh

# TCP (-h 127.0.0.1): chỉ "healthy" khi server thật đã chạy, không phải server tạm lúc đang chạy script khởi tạo
HEALTHCHECK --interval=10s --timeout=5s --start-period=30s --retries=5 \
    CMD pg_isready -h 127.0.0.1 -U ocr -d ocr || exit 1
