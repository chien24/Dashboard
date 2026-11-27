# Hướng dẫn đưa OCR Dashboard CNKT3 lên internet (miễn phí, dữ liệu để ở máy local)

Tài liệu này hướng dẫn từ đầu: cài đặt, lấy tên miền miễn phí, rồi mở dashboard cho người khác truy cập qua internet. **Dữ liệu và API key luôn nằm trên máy của bạn.** Không cần mở port router, không tốn tiền.

App chạy bằng **Docker**: máy chạy không cần Python, không cần source code. Chi tiết từng lệnh Docker xem [HUONG_DAN_DOCKER.md](HUONG_DAN_DOCKER.md).

---

## 0. Cách hoạt động

```
Người dùng (trình duyệt)
        │  https://ocr.<ten-mien-cua-ban>
        ▼
Cloudflare (tên miền + tunnel, miễn phí)
        │  kết nối do máy bạn chủ động mở ra, không cần mở port
        ▼
Máy Windows của bạn
   ├─ cloudflared (Windows service, tự chạy khi bật máy) ──► http://localhost:8000
   └─ Docker Desktop (tự chạy khi đăng nhập Windows)
         ├─ frontend (nginx)    cổng 8000 trên máy: giao diện, chuyển /api sang backend
         ├─ backend (FastAPI)   OCR, chatbot ── ảnh, log: volume ocr-dashboard-data
         └─ db (PostgreSQL)     database      ── volume ocr-dashboard-db
                 backend gọi API OCR: Cloudflare / NVIDIA / OpenRouter, chatbot: Groq
```

Bạn cần nhớ:

- **Máy phải bật** (và không ở chế độ Sleep) thì người khác mới dùng được.
- Chỉ có **một link duy nhất**. Không cần Vercel.
- Người dùng phải **đăng nhập** bằng tài khoản `AUTH_USER` / `AUTH_PASSWORD` trong `.env` mới xem được dữ liệu.

### Những gì cần chuẩn bị

| Thứ cần có | Ghi chú |
|---|---|
| Máy Windows 10/11 | Máy sẽ chạy app, nên bật thường xuyên |
| Bộ cài app (3 file) | `ocr-dashboard.tar`, `docker-compose.yml`, `.env.example`. Người bàn giao gửi, hoặc tự tạo theo mục 1 của [HUONG_DAN_DOCKER.md](HUONG_DAN_DOCKER.md) |
| Tài khoản Gmail | Dùng để đăng ký Cloudflare và DigitalPlat |
| Tài khoản GitHub | Dùng để xác minh tài khoản DigitalPlat |
| Ít nhất 1 API key OCR | Cloudflare, NVIDIA NIM hoặc OpenRouter (mục 2.2) |
| Khoảng 1 tiếng | Phần lớn thời gian là chờ tên miền kích hoạt |

---

## 1. Cài phần mềm cần thiết

Mở **PowerShell** và chạy:

```powershell
winget install --id Docker.DockerDesktop
winget install --id Cloudflare.cloudflared
```

Cài xong thì **khởi động lại máy**, mở **Docker Desktop** một lần và làm theo hướng dẫn trên màn hình (chấp nhận điều khoản, có thể phải cài thêm WSL). Sau đó:

- Trong Docker Desktop, vào **Settings → General**, bật **Start Docker Desktop when you sign in to your computer**. App sẽ tự chạy lại mỗi khi bật máy.
- Mở lại PowerShell và kiểm tra:

  ```powershell
  docker --version
  docker compose version
  cloudflared --version
  ```

---

## 2. Cài app và chạy thử trên máy

### 2.1. Nạp app

Tạo thư mục `D:\OCRDashboard`, chép 3 file của bộ cài vào đó, rồi trong PowerShell:

```powershell
cd D:\OCRDashboard
docker load -i ocr-dashboard.tar
Copy-Item .env.example .env
notepad .env
```

### 2.2. Điền file `.env`

