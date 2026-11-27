---
id: faq
title: Câu hỏi thường gặp
loai: faq
trang: chung
he_thong: chung
aliases: [FAQ, hỏi đáp, câu hỏi hay gặp, thắc mắc thường gặp]
lien_quan: [bat-dau-nhanh, gioi-han-va-quy-tac, trang-thai, thuat-ngu]
nguon_code: [frontend/js/api.js, frontend/js/upload.js, frontend/js/dashboard.js, frontend/js/history.js, frontend/js/report.js, frontend/js/chat.js, frontend/js/chat-widget.js]
cap_nhat: 2026-11-20
---
# Câu hỏi thường gặp

## Làm sao để đăng nhập vào OCR Dashboard?

Bấm nút **"Nhập Môn"** ở góc trên bên phải, điền "Tài khoản" và "Mật khẩu", bấm **"Nhập Môn"**. Cả chi nhánh dùng chung một tài khoản. Một lần đăng nhập giữ 7 ngày. Xem [Đăng nhập](tac-vu/dang-nhap.md).

## Tại sao đăng nhập báo "Tư chất quá kém, tiên duyên chưa đủ…"?

Tài khoản hoặc mật khẩu sai. Kiểm tra Caps Lock và tắt bộ gõ tiếng Việt rồi gõ lại. Sai 8 lần trong 5 phút sẽ bị khóa 5 phút. Xem [lỗi sai mật khẩu](loi/sai-mat-khau.md).

## Tại sao bị đưa sang trang có đồng hồ đếm ngược?

Đó là trang "Thiên Đạo phong ấn", hiện khi sai mật khẩu 8 lần. Chờ hết 5 phút, trang tự về dashboard, rồi đăng nhập lại với mật khẩu đúng. Nút Back không thoát được trang Thiên Đạo phong ấn. Xem [bị khóa đăng nhập](loi/bi-khoa-dang-nhap.md).

## Muốn đổi mật khẩu thì làm sao?

Trang web không có chức năng tự đổi mật khẩu. Gửi email cho người viết code (Khoa) tại chiencodedao@gmail.com. Sau khi đổi, mọi người đăng nhập bằng mật khẩu mới.

## Làm sao để đăng xuất?

Bấm nút **"Xuất Môn"** ở góc trên bên phải. Trang tải lại và báo "Xuất Môn thành công. Hẹn ngày tái ngộ!". Xem [Đăng xuất](tac-vu/dang-xuat.md).

## Tại sao mở trang mà không thấy số liệu nào?

Thường là chưa đăng nhập: các trang vẫn mở nhưng trống. Bấm **"Nhập Môn"**. Nếu đã đăng nhập mà vẫn trống, có thể khoảng ngày chưa có ảnh nào. Xem [Lọc dashboard theo ngày](tac-vu/loc-dashboard-theo-ngay.md).

## Làm sao để đổi sang giao diện tối?

Bấm nút tròn hình mặt trăng ở góc trên bên phải. Bấm lại (hình mặt trời) để về giao diện sáng. Trang nhớ lựa chọn trên trình duyệt đó. Xem [Đổi giao diện sáng / tối](tac-vu/doi-che-do-sang-toi.md).

## Tải ảnh lên như thế nào?

Vào trang **"Truyền Pháp Ảnh"**, kéo thả ảnh vào vùng "Kéo thả ảnh vào đây", chọn loại ảnh, bấm **"Khai Phá Thiên Cơ"**. Mỗi ảnh có thanh tiến trình riêng. Xem [Tải ảnh lên](tac-vu/tai-anh-len.md).

## Ảnh được tải lên định dạng gì, tối đa bao nhiêu MB?

Ảnh .jpg, .jpeg, .png hoặc .webp, tối đa 10 MB mỗi ảnh. File định dạng khác bị bỏ qua, không hiện trong danh sách. Xem [Giới hạn và quy tắc](tham-chieu/gioi-han-va-quy-tac.md).

## Có tải nhiều ảnh cùng lúc được không?

Được. Chọn hoặc kéo thả nhiều ảnh một lần, rồi bấm "Khai Phá Thiên Cơ". Các ảnh được gửi và đọc lần lượt từng ảnh.

