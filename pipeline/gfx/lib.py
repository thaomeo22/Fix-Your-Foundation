"""Chữ động kiểu Fix Your Foundation (theo style/video-mau.mp4) + đồ hoạ phụ.

Mỗi project viết graphics.py:
    from lib import *
    C = captions(HERE, y=[(0, 300), (12.4, 880)], hide=[(30.4, 33.6)])
    E = [card(...), counter(...), ...]
    build(E, C, sys.argv[1])

lines.txt — 1 dòng = 1 đoạn trong edl.txt (cùng thứ tự), lời đã sửa chính tả + đánh dấu:
    |          ngắt cụm chữ (mỗi cụm hiện 1 lần ở vùng trên đầu)
    //         xuống dòng phụ trong cụm (nhỏ hơn, lệch phải — kiểu "because / they look")
    **chữ**    nhấn: sans đậm vàng chanh            (vd **CHUYÊN NGHIỆP**)
    __chữ__    chữ viết tay to                      (vd __Professional__)
    !!chữ!!    số / chữ cực to, sans đậm trắng      (vd !!300 triệu!!)
    ((chữ))    vẽ vòng elip quanh chữ               (kết hợp được: ((__2 tháng__)))
"""
import json, os, glob, re, sys, math, html as _html

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
FONTS = os.path.join(ROOT, ".cache", "fonts")
try:
    LANG = json.load(open(os.path.join(ROOT, "studio.json")))["language"]
except Exception:
    LANG = "vi"
THOUSANDS = "." if LANG == "vi" else ","

CAP_SIZE = 76          # cỡ chữ cụm chính (px)
CAP_MAXW = 4           # tối đa số chữ / cụm khi không có dấu |
MAX_WIDTH = 980        # cụm dài hơn sẽ tự thu nhỏ


# ---------------------------------------------------------------- phụ đề / chữ động
_TOK = re.compile(r"\*\*|__|!!|\(\(|\)\)|//|\||[^\s|]+?(?=\*\*|__|!!|\(\(|\)\)|//|\||\s|$)")


def _parse(line):
    """-> list of words: {w, st:set, ring:int|None, br:'|'|'//'|None (ngắt TRƯỚC chữ này)}"""
    st, ring, rid, out, pending = set(), None, 0, [], None
    flag = {"**": "pop", "__": "scr", "!!": "big"}
    for tok in _TOK.findall(line):
        if tok in flag:
            st ^= {flag[tok]}
        elif tok == "((":
            rid += 1; ring = rid
        elif tok == "))":
            ring = None
        elif tok in ("|", "//"):
            pending = tok
        else:
            out.append({"w": tok, "st": set(st), "ring": ring, "br": pending})
            pending = None
    return out


class Captions:
    def __init__(self, phrases, words, y, hide):
        self.phrases, self.words, self.y, self.hide = phrases, words, y, hide

    def t(self, text, nth=1):
        """Mốc thời gian (giây) của lần thứ nth chữ/cụm `text` được nói — để đặt đồ hoạ đúng từ khoá."""
        key = text.lower().split()
        flat = [re.sub(r"[^\w%]", "", w["w"].lower()) for w in self.words]
        key = [re.sub(r"[^\w%]", "", k) for k in key]
        hits = [i for i in range(len(flat)) if flat[i:i + len(key)] == key]
        assert len(hits) >= nth, f"không thấy '{text}' (lần {nth}) trong lines.txt"
        return self.words[hits[nth - 1]]["s"]


def captions(project_dir, y=((0, 300),), hide=(), maxw=CAP_MAXW):
    """y: [(từ giây, top px)] — đổi vị trí khi góc máy đổi (đầu người cao/thấp).
    hide: [(a, b)] — khoảng ẩn chữ (vd lúc hiện title card / thẻ ảnh lớn)."""
    segs = json.load(open(os.path.join(project_dir, "transcript.json")))
    fixed = [l.rstrip("\n") for l in open(os.path.join(project_dir, "lines.txt"), encoding="utf-8")]
    fixed = [l for l in fixed if l.strip() and not l.lstrip().startswith("#")]
    assert len(fixed) == len(segs), f"lines.txt có {len(fixed)} dòng, edl/transcript có {len(segs)} đoạn"
    words = []
    for seg, line in zip(segs, fixed):
        cw, ws = _parse(line), seg["words"]
        n, m = len(cw), len(ws)
        for i, w in enumerate(cw):
            if m:
                j = i if n == m else min(m - 1, int(i * m / n))
                w["s"], w["e"] = ws[j]["s"], ws[j]["e"]
            else:  # đoạn không nhận dạng được: chia đều
                span = (seg["end"] - seg["start"]) / max(n, 1)
                w["s"], w["e"] = seg["start"] + i * span, seg["start"] + (i + 1) * span
            w["seg"] = seg["start"]
            words.append(w)
        if cw:
            cw[0]["br"] = cw[0]["br"] or "seg"
    manual = {id(w) for w in words if w["br"] == "|"}
    phrases, cur = [], []
    for k, w in enumerate(words):
        prev = words[k - 1] if k else None
        new = (not cur or w["br"] in ("|", "seg")
               or prev["w"][-1] in ".!?:;"
               or (prev["w"][-1] == "," and len(cur) >= 2)
               or w["s"] - prev["e"] > 0.5
               or (len(cur) >= maxw and not any(id(x) in manual for x in words if x["seg"] == w["seg"])))
        if new and cur:
            phrases.append(cur); cur = []
        cur.append(w)
    if cur:
        phrases.append(cur)
    out = []
    for i, ph in enumerate(phrases):
        t0 = ph[0]["s"] - 0.04
        nxt = phrases[i + 1][0]["s"] - 0.04 if i + 1 < len(phrases) else 1e9
        t1 = min(nxt, ph[-1]["e"] + 0.7)
        out.append({"t0": round(t0, 3), "t1": round(t1, 3), "words": ph})
    return Captions(out, words, sorted(y), list(hide))


