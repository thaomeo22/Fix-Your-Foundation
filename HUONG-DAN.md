# Xây xưởng video tự động của riêng bạn

Bộ khung này biến Claude Code thành một đội làm video ngắn (dọc 9:16) cho **bất kỳ lĩnh vực nào**: tài chính, nấu ăn, học tập, sức khoẻ, công nghệ… Bạn chỉ làm 3 việc: **duyệt ý tưởng, sửa script một lượt, thu voice + quay cảnh**. Phần còn lại Claude làm.

```
1 Nghiên cứu      Claude  quét kênh mẫu → 1 Doc ý tưởng cho cả đợt (vd 7 video/tuần)
2 Viết script     Claude  đọc transcript bạn dán → 1 Doc script, mỗi video: Hook · Script ghi âm · Caption đăng
3 Sửa script      Bạn     sửa thẳng trên Doc, một lượt
4 Up nguyên liệu  Bạn     thu voice + quay cảnh → up vào thư mục "Video NN" trên Drive
5 Dựng video      Claude  nhận dạng voice, ghép cảnh theo thứ tự quay, đồ hoạ, phụ đề, kiểm tra
6 Final           Bạn     lấy video ở thư mục "Final Video" (hoặc trong chat), tự đăng
```
Tiến độ hiện trên **bản đồ 3D** (thị trấn nhỏ có 6 trạm, số video chờ ở từng trạm, nhật ký việc), cập nhật trực tiếp.

---

## Bước 1 — Chuẩn bị tài khoản
- **Claude** gói có Claude Code trên web (claude.ai/code).
- **GitHub** (miễn phí): github.com.
- **Google Drive** (tài khoản Google bất kỳ).

## Bước 2 — Đưa bộ khung lên GitHub
1. Giải nén file zip, bạn có thư mục `xuong-video`.
2. Vào https://github.com/new → đặt tên repo (vd `xuong-video-cua-toi`) → chọn **Private** → **Create repository**.
3. Trong trang repo vừa tạo, bấm **uploading an existing file** → kéo **toàn bộ nội dung bên trong** thư mục `xuong-video` vào (không kéo chính thư mục đó) → **Commit changes**.
   - Bộ khung có thư mục ẩn `.claude` và file `.gitignore`. Trên Mac bấm `Cmd + Shift + .` trong Finder để hiện file ẩn; trên Windows bật "Hidden items" trong File Explorer. Thiếu `.claude` thì Claude sẽ không có 4 agent.

## Bước 3 — Kết nối GitHub và Google Drive với Claude
1. Vào https://claude.ai/connect-github → đăng nhập GitHub → khi được hỏi cài **Claude GitHub App**, chọn **Only select repositories** → tích repo vừa tạo → **Install**.
2. Vào claude.ai → **Settings → Connectors** → bật **Google Drive** và đăng nhập tài khoản Google sẽ chứa video.

## Bước 4 — Tạo môi trường cloud
Trong claude.ai/code, mở menu môi trường (góc thanh tiêu đề) → tạo mới hoặc **Edit** → **Network access** → **Allowed domains**, thêm:
```
drive.usercontent.google.com
drive.google.com
huggingface.co
cdn-lfs.huggingface.co
cas-bridge.xethub.hf.co
youtube.com
www.youtube.com
```
Giữ nguyên ô "Allow package managers" (để cài thư viện từ pypi và npm).

## Bước 5 — Mở phiên và khởi tạo
1. Bấm phiên mới, chọn môi trường ở bước 4 và repo ở bước 2.
2. Dán: **`Đọc KHOI-TAO.md và khởi tạo xưởng video cho tôi.`**
3. Claude sẽ hỏi: tên xưởng, lĩnh vực, ngôn ngữ, bạn là ai và xưng hô thế nào, kênh YouTube mẫu, script cũ / video mẫu (nếu có). Sau đó Claude tự tạo thư mục Drive, file cấu hình `studio.json`, và bản đồ 3D, rồi gửi bạn link.