## Hệ thống có tự nhận loại ảnh không?

Có. Để loại là **"Thần Niệm (tự nhận diện)"** thì hệ thống tự đoán, nhưng tốn thêm một lượt đọc mỗi ảnh. Chọn sẵn loại đúng thì nhanh hơn và ít lỗi hơn. Xem [Chọn loại ảnh](tac-vu/chon-loai-anh.md).

## Chọn sai loại ảnh thì sao?

Ảnh thường bị "✕ Thất bại" hoặc ra số vô lý kèm nhiều cảnh báo. Khi thất bại, chọn lại loại đúng ở ô cạnh tên ảnh và bấm **"Thử lại"**. Xem [Chọn loại ảnh](tac-vu/chon-loai-anh.md).

## Tải ảnh xong phải chờ bao lâu?

Không cố định: tùy tốc độ mạng, dịch vụ đọc ảnh và số ảnh đang chờ trong hàng đợi chung. Mỗi ảnh đọc 2 lần. Theo dõi chữ trạng thái và đồng hồ phút:giây trên từng dòng ảnh. Xem [Theo dõi tiến độ](tac-vu/theo-doi-tien-do-xu-ly-anh.md).

## Xem tiến độ xử lý ảnh ở đâu?

Trên trang **"Truyền Pháp Ảnh"**, mỗi dòng ảnh có thanh tiến trình và chữ trạng thái: "Đang gửi ảnh…", "Đang chờ tới lượt", "Đang OCR · …". Lỡ đóng trang thì ảnh vẫn được đọc; xem kết quả ở Tàng Kinh Các.

## Upload ảnh xong mà không thấy số liệu là sao?

Có thể ảnh đọc thất bại ("✕ Thất bại"), ảnh còn trong hàng đợi, hoặc dashboard đang lọc khoảng ngày khác ngày báo cáo của ảnh. Cũng có thể ảnh mới bị báo cáo khác cùng kỳ thay. Kiểm tra ở trang Tàng Kinh Các. Xem [lỗi OCR thất bại](loi/ocr-that-bai.md).

## Tải lại một ảnh đã tải trước đó thì sao?

Hệ thống báo "Ảnh đã được xử lý trước đó" và hiện kết quả cũ, không đọc lại. Ảnh trùng là ảnh giống hệt nội dung, không xét tên file. Xem [Tải lại ảnh đã tải trước đó](tac-vu/tai-lai-anh-da-tai-truoc-do.md).

## Muốn bắt hệ thống đọc lại một ảnh thì làm thế nào?

Ở trang Truyền Pháp Ảnh, khi ảnh bị báo trùng, bấm nút **"OCR lại"**. Hoặc mở báo cáo ở trang Xem / sửa report và bấm nút **"OCR lại"**, không cần chọn gì thêm. Xem [OCR lại báo cáo](tac-vu/ocr-lai-bao-cao.md).

## Trạng thái "can_kiem_tra" (Cần kiểm tra) nghĩa là gì?

Số liệu có thể sai: hai lần đọc ra số khác nhau, hoặc các số không khớp nhau về số học. Mở báo cáo, đọc hộp "Cảnh báo", so với ảnh và sửa nếu sai. Xem [Trạng thái](tham-chieu/trang-thai.md).

## Trạng thái "da_sua_tay" (Đã sửa tay) nghĩa là gì?

Đã có người lưu số liệu của báo cáo bằng tay ở trang Xem / sửa report. Dashboard dùng số đã sửa. Xem [Trạng thái](tham-chieu/trang-thai.md).

## Trạng thái "ok" nghĩa là gì?

Hai lần đọc khớp nhau và số học đúng. Báo cáo "ok" vẫn có thể có ghi chú nhẹ trong cảnh báo. Xem [Trạng thái](tham-chieu/trang-thai.md).

## Nhãn "Đã được thay" nghĩa là gì?

Đã có ảnh mới hơn cùng kỳ báo cáo, nên báo cáo này không còn hiện trên dashboard. Báo cáo vẫn được giữ ở Tàng Kinh Các để xem lại. Xem [Số nào được hiển thị](tham-chieu/so-lieu-nao-duoc-hien-thi.md).