def _phrase_html(ph, y):
    lines, cur = [], []
    for w in ph["words"]:
        if w["br"] == "//" and cur:
            lines.append(cur); cur = []
        cur.append(w)
    lines.append(cur)
    out = []
    for li, ln in enumerate(lines):
        parts, k = [], 0
        while k < len(ln):
            w = ln[k]
            disp = w["w"].rstrip(",.;:") if w["w"][-1:] in ",.;:" else w["w"]
            span = (f'<span class="w {" ".join(sorted(w["st"]))}" data-t="{w["s"]:.3f}">'
                    f'{_html.escape(disp)}</span>')
            if w["ring"] and (k == 0 or ln[k - 1]["ring"] != w["ring"]):
                grp = [x for x in ln[k:] if x["ring"] == w["ring"]]
                inner = []
                for x in grp:
                    d = x["w"].rstrip(",.;:")
                    inner.append(f'<span class="w {" ".join(sorted(x["st"]))}" data-t="{x["s"]:.3f}">{_html.escape(d)}</span>')
                parts.append(f'<span class="ring" data-t="{w["s"]:.3f}">{" ".join(inner)}'
                             '<svg viewBox="0 0 100 40" preserveAspectRatio="none"><ellipse cx="50" cy="20" rx="49" ry="18" '
                             'pathLength="1"/></svg></span>')
                k += len(grp)
                continue
            parts.append(span)
            k += 1
        out.append(f'<div class="ln{" sub" if li else ""}">{" ".join(parts)}</div>')
    return f'<div class="ph" data-t0="{ph["t0"]}" data-t1="{ph["t1"]}" style="top:{y}px">{"".join(out)}</div>'


# ---------------------------------------------------------------- đồ hoạ phụ
def el(t0, t1, x, y, inner, rot=0, w=None, cls=""):
    """Phần tử bất kỳ, bật lên ở t0 và tắt ở t1. x, y = góc trên trái (px, khung 1080×1920)."""
    style = f"left:{x}px;top:{y}px;--r:{rot}deg;" + (f"width:{w}px;" if w else "")
    return f'<div class="el {cls}" data-t0="{t0}" data-t1="{t1}" style="{style}">{inner}</div>'


def txt(t0, t1, x, y, text, size=56, font="serif", color="#fffaf0", rot=0, align="left", w=None):
    """Chữ tự do. font: serif | sans | script."""
    return el(t0, t1, x, y, f'<div class="t {font}" style="font-size:{size}px;color:{color};text-align:{align}">{text}</div>',
              rot, w)


def img(t0, t1, x, y, src, w=160, rot=0, radius=18, shadow=True):
    """Ảnh/logo trong work/<slug>/assets (vd logo app, ảnh chụp màn hình nhỏ)."""
    return el(t0, t1, x, y, f'<img src="assets/{src}" style="width:{w}px;border-radius:{radius}px" '
                            f'class="{"sh" if shadow else ""}">', rot)


def card(t0, t1, src, source="", y=150, w=900, rot=-1.5):
    """Thẻ ảnh chụp màn hình lớn (biểu đồ, bài báo) ở phía trên + dòng nguồn nhỏ — kiểu 'Here's the data'."""
    cap = f'<div class="src">Nguồn: {_html.escape(source)}</div>' if source else ""
    return el(t0, t1, (1080 - w) // 2, y, f'<div class="card"><img src="assets/{src}" style="width:100%">{cap}</div>',
              rot, w)


