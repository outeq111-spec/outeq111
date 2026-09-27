"""원과 직선 중단원 마무리: 문제 슬라이드는 기존 것을 쓰고, 풀이 슬라이드(02~11)는 점을 교과서 그림에 맞춰 다시 만든다."""
import sys, re, base64, math
sys.path.insert(0, '/tmp/claude-0/-home-user-outeq111/d86e19ab-ec80-5ac1-a09b-c4db87ef5a17/scratchpad/gen')
from lib import *
from geo import G, E

BASE = '/tmp/claude-0/-home-user-outeq111/d86e19ab-ec80-5ac1-a09b-c4db87ef5a17'
FIGS = BASE + '/figs'
OLD = BASE + '/scratchpad/deck/project/slides'
BLOBS = {'4f18e1419902a3f35c681668f8afb9d3': 'crops/q01.png', 'b98c2a675bd5d404e962d78e9079803a': 'crops/q02.png', 'cd07f751c555bc42f81a90f3edfd53a0': 'crops/q03.png', '9f958b414d063fa9aa1bfaa940ba8756': 'crops/q04.png', 'f368a7db9cee74073118a6e89eccf500': 'crops/q05.png', '1e013f7b2180249464e4273aadccd1ca': 'crops/q06.png', '28a4cf95e2590457dbf745c29c86508f': 'crops/q07.png', 'cabad0e1b4ef745fc097046e5712fe24': 'crops/q08.png', 'e73adb52bad7fd95e8542d10edfdef4d': 'crops/q09.png', '743aa8d3fe5bd5bc6b649a67131da94a': 'crops/q10.png', '4e36495357f31dfc1e4feed9572b55a5': 'crops/q11.png'}

def old(sid):
    h = open(f'{OLD}/{sid}.html').read()
    h = re.sub(r'src="/_blob/([0-9a-f]{32})"', lambda m: 'src="data:image/png;base64,' + base64.b64encode(open(f'{BASE}/{BLOBS[m.group(1)]}', 'rb').read()).decode() + '"', h)
    return h.replace("'Noto Sans KR', Arial, sans-serif", FONT)

def g(name, p, edges, circ=None, onc=''):
    return G(name, p, fig_dir=FIGS, spec=(E(edges), circ, onc))

def foot(p, a, b):
    ax, ay = a; bx, by = b; t = ((p[0]-ax)*(bx-ax) + (p[1]-ay)*(by-ay)) / ((bx-ax)**2 + (by-ay)**2)
    return (ax + t*(bx-ax), ay + t*(by-ay))

def mid(a, b): return ((a[0]+b[0])/2, (a[1]+b[1])/2)

import lib
_fig_uri = lib.fig_uri
lib.fig_uri = lambda name: _fig_uri(name) if not name.startswith('f') else (lambda im: ('data:image/png;base64,' + base64.b64encode(open(f'{FIGS}/{name}.png', 'rb').read()).decode(), im.size))(Image.open(f'{FIGS}/{name}.png'))

def sol(n, fig, steps, ans, notes='', accent=TEAL):
    return solve(f'{n} 풀이', None, fig, steps, ans, notes=notes, accent=accent, figmax=(880, 800))

S = [old('cover'), old('concept'), old('p01'), old('s01')]
T = 13  # label size in these smaller figures

# 02
p, C = g('f02', dict(A=(32, 155), B=(198, 155), T=(175, 38), O=(115, 108)), 'A-B O-T', ((115, 108), 95), 'A B T')
M = foot(p['O'], p['A'], p['B'])
S += [old('p02'), sol('02', 'f02', [
    ('① 원 위의 점이 O에 닿도록 접었으니\n[r]OM = 10 ÷ 2 = 5[/r]', [line(p['O'], M, R, 2.5, True), right(M, p['O'], p['B'], 7, R), text((M[0]+5, (p['O'][1]+M[1])/2+4), '5', R, T), text((M[0]-4, M[1]+14), 'M', R, 11, 'end')]),
    ('② [b]△OAM[/b]에서\nAM² = 10² − 5² = 75 → AM = 5√3', [poly([p['O'], p['A'], M], BL, 0.2), line(p['O'], p['A'], BL, 2.5), text(((p['O'][0]+p['A'][0])/2-4, (p['O'][1]+p['A'][1])/2-4), '10', BL, T, 'end'), text(((p['A'][0]+M[0])/2, M[1]-5), '5√3', BL, 12, 'middle')]),
    ('③ 수선은 현을 이등분\n→ [g]AB = 2 × 5√3 = 10√3[/g]', [line(p['A'], p['B'], G, 4), text((M[0]+30, M[1]+22), '10√3', G, T)]),
], '답 · 10√3 cm')]