## Vì sao số liệu bị đánh dấu cần kiểm tra, cảnh báo nghĩa là gì?

Hệ thống tự kiểm tra sau khi đọc: so hai lần đọc và kiểm tra các phép cộng, tỷ lệ. Mỗi chỗ không khớp thành một dòng cảnh báo. Xem [Cảnh báo số liệu](tham-chieu/canh-bao-so-lieu.md).

## Sửa số liệu bị OCR sai như thế nào?

Ở Tàng Kinh Các, mở báo cáo, bấm **"Xem / sửa số liệu"**. So từng ô với ảnh gốc bên trái, sửa ô sai, bấm **"Lưu"**. Trạng thái đổi thành "Đã sửa tay". Xem [Sửa số liệu bị đọc sai](tac-vu/sua-so-lieu-ocr-sai.md).

## Muốn thêm hoặc bớt một dòng số liệu thì làm sao?

Ở trang Xem / sửa report, bấm **"Thêm giá trị"** để thêm một dòng (loại bất thường, ngày công suất, Scanner), hoặc bấm **"Xóa dòng"** cạnh dòng thừa, rồi bấm **"Lưu"**. Xem [Thêm hoặc xóa dòng](tac-vu/them-xoa-dong-so-lieu.md).

## Lỡ sửa sai, muốn quay lại số hệ thống đọc ban đầu thì làm sao?

Ở trang Xem / sửa report, mục **"OCR Version"** liệt kê mọi lần đọc của ảnh. Bấm **"Dùng bản này"** ở lần đọc đúng. Xem [Quay về một lần đọc cũ](tac-vu/quay-ve-phien-ban-ocr.md).

## Hai người cùng sửa một báo cáo thì sao?

Người lưu trước thành công. Người lưu sau nhận lỗi "Report này vừa được sửa ở máy khác…", phần sửa chưa được lưu. Tải lại trang rồi sửa lại. Xem [lỗi này](loi/report-vua-duoc-sua-o-may-khac.md).

## Lưu số liệu báo lỗi "Sai schema" là sao?

Có ô bị gõ sai kiểu, ví dụ số có dấu chấm ngăn nghìn hoặc dấu %, hoặc ngày giờ sai dạng. Sửa lại ô đó rồi lưu. Xem [lỗi khi lưu số liệu](loi/du-lieu-sua-khong-hop-le.md).

## Xóa một báo cáo như thế nào?

Mở báo cáo ở trang Xem / sửa report, bấm **"Xóa report"**, xác nhận. Xóa là vĩnh viễn. Báo cáo cũ hơn đã bị thay không tự quay lại dashboard. Xem [Xóa báo cáo](tac-vu/xoa-bao-cao.md).

## Một ngày có nhiều ảnh trùng kỳ báo cáo thì số nào được hiển thị?

Không cộng. SCADA cùng dây chuyền cùng kỳ, hoặc Sorted / BCR rate cùng kỳ: dùng ảnh đọc xong sau cùng. Capacity: mỗi ngày dùng ảnh có ngày cuối khoảng truy vấn muộn hơn. Xem [Số nào được hiển thị](tham-chieu/so-lieu-nao-duoc-hien-thi.md).

## Vì sao không thấy dữ liệu của một ngày?

Có ba khả năng: ngày đó chưa có ảnh, ảnh đang xử lý, hoặc ngày đã quá 35 ngày nên bị xóa. Ngày không có dữ liệu hiện dấu "—", không phải 0. Kiểm tra ở Tàng Kinh Các.

## Dữ liệu được giữ bao lâu?

Báo cáo và ảnh: 35 ngày, tính theo ngày báo cáo. Cuộc trò chuyện với chatbot: xóa khi không dùng quá 30 ngày. Việc dọn chạy mỗi đêm lúc 2 giờ sáng, dữ liệu đã xóa không khôi phục được. Xem [Giới hạn và quy tắc](tham-chieu/gioi-han-va-quy-tac.md).

## Muốn xem biểu đồ công suất thì bấm vào đâu?