| Biến | Điền gì |
|---|---|
| `AUTH_USER`, `AUTH_PASSWORD` | **Bắt buộc.** Tài khoản đăng nhập web, do bạn tự đặt. Mật khẩu nên dài, khó đoán |
| `SESSION_SECRET` | Một chuỗi ngẫu nhiên dài (gõ bừa khoảng 40 ký tự chữ và số) |
| `POSTGRES_PASSWORD`, `DB_PASSWORD`, `DB_RO_PASSWORD` | **Bắt buộc.** 3 mật khẩu database, mỗi cái khác nhau, **chỉ chữ và số**, từ 16 ký tự. Không cần nhớ, chỉ để trong file này |
| `CLOUDFLARE_API_KEY` + `CLOUDFLARE_ACCOUNT_ID` | https://dash.cloudflare.com → AI → Workers AI (token quyền Workers AI) |
| `NVIDIA_API_KEY` | https://build.nvidia.com (chỉ dùng model có tag _Free Endpoint_) |
| `OPEN_ROUTER_API_KEY` | https://openrouter.ai/keys |
| `GROQ_API_KEY` | https://console.groq.com/keys (cho chatbot) |
| `TUNNEL_TOKEN` | **Để trống.** Tunnel chạy dạng Windows service (mục 5), không cần biến này |

Cần **ít nhất một** API key OCR. Lưu file lại.

> ⚠️ **Không bao giờ** commit hay gửi file `.env` cho ai. Nếu lỡ để lộ, hãy vào trang của nhà cung cấp, xóa key cũ và tạo key mới.

### 2.3. Chạy

```powershell
docker compose up -d
docker compose ps
```

Đợi đến khi cả 3 dòng `db`, `backend`, `frontend` hiện **(healthy)**, thường chỉ vài chục giây. Mở trình duyệt vào **http://localhost:8000**, đăng nhập bằng `AUTH_USER` / `AUTH_PASSWORD`, rồi thử upload 1 ảnh ở trang "Truyền Pháp Ảnh" để chắc chắn API key hoạt động.

App **tự chạy lại** sau khi tắt máy hay khởi động lại, miễn là Docker Desktop được bật cùng Windows (mục 1).

---

## 3. Lấy tên miền miễn phí (DigitalPlat)

Tunnel cố định của Cloudflare cần một tên miền **của riêng bạn**. DigitalPlat cấp miễn phí tên miền dạng `ten-ban.dpdns.org`.

### 3.1. Tạo tài khoản

1. Vào **https://dash.domain.digitalplat.org/** và đăng ký bằng Gmail. Mở email và bấm link xác nhận.
2. Đăng nhập. Làm theo yêu cầu **xác minh tài khoản bằng GitHub**.

### 3.2. Đăng ký tên miền

1. Ở menu trái, vào khu **DigitalPlat Domains** (khu miễn phí).
   > ⚠️ Đừng dùng mục **Domains → Register Domain**. Đó là chỗ **mua** tên miền có trả phí, sẽ hiện giá tiền.
2. **Chỉ gõ phần tên**, ví dụ `cnkt3dash`, rồi chọn đuôi **`.dpdns.org`**.
   - Nên chọn tên ngắn, không dấu gạch ngang, không chứa tên thương hiệu. Tên dài hoặc có nhiều dấu `-` thường bị từ chối.
3. Khi hiện ô **Register domain**:
   - **Delegation mode**: chọn **Configure later**.
     > Đừng chọn _DigitalPlat DNS_, vì như vậy DNS không nằm ở Cloudflare và bạn không làm tunnel được.
   - **Domain slot**: giữ **Free domain slot**.
   - Bấm **Register**.

> 📅 **Tên miền free có hạn sử dụng** (hiện là 120 ngày). Hãy xem ngày hết hạn trong **Domain List** và **đặt lịch nhắc trước 2 tuần** để gia hạn. Nếu không gia hạn free được thì xem mục 8.

---

## 4. Đưa tên miền vào Cloudflare

### 4.1. Tạo tài khoản Cloudflare

Vào **https://dash.cloudflare.com/sign-up** và đăng ký bằng Gmail (gói Free).

### 4.2. Thêm tên miền

1. Trên dashboard, vào **Account home** rồi bấm **Add a domain** (có nơi ghi _Onboard a domain_).
   > ⚠️ Đừng dùng **Domains → Registrations**. Đó là chỗ mua tên miền.
2. Nhập đúng tên miền vừa đăng ký, ví dụ `cnkt3dash.dpdns.org`.
3. Chọn gói **Free**.
4. Đến bước bản ghi DNS, bấm **Continue**. Nếu hiện cảnh báo _"Add records later"_ thì bấm **Confirm**. Không sao cả, tunnel sẽ tự tạo bản ghi sau.
5. Cloudflare hiện **2 nameserver** dạng `xxxx.ns.cloudflare.com`. **Copy cả hai.**

### 4.3. Trỏ tên miền về Cloudflare

