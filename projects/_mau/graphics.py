"""Ví dụ graphics.py cho 1 video talking-head (dựng lại từ style/video-mau.mp4).
Chạy: python3 graphics.py <work_dir>   (tạo <work_dir>/overlay.html). Đi kèm edl.txt + lines.txt cùng thư mục."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "pipeline", "gfx"))
from lib import *

# chữ ở y=300 (trên đầu); ẩn chữ lúc hiện title card và thẻ biểu đồ
C = captions(HERE, y=[(0, 300)], hide=[(12.25, 14.75), (30.6, 39.2)])
E = [
    title_card(12.3, 14.7, "The diary of a Creator", "Journalist", "Creator", ["Eps #03", "@handle", "Taipei"]),
    img(C.t("expensive"), C.t("always"), 120, 520, "chart.png", w=150, rot=-8),
    cloud(C.t("for"), C.t("skeptical") - 0.1, ["Documentary", "News", "Commercials", "Music Videos", "Short films", "Weddings"], cy=360),
    card(C.t("data"), 39.2, "chart.png", "Sensor Tower / Bloomberg", y=140),
    counter(C.t("grew"), C.t("still"), 0, 520, 500, 100000, dur=1.6),
    sparkle(C.t("2"), C.t("I", 4), 820, 250),
]
build(E, C, sys.argv[1])
