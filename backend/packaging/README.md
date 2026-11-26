# Đóng gói OCR Dashboard thành bộ cài Windows

Máy người dùng **không cần cài Python**. Python và toàn bộ thư viện nằm sẵn trong bộ cài.

## Build (trên máy có Python, chỉ làm 1 lần mỗi khi có code mới)

1. (Khuyến nghị) Cài Inno Setup 6 để ra file `Setup.exe`: `winget install JRSoftware.InnoSetup`
2. Bấm đúp `backend\packaging\build.bat`. Lần đầu mất vài phút vì phải tải thư viện.
3. Kết quả nằm trong `backend\packaging\dist\`:
   - `OCRDashboard-Setup.exe`: bộ cài, gửi file này cho người dùng.
   - Không có Inno Setup thì thay bằng `OCRDashboard-portable.zip`: giải nén rồi chạy `OCRDashboard.exe`.

`build.bat` tạo môi trường Python riêng trong `packaging\build\venv`, nên không đụng tới Python hay `.venv` đang dùng để code. Hai thư mục `build\` và `dist\` không được commit.

**Bộ cài KHÔNG chứa `.env`, dữ liệu, ảnh hay log.** `build.bat` tự dừng nếu thấy những thứ đó trong gói. Nhờ vậy gửi `Setup.exe` cho ai cũng không lộ key.

## Cài và chạy (máy người dùng)

1. Chạy `OCRDashboard-Setup.exe`. Không cần quyền Administrator.
   - Windows có thể báo "Windows protected your PC" vì file chưa có chữ ký số: bấm **More info → Run anyway**.
2. Lần chạy đầu, app tạo file cấu hình rồi mở Notepad. Điền:
   - `AUTH_USER`, `AUTH_PASSWORD` (bắt buộc), `SESSION_SECRET`;
   - API key OCR (ít nhất 1 provider) và `GROQ_API_KEY` cho chatbot.

   Lưu lại, rồi mở **OCR Dashboard** lần nữa.
3. Trình duyệt tự mở `http://localhost:8000`. **Đóng cửa sổ console = tắt web.**

Shortcut trong Start Menu → OCR Dashboard:

| Shortcut | Việc |
|---|---|
| OCR Dashboard | Chạy web |
| Sửa cấu hình (.env) | Mở `.env` bằng Notepad. Sửa xong tắt app rồi mở lại |
| Xem log (trực tiếp) | `OCRDashboard.exe logs -f` (hỏi tài khoản web) |

Lệnh dòng lệnh (gõ trong thư mục cài, giống `scripts/*.py` khi chạy từ source):

```
OCRDashboard.exe logs -n 100 --level warning
OCRDashboard.exe db info
OCRDashboard.exe env list
OCRDashboard.exe help
```

## Dữ liệu nằm ở đâu

| | Vị trí |
|---|---|
| Chương trình | `%LOCALAPPDATA%\Programs\OCRDashboard\` (bộ cài ghi đè khi cập nhật) |
| `.env` và `data\` (`ocr.db`, `uploads\`, `logs\`) | `%LOCALAPPDATA%\OCRDashboard\` (tạo lúc chạy lần đầu) |

- Gỡ cài đặt hoặc cài bản mới **không** xóa `.env` và dữ liệu.
- Muốn để dữ liệu ở chỗ khác (ví dụ ổ D): đặt biến môi trường Windows `OCR_DASHBOARD_HOME=D:\OCRDashboard`.
- Sao lưu: tắt app, rồi chép nguyên thư mục `%LOCALAPPDATA%\OCRDashboard\`.
- Chuyển dữ liệu từ bản chạy source: chép `backend\.env` và `backend\data\` vào `%LOCALAPPDATA%\OCRDashboard\`.

## Cập nhật phiên bản

Sửa code → chạy lại `build.bat` → gửi `OCRDashboard-Setup.exe` mới. Người dùng tắt app, chạy bộ cài mới (ghi đè lên bản cũ), mở lại.

## Lưu ý khi sửa code

- File tài nguyên mới trong `backend/app/` (prompt, `.json`, `.sql`, `.yaml`...) tự được gói. Thư mục tài nguyên mới **ngoài** `backend/app/` thì phải thêm vào `datas` trong `ocr_dashboard.spec`.
- Đọc file tài nguyên bằng `Path(__file__).parent / ...` (trong `app/`) hoặc `config.RESOURCE_DIR` (frontend, docs). Ghi file thì **chỉ** ghi vào `config.DATA_DIR`. Không ghi cạnh code, vì thư mục cài sẽ bị ghi đè khi cập nhật.
- Thêm biến `.env` mới: thêm vào `backend/.env.example` với **giá trị trống** nếu là key hoặc mật khẩu. File này được gói vào bộ cài, và `tests/test_packaging.py` sẽ báo lỗi nếu lỡ điền.
- Chạy thử launcher từ source: `cd backend && py launcher.py` (dùng `backend\.env` và `backend\data` như bình thường).