1. Quay lại DigitalPlat, vào **Domain List**, chọn tên miền của bạn.
2. Chuyển sang **External nameservers** và dán 2 nameserver của Cloudflare, rồi lưu.
3. Về Cloudflare, mở tên miền và bấm **Check nameservers now**.
4. Chờ đến khi trạng thái chuyển thành **Active**. Thường mất 5 đến 30 phút, có khi vài giờ. Cloudflare sẽ gửi email khi xong.

Kiểm tra bằng PowerShell (phải thấy `*.ns.cloudflare.com`):

```powershell
nslookup -type=ns cnkt3dash.dpdns.org
```

---

## 5. Tạo tunnel cố định (Cloudflare Tunnel)

Cách dưới đây làm hoàn toàn trên giao diện web. Sau khi làm xong, bạn xem và quản lý tunnel ngay trên dashboard Cloudflare.

1. Trên dashboard Cloudflare, vào **Networking → Tunnels**. Giao diện có thể thay đổi; nếu không thấy, tìm "Tunnels" trong ô **Quick search**, hoặc vào **Zero Trust → Networks → Tunnels**.
2. Bấm **Create a tunnel** và chọn loại **Cloudflared**.
3. Đặt tên, ví dụ `ocr-dashboard`, rồi bấm **Save**.
4. Chọn hệ điều hành **Windows**. Cloudflare sẽ hiện một lệnh dạng:

   ```
   cloudflared.exe service install eyJhIjoi...(token rất dài)...
   ```

   - Mở **PowerShell bằng quyền Administrator**: chuột phải vào biểu tượng PowerShell, chọn _Run as administrator_.
   - Dán lệnh đó vào và chạy.
   - Lệnh này cài tunnel thành **service tự chạy mỗi khi bật máy**.

   > ⚠️ Token là "chìa khóa" của tunnel. Đừng gửi cho ai và đừng commit lên GitHub. **Không** điền token này vào `.env` (biến `TUNNEL_TOKEN` để trống).
   >
   > Tunnel **đã có sẵn** và chỉ cần cài lên máy mới: mở tunnel, bấm **+ Add a replica**, chọn **Windows** để lấy lại lệnh trên. Đừng bấm **Rotate token** (làm hỏng kết nối của máy đang chạy).

5. Quay lại trang tunnel `ocr-dashboard`. Khi **Status** báo **Healthy** (khung _Replicas_ hiện tên máy của bạn) là tunnel đã kết nối.
6. Thêm route để tên miền trỏ vào app. Ở khung **Routes**, bấm **+ Add route** và chọn **Published application**. Đừng chọn Private network hay Private hostname. Điền:
   | Ô | Giá trị |
   |---|---|
   | Subdomain | `ocr` |
   | Domain | `cnkt3dash.dpdns.org` (chọn trong danh sách) |
   | Path | để trống |
   | Service URL | `http://localhost:8000` |

   > ⚠️ Service URL viết **`http`** (không có `s`) và cổng **`8000`**, không phải `8080` như chữ mờ ví dụ trong ô. Phần _Additional application settings_ không cần chỉnh.
   >
   > Nếu ô **Domain** không có tên miền của bạn thì tên miền chưa **Active** (mục 4.3). Chờ thêm rồi làm lại.

7. Bấm **Add route**. Ô _Full hostname_ phải hiện `ocr.cnkt3dash.dpdns.org`.

Từ giờ địa chỉ của dashboard là **`https://ocr.cnkt3dash.dpdns.org`** và địa chỉ này **không đổi**.

> **Mỗi tunnel chỉ nên có 1 máy chạy app.** Nếu chuyển app sang máy khác, gỡ tunnel ở máy cũ (mục 7.4, bước 2). Nếu 2 máy cùng là replica, Cloudflare sẽ chia lượt truy cập sang máy cũ, và các lượt đó báo lỗi 502 khi máy cũ không còn chạy app.

---

## 6. Kiểm tra tự chạy khi bật máy

| Thành phần | Tự chạy nhờ |
|---|---|
| Tunnel (cloudflared) | Windows service (mục 5, bước 4) |
| App (3 container) | Docker Desktop bật cùng Windows (mục 1) + `restart: unless-stopped` trong `docker-compose.yml` |

Thử khởi động lại máy, đăng nhập Windows, đợi khoảng 1 phút rồi mở **https://ocr.cnkt3dash.dpdns.org**.

**Tắt chế độ Sleep:** vào **Settings → System → Power**, đặt _Sleep_ thành **Never** khi cắm sạc.

---

## 7. Sử dụng hằng ngày, bật và tắt

Mọi lệnh `docker compose` chạy trong thư mục `D:\OCRDashboard`.

### 7.1. Hằng ngày