def counter(t0, t1, x, y, v0, v1, dur=0.9, suffix="", prefix="", size=150, w=1080, align="center"):
    """Số chạy từ v0 tới v1 (vd 500 -> 95.000), kiểu kết quả trước/sau."""
    return el(t0, t1, x, y, f'<div class="t sans cnt" data-v0="{v0}" data-v1="{v1}" data-d="{dur}" data-p="{prefix}" '
                            f'data-s="{suffix}" style="font-size:{size}px;text-align:{align}">{prefix}{v1}{suffix}</div>',
              0, w)


def cloud(t0, t1, words, cx=540, cy=420, rx=380, ry=150, size=34, step=0.12):
    """Rải các chữ nhỏ quanh 1 tâm (kiểu 'Documentary · News · Commercials' quanh 'for Everything')."""
    out = []
    for i, wd in enumerate(words):
        a = -math.pi / 2 + i * 2 * math.pi / len(words) + 0.35
        x, y = cx + rx * math.cos(a) - 90, cy + ry * math.sin(a) - 20
        out.append(txt(t0 + i * step, t1, int(x), int(y), _html.escape(wd), size, "serif", rot=(i % 3 - 1) * 6, w=220,
                       align="center"))
    return "".join(out)


def sparkle(t0, t1, x, y, size=60):
    return el(t0, t1, x, y, f'<svg class="spk" width="{size}" height="{size}" viewBox="0 0 100 100">'
                            '<path d="M50 0 C54 38 62 46 100 50 C62 54 54 62 50 100 C46 62 38 54 0 50 C38 46 46 38 50 0Z"/>'
                            '</svg>')


def title_card(t0, t1, series, script_word, bold_word, meta, y=1080):
    """Thẻ tập của series, kiểu 'The diary of … / Journalist becoming Creator. / Eps #03 @handle'.
    series: tên series (studio.json → series.ten); meta: list dòng nhỏ (vd ['Eps #03', '@handle', 'Hà Nội'])."""
    m = "".join(f"<div>{_html.escape(x)}</div>" for x in meta)
    return (el(t0, t1, 0, 330, f'<div class="t serif ser">{_html.escape(series)}</div>', 0, 1080)
            + el(t0 + 0.15, t1, 0, y, f'<div class="tc"><div class="t script tcs">{_html.escape(script_word)}</div>'
                                      f'<div class="t sans tcb">{_html.escape(bold_word)}<span class="dot">.</span></div>'
                                      f'<div class="t serif tcm">{m}</div></div>', -2, 1080))


# ---------------------------------------------------------------- dựng overlay.html
def _ff(name, pat, weight, style="normal"):
    hits = glob.glob(f"{FONTS}/**/files/{pat}", recursive=True)
    if not hits:
        sys.exit(f"Thiếu font {pat} — chạy bash setup.sh")
    return (f"@font-face{{font-family:'{name}';src:url('file://{hits[0]}') format('woff2');"
            f"font-weight:{weight};font-style:{style};}}")


CSS = """
html,body{margin:0;width:1080px;height:1920px;background:transparent;overflow:hidden}
*{box-sizing:border-box}
.ph{position:absolute;left:0;width:1080px;text-align:center;display:none;font-size:%(cs)dpx}
.ln{white-space:nowrap;font-family:Serif;font-weight:500;font-size:1em;line-height:1.02;color:#fffaf0;letter-spacing:-1px;
  text-shadow:0 2px 4px rgba(0,0,0,.45),0 0 26px rgba(0,0,0,.30)}
.ln.sub{font-size:.76em;margin-top:-.12em;padding-left:200px}
.w{display:inline-block;opacity:0;will-change:transform}
.w.pop{font-family:Sans;font-weight:800;color:#eef36a;letter-spacing:-.03em}
.w.big{font-family:Sans;font-weight:800;font-size:1.45em;letter-spacing:-.04em;color:#fff}
.w.pop.big{color:#eef36a}
.w.scr{font-family:Script;font-weight:400;font-size:1.6em;color:#f6f2c8;letter-spacing:0;line-height:.75}
.ring{position:relative;display:inline-block;padding:0 .1em}
.ring svg{position:absolute;left:-12%%;top:-28%%;width:124%%;height:156%%;overflow:visible}
.ring ellipse{fill:none;stroke:#fffaf0;stroke-width:3;vector-effect:non-scaling-stroke;stroke-dasharray:1;
  stroke-dashoffset:var(--o,1);filter:drop-shadow(0 1px 2px rgba(0,0,0,.4))}
.el{position:absolute;opacity:0;transform-origin:50%% 50%%;will-change:transform}
.t{line-height:1.05;color:#fffaf0;text-shadow:0 2px 4px rgba(0,0,0,.45),0 0 22px rgba(0,0,0,.3)}
.serif{font-family:Serif;font-weight:500}
.sans{font-family:Sans;font-weight:800;letter-spacing:-.03em}
.script{font-family:Script;font-weight:400}
.sh{box-shadow:0 14px 34px rgba(0,0,0,.35)}
.card{background:#fff;padding:14px 14px 10px;border-radius:14px;box-shadow:0 18px 40px rgba(0,0,0,.35)}
.card img{display:block;border-radius:6px}
.card .src{font-family:Serif;font-size:26px;color:#555;padding-top:8px}
.spk path{fill:#fffaf0;filter:drop-shadow(0 1px 3px rgba(0,0,0,.4))}
.ser{text-align:center;font-size:34px;letter-spacing:2px}
.tc{text-align:center}
.tcs{font-size:150px;line-height:.7;margin-right:160px;color:#fffaf0}
.tcb{font-size:150px;line-height:.95}
.tcb .dot{color:#eef36a}
.tcm{font-size:30px;margin-top:40px;line-height:1.35}
"""

