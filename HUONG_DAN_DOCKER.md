# Chạy OCR Dashboard bằng Docker

Máy chạy **không cần Python, không cần source code**. Chỉ cần Docker (Windows/macOS: Docker Desktop; Linux: Docker Engine + plugin compose).

- Code và Python nằm trong **image** `ocr-dashboard:latest`.
- Cấu hình nằm trong file **`.env`**, đặt cạnh `docker-compose.yml`. File này không nằm trong image.
- Dữ liệu (database, ảnh, log) nằm trong **volume** `ocr-dashboard-data`. Xóa container hay cài image mới thì dữ liệu vẫn còn.

---

## 1. Máy có source code: build và đóng gói

```powershell
cd D:\Học\TT\project\dashboard
docker build -t ocr-dashboard:latest .
docker save -o ocr-dashboard.tar ocr-dashboard:latest
```

Gửi cho máy nhận **3 file**:

| File | Lấy ở đâu |
|---|---|
| `ocr-dashboard.tar` | vừa tạo bằng lệnh `docker save` |
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
   - API key OCR: ít nhất một trong `CLOUDFLARE_ACCOUNT_ID` + `CLOUDFLARE_API_KEY`, `NVIDIA_API_KEY`, `OPEN_ROUTER_API_KEY`;
   - `GROQ_API_KEY` nếu dùng chatbot.
4. Chạy:

   ```powershell
   docker compose up -d
   docker compose ps          # đợi cột STATUS hiện "healthy" (khoảng 10–30 giây)
   ```

5. Mở trình duyệt: **http://localhost:8000**

App tự khởi động lại khi máy khởi động lại, miễn là Docker Desktop được bật cùng Windows.

**Đổi cổng:** thêm dòng `APP_PORT=8080` vào `.env`, rồi chạy `docker compose up -d`.

---

## 3. Dùng hằng ngày

Mọi lệnh chạy trong thư mục có `docker-compose.yml`.

| Muốn | Lệnh |
|---|---|
| Tắt web | `docker compose stop` |
| Bật lại | `docker compose start` |
| Xem trạng thái | `docker compose ps` |
| Xem log trực tiếp | `docker compose logs -f app` (Ctrl + C để thoát) |
| Xem log có lọc (hỏi tài khoản web) | `docker compose exec app python scripts/logs.py --level WARNING` |
| Xem database, chỉ đọc (hỏi tài khoản web) | `docker compose exec app python scripts/dbshell.py info` |

`logs.py` và `dbshell.py` dùng giống như khi chạy từ source. Các tham số xem `--help`, ví dụ `docker compose exec app python scripts/dbshell.py --help`.

### Sửa cấu hình `.env`

1. Sửa file `.env` cạnh `docker-compose.yml` (`notepad .env` hoặc `nano .env`).
2. Áp dụng: `docker compose up -d`. Lệnh này thấy `.env` đổi thì tự tạo lại container. Dữ liệu không mất.

Không dùng được `scripts/env.py` trong container, vì `.env` nằm ngoài container.

---

## 4. Cloudflare Tunnel (tùy chọn: cho người ngoài truy cập)

1. Trên Cloudflare Zero Trust, tạo tunnel rồi lấy **token**.
2. Trong phần **Public Hostname** của tunnel, cho hostname trỏ tới **`http://app:8000`**. Phải là `app`, không phải `localhost`.
3. Điền `TUNNEL_TOKEN=<token>` vào `.env`.
4. Chạy kèm tunnel:

   ```powershell
   docker compose --profile tunnel up -d
   ```

Tắt tunnel nhưng giữ web: `docker compose stop tunnel`.

---

## 5. Cập nhật phiên bản mới

- **Máy có source:** build và `docker save` lại như mục 1, rồi chỉ gửi `ocr-dashboard.tar` mới. `docker-compose.yml` chỉ gửi lại khi có thay đổi.
- **Máy nhận:**

  ```powershell
  docker load -i ocr-dashboard.tar
  docker compose up -d
  ```

Dữ liệu và `.env` giữ nguyên. Nếu bản mới có thêm biến trong `.env.example`, tự thêm biến đó vào `.env`.

---

## 6. Sao lưu và khôi phục dữ liệu

**Sao lưu** ra file `backup.tgz` trong thư mục hiện tại:

```powershell
docker compose stop app
docker run --rm -v ocr-dashboard-data:/data -v "${PWD}:/backup" ocr-dashboard:latest tar czf /backup/backup.tgz -C /data .
docker compose start app
```

**Khôi phục** từ `backup.tgz` (ghi đè dữ liệu hiện có):

```powershell
docker compose stop app
docker run --rm -v ocr-dashboard-data:/data -v "${PWD}:/backup" ocr-dashboard:latest sh -c "rm -rf /data/* && tar xzf /backup/backup.tgz -C /data"
docker compose start app
```

---

## 7. Chuyển dữ liệu từ bản chạy source (start_backend.bat) sang Docker

1. **Tắt backend cũ** (đóng cửa sổ `start_backend.bat`), để database ghi xong.
2. Chạy Docker lần đầu như mục 2 (để tạo volume), rồi tắt app:

   ```powershell
   docker compose up -d
   docker compose stop app
   ```

3. Chép database và ảnh cũ vào volume. Đổi đường dẫn `D:\...\backend\data` thành thư mục `backend\data` của máy cũ:

   ```powershell
   docker run --rm -v ocr-dashboard-data:/data -v "D:\Học\TT\project\dashboard\backend\data:/old:ro" ocr-dashboard:latest sh -c "cp -a /old/ocr.db* /data/ && cp -a /old/uploads /data/"
   ```

4. Bật app rồi **sửa đường dẫn ảnh**. Bảng `uploads` còn lưu đường dẫn Windows của máy cũ, nên nếu không sửa thì ảnh cũ không hiện:

   ```powershell
   docker compose start app
   docker compose exec app python scripts/fix_upload_paths.py            # xem trước sẽ sửa bao nhiêu dòng
   docker compose exec app python scripts/fix_upload_paths.py --apply    # ghi vào database
   ```

   Lệnh hỏi tài khoản web. Đó là tài khoản trong `.env` mới, không phải của máy cũ nếu bạn đã đổi.

5. Mở web, vào **Tàng Kinh Các**, mở thử một báo cáo cũ xem ảnh có hiện không.

---

## 8. Gỡ hẳn

```powershell
docker compose down              # xóa container, GIỮ dữ liệu
docker compose down -v           # xóa container VÀ dữ liệu (không lấy lại được)
docker image rm ocr-dashboard:latest
```
