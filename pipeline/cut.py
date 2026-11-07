"""Bước cut: cắt các đoạn theo edl.txt (giữ tiếng gốc), ghép thành base.mov, và dựng transcript.json theo
dòng thời gian của video (lấy từ ASR từng clip, không phải nhận dạng lại).
usage: python3 cut.py <project_dir> <work_dir>

edl.txt — mỗi dòng 1 đoạn, theo thứ tự xuất hiện trong video:
    <clip>  <vào>  <ra>  [zoom]  [cy]  [cover=<clip>@<giây>]      (vd: A02.mp4  3.10  8.42  1.15  0.35)
  zoom   1.0 = khung gốc; 1.12–1.25 = punch-in (đổi cỡ cảnh khi nhảy cắt trong cùng 1 clip)
  cy     vị trí cắt dọc khi zoom (0 = giữ phần trên, 1 = giữ phần dưới)
  cover  thay hình bằng clip khác (b-roll) từ giây đó, tiếng vẫn lấy từ <clip>
"""
import json, os, subprocess, sys
from concurrent.futures import ThreadPoolExecutor

P, W = sys.argv[1], sys.argv[2]
FADE = 0.012  # khử tiếng "tạch" ở mỗi điểm cắt


def dur(f):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f],
                                capture_output=True, text=True).stdout)


segs = []
for ln, line in enumerate(open(os.path.join(P, "edl.txt"), encoding="utf-8"), 1):
    line = line.split("#")[0].split()
    if not line:
        continue
    s = {"src": line[0], "in": float(line[1]), "out": float(line[2]), "zoom": 1.0, "cy": 0.4, "cover": None}
    pos = ["zoom", "cy"]
    for x in line[3:]:
        k, _, v = x.partition("=")
        if not v:  # viết tắt theo vị trí: <zoom> <cy>
            k, v = pos.pop(0), x
        if k == "cover":
            c, _, t = v.partition("@")
            s["cover"] = (c, float(t or 0))
        else:
            s[k] = float(v)
    srcf = os.path.join(W, "src", s["src"])
    assert os.path.exists(srcf), f"edl dòng {ln}: không có {srcf}"
    assert 0 <= s["in"] < s["out"] <= dur(srcf) + 0.05, f"edl dòng {ln}: vào/ra sai ({s['in']}–{s['out']})"
    segs.append(s)


def vf(z, cy):
    return (f"fps=30,scale=w={1080 * z:.0f}:h={1920 * z:.0f}:force_original_aspect_ratio=increase:force_divisible_by=2,"
            f"crop=1080:1920:(iw-1080)/2:(ih-1920)*{cy},setsar=1")


def render(i):
    s = segs[i]
    d = s["out"] - s["in"]
    out = os.path.join(W, "seg", f"{i:03d}.mov")
    cmd = ["ffmpeg", "-v", "error", "-y", "-ss", f"{s['in']:.3f}", "-t", f"{d:.3f}", "-i", os.path.join(W, "src", s["src"])]
    vmap = "0:v:0"
    if s["cover"]:
        cmd += ["-ss", f"{s['cover'][1]:.3f}", "-t", f"{d:.3f}", "-i", os.path.join(W, "src", s["cover"][0])]
        vmap = "1:v:0"
    cmd += ["-map", vmap, "-map", "0:a:0", "-vf", vf(s["zoom"], s["cy"]),
            "-af", f"afade=t=in:d={FADE},afade=t=out:st={d - FADE:.3f}:d={FADE},aresample=48000",
            "-ac", "2", "-c:v", "libx264", "-preset", "fast", "-crf", "16", "-pix_fmt", "yuv420p",
            "-c:a", "pcm_s16le", "-t", f"{d:.3f}", out]
    subprocess.run(cmd, check=True)
    return out


os.makedirs(os.path.join(W, "seg"), exist_ok=True)
for f in os.listdir(os.path.join(W, "seg")):
    os.remove(os.path.join(W, "seg", f))
with ThreadPoolExecutor(4) as ex:
    outs = list(ex.map(render, range(len(segs))))
with open(os.path.join(W, "concat.txt"), "w") as fh:
    fh.write("".join(f"file '{o}'\n" for o in outs))
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", os.path.join(W, "concat.txt"),
                "-c", "copy", os.path.join(W, "base.mov")], check=True)

# transcript theo dòng thời gian video: 1 segment = 1 đoạn edl (lines.txt cũng 1 dòng = 1 đoạn edl)
trans, t = [], 0.0
for i, s in enumerate(segs):
    d = dur(outs[i])
    words = []
    asr = os.path.join(P, "asr", s["src"] + ".json")
    for seg in json.load(open(asr)) if os.path.exists(asr) else []:
        for w in seg["words"]:
            if s["in"] <= (w["s"] + w["e"]) / 2 <= s["out"]:
                words.append({"s": round(t + max(0, w["s"] - s["in"]), 3), "e": round(t + min(d, w["e"] - s["in"]), 3),
                              "w": w["w"]})
    trans.append({"start": round(t, 3), "end": round(t + d, 3), "text": "".join(w["w"] for w in words).strip(),
                  "words": words})
    print(f"{i:02d} {t:6.2f}-{t + d:6.2f} {s['src']:<12} {trans[-1]['text']}")
    t += d
json.dump(trans, open(os.path.join(P, "transcript.json"), "w"), ensure_ascii=False, indent=1)
print(f"base.mov: {dur(os.path.join(W, 'base.mov')):.2f}s, {len(segs)} đoạn -> transcript.json")
