"""Audit: every wedge/right-angle ray must lie on textbook ink or on a line drawn in this or an earlier step.
Import after lib; call install(fig_dir) before building; report() after."""
import math, lib
from refine import _ink, seg_score

LOG = []          # (fig, step, kind, v, p) rays
LINES = []        # (fig, step, a, b)
_cur = {'fig': None, 'step': 0}
_ow, _or, _ol, _os = lib.wedge, lib.right, lib.line, lib.solve

REC = {}
def wedge(v, p1, p2, *a, **k):
    s = _ow(v, p1, p2, *a, **k); REC[s] = ('ray', '각', v, p1, p2); return s
def right(v, p1, p2, *a, **k):
    s = _or(v, p1, p2, *a, **k); REC[s] = ('ray', '직각', v, p1, p2); return s
def line(a, b, *x, **k):
    s = _ol(a, b, *x, **k); REC[s] = ('line', a, b); return s
def solve(label, title, fig, steps, *a, **k):
    for i, (_, els) in enumerate(steps):
        for e in els:
            r = REC.get(e)
            if not r: continue
            if r[0] == 'line': LINES.append((fig, i, r[1], r[2], label))
            else:
                LOG.append((fig, i, r[1], r[2], r[3], label)); LOG.append((fig, i, r[1], r[2], r[4], label))
    return _os(label, title, fig, steps, *a, **k)

def install(g):
    for n, f in (('wedge', wedge), ('right', right), ('line', line), ('solve', solve)):
        setattr(lib, n, f); g[n] = f

class Step:  # used as: with fig('m01'): steps built in order via st(i)
    pass

def begin(fig): _cur['fig'] = fig; _cur['step'] = 0
def st(i): _cur['step'] = i

def _on_line(v, p, a, b):
    # ray v->p (first 30px) lies along segment a-b ?
    def dist(q):
        ax, ay = a; bx, by = b; L2 = (bx-ax)**2 + (by-ay)**2 or 1
        t = max(0, min(1, ((q[0]-ax)*(bx-ax) + (q[1]-ay)*(by-ay)) / L2))
        return math.hypot(q[0]-ax-t*(bx-ax), q[1]-ay-t*(by-ay))
    d = math.hypot(p[0]-v[0], p[1]-v[1]) or 1
    q = (v[0]+(p[0]-v[0])/d*25, v[1]+(p[1]-v[1])/d*25)
    return dist(v) < 3 and dist(q) < 3

def report(fig_dir):
    bad = []; cache = {}
    for fig, step, kind, v, p, label in LOG:
        if fig not in cache: cache[fig] = _ink(f'{fig_dir}/{fig}.png')
        d = math.hypot(p[0]-v[0], p[1]-v[1]) or 1
        q = (v[0]+(p[0]-v[0])/d*40, v[1]+(p[1]-v[1])/d*40)
        ink = seg_score(cache[fig], v, q, trim=6)
        drawn = any(f == fig and s <= step and _on_line(v, p, a, b) for f, s, a, b, _ in LINES)
        if ink < 70 and not drawn:
            bad.append((label, step+1, kind, tuple(round(x) for x in v), tuple(round(x) for x in p), round(ink)))
    return bad
