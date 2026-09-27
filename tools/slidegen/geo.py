"""Edges (textbook segments) and rough circles per figure; G() snaps points to the ink."""
import json, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from refine import refine, check, fit_circle, _ink

FIG = '/tmp/claude-0/-home-user-outeq111/d86e19ab-ec80-5ac1-a09b-c4db87ef5a17/ch2/fg'
CACHE = os.path.join(os.path.dirname(__file__), 'geo_cache.json')
CHK = '/tmp/claude-0/-home-user-outeq111/d86e19ab-ec80-5ac1-a09b-c4db87ef5a17/chk'

E = lambda s: [tuple(x.split('-')) for x in s.split()]
SPEC = {
    'pre1':  (E('BL-A A-BR BL-E'), None, ''),
    'pre2a': (E('O-T O-R T-R O-L O-Rb L-Rb'), ((165, 150), 135), 'T R L Rb'),
    'pre2b': (E('O-L1 O-L2 O-R1 O-R2'), ((255, 145), 136), 'L1 L2 R1 R2'),
    'def':   (E('P-A P-B O-A O-B'), ((185, 200), 158), 'P A B'),
    'c1':    (E('P-A P-O O-B O-A'), ((180, 168), 145), 'P A B'),
    'c2':    (E('P-A P-B O-A O-B P-Q'), ((170, 200), 148), 'P A B Q'),
    'p1':    (E('P-Q P-A P-B O-A O-B'), ((180, 225), 150), 'P Q A B'),
    'semi':  (E('A-B P-A P-B'), ((212, 200), 158), 'P A B'),
    'p2a':   (E('T-A T-B O-A O-B'), ((208, 164), 146), 'T A B'),
    'p2b':   (E('L-O O-R L-M O-M'), ((201, 164), 146), 'L M R'),
    'p2c':   (E('O-L O-R P-L P-R'), ((190, 164), 148), 'L R P'),
    'p3a':   (E('T-A T-B O-A O-B R-A R-B'), ((207, 163), 148), 'T A B R'),
    'p3b':   (E('A-B A-D C-O O-B C-D'), ((203, 170), 148), 'A B C D'),
    'p3c':   (E('A-C A-D B-C B-D O-C O-D'), ((195, 165), 150), 'A B C D'),
    'p4a':   (E('L-O O-R T-L T-R'), ((212, 168), 150), 'L R T'),
    'p4b':   (E('P-A P-B A-O O-C C-B A-B'), ((229, 168), 150), 'P A B C'),
    'bora':  (E('c1a-c1b c2a-c2b'), ((166, 164), 136), 'c1a c1b c2a c2b'),
    'won':   (E('V-L V-R H1-H2 H2-V2'), ((175, 168), 136), 'V L R H1 V2'),
    'e2':    (E('P-A P-B Q-C Q-D O-A O-B O-C O-D'), ((187, 184), 160), 'P Q A B C D'),
    'p6a':   (E('R-L1 R-L2 T-B1 T-B2'), ((284, 170), 144), 'T L1 L2 R B1 B2'),
    'p6b':   (E('T-R L1-R L2-O O-R L2-Bt Bt-R L1-T'), ((259, 203), 150), 'T R L1 L2 Bt'),
    'k1a':   (E('T-A T-B O-A O-B'), ((165, 157), 145), 'T A B'),
    'k1b':   (E('A-T T-B A-O O-B A-C C-B'), ((168, 158), 148), 'T A B C'),
    'k1c':   (E('T-C T-B A-O O-B A-C C-B'), ((166, 158), 148), 'T A B C'),
    'think': (E('A-B B-C C-D A-D A-C B-D'), ((181, 194), 148), 'A B C D'),
    'a1':    (E('A-C C-B A-E E-D D-F F-B E-C C-F'), ((222, 210), 180), 'A B D'),
    'a2':    (E('A-C C-B G-A G-B G-C'), ((221, 236), 178), 'A B G'),
}

_cache = json.load(open(CACHE)) if os.path.exists(CACHE) else {}

def G(name, p, fig_dir=FIG, spec=None):
    """Return (refined points, (center, r) or None). Cached by rough input."""
    edges, circ, onc = spec or SPEC[name]
    key = name + json.dumps(p, sort_keys=True) + json.dumps(edges)
    if key in _cache:
        d = _cache[key]; return {k: tuple(v) for k, v in d['p'].items()}, (tuple(d['c'][0]), d['c'][1]) if d['c'] else None
    path = f'{fig_dir}/{name}.png'
    pts = dict(p)
    fitted = fit_circle(_ink(path), circ[0], circ[1]) if circ else None
    if fitted and 'O' in pts:
        pts['O'] = fitted[0]
    q, c = refine(path, pts, edges, circ, onc.split(), fixed=('O',), fitted=fitted)
    os.makedirs(CHK, exist_ok=True)
    check(path, q, edges, c, f'{CHK}/{name}.png')
    _cache[key] = {'p': q, 'c': [list(c[0]), c[1]] if c else None}
    json.dump(_cache, open(CACHE, 'w'))
    return q, c
