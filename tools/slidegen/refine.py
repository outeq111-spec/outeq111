"""Snap hand-read figure coordinates onto the actual ink of the textbook figure.

refine(img_path, pts, edges, circle=None) -> (pts, circle)
  pts:    {name: (x, y)} rough coordinates (figure pixel units)
  edges:  [(a, b), ...] textbook line segments between named points
  circle: ((cx, cy), r) rough circle, or None
Points are moved (coordinate descent, ±R px) to maximise mean ink along their
incident segments; points marked on the circle are also pulled onto it.
"""
import math
import numpy as np
from PIL import Image, ImageFilter

def _ink(path):
    im = Image.open(path).convert('L').filter(ImageFilter.GaussianBlur(0.8))
    a = 255.0 - np.asarray(im, dtype=float)
    return a

def _sample(a, x, y):
    h, w = a.shape
    x = min(max(x, 0), w - 1.001); y = min(max(y, 0), h - 1.001)
    x0, y0 = int(x), int(y); fx, fy = x - x0, y - y0
    return (a[y0, x0]*(1-fx)*(1-fy) + a[y0, x0+1]*fx*(1-fy) + a[y0+1, x0]*(1-fx)*fy + a[y0+1, x0+1]*fx*fy)

def seg_score(a, p, q, trim=5):
    L = math.hypot(q[0]-p[0], q[1]-p[1])
    if L < 2*trim + 2: return 0.0
    n = max(8, int(L/2))
    s = 0.0
    for i in range(n):
        t = (trim + (L - 2*trim) * i/(n-1)) / L
        s += _sample(a, p[0] + (q[0]-p[0])*t, p[1] + (q[1]-p[1])*t)
    return s / n

def fit_circle(a, c, r, band=16):
    xs, ys = [], []
    for k in range(360):
        th = math.radians(k)
        best, bv = None, 0
        for d in np.arange(-band, band+0.01, 0.5):
            x, y = c[0] + (r+d)*math.cos(th), c[1] + (r+d)*math.sin(th)
            v = _sample(a, x, y)
            if v > bv: bv, best = v, (x, y)
        if bv > 90: xs.append(best[0]); ys.append(best[1])
    xs, ys = np.array(xs), np.array(ys)
    for _ in range(3):  # least squares + outlier trim
        A = np.c_[2*xs, 2*ys, np.ones(len(xs))]; b = xs**2 + ys**2
        cx, cy, k = np.linalg.lstsq(A, b, rcond=None)[0]
        rr = math.sqrt(k + cx*cx + cy*cy)
        res = np.abs(np.hypot(xs-cx, ys-cy) - rr)
        keep = res < max(1.5, np.percentile(res, 80))
        xs, ys = xs[keep], ys[keep]
    return (round(cx, 1), round(cy, 1)), round(rr, 1)

def refine(path, pts, edges, circle=None, oncircle=(), R=10, step=0.5, iters=4, fixed=(), fitted=None):
    a = _ink(path)
    pts = {k: (float(v[0]), float(v[1])) for k, v in pts.items()}
    if fitted: circle = fitted
    elif circle:
        circle = fit_circle(a, circle[0], circle[1])
    inc = {k: [] for k in pts}
    for u, v in edges:
        inc[u].append(v); inc[v].append(u)
    def proj(k, p):
        if circle and k in oncircle:
            (cx, cy), r = circle
            th = math.atan2(p[1]-cy, p[0]-cx)
            return (cx + r*math.cos(th), cy + r*math.sin(th))
        return p
    for k in pts: pts[k] = proj(k, pts[k])
    for _ in range(iters):
        for k in pts:
            if not inc[k] or k in fixed: continue
            x0, y0 = pts[k]
            best, bv = pts[k], -1
            for dx in np.arange(-R, R+0.01, step):
                for dy in np.arange(-R, R+0.01, step):
                    p = proj(k, (x0+dx, y0+dy))
                    v = sum(seg_score(a, p, pts[m]) for m in inc[k])
                    if v > bv: bv, best = v, p
            pts[k] = best
        R = max(2, R*0.6)
    return {k: (round(v[0], 1), round(v[1], 1)) for k, v in pts.items()}, circle

def check(path, pts, edges, circle, out, scale=4):
    """Diagnostic: draw fitted segments/circle thinly in red over the figure."""
    from PIL import ImageDraw
    im = Image.open(path).convert('RGB')
    im = im.resize((im.width*scale, im.height*scale), Image.LANCZOS)
    d = ImageDraw.Draw(im)
    if circle:
        (cx, cy), r = circle
        d.ellipse([(cx-r)*scale, (cy-r)*scale, (cx+r)*scale, (cy+r)*scale], outline=(0, 160, 255), width=1)
    for u, v in edges:
        d.line([pts[u][0]*scale, pts[u][1]*scale, pts[v][0]*scale, pts[v][1]*scale], fill=(255, 0, 0), width=1)
    for k, p in pts.items():
        d.ellipse([p[0]*scale-4, p[1]*scale-4, p[0]*scale+4, p[1]*scale+4], outline=(255, 0, 255), width=2)
        d.text((p[0]*scale+6, p[1]*scale+4), k, fill=(200, 0, 200))
    im.save(out)
