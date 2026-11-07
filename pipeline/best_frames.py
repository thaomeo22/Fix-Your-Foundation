"""Chấm điểm từng đoạn của 1 clip (độ nét cao, ít rung) để chọn khung đẹp nhất cho montage.
usage: python3 best_frames.py <clip> [độ dài đoạn, mặc định 2.5]
In ra 4 điểm bắt đầu tốt nhất (không chồng nhau) kèm điểm. Sau đó vẫn phải xem ảnh để chốt."""
import subprocess, sys, numpy as np
f, win = sys.argv[1], float(sys.argv[2]) if len(sys.argv) > 2 else 2.5
FPS, W, H = 6, 216, 384
raw = subprocess.run(["ffmpeg", "-v", "error", "-i", f, "-vf", f"fps={FPS},scale={W}:{H},format=gray", "-f", "rawvideo", "-"],
                     capture_output=True).stdout
fr = np.frombuffer(raw, np.uint8).reshape(-1, H, W).astype(np.float32)
lap = lambda a: np.var(a[1:-1, 1:-1] * 4 - a[:-2, 1:-1] - a[2:, 1:-1] - a[1:-1, :-2] - a[1:-1, 2:])
sharp = np.array([lap(a) for a in fr])
mot = np.r_[0, [np.mean(np.abs(fr[i] - fr[i - 1])) for i in range(1, len(fr))]]
n = int(win * FPS); best = []
s_n = sharp / np.median(sharp)
for i in range(int(0.3 * FPS), len(fr) - n - 1):
    sc = np.mean(s_n[i:i + n]) - 0.08 * np.mean(mot[i:i + n]) - 0.15 * np.max(mot[i:i + n]) / 10
    best.append((sc, i / FPS))
best.sort(reverse=True)
picked = []
for sc, t in best:
    if all(abs(t - p) > win for _, p in picked):
        picked.append((sc, t))
    if len(picked) == 4: break
print(f, " ".join(f"{t:.1f}({sc:.2f})" for sc, t in picked))
