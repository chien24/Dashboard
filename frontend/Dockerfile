# FE: nginx phục vụ giao diện, chuyển /api/ và /uploads/ sang BE (backend:8000). Build:  docker build -t ocr-dashboard-frontend frontend
FROM nginx:1.30.8-alpine

# vá gói Alpine; chạy nginx bằng user thường: bỏ "user", pid ra /tmp, cho user nginx ghi thư mục cache
RUN apk upgrade --no-cache \
    && sed -i -e '/^user /d' -e 's,^pid .*,pid /tmp/nginx.pid;,' /etc/nginx/nginx.conf \
    && chown -R nginx:nginx /var/cache/nginx \
    && rm -f /usr/share/nginx/html/index.html /usr/share/nginx/html/50x.html

COPY nginx.conf /etc/nginx/conf.d/default.conf
# từng thư mục riêng: không đưa Dockerfile, nginx.conf, vercel.json ra web
COPY favicon.ico /usr/share/nginx/html/
COPY html /usr/share/nginx/html/html
COPY css /usr/share/nginx/html/css
COPY js /usr/share/nginx/html/js
COPY img /usr/share/nginx/html/img
COPY assets /usr/share/nginx/html/assets
COPY media /usr/share/nginx/html/media

USER nginx
EXPOSE 8080
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD wget -q -O /dev/null http://127.0.0.1:8080/html/index.html || exit 1
