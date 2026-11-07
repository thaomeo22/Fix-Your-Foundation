#!/bin/bash
# Tải file Drive đã chia sẻ "Anyone with the link".  usage: drive_fetch.sh <file_id> <output>
curl -sSL --fail -o "$2" "https://drive.usercontent.google.com/download?id=$1&export=download&confirm=t"
