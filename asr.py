"""Nhận dạng voice kèm mốc thời gian từng từ (ngôn ngữ lấy từ studio.json).
usage: python3 asr.py <voice.wav 16kHz mono> <transcript.json> [gợi ý từ khoá]"""
import sys, json, os, wave, numpy as np
from faster_whisper import WhisperModel

w = wave.open(sys.argv[1])
audio = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32) / 32768
prompt = sys.argv[3] if len(sys.argv) > 3 else None
model = WhisperModel("medium", device="cpu", compute_type="int8", cpu_threads=3)
LANG = json.load(open(os.path.join(os.path.dirname(__file__), "..", "studio.json")))["language"]
segs, _ = model.transcribe(audio, language=LANG, word_timestamps=True, initial_prompt=prompt)
out = []
for s in segs:
    out.append({"start": s.start, "end": s.end, "text": s.text,
                "words": [{"s": x.start, "e": x.end, "w": x.word} for x in s.words]})
    print(f"{s.start:6.2f}-{s.end:6.2f} {s.text}", flush=True)
json.dump(out, open(sys.argv[2], "w"), ensure_ascii=False, indent=1)
