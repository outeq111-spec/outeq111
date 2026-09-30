import math, base64, io, re, html as H
from PIL import Image

B = '/tmp/claude-0/-home-user-outeq111/d86e19ab-ec80-5ac1-a09b-c4db87ef5a17/ch2'
R, BL, G, OR, PU = '#E4572E', '#1F6FB2', '#2E9E5B', '#D9822B', '#8E44AD'
COLORS = {'r': R, 'b': BL, 'g': G, 'o': '#B5651D', 'p': PU}
BG1, BG2, DARK, TEAL = '#F7F6F1', '#EEF4F4', '#1E2A3A', '#1F7A8C'
FONT = "'Noto Sans KR','Apple SD Gothic Neo','Malgun Gothic','Nanum Gothic',sans-serif"

_pages = {}
def page(n):
    if n not in _pages:
        _pages[n] = Image.open(f'{B}/h{n}.png').convert('RGB')
    return _pages[n]

def crop_uri(p, box):
    im = page(p).crop(box)
    if im.width > 1700:
        im = im.resize((1700, round(im.height*1700/im.width)), Image.LANCZOS)
    buf = io.BytesIO(); im.save(buf, 'JPEG', quality=85)
    return 'data:image/jpeg;base64,' + base64.b64encode(buf.getvalue()).decode(), im.size

def fig_uri(name):
    im = Image.open(f'{B}/fg/{name}.png').convert('RGB')
    buf = io.BytesIO(); im.save(buf, 'PNG', optimize=True)
    return 'data:image/png;base64,' + base64.b64encode(buf.getvalue()).decode(), im.size

def rich(s):
    s = H.escape(s)
    s = re.sub(r'\[(\w)\](.*?)\[/\1\]', lambda m: f'<b style="color:{COLORS[m.group(1)]}">{m.group(2)}</b>', s)
    s = s.replace('\n', '<br>')
    return s

# ---------- svg primitives (figure pixel units) ----------
def _pt(p): return f'{p[0]:.1f},{p[1]:.1f}'
def line(a, b, c=R, w=3, dash=False):
    d = ' stroke-dasharray="7 4"' if dash else ''
    return f'<line x1="{a[0]}" y1="{a[1]}" x2="{b[0]}" y2="{b[1]}" stroke="{c}" stroke-width="{w}" stroke-linecap="round"{d}/>'
def poly(pts, c=BL, op=0.2, stroke=None):
    s = f' stroke="{stroke}" stroke-width="2.5"' if stroke else ''
    return f'<polygon points="{" ".join(_pt(p) for p in pts)}" fill="{c}" fill-opacity="{op}"{s}/>'
def dot(p, c=R, r=5):
    return f'<circle cx="{p[0]}" cy="{p[1]}" r="{r}" fill="{c}"/>'
def text(p, s, c=R, size=26, anchor='start'):
    return (f'<text x="{p[0]}" y="{p[1]}" font-size="{size}" font-family="Arial, sans-serif" font-weight="700" '
            f'fill="{c}" stroke="#FFFFFF" stroke-width="5" paint-order="stroke" text-anchor="{anchor}">{H.escape(s)}</text>')
def lab(p, s, dx=10, dy=-10):
    return text((p[0]+dx, p[1]+dy), s, DARK, 24)
def _ang(v, p): return math.atan2(p[1]-v[1], p[0]-v[0])
def wedge(v, p1, p2, r=34, c=R, op=0.45, reflex=False):
    a1, a2 = _ang(v, p1), _ang(v, p2)
    d = (a2 - a1) % (2*math.pi)
    if (d > math.pi) != reflex:
        a1, a2 = a2, a1; d = 2*math.pi - d
    s = (v[0]+r*math.cos(a1), v[1]+r*math.sin(a1)); e = (v[0]+r*math.cos(a2), v[1]+r*math.sin(a2))
    large = 1 if d > math.pi else 0
    return (f'<path d="M{_pt(v)} L{_pt(s)} A{r},{r} 0 {large} 1 {_pt(e)} Z" fill="{c}" fill-opacity="{op}" '
            f'stroke="{c}" stroke-width="2"/>')