# 03
p, C = g('f03', dict(P=(112, 41), Q=(112, 220), A=(66, 220), B=(160, 220)), 'P-Q A-B', ((112, 137), 96), 'P A B')
O = C[0]
S += [old('p03'), sol('03', 'f03', [
    ('① PQ는 AB의 수직이등분선\n→ [r]중심 O는 PQ 위[/r]', [dot(O, R, 3), text((O[0]-8, O[1]+5), 'O', R, 14, 'end')]),
    ('② 반지름을 r이라 하면 [b]OA = OP = r[/b],\n[r]OQ = 8 − r[/r]', [line(O, p['A'], BL, 2.5), line(p['P'], O, BL, 3), line(O, p['Q'], R, 3), text((p['P'][0]-5, (p['P'][1]+O[1])/2), 'r', BL, 14, 'end'), text(((O[0]+p['A'][0])/2-5, (O[1]+p['A'][1])/2), 'r', BL, 14, 'end'), text((O[0]+4, (O[1]+p['Q'][1])/2+14), '8−r', R, 12)]),
    ('③ [g]△OAQ[/g]에서 r² = (8 − r)² + 2²', [poly([O, p['A'], p['Q']], G, 0.25)]),
    ('④ r² = 64 − 16r + r² + 4 → 16r = 68 → r = 17/4', []),
], '답 · 17/4 cm')]

# 04
p, C = g('f04', dict(A=(113, 41), B=(30, 183), C=(196, 183), D=(72, 114), E=(113, 183), F=(155, 114), O=(113, 136)), 'A-B B-C C-A O-D O-E O-F', ((113, 136), 95), 'A B C')
S += [old('p04'), sol('04', 'f04', [
    ('① OD = OE = OF → 세 현의 길이가 같다\n→ [b]△ABC는 정삼각형[/b]', [poly([p['A'], p['B'], p['C']], BL, 0, BL)]),
    ('② D는 AB의 중점 → [r]AB = 2√3[/r]', [line(p['A'], p['D'], R, 3.5), line(p['D'], p['B'], R, 3.5), text(((p['D'][0]+p['B'][0])/2-6, (p['D'][1]+p['B'][1])/2), '√3', R, T, 'end')]),
    ('③ BE = √3이므로 [g]높이 AE[/g] = √(12 − 3) = 3', [line(p['A'], p['E'], G, 2.5, True), text((p['A'][0]+4, (p['A'][1]+p['O'][1])/2), '3', G, 14), text(((p['B'][0]+p['E'][0])/2, p['E'][1]-4), '√3', G, 12, 'middle')]),
    ('④ 넓이 = ½ × 2√3 × 3 = 3√3', []),
], '답 · 3√3 cm²')]

# 05
p, C = g('f05', dict(A=(42, 60), B=(81, 212), E=(62, 138), O=(112, 127), C=(140, 38), D=(181, 191)), 'A-B O-E O-C O-D C-D', ((112, 127), 96), 'A B C D')
H = foot(p['O'], p['C'], p['D'])
S += [old('p05'), sol('05', 'f05', [
    ('① AB = CD이면 중심까지 거리도 같다\n→ [r]OH = OE = 7[/r]', [line(p['O'], H, R, 2.5, True), right(H, p['O'], p['C'], 6, R), text(((p['O'][0]+H[0])/2, (p['O'][1]+H[1])/2+14), '7', R, T), text((H[0]+5, H[1]-2), 'H', R, 12)]),
    ('② [b]△OCH[/b]에서 CH² = 13² − 7² = 120\n→ CH = 2√30', [poly([p['O'], p['C'], H], BL, 0.25), line(p['C'], H, BL, 3), text(((p['C'][0]+H[0])/2+6, (p['C'][1]+H[1])/2), '2√30', BL, 12)]),
    ('③ [g]CD = 2CH = 4√30[/g]', [line(p['C'], p['D'], G, 3.5), text(((H[0]+p['D'][0])/2+6, (H[1]+p['D'][1])/2+6), '4√30', G, 12)]),
    ('④ △ODC = ½ × 4√30 × 7 = 14√30', []),
], '답 · 14√30 cm²')]

