---
id: report-vua-duoc-sua-o-may-khac
title: Lỗi "Report này vừa được sửa ở máy khác. Tải lại trang để xem bản mới rồi sửa lại."
loai: loi
trang: Xem / sửa report
he_thong: chung
aliases: [hai người cùng sửa, xung đột khi lưu, sửa cùng lúc, không lưu được vì máy khác, conflict]
lien_quan: [sua-so-lieu-ocr-sai, them-xoa-dong-so-lieu, quay-ve-phien-ban-ocr, gioi-han-va-quy-tac]
nguon_code: [frontend/js/report.js, backend/app/api/reports.py]
cap_nhat: 2026-11-20
---
# Lỗi "Report này vừa được sửa ở máy khác. Tải lại trang để xem bản mới rồi sửa lại."

Còn gọi là: hai người cùng sửa, sửa cùng lúc, "lưu không được vì máy khác".

**Xuất hiện ở:** trang **Xem / sửa report**, chữ đỏ cạnh nút **"Lưu"**, sau khi bấm **"Lưu"** hoặc **"Dùng bản này"** (mục OCR Version).

**Nghĩa là:** từ lúc bạn mở trang tới lúc bấm Lưu, đã có người khác (hoặc chính bạn ở tab khác) lưu báo cáo này. Hệ thống không ghi đè lên bản của người kia, nên phần sửa của bạn **chưa được lưu**.

**Nguyên nhân thường gặp:**
- Hai người cùng mở một báo cáo "Cần kiểm tra" để sửa.
- Mở cùng báo cáo ở hai tab trình duyệt, đã lưu ở tab kia.
- Để trang mở lâu, trong lúc đó người khác đã sửa.

**Cách xử lý:**
1. Ghi lại các số bạn vừa sửa (chép ra giấy hoặc Notepad), vì tải lại trang sẽ mất phần chưa lưu.
2. Tải lại trang (F5). Trang hiện bản mới nhất của người kia.
3. Xem bản mới đã đúng chưa. Nếu còn sai, sửa lại và bấm **"Lưu"**.

**Nếu vẫn lỗi:** báo lỗi lặp lại liên tục dù đã tải lại trang thì có người khác đang sửa liên tục. Thống nhất với đồng nghiệp ai sửa báo cáo này. Vẫn không được thì báo người hỗ trợ ở mục **"Gặp Kiếp Nạn"** cuối trang.
