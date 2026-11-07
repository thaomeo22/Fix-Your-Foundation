# Xưởng video tự động

Đội agent sản xuất video ngắn dọc 9:16. **Mọi thông tin riêng của xưởng nằm trong `studio.json`** (tên xưởng, lĩnh vực, chủ kênh, kênh mẫu, ngôn ngữ, id thư mục Drive, link bản đồ). Đọc file đó trước mọi việc. Nói chuyện với chủ kênh bằng ngôn ngữ trong `studio.json` (`language`).

Nếu `studio.json` chưa có hoặc còn trống: làm theo `KHOI-TAO.md` trước.

## Quy trình

**Quy tắc: mỗi công đoạn chỉ tạo 1 file.** Không tạo file phụ, bản nháp, bản sao hay Doc trung gian trên Drive.

```
Nghiên cứu ─> 1 Doc "Đợt DD/MM — Ý tưởng & transcript" trong 00 Kế hoạch (mọi ý tưởng của đợt + chỗ dán transcript)
  ─> [CHỦ KÊNH duyệt ý tưởng, dán transcript vào chính Doc đó]
  ─> Viết script ─> 1 Doc "Script đợt DD/MM" trong 00 Kế hoạch, mỗi video một mục Heading 1 (Hook · Script ghi âm · Caption đăng)
     + tạo thư mục trống "Video NN - <tên>" cho mỗi video
  ─> [CHỦ KÊNH sửa Doc script một lượt, thu voice, up voice + video quay vào thư mục "Video NN"]
  ─> Dựng video (lần lượt từng video, cảnh theo thứ tự quay) ─> QA ─> up vào "Final Video" ─> [CHỦ KÊNH tự đăng]
```

### Cấu trúc Drive (id trong `studio.json` → `drive`)
```
<Tên xưởng>/                       drive.goc
  00 Kế hoạch/                     drive.ke_hoach     — mỗi đợt: 1 Doc ý tưởng & transcript + 1 Doc script
  Final Video/                     drive.final_video  — 1 file video final cho mỗi video
  Video NN - <tên>/                id ghi trong projects/<slug>/project.json (`drive_folder`)
    <voice>, <video quay>          chủ kênh up (Claude không tạo file nào ở đây)
```
Công cụ Google Drive chỉ **tạo** file/thư mục và **đọc** nội dung, không sửa được Doc có sẵn. Cần sửa thì nhờ chủ kênh sửa hoặc gửi nội dung trong chat — không tạo Doc mới để thay thế. Tìm file trong thư mục: `search_files` với `parentId = '<id>'`, đi hết `nextPageToken`.

| Agent (skill) | Việc | Đầu ra |
|---|---|---|
| `nghien-cuu` | Chọn chủ đề từ kênh mẫu, tránh trùng chủ đề đã làm | Doc ý tưởng & transcript |
| `viet-script` | Rút gọn video mẫu thành script theo style xưởng, kiểm tra nguồn | Doc script của đợt |
| `dung-video` | Script đã sửa + voice + video quay → video final: cảnh theo thứ tự quay, đồ hoạ, phụ đề | `work/<slug>/final.mp4` |
| `qa-video` | Kiểm tra trước khi giao | Kết quả vào nhật ký |

Mỗi khi một bước xong, cập nhật:
1. **Bản đồ 3D** (`studio.json` → `ban_do_url`) bằng tool `ArtifactData`:
   - Collection `videos`, doc id = số video (`"03"`): `{n, title, stage, state, note, scriptUrl, folderUrl, finalUrl}`.
     `stage` 0–5 = Nghiên cứu · Viết script · Chủ kênh sửa script · Up lên Drive · Dựng video · Final; `state` = `active` | `paused` | `done`; `note` = 1 câu "đang chờ gì". Sửa bằng `update` kèm `if_version`.
   - Collection `log`: mỗi việc xong thêm 1 doc (id = thời điểm, vd `2026-10-27T09-15`): `{ts (ISO), date, agent, text}`.
2. **`BOARD.md`** trong repo (bản lưu trữ).

## Quy tắc chung
- Không bịa trải nghiệm cá nhân của chủ kênh. Câu kể chuyện riêng chưa chắc đúng → đánh dấu **[xác nhận]**.
- Mọi số liệu / nghiên cứu trong script phải có nguồn kiểm tra được, ghi ở cuối mỗi script.
- Video final: dài đúng bằng voice, 1080×1920, 30fps.
- Không đưa tên model AI vào commit, file hay video.
- File media không commit — để trong `work/` (đã gitignore).
- Style: `style/script-style.md`, `style/edit-style.md`. Chủ kênh góp ý gì thì ghi luôn vào file style để lần sau tự làm đúng.

## Môi trường
- Chạy `bash setup.sh` đầu mỗi phiên.
- Network cần cho phép: `drive.usercontent.google.com`, `drive.google.com`, `huggingface.co`, `cdn-lfs.huggingface.co`, `cas-bridge.xethub.hf.co`, `youtube.com`, `www.youtube.com` (+ `www.googleapis.com`, `oauth2.googleapis.com` nếu tự up video final).
- Công cụ Drive chỉ tải/đẩy file ≤ 10 MB → file lớn tải bằng `pipeline/drive_fetch.sh` (thư mục phải chia sẻ "Anyone with the link"). Up video final: `pipeline/drive_upload.sh` (cần biến môi trường `RCLONE_DRIVE_TOKEN`); chưa có thì gửi file cho chủ kênh trong chat.
- YouTube chặn tải transcript từ máy chủ cloud → nhờ chủ kênh dán transcript. Không cố lách cơ chế chống bot.