| Việc | Cách làm |
|---|---|
| **Link gửi người dùng** | `https://ocr.cnkt3dash.dpdns.org` |
| **Bật web** | Bật máy và đăng nhập Windows, đợi khoảng 1 phút là dùng được |
| **Kiểm tra** | `docker compose ps`: cả 3 dòng **(healthy)** là app ổn. Cloudflare → **Networking → Tunnels**: **Healthy** là tunnel ổn, **Down** là máy tắt hoặc mất mạng. Tunnel Healthy mà web báo **502** thì app chưa chạy |
| **Xem log** | `docker compose logs -f backend`, hoặc lọc: `docker compose exec backend python scripts/logs.py --level WARNING` (hỏi tài khoản web) |
| **Sửa `.env`** | `notepad .env`, lưu, rồi `docker compose up -d` |
| **Cập nhật phiên bản** | Nhận file `ocr-dashboard.tar` mới, rồi `docker load -i ocr-dashboard.tar` và `docker compose up -d` |
| **Sao lưu dữ liệu** | Xem mục 6 của [HUONG_DAN_DOCKER.md](HUONG_DAN_DOCKER.md) |

Dữ liệu cũ hơn 35 ngày được app **tự xóa** lúc 2h sáng mỗi ngày (chỉnh bằng `RETENTION_DAYS` trong `.env`).

### 7.2. Tắt tạm (hôm nay không dùng)

- **Tắt:** `docker compose stop`. Web sẽ báo lỗi 502, dữ liệu vẫn còn nguyên.
- **Bật lại:** `docker compose start`.

### 7.3. Không cho tự chạy khi bật máy nữa

**App:** trong Docker Desktop, **Settings → General**, tắt **Start Docker Desktop when you sign in**. Hoặc chạy `docker compose stop`: container đã dừng bằng tay thì không tự bật lại.

**Tunnel:** mở PowerShell bằng quyền **Administrator**:

```powershell
Stop-Service cloudflared
Set-Service cloudflared -StartupType Manual
```

**Bật lại khi cần:**

```powershell
# PowerShell (Administrator)
Start-Service cloudflared                          # bật tunnel ngay
Set-Service cloudflared -StartupType Automatic     # (tùy chọn) cho tự chạy khi bật máy như cũ
```

Sau đó chạy `docker compose start` trong `D:\OCRDashboard`.

### 7.4. Gỡ bỏ hẳn (không dùng nữa)

1. Gỡ app: trong `D:\OCRDashboard` chạy `docker compose down` (giữ dữ liệu) hoặc `docker compose down -v` (**xóa luôn dữ liệu**).
2. Gỡ service tunnel (PowerShell bằng quyền Administrator):
   ```powershell
   cloudflared service uninstall
   ```
3. Trên Cloudflare, vào **Networking → Tunnels**, chọn `ocr-dashboard`, xóa **route** `ocr.cnkt3dash.dpdns.org` trước rồi xóa **tunnel**.
4. Nếu không giữ tên miền nữa: xóa `cnkt3dash.dpdns.org` khỏi Cloudflare và DigitalPlat. Còn không thì cứ để đó, không tốn tiền.

> `docker compose down` (không có `-v`) và gỡ tunnel **không làm mất** dữ liệu và `.env`. Muốn xóa hẳn: `docker compose down -v`, rồi xóa thư mục `D:\OCRDashboard`.

---

## 8. Khi tên miền free hết hạn

1. Vào DigitalPlat, mở **Domain List**. Nếu có nút **Renew** thì gia hạn là xong.
2. Nếu không gia hạn free được:
   - Đăng ký tên miền free mới (làm lại **mục 3**).
   - Thêm vào Cloudflare và đổi nameserver (làm lại **mục 4**).
   - Vào **Networking → Tunnels**, chọn `ocr-dashboard`, xóa route cũ và **Add route** mới với tên miền mới (giống mục 5, bước 6).
   - Gửi link mới cho người dùng.
   - **Không cần** cài lại tunnel hay app, và **dữ liệu không mất**.

---

## 9. Xử lý lỗi thường gặp

