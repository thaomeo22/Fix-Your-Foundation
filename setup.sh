#!/bin/bash
# Cài công cụ cho pipeline dựng video. Chạy một lần mỗi phiên: bash setup.sh
# Cần các domain: pypi.org, registry.npmjs.org, huggingface.co (model Whisper),
# drive.usercontent.google.com (tải source từ Drive).
set -e
ROOT="$(cd "$(dirname "$0")" && pwd)"

# Nhận dạng giọng nói (Whisper) chạy bằng Python hệ thống
python3 -m pip install -q faster-whisper

# Font hỗ trợ tiếng Việt cho đồ hoạ
F="$ROOT/.cache/fonts"; mkdir -p "$F"
for p in @fontsource/fraunces @fontsource/dancing-script @fontsource/patrick-hand @fontsource/ibm-plex-mono; do
  d="$F/$(echo $p | tr '/@' '__')"
  [ -d "$d" ] && continue
  mkdir -p "$d" && (cd "$d" && t=$(npm pack -q "$p" 2>/dev/null | tail -1) && tar xzf "$t" && rm "$t")
done

command -v ffmpeg >/dev/null || { echo "Thiếu ffmpeg"; exit 1; }
node -e "require('playwright')" || { echo "Thiếu playwright"; exit 1; }
echo "Setup xong."