JS = """
const ph=[...document.querySelectorAll('.ph')], els=[...document.querySelectorAll('.el')];
const HIDE=%(hide)s, SEP='%(sep)s';
const ease=x=>1-Math.pow(1-x,3), cl=x=>Math.max(0,Math.min(1,x));
const back=x=>{const c1=1.70158,c3=c1+1;return 1+c3*Math.pow(x-1,3)+c1*Math.pow(x-1,2)};
let fitted=false;
function fit(){
  for(const p of ph){p.style.display='block';
    for(const l of p.querySelectorAll('.ln')){const w=l.scrollWidth;if(w>%(maxw)d)l.style.fontSize=(parseFloat(getComputedStyle(l).fontSize)*%(maxw)d/w)+'px'}
    p.style.display='none'}
  fitted=true;
}
const fmt=v=>Math.round(v).toString().replace(/\\B(?=(\\d{3})+(?!\\d))/g,SEP);
window.setT=function(t){
  if(!fitted)fit();
  const hidden=HIDE.some(h=>t>=h[0]&&t<h[1]);
  for(const p of ph){
    const on=!hidden&&t>=+p.dataset.t0&&t<+p.dataset.t1;
    p.style.display=on?'block':'none'; if(!on)continue;
    for(const w of p.querySelectorAll('.w')){
      const s=w.classList.contains('scr');
      const a=cl((t-(+w.dataset.t))/(s?0.30:0.14));
      w.style.opacity=ease(a);
      w.style.transform=s?`translateY(${(1-ease(a))*20}px) rotate(${(1-ease(a))*-6}deg) scale(${0.9+0.1*ease(a)})`
                         :`translateY(${(1-ease(a))*14}px) scale(${0.94+0.06*back(a)})`;
    }
    for(const r of p.querySelectorAll('.ring'))r.style.setProperty('--o',1-ease(cl((t-(+r.dataset.t)-0.1)/0.45)));
  }
  for(const e of els){
    const t0=+e.dataset.t0,t1=+e.dataset.t1;
    if(t<t0-0.01||t>t1+0.01){e.style.opacity=0;continue}
    const a=cl((t-t0)/0.28),b=cl((t1-t)/0.15);
    e.style.opacity=Math.min(ease(a),b);
    e.style.transform=`translateY(${(1-ease(a))*20}px) rotate(var(--r)) scale(${a<1?0.85+0.15*back(a):1})`;
    for(const c of e.querySelectorAll('.cnt')){
      const p=ease(cl((t-t0)/(+c.dataset.d)));
      c.textContent=c.dataset.p+fmt(+c.dataset.v0+(+c.dataset.v1-(+c.dataset.v0))*p)+c.dataset.s;
    }
  }
};
"""


def build(E, C, work_dir, maxw=MAX_WIDTH):
    fonts = "".join(_ff(n, f"{fam}-{sub}-{w}-{st}.woff2", w, st)
                    for n, fam, w, st in [("Serif", "newsreader", 500, "normal"), ("Serif", "newsreader", 500, "italic"),
                                          ("Sans", "inter-tight", 800, "normal"), ("Script", "great-vibes", 400, "normal")]
                    for sub in ("vietnamese", "latin", "latin-ext"))
    yat = lambda t: [y for (a, y) in C.y if a <= t + 0.05][-1] if any(a <= t + 0.05 for a, _ in C.y) else C.y[0][1]
    phr = "".join(_phrase_html(p, yat(p["t0"])) for p in C.phrases)
    css = fonts + CSS % {"cs": CAP_SIZE}
    js = JS % {"hide": json.dumps(C.hide), "sep": THOUSANDS, "maxw": maxw}
    out = os.path.join(work_dir, "overlay.html")
    open(out, "w", encoding="utf-8").write(
        f'<!doctype html><html><head><meta charset="utf-8"><style>{css}</style></head>'
        f'<body>{phr}{"".join(E)}<script>{js}</script></body></html>')
    print(f"{len(C.phrases)} cụm chữ, {len(E)} đồ hoạ -> {out}")
