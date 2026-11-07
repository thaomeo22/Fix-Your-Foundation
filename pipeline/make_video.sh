#!/bin/bash
# Dựng video Fix Your Foundation từ một project:  bash pipeline/make_video.sh projects/<slug> [bước]
# Các bước (chạy tuần tự; bước đã có kết quả sẽ được bỏ qua):
#   fetch  tải clip quay + ảnh minh hoạ từ Drive           -> work/<slug>/{src,assets}
#   takes  nhận dạng lời từng clip + contact sheet          -> projects/<slug>/takes.txt, work/<slug>/thumbs
#          >> Claude chọn take, viết projects/<slug>/edl.txt
#   cut    cắt + ghép theo edl.txt (giữ tiếng gốc)          -> work/<slug>/base.mov, projects/<slug>/transcript.json
#          >> Claude viết lines.txt (sửa chính tả + đánh dấu nhấn) và graphics.py
#   gfx    chữ động + đồ hoạ từ graphics.py                 -> work/<slug>/frames
#   final  ghép + chỉnh màu + xử lý tiếng                   -> work/<slug>/final.mp4 (+ final_sheet.jpg)
set -e
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
P="$(cd "$1" && pwd)"; NAME="$(basename "$P")"; ONLY="$2"
W="$ROOT/work/$NAME"; mkdir -p "$W/src" "$W/assets" "$W/thumbs"
J() { python3 -c "import json,sys;d=json.load(open('$P/project.json'));print(eval(sys.argv[1]))" "$1"; }
run() { [ -z "$ONLY" ] || [ "$ONLY" = "$1" ]; }

if run fetch; then
  for kind in sources assets; do
    dir=src; [ "$kind" = assets ] && dir=assets
    for name in $(J "' '.join(d.get('$kind',{}))"); do
      [ -s "$W/$dir/$name" ] || "$ROOT/pipeline/drive_fetch.sh" "$(J "d['$kind']['$name']")" "$W/$dir/$name" &
    done
  done; wait
  echo "fetch xong: $(ls "$W/src" | wc -l) clip, $(ls "$W/assets" | wc -l) ảnh"
fi

if run takes; then
  python3 "$ROOT/pipeline/takes.py" "$P" "$W"
  echo ">> Đọc takes.txt + thumbs, viết $P/edl.txt rồi chạy bước cut."
fi

if run cut; then
  python3 "$ROOT/pipeline/cut.py" "$P" "$W"
  echo ">> Viết lines.txt (1 dòng / 1 đoạn edl) và graphics.py rồi chạy bước gfx."
fi

DUR() { ffprobe -v error -show_entries format=duration -of csv=p=0 "$W/base.mov"; }

if run gfx && [ -f "$P/graphics.py" ]; then
  python3 "$P/graphics.py" "$W"
  rm -rf "$W/frames"; mkdir -p "$W/frames"
  N=$(python3 -c "import math;print(math.ceil($(DUR)*30)+1)")
  for k in 0 1 2 3; do
    node "$ROOT/pipeline/gfx/render.js" "$W/overlay.html" "$W/frames" 30 $((k*N/4)) $(((k+1)*N/4)) &
  done; wait
  echo "gfx xong: $(ls "$W/frames" | wc -l) khung"
fi

if run final; then
  GRADE=$(J 'd.get("grade","eq=contrast=1.04:saturation=1.05:brightness=0.01,colortemperature=temperature=5400:mix=0.35")')
  # audio: "voice" (mặc định, có lời nói) | "ambient" (giữ tiếng nền nhỏ, không nâng) | "mute"
  case "$(J 'd.get("audio","voice")')" in
    ambient) AF="volume=0.6,aresample=48000" ;;
    mute)    AF="volume=0,aresample=48000" ;;
    *)       AF="highpass=f=80,afftdn=nf=-25,acompressor=threshold=-18dB:ratio=3:attack=5:release=80,loudnorm=I=-14:TP=-1.5:LRA=11,aresample=48000" ;;
  esac
  if [ -f "$P/graphics.py" ]; then
    IN=(-i "$W/base.mov" -framerate 30 -i "$W/frames/f_%05d.png")
    VF="[0:v]$GRADE[b];[b][1:v]overlay=0:0:format=auto:eof_action=pass[v]"
  else
    IN=(-i "$W/base.mov"); VF="[0:v]$GRADE[v]"
  fi
  ffmpeg -v error -y "${IN[@]}" \
   -filter_complex "$VF;[0:a]$AF[a]" \
   -map "[v]" -map "[a]" -c:v libx264 -preset slow -crf 20 -maxrate 8M -bufsize 16M -pix_fmt yuv420p -r 30 \
   -c:a aac -b:a 192k -movflags +faststart -t "$(DUR)" "$W/final.mp4"
  ffmpeg -v error -y -i "$W/final.mp4" -vf "fps=1/3,scale=240:-1,tile=8x3" -frames:v 1 "$W/final_sheet.jpg"
  ffprobe -v error -show_entries format=duration,size -of compact "$W/final.mp4"
fi