Trang **"Thiên Cơ Các"**, tab **"HT2 – DMWCS (CBS)"**, khung "Công suất AVG theo ngày". Công suất MAX của HT1 xem ở thẻ "Công suất MAX" và biểu đồ "So sánh 4 dây chuyền" của tab HT1. Xem [Xem công suất](tac-vu/xem-cong-suat-va-thoi-gian-su-dung.md).

## Lọc dashboard theo ngày như thế nào?

Ở đầu mỗi tab của trang Thiên Cơ Các, chọn ô **"Từ ngày"** và **"Đến ngày"**. Biểu đồ và bảng vẽ lại ngay, tối đa 35 ngày. Xem [Lọc theo ngày](tac-vu/loc-dashboard-theo-ngay.md).

## Lọc theo dây chuyền ở đâu?

Tab **"HT1 – SCADA"**, ô **"Dây chuyền"** ở hàng lọc đầu tab. HT2 không có lọc dây chuyền. Xem [Lọc theo dây chuyền](tac-vu/loc-theo-day-chuyen.md).

## Xem chỉ số của hôm qua thế nào?

Bấm vào cột của ngày hôm qua trên một biểu đồ theo ngày. Năm thẻ chỉ số đổi sang ngày đó. Xem [Xem chỉ số của một ngày](tac-vu/xem-chi-so-cua-mot-ngay.md).

## So sánh các dây chuyền ở đâu?

Tab HT1, khung **"So sánh 4 dây chuyền"**, chọn chỉ số ở ô góc trên bên phải khung. Xem [So sánh các dây chuyền](tac-vu/so-sanh-cac-day-chuyen.md).

## Scanner nào đọc mã vạch kém nhất xem ở đâu?

Tab HT2, khung **"Tỷ lệ đọc thành công của từng Scanner"**. Cần tải ảnh loại "DMWCS BCR rate". Xem [Tỷ lệ đọc của Scanner](tac-vu/xem-ty-le-doc-cua-scanner.md).

## REJECT gồm những gì?

HT1: "Không có mã vạch" + "Yêu cầu ống dẫn thất bại". HT2: RejectChute, gồm NoRead, NoPostOffice, NoChute. Xem [Thành phần REJECT](tac-vu/xem-thanh-phan-reject.md).

## CORRECT của HT2 có tính PDA không?

Có. CORRECT HT2 = CorrectChute + PDA, nên CORRECT + REJECT = ALL. Cột "trong đó PDA" của bảng cho biết phần PDA. Xem [Chỉ số HT2](tham-chieu/chi-so-ht2-dmwcs.md).

## Thời gian sử dụng tính thế nào?

HT1 = ALL / Công suất MAX, là ước tính, thời gian thực tế lớn hơn hoặc bằng. HT2 = ALL / Công suất AVG cùng ngày. Đơn vị giờ. Đây là thẻ trên dashboard Thiên Cơ Các. Muốn cộng giờ thật từ file Excel xuất từ máy thì dùng trang **"Đạo Vận Chi Lượng"**.

## Cộng cột thời gian (1h33m40s) trong file Excel ở đâu?

Trang **"Đạo Vận Chi Lượng"** trên menu. Kéo thả một hoặc nhiều file .xlsx, trang cộng cột F, chia theo thiết bị ở cột A và vẽ biểu đồ. Không cần đăng nhập. File không được lưu, tải lại trang là mất. Xem [Tính tổng thời gian từ file Excel](tac-vu/tinh-tong-thoi-gian-tu-file-excel.md).

## Xuất số liệu ra Excel được không?

Được. Bấm **"Xuất CSV"** ở góc trên bên phải bảng chi tiết của tab HT1 hoặc HT2. File mở được bằng Excel. Xem [Xuất CSV](tac-vu/xuat-bang-ra-csv.md).

## Tìm một ảnh đã tải lên ở đâu?

Trang **"Tàng Kinh Các"**, gõ một phần tên file vào ô "Truy tìm bí pháp". Lọc thêm theo ngày báo cáo và trạng thái được. Xem [Tìm báo cáo](tac-vu/tim-bao-cao.md).

## Xem ảnh gốc của một báo cáo ở đâu?

Ở Tàng Kinh Các, mở dòng báo cáo, bấm ảnh nhỏ để mở ảnh gốc. Trang Xem / sửa report cũng hiện ảnh gốc bên trái. Xem [Xem chi tiết báo cáo](tac-vu/xem-chi-tiet-bao-cao.md).

