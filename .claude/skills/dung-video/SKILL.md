---
name: dung-video
description: Agent Dựng video — từ script đã sửa, voice và video quay chủ kênh up lên Drive, dựng video dọc 9:16 (cảnh theo thứ tự quay), đồ hoạ, phụ đề từng cụm chữ. Dùng khi chủ kênh báo đã up voice / source, hoặc muốn sửa video đã dựng.
---

# Dựng video

Đọc `style/edit-style.md` trước. Chạy `bash setup.sh` nếu phiên mới. Lệnh chính: `bash pipeline/make_video.sh projects/<slug> [bước]`.

## 0. Đọc script đã sửa
Đọc mục của video này trong Doc "Script đợt DD/MM" chủ kênh đã sửa (Drive `read_file_content`), cập nhật `script.md`. Hook trong Doc là tiêu đề màn hình từ 0s; giữ Caption đăng để gửi kèm video final.

## 1. Điền project.json
Tìm file trong thư mục video (`drive_folder` trong project.json) bằng Drive `search_files` (`parentId = '<folder>'`, **đi hết các trang** `nextPageToken`): file `audio/*` là voice, file `video/*` là source. Ghi tên + `drive_id` vào `voice` và `sources`. File phải chia sẻ "Anyone with the link" thì `drive_fetch.sh` mới tải được.

## 2. `fetch` rồi `asr`
`asr` tạo `transcript.json`. Đối chiếu với script, viết **`lines.txt`**: đúng số dòng = số segment, mỗi dòng là lời *thực sự* được nói, đã sửa chính tả (Whisper hay nghe nhầm từ đồng âm và thuật ngữ tiếng Anh). Chỉ sửa chính tả, không đổi lời.

## 3. `probe` rồi viết `edl.txt`
Xem contact sheet từng source (Read ảnh `work/<slug>/thumbs/*.jpg`). Viết `edl.txt`: `n source start dur zoom`.
- Sắp clip **theo thời gian quay** (`ffprobe -show_entries format_tags=creation_time`), mỗi clip một dòng chạy liền, không cắt xen kẽ.
- Tổng `dur` = độ dài voice (lệch < 0.05s). Điểm chuyển clip trùng ranh giới câu trong transcript; dư thì bỏ đầu/cuối clip.
- Không vượt quá độ dài source. Zoom = 1 cho mọi clip.

## 4. `seg`
Cắt từng clip (nhanh, không làm đẹp). Nếu chủ kênh up nhiều video, dựng **lần lượt từng video** cho xong rồi mới sang video sau.

## 5. Viết `graphics.py` rồi `gfx`
Copy `projects/_mau/graphics.vi-du.py` làm mẫu (sửa đường dẫn transcript/lines cho video hiện tại). Mỗi câu/ý có một thẻ đồ hoạ; thời điểm lấy từ word timestamps (in nhanh: `python3 -c "import json;[print(i,' '.join(f\"{w['w'].strip()}@{w['s']:.1f}\" for w in s['words'])) for i,s in enumerate(json.load(open('transcript.json')))]"`).
Xem thử trước khi render hết: `python3 graphics.py work/<slug>` rồi `node pipeline/gfx/render.js work/<slug>/overlay.html <dir> times 3,12,30` và ghép lên `base.mp4` để nhìn (không che mặt, chữ hiển thị đủ dấu).

## 6. `final`
Ra `work/<slug>/final.mp4` + `final_sheet.jpg`. Chuyển cho agent `qa-video`. Đạt thì up lên "Final Video": `bash pipeline/drive_upload.sh work/<slug>/final.mp4 "Video NN - <tên>.mp4"`. Nếu chưa cấu hình rclone (thiếu `RCLONE_DRIVE_TOKEN`), gửi file cho chủ kênh trong chat và nhắc mục "Tự up video final" trong HUONG-DAN.md. Gửi kèm Caption đăng từ Doc script. Chỉ up **1 file final** cho mỗi video (không up bản nháp, contact sheet hay bản cũ).

Cập nhật bản đồ 3D (xem CLAUDE.md: `videos` stage 4 khi bắt đầu dựng, stage 5 + `state: done` + `finalUrl` khi xong; thêm dòng `log`) và `BOARD.md` sau mỗi bước lớn.
