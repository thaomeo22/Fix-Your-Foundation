#!/bin/bash
# Dựng video từ một project:  bash pipeline/make_video.sh projects/<tên> [bước]
# Các bước (chạy tuần tự, bước đã có kết quả sẽ được bỏ qua):
#   fetch   tải voice + source từ Drive          -> work/<tên>/{voice,src}
#   asr     nhận dạng voice                       -> projects/<tên>/transcript.json
#   probe   in độ dài voice + source + contact sheet để chọn cảnh (viết edl.txt)
#   seg     cắt từng đoạn theo edl.txt (theo thứ tự quay) -> work/<tên>/seg
#   gfx     đồ hoạ + phụ đề từ graphics.py        -> work/<tên>/frames
#   final   ghép + xử lý voice                    -> work/<tên>/final.mp4 (+ final_sheet.jpg)
set -e
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
P="$(cd "$1" && pwd)"; NAME="$(basename "$P")"; ONLY="$2"
W="$ROOT/work/$NAME"; mkdir -p "$W/voice" "$W/src" "$W/thumbs"
J() { python3 -c "import json,sys;d=json.load(open('$P/project.json'));print(eval(sys.argv[1]))" "$1"; }
run() { [ -z "$ONLY" ] || [ "$ONLY" = "$1" ]; }
VOICE="$W/voice/$(J 'd["voice"]["name"]')"

if run fetch; then
  [ -s "$VOICE" ] || "$ROOT/pipeline/drive_fetch.sh" "$(J 'd["voice"]["drive_id"]')" "$VOICE"
  for name in $(J '" ".join(d["sources"])'); do
    [ -s "$W/src/$name" ] || "$ROOT/pipeline/drive_fetch.sh" "$(J "d['sources']['$name']")" "$W/src/$name" &
  done; wait
  ffmpeg -v error -y -i "$VOICE" -ac 1 -ar 16000 "$W/voice/voice.wav"
  echo "fetch xong"
fi

if run asr && [ ! -s "$P/transcript.json" ]; then
  python3 "$ROOT/pipeline/asr.py" "$W/voice/voice.wav" "$P/transcript.json" "$(J 'd.get("asr_prompt","")')"
  echo ">> Viết lines.txt (1 dòng/segment, sửa chính tả) trước khi chạy bước gfx."
fi

DUR=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$VOICE")

if run probe; then
  echo "voice: ${DUR}s"
  for f in "$W"/src/*; do
    n=$(basename "$f"); d=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$f")
    ffmpeg -v error -y -i "$f" -vf "fps=1/3,scale=240:-1,tile=8x2" -frames:v 1 "$W/thumbs/${n%.*}.jpg"
    echo "source $n: ${d}s  -> $W/thumbs/${n%.*}.jpg (1 ảnh / 3 giây)"
  done
fi

if run seg; then
  grep -v '^#' "$P/edl.txt" | awk -v w="$W" 'NF{print w, $0}' | xargs -P 4 -L 1 "$ROOT/pipeline/render_segment.sh"
  ls "$W"/seg/*.mp4 | sort | sed "s/^/file '/;s/$/'/" > "$W/concat.txt"
  ffmpeg -v error -y -f concat -safe 0 -i "$W/concat.txt" -c copy "$W/base.mp4"
fi

if run gfx; then
  python3 "$P/graphics.py" "$W"
  rm -rf "$W/frames"; mkdir -p "$W/frames"
  N=$(python3 -c "import math;print(math.ceil($DUR*30)+1)")
  for k in 0 1 2 3; do
    node "$ROOT/pipeline/gfx/render.js" "$W/overlay.html" "$W/frames" 30 $((k*N/4)) $(((k+1)*N/4)) &
  done; wait
  echo "gfx xong: $(ls "$W/frames" | wc -l) khung"
fi

if run final; then
  ffmpeg -v error -y -i "$W/base.mp4" -framerate 30 -i "$W/frames/f_%05d.png" -i "$VOICE" \
   -filter_complex "[0:v]eq=brightness=0.015:saturation=1.06:contrast=1.03[b];[b][1:v]overlay=0:0:format=auto:eof_action=pass[v];[2:a]highpass=f=80,afftdn=nf=-25,acompressor=threshold=-18dB:ratio=3:attack=5:release=80,loudnorm=I=-14:TP=-1.5:LRA=11[a]" \
   -map "[v]" -map "[a]" -c:v libx264 -preset slow -crf 21 -maxrate 6M -bufsize 12M -pix_fmt yuv420p \
   -c:a aac -b:a 192k -movflags +faststart -t "$DUR" "$W/final.mp4"
  ffmpeg -v error -y -i "$W/final.mp4" -vf "fps=1/6,scale=240:-1,tile=7x2" -frames:v 1 "$W/final_sheet.jpg"
  ffprobe -v error -show_entries format=duration,size -of compact "$W/final.mp4"
fi
