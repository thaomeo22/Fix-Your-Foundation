# Câu lệnh khởi tạo xưởng

**Chủ kênh:** sau khi làm xong các bước 1–5 trong `HUONG-DAN.md`, mở một phiên Claude Code mới với repo của bạn rồi dán nguyên câu dưới đây:

```
Đọc KHOI-TAO.md và khởi tạo xưởng video cho tôi.
```

---

## Hướng dẫn cho Claude (làm lần lượt, hỏi chủ kênh từng nhóm câu, đừng hỏi dồn một lúc)

1. **Kiểm tra môi trường.** Chạy `bash setup.sh`. Thử tải danh sách 1 kênh YouTube bất kỳ bằng yt-dlp và thử Drive `search_files`. Thiếu domain hay thiếu connector thì chỉ rõ cho chủ kênh cần thêm gì (xem HUONG-DAN.md bước 4–5) rồi dừng.
2. **Hỏi về xưởng** (dùng AskUserQuestion khi có lựa chọn rõ ràng):
   - Tên xưởng, lĩnh vực / chủ đề chính, ngôn ngữ video.
   - Chủ kênh là ai (nghề nghiệp, kinh nghiệm, điều làm họ đáng tin) và xưng hô ("mình – bạn", "tôi – các bạn"…).
   - 1–3 kênh YouTube mẫu để lấy chủ đề.
   - Có Google Sheet / Doc chứa script cũ không (để học giọng văn và tránh trùng)? Có video mẫu muốn bắt chước kiểu dựng không?
   - Độ dài video mong muốn, hashtag hay dùng.
3. **Học giọng văn.** Nếu có script cũ: đọc, rút ra cấu trúc hook, cách mở bài, cách chia ý, độ dài → viết lại `style/script-style.md` (giữ khung 3 phần Hook · Script ghi âm · Caption đăng). Nếu có video mẫu kiểu dựng: xem vài khung hình (ffmpeg contact sheet) → chỉnh `style/edit-style.md` và màu/font trong `pipeline/gfx/lib.py` nếu cần (font phải hỗ trợ ngôn ngữ video; tải qua npm `@fontsource/*` trong `setup.sh`).
4. **Tạo Drive** (chỉ thư mục, không tạo Doc nào): thư mục gốc `<Tên xưởng>`, bên trong `00 Kế hoạch` và `Final Video`. Nhắc chủ kênh đặt thư mục gốc ở chế độ "Anyone with the link".
5. **Ghi `studio.json`** (copy từ `studio.example.json`) với mọi câu trả lời và id thư mục.
6. **Tạo bản đồ 3D.** Copy `docs/ban-do-3d.html`, thay `{{TEN_XUONG}}` bằng tên xưởng, publish bằng tool Artifact với
   `capabilities: {"db": {"rules": [{"path": "videos", "read": "view", "write": "admin"}, {"path": "log", "read": "view", "write": "admin"}]}}`.
   Ghi link vào `studio.json` → `ban_do_url`. Thêm 1 dòng `log` "Khởi tạo xưởng".
7. **Tạo `BOARD.md`** (bảng trạng thái trống + nhật ký), commit và push lên nhánh chính.
8. **Báo chủ kênh**: link thư mục Drive, link bản đồ 3D, và câu nói để bắt đầu: "Tìm 7 chủ đề cho tuần này".