# 06
p, C = g('f06', dict(O=(97, 116), A=(122, 38), B=(134, 193), P=(300, 116)), 'A-P B-P O-P O-B', ((97, 116), 88), 'A B')
(cx, cy), r = C; u = ((p['P'][0]-cx), (p['P'][1]-cy)); n = math.hypot(*u); Cc = (cx + u[0]/n*r, cy + u[1]/n*r)
S += [old('p06'), sol('06', 'f06', [
    ('① [r]OC = OB = 3[/r] (반지름)\n→ [b]OP = 3 + 4 = 7[/b]', [line(p['O'], Cc, R, 3.5), text(((p['O'][0]+Cc[0])/2, Cc[1]-6), '3', R, T, 'middle'), text(((Cc[0]+p['P'][0])/2+10, Cc[1]-8), 'OP = 7', BL, 12, 'middle')]),
    ('② 접선 ⊥ 반지름\n→ ∠OAP = 90°, OA = 3', [line(p['O'], p['A'], R, 3), right(p['A'], p['O'], p['P'], 7, R), text(((p['O'][0]+p['A'][0])/2-5, (p['O'][1]+p['A'][1])/2), '3', R, T, 'end'), poly([p['O'], p['A'], p['P']], BL, 0.12)]),
    ('③ AP² = 7² − 3² = 40\n→ [g]AP = 2√10[/g]', [line(p['A'], p['P'], G, 3.5), text(((p['A'][0]+p['P'][0])/2, (p['A'][1]+p['P'][1])/2-8), '2√10', G, T, 'middle')]),
], '답 · 2√10 cm', notes='OP를 4로 착각하는 실수가 많습니다. OC도 반지름임을 강조하세요.')]

# 07
p, C = g('f07', dict(A=(36, 114), B=(118, 64), C=(118, 165), D=(161, 40), E=(118, 114), F=(161, 188), O=(206, 114)), 'A-D A-F B-C O-D O-E O-F O-B O-C', ((206, 114), 88), 'D E F')
S += [old('p07'), sol('07', 'f07', [
    ('① 접선의 길이\n[r]BD = BE[/r], [b]CF = CE[/b]', [line(p['B'], p['D'], R, 4), line(p['B'], p['E'], R, 4), line(p['E'], p['C'], BL, 4), line(p['C'], p['F'], BL, 4)]),
    ('② (ㄹ) BC = BE + EC = BD + CF ⭕', []),
    ('③ (ㄷ) [o]△OCE ≡ △OCF[/o] (RHS)\n→ ∠OCE = ∠OCF ⭕', [poly([p['O'], p['C'], p['E']], OR, 0.3), poly([p['O'], p['C'], p['F']], OR, 0.3), line(p['O'], p['C'], OR, 3)]),
    ('④ (ㄱ), (ㄴ) 항상 성립하지는 않음 ❌', []),
], '답 · ㄷ, ㄹ', notes='(ㄱ), (ㄴ)은 접선 BC가 AO에 수직일 때만 성립합니다. △OCE, △OCF: 빗변 OC 공통, OE = OF, 직각.')]

# 08
p, C = g('f08', dict(D=(82, 36), A=(82, 185), B=(274, 185), C=(274, 125), P=(218, 99)), 'D-A A-B B-C C-P P-D')
Hh = foot(p['C'], p['A'], p['D'])
S += [old('p08'), sol('08', 'f08', [
    ('① AD, BC도 반원의 접선\n[r]DP = DA = 10[/r], [b]CP = CB = 4[/b]', [line(p['D'], p['A'], R, 3.5), line(p['D'], p['P'], R, 3.5), line(p['P'], p['C'], BL, 3.5), line(p['C'], p['B'], BL, 3.5), text(((p['D'][0]+p['P'][0])/2, (p['D'][1]+p['P'][1])/2-6), '10', R, T, 'middle'), text(((p['P'][0]+p['C'][0])/2, (p['P'][1]+p['C'][1])/2-6), '4', BL, T, 'middle')]),
    ('② 수선 CH를 그으면 [g]CD = 14[/g],\n[g]DH = 10 − 4 = 6[/g]', [poly([p['D'], Hh, p['C']], G, 0.2), line(Hh, p['C'], G, 2.5, True), right(Hh, p['D'], p['C'], 6, G), text((Hh[0]+5, (p['D'][1]+Hh[1])/2), '6', G, T), text((Hh[0]-4, Hh[1]+4), 'H', G, 12, 'end')]),
    ('③ AB = CH, CH² = 14² − 6² = 160\n→ [o]AB = 4√10[/o]', [line(p['A'], p['B'], OR, 4), text(((p['A'][0]+p['B'][0])/2-40, p['A'][1]+16), '4√10', '#B5651D', T, 'middle')]),
], '답 · 4√10 cm')]

