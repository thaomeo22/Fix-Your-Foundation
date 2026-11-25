"""Thư viện đồ hoạ scrapbook (theo style video mẫu) + phụ đề từng cụm chữ.
Mỗi project viết graphics.py: from lib import *; E = [...]; build(E, PROJECT_DIR)"""
import json, os, glob, math, sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
FONTS = os.path.join(ROOT, ".cache", "fonts")


def load_captions(transcript_path, lines_path, hide_before=0.0, total=None):
    """Ghép lời đã sửa chính tả (lines.txt, 1 dòng = 1 segment Whisper) vào mốc thời gian từng từ."""
    segs = json.load(open(transcript_path))
    fixed = [l.strip() for l in open(lines_path, encoding="utf-8") if l.strip()]
    assert len(fixed) == len(segs), f"lines.txt có {len(fixed)} dòng, transcript có {len(segs)} segment"
    caps = []
    for seg, text in zip(segs, fixed):
        ws, cw = seg["words"], text.split()
        n, m = len(cw), len(ws)
        timed = [(ws[i if n == m else min(m - 1, int(i * m / n))]["s"], ws[i if n == m else min(m - 1, int(i * m / n))]["e"], w)
                 for i, w in enumerate(cw)]
        chunk = []
        for k, (s, e, w) in enumerate(timed):
            chunk.append((s, e, w))
            if w[-1] in ",.:" or chunk[-1][1] - chunk[0][0] >= 0.42 or len(chunk) == 3 or k == len(timed) - 1:
                caps.append([round(chunk[0][0], 2), " ".join(x[2] for x in chunk).rstrip(",.:")])
                chunk = []
    end = total or (segs[-1]["end"] + 0.5)
    for i in range(len(caps)):
        nxt = caps[i + 1][0] if i + 1 < len(caps) else end
        caps[i].append(round(min(nxt, caps[i][0] + 1.6), 2))
    return [c for c in caps if c[0] >= hide_before]


def star(n, size=96, color="#f2c94c"):
    pts = []
    import math
    for i in range(10):
        r = 48 if i % 2 == 0 else 22
        a = math.pi / 2 + i * math.pi / 5
        pts.append(f"{50 + r * math.cos(a):.1f},{50 - r * math.sin(a):.1f}")
    return (f'<div class="star" style="width:{size}px;height:{size}px">'
            f'<svg viewBox="0 0 100 100"><polygon points="{" ".join(pts)}" fill="{color}" stroke="#3a2f1e" stroke-width="2.5" stroke-linejoin="round"/></svg>'
            f'<span>{n}</span></div>')

def el(t0, t1, x, y, html, rot=0, w=None, cls=""):
    style = f"left:{x}px;top:{y}px;--r:{rot}deg;" + (f"width:{w}px;" if w else "")
    return f'<div class="el {cls}" data-t0="{t0}" data-t1="{t1}" style="{style}">{html}</div>'

def paper(inner, tape=True, cls="paper"):
    return f'<div class="{cls}">' + ('<i class="tape"></i>' if tape else "") + inner + "</div>"

R = lambda t, inner, cls="": f'<div class="rv {cls}" data-t="{t}">{inner}</div>'
S = lambda t, inner: f'<span class="strike" data-t="{t}">{inner}</span>'
H = lambda t, inner: f'<span class="hl" data-t="{t}">{inner}</span>'



def _ff(name, pat, weight, style="normal"):
    hits = glob.glob(f"{FONTS}/*/**/files/{pat}", recursive=True)
    if not hits:
        sys.exit(f"Thiếu font {pat} — chạy bash setup.sh")
    return (f"@font-face{{font-family:'{name}';src:url('file://{hits[0]}') format('woff2');"
            f"font-weight:{weight};font-style:{style};}}")


