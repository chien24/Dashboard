# BE: FastAPI + worker OCR + chatbot. Build từ thư mục gốc repo (cần docs/user-guide cho chatbot):
#   docker build -f backend/Dockerfile -t ocr-dashboard-backend .
# .env KHÔNG nằm trong image (truyền lúc chạy bằng env_file); ảnh, log nằm ở volume /data; database là container riêng.
FROM python:3.12.15-slim-trixie

# TZ: giờ trong log theo giờ Việt Nam (app tự tính ngày báo cáo theo TIMEZONE trong .env)
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 TZ=Asia/Ho_Chi_Minh DATA_DIR=/data

RUN apt-get update && apt-get install -y --no-install-recommends tzdata \
    && rm -rf /var/lib/apt/lists/* \
    && useradd --create-home --uid 1000 app \
    && mkdir /data && chown app:app /data

WORKDIR /app/backend
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
# code thuộc root, user app chỉ đọc; chỉ ghi được vào /data (.dockerignore ở thư mục gốc: chỉ backend/ + docs/user-guide/)
COPY . /app

USER app
EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=5s --start-period=30s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/api/system/health', timeout=4)"
# đúng 1 tiến trình: worker OCR và lịch dọn dữ liệu chạy trong tiến trình này, KHÔNG thêm --workers.
# --proxy-headers: lấy IP thật từ FE (nginx) / tunnel; BE không mở cổng ra ngoài nên chỉ FE / tunnel gửi được header này
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--proxy-headers", "--forwarded-allow-ips=*"]