## Chatbot hỏi được gì?

Số liệu HT1, HT2 theo ngày, khoảng ngày, dây chuyền, Scanner; so sánh, xếp hạng, xu hướng; báo cáo cần kiểm tra. Không sửa dữ liệu, không dự báo, không giải thích nguyên nhân. Xem [Chatbot hỏi được gì](tham-chieu/chatbot-hoi-duoc-gi.md).

## Hỏi chatbot ở đâu?

Trang **"Vấn Đạo Đài"** trên menu, hoặc nút tròn hình bong bóng chat ở góc phải dưới các trang khác. Xem [Hỏi đáp với chatbot](tac-vu/hoi-dap-so-lieu-voi-chatbot.md).

## Xem bảng kết quả của chatbot ở đâu?

Trên trang Vấn Đạo Đài, dưới mỗi câu trả lời có bảng kết quả. Khung chat nhanh không hiện bảng; bấm "Xem bảng kết quả" để sang trang Vấn Đạo Đài.

## Xem lại lịch sử hỏi chatbot ở đâu?

Trang **"Vấn Đạo Đài"**, cột bên trái liệt kê mọi cuộc trò chuyện, chia theo "Hôm nay", "Hôm qua", "7 ngày qua", "30 ngày qua". Bấm một dòng để mở lại. Xem [Xem lịch sử hỏi đáp](tac-vu/xem-lich-su-hoi-dap.md).

## Có xem lịch sử chat trên máy khác được không?

Được. Cả chi nhánh dùng chung tài khoản nên danh sách lịch sử ở trang Vấn Đạo Đài là chung cho mọi máy. Mỗi máy vẫn mở một cuộc trò chuyện riêng, không lẫn vào nhau. Tải lại trang để thấy cuộc máy khác vừa tạo.

## Tại sao chatbot báo "Hỏi nhanh quá"?

Đã hỏi 10 câu trong 1 phút. Chờ số giây ghi trong thông báo rồi hỏi tiếp. Xem [lỗi Hỏi nhanh quá](loi/hoi-nhanh-qua.md).

## Tại sao chatbot báo "Đã hết lượt hỏi miễn phí"?

Dịch vụ AI của chatbot đã hết lượt dùng chung của cả chi nhánh. Chờ số phút ghi trong thông báo. Xem [lỗi này](loi/het-luot-hoi-mien-phi.md).

## Tại sao chatbot nói "Mình chưa trả lời được câu này"?

Câu hỏi chưa rõ. Hỏi lại đủ hệ thống, chỉ số và ngày, ví dụ "Tỷ lệ REJECT HT2 ngày 12/11". Xem [lỗi này](loi/chatbot-chua-tra-loi-duoc.md).

## Chatbot nói "chưa có dữ liệu" nghĩa là sao?

Khoảng ngày hỏi chưa có ảnh nào được đọc. Chatbot không bao giờ coi ngày thiếu là 0, và thường gợi ý ngày gần nhất có dữ liệu. Xem [Cảnh báo của chatbot](tham-chieu/canh-bao-cua-chatbot.md).

## Chatbot có sửa được số liệu không?

Không. Chatbot chỉ đọc dữ liệu. Muốn sửa: trang Tàng Kinh Các, mở báo cáo, bấm "Xem / sửa số liệu".

## Bắt đầu cuộc trò chuyện mới với chatbot thế nào?

Trên trang Vấn Đạo Đài, bấm **"+ Cuộc trò chuyện mới"** trên cùng cột trái. Cuộc trò chuyện cũ vẫn nằm trong danh sách để mở lại. Xem [Cuộc trò chuyện mới](tac-vu/bat-dau-cuoc-tro-chuyen-moi.md).

## Câu hỏi cho chatbot dài tối đa bao nhiêu?

1000 ký tự. Ô nhập không cho gõ dài hơn.

## Gặp lỗi không tự xử lý được thì liên hệ ai?

Xem mục **"Gặp Kiếp Nạn"** ở chân trang, có tên người phụ trách và email hỗ trợ. Gửi kèm ảnh chụp màn hình thông báo lỗi.
