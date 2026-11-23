# Hướng dẫn đưa OCR Dashboard CNKT3 lên internet (miễn phí, dữ liệu để ở máy local)

Tài liệu này hướng dẫn từ đầu: tạo tài khoản, lấy tên miền miễn phí, cài đặt, rồi mở dashboard cho người khác truy cập qua internet. **Dữ liệu và API key luôn nằm trên máy của bạn.** Không cần mở port router, không cần Docker, không tốn tiền.

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
   ├─ cloudflared (service, tự chạy khi bật máy)
   └─ Backend FastAPI :8000 (phục vụ luôn giao diện)
         ├─ backend/data/ocr.db       (SQLite)
         ├─ backend/data/uploads/     (ảnh upload)
         └─ gọi API OCR: Cloudflare / NVIDIA / OpenRouter
```

Bạn cần nhớ:

- **Máy phải bật** (và không ở chế độ Sleep) thì người khác mới dùng được.
- Backend đã phục vụ cả giao diện lẫn API, nên **một link duy nhất** là đủ. Không cần Vercel (xem Phụ lục B nếu vẫn muốn dùng).

### Những gì cần chuẩn bị

| Thứ cần có            | Ghi chú                                            |
| --------------------- | -------------------------------------------------- |
| Máy Windows 10/11     | Máy sẽ chạy backend, nên bật thường xuyên          |
| Tài khoản Gmail       | Dùng để đăng ký các dịch vụ                        |
| Tài khoản GitHub      | Dùng để lấy code và xác minh tài khoản DigitalPlat |
| Ít nhất 1 API key OCR | Cloudflare, NVIDIA NIM hoặc OpenRouter (mục 2.3)   |
| Khoảng 1 tiếng        | Phần lớn thời gian là chờ tên miền kích hoạt       |

---

## 1. Cài phần mềm cần thiết

Mở **PowerShell** và chạy từng dòng:

```powershell
winget install --id Python.Python.3.12
winget install --id Git.Git
winget install --id Cloudflare.cloudflared
```

Cài xong thì **đóng PowerShell và mở lại**, rồi kiểm tra:

```powershell
python --version        # phải là 3.11 trở lên
git --version
cloudflared --version
```

---

## 2. Lấy code và chạy thử trên máy

### 2.1. Tải code

```powershell
cd $HOME\Documents
git clone https://github.com/chien24/Dashboard.git dashboard
cd dashboard
```

### 2.2. Cài thư viện Python

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r backend/requirements.txt
copy backend\.env.example backend\.env
```

> Dùng **conda** thay vì `.venv` cũng được: bỏ 2 dòng đầu, cài thư viện bằng `py -m pip install -r backend/requirements.txt`. `start_backend.bat` sẽ tự dùng `py`.

### 2.3. Điền API key

Mở file `backend\.env` bằng Notepad và điền **ít nhất một** key:

| Biến                  | Lấy ở đâu                                                        |
| --------------------- | ---------------------------------------------------------------- |
| `CLOUDFLARE_API_KEY` + `CLOUDFLARE_ACCOUNT_ID` | https://dash.cloudflare.com → AI → Workers AI (token quyền Workers AI) |
| `NVIDIA_API_KEY`      | https://build.nvidia.com (chỉ dùng model có tag _Free Endpoint_) |
| `OPEN_ROUTER_API_KEY` | https://openrouter.ai/keys                                       |
| `GROQ_API_KEY`        | https://console.groq.com/keys                                    |

> ⚠️ **Không bao giờ** commit hay gửi file `.env` cho ai. Nếu lỡ để lộ, hãy vào trang của nhà cung cấp, xóa key cũ và tạo key mới.

### 2.4. Chạy thử

```powershell
cd backend
..\.venv\Scripts\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

Mở trình duyệt vào **http://localhost:8000**. Thấy trang Dashboard là được. Thử upload 1 ảnh ở trang "Upload ảnh" để chắc chắn API key hoạt động.

Bấm `Ctrl + C` để tắt.

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

   > ⚠️ Token là "chìa khóa" của tunnel. Đừng gửi cho ai và đừng commit lên GitHub.

5. Quay lại trang tunnel `ocr-dashboard`. Khi **Status** báo **Healthy** (khung _Replicas_ hiện tên máy của bạn) là tunnel đã kết nối.
6. Thêm route để tên miền trỏ vào backend. Ở khung **Routes**, bấm **+ Add route** và chọn **Published application**. Đừng chọn Private network hay Private hostname. Điền:
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

---

## 6. Cho backend tự chạy khi bật máy

Tunnel đã tự chạy khi bật máy, vì lệnh `service install` ở mục 5 biến nó thành service. Chỉ còn **backend** là cần cài để tự chạy.

### 6.1. File khởi động `start_backend.bat`

File **`start_backend.bat`** đã có sẵn trong **thư mục gốc của project** (cùng chỗ với `backend\` và `frontend\`) sau khi `git clone`. Không cần tạo lại.

File tự chọn Python theo thứ tự:
1. `.venv` của project (mục 2.2).
2. `py`, trình khởi chạy Python của Windows. Lệnh này dùng được ngay cả khi bạn cài thư viện vào **conda** mà không bật conda.
3. `python`.

Bấm đúp vào file để chạy thử:

- **Thành công:** cửa sổ đen hiện `Uvicorn running on http://127.0.0.1:8000` và **đứng yên**. Mở **https://ocr.cnkt3dash.dpdns.org**, thấy dashboard là được 🎉
- **Lỗi:** cửa sổ dừng lại và hiện nội dung lỗi (không tự tắt nữa). Xem mục 9.