| Hiện tượng | Nguyên nhân / cách xử lý |
|---|---|
| `docker compose up` báo `Điền POSTGRES_PASSWORD trong .env` (hoặc `DB_PASSWORD`, `DB_RO_PASSWORD`) | Chưa điền 3 mật khẩu database (mục 2.2) |
| `docker compose up` báo `no configuration file provided` | Đang đứng sai thư mục. `cd D:\OCRDashboard` |
| `docker` báo không kết nối được (`error during connect`, `pipe ... docker_engine`) | Docker Desktop chưa chạy. Mở Docker Desktop, đợi biểu tượng cá voi đứng yên |
| `docker compose ps` có dòng **unhealthy** hoặc **Restarting** | Xem lỗi: `docker compose logs --tail 50 backend` (hoặc `db`) |
| `docker compose up` báo cổng 8000 đã bị dùng (`port is already allocated`) | Có chương trình khác dùng cổng 8000 (ví dụ bản cũ `start_backend.bat` còn chạy). Tắt nó, hoặc đặt `APP_PORT=8001` trong `.env` **và** sửa Service URL của tunnel thành `http://localhost:8001` |
| Đăng nhập luôn báo sai | `AUTH_USER` / `AUTH_PASSWORD` trong `.env` còn trống hoặc gõ sai. Sửa rồi `docker compose up -d` |
| Lỗi **502 Bad Gateway** | App chưa chạy. `docker compose ps`, nếu dừng thì `docker compose up -d` |
| Lỗi **1033** hoặc _"Cloudflare Tunnel error"_ | Tunnel không kết nối: máy tắt hoặc mất mạng, hoặc service bị dừng. PowerShell (Admin): `Start-Service cloudflared` |
| Không mở được link, báo không tìm thấy tên miền | Tên miền chưa **Active** trên Cloudflare (mục 4.3), hoặc đã hết hạn (mục 8) |
| `localhost:8000` chạy nhưng link ngoài không chạy | Kiểm tra route (mục 5, bước 6): Service URL phải là `http://localhost:8000` |
| Lúc được lúc lỗi 502 | Tunnel có 2 replica (2 máy), máy kia không chạy app. Gỡ tunnel ở máy đó (mục 7.4, bước 2) |
| Upload xong nhưng OCR lỗi | API key sai hoặc hết quota. Kiểm tra `.env`, rồi `docker compose up -d` |
| Mạng công ty chặn | Một số mạng chặn tên miền free. Thử bằng 4G, hoặc nhờ IT |

---

## 10. Bảo mật (nên đọc)

- Người dùng phải **đăng nhập** mới xem được dữ liệu hay upload ảnh. Mọi người dùng **chung một tài khoản**, nên chỉ đưa tài khoản cho người cần dùng. Đổi mật khẩu: sửa `AUTH_PASSWORD` trong `.env` rồi `docker compose up -d`. Muốn mọi máy đang đăng nhập phải đăng nhập lại thì đổi luôn `SESSION_SECRET`.
- Sai mật khẩu 8 lần trong 5 phút thì địa chỉ IP đó bị khóa đăng nhập 5 phút.
- Muốn chặn người lạ ngay từ trước trang đăng nhập, bật **Cloudflare Access** (miễn phí đến 50 người):
  Zero Trust → **Access → Applications → Add an application → Self-hosted** → domain `ocr.cnkt3dash.dpdns.org` → Policy **Allow**, Include **Emails** và liệt kê email của đồng nghiệp. Người dùng sẽ phải nhập mã gửi về email mới vào được.
- Đây là dữ liệu vận hành nội bộ, nên **hỏi ý kiến IT công ty** trước khi mở ra internet.

---

## Phụ lục A: Chạy tạm không cần tên miền (Quick Tunnel)

Dùng khi chỉ cần demo nhanh. Link sẽ **đổi mỗi lần chạy lại** và không quản lý được trên dashboard.

```powershell
# app đang chạy bằng docker compose (mục 2.3), rồi:
cloudflared tunnel --url http://localhost:8000
```

Copy link `https://....trycloudflare.com` in ra trong log và gửi cho người dùng. Bấm `Ctrl + C` để tắt.

---

## Phụ lục B: Chạy từ source code (cho người sửa code)

Người sửa code chạy trực tiếp bằng Python (dùng SQLite trong `backend\data\`, không cần Docker):

```powershell
git clone https://github.com/chien24/Dashboard.git dashboard
cd dashboard
python -m venv .venv
.venv\Scripts\activate
pip install -r backend/requirements.txt
copy backend\.env.example backend\.env      # điền AUTH_USER, AUTH_PASSWORD, API key
start_backend.bat                           # hoặc: cd backend; uvicorn app.main:app --reload
```

Sửa code xong, build lại bộ cài Docker theo mục 1 của [HUONG_DAN_DOCKER.md](HUONG_DAN_DOCKER.md). Dữ liệu của bản chạy source chuyển sang Docker theo mục 7 của file đó.
