"""Đồ hoạ cho video 01. Chạy: python3 graphics.py <work_dir>  (tạo <work_dir>/overlay.html)"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "pipeline", "gfx"))
from lib import *

HOOK_END = 2.85
caps = load_captions(os.path.join(HERE, "transcript.json"), os.path.join(HERE, "lines.txt"), hide_before=HOOK_END, total=82.3)

E = []
# 1 hook — hiện đủ ngay từ 0s (t0 âm để không có hiệu ứng bật lên ở khung đầu)
E.append(el(-1, 2.85, 0, 150, '<div class="hook">'
            + '<div class="script" style="margin-left:90px">đọc lại 5 lần không bằng</div>'
            + '<div class="title">tự kiểm tra</div>'
            + '<div class="script" style="text-align:right;margin-right:120px;margin-top:-30px">1 lần</div>'
            + "</div>", w=1080))
# 2 study source
E.append(el(3.0, 6.4, 170, 170, paper('<div class="mono">thí nghiệm · 2006</div><div class="hand big">Roediger &amp; Karpicke</div>'
            + R(4.2, '<div class="hand">2 nhà tâm lý học · 1 đoạn văn</div>')), rot=-3, w=740))
# 3 groups
E.append(el(6.55, 12.4, 50, 160, paper('<div class="label">nhóm 1</div><div class="hand big">đọc lại ×4</div>'), rot=-4, w=440))
E.append(el(8.45, 12.4, 540, 230, paper('<div class="label">nhóm 2</div><div class="hand big">đọc ×1</div>'
            + R(10.0, '<div class="hand big">+ tự kiểm tra ×3</div>')), rot=3, w=500))
# 4 results
E.append(el(12.65, 17.4, 330, 110, '<div class="label lg">sau 1 tuần</div>', rot=-2))
E.append(el(14.35, 17.4, 70, 240, paper('<div class="num grey">40%</div><div class="hand">đọc lại</div>', tape=False), rot=-5, w=400))
E.append(el(16.3, 17.4, 590, 220, paper('<div class="num red">61%</div><div class="hand">' + H(16.5, "tự kiểm tra") + '</div>', tape=False), rot=4, w=420))
# 5 familiarity illusion
E.append(el(18.75, 22.9, 640, 120, '<div class="label">tự tin hơn ?!</div>', rot=6))
E.append(el(20.15, 22.9, 140, 230, paper('<div class="serif">quen mắt</div>' + R(21.85, '<div class="serif red">≠ đã hiểu</div>'), cls="paper torn"), rot=-3, w=620))
# 6 cooking analogy
E.append(el(23.0, 26.5, 130, 150, paper('<div class="mono">học = nấu ăn</div>'
            + R(24.4, '<div class="hand big">' + S(25.3, "đọc công thức ×10") + '</div>')
            + R(25.6, '<div class="hand big">' + H(25.75, "tự tay nấu ×1") + '</div>')), rot=-2, w=760))
# 7 list of 4
items = [("gấp sách &amp; tự hỏi", 27.15), ("ôn giãn cách", 27.45), ("giảng lại (Feynman)", 27.75), ("học theo block", 28.05)]
lst = '<div class="sticky"><i class="tape"></i><div class="mono">4 cách học</div>' + "".join(
    R(t, star(i + 1, 70) + f'<span class="hand">{txt}</span>', "row") for i, (txt, t) in enumerate(items)) + "</div>"
E.append(el(27.0, 30.7, 230, 90, lst, rot=-2, w=620))
# 8 method 1
E.append(el(30.8, 38.6, 60, 110, '<div class="hdr">' + star(1) + '<div class="label lg">gấp sách lại &amp; tự hỏi</div></div>', rot=-1))
E.append(el(33.8, 36.6, 250, 280, paper('<div class="hand big">đóng tài liệu</div><div class="hand">→ tự viết ra / nói ra</div>'), rot=3, w=560))
E.append(el(36.7, 38.6, 230, 280, paper('<div class="hand big">chỗ nào bí</div><div class="hand">= ' + H(37.5, "chỗ cần học lại") + '</div>', cls="paper torn"), rot=-3, w=600))
E.append(el(38.9, 42.6, 170, 150, paper('<div class="mono">tổng quan · 2013</div><div class="serif">10 phương pháp học</div><div class="hand">được chấm điểm hiệu quả</div>'), rot=-2, w=740))
E.append(el(42.9, 47.9, 60, 170, paper('<div class="hand big">tự kiểm tra</div><div class="tick">✓ top hiệu quả</div>', tape=False), rot=-4, w=440))
E.append(el(45.0, 47.9, 560, 230, paper('<div class="hand big">' + S(46.6, "đọc lại · highlight") + '</div><div class="cross">kém hiệu quả</div>', tape=False), rot=4, w=470))
# 9 method 2
E.append(el(48.3, 57.1, 60, 110, '<div class="hdr">' + star(2) + '<div class="label lg">ôn giãn cách</div></div>', rot=-1))
E.append(el(50.0, 53.9, 210, 280, paper('<div class="hand big">' + S(51.5, "5 tiếng / 1 đêm") + '</div>'
            + R(51.8, '<div class="hand big">' + H(52.0, "1 tiếng × vài ngày") + '</div>')), rot=2, w=640))
E.append(el(54.3, 57.1, 200, 280, paper('<div class="hand big">gần quên → cố nhớ lại</div>' + R(55.8, '<div class="serif red">= nhớ sâu hơn</div>'), cls="paper torn"), rot=-3, w=680))
# 10 method 3
E.append(el(57.35, 66.6, 60, 110, '<div class="hdr">' + star(3) + '<div class="label lg">giảng lại cho người mới</div></div>', rot=-1))
E.append(el(59.4, 63.4, 250, 290, paper('<div class="mono">kỹ thuật</div><div class="serif">Feynman</div>'
            + R(61.3, '<div class="hand">giải thích cho bạn nhỏ 12 tuổi</div>')), rot=3, w=600))
E.append(el(63.6, 66.6, 200, 290, paper('<div class="hand big">' + S(64.9, "dùng thuật ngữ để che") + '</div>'
            + R(65.4, '<div class="serif red">= chưa thật sự hiểu</div>'), cls="paper torn"), rot=-2, w=700))
# 11 method 4
E.append(el(66.85, 75.4, 60, 110, '<div class="hdr">' + star(4) + '<div class="label lg">học theo block</div></div>', rot=-1))
E.append(el(69.5, 73.2, 220, 280, paper('<div class="serif">25–50 phút</div>'
            + R(71.2, '<div class="hand">điện thoại → phòng khác</div>')
            + R(72.4, '<div class="hand big">rồi ' + H(72.5, "nghỉ hẳn") + '</div>')), rot=2, w=640))
E.append(el(73.3, 75.4, 200, 290, paper('<div class="hand big">biết lúc được nghỉ</div><div class="hand">→ não dễ bắt đầu hơn</div>', cls="paper torn"), rot=-3, w=660))
# 12 outro
E.append(el(75.6, 77.3, 0, 180, '<div class="hook"><div class="script" style="text-align:center">'
            + S(76.4, "học nhiều giờ") + '</div></div>', w=1080))
E.append(el(77.4, 80.3, 0, 160, '<div class="hook"><div class="script" style="margin-left:150px">học</div><div class="title">đúng cách</div>'
            + R(78.6, '<div class="script" style="text-align:right;margin-right:110px;margin-top:-30px">nhớ lâu · nhẹ đầu</div>') + "</div>", w=1080))
E.append(el(80.4, 82.3, 0, 170, '<div class="hook"><div class="script" style="margin-left:120px">lần tới học, thử</div><div class="title" style="font-size:112px">gấp sách lại</div></div>', w=1080))


build(E, caps, os.path.join(sys.argv[1], "overlay.html"))
