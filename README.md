# OCR Dashboard CNKT3 (DMWCS & SCADA)

Upload ảnh chụp màn hình báo cáo SCADA (HT1) và DMWCS (HT2). Hệ thống OCR bằng AI (Gemini → NVIDIA → OpenRouter), kiểm tra số liệu, lưu vào SQLite và vẽ dashboard theo ngày. Không cần Docker, không cần database server.

<p align="center">
  <img src="frontend/img/favicon.png" alt="OCR Dashboard CNKT3" width="240">
</p>

| `loai` | Màn hình |
|---|---|
| `scada` | SCADA, trang "Thống kê và phân tích dữ liệu" (4 dây chuyền) |
| `dmwcs_sorted` | DMWCS, "The Report of Sorted parcels" |
| `dmwcs_capacity` | DMWCS, "The Report of Capacity" (công suất theo ngày) |
| `dmwcs_bcr_rate` | DMWCS, Hours&BcrRate (tỷ lệ đọc mã theo Scanner) |

---

## 1. Yêu cầu

- Python **3.11+**. Không cần Docker.
- Ít nhất 1 API key:
  - Gemini: https://aistudio.google.com/apikey
  - NVIDIA NIM: https://build.nvidia.com (chỉ dùng model có tag *Free Endpoint*)
  - OpenRouter: https://openrouter.ai/keys (free tier ~50 request/ngày)
  - Groq: https://console.groq.com/keys

## 2. Cài đặt

```powershell
cd dashboard
python -m venv .venv
.venv\Scripts\activate            # Linux/macOS: source .venv/bin/activate
pip install -r backend/requirements.txt
copy backend\.env.example backend\.env   # rồi điền key vào backend/.env
```

Nếu không có `backend/.env`, app đọc `dashboard/.env` (file key đang dùng hiện nay).

## 3. Chạy

```powershell
cd backend
uvicorn app.main:app --reload
```

- Dashboard: http://localhost:8000
- Upload ảnh: http://localhost:8000/html/upload.html
- Đạo Vận Chi Lượng – thời gian sử dụng (cộng cột F của file Excel .xlsx ngay trên trình duyệt, không lưu, không cần backend): http://localhost:8000/html/thoi-gian.html
- Lịch sử (tìm theo tên file, lọc ngày, xem chi tiết từng lần OCR kể cả bản đã bị thay): http://localhost:8000/html/history.html
- Swagger (tài liệu API): http://localhost:8000/docs

Dữ liệu nằm trong `backend/data/` (`ocr.db` và `uploads/`). Xóa thư mục này là về trạng thái trống.

### Cài trên máy không có Python

Đóng gói thành `OCRDashboard-Setup.exe` (Python nằm sẵn trong bộ cài, `.env` và dữ liệu tạo lúc chạy lần đầu): xem [backend/packaging/README.md](backend/packaging/README.md).

### Mở cho người khác dùng qua link Vercel