### 6.2. Tự chạy khi đăng nhập Windows

1. Nhấn `Win + R`, gõ `shell:startup` rồi Enter.
2. Chuột phải vào `start_backend.bat`, chọn **Create shortcut**, rồi kéo shortcut vừa tạo vào thư mục Startup vừa mở.

### 6.3. Tắt chế độ Sleep

Vào **Settings → System → Power**, đặt _Sleep_ thành **Never** khi cắm sạc.

---

## 7. Sử dụng hằng ngày, bật và tắt

### 7.1. Hằng ngày

| Thành phần           | Bật máy có tự chạy không?             |
| -------------------- | ------------------------------------- |
| Tunnel (cloudflared) | ✅ Có, chạy dưới dạng Windows service |
| Backend              | ✅ Có, nếu đã làm mục 6.2             |

| Việc                    | Cách làm                                                                                                                                                         |
| ----------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Link gửi người dùng** | `https://ocr.cnkt3dash.dpdns.org`                                                                                                                                |
| **Bật web**             | Bật máy và đăng nhập Windows. Cửa sổ đen của backend tự hiện, đợi vài giây là dùng được.                                                                         |
| **Kiểm tra**            | Cloudflare → **Networking → Tunnels**: **Healthy** là tunnel ổn, **Down** là máy tắt hoặc mất mạng. Nếu tunnel Healthy mà web báo **502** thì backend chưa chạy. |
| **Cập nhật code**       | `git pull` trong thư mục project, rồi đóng và mở lại `start_backend.bat`                                                                                         |
| **Sao lưu dữ liệu**     | Copy thư mục `backend\data\` ra chỗ khác                                                                                                                         |

Dữ liệu cũ hơn 35 ngày được backend **tự xóa** lúc 2h sáng mỗi ngày (chỉnh bằng `RETENTION_DAYS` trong `.env`).

### 7.2. Tắt tạm (hôm nay không dùng)

- **Tắt:** đóng **cửa sổ đen** của backend. Web sẽ báo lỗi 502, dữ liệu vẫn còn nguyên.
- **Bật lại** (không cần khởi động lại máy): bấm đúp `start_backend.bat`.

### 7.3. Không cho tự chạy khi bật máy nữa

**Backend:** nhấn `Win + R`, gõ `shell:startup`, rồi xóa shortcut `start_backend.bat` trong đó.

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

Sau đó bấm đúp `start_backend.bat`. Muốn backend tự chạy lại thì làm lại mục 6.2.

### 7.4. Gỡ bỏ hẳn (không dùng nữa)

1. Làm như mục 7.3.
2. Gỡ service tunnel (PowerShell bằng quyền Administrator):
   ```powershell
   cloudflared service uninstall
   ```
3. Trên Cloudflare, vào **Networking → Tunnels**, chọn `ocr-dashboard`, xóa **route** `ocr.cnkt3dash.dpdns.org` trước rồi xóa **tunnel**.
4. Nếu không giữ tên miền nữa: xóa `cnkt3dash.dpdns.org` khỏi Cloudflare và DigitalPlat. Còn không thì cứ để đó, không tốn tiền.
5. Nếu có dùng Vercel (Phụ lục B): vào project, mở **Settings**, kéo xuống cuối trang để xóa project.

> Dữ liệu (`backend\data\`) và API key (`backend\.env`) vẫn nằm trên máy. Gỡ tunnel hay Vercel **không làm mất** chúng. Muốn xóa hẳn thì tự xóa thư mục và file đó.

---

## 8. Khi tên miền free hết hạn

1. Vào DigitalPlat, mở **Domain List**. Nếu có nút **Renew** thì gia hạn là xong.
2. Nếu không gia hạn free được:
   - Đăng ký tên miền free mới (làm lại **mục 3**).
   - Thêm vào Cloudflare và đổi nameserver (làm lại **mục 4**).
   - Vào **Networking → Tunnels**, chọn `ocr-dashboard`, xóa route cũ và **Add route** mới với tên miền mới (giống mục 5, bước 6).
   - Gửi link mới cho người dùng.
   - **Không cần** cài lại tunnel hay backend, và **dữ liệu không mất**.

---

## 9. Xử lý lỗi thường gặp

| Hiện tượng                                                                 | Nguyên nhân / cách xử lý                                                                                            |
| -------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------- |
| Bấm `start_backend.bat` thì cửa sổ hiện lên rồi **tắt ngay**               | Đang dùng bản `.bat` cũ: bản cũ gọi cứng `.venv\Scripts\python.exe`, máy không có `.venv` thì cmd báo _"The system cannot find the path specified"_ rồi đóng luôn vì không có `pause`. Dùng bản trong repo (mục 6.1): tự chọn `.venv` → `py` → `python` và giữ cửa sổ lại để đọc lỗi. |
| Cửa sổ báo `[LOI] File .bat phai nam trong thu muc goc...`                 | Chuyển file `.bat` vào thư mục chứa `backend\` và `frontend\`.                                                      |
| Cửa sổ báo `No module named uvicorn`                                       | Python được chọn (dòng `Dang dung Python:`) chưa cài thư viện. Làm lại mục 2.2, hoặc cài vào đúng Python đó: `py -m pip install -r backend/requirements.txt`. |
| Cửa sổ báo `'python' is not recognized`                                    | Chưa cài Python (không có cả `.venv` lẫn `py`). Làm lại mục 1 và 2.2.                                               |
| Cửa sổ báo lỗi cổng 8000 đang bị dùng (`address already in use` / `10048`) | Backend đã chạy ở cửa sổ khác. Đóng cửa sổ đó, hoặc dùng luôn nó.                                                   |
| Lỗi **502 Bad Gateway**                                                    | Backend chưa chạy. Mở `start_backend.bat`.                                                                          |
| Lỗi **1033** hoặc _"Cloudflare Tunnel error"_                              | Tunnel không kết nối: máy tắt hoặc mất mạng, hoặc service bị dừng. PowerShell (Admin): `Start-Service cloudflared`. |
| Không mở được link, báo không tìm thấy tên miền                            | Tên miền chưa **Active** trên Cloudflare (mục 4.3), hoặc đã hết hạn (mục 8).                                        |
| `localhost:8000` chạy nhưng link ngoài không chạy                          | Kiểm tra Public hostname (mục 5, bước 6): Service phải là `HTTP` và `localhost:8000`.                               |
| Upload xong nhưng OCR lỗi                                                  | API key sai hoặc hết quota. Kiểm tra `backend\.env`.                                                                |
| Mạng công ty chặn                                                          | Một số mạng chặn tên miền free. Thử bằng 4G, hoặc nhờ IT.                                                           |

---

## 10. Bảo mật (nên đọc)

- Hiện tại **ai có link cũng dùng được app**, kể cả upload ảnh, tức là tiêu tốn quota API OCR của bạn. Chỉ gửi link cho người cần dùng.
- Muốn chặn người lạ, bật **Cloudflare Access** (miễn phí đến 50 người):
  Zero Trust → **Access → Applications → Add an application → Self-hosted** → domain `ocr.cnkt3dash.dpdns.org` → Policy **Allow**, Include **Emails** và liệt kê email của đồng nghiệp. Người dùng sẽ phải nhập mã gửi về email mới vào được.
- Đây là dữ liệu vận hành nội bộ, nên **hỏi ý kiến IT công ty** trước khi mở ra internet.

---

## Phụ lục A: Chạy tạm không cần tên miền (Quick Tunnel)

Dùng khi chỉ cần demo nhanh. Link sẽ **đổi mỗi lần chạy lại** và không quản lý được trên dashboard.

```powershell
# Cửa sổ 1
cd $HOME\Documents\dashboard\backend
..\.venv\Scripts\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8000

