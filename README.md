# Xưởng video Fix Your Foundation

Claude Code làm video ngắn dọc 9:16 theo định dạng **Fix Your Foundation** (mẫu `style/video-mau.mp4`): nghiên cứu chủ đề → viết script 7 nhịp → (bạn quay, nói thẳng vào máy) → chọn take, nhảy cắt, chữ động → kiểm tra. Có thêm kiểu **montage** cảnh thao tác (mỗi clip 2–3s theo thứ tự tên file).

**Bắt đầu: đọc [`HUONG-DAN.md`](HUONG-DAN.md).** Cách quay: [`style/quay-style.md`](style/quay-style.md).

```
pipeline/make_video.sh   fetch → takes → cut → gfx → final
pipeline/takes.py        nhận dạng lời từng clip để chọn take
pipeline/cut.py          cắt/ghép theo edl.txt (giữ tiếng gốc, đổi góc, punch-in, cover b-roll)
pipeline/best_frames.py  chấm điểm độ nét + độ rung để chọn đoạn đẹp (montage)
pipeline/gfx/lib.py      chữ động + title card, thẻ ảnh, số chạy, logo
```
