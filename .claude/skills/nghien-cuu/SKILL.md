---
name: nghien-cuu
description: Agent Nghiên cứu — đề xuất một đợt chủ đề video từ các kênh mẫu trong studio.json, tránh trùng chủ đề đã làm, tạo 1 Doc ý tưởng & transcript. Dùng khi chủ kênh hỏi "làm video gì tiếp", "tìm chủ đề cho tuần", hoặc bắt đầu đợt mới.
---

# Nghiên cứu chủ đề

1. Đọc `studio.json` (lĩnh vực, kênh mẫu, ngôn ngữ) và `style/script-style.md`.
2. Lấy danh sách video từng kênh mẫu (không cần đăng nhập):
   `python3 -m yt_dlp --flat-playlist --print "%(id)s | %(title)s | %(view_count)s" "<url kênh>/videos"` (`pip install yt-dlp` nếu thiếu).
   YouTube đòi đăng nhập khi lấy transcript từ máy chủ cloud: **không lách**, nhờ chủ kênh dán transcript.
3. Loại chủ đề đã làm: thư mục `projects/`, `BOARD.md`, và Content plan nếu `studio.json` có `content_plan_sheet_id`.
4. Chọn số chủ đề chủ kênh yêu cầu (mặc định 7 = 1 tuần), ưu tiên đúng lĩnh vực, nhiều lượt xem, hợp với cảnh chủ kênh quay được.
5. **Chỉ tạo 1 file**: Doc **"Đợt DD/MM — Ý tưởng & transcript"** trong `drive.ke_hoach` (HTML → `create_file`, `contentMimeType: text/html`). Mỗi video một mục Heading 2: số NN (tiếp theo số lớn nhất trong `projects/`), hook nháp, góc rút gọn, link video gốc, chỗ trống "(dán transcript ở đây)". Không tạo thư mục video ở bước này.
6. Thêm các video vào bản đồ 3D (`videos`, stage 0, state active) và 1 dòng `log`; ghi `BOARD.md`.
7. Nhờ chủ kênh duyệt ý tưởng và dán transcript vào chính Doc đó.
