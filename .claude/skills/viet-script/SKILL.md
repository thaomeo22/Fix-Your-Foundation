---
name: viet-script
description: Viết script Fix Your Foundation cho cả đợt từ Doc ý tưởng đã có transcript, tạo 1 Doc "Script đợt DD/MM" và thư mục "Video NN - <tên>" trên Drive. Dùng khi chủ kênh nói "đã dán transcript", "viết script".
---
# Viết script

1. Đọc `studio.json`, `style/script-style.md`, `style/quay-style.md`. Đọc Doc ý tưởng của đợt (chỉ những video chủ kênh đã duyệt + có transcript).
2. Mỗi video: rút gọn transcript gốc theo **khung 7 nhịp**, 45–60s (≈ 180–230 chữ tiếng Việt). Viết lại bằng giọng chủ kênh; **mỗi câu 1 dòng** trong "Script ghi âm".
3. Kiểm tra nguồn: mọi số liệu phải mở được link và khớp con số (WebSearch/WebFetch). Không kiểm được → bỏ hoặc đổi số. Ghi **Nguồn** cuối mục.
   Câu về trải nghiệm chủ kênh chưa có trong `studio.json`/Doc → **[xác nhận]**.
4. Mỗi video thêm **Bảng góc quay**: nhịp → góc (A–E trong `quay-style.md`) + ảnh chụp màn hình cần cho thẻ dữ liệu.
5. Tạo **1** Doc `Script đợt DD/MM` trong `drive.ke_hoach`, mỗi video 1 mục Heading 1 "Video NN — <tên>" (Hook · Script ghi âm · Caption đăng · Bảng góc quay · Độ dài · Nguồn).
6. Tạo thư mục trống `Video NN - <tên>` trong `drive.goc` cho mỗi video. Tạo `projects/NN-<slug>/project.json`: `{n, title, kieu: "noi", audio: "voice", drive_folder, sources: {}, assets: {}}`.
7. Bản đồ: stage 2, note "chờ chủ kênh sửa script + quay". Log + `BOARD.md`. Gửi link Doc + nhắc đọc `quay-style.md` (gửi nội dung trong chat).
