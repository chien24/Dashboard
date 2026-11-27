# Kiểm kê giao diện OCR Dashboard (không đưa vào RAG)

Ngày kiểm kê: 2026-11-20, bổ sung trang Đạo Vận Chi Lượng 2026-11-21. Nguồn: `frontend/` và các phần `backend/` mà giao diện gọi tới.
Đường dẫn tính từ thư mục `dashboard/`. Mỗi dòng có mã (T, P, H, M, S, C, G, B) để đối chiếu trong `_coverage.md`.

## 1. Trang

| Mã | Trang / màn hình | Cách mở | Nguồn |
| --- | --- | --- | --- |
| T1 | Thiên Cơ Các (Dashboard), tab "HT1 – SCADA" | Menu "Thiên Cơ Các", logo Viettel Post, `/` | frontend/html/index.html:17-56 |
| T2 | Thiên Cơ Các, tab "HT2 – DMWCS (CBS)" | Bấm tab, hoặc link `index.html#ht2` | frontend/html/index.html:59-81, frontend/js/dashboard.js:313 |
| T3 | Truyền Pháp Ảnh (tiêu đề "Truyền Tống Linh Ảnh") | Menu "Truyền Pháp Ảnh" | frontend/html/upload.html |
| T4 | Tàng Kinh Các (tiêu đề "Thiên Đạo Ký Sơ") | Menu "Tàng Kinh Các"; tab HT2 qua `#ht2` | frontend/html/history.html |
| T5 | Xem / sửa report | "Xem / sửa số liệu" ở Tàng Kinh Các; "Xem / Sửa" ở Truyền Pháp Ảnh; `report.html?id=` | frontend/html/report.html |
| T6 | Vấn Đạo Đài (chatbot) | Menu "Vấn Đạo Đài"; "Xem lịch sử" trong khung chat nổi | frontend/html/chat.html |
| T7 | Khung chat nổi (góc phải dưới) | Nút tròn góc phải dưới, mọi trang trừ Vấn Đạo Đài và trang phong ấn | frontend/js/chat-widget.js |
| T8 | Hộp thoại "Nhập Môn" (đăng nhập) | Nút "Nhập Môn" trên header; "Bắt đầu ngay" khi chưa đăng nhập | frontend/js/api.js:106-114, 168-198 |
| T9 | Popup chào mừng | Tự hiện lần đầu mở web trong phiên trình duyệt | frontend/js/api.js:238-262 |
| T10 | Trang "Thiên Đạo phong ấn" | Tự chuyển tới khi sai mật khẩu 8 lần | frontend/html/jail.html |
| T11 | Header, menu, footer, thông báo nổi (chung mọi trang) | Luôn có | frontend/html/*.html:13-17, frontend/js/api.js:80-103, 139-155 |
| T12 | Đạo Vận Chi Lượng (cộng cột F file Excel, chỉ chạy trên trình duyệt) | Menu "Đạo Vận Chi Lượng" | frontend/html/thoi-gian.html, frontend/js/thoi-gian.js |

## 2. Phần tử giao diện

| Mã | Phần tử (nhãn nguyên văn) | Trang | Nguồn |
| --- | --- | --- | --- |
| P1 | Logo Viettel Post (về Dashboard), chữ "OCR Dashboard CNKT3" | chung | index.html:13-14 |
| P2 | Nút sáng/tối (tooltip "Chuyển sang chế độ sáng" / "Chuyển sang chế độ tối") | chung | api.js:59-69, 271-276 |
| P3 | Nút "Nhập Môn" / "Xuất Môn" | chung | api.js:168-177 |
| P4 | Menu "Thiên Cơ Các", "Truyền Pháp Ảnh", "Tàng Kinh Các", "Vấn Đạo Đài", "Đạo Vận Chi Lượng" | chung | index.html:17 |
| P5 | Footer: "Xem địa chỉ trên Google Maps", mục "Gặp Kiếp Nạn", mục "Dẫn Lộ Bàn", nút "Lên đầu trang" | chung | api.js:80-103 |
| P6 | Ô "Tài khoản", "Mật khẩu", nút "Hủy", "Nhập Môn" | T8 | api.js:106-114 |
| P7 | Popup: "Chào mừng bạn đến với hệ thống Thiên Đạo", nút "Bắt đầu ngay", "Bỏ qua", "✕" | T9 | api.js:238-262 |
| P8 | Tab "HT1 – SCADA", "HT2 – DMWCS (CBS)" | T1, T2 | index.html:22-25 |
| P9 | Ô "Từ ngày", "Đến ngày" (HT1 và HT2) | T1, T2 | index.html:30-31, 61-62 |
| P10 | Ô chọn "Dây chuyền" (mục "Tất cả" + tên dây chuyền OCR đọc được) | T1 | index.html:32, dashboard.js:211 |
| P11 | Gợi ý "Bấm vào một ngày trên biểu đồ để xem chỉ số của ngày đó." | T1, T2 | index.html:33, 63 |
| P12 | Dòng "Chỉ số ngày dd/mm/yyyy · Tất cả dây chuyền" / "· máy CBS" | T1, T2 | dashboard.js:218, 267 |
| P13 | Thẻ HT1: "ALL", "CORRECT", "REJECT", "Công suất MAX", "Thời gian sử dụng" | T1 | dashboard.js:223-230 |
| P14 | Thẻ HT2: "ALL", "CORRECT", "REJECT", "Công suất AVG", "Thời gian sử dụng" | T2 | dashboard.js:268-274 |
| P15 | Biểu đồ "Sản lượng theo ngày" (HT1: CORRECT, REJECT) | T1 | index.html:38, dashboard.js:234-236 |
| P16 | Biểu đồ "REJECT theo loại" (Không có mã vạch, Yêu cầu ống dẫn thất bại) | T1 | index.html:39, dashboard.js:237-239 |
| P17 | Biểu đồ "So sánh 4 dây chuyền" + ô chọn "Sản lượng ALL", "REJECT", "Tỷ lệ REJECT (%)", "Công suất MAX", "Thời gian sử dụng (h)" | T1 | index.html:41-48 |
| P18 | "Bảng chi tiết" + nút "Xuất CSV" + ghi chú "Thời gian sử dụng = ALL / Công suất MAX…" | T1 | index.html:50-54, dashboard.js:246-253 |
| P19 | Biểu đồ "Sản lượng theo ngày" HT2 (CORRECT – CorrectChute, CORRECT – PDA, REJECT) | T2 | dashboard.js:277-280 |
| P20 | Biểu đồ "Thành phần REJECT" (NoRead, NoPostOffice, NoChute) | T2 | dashboard.js:281-284 |
| P21 | Biểu đồ "Công suất AVG theo ngày" + ghi chú "Mỗi ngày đúng 1 giá trị…" | T2 | index.html:70-71 |
| P22 | Biểu đồ "Tỷ lệ đọc thành công của từng Scanner" + bảng BCR_NO/TOTAL/SUCCESS/FAILED/RATE | T2 | dashboard.js:58-85, 288-298 |
| P23 | Biểu đồ "Thời gian sử dụng (h)" | T2 | index.html:73, dashboard.js:299-300 |
| P24 | "Bảng chi tiết theo ngày" + nút "Xuất CSV" + ghi chú "CORRECT = CorrectChute + PDA…" | T2 | index.html:75-79, dashboard.js:302-309 |
| P25 | Ô nhỏ hiện số khi rê chuột lên biểu đồ (tooltip), dòng "Tổng" | T1, T2 | dashboard.js:94-100, 159-168 |
| P26 | Huy hiệu cảnh báo "⚠ n" / "✓ 0" trong bảng | T1, T2, T4 | dashboard.js:174-177, history.js:68 |
| P27 | Link "Tàng Kinh Các" dưới mỗi tab dashboard | T1, T2 | index.html:55, 80 |
| P28 | Vùng "Kéo thả ảnh vào đây hoặc bấm để chọn" | T3 | upload.html:22-25 |
| P29 | Ô chọn "Loại cho tất cả ảnh": "Thần Niệm (tự nhận diện)", "SCADA", "DMWCS Sorted", "DMWCS Capacity", "DMWCS BCR rate" | T3 | upload.html:28-33 |
| P30 | Nút "Khai Phá Thiên Cơ", "Xóa Bỏ Phế Tích", gợi ý "Dùng "Thần Niệm" sẽ tốn thêm 1 lần Thiên Cơ lệnh mỗi ảnh." | T3 | upload.html:34-36 |
| P31 | Dòng từng ảnh: ảnh nhỏ, tên file, ô chọn loại riêng ("Theo lựa chọn chung", …), thanh tiến trình, chữ trạng thái, đồng hồ m:ss | T3 | upload.js:5-20 |
| P32 | Khối kết quả: tên loại, trạng thái, hộp "Cảnh báo", mục "Dữ liệu đọc được (N trường lệch)" | T3 | upload.js:126-139 |
| P33 | Nút "OCR lại" (ảnh trùng), "Thử lại" (thất bại), link "xem kết quả cũ", "Xem / Sửa" | T3 | upload.js:87-122 |
| P34 | Ô "Truy tìm bí pháp (chung cho cả HT1 và HT2)" (gợi ý "vd: Screenshot 2026-11-16, 3.jpg") | T4 | history.html:23-24 |
| P35 | Ô "Ngày báo cáo từ", "đến", ô chọn "Trạng thái" (Tất cả, OK, Cần kiểm tra, Đã sửa tay), nút "Xóa bộ lọc" | T4 | history.html:25-32 |
| P36 | Tab HT1/HT2 có số đếm; dòng tóm tắt "Tìm thấy N báo cáo · HT1: a · HT2: b" | T4 | history.html:35-39, history.js:43 |
| P37 | Danh sách theo "Ngày dd/mm/yyyy"; mỗi dòng: tiêu đề, tên file, trạng thái, cảnh báo, "Đã được thay", "upload …" | T4 | history.js:78-91 |
| P38 | Nút "Tải thêm (còn N)" | T4 | history.js:90 |
| P39 | Chi tiết khi mở dòng: ảnh (bấm mở ảnh gốc), "Tên file", "Upload lúc", "Model", "Trên dashboard", nút "Xem / sửa số liệu", số liệu theo loại, "Cảnh báo" | T4 | history.js:103-138 |
| P40 | Tiêu đề "<Loại> · <tên file>", dòng "Ngày báo cáo … · trạng thái · …", hộp "Cảnh báo" | T5 | report.js:32-36 |
| P41 | Khung ảnh gốc (tooltip "Bấm để phóng to / thu nhỏ"; "Không có ảnh gốc (report import từ JSON).") | T5 | report.html:23, report.js:54 |
| P42 | Form số liệu (mỗi trường một ô, nhóm theo khung; mỗi dòng danh sách có nút "Xóa dòng") + nút "Lưu" | T5 | report.js, report.html |
| P43 | Nút "Thêm giá trị" (chỉ SCADA, Capacity, BCR rate) | T5 | report.html, report.js (LIST) |
| P44 | Nút "OCR lại" (tự đọc lại, không cần chọn) | T5 | report.html, report.js |
| P45 | Mục "OCR Version": "OCR lần N" + giờ, nhãn "Đang dùng", "Xem JSON", nút "Dùng bản này" | T5 | report.js (renderVersions); backend/app/api/reports.py versions() |
| P46 | Nút "Xóa report" | T5 | report.html:37 |
| P47 | Cột trái: nút "+ Cuộc trò chuyện mới", danh sách cuộc trò chuyện mọi máy theo nhóm "Hôm nay / Hôm qua / 7 ngày qua / 30 ngày qua", ghi chú 30 ngày; nút "Lịch sử trò chuyện" ở màn hình hẹp | T6 | chat.html, chat.js (loadList), backend/app/chatbot/router.py conversations() |
| P48 | Câu hỏi mẫu "Thử một câu hỏi:" (6 câu) | T6 | chat.html:31-34, chat.js:5-12 |
| P49 | Ô nhập (gợi ý "VD: Tỷ lệ REJECT HT2 hôm qua?"), nút "Gửi câu hỏi", "Hủy"; dòng "Enter để gửi, Shift+Enter để xuống dòng." và dòng thống kê "Hôm nay: …" | T6 | chat.html:36-44, chat.js:131-136 |
| P50 | Câu trả lời: chữ, danh sách cảnh báo, nút lựa chọn, bảng kết quả, dòng thời gian trả lời | T6 | chat.js:40-65 |
| P51 | Nút tròn mở khung chat (tooltip "Hỏi đáp dữ liệu"), tiêu đề "Vấn Đạo Đài", link "Xem lịch sử", nút "✕", ô "Nhập câu hỏi…", nút "Gửi", link "Xem bảng kết quả" | T7 | chat-widget.js |
| P52 | Trang phong ấn: đồng hồ đếm ngược, nút "Bật âm thanh" / "Tắt âm thanh", lời phán | T10 | jail.html:45-51 |
| P53 | Vùng "Kéo thả file Excel vào đây hoặc bấm để chọn"; thẻ "Tổng thời gian sử dụng", "Số lần chạy", "Số thiết bị", "Trung bình mỗi thiết bị" | T12 | thoi-gian.html, thoi-gian.js |
| P54 | Biểu đồ "Thời gian theo thiết bị", "Tổng thời gian theo file"; khung từng file với "Tổng:" và "Chi tiết theo thiết bị" | T12 | thoi-gian.js |

## 3. Hành động người dùng

| Mã | Thao tác | Trang web phản hồi | Nguồn |
| --- | --- | --- | --- |
| H1 | Bấm "Nhập Môn", điền, bấm "Nhập Môn" | Đúng: tải lại trang, thông báo "Nhập Môn thành công. Chào mừng đạo hữu!". Sai: câu báo lỗi và câu phụ theo số lần sai | api.js:181-197 |
| H2 | Bấm "Xuất Môn" | Tải lại trang, thông báo "Xuất Môn thành công. Hẹn ngày tái ngộ!" | api.js:174-176 |
| H3 | Bấm nút sáng/tối | Đổi giao diện, nhớ lựa chọn cho lần sau | api.js:271-276 |
| H4 | Đổi tab HT1/HT2 trên Dashboard | Hiện tab tương ứng | dashboard.js:189-193 |
| H5 | Đổi "Từ ngày" / "Đến ngày" | Vẽ lại biểu đồ, bảng; ngày chỉ số về ngày mới nhất có dữ liệu. Tối đa 35 ngày cuối của khoảng | dashboard.js:194-208 |
| H6 | Đổi "Dây chuyền" | Lọc thẻ, biểu đồ, bảng HT1 theo dây chuyền | dashboard.js:257 |
| H7 | Bấm vào một ngày trên biểu đồ | Thẻ chỉ số chuyển sang ngày đó, cột ngày đó được tô nền | dashboard.js:233, 275 |
| H8 | Rê chuột lên biểu đồ | Hiện ô số liệu của ngày / Scanner | dashboard.js:159-168, 78-84 |
| H9 | Đổi chỉ số ở "So sánh 4 dây chuyền" | Vẽ lại biểu đồ theo chỉ số chọn | dashboard.js:240-244 |
| H10 | Bấm "Xuất CSV" | Tải file h1-table.csv / h2-table.csv đúng như bảng đang hiện | dashboard.js:183-188 |
| H11 | Kéo thả / chọn ảnh | Thêm dòng ảnh, file không phải .jpg/.jpeg/.png/.webp bị bỏ qua im lặng | upload.js:8-31 |
| H12 | Bấm "Khai Phá Thiên Cơ" | Gửi lần lượt từng ảnh chưa gửi, theo dõi tiến trình 2 giây/lần | upload.js:148-151, 109-115 |
| H13 | Bấm "Xóa Bỏ Phế Tích" | Xóa danh sách ảnh trên màn hình (ảnh đã gửi vẫn được xử lý) | upload.js:32 |
| H14 | Bấm "OCR lại" (ảnh trùng) / "Thử lại" (thất bại) | Gửi lại ảnh, bắt đọc lại | upload.js:90, 106 |
| H15 | Gõ tìm kiếm ở Tàng Kinh Các | Tìm sau 0,3 giây; tô vàng phần khớp; tự chuyển tab nếu tab đang xem không có kết quả | history.js:42, 63-67, 161 |
| H16 | Đổi ngày / trạng thái, bấm "Xóa bộ lọc" | Tải lại danh sách | history.js:162-163 |
| H17 | Bấm một dòng report | Mở chi tiết | history.js:92, 141-150 |
| H18 | Bấm "Tải thêm (còn N)" | Tải thêm 50 report | history.js:49-54 |
| H19 | Bấm ảnh ở trang report | Phóng to / thu nhỏ | report.js:54 |
| H20 | Sửa ô, bấm "Lưu" | "Đang lưu…" rồi "Đã lưu. Dashboard dùng số liệu mới."; trạng thái thành Đã sửa tay | report.js:44-52; backend/app/api/reports.py:95-119 |
| H21 | Bấm "Thêm giá trị" / "Xóa dòng" | Thêm / bỏ 1 dòng trên form: "Đã thêm 1 dòng. Điền giá trị rồi bấm Lưu." / "Đã bỏ 1 dòng. Bấm Lưu để lưu lại." | report.js |
| H22 | Bấm "OCR lại" | "Đang OCR lại…", xong thì mở report mới | report.js |
| H22b | Bấm "Dùng bản này" ở OCR Version | Hỏi xác nhận, lưu số của lần đọc đó: "Đã quay về OCR lần N. Dashboard dùng số liệu này." | report.js |
| H23 | Bấm "Xóa report" | Hộp xác nhận "Xóa report này? Số liệu của nó sẽ biến mất khỏi dashboard.", đồng ý thì về Dashboard. Ảnh không còn report nào thì bị xóa luôn (cùng job, file) | report.js:73-77; backend/app/api/reports.py delete_report |
| H24 | Gửi câu hỏi ở Vấn Đạo Đài | "Đang truy vấn…" rồi câu trả lời | chat.js:72-100 |
| H25 | Bấm "Hủy" khi đang chờ | "Đã hủy chờ. Câu hỏi vẫn có thể đang chạy ở máy chủ." | chat.js:95 |
| H26 | Bấm câu hỏi mẫu / nút lựa chọn | Gửi câu đó | chat.js:126-129 |
| H27 | Bấm "+ Cuộc trò chuyện mới" | Cột phải trống, hiện câu hỏi mẫu | chat.js |
| H27b | Bấm một cuộc trò chuyện ở cột trái | Mở cuộc đó (kể cả của máy khác), hỏi tiếp được | chat.js (openConv) |
| H28 | Mở lại Vấn Đạo Đài | Mở cuộc trò chuyện đang dùng của máy này; cột trái liệt kê mọi máy | chat.js |
| H29 | Bấm nút tròn góc phải dưới, gửi câu hỏi | Mở khung chat; câu trả lời ngắn; Esc / "✕" để đóng | chat-widget.js |
| H30 | Rời trang phong ấn bằng nút Back | Không rời được tới khi hết giờ | jail.html:79-80 |
| H31 | Chọn / kéo thả file .xlsx ở Đạo Vận Chi Lượng | Cộng cột F, hiện thẻ, biểu đồ, khung từng file; file không đuôi .xlsx khi kéo thả bị bỏ qua | thoi-gian.js |
| H32 | Tải lại trang Đạo Vận Chi Lượng | Mất kết quả, không lưu gì | thoi-gian.js |

## 4. Thông báo

| Mã | Chuỗi hiển thị | Khi nào | Nguồn |
| --- | --- | --- | --- |
| M1 | "Tư chất quá kém, tiên duyên chưa đủ, mời ngươi quay về đi!" + câu phụ theo lần sai | Sai tài khoản/mật khẩu | api.js:116-130 |
| M2 | Chuyển tới trang phong ấn ("Sai mật khẩu 8 lần…") | Sai lần thứ 8 trong 5 phút | api.js:132-136; backend/app/api/auth.py |
| M3 | "Nhập Môn thành công. Chào mừng đạo hữu!" / "Xuất Môn thành công. Hẹn ngày tái ngộ!" | Đăng nhập / đăng xuất | api.js:175, 190 |
| M4 | "Cần đăng nhập" (trong "Không tải được …: Cần đăng nhập") | Hết phiên khi đang dùng | backend/app/main.py:60 |
| M5 | "Không tải được dữ liệu: …" | Dashboard lỗi tải | dashboard.js:316 |
| M6 | "Không có dữ liệu trong khoảng ngày đã chọn" | Bảng chi tiết trống | dashboard.js:252, 308 |
| M7 | "Chưa có dữ liệu Scanner ngày …" / "Ngày … chưa có dữ liệu Scanner, đang hiện ngày gần nhất có dữ liệu." | Biểu đồ Scanner | dashboard.js:294-297 |
| M8 | "Chưa nhập môn, chưa thể truyền ảnh. Hãy thực hiện Nhập Môn ở góc trên bên phải." | Upload khi chưa đăng nhập | upload.js:159 |
| M9 | "Chưa gửi", "Đang gửi ảnh…", "Đang chờ tới lượt", "Đang OCR · …" | Tiến trình từng ảnh | upload.js:19, 83, 113 |
| M10 | "✓ Thành công · Xem / Sửa" + thông báo "OCR thành công (…)" | OCR xong, không cảnh báo lỗi | upload.js:122 |
| M11 | "✓ Xong, cần kiểm tra · Xem / Sửa" + "OCR xong nhưng có N cảnh báo, nên kiểm tra lại số liệu." | OCR xong, cần kiểm tra | upload.js:119-121 |
| M12 | "Ảnh đã được xử lý trước đó · xem kết quả cũ · OCR lại" + "Ảnh này đã OCR trước đó, đang hiện kết quả cũ." | Ảnh trùng | upload.js:88-89 |
| M13 | "✕ Thất bại", "OCR thất bại: <tên file>", "Không đọc được ảnh này." + "Có thể chọn đúng loại ảnh ở ô bên cạnh tên file rồi thử lại." | OCR lỗi | upload.js:100-107 |
| M14 | "Tất cả provider/model đều lỗi: …" | Mọi nguồn đọc đều lỗi | backend/app/ocr/router.py:24-28 |
| M15 | "Không nhận diện được loại màn hình. Hãy chọn loại khi upload." | Thần Niệm không nhận ra loại ảnh | backend/app/ocr/classify.py:12 |
| M16 | "Mất kết nối tới server: …" | Mất mạng khi theo dõi tiến trình | upload.js:110 |
| M17 | "File không phải ảnh hợp lệ: …" | File hỏng / giả ảnh | backend/app/api/upload.py:29 |
| M18 | "Chỉ nhận ảnh .jpg, .jpeg, .png, .webp: …" | Sai đuôi file | backend/app/api/upload.py:60 |
| M19 | "<tên file> lớn hơn 10.0 MB" | Ảnh quá dung lượng | backend/app/api/upload.py:62, 65 |
| M20 | "Chưa Nhập môn, không thể tra cứu Tàng Kinh Các." | Tàng Kinh Các khi chưa đăng nhập | history.js:26 |
| M21 | "Đang tìm…", "Không tải được lịch sử: …", "Không tải được chi tiết: …", "Đang tải…" | Tàng Kinh Các | history.js:30, 37, 87, 148 |
| M22 | "Không có báo cáo nào khớp bộ lọc. Thử bỏ bớt điều kiện hoặc bấm Xóa bộ lọc." / "Thiên Cơ trống rỗng. Hãy tiến hành Nạp Linh Ảnh để khai phá." | Danh sách trống | history.js:74-75 |
| M23 | "Thiếu ?id= trên đường dẫn", "Chưa nhập môn, không thể xem / sửa report", "Không tải được report: …", "Không có report này" | Trang report | report.js:80-92; reports.py:48 |
| M24 | "Đang lưu…", "Đã lưu. Dashboard dùng số liệu mới." | Lưu report | report.js:45, 48 |
| M25 | "Report này vừa được sửa ở máy khác. Tải lại trang để xem bản mới rồi sửa lại." | Hai máy cùng sửa | backend/app/api/reports.py:105 |
| M26 | Lỗi kiểm tra dữ liệu khi lưu ("Sai schema: …", "thoi_gian_tu không hợp lệ: …", "den_ngay không hợp lệ: …") | Lưu số liệu sai kiểu | backend/app/api/reports.py:109-113; backend/app/services/normalize.py:26, 30 |
| M27 | "Đã quay về OCR lần N. Dashboard dùng số liệu này.", hộp xác nhận "Thay số liệu đang dùng bằng OCR lần N? …", "Không có bản OCR nào (report import từ JSON)." | OCR Version | report.js |
| M28 | "Đang OCR lại…", "Đang OCR lại · …", "Report import từ JSON, không có ảnh gốc để OCR lại" | OCR lại | report.js; reports.py |
| M29 | "Xóa report này? Số liệu của nó sẽ biến mất khỏi dashboard." | Xóa report | report.js:74 |
| M30 | "Bạn cần Nhập Môn (nút ở góc trên bên phải) để hỏi đáp dữ liệu." / "Bạn cần Nhập Môn (đăng nhập) trước khi hỏi." | Chat khi chưa đăng nhập / hết phiên | chat.js:94, 141 |
| M31 | "Đang truy vấn…", "Đã hủy chờ. Câu hỏi vẫn có thể đang chạy ở máy chủ.", "Không gửi được câu hỏi: …" | Chat | chat.js:79, 95-96 |
| M32 | "Hỏi nhanh quá, chờ N giây rồi hỏi tiếp" | Quá 10 câu/phút | backend/app/chatbot/router.py:27 |
| M33 | "Đã hết lượt hỏi miễn phí, thử lại sau khoảng N phút." / "…, thử lại sau ít phút." | Hết lượt dịch vụ AI | backend/app/chatbot/pipeline.py:129 |
| M34 | "Chatbot chưa gọi được model nào. Báo quản trị kiểm tra …" | Chatbot chưa cấu hình được | backend/app/chatbot/pipeline.py:131 |
| M35 | "Mình chưa trả lời được câu này. Bạn thử diễn đạt lại cụ thể hơn…" | Chatbot không tạo được truy vấn | backend/app/chatbot/pipeline.py:19-20 |
| M36 | "Câu hỏi rỗng", "Câu hỏi dài quá 1000 ký tự" | Gửi câu hỏi sai | backend/app/chatbot/router.py:60-62 |
| M37 | "Không có cuộc trò chuyện này (có thể đã bị xóa theo chính sách lưu trữ)" | Hội thoại đã quá hạn lưu | backend/app/chatbot/router.py:66, 94 |
| M38 | Cảnh báo trong câu trả lời chatbot: dữ liệu đã bị xóa, ngày sau hôm nay, ngày thiếu, report cần kiểm tra, loại chưa phân loại, NoChute bị cắt, ảnh đang OCR | Chat | backend/app/chatbot/checks.py:46-99 |
| M39 | Kết quả rỗng: "Chưa có dữ liệu … cho … (chưa có ảnh được OCR cho khoảng này)…", "Không có dòng nào khớp điều kiện của câu hỏi…" | Chat | backend/app/chatbot/checks.py:109-123 |
| M40 | Ghi chú bảng chat: "Đang hiển thị N dòng đầu, kết quả còn nhiều dòng hơn.", "Đang hiển thị a/b dòng đã lưu.", "N dòng" | Chat | chat.js:36-37 |
| M41 | Cảnh báo số liệu của report (kiểm tra số học, lệch 2 lần đọc, ghi chú khi đọc, "Đã sửa tay", Công suất AVG khác ảnh trước, loại bất thường chưa có) | Upload, Tàng Kinh Các, report, bảng dashboard | backend/app/services/validate.py; backend/app/ocr/pipeline.py:40-44; backend/app/services/ingest.py:41, 76-77; reports.py:117 |
| M43 | "Đang đọc N file…", "Không phải file .xlsx hợp lệ", "Không tìm thấy sheet1 trong file", "Bỏ qua N ô không đúng dạng thời gian:" | Đạo Vận Chi Lượng | thoi-gian.js |
| M42 | "Hỏi nhanh số liệu HT1 (SCADA) và HT2 (DMWCS). VD: …", "Bạn cần Nhập Môn (nút ở góc trên bên phải) trước khi hỏi.", "Phiên đăng nhập đã hết, hãy Nhập Môn lại." | Khung chat nổi | chat-widget.js |

## 5. Trạng thái

| Mã | Giá trị (hiển thị) | Ý nghĩa | Nguồn |
| --- | --- | --- | --- |
| S1 | `ok` / "OK" | Hai lần đọc khớp, số học đúng | backend/app/ocr/pipeline.py:50; history.js:11 |
| S2 | `can_kiem_tra` / "Cần kiểm tra" | Lệch giữa các lần đọc hoặc sai số học | backend/app/ocr/pipeline.py:43-50 |
| S3 | `da_sua_tay` / "Đã sửa tay" | Người dùng đã lưu số liệu bằng tay | backend/app/api/reports.py:118 |
| S4 | "Đã được thay" / "Đang dùng" / "Đã được thay bằng ảnh mới hơn" | Report có / không còn hiện trên dashboard | history.js:85, 133 |
| S5 | Tiến trình ảnh: chưa gửi, đang gửi, chờ tới lượt, đang OCR, thành công, cần kiểm tra, ảnh trùng, thất bại | Trang Truyền Pháp Ảnh | upload.js |
| S6 | Huy hiệu cảnh báo "⚠ n" / "✓ 0" | Số cảnh báo của report | dashboard.js:174-177 |

## 6. Chỉ số và trường dữ liệu

| Mã | Tên trên giao diện | Ý nghĩa, đơn vị | HT | Nguồn |
| --- | --- | --- | --- | --- |
| C1 | ALL | Số lượng đã quét, bưu kiện | HT1 | dashboard.js:40; request/data_dictionary.md 1.1 |
| C2 | REJECT | Không có mã vạch + Yêu cầu ống dẫn thất bại | HT1 | dashboard.js:40 |
| C3 | CORRECT | ALL − REJECT | HT1 | dashboard.js:42 |
| C4 | Tỷ lệ REJECT | REJECT / ALL, % | HT1, HT2 | dashboard.js:43, 89 |
| C5 | Công suất MAX, Khung giờ MAX | Công suất cao nhất trong 1 giờ, bưu kiện/giờ | HT1 | dashboard.js:43, 227 |
| C6 | Thời gian sử dụng (HT1) | ALL / Công suất MAX, giờ, ước tính | HT1 | dashboard.js:43 |
| C7 | Không có mã vạch, Yêu cầu ống dẫn thất bại | Hai loại bất thường cộng vào REJECT | HT1 | dashboard.js:29, 40 |
| C8 | Số liệu SCADA ở Tàng Kinh Các: Số lượng gói theo lưới, Số lượng bưu kiện bất thường, Tỷ lệ bất thường, Thời gian quét trung bình, loại bất thường | Tham khảo | HT1 | history.js:107-114 |
| C9 | ALL (Total), CORRECT (CorrectChute + PDA), REJECT (RejectChute) | bưu kiện | HT2 | dashboard.js:88 |
| C10 | Công suất AVG | Công suất trung bình trong ngày, bưu kiện/giờ | HT2 | dashboard.js:273 |
| C11 | Thời gian sử dụng (HT2) | ALL / Công suất AVG, giờ | HT2 | dashboard.js:89 |
| C12 | NoRead, NoPostOffice, NoChute, danh sách máng NoChute, SortFailed, biểu đồ tròn Correct/Reject | Thành phần REJECT và tham khảo | HT2 | dashboard.js:282-284; history.js:116-122 |
| C13 | Scanner n: RATE, TOTAL, SUCCESS, FAILED | Tỷ lệ đọc mã vạch theo đầu đọc, % và lượt | HT2 | dashboard.js:58-85 |
| C14 | Tỷ lệ CORRECT (HT2) | 1 − Tỷ lệ REJECT | HT2 | dashboard.js:306 |
| C15 | Cột "Nguồn": "Sorted + Capacity" / "Chỉ Capacity" | Ngày có đủ báo cáo nào | HT2 | dashboard.js:305 |

## 7. Giới hạn và quy tắc

| Mã | Quy tắc | Nguồn |
| --- | --- | --- |
| G1 | Định dạng ảnh: .jpg, .jpeg, .png, .webp; kiểm tra đúng là ảnh | backend/app/api/upload.py:16-29 |
| G2 | Dung lượng tối đa mỗi ảnh: 10 MB (mặc định) | backend/app/config.py:24 |
| G3 | Ảnh trùng = cùng nội dung (không xét tên file): không đọc lại trừ khi bấm "OCR lại" | backend/app/api/upload.py:66-70 |
| G4 | Ảnh xử lý lần lượt theo hàng đợi; mỗi ảnh đọc 2 lần rồi đối chiếu | backend/app/services/worker.py; backend/app/config.py:23 |
| G5 | "Thần Niệm" tốn thêm 1 lần đọc để nhận diện loại | backend/app/ocr/pipeline.py:16-19 |
| G6 | Lưu 35 ngày theo ngày báo cáo; dọn tự động 2 giờ sáng mỗi ngày; hội thoại chatbot không dùng 30 ngày bị xóa (CHAT_RETENTION_DAYS) | backend/app/services/retention.py; backend/app/main.py:39 |
| G7 | Ghi đè: report mới cùng dây chuyền + cùng kỳ (SCADA) hoặc cùng kỳ (Sorted, BCR) thay report cũ trên dashboard; Capacity mỗi ngày 1 giá trị, lấy ảnh có ngày cuối khoảng truy vấn muộn hơn | backend/app/services/ingest.py |
| G8 | Hai người cùng sửa 1 report: người lưu sau bị từ chối | backend/app/api/reports.py:101-107 |
| G9 | Đăng nhập: 1 tài khoản dùng chung; phiên 7 ngày; sai 8 lần trong 5 phút thì khóa 5 phút | backend/app/api/auth.py:255-261 |
| G10 | Chưa đăng nhập: thấy giao diện trống, không xem/tải ảnh, không hỏi chatbot | backend/app/main.py:53-64 |
| G11 | Dashboard hiện tối đa 35 ngày cuối của khoảng chọn; mặc định 7 ngày tới ngày mới nhất có dữ liệu | dashboard.js:194-208 |
| G12 | Chatbot: câu hỏi tối đa 1000 ký tự; 10 câu/phút; bảng hiện tối đa 200 dòng; lưu tối đa 50 dòng mỗi câu trả lời; chỉ đọc dữ liệu | backend/app/chatbot/router.py; backend/app/config.py:60-66 |
| G13 | Mỗi máy mở một cuộc trò chuyện riêng (localStorage); danh sách lịch sử chung mọi máy | chat.js |
| G14 | Tàng Kinh Các tải 50 report mỗi lần | history.js:12 |
| G15 | Biểu đồ Scanner: tối đa 6 màu riêng, Scanner 7 trở lên màu xám | dashboard.js:55-56 |
| G16 | Đạo Vận Chi Lượng: chỉ .xlsx, chỉ sheet đầu, cộng cả cột F; quá 7 file thì biểu đồ thiết bị gộp một màu | thoi-gian.js |

## 8. Chỉ có ở backend (giao diện chưa có đường vào)

| Mã | Tính năng | Nguồn |
| --- | --- | --- |
| B1 | Đánh giá câu trả lời chatbot (thích / không thích, ghi chú) | backend/app/chatbot/router.py:99-108 |
| B2 | Thống kê lượt dùng chatbot chia theo từng model | backend/app/chatbot/router.py:111-122 (giao diện chỉ hiện tổng) |
| B3 | Tổng hợp loại bất thường HT1 theo khoảng ngày | backend/app/api/dashboard.py:52-64 |
| B4 | So sánh SCADA và DMWCS theo cùng ngày | backend/app/api/dashboard.py:103-115 |
| B5 | Xem / đặt lại trạng thái các nguồn đọc ảnh, OCR lại bằng một nguồn chỉ định (giao diện chỉ dùng chuỗi mặc định) | backend/app/api/system.py:20-29 |
| B6 | Dọn dữ liệu cũ thủ công (xem trước / xóa) | backend/app/api/system.py:32-35 |
| B7 | Lọc report theo loại cụ thể và theo dây chuyền ở danh sách report | backend/app/api/reports.py:55-80 |
| B8 | Lọc số liệu dashboard theo ngày, dây chuyền, Scanner phía máy chủ (giao diện tải hết rồi lọc tại chỗ) | backend/app/api/dashboard.py |
| B9 | Kiểm tra máy chủ còn chạy (health) | backend/app/api/system.py:15-18 |
| B10 | Hỏi chatbot bằng dòng lệnh | backend/app/chatbot/cli.py |