# Cửa sổ 2
cloudflared tunnel --url http://localhost:8000
```

Copy link `https://....trycloudflare.com` in ra trong log và gửi cho người dùng. Bấm `Ctrl + C` ở cả hai cửa sổ để tắt.

---

## Phụ lục B: Dùng Vercel cho giao diện (không bắt buộc)

Vì backend đã phục vụ giao diện, Vercel **không cần thiết**. Lưu ý thêm: gói Hobby (miễn phí) của Vercel chỉ cho phép dùng **cá nhân, phi thương mại**.

Nếu vẫn muốn dùng:

1. Đăng nhập **https://vercel.com** bằng GitHub, chọn **Add New → Project** và import repo.
2. Ở màn hình Configure Project:
   - **Root Directory**: `frontend` (bắt buộc, nếu không Vercel sẽ cố deploy cả backend).
   - **Framework Preset**: `Other`.
   - Không điền Build settings, **không** thêm Environment Variables (không đưa API key lên Vercel).
3. Sửa file `frontend/vercel.json` cho rewrites trỏ cố định về tên miền của bạn. File trong repo có thể đang trỏ về một link `*.trycloudflare.com` cũ của Quick Tunnel; link đó chết khi tunnel tắt.
   ```json
   {
     "redirects": [
       { "source": "/", "destination": "/html/index.html", "permanent": false }
     ],
     "rewrites": [
       {
         "source": "/api/:path*",
         "destination": "https://ocr.cnkt3dash.dpdns.org/api/:path*"
       },
       {
         "source": "/uploads/:path*",
         "destination": "https://ocr.cnkt3dash.dpdns.org/uploads/:path*"
       }
     ]
   }
   ```
4. Commit và push lên `main`; Vercel tự deploy lại sau mỗi lần push.

Khi máy tắt, trang Vercel vẫn mở được nhưng **không có dữ liệu**.
