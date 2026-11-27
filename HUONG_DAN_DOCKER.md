# Chạy OCR Dashboard bằng Docker

Máy chạy **không cần Python, không cần source code**. Chỉ cần Docker (Windows/macOS: Docker Desktop; Linux: Docker Engine + plugin compose).

## Cấu trúc: 3 container nối nhau qua cổng

```
trình duyệt ──► frontend (nginx, cổng 8080) ──/api, /uploads──► backend (FastAPI, cổng 8000) ──► db (PostgreSQL, cổng 5432)
   localhost:8000 ──┘
```

| Container | Image | Việc |
|---|---|---|
| `frontend` | `ocr-dashboard-frontend` | Giao diện web (HTML/CSS/JS). Chuyển `/api/` và `/uploads/` sang backend |
| `backend` | `ocr-dashboard-backend` | API, OCR, chatbot. Ảnh và log nằm trong volume `ocr-dashboard-data` |
| `db` | `ocr-dashboard-db` | Database PostgreSQL, nằm trong volume `ocr-dashboard-db` |

- Chỉ `frontend` mở cổng ra máy, và chỉ ở `127.0.0.1`. `backend` và `db` chỉ thấy được trong mạng nội bộ của Docker.
- Cấu hình nằm trong file **`.env`**, đặt cạnh `docker-compose.yml`. File này không nằm trong image.
- Dữ liệu nằm trong 2 volume. Xóa container hay cài image mới thì dữ liệu vẫn còn.

---

## 1. Máy có source code: build và đóng gói

```powershell
cd D:\Học\TT\project\dashboard
docker build -t ocr-dashboard-db:latest database
docker build -t ocr-dashboard-backend:latest -f backend/Dockerfile .
docker build -t ocr-dashboard-frontend:latest frontend
docker save -o ocr-dashboard.tar ocr-dashboard-frontend:latest ocr-dashboard-backend:latest ocr-dashboard-db:latest
```

Gửi cho máy nhận **3 file**:

| File | Lấy ở đâu |
|---|---|
| `ocr-dashboard.tar` | vừa tạo bằng lệnh `docker save` (chứa cả 3 image) |
| `docker-compose.yml` | thư mục gốc repo |
| `.env.example` | `backend\.env.example` |

**Không gửi `.env` thật.** Nếu cần đưa API key cho người nhận, gửi riêng qua kênh an toàn.

---

## 2. Máy nhận: cài và chạy lần đầu

1. Tạo một thư mục, ví dụ `D:\OCRDashboard`, rồi chép 3 file vào đó.
2. Mở PowerShell (hoặc terminal) trong thư mục đó:

   ```powershell
   docker load -i ocr-dashboard.tar
   Copy-Item .env.example .env        # Linux: cp .env.example .env
   notepad .env                       # Linux: nano .env
   ```

3. Trong `.env`, điền ít nhất:
   - `AUTH_USER`, `AUTH_PASSWORD`: tài khoản đăng nhập web, **bắt buộc**;
   - `SESSION_SECRET`: một chuỗi ngẫu nhiên dài;
   - `POSTGRES_PASSWORD`, `DB_PASSWORD`, `DB_RO_PASSWORD`: 3 mật khẩu database, **bắt buộc**. Mỗi mật khẩu khác nhau, **chỉ dùng chữ và số**, nên từ 16 ký tự trở lên;
   - API key OCR: ít nhất một trong `CLOUDFLARE_ACCOUNT_ID` + `CLOUDFLARE_API_KEY`, `NVIDIA_API_KEY`, `OPEN_ROUTER_API_KEY`;
   - `GROQ_API_KEY` nếu dùng chatbot.
4. Chạy:

   ```powershell
   docker compose up -d
   docker compose ps          # đợi cả 3 dòng hiện "healthy" (khoảng 10–40 giây)
   ```

5. Mở trình duyệt: **http://localhost:8000**

