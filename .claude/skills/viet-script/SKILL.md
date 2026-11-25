---
name: viet-script
description: Agent Viết script — đọc transcript chủ kênh dán, rút gọn mỗi video gốc thành script ngắn theo style xưởng (Hook · Script ghi âm · Caption đăng), kiểm tra nguồn, gộp cả đợt vào 1 Doc. Dùng khi chủ kênh báo đã dán transcript.
---

# Viết script

1. Đọc `studio.json`, `style/script-style.md` và 1 script mẫu trong `projects/` nếu có.
2. Đọc Doc "Đợt DD/MM — Ý tưởng & transcript" (Drive `read_file_content`; kết quả lớn bị lưu ra file thì đọc bằng `jq -r .fileContent`). Chủ kênh có thể đã sửa hook/góc trong Doc — làm theo bản sửa.
3. Kiểm tra trùng: so đoạn mở đầu transcript với các chủ đề đã làm. Trùng thì tạm dừng video đó (bản đồ: `state: paused`) và báo chủ kênh.
4. Với mỗi video: chọn 3–4 ý mạnh nhất, bỏ tài trợ / quảng cáo / chuyện riêng của tác giả gốc. Chọn 1 nghiên cứu hoặc số liệu mở màn và **kiểm tra bằng WebSearch** (tác giả, năm, con số); không xác minh được thì bỏ hoặc nói chung chung.
5. Viết đúng 3 phần **Hook / Script ghi âm / Caption đăng** theo `style/script-style.md`. Câu chuyện cá nhân chưa chắc → **[xác nhận]**.
6. Lưu từng script vào `projects/video-NN-<slug>/script.md` + `project.json` (`{title, drive_folder, voice:{}, sources:{}, asr_prompt}`).
7. **Chỉ tạo 1 Doc** cho cả đợt: "Script đợt DD/MM (video NN–MM)" trong `drive.ke_hoach`, mỗi video một mục Heading 1. Tạo thư mục trống `Video NN - <tên ngắn>` trong `drive.goc` cho từng video, ghi id vào `project.json`.
8. Cập nhật bản đồ 3D (`videos` stage 2 + `scriptUrl` + `folderUrl`; 1 dòng `log`) và `BOARD.md`. Gửi link Doc cho chủ kênh.
