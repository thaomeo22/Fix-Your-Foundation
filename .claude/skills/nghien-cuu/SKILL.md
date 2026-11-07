---
name: nghien-cuu
description: Tìm chủ đề video Fix Your Foundation cho một đợt từ kênh mẫu, tránh trùng, tạo 1 Doc "Đợt DD/MM — Ý tưởng & transcript". Dùng khi chủ kênh nói "tìm N chủ đề", "lên ý tưởng tuần này".
---
# Nghiên cứu chủ đề

1. Đọc `studio.json` (lĩnh vực, kênh mẫu, chủ kênh), `style/script-style.md`, `BOARD.md` + danh sách `projects/` (chủ đề đã làm).
2. Lấy danh sách video mới của từng kênh mẫu: `yt-dlp --flat-playlist --print "%(id)s\t%(view_count)s\t%(duration)s\t%(title)s" <url> | head -60`. Chỉ lấy video ≤ 90s hoặc có thể rút gọn thành 45–60s.
3. Chọn N chủ đề hợp **khung 7 nhịp** (cần: 1 niềm tin sai phổ biến để làm hook + 1 số liệu kiểm chứng được + chỗ cho kết quả cá nhân của chủ kênh). Ưu tiên lượt xem cao so với trung bình kênh. Loại chủ đề trùng (so cả ý chính, không chỉ tiêu đề).
4. Tạo **1** Google Doc trong `drive.ke_hoach`, tên `Đợt DD/MM — Ý tưởng & transcript`. Mỗi ý tưởng 1 mục Heading 1 "Video NN — <tên>":
   - Link video gốc, lượt xem, vì sao chọn.
   - Hook dự kiến (nhịp 1) + niềm tin sai bị lật.
   - Số liệu dự kiến + nguồn cần tìm.
   - Câu hỏi cho chủ kênh: trải nghiệm/con số cá nhân nào dùng được ở nhịp 6.
   - Dòng trống "**Dán transcript ở đây:**".
5. Đánh số video NN tiếp nối số lớn nhất đã có.
6. Cập nhật bản đồ (`videos/NN`: stage 0, state active, note "chờ chủ kênh duyệt + dán transcript") + 1 dòng `log`, và `BOARD.md`. Gửi link Doc cho chủ kênh.

YouTube chặn tải transcript từ cloud → không cố lách, nhờ chủ kênh dán.
