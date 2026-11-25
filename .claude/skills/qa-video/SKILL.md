---
name: qa-video
description: Agent QA-QC — kiểm tra video final trước khi giao cho chủ kênh (độ dài, khung hình, phụ đề, âm thanh, đồ hoạ). Dùng sau khi dựng xong hoặc khi chủ kênh báo lỗi video.
---

# QA video

Chạy và ghi kết quả (đạt / lỗi + cách sửa) vào nhật ký (bản đồ 3D `log` + `BOARD.md`):

1. **Thông số**: `ffprobe` → 1080×1920, 30fps, độ dài = voice (lệch < 0.1s), có audio AAC.
2. **Khung đen / đứng hình**: `ffmpeg -i final.mp4 -vf blackdetect=d=0.2,freezedetect=d=1.5 -f null -` không có cảnh báo.
3. **Âm lượng**: `ffmpeg -i final.mp4 -af ebur128 -f null -` → Integrated ≈ −14 LUFS (±1.5), True peak ≤ −1 dB.
4. **Nhìn**: Read `final_sheet.jpg` + 6–8 khung ở thời điểm có đồ hoạ: không che mặt, không tràn mép, chữ hiển thị đủ dấu.
5. **Phụ đề**: so `lines.txt` với script — không sót câu, không lỗi chính tả, số liệu khớp nguồn.
6. **Nội dung**: không còn câu **[xác nhận]** chưa được chủ kênh duyệt.

Lỗi nào sửa được thì quay lại bước tương ứng của `dung-video` (vd chỉ chạy lại `gfx` + `final`).