def right(v, p1, p2, s=14, c=R):
    def u(p):
        dx, dy = p[0]-v[0], p[1]-v[1]; n = math.hypot(dx, dy); return dx/n, dy/n
    u1, u2 = u(p1), u(p2)
    a = (v[0]+u1[0]*s, v[1]+u1[1]*s); b = (a[0]+u2[0]*s, a[1]+u2[1]*s); cc = (v[0]+u2[0]*s, v[1]+u2[1]*s)
    return f'<path d="M{_pt(a)} L{_pt(b)} L{_pt(cc)}" fill="none" stroke="{c}" stroke-width="2.5"/>'
def arc(cen, r, p1, p2, via, c=R, w=6):
    a1, a2, av = _ang(cen, p1), _ang(cen, p2), _ang(cen, via)
    d = (a2 - a1) % (2*math.pi); dv = (av - a1) % (2*math.pi)
    sweep = 1
    if dv > d:  # via not on clockwise path -> go other way
        sweep = 0; d = 2*math.pi - d
    s = (cen[0]+r*math.cos(a1), cen[1]+r*math.sin(a1)); e = (cen[0]+r*math.cos(a2), cen[1]+r*math.sin(a2))
    large = 1 if d > math.pi else 0
    return f'<path d="M{_pt(s)} A{r},{r} 0 {large} {sweep} {_pt(e)}" fill="none" stroke="{c}" stroke-width="{w}" stroke-linecap="round" stroke-opacity="0.85"/>'
def circle(cen, r, c=R, op=0.15, stroke=None):
    s = f' stroke="{stroke}" stroke-width="3"' if stroke else ''
    return f'<circle cx="{cen[0]}" cy="{cen[1]}" r="{r}" fill="{c}" fill-opacity="{op}"{s}/>'
def inter(a, b, c, d):
    x1, y1 = a; x2, y2 = b; x3, y3 = c; x4, y4 = d
    den = (x1-x2)*(y3-y4) - (y1-y2)*(x3-x4)
    t = ((x1-x3)*(y3-y4) - (y1-y3)*(x3-x4)) / den
    return (round(x1+t*(x2-x1), 1), round(y1+t*(y2-y1), 1))

# ---------- slide builders ----------
def _sec(bg, inner, notes=''):
    a = f'<aside>{H.escape(notes)}</aside>' if notes else ''
    return (f'<section style="background:{bg}; color:{DARK}; font-family:{FONT}; padding:96px; display:flex; flex-direction:column">'
            f'{inner}{a}</section>')

def _head(label, title, accent=TEAL):
    s = f'<p style="position:absolute; left:96px; top:44px; width:1700px; font-size:30px; font-weight:700; color:{accent}">{H.escape(label)}</p>'
    if title:
        s += f'<p style="position:absolute; left:96px; top:90px; width:1728px; font-size:44px; font-weight:700; line-height:1.3">{rich(title)}</p>'
    return s

def cover(title, sub, eyebrow):
    inner = (f'<div style="display:flex; flex-direction:column; justify-content:center; gap:32px; height:100%">'
             f'<p style="font-size:32px; font-weight:700; color:#7CC6D2">{H.escape(eyebrow)}</p>'
             f'<h1 style="font-size:120px; font-weight:900; line-height:1.1; color:#F7F6F1">{rich(title.replace("<br>", chr(10)))}</h1>'
             f'<p style="font-size:36px; color:#BFD8D5">{H.escape(sub)}</p></div>')
    return f'<section style="background:{DARK}; color:#F7F6F1; font-family:{FONT}; padding:128px; display:flex; flex-direction:column">{inner}</section>'

