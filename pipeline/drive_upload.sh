#!/bin/bash
# Up file lên thư mục "Final Video" trên Drive của chủ kênh bằng rclone.
#   usage: drive_upload.sh <file> [tên trên Drive]
# Cần: biến môi trường RCLONE_DRIVE_TOKEN (JSON token từ `rclone authorize "drive"` trên máy chủ kênh),
#      domain www.googleapis.com + oauth2.googleapis.com được phép.
set -e
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
FINAL_FOLDER_ID=$(python3 -c "import json;print(json.load(open('$ROOT/studio.json'))['drive']['final_video'])")
[ -n "$RCLONE_DRIVE_TOKEN" ] || { echo "Chưa có RCLONE_DRIVE_TOKEN — xem README mục 'Tự up video final'"; exit 2; }
if ! command -v rclone >/dev/null; then
  ROOT="$(cd "$(dirname "$0")/.." && pwd)"; mkdir -p "$ROOT/.cache/bin"
  if [ ! -x "$ROOT/.cache/bin/rclone" ]; then
    v=$(curl -sSL https://api.github.com/repos/rclone/rclone/releases/latest | python3 -c "import json,sys;print(json.load(sys.stdin)['tag_name'])")
    curl -sSL -o /tmp/rclone.zip "https://github.com/rclone/rclone/releases/download/$v/rclone-$v-linux-amd64.zip"
    python3 -c "import zipfile;z=zipfile.ZipFile('/tmp/rclone.zip');n=[x for x in z.namelist() if x.endswith('/rclone')][0];open('$ROOT/.cache/bin/rclone','wb').write(z.read(n))"
    chmod +x "$ROOT/.cache/bin/rclone"
  fi
  PATH="$ROOT/.cache/bin:$PATH"
fi
export RCLONE_CONFIG_PINGU_TYPE=drive RCLONE_CONFIG_PINGU_SCOPE=drive RCLONE_CONFIG_PINGU_TOKEN="$RCLONE_DRIVE_TOKEN" \
       RCLONE_CONFIG_PINGU_ROOT_FOLDER_ID="$FINAL_FOLDER_ID"
rclone copyto --progress "$1" "pingu:${2:-$(basename "$1")}"
echo "Đã up: ${2:-$(basename "$1")} -> Final Video"