# 09
p, C = g('f09', dict(A=(45, 64), B=(75, 203), C=(287, 203), D=(171, 42), P=(60, 140), Q=(138, 203), R=(205, 93), S=(135, 49)), 'A-P P-B B-Q Q-C C-R R-D D-S S-A', ((136, 127), 78), 'P Q R S')
lb = lambda a, b, s, c, dx=0, dy=0: text(((a[0]+b[0])/2+dx, (a[1]+b[1])/2+dy), s, c, T, 'middle')
S += [old('p09'), sol('09', 'f09', [
    ('① [b]BQ = BP = 4[/b]', [line(p['B'], p['P'], BL, 4), line(p['B'], p['Q'], BL, 4), lb(p['B'], p['Q'], '4', BL, 0, -6)]),
    ('② [g]CR = CQ = 15 − 4 = 11[/g]', [line(p['C'], p['Q'], G, 4), line(p['C'], p['R'], G, 4), lb(p['Q'], p['C'], '11', G, 0, -6), lb(p['C'], p['R'], '11', G, -10, 0)]),
    ('③ [o]DS = DR = 14 − 11 = 3[/o]', [line(p['D'], p['R'], OR, 4), line(p['D'], p['S'], OR, 4), lb(p['D'], p['R'], '3', '#B5651D', -8, 0), lb(p['D'], p['S'], '3', '#B5651D', 0, -6)]),
    ('④ [r]AP = AS = 9 − 3 = 6[/r]', [line(p['A'], p['S'], R, 4), line(p['A'], p['P'], R, 4), lb(p['A'], p['S'], '6', R, 0, -6), lb(p['A'], p['P'], '6', R, -8, 0)]),
    ('다른 풀이: AB + CD = AD + BC → AB = 10, AP = 10 − 4 = 6', []),
], '답 · 6 cm')]

# 10
p, C = g('f10', dict(P=(70, 36), A=(38, 177), B=(189, 177)), 'P-A P-B A-B', ((113, 119), 95), 'P A B')
O = C[0]; M = foot(O, p['A'], p['B']); v = (O[0]-M[0], O[1]-M[1]); nv = math.hypot(*v); Pm = (O[0]+v[0]/nv*C[1], O[1]+v[1]/nv*C[1])
S += [old('p10'), sol('10', 'f10', [
    ('① 수선 OM: AM = 4\n[r]OM = √(5² − 4²) = 3[/r]', [line(O, M, R, 2.5, True), line(O, p['A'], R, 2.5), right(M, O, p['B'], 6, R), text(((p['A'][0]+M[0])/2, M[1]-5), '4', R, T, 'middle'), text((M[0]+4, (O[1]+M[1])/2+5), '3', R, T), text((M[0]-4, M[1]+14), 'M', R, 11, 'end')]),
    ('② 밑변 AB는 고정 → [b]P가 MO의 연장선 위[/b]일 때 높이 최대', [poly([p['A'], Pm, p['B']], BL, 0.15, BL), dot(Pm, BL, 3), text((Pm[0]+5, Pm[1]-3), 'P', BL, 12)]),
    ('③ [g]최대 높이 = 5 + 3 = 8[/g]', [line(Pm, M, G, 3.5), text((Pm[0]+5, (Pm[1]+O[1])/2), '5 + 3 = 8', G, 12)]),
    ('④ 넓이 = ½ × 8 × 8 = 32', []),
], '답 · 32 cm²', notes='이때 P는 AB의 수직이등분선 위에 있어 PA = PB인 이등변삼각형이 됩니다.', accent='#B5651D')]

# 11
p, C = g('f11', dict(A=(93, 52), B=(93, 242), C=(258, 242), D=(258, 52), E=(200, 242)), 'A-B B-E E-C C-D D-A A-E')
Tp = foot(mid(p['C'], p['D']), p['A'], p['E'])
S += [old('p11'), sol('11', 'f11', [
    ('① AD, BC도 반원의 접선.\nAE와 반원의 접점을 [r]P[/r]라 하자.', [dot(Tp, R, 3), text((Tp[0]+6, Tp[1]-2), 'P', R, 13)]),
    ('② [r]AP = AD = 6[/r], [b]EP = EC = x[/b]', [line(p['A'], p['D'], R, 4), line(p['A'], Tp, R, 4), line(Tp, p['E'], BL, 4), line(p['E'], p['C'], BL, 4), text(((p['A'][0]+Tp[0])/2-6, (p['A'][1]+Tp[1])/2), '6', R, 14, 'end'), text(((Tp[0]+p['E'][0])/2+6, (Tp[1]+p['E'][1])/2), 'x', BL, 14), text(((p['E'][0]+p['C'][0])/2, p['E'][1]-5), 'x', BL, 14, 'middle')]),
    ('③ [g]△ABE[/g]: AE = 6 + x, BE = 6 − x\n(6 + x)² = (6 − x)² + (4√3)²', [poly([p['A'], p['B'], p['E']], G, 0.2), text(((p['B'][0]+p['E'][0])/2, p['B'][1]-6), '6 − x', G, 12, 'middle'), text(((p['A'][0]+p['E'][0])/2+8, (p['A'][1]+p['E'][1])/2), '6 + x', G, 12)]),
    ('④ 24x = 48 → x = 2', []),
], '답 · 2 cm', notes='검산: AE = 8, BE = 4, AB = 4√3 → 16 + 48 = 64 = 8²', accent='#B5651D')]

write('/home/user/outeq111/원과직선_중단원마무리_풀이.html', '원과 직선 중단원 마무리 풀이', S)
print(len(S), 'slides')