App tự khởi động lại khi máy khởi động lại, miễn là Docker Desktop được bật cùng Windows: trong Docker Desktop, **Settings → General**, bật **Start Docker Desktop when you sign in to your computer**.

**Đổi cổng:** thêm dòng `APP_PORT=8080` vào `.env`, rồi chạy `docker compose up -d`.

---

## 3. Dùng hằng ngày

Mọi lệnh chạy trong thư mục có `docker-compose.yml`.

| Muốn | Lệnh |
|---|---|
| Tắt web | `docker compose stop` |
| Bật lại | `docker compose start` |
| Xem trạng thái | `docker compose ps` |
| Xem log trực tiếp | `docker compose logs -f backend` (Ctrl + C để thoát) |
| Xem log có lọc (hỏi tài khoản web) | `docker compose exec backend python scripts/logs.py --level WARNING` |
| Xem database, chỉ đọc (hỏi tài khoản web) | `docker compose exec backend python scripts/dbshell.py info` |

`logs.py` và `dbshell.py` dùng giống như khi chạy từ source. Các tham số xem `--help`, ví dụ `docker compose exec backend python scripts/dbshell.py --help`.

### Sửa cấu hình `.env`

1. Sửa file `.env` cạnh `docker-compose.yml` (`notepad .env` hoặc `nano .env`).
2. Áp dụng: `docker compose up -d`. Lệnh này thấy `.env` đổi thì tự tạo lại container. Dữ liệu không mất.

Không dùng được `scripts/env.py` trong container, vì `.env` nằm ngoài container.

### Đổi mật khẩu database

3 mật khẩu database chỉ được dùng **lúc tạo database lần đầu**. Muốn đổi về sau thì phải đổi cả trong database lẫn trong `.env`:

```powershell
docker compose exec db psql -U postgres -c "ALTER ROLE ocr PASSWORD 'MatKhauMoi123'"
# sửa DB_PASSWORD=MatKhauMoi123 trong .env, rồi:
docker compose up -d
```

`DB_RO_PASSWORD` (role `ocr_ro`) và `POSTGRES_PASSWORD` (role `postgres`) đổi theo cách tương tự.

---

## 4. Cloudflare Tunnel (cho người ngoài truy cập)

### Cách A, đang dùng: tunnel chạy dạng Windows service

Làm theo mục 3–5 của [HUONG_DAN_DEPLOY.md](HUONG_DAN_DEPLOY.md): cài `cloudflared` thành Windows service, route trỏ tới **`http://localhost:8000`** (cổng mà `frontend` mở trên máy). Cách này:

- **không** cần `TUNNEL_TOKEN` trong `.env` (để trống);
- **không** chạy profile `tunnel`;
- tunnel tự chạy khi bật máy, độc lập với Docker.

Tunnel đã có sẵn, chỉ cần cài lên máy mới: trên Cloudflare mở tunnel, bấm **+ Add a replica**, chọn **Windows**, rồi chạy lệnh `cloudflared.exe service install <token>` trong PowerShell mở bằng quyền Administrator. **Không** bấm _Rotate token_.

### Cách B: tunnel chạy trong Docker

1. Trên Cloudflare mở tunnel, bấm **+ Add a replica**, chọn **Docker**, copy phần sau `--token` (chuỗi `eyJ...`).
2. Điền `TUNNEL_TOKEN=<token>` vào `.env`.
3. Sửa route của tunnel: Service URL thành **`http://frontend:8080`**. Phải là `frontend`, không phải `localhost`.
4. Chạy kèm tunnel: `docker compose --profile tunnel up -d`.

⚠️ **Không dùng song song cách A và cách B** cho cùng một tunnel. Cloudflare sẽ chia lượt truy cập cho cả hai replica, mà mỗi bên chỉ hiểu một kiểu route (`localhost:8000` hoặc `frontend:8080`), nên khoảng một nửa lượt vào web báo lỗi. Chuyển sang cách B thì gỡ service Windows trước: `cloudflared service uninstall` (PowerShell Admin).

