# Style dựng video

> Mặc định: talking-head / b-roll + đồ hoạ scrapbook. Câu lệnh khởi tạo có thể đổi theo video mẫu của bạn.

## Khung hình
- 1080×1920, 30fps, dài đúng bằng voice.
- **Cảnh theo thứ tự thời gian quay** (xem `creation_time` bằng ffprobe): chạy hết clip này rồi mới sang clip khác,
  **không cắt xen kẽ**, không quay lại clip cũ. Chỉ cắt ở ranh giới câu (lấy từ `transcript.json`); bỏ bớt phần đầu/cuối clip nếu dư.
- Mỗi clip zoom chậm 7% suốt đoạn cho đỡ tĩnh.

## Màu
**Không làm đẹp mặt / chỉnh dáng tự động** (đã thử, kết quả không đẹp). Chủ kênh tự chỉnh source trước khi up nếu cần.
Toàn khung chỉ chỉnh nhẹ: brightness +0.015, saturation 1.06, contrast 1.03.

## Đồ hoạ (`pipeline/gfx/lib.py`)
- **Hook**: chữ viết tay (Dancing Script) + tiêu đề lớn Fraunces 800 màu kem `#f8eda0`. **Hiện đủ cả câu ngay từ 0s** (dùng `t0` âm, không reveal từng chữ) để người xem biết ngay nội dung.
- **Giấy ghi chú** dán băng keo, giấy xé (`paper(..., cls="paper torn")`), chữ tay Patrick Hand, chữ đánh máy IBM Plex Mono.
- **Nhãn highlight vàng** + **ngôi sao đánh số** cho từng ý (`star(n)` + `label lg`).
- **Gạch ngang** `S(t, text)` khi nói điều sai / kém hiệu quả; **highlight** `H(t, text)` cho từ khoá đúng.
- Số liệu to: `num red` / `num grey`.
- Giấy nhớ vàng có dòng kẻ cho danh sách N ý.
- Đặt đồ hoạ ở vùng **y 90–650** (trên đầu người), không che mặt. Xuất hiện đúng từ khoá (lấy mốc từ word timestamps).
- **Phụ đề**: Fraunces italic 58px, 1–3 chữ/cụm, góc trái y≈1240, ẩn trong lúc hook.

## Âm thanh
highpass 80Hz → khử ồn → compressor → loudnorm −14 LUFS. Chưa có nhạc nền (chờ chủ kênh gửi nhạc).
