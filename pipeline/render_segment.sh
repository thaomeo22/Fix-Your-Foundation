#!/bin/bash
# Cắt 1 đoạn từ source, chuẩn hoá 1080x1920@30, encode (không làm đẹp — chủ kênh đã bỏ bước này).
# usage: render_segment.sh <work_dir> <n> <src_name> <start> <dur> <zoom 0|1>
W=$1; n=$2; src=$3; ss=$4; d=$5; z=$6
if [ "$z" = 1 ]; then
  vf="fps=30,scale=w='trunc(1080*(1+0.07*t/$d)/2)*2':h='trunc(1920*(1+0.07*t/$d)/2)*2':eval=frame,crop=1080:1920"
else
  vf="fps=30,scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920"
fi
mkdir -p "$W/seg"
ffmpeg -v error -y -ss "$ss" -t "$d" -i "$W/src/$src" -an -vf "$vf" -c:v libx264 -preset fast -crf 17 -pix_fmt yuv420p "$W/seg/$n.mp4"
echo "seg $n done $(ffprobe -v error -show_entries format=duration -of csv=p=0 "$W/seg/$n.mp4")"