def crops(label, title, imgs, builds=(), notes='', bg=BG1, area=None, accent=TEAL):
    """imgs: list of (page, box) stacked vertically in area; builds: list of text pills revealed in order."""
    top = 180 if title else 120
    x0, y0, W, Hh = area or (96, top, 1728, (700 if builds else 860) - (top-120))
    data = [crop_uri(p, b) for p, b in imgs]
    gap = 24
    totw = max(s[0] for _, s in data); toth = sum(s[1] for _, s in data) + gap*(len(data)-1)
    k = min(W/totw, Hh/toth)
    out = _head(label, title, accent)
    y = y0
    for uri, (w, h) in data:
        ww, hh = w*k, h*k
        out += f'<img src="{uri}" style="position:absolute; left:{x0+(W-ww)/2:.0f}px; top:{y:.0f}px; width:{ww:.0f}px; height:{hh:.0f}px; background:#FFFFFF; border-radius:12px">'
        y += hh + gap
    by = max(y + 10, 820) if builds else 0
    by = min(by, 880)
    for i, b in enumerate(builds):
        out += (f'<p data-build-in="rise {i+1}" style="position:absolute; left:96px; top:{by + i*0:.0f}px; width:1728px; font-size:38px; line-height:1.4; '
                f'background:#FCE0C4; padding:18px 28px; border-radius:14px">{rich(b)}</p>') if len(builds) == 1 else ''
    if len(builds) > 1:
        # stack pills upward from bottom
        n = len(builds); h1 = 88
        for i, b in enumerate(builds):
            yy = 1000 - (n - i) * (h1 + 12)
            out += (f'<p data-build-in="rise {i+1}" style="position:absolute; left:96px; top:{yy}px; width:1728px; font-size:36px; line-height:1.3; '
                    f'background:#FCE0C4; padding:14px 28px; border-radius:14px">{rich(b)}</p>')
    return _sec(bg, out, notes)

def solve(label, title, fig, steps, answer=None, notes='', bg=BG2, accent=TEAL, figmax=(880, 760), stepfont=40):
    """fig: figure name; steps: list of (text, [svg elements])"""
    uri, (w, h) = fig_uri(fig)
    k = min(figmax[0]/w, figmax[1]/h)
    fw, fh = w*k, h*k
    top = 200
    out = _head(label, title, accent)
    box = f'position:absolute; left:96px; top:{top}px; width:{fw:.0f}px; height:{fh:.0f}px'
    out += f'<img src="{uri}" style="{box}; background:#FFFFFF; border-radius:14px">'
    for i, (_, els) in enumerate(steps):
        if els:
            out += f'<svg data-build-in="fade {i+1}" style="{box}" viewBox="0 0 {w} {h}">{"".join(els)}</svg>'
    sx = 96 + fw + 56; sw = 1824 - sx
    y = top
    per_line = max(10, int(sw / (stepfont*0.95)))
    for i, (t, _) in enumerate(steps):
        lines = sum(max(1, math.ceil(len(seg)/per_line)) for seg in re.sub(r'\[/?\w\]', '', t).split('\n'))
        out += f'<p data-build-in="rise {i+1}" style="position:absolute; left:{sx:.0f}px; top:{y:.0f}px; width:{sw:.0f}px; font-size:{stepfont}px; line-height:1.4">{rich(t)}</p>'
        y += lines*stepfont*1.4 + 34
    if answer:
        ay = max(y + 10, 840)
        out += (f'<p data-build-in="pop {len(steps)+1}" style="position:absolute; left:{sx:.0f}px; top:{min(ay, 900):.0f}px; width:{min(sw, 800):.0f}px; font-size:42px; font-weight:700; '
                f'background:#FCE0C4; padding:18px 30px; border-radius:16px">{rich(answer)}</p>')
    return _sec(bg, out, notes)

def textslide(label, title, steps, notes='', bg=BG2, accent=TEAL, answer=None):
    out = _head(label, title, accent)
    y = 200
    for i, t in enumerate(steps):
        lines = sum(max(1, math.ceil(len(seg)/46)) for seg in re.sub(r'\[/?\w\]', '', t).split('\n'))
        out += f'<p data-build-in="rise {i+1}" style="position:absolute; left:96px; top:{y:.0f}px; width:1728px; font-size:36px; line-height:1.45">{rich(t)}</p>'
        y += lines*36*1.45 + 36
    if answer:
        out += (f'<p data-build-in="pop {len(steps)+1}" style="position:absolute; left:96px; top:{max(y+10, 840):.0f}px; width:1300px; font-size:40px; font-weight:700; '
                f'background:#FCE0C4; padding:18px 30px; border-radius:16px">{rich(answer)}</p>')
    return _sec(bg, out, notes)

import os as _os
SHELL = open(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), 'shell.html')).read()
def write(path, title, sections):
    open(path, 'w').write(SHELL.replace('%%TITLE%%', H.escape(title)).replace('%%SLIDES%%', '\n'.join(sections)))
