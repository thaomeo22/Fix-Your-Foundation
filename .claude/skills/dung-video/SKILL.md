---
name: dung-video
description: Dựng video Fix Your Foundation từ clip chủ kênh up lên Drive (talking-head có tiếng + chữ động, hoặc montage cảnh thao tác). Dùng khi chủ kênh nói "Video NN đã up", gửi link thư mục Drive có clip, hoặc nhờ edit thử các video.
---
# Dựng video

Đọc trước: `studio.json`, `style/edit-style.md`, `projects/<slug>/project.json`. Chạy `bash setup.sh` nếu chưa chạy trong phiên.
Lệnh chung: `bash pipeline/make_video.sh projects/<slug> <bước>`.

## 1. Lấy nguồn
- `search_files` với `parentId = '<id thư mục>'`, đi hết `nextPageToken`. Ghi mọi video vào `sources` (tên file → id), ảnh vào `assets`.
- Xác định `kieu`: clip có người nói vào máy → `noi`; chỉ cảnh thao tác/không lời → `montage` (`audio: ambient`). Chủ kênh nói rõ thì theo lời chủ kênh.
- Bước `fetch` (thư mục phải "Anyone with the link"; lỗi 403 → nhắc chủ kênh).

## 2. Xem nguồn
- Contact sheet mỗi clip có mốc giờ: `ffmpeg -skip_frame nokey -i src/X -vf "fps=1/<bước>,scale=180:-1,drawtext=text='%{pts\:hms}':…,tile=8x3"`. Xem hết.
- Kiểu `noi`: bước `takes` → đọc `projects/<slug>/takes.txt` (mỗi câu: clip, vào, ra, lời).

## 3a. edl.txt — kiểu `noi`
- Đi theo thứ tự câu trong Doc script (chủ kênh đã sửa). Mỗi câu lấy **take cuối nói trơn**; vào = từ đầu − 0,08s, ra = từ cuối + 0,12s.
- Đổi góc / punch-in theo `edit-style.md`; b-roll bằng `cover=`.
- Chạy `cut`, xem bảng timeline in ra: không câu nào thiếu/lặp, không lặng > 0,3s.

## 3b. edl.txt — kiểu `montage`
- Thứ tự = **thứ tự tên file** (sắp theo số). Mỗi clip 1 đoạn 2–3s (thành phẩm cuối 3s).
- Chấm điểm: `python3 -I pipeline/best_frames.py work/<slug>/src/<clip> 2.5` → 4 điểm bắt đầu tốt nhất.
- Xuất 3 khung (đầu/giữa/cuối) của 2–3 ứng viên mỗi clip thành 1 ảnh lưới, **xem và chốt** đoạn: rõ sản phẩm/móng, tay không che, máy yên. Ghi lý do chọn sau `#` trong edl.
- Chạy `cut`.

## 4. Chữ động (chỉ kiểu `noi`)
- `lines.txt`: 1 dòng / 1 đoạn edl, sửa chính tả theo script, thêm đánh dấu (`** __ !! (( // |`) theo `edit-style.md`.
- `graphics.py` (mẫu: `projects/_mau/graphics.py`): `captions(y=…, hide=…)`, `title_card` (từ `studio.json` → `series`), `card`/`counter`/`img` cho nhịp 5–6. Dùng `C.t("từ khoá")` để lấy mốc thời gian.
- Xem thử nhanh: `node pipeline/gfx/render.js work/<slug>/overlay.html <dir> times 1.5,8,20` rồi chồng lên `base.mov`.
- Chạy `gfx`.

## 5. Final
- Chạy `final` → `work/<slug>/final.mp4` + `final_sheet.jpg`. Gọi skill `qa-video`.
- Giao: `pipeline/drive_upload.sh work/<slug>/final.mp4 "Video NN - <tên>.mp4"` nếu có `RCLONE_DRIVE_TOKEN`; không thì gửi file trong chat (SendUserFile) kèm caption đăng.
- Bản đồ: stage 5 (state done khi đã giao), log, `BOARD.md`. Commit `project.json`, `edl.txt`, `lines.txt`, `graphics.py` (không commit media).
- Chủ kênh góp ý → sửa đúng bước, chạy lại từ bước đó, **ghi góp ý vào `style/edit-style.md`**.