Tắt tunnel nhưng giữ web (cách B): `docker compose stop tunnel`.

---

## 5. Cập nhật phiên bản mới

- **Máy có source:** build và `docker save` lại như mục 1, rồi gửi `ocr-dashboard.tar` mới. `docker-compose.yml` chỉ gửi lại khi có thay đổi.
- **Máy nhận:**

  ```powershell
  docker load -i ocr-dashboard.tar
  docker compose up -d
  ```

Dữ liệu và `.env` giữ nguyên. Nếu bản mới có thêm biến trong `.env.example`, tự thêm biến đó vào `.env`.

---

## 6. Sao lưu và khôi phục dữ liệu

Có 2 phần cần sao lưu: **database** và **ảnh + log**.

**Sao lưu** ra 2 file trong thư mục hiện tại:

```powershell
docker compose exec db pg_dump -U postgres -Fc -f /tmp/db.dump ocr
docker compose cp db:/tmp/db.dump db.dump
docker run --rm -v ocr-dashboard-data:/data -v "${PWD}:/backup" ocr-dashboard-backend:latest tar czf /backup/data.tgz -C /data .
```

Không dùng `pg_dump ... > db.dump`, vì PowerShell làm hỏng file nhị phân khi ghi qua `>`.

**Khôi phục** (ghi đè dữ liệu hiện có):

```powershell
docker compose stop backend
docker compose cp db.dump db:/tmp/db.dump
docker compose exec db pg_restore -U postgres -d ocr --clean --if-exists --no-owner --role=ocr /tmp/db.dump
docker run --rm -v ocr-dashboard-data:/data -v "${PWD}:/backup" ocr-dashboard-backend:latest sh -c "rm -rf /data/* && tar xzf /backup/data.tgz -C /data"
docker compose start backend
```

---

## 7. Chuyển dữ liệu từ bản chạy source (start_backend.bat) sang Docker

Bản chạy source dùng SQLite (`backend\data\ocr.db`), còn Docker dùng PostgreSQL. Script `sqlite_to_postgres.py` chép toàn bộ dữ liệu sang. Script chỉ chép vào database **còn trống**.

1. **Tắt backend cũ** (đóng cửa sổ `start_backend.bat`), để database ghi xong.
2. Chạy Docker lần đầu như mục 2, **chưa** tải ảnh hay tạo dữ liệu gì trên bản Docker.
3. Chép database cũ sang. Đổi đường dẫn `D:\...\backend\data` thành thư mục `backend\data` của máy cũ:

   ```powershell
   docker compose run --rm -v "D:\Học\TT\project\dashboard\backend\data:/old:ro" backend python scripts/sqlite_to_postgres.py /old/ocr.db
   ```

4. Chép ảnh cũ vào volume:

   ```powershell
   docker run --rm -v ocr-dashboard-data:/data -v "D:\Học\TT\project\dashboard\backend\data:/old:ro" ocr-dashboard-backend:latest cp -a /old/uploads /data/
   ```

5. **Sửa đường dẫn ảnh.** Bảng `uploads` còn lưu đường dẫn Windows của máy cũ, nên nếu không sửa thì ảnh cũ không hiện:

   ```powershell
   docker compose exec backend python scripts/fix_upload_paths.py            # xem trước sẽ sửa bao nhiêu dòng
   docker compose exec backend python scripts/fix_upload_paths.py --apply    # ghi vào database
   ```

   Các lệnh ở bước 3 và bước 5 hỏi tài khoản web. Đó là tài khoản trong `.env` mới.

6. Mở web, vào **Tàng Kinh Các**, mở thử một báo cáo cũ xem số liệu và ảnh có hiện không.

---

## 8. Gỡ hẳn

```powershell
docker compose down              # xóa container, GIỮ dữ liệu
docker compose down -v           # xóa container VÀ dữ liệu: database, ảnh, log (không lấy lại được)
docker image rm ocr-dashboard-frontend:latest ocr-dashboard-backend:latest ocr-dashboard-db:latest
```
