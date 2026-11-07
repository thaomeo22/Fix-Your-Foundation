# Style dựng video — Fix Your Foundation

Video tham chiếu: `style/video-mau.mp4` (xem bằng `ffmpeg … tile` trước khi dựng video đầu tiên của phiên).
Có 2 kiểu dựng, ghi trong `project.json` → `"kieu"`:

| `kieu` | Khi nào | Tiếng (`audio`) | Chữ |
|---|---|---|---|
| `noi` (mặc định) | Chủ kênh nói thẳng vào máy, có mic | `voice` | chữ động theo lời (`graphics.py` + `lines.txt`) |
| `montage` | Chỉ có cảnh thao tác, không lời | `ambient` hoặc `mute` | không có (hoặc vài chữ tiêu đề nếu chủ kênh xin) |

## Khung hình
- 1080×1920, 30fps, dài đúng bằng tổng các đoạn trong `edl.txt`.
- Clip gốc 4K dọc → thu nhỏ, giữ nét. Clip ngang sẽ bị cắt 2 bên: báo chủ kênh.
- Chỉnh màu mặc định (ấm, nhẹ): `eq=contrast=1.04:saturation=1.05:brightness=0.01,colortemperature=temperature=5400:mix=0.35`.
  Ghi đè bằng `project.json` → `"grade"` nếu cảnh quá vàng (vd phòng trắng).
- **Không làm đẹp mặt / chỉnh dáng tự động.**

## Kiểu `noi` — talking-head có tiếng trực tiếp
- **Chọn take:** đọc `takes.txt`. Câu nào nói nhiều lần → lấy lần **cuối cùng nói trơn tru**. Bỏ câu vấp, ậm ừ, khoảng lặng.
- **Nhảy cắt (jump cut)** giữa các câu: cắt sát từ đầu/cuối (chừa ~0,08s trước, ~0,12s sau). Không để lặng > 0,3s.
- **Đổi cỡ cảnh** mỗi 1–3 câu: đổi góc máy (clip khác) hoặc punch-in `zoom 1.12–1.2` trên cùng clip. Hai đoạn liền nhau cùng clip thì phải khác zoom.
- Thứ tự góc gợi ý theo video mẫu: chính diện ngồi ghế (hook) → góc cao nhìn xuống (lời hứa) → cận cầm máy selfie (giới thiệu/title card) → chính diện (uy tín, hoài nghi) → qua vai nhìn màn hình / cảnh thao tác (dữ liệu, `cover=`) → chính diện (kết quả) → nghiêng ở bàn làm việc (con số trước/sau) → chính diện (kết).
- Cảnh thao tác chứng minh (sản phẩm, màn hình, tay làm) chèn bằng `cover=<clip>@<giây>` — tiếng vẫn là lời nói.

### Chữ động (`pipeline/gfx/lib.py`)
- **Mọi câu nói đều hiện chữ**, từng cụm 2–4 chữ, ở vùng **trên đầu người** (mặc định `y=300`; đổi theo góc máy bằng `captions(y=[(giây, y)])`). Không dùng phụ đề dưới đáy.
- Chữ hiện **từng từ đúng lúc nói** (bật nhẹ lên). Cụm sau thay cụm trước, không chồng.
- Font: serif **Newsreader** trắng kem (chữ thường) · **Inter Tight 800** (nhấn) · **Great Vibes** (viết tay).
- Đánh dấu trong `lines.txt`:
  - `**chữ**` nhấn vàng chanh `#eef36a` — từ khoá cảm xúc (vd **so**, **chuyên nghiệp**). Tối đa 1 lần / 2 câu.
  - `__chữ__` viết tay to — tính từ "đắt giá" (vd __Professional__, __skeptical__).
  - `!!chữ!!` số liệu / chữ chốt cực to (vd !!300 triệu!!, !!3–4 giờ!!).
  - `((chữ))` vòng elip — chỗ đảo ngược / mốc thời gian (vd ((không tin)), ((2 tháng))).
  - `//` dòng phụ nhỏ lệch phải ("vì // trông nó"), `|` ngắt cụm.
- Đồ hoạ phụ (chỉ khi có lý do):
  - `title_card` sau phần uy tín: tên series + vai trò + "Eps #NN · @handle · nơi chốn" (lấy từ `studio.json` → `series`).
  - `card` ảnh chụp màn hình bằng chứng (bài báo, biểu đồ) ở nửa trên + dòng nguồn. Ẩn chữ lúc card hiện.
  - `counter` số chạy cho kết quả trước → sau. `img` logo/sản phẩm nhỏ bay cạnh chữ. `cloud` rải các từ quanh 1 chữ to.
- Không che mặt: đồ hoạ trong vùng y 120–700 hoặc cạnh người.

## Kiểu `montage` — cảnh thao tác không lời
- **Theo đúng thứ tự tên file** (1, 2, 3 …), mỗi clip **1 đoạn 2–3 giây** (clip cuối/thành phẩm được 3s). *(Chủ kênh yêu cầu, 07/11/2026.)*
- **Chọn khung đẹp nhất** mỗi clip: chấm điểm độ nét + độ rung (xem `dung-video` bước 3b), rồi xem contact sheet để chốt: thấy rõ móng/sản phẩm, tay không che, máy đứng yên, không lúc đang chuyển động mạnh.
- Cắt thẳng (hard cut), không hiệu ứng chuyển cảnh.
- Tiếng: `ambient` (giữ tiếng nền, giảm còn 60%, không nâng âm lượng) — chủ kênh thường lồng nhạc khi đăng.

## Âm thanh (`audio: voice`)
highpass 80Hz → khử ồn → compressor → loudnorm −14 LUFS. Mỗi điểm cắt có fade 12ms để không "tạch".
