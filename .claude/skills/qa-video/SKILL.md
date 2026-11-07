---
name: qa-video
description: Kiểm tra video final Fix Your Foundation trước khi giao (kỹ thuật, nội dung, chữ, tiếng). Dùng sau khi dung-video chạy xong bước final.
---
# QA video

1. **Kỹ thuật** (`ffprobe`): 1080×1920, 30fps, h264 + aac, thời lượng = tổng edl (±0,1s). Không khung đen ở đầu/cuối.
2. **Hình**: xem `final_sheet.jpg` + trích 1 khung ở **mỗi điểm cắt** (±0,2s). Không khung nhoè/rung mạnh, không giật ngược, không lộ viền đen khi zoom, màu không quá vàng.
3. **Chữ** (kiểu `noi`): khung ở 6–8 mốc — chữ không che mặt, không tràn mép (≤ 980px), đúng chính tả, dấu tiếng Việt đủ, hook hiện ngay từ giây đầu, chữ khớp lời (lệch ≤ 0,15s).
4. **Tiếng**: `ffmpeg -af ebur128` — kiểu `voice` ≈ −14 LUFS, đỉnh ≤ −1 dB; nghe-đọc lại bằng ASR nhanh (`ASR_MODEL=small`) trên final: không mất chữ đầu/cuối câu, không câu lặp.
5. **Nội dung**: đủ 7 nhịp như script, số liệu đúng script, còn **[xác nhận]** nào chưa được chủ kênh trả lời thì báo.
6. Ghi kết quả 1 dòng vào `log` bản đồ + `BOARD.md` ("QA đạt" hoặc liệt kê lỗi). Lỗi → sửa ở `dung-video` rồi QA lại.