Frontend nằm trên Vercel (https://dashboard-frontend-silk-zeta.vercel.app). Vercel chuyển `/api/*` và `/uploads/*` về backend chạy trên máy này qua Cloudflare Quick Tunnel; dữ liệu và API key vẫn ở máy local.

```powershell
# một lần: winget install --id Cloudflare.cloudflared
powershell -ExecutionPolicy Bypass -File backend\scripts\start_public.ps1   # chạy từ thư mục gốc repo
```

Script chạy backend (cổng 8000) + tunnel, ghi link `*.trycloudflare.com` mới vào `frontend/vercel.json`, commit và push **riêng file đó** để Vercel deploy lại (~1 phút). Giữ cửa sổ mở; **Ctrl+C** tắt cả hai. Máy tắt hoặc script dừng thì link Vercel không dùng được. Không chạy song song với `uvicorn` khác ở cổng 8000.

## 4. Import dữ liệu JSON cũ

```powershell
cd backend
python scripts/import_json.py ../ket_qua_json
```

Nhận file 1 bản ghi hoặc mảng (`tong_hop_*.json`). Chạy lại không tạo bản sao. Cảnh báo được tính lại bằng bộ kiểm tra hiện tại.

Các công cụ dòng lệnh khác (đều chạy trong `backend/`):

| Lệnh | Việc |
|---|---|
| `python scripts/ocr_folder.py ../sample_dashboar/HT2/sorted --bao-cao sorted` | OCR cả thư mục ảnh ra JSON (không ghi DB) |
| `python scripts/compare_models.py ../sample_dashboar/HT2/bcr_rate --bao-cao bcr_rate --gt ../ket_qua_json/HT2` | So độ chính xác từng model |
| `pytest` | Test không cần API key |
| `pytest tests/test_hoi_quy.py` | So kết quả OCR với số đã đối chiếu tay (cần chạy `ocr_folder.py` trước) |

## 5. Cấu trúc thư mục

```
dashboard/
├── backend/
│   ├── app/
│   │   ├── main.py            # tạo app, mount frontend + uploads, start worker + scheduler
│   │   ├── config.py          # đọc .env, chuỗi provider/model, RETENTION_DAYS
│   │   ├── db.py, models.py   # SQLAlchemy, các bảng (mục 7)
│   │   ├── schemas.py         # Pydantic cho 4 loại output (dùng cả làm response_schema cho Gemini)
│   │   ├── api/               # upload.py, reports.py, dashboard.py, system.py
│   │   ├── ocr/
│   │   │   ├── prompts/*.txt  # prompt (sửa được không cần sửa code)
│   │   │   ├── providers/     # base.py (exception chuẩn), gemini.py, nvidia.py, openrouter.py
│   │   │   ├── router.py      # chuỗi fallback provider/model + cooldown
│   │   │   ├── classify.py    # tự nhận diện loại ảnh
│   │   │   ├── pipeline.py    # OCR 2 lần → so sánh → validate
│   │   │   └── abnormal_types.json
│   │   └── services/          # ingest, normalize, validate, retention, worker (hàng đợi OCR)
│   ├── scripts/               # import_json.py, ocr_folder.py, compare_models.py
│   ├── tests/                 # fixtures/ (4 file mẫu), test_validate, test_ingest, test_router, test_hoi_quy
│   ├── data/                  # (gitignore) ocr.db, uploads/
│   ├── requirements.txt, .env.example, pytest.ini
├── frontend/
│   ├── html/                  # index.html (dashboard), upload.html, history.html, report.html, chat.html, thoi-gian.html
│   ├── css/                   # base.css, dashboard.css, upload.css
│   └── js/                    # api.js (mọi fetch đi qua đây), dashboard.js, upload.js, report.js, history.js, thoi-gian.js (đọc .xlsx, cộng giờ, vẽ biểu đồ)
├── sample_dashboar/           # ảnh mẫu: HT1/, HT2/{sorted,capacity,bcr_rate}/
├── ket_qua_json/              # JSON OCR cũ (import được)
├── data_dictionary.md         # ý nghĩa từng trường, lỗi OCR đã biết
└── README.md
```

## 6. Luồng OCR

```
upload ảnh ──► lưu file (sha256, trùng thì trả kết quả cũ) ──► job vào hàng đợi (xử lý tuần tự)
   ──► chưa chọn loại? nhận diện loại (1 lần gọi API)
   ──► OCR lần 1, OCR lần 2 (mỗi lần đi qua chuỗi provider bên dưới)
   ──► so từng trường số giữa 2 lần + kiểm tra số học
   ──► status: ok | can_kiem_tra   ──► ghi DB (raw JSON 2 lần + log fallback) ──► dashboard
```

Thứ tự: **Gemini → NVIDIA NIM → OpenRouter**, mỗi provider có danh sách model riêng (`config.py`, override bằng `GEMINI_MODELS`, `NVIDIA_MODELS`, `OPENROUTER_MODELS`).

| Lỗi (exception chuẩn) | Ví dụ | Router làm gì |
|---|---|---|
| `QuotaExceeded` | 429, `RESOURCE_EXHAUSTED` | Đổi model kế tiếp. Model cooldown 60s; nếu lỗi theo ngày ("per day"/"daily" hoặc 429 liên tiếp 3 lần) thì cooldown tới 00:00 hôm sau |
| `AuthError` | 401/403/402, key sai/hết hạn | Bỏ cả provider, provider `disabled` tới khi restart app hoặc bấm reset |
| `ProviderUnavailable` | timeout, lỗi mạng, 5xx | Thử lại 2 lần (1s, 3s), vẫn lỗi thì đổi provider |
| `ModelNotFound` | 404, model bị gỡ | Đổi model, model `disabled` |
| `BadOutput` | JSON hỏng, sai schema | Thử lại 1 lần cùng model, vẫn sai thì đổi model |

Trạng thái lưu ở bảng `model_status`, xem tại `GET /api/system/providers` (hoặc Swagger `/docs`), gỡ bằng `POST /api/system/providers/reset`.

**Status của report:** `ok` · `can_kiem_tra` (2 lần đọc lệch hoặc sai số học, chi tiết trong `canh_bao`; trang upload tô vàng cảnh báo, tô đỏ trường lệch) · `da_sua_tay` (đã sửa ở `report.html`).

## 7. Database (SQLite, `backend/data/ocr.db`)

| Bảng | Nội dung |
|---|---|
| `uploads` | Ảnh đã upload: tên gốc, đường dẫn, `sha256` (unique), kích thước |
| `jobs` | Hàng đợi OCR: `pending/running/done/failed`, tiến trình, lỗi |
| `reports` | Mỗi kết quả OCR: `loai`, provider/model 2 lần, `status`, `canh_bao`, `report_date`, `data` (dữ liệu đang dùng), `raw_json_1/2`, `attempts` |
| `scada_summary` | 1 dòng/report: mọi thẻ số SCADA. Unique theo (`day_chuyen_key`, ca) |
| `scada_abnormal` | n dòng/report: `loai_raw`, `loai_key`, `loai_vi`, `so_luong`, `ty_le` |
| `dmwcs_sorted` (+ `dmwcs_no_chute_items`) | Total, Correct, PDA, Reject, NoRead/NoPostOffice/NoChute, danh sách máng NoChute |
| `dmwcs_capacity_daily` | Mỗi ngày đúng 1 dòng; ảnh có khoảng truy vấn mới hơn thắng, khác giá trị thì cảnh báo |
| `dmwcs_bcr` | Mỗi Scanner 1 dòng: `bcr_no`, total, success, failed, rate |
| `model_status` | Trạng thái provider/model của router |

Upload lại cùng ca/cùng ngày thì **ghi đè** trên dashboard; report cũ vẫn giữ trong `reports` (raw JSON).
Muốn đổi sang PostgreSQL: chỉ đổi `DATABASE_URL`.

## 8. Tự động xóa sau 35 ngày

- `RETENTION_DAYS=35` trong `.env`. Chạy khi app khởi động và mỗi ngày 02:00 (giờ Việt Nam). VACUUM mỗi Chủ nhật 03:00.
- Xóa: report có `report_date` cũ hơn 35 ngày (kèm dòng chi tiết), dòng `dmwcs_capacity_daily` theo `ngay`, upload không còn report nào (kèm file ảnh), job cũ.
- Xem trước: `POST /api/system/cleanup?dry_run=true`. Xóa thật: `dry_run=false`.

## 9. Thêm / sửa tên loại bất thường SCADA

Sửa `backend/app/ocr/abnormal_types.json`: mỗi `loai_key` có `vi` (tên hiển thị) và `bien_the` (các cách OCR đã đọc). Khi so khớp: bỏ dấu, chữ thường, ký tự `?` khớp 1 ký tự bất kỳ; không khớp hẳn thì so gần đúng (≥ 80%). Không khớp gì thì lưu `UNKNOWN` và thêm cảnh báo. Khởi động lại app sau khi sửa.

## 10. Troubleshooting

| Hiện tượng | Cách xử lý |
|---|---|
| 429 / hết quota | Router tự đổi model/provider. Xem `GET /api/system/providers`; model "tạm nghỉ" tự hết cooldown. Hết cả chuỗi thì đợi hoặc thêm key provider khác |
| Key sai / hết hạn / hết credit | Provider bị "tắt" (`disabled`). Sửa key trong `.env`, khởi động lại app (hoặc `POST /api/system/providers/reset`) |
| Model bị gỡ khỏi free tier (404) | Model bị tắt. Đổi danh sách model trong `.env` (`NVIDIA_MODELS=...`) |
| Ảnh quá lớn | Giới hạn upload `MAX_UPLOAD_MB` (mặc định 10). Với NVIDIA/OpenRouter, ảnh bị chê quá lớn sẽ tự nén JPEG ≤ 2048px rồi gửi lại |
| Kết quả sai | Mở report (`Xem / sửa`), sửa số, Lưu → `da_sua_tay`. Hoặc "OCR lại" bằng provider/model khác |
| Ảnh "đã được xử lý trước đó" | Upload trùng ảnh (cùng sha256). Bấm "OCR lại" nếu muốn đọc lại |

Xem thêm [data_dictionary.md](data_dictionary.md) cho ý nghĩa từng trường và lỗi OCR đã gặp.