## Bước 6 — Dùng hằng ngày
| Bạn nói | Claude làm |
|---|---|
| "Tìm 7 chủ đề cho tuần này" | Tạo Doc ý tưởng trong `00 Kế hoạch`. Bạn duyệt, rồi dán transcript từng video gốc vào chính Doc đó (YouTube → "…Thêm" → "Hiện bản chép lời"). |
| "Đã dán transcript" | Viết script cả đợt vào 1 Doc, tạo thư mục `Video NN` cho từng video. |
| "Video 03 đã up" | Tải voice + cảnh quay, dựng, kiểm tra, giao video final kèm caption. |
| "Đồ hoạ to hơn", "phụ đề chậm hơn"… | Sửa đúng bước liên quan và ghi vào file style để lần sau tự làm đúng. |

**Quay cảnh:** quay dọc, đủ sáng, nhiều cảnh làm việc / sinh hoạt hợp chủ đề. Cảnh đang nói vào mic sẽ không khớp miệng với voice thu riêng. Claude ghép cảnh **theo đúng thứ tự quay**, không cắt xen kẽ.

## Bước 7 (tuỳ chọn) — Tự up video final lên Drive
Công cụ Drive của Claude chỉ đẩy được file rất nhỏ, nên video final cần rclone:
1. Trên máy tính, cài rclone (https://rclone.org/install/), mở Terminal, chạy `rclone authorize "drive"`, đăng nhập Google → Terminal in ra một đoạn JSON.
2. Vào cài đặt môi trường Claude → thêm biến môi trường **`RCLONE_DRIVE_TOKEN`** = đoạn JSON đó. **Không dán vào chat.**
3. Thêm domain `www.googleapis.com` và `oauth2.googleapis.com`.
Chưa làm bước này thì Claude gửi video final trong chat để bạn tải về.

---

## Những điều đã thử và rút ra (để bạn khỏi mất công)
- **Mỗi công đoạn chỉ 1 file.** Ý tưởng: 1 Doc/đợt. Script: 1 Doc/đợt, mỗi video một mục (bấm tên video ở thanh Dàn ý bên trái để nhảy tới). Nhiều file lẻ rất rối.
- **Không làm đẹp mặt tự động** (làm trắng da, son, chỉnh dáng): kết quả trông giả. Nếu cần, chỉnh bằng app trên điện thoại trước khi up.
- **Hook hiện đủ ngay từ giây 0**, không hiện từng chữ, để người xem biết ngay video nói gì.
- **Cảnh theo thứ tự quay**, chuyển cảnh đúng chỗ hết câu.
- **YouTube chặn tải transcript từ máy chủ cloud** → bạn dán transcript. Đừng nhờ Claude lách.
- **Claude không sửa được Doc đã có** (chỉ tạo và đọc). Muốn đổi script thì bạn sửa trên Doc, hoặc nhờ Claude gửi đoạn sửa trong chat.
- **Mọi số liệu trong script đều có nguồn** ở cuối mục; câu kể chuyện cá nhân chưa chắc đúng được đánh dấu **[xác nhận]** để bạn kiểm.

## Xử lý sự cố
| Hiện tượng | Cách xử lý |
|---|---|
| Claude báo "403" / không tải được file Drive | Thiếu domain ở bước 4, hoặc thư mục chưa để "Anyone with the link". |
| Không nhận dạng được voice | Thiếu domain `huggingface.co` (+ 2 domain cdn) ở bước 4. |
| Claude không thấy 4 agent | Thư mục ẩn `.claude` chưa được up lên GitHub (bước 2). |
| Bản đồ 3D không cập nhật | Tải lại trang; kiểm tra `ban_do_url` trong `studio.json` đúng link bản đồ. |
| Không tạo được file trên Drive | Kiểm tra connector Google Drive đã bật trong Settings → Connectors (bước 3). |

## Bên trong bộ khung
```
HUONG-DAN.md         hướng dẫn này
KHOI-TAO.md          câu lệnh khởi tạo + các bước Claude làm khi khởi tạo
CLAUDE.md            quy tắc chung cho đội agent
studio.example.json  mẫu cấu hình xưởng (Claude điền thành studio.json)
style/               giọng văn script, kiểu dựng video
.claude/skills/      4 agent: nghien-cuu, viet-script, dung-video, qa-video
pipeline/            code dựng video: tải Drive, nhận dạng voice, cắt cảnh, đồ hoạ, phụ đề, ghép final, up Drive
docs/ban-do-3d.html  bản đồ 3D tiến độ
projects/_mau/       ví dụ file đồ hoạ của 1 video
setup.sh             cài công cụ đầu mỗi phiên
```
