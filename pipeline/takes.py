"""Bước takes: nhận dạng lời từng clip quay + contact sheet, để Claude chọn take tốt nhất.
usage: python3 takes.py <project_dir> <work_dir>
Ghi:  <project_dir>/asr/<clip>.json   (mốc thời gian từng từ, có cache)
      <project_dir>/takes.txt         (mỗi dòng: clip  vào  ra  lời — vào/ra = từ đầu/cuối của câu)
      <work_dir>/thumbs/<clip>.jpg    (1 ảnh / 2 giây)"""
import json, os, subprocess, sys, tempfile

P, W = sys.argv[1], sys.argv[2]
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
proj = json.load(open(os.path.join(P, "project.json")))
os.makedirs(os.path.join(P, "asr"), exist_ok=True)


def probe(f):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                          "format=duration:format_tags=creation_time:stream=codec_type,width,height:stream_side_data=rotation",
                          "-of", "json", f], capture_output=True, text=True).stdout
    return json.loads(out)


rows, info = [], []
for name in sorted(proj.get("sources", {})):
    f = os.path.join(W, "src", name)
    d = probe(f)
    dur = float(d["format"]["duration"])
    ct = d["format"].get("tags", {}).get("creation_time", "?")
    v = next((s for s in d["streams"] if s["codec_type"] == "video"), {})
    has_audio = any(s["codec_type"] == "audio" for s in d["streams"])
    rot = next((sd.get("rotation", 0) for s in d["streams"] for sd in s.get("side_data_list", [])), 0)
    w, h = v.get("width", 0), v.get("height", 0)
    if abs(int(rot)) in (90, 270):
        w, h = h, w
    info.append(f"# {name}: {dur:.1f}s  {w}x{h}{'  (NGANG — sẽ bị cắt 2 bên)' if w > h else ''}  quay {ct}"
                f"{'' if has_audio else '  (KHÔNG có tiếng — chỉ dùng làm cover)'}")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", f, "-vf", "fps=1/2,scale=200:-1,tile=10x3",
                    "-frames:v", "1", os.path.join(W, "thumbs", os.path.splitext(name)[0] + ".jpg")])
    if not has_audio:
        continue
    cache = os.path.join(P, "asr", name + ".json")
    if not os.path.exists(cache):
        with tempfile.TemporaryDirectory() as td:
            wav = os.path.join(td, "a.wav")
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", f, "-vn", "-ac", "1", "-ar", "16000", wav], check=True)
            subprocess.run([sys.executable, os.path.join(ROOT, "pipeline", "asr.py"), wav, cache, proj.get("asr_prompt", "")],
                           check=True)
    for s in json.load(open(cache)):
        if s["words"]:
            rows.append(f"{name}\t{s['words'][0]['s']:7.2f}\t{s['words'][-1]['e']:7.2f}\t{s['text'].strip()}")

with open(os.path.join(P, "takes.txt"), "w", encoding="utf-8") as fh:
    fh.write("\n".join(info) + "\n# clip\tvào\tra\tlời\n" + "\n".join(rows) + "\n")
print("\n".join(info))
print(f"{len(rows)} câu -> {os.path.join(P, 'takes.txt')}")