def build(E, caps, out_html):
    fonts = "".join(_ff(n, f"{fam}-{sub}-{w}-{st}.woff2", w, st)
                    for n, fam, w, st in [("Fraunces", "fraunces", 800, "normal"), ("Fraunces", "fraunces", 700, "normal"),
                                          ("Fraunces", "fraunces", 600, "italic"), ("Dancing", "dancing-script", 600, "normal"),
                                          ("Hand", "patrick-hand", 400, "normal"), ("Mono", "ibm-plex-mono", 500, "normal")]
                    for sub in ("vietnamese", "latin"))
    css = fonts + """
    html,body{margin:0;width:1080px;height:1920px;background:transparent;overflow:hidden}
    *{box-sizing:border-box}
    .el{position:absolute;opacity:0;transform-origin:50% 40%;will-change:transform}
    .hook{width:1080px}
    .title{font-family:Fraunces;font-weight:800;font-size:132px;line-height:1;color:#f8eda0;text-align:center;
      text-shadow:0 4px 18px rgba(0,0,0,.35),0 1px 0 rgba(0,0,0,.25);letter-spacing:-2px}
    .script{font-family:Dancing;font-weight:600;font-size:64px;color:#fff;text-shadow:0 2px 10px rgba(0,0,0,.45)}
    .paper{position:relative;background:#fbf6ea;padding:34px 38px 30px;border-radius:3px;
      box-shadow:0 14px 30px rgba(0,0,0,.28),0 2px 4px rgba(0,0,0,.15);
      background-image:repeating-linear-gradient(0deg,rgba(120,100,60,.035) 0 2px,transparent 2px 5px)}
    .paper.torn{clip-path:polygon(0 3%,6% 0,14% 2%,22% 0,31% 3%,40% 1%,52% 3%,61% 0,72% 2%,83% 0,92% 3%,100% 1%,99% 96%,92% 100%,81% 97%,70% 100%,58% 97%,47% 100%,36% 97%,24% 100%,13% 97%,4% 100%,0 97%)}
    .tape{position:absolute;top:-24px;left:50%;width:150px;height:46px;margin-left:-75px;transform:rotate(-4deg);
      background:rgba(232,218,182,.82);box-shadow:0 1px 3px rgba(0,0,0,.12)}
    .sticky{position:relative;background:#fbef8f;padding:40px 40px 26px;
      background-image:repeating-linear-gradient(180deg,transparent 0 63px,rgba(90,120,200,.35) 63px 65px);
      box-shadow:0 14px 30px rgba(0,0,0,.28)}
    .sticky .row{display:flex;align-items:center;gap:14px;height:66px}
    .mono{font-family:Mono;font-weight:500;font-size:30px;color:#4a4237;letter-spacing:1px;text-transform:lowercase}
    .hand{font-family:Hand;font-size:46px;color:#2c2620;line-height:1.15}
    .hand.big{font-size:60px}
    .serif{font-family:Fraunces;font-weight:700;font-size:72px;color:#2c2620;line-height:1.05}
    .red{color:#c8433a}
    .num{font-family:Fraunces;font-weight:800;font-size:150px;line-height:1}
    .num.grey{color:#8a8173}.num.red{color:#c8433a}
    .label{display:inline-block;font-family:Mono;font-weight:500;font-size:34px;color:#2a2620;
      background:linear-gradient(100deg,rgba(248,228,92,.0) 0,rgba(248,228,92,.95) 3%,rgba(248,228,92,.95) 97%,rgba(248,228,92,0) 100%);
      padding:8px 22px;box-shadow:0 6px 14px rgba(0,0,0,.18)}
    .label.lg{font-size:40px;padding:10px 26px}
    .paper .label{font-size:30px;padding:4px 14px;margin-bottom:8px;box-shadow:none}
    .hdr{display:flex;align-items:center;gap:6px}
    .star{position:relative;flex:none;filter:drop-shadow(0 4px 6px rgba(0,0,0,.25))}
    .star svg{width:100%;height:100%}
    .star span{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;
      font-family:Hand;font-size:46px;color:#3a2f1e;padding-top:4px}
    .sticky .star span{font-size:34px}
    .tick{font-family:Hand;font-size:44px;color:#2f8a4e}
    .cross{font-family:Hand;font-size:44px;color:#c8433a}
    .strike{position:relative;display:inline-block}
    .strike::after{content:"";position:absolute;left:-4%;top:52%;height:7px;width:108%;background:#d2463c;border-radius:4px;
      transform-origin:0 50%;transform:scaleX(var(--s,0)) rotate(-2deg)}
    .hl{position:relative;display:inline-block;z-index:0}
    .hl::before{content:"";position:absolute;left:-6px;right:-6px;bottom:4%;height:46%;background:rgba(248,214,72,.85);z-index:-1;
      transform-origin:0 50%;transform:scaleX(var(--s,0))}
    .rv{opacity:0}
    #cap{position:absolute;left:70px;top:1240px;font-family:Fraunces;font-style:italic;font-weight:600;font-size:58px;color:#fffaf0;
      text-shadow:0 2px 3px rgba(0,0,0,.55),0 0 18px rgba(0,0,0,.45);white-space:nowrap}
    """

    js = """
    const CAPS=%s;
    const els=[...document.querySelectorAll('.el')];
    const ease=x=>1-Math.pow(1-x,3);
    const back=x=>{const c1=1.70158,c3=c1+1;return 1+c3*Math.pow(x-1,3)+c1*Math.pow(x-1,2)};
    const cl=x=>Math.max(0,Math.min(1,x));
    window.setT=function(t){
      for(const e of els){
        const t0=+e.dataset.t0,t1=+e.dataset.t1;
        if(t<t0-0.01||t>t1+0.01){e.style.opacity=0;continue}
        const a=cl((t-t0)/0.32), b=cl((t1-t)/0.22);
        const sc=(a<1?0.82+0.18*back(a):1)*(b<1?0.94+0.06*b:1);
        const wob=Math.sin((t-t0)*1.6)*0.6;
        e.style.opacity=Math.min(ease(a),b);
        e.style.transform=`translateY(${(1-ease(a))*24}px) rotate(calc(var(--r) + ${wob+(1-ease(a))*-4}deg)) scale(${sc})`;
        for(const r of e.querySelectorAll('.rv')){
          const p=cl((t-(+r.dataset.t))/0.28);
          r.style.opacity=ease(p); r.style.transform=`translateY(${(1-ease(p))*18}px) scale(${0.9+0.1*back(p)})`;
        }
        for(const s of e.querySelectorAll('.strike,.hl')){
          s.style.setProperty('--s',ease(cl((t-(+s.dataset.t))/0.35)));
        }
      }
      const cap=document.getElementById('cap');
      const c=CAPS.find(c=>t>=c[0]&&t<c[2]);
      if(c){const p=cl((t-c[0])/0.12);cap.textContent=c[1];cap.style.opacity=p;cap.style.transform=`translateY(${(1-p)*10}px)`}
      else cap.style.opacity=0;
    };
    """ % json.dumps(caps, ensure_ascii=False)

    html = f"""<!doctype html><html><head><meta charset="utf-8"><style>{css}</style></head>
<body>{''.join(E)}<div id="cap"></div><script>{js}</script></body></html>"""
    open(out_html, "w").write(html)
    print(len(E), "elements,", len(caps), "captions ->", out_html)
