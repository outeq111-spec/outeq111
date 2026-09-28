"""Ⅵ-2 중단원 마무리(204~206) · Ⅵ 대단원 마무리(207~209)."""
import sys, math
sys.path.insert(0, '/tmp/claude-0/-home-user-outeq111/d86e19ab-ec80-5ac1-a09b-c4db87ef5a17/scratchpad/gen')
import lib
lib.B = '/tmp/claude-0/-home-user-outeq111/d86e19ab-ec80-5ac1-a09b-c4db87ef5a17/ch4/m'
from lib import *
_poly = poly
def poly(pts, c=BL, op=0.2, stroke=None):
    return _poly(pts, c, op, stroke or c)
from geo import G as SNAP, E
import audit; audit.install(globals())
exec(open('/tmp/claude-0/-home-user-outeq111/d86e19ab-ec80-5ac1-a09b-c4db87ef5a17/ch4/spec.py').read())

FIG = lib.B + '/fg'
def g(name, p, edges, circ=None, onc=''):
    return SNAP(name, p, fig_dir=FIG, spec=(E(edges), circ, onc))
def refl(a, t): return (2*a[0]-t[0], 2*a[1]-t[1])
def mid(a, b): return ((a[0]+b[0])/2, (a[1]+b[1])/2)
def foot(p, a, b):
    ax, ay = a; bx, by = b; t = ((p[0]-ax)*(bx-ax) + (p[1]-ay)*(by-ay)) / ((bx-ax)**2 + (by-ay)**2)
    return (ax + t*(bx-ax), ay + t*(by-ay))
def lb(a, b, s, c, dx=0, dy=0, size=24):
    return text(((a[0]+b[0])/2+dx, (a[1]+b[1])/2+dy), s, c, size, 'middle')

S = []
def quadrev(title):
    import base64
    uri = 'data:image/png;base64,' + base64.b64encode(open('/tmp/claude-0/-home-user-outeq111/d86e19ab-ec80-5ac1-a09b-c4db87ef5a17/ch4/quad.png','rb').read()).decode()
    S.append('<section style="background:#F7F6F1; color:#1E2A3A; font-family:' + FONT + '; padding:96px; display:flex; flex-direction:column">'
             '<p style="position:absolute; left:96px; top:44px; width:1700px; font-size:30px; font-weight:700; color:#1F7A8C">복습 · 여러 가지 사각형 사이의 관계</p>'
             f'<p style="position:absolute; left:96px; top:90px; width:1728px; font-size:40px; font-weight:700">{title}</p>'
             f'<img src="{uri}" style="position:absolute; left:156px; top:190px; width:1608px; height:796px; object-fit:contain; background:#FFFFFF; border-radius:14px"></section>')
def prob(k, label, hint, accent=TEAL):
    pg, box, _ = P[k]
    if k.startswith('m'): box = (640,) + box[1:]
    S.append(crops(label, None, [(pg, box)], [f'[b]핵심[/b] · {hint}'], bg=BG1, accent=accent))
def sol(k, label, steps, ans, notes='', accent=TEAL):
    S.append(solve(label + ' 풀이', None, k, steps, ans, notes=notes, accent=accent))

# ================= 중단원 마무리 =================
S.append(cover('중단원 마무리<br>2. 원주각', '스스로 완성해 봅시다 · 표준 문제 01~08 · 도전 문제 09~11', 'Ⅵ. 원의 성질 · 교과서 204~206쪽'))
S.append(crops('스스로 완성해 봅시다', None, [(1, (560, 360, 2200, 1680))], [
    '① (1) ① ½  ② 원주각  ③ 90°   (2) ① 원주각  ② 호',
    '② (1) 180°  (2) 내접   ③ 원주각']))

p, C = g('m01', dict(A=(114, 43), C=(312, 102), B=(102, 297), O=(181, 172)), 'A-C A-B O-A O-C', ((180, 168), 148), 'A B C')
prob('m01', '표준 문제 01', '호의 길이는 중심각의 크기에 정비례')
sol('m01', '01', [
    ('① ∠AOC = 90°이고 호 AC : 호 BC = 3 : 5\n→ 호 BC에 대한 중심각 = 90° × 5/3 = [r]150°[/r]', [arc(C[0], C[1], p['B'], p['C'], (320, 250), R, 8), line(p['O'], p['B'], R, 4, True), wedge(p['O'], p['C'], p['B'], 30, R)]),
    ('② ∠BAC는 호 BC에 대한 [b]원주각[/b]\n→ ∠BAC = ½ × 150° = 75°', [wedge(p['A'], p['B'], p['C'], 40, BL, 0.55)]),
], '답 · 75°')

p, C = g('m02', dict(P=(172, 44), D=(117, 120), C=(225, 122), A=(21, 259), B=(319, 259), O=(170, 259)), 'P-A P-B A-B O-D O-C A-C B-D', ((170, 259), 149), 'D C A B')
prob('m02', '표준 문제 02 · 서술형', '원주각의 크기는 중심각의 ½, 반원에 대한 원주각은 90°')
sol('m02', '02', [
    ('① ∠DBC는 호 DC에 대한 원주각\n→ [r]∠DBC = ½ × 42° = 21°[/r]', [line(p['D'], p['B'], R, 4), wedge(p['B'], p['D'], p['C'], 60, R)]),
    ('② AB는 지름 → [b]∠ADB = 90°[/b]\n→ ∠PDB = 90°', [line(p['D'], p['B'], BL, 4), right(p['D'], p['P'], p['B'], 16, BL)]),
    ('③ [g]△PDB[/g]에서 ∠APB = 180° − 90° − 21° = 69°', [line(p['D'], p['B'], G, 4), poly([p['P'], p['D'], p['B']], G, 0.2)]),
], '답 · 69°')

p, C = g('m03', dict(A=(26, 152), D=(233, 61), B=(149, 337), C=(247, 315)), 'A-C B-D A-B', ((167, 190), 148), 'A B C D')
p['E'] = inter(p['A'], p['C'], p['B'], p['D'])
prob('m03', '표준 문제 03', '원주각의 크기와 호의 길이는 정비례')
sol('m03', '03', [
    ('① [g]△ABE[/g]에서 ∠BEC는 외각\n→ 70° = 20° + ∠ABE → [r]∠ABD = 50°[/r]', [line(p['A'], p['B'], G, 4), poly([p['A'], p['B'], p['E']], G, 0.2), wedge(p['B'], p['A'], p['D'], 40, R)]),
    ('② 호 AD : 호 BC = 50° : 20°', [arc(C[0], C[1], p['A'], p['D'], (70, 70), R, 8), arc(C[0], C[1], p['B'], p['C'], (200, 340), BL, 8)]),
    ('③ 호 AD : 8 = 5 : 2 → 호 AD = 20 cm', []),
], '답 · 20 cm')

p, C = g('m04', dict(A=(175, 44), E=(269, 84), B=(29, 139), C=(40, 261), D=(280, 285), O=(167, 190)), 'A-E E-D D-C C-B B-A B-D A-D O-E O-D', ((167, 190), 147), 'A B C D E')
prob('m04', '표준 문제 04 · 서술형', '원에 내접하는 사각형의 대각의 합은 180°')
sol('m04', '04', [
    ('① 보조선 AD를 그으면 □ABCD는 원에 내접\n→ [r]∠BAD = 180° − 100° = 80°[/r]', [line(p['A'], p['D'], R, 4, True), wedge(p['A'], p['B'], p['D'], 40, R)]),
    ('② [b]∠DAE = 124° − 80° = 44°[/b]', [wedge(p['A'], p['D'], p['E'], 52, BL)]),
    ('③ ∠EOD는 호 ED에 대한 중심각\n→ ∠EOD = 2 × 44° = 88°', [wedge(p['O'], p['E'], p['D'], 30, G, 0.55)]),
], '답 · 88°')

quadrev('어떤 사각형이 원에 내접할까? 대각의 합이 180°인지 떠올리며 보자.')
prob('m05', '표준 문제 05 · 추론', '한 쌍의 대각의 합이 180°인 사각형은 원에 내접')
S.append(textslide('05 풀이', '항상 원에 내접하는 사각형을 모두 고르시오.', [
    '(ㄱ) 등변사다리꼴 · 아랫변의 두 밑각이 같고, 윗각 + 아랫각 = 180° → 대각의 합 180° [g]⭕[/g]',
    '(ㄴ) 평행사변형 · 대각의 크기가 같다 → 합이 180°인 것은 직사각형일 때뿐 [r]❌[/r]',
    '(ㄷ) 마름모 · 정사각형일 때만 원에 내접 [r]❌[/r]',
    '(ㄹ) 직사각형 · 네 각이 모두 90° → 대각의 합 180° [g]⭕[/g]',
], answer='답 · (ㄱ), (ㄹ)'))

p, C = g('m06', dict(A=(61, 53), D=(281, 91), B=(29, 160), C=(160, 274), E=(266, 275)), 'A-D D-C C-B B-A A-C C-E', ((160, 144), 133), 'A B C D')
prob('m06', '표준 문제 06', '접선과 현이 이루는 각 = 내부에 있는 호에 대한 원주각')
sol('m06', '06', [
    ('① 접선과 현 CD가 이루는 각\n→ [r]∠DCE = ∠CAD = 56°[/r]', [wedge(p['C'], p['D'], p['E'], 34, R), wedge(p['A'], p['C'], p['D'], 40, R)]),
    ('② [b]∠ACD = ∠DCE = 56°[/b]', [wedge(p['C'], p['A'], p['D'], 44, BL)]),
    ('③ [g]△ACD[/g]에서 ∠D = 180° − 56° − 56° = 68°', [poly([p['A'], p['C'], p['D']], G, 0.2)]),
    ('④ □ABCD는 원에 내접 → ∠B = 180° − 68° = 112°', [wedge(p['B'], p['A'], p['C'], 34, OR, 0.55)]),
], '답 · 112°')

p, C = g('m07', dict(B=(361, 44), A=(141, 166), P=(34, 230), T=(252, 232), Q=(338, 232)), 'P-B P-Q T-B T-A', ((252, 106), 126), 'A B T')
p['A'] = foot(p['A'], p['P'], p['B'])
prob('m07', '표준 문제 07', '접선과 현이 이루는 각, 반원에 대한 원주각 90°')
sol('m07', '07', [
    ('① 접선과 현 TB가 이루는 각\n→ [r]∠BAT = ∠BTQ = 60°[/r]', [line(p['A'], p['T'], R, 4), wedge(p['T'], p['B'], p['Q'], 34, R), wedge(p['A'], p['T'], p['B'], 32, R)]),
    ('② AB는 지름 → [b]∠ATB = 90°[/b]\n→ ∠ATP = 180° − 90° − 60° = 30°', [right(p['T'], p['A'], p['B'], 16, BL), wedge(p['T'], p['P'], p['A'], 50, BL)]),
    ('③ [g]△APT[/g]에서 ∠BAT는 외각\n60° = ∠BPT + 30° → ∠BPT = 30°', [line(p['A'], p['T'], G, 4), poly([p['A'], p['P'], p['T']], G, 0.22)]),
], '답 · 30°')

p, C = g('m08', dict(A=(245, 65), B=(42, 363), C=(310, 363)), 'A-B B-C C-A')
p['D'] = foot((136, 228), p['A'], p['B']); p['F'] = foot((290, 260), p['A'], p['C']); p['E'] = foot((205, 363), p['B'], p['C'])
prob('m08', '표준 문제 08', '원 밖의 한 점에서 그은 두 접선의 길이는 같다')
sol('m08', '08', [
    ('① AD = AF → [r]∠ADF = (180° − 46°) ÷ 2 = 67°[/r]', [wedge(p['D'], p['A'], p['F'], 30, R)]),
    ('② 접선과 현 DF가 이루는 각 → [r]∠DEF = 67°[/r]\n→ △DEF에서 [b]∠DFE = 180° − 50° − 67° = 63°[/b]', [wedge(p['E'], p['D'], p['F'], 34, R), wedge(p['F'], p['D'], p['E'], 30, BL)]),
    ('③ 접선과 현 DE가 이루는 각\n→ ∠BDE = ∠BED = 63°', [wedge(p['D'], p['B'], p['E'], 30, BL), wedge(p['E'], p['D'], p['B'], 30, BL)]),
    ('④ [g]△BDE[/g]에서 ∠B = 180° − 63° − 63° = 54°', [poly([p['B'], p['D'], p['E']], G, 0.2)]),
], '답 · 54°')

p, C = g('m09', dict(A=(78, 68), B=(218, 68), P=(293, 228)), 'A-B P-A P-B', ((148, 201), 143), 'A B P')
O = C[0]
prob('m09', '도전 문제 09 · 문제 해결', '한 호에 대한 원주각은 중심각의 ½', accent='#B5651D')
sol('m09', '09', [
    ('① ∠APB = 30° → 중심각 [r]∠AOB = 60°[/r]\n→ △OAB는 정삼각형 → 반지름 12 m', [dot(O, R, 6), line(O, p['A'], R, 4), line(O, p['B'], R, 4), wedge(O, p['A'], p['B'], 26, R)]),
    ('② 무대를 뺀 부분 = [b]중심각 300°인 부채꼴[/b] + [o]△OAB[/o]', [f'<path d="M{O[0]},{O[1]} L{p["A"][0]},{p["A"][1]} A{C[1]},{C[1]} 0 1 0 {p["B"][0]},{p["B"][1]} Z" fill="#1F6FB2" fill-opacity="0.18" stroke="#1F6FB2" stroke-width="3"/>', poly([p['A'], p['B'], O], OR, 0.35)]),
    ('③ 부채꼴 = π × 12² × 300/360 = [b]120π[/b]\n△OAB = (√3/4) × 12² = [o]36√3[/o]', []),
], '답 · (36√3 + 120π) m²', accent='#B5651D')

p, C = g('m10', dict(A=(228, 54), B=(42, 264), C=(340, 264), H=(340, 152), O=(190, 210)), 'A-B B-C C-A A-H C-H B-H', ((190, 210), 156), 'A B C H')
O = C[0]
p['E'] = foot(p['A'], p['B'], p['C']); p['D'] = foot(O, p['B'], p['C']); p['F'] = foot(p['C'], p['A'], p['B'])
p['G'] = inter(p['A'], p['E'], p['C'], p['F'])
quadrev('두 쌍의 대변이 각각 평행 → 평행사변형')
prob('m10', '도전 문제 10 · 서술형', 'BH는 지름 → 지름에 대한 원주각은 90°', accent='#B5651D')
sol('m10', '10 (1)', [
    ('① BH는 지름 → [r]∠BCH = 90°[/r] → CH ⊥ BC\nAE ⊥ BC이므로 [r]AG ∥ CH[/r]', [right(p['C'], p['B'], p['H'], 14, R), line(p['C'], p['H'], R, 4), line(p['A'], p['G'], R, 4)]),
    ('② [b]∠BAH = 90°[/b] → AH ⊥ AB\nCF ⊥ AB이므로 [b]AH ∥ GC[/b]', [right(p['A'], p['B'], p['H'], 14, BL), line(p['A'], p['H'], BL, 4), line(p['G'], p['C'], BL, 4)]),
    ('③ 두 쌍의 대변이 각각 평행', [poly([p['A'], p['G'], p['C'], p['H']], G, 0.25)]),
], '답 · 평행사변형', accent='#B5651D')
sol('m10', '10 (2)', [
    ('① O는 BH의 중점, D는 BC의 중점 (중심에서 현에 내린 수선)', [dot(p['D'], R, 5), line(O, p['D'], R, 4)]),
    ('② △BCH에서 [r]CH = 2OD = 2√5[/r] (삼각형의 중점연결정리)', [line(p['C'], p['H'], R, 5)]),
    ('③ 평행사변형 → [g]AG = CH = 2√5[/g]', [line(p['A'], p['G'], G, 5)]),
], '답 · 2√5 cm', accent='#B5651D')

p, C = g('m11', dict(A=(338, 54), B=(142, 228), C=(262, 304), D=(396, 198), E=(58, 304)), 'E-A A-C C-D D-A B-C E-C', ((262, 168), 136), 'A B C D')
prob('m11', '도전 문제 11', '접선과 현이 이루는 각, 원에 내접하는 사각형', accent='#B5651D')
sol('m11', '11', [
    ('① AB = AC → [r]∠ABC = ∠ACB = x[/r]라 하자.', [wedge(p['B'], p['A'], p['C'], 30, R), wedge(p['C'], p['B'], p['A'], 30, R)]),
    ('② 접선과 현 BC가 이루는 각\n→ [b]∠BCE = ∠BAC = 180° − 2x[/b]', [wedge(p['C'], p['E'], p['B'], 44, BL), wedge(p['A'], p['B'], p['C'], 34, BL)]),
    ('③ △EBC에서 외각 ∠ABC: x = 42° + (180° − 2x)\n→ x = 74°', [poly([p['E'], p['B'], p['C']], G, 0.22)]),
    ('④ □ABCD는 원에 내접 → ∠D = 180° − 74° = 106°', [wedge(p['D'], p['A'], p['C'], 30, OR, 0.55)]),
], '답 · 106°', accent='#B5651D')
write('/home/user/outeq111/원주각_중단원마무리_풀이.html', '원주각 중단원 마무리', S)
print('mid', len(S))

# ================= 대단원 마무리 =================
S = [cover('대단원 마무리<br>Ⅵ. 원의 성질', '01~16번 풀이 · 자기 평가', 'Ⅵ. 원의 성질 · 교과서 207~209쪽')]
V = '#6B4FA0'
def bprob(k, n, hint): prob(k, f'대단원 {n}', hint, accent=V)
def bsol(k, n, steps, ans, notes=''): sol(k, n, steps, ans, notes, accent=V)

p, C = g('b01', dict(L=(34, 228), Rr=(299, 228), O=(164, 164)), 'L-Rr', ((164, 164), 145), 'L Rr')
M = foot(p['O'], p['L'], p['Rr'])
bprob('b01', '01', '원의 중심에서 현에 내린 수선은 현을 이등분')
bsol('b01', '01', [
    ('① 수선은 현을 이등분 → [r]반현 = 4√10[/r]', [line(p['L'], M, R, 5), lb(p['L'], M, '4√10', R, 0, -8)]),
    ('② [b]반지름[/b]을 그으면 직각삼각형', [line(p['O'], p['L'], BL, 4), poly([p['O'], p['L'], M], BL, 0.2)]),
    ('③ r² = (4√10)² + 6² = 160 + 36 = 196 → r = 14', []),
], '답 · 14 cm')

p, C = g('b02', dict(C=(167, 54), D=(167, 348), A=(22, 242), B=(310, 242)), 'C-D A-B', ((167, 201), 147), 'A B C D')
O = C[0]; Ee = inter(p['A'], p['B'], p['C'], p['D'])
bprob('b02', '02', '원의 중심에서 현에 내린 수선은 현을 이등분')
bsol('b02', '02', [
    ('① 지름 CD = 14 + 8 = 22 → [r]반지름 11[/r]\n→ OE = 11 − 8 = 3', [line(O, Ee, R, 5), lb(O, Ee, '3', R, 14, 6)]),
    ('② [b]△OAE[/b]에서 AE² = 11² − 3² = 112\n→ AE = 4√7', [line(O, p['A'], BL, 4), poly([O, p['A'], Ee], BL, 0.2)]),
    ('③ AB = 2AE = 8√7', [line(p['A'], p['B'], G, 5)]),
], '답 · 8√7 cm')

p, C = g('b03', dict(A=(211, 52), B=(42, 257), C=(309, 257)), 'A-B B-C C-A', ((174, 191), 144), 'A B C')
bprob('b03', '03', '중심에서 같은 거리의 두 현은 길이가 같다')
bsol('b03', '03', [
    ('① OD = OE → [r]AB = BC[/r]', [line(p['A'], p['B'], R, 5), line(p['B'], p['C'], R, 5)]),
    ('② △ABC는 이등변삼각형 → [b]∠C = ∠A = 65°[/b]', [wedge(p['C'], p['A'], p['B'], 34, BL), wedge(p['A'], p['B'], p['C'], 34, BL)]),
    ('③ ∠B = 180° − 65° − 65° = 50°', []),
], '답 · 50°')

p, C = g('b04', dict(P=(122, 61), A=(123, 339), B=(338, 257), D=(253, 185)), 'P-A P-B', ((240, 333), 117), 'A B')
p['C'] = (p['P'][0] + (p['A'][0]-p['P'][0])*7/9, p['P'][1] + (p['A'][1]-p['P'][1])*7/9)
p['E'] = foot(C[0], p['C'], p['D'])
bprob('b04', '04', '원 밖의 한 점에서 그은 두 접선의 길이는 같다')
bsol('b04', '04', [
    ('① [r]CE = CA = 2[/r], [b]DE = DB[/b]', [line(p['C'], p['E'], R, 5), line(p['C'], p['A'], R, 5), line(p['D'], p['E'], BL, 5), line(p['D'], p['B'], BL, 5)]),
    ('② 둘레 = PC + CE + ED + DP\n= PC + CA + DB + DP = PA + PB', []),
    ('③ PA = PB = 9 → 둘레 = 18', [line(p['P'], p['A'], G, 3, True), line(p['P'], p['B'], G, 3, True)]),
], '답 · 18 cm')

p, C = g('b05', dict(A=(74, 109), D=(193, 74), C=(419, 246), B=(112, 248)), 'A-D D-C C-B B-A', ((174, 165), 82), '')
O = C[0]; Et = foot(O, p['A'], p['D']); Ft = foot(O, p['A'], p['B'])
quadrev('∠A = 90°와 접선의 성질로 어떤 사각형이 생기는지 떠올려 보자.')
bprob('b05', '05', '원에 외접하는 사각형은 대변의 길이의 합이 같다')
bsol('b05', '05', [
    ('① AB + CD = AD + BC → 7 + 14 = AD + 15\n→ [r]AD = 6[/r]', [line(p['A'], p['D'], R, 5)]),
    ('② [b]AE = AD − DE = 6 − 2 = 4[/b]', [line(p['A'], Et, BL, 5)]),
    ('③ ∠A = 90°, 접선 ⊥ 반지름 → [g]정사각형[/g] → 반지름 = AE = 4', [poly([p['A'], Et, O, Ft], G, 0.3, G)]),
    ('④ 넓이 = π × 4² = 16π', []),
], '답 · 16π cm²')

p, C = g('b06', dict(C=(28, 157), A=(234, 50), B=(234, 263), P=(408, 157)), 'C-A C-B P-A P-B', ((149, 157), 121), 'A B C')
bprob('b06', '06', '접선과 현이 이루는 각, 두 접선의 길이는 같다')
bsol('b06', '06', [
    ('① 접선과 현 AB가 이루는 각\n→ [r]∠PAB = ∠PBA = ∠ACB = 62°[/r]', [line(p['A'], p['B'], R, 3, True), wedge(p['A'], p['B'], p['P'], 30, R), wedge(p['B'], p['P'], p['A'], 30, R)]),
    ('② [g]△PAB[/g]에서 ∠APB = 180° − 62° − 62° = 56°', [poly([p['P'], p['A'], p['B']], G, 0.2)]),
], '답 · 56°')

p, C = g('b07', dict(A=(62, 78), D=(226, 32), B=(74, 282), C=(264, 288)), 'A-C B-D A-B', ((174, 174), 148), 'A B C D')
p['P'] = inter(p['A'], p['C'], p['B'], p['D'])
bprob('b07', '07', '원주각의 크기와 호의 길이는 정비례')
bsol('b07', '07', [
    ('① [g]△ABP[/g]에서 외각 ∠BPC = 75°\n→ [r]∠BAC = 75° − 35° = 40°[/r]', [poly([p['A'], p['B'], p['P']], G, 0.2), wedge(p['A'], p['B'], p['C'], 44, R)]),
    ('② 호 BC에 대한 중심각 = 80°', [arc(C[0], C[1], p['B'], p['C'], (170, 322), R, 8)]),
    ('③ 둘레 : 6π = 360° : 80° → 둘레 = 27π', []),
], '답 · 27π cm')

p, C = g('b08', dict(A=(38, 158), D=(334, 158), B=(64, 244), C=(306, 244)), 'A-C B-D B-C', ((186, 158), 148), 'A B C D')
p['P'] = inter(p['A'], p['C'], p['B'], p['D'])
bprob('b08', '08', '길이가 같은 호에 대한 원주각은 크기가 같다')
bsol('b08', '08', [
    ('① 호 AB = 호 CD → [r]∠DBC = ∠ACB = 18°[/r]', [wedge(p['B'], p['C'], p['D'], 50, R), wedge(p['C'], p['A'], p['B'], 50, R)]),
    ('② [g]△PBC[/g]에서 외각\n∠APB = 18° + 18° = 36°', [poly([p['P'], p['B'], p['C']], G, 0.2), wedge(p['P'], p['A'], p['B'], 26, BL)]),
], '답 · 36°')

p, C = g('b09', dict(A=(30, 158), B=(326, 158), C=(266, 40), D=(106, 326), E=(253, 326)), 'A-B A-C C-D C-E C-B', ((178, 158), 148), 'A B C D E')
p['F'] = inter(p['A'], p['B'], p['C'], p['E'])
bprob('b09', '09', '원주각의 크기는 호의 길이에 정비례')
bsol('b09', '09', [
    ('① 반원 위쪽: 호 AC : 호 CB = 7 : 3\n→ [r]∠ABC = 63°[/r], ∠BAC = 27°', [wedge(p['B'], p['A'], p['C'], 34, R)]),
    ('② 아래쪽 반원은 3등분 → 호 AE의 원주각\n[b]∠ACE = 180° × 2/3 ÷ 2 = 60°[/b]', [wedge(p['C'], p['A'], p['E'], 40, BL)]),
    ('③ [g]△AFC[/g]에서 외각\n∠AFE = 27° + 60° = 87°', [poly([p['A'], p['F'], p['C']], G, 0.2)]),
], '답 · 87°')

p, C = g('b10', dict(P=(166, 56), Q=(38, 382), B=(216, 382), C=(374, 382), A=(193, 240), D=(252, 189)), 'P-B P-C Q-D Q-C', ((297, 282), 125), 'A B C D')
quadrev('원에 내접하는 사각형: 대각의 합이 180°')
bprob('b10', '10', '원에 내접하는 사각형의 성질')
bsol('b10', '10', [
    ('① ∠C = x라 하면 [r]△PBC[/r]에서\n∠ABC = 180° − 24° − x = 156° − x', [poly([p['P'], p['B'], p['C']], R, 0.12), wedge(p['C'], p['P'], p['B'], 36, R)]),
    ('② □ABCD는 원에 내접\n→ [b]∠ADC = 180° − ∠ABC = 24° + x[/b]', [wedge(p['D'], p['A'], p['C'], 30, BL)]),
    ('③ [g]△QDC[/g]에서 42° + (24° + x) + x = 180°\n→ x = 57°', [poly([p['Q'], p['D'], p['C']], G, 0.15)]),
], '답 · 57°')

p, C = g('b11', dict(A=(230, 55), T=(61, 325), B=(204, 325), C=(340, 199)), 'T-A T-B A-B A-C C-B', ((205, 188), 137), 'A B C')
bprob('b11', '11', '접선과 현이 이루는 각')
bsol('b11', '11', [
    ('① 접선과 현 AB가 이루는 각\n→ [r]∠TBA = ∠ACB = 95°[/r]', [wedge(p['B'], p['T'], p['A'], 30, R), wedge(p['C'], p['A'], p['B'], 30, R)]),
    ('② [g]△ATB[/g]에서 ∠ATB = 180° − 27° − 95° = 58°', [poly([p['A'], p['T'], p['B']], G, 0.2)]),
], '답 · 58°')

p, C = g('b12', dict(A=(241, 78), B=(56, 232), C=(269, 232), D=(423, 232)), 'A-B A-C A-D B-D', ((160, 169), 122), 'A B C')
bprob('b12', '12', '접선과 현이 이루는 각')
bsol('b12', '12', [
    ('① AB = AD → [r]∠ABD = ∠ADB = 40°[/r]', [wedge(p['B'], p['A'], p['D'], 44, R), wedge(p['D'], p['A'], p['B'], 44, R)]),
    ('② 접선과 현 AC가 이루는 각\n→ [b]∠CAD = ∠ABC = 40°[/b]', [wedge(p['A'], p['C'], p['D'], 44, BL)]),
    ('③ △ABD에서 ∠BAD = 100°\n→ ∠BAC = 100° − 40° = 60°', [wedge(p['A'], p['B'], p['C'], 34, G)]),
], '답 · 60°')

p, C = g('b13', dict(O=(173, 166), A=(78, 280), B=(270, 280), C=(173, 313)), 'O-C A-B O-A', ((173, 166), 147), 'A B C')
O = p['O']; Dd = inter(p['A'], p['B'], O, p['C'])
bprob('b13', '13 · 서술형', '중심에서 현에 내린 수선은 현을 이등분')
bsol('b13', '13', [
    ('① 수선은 현을 이등분 → [r]AD = BD = 5[/r]', [line(p['A'], Dd, R, 5)]),
    ('② OA = r이라 하면 [b]OD = r − 2[/b]', [line(O, p['A'], BL, 4), line(O, Dd, BL, 5)]),
    ('③ [g]△OAD[/g]에서 r² = 5² + (r − 2)²\n→ 4r = 29 → r = 29/4', [poly([O, p['A'], Dd], G, 0.2)]),
], '답 · 29/4 cm')

p = dict(A=(62, 242), B=(287, 242)); O = (174, 142); T = foot(O, p['A'], p['B'])
bprob('b14', '14 · 서술형', '접선 ⊥ 반지름, 현의 수직이등분')
bsol('b14', '14', [
    ('① 작은 원의 접점을 H라 하면 [r]OH ⊥ AB[/r]\n→ AH = 8', [line(O, T, R, 4), right(T, O, p['B'], 12, R), line(p['A'], T, R, 5)]),
    ('② 큰 원의 반지름 R, 작은 원의 반지름 r\n→ [b]R² − r² = 8² = 64[/b]', [line(O, p['A'], BL, 4), poly([O, p['A'], T], BL, 0.2)]),
    ('③ 색칠한 부분 = πR² − πr² = 64π', []),
], '답 · 64π cm²')

p, C = g('b15', dict(A=(36, 136), D=(121, 61), B=(44, 277), C=(159, 346)), 'A-C B-D', ((169, 199), 147), 'A B C D')
p['E'] = inter(p['A'], p['C'], p['B'], p['D'])
bprob('b15', '15 · 서술형', '원주각의 크기와 호의 길이는 정비례')
bsol('b15', '15', [
    ('① 보조선 AB: [g]△ABE[/g]에서 외각\n∠AED = [r]∠CAB + ∠DBA = 50°[/r]', [line(p['A'], p['B'], R, 4, True), poly([p['A'], p['B'], p['E']], G, 0.2), wedge(p['A'], p['B'], p['C'], 36, R), wedge(p['B'], p['D'], p['A'], 36, R)]),
    ('② ∠CAB는 호 BC, ∠DBA는 호 AD에 대한 원주각\n→ [b]호 AD + 호 BC[/b]의 중심각 합 = 100°', [arc(C[0], C[1], p['A'], p['D'], (80, 80), BL, 8), arc(C[0], C[1], p['B'], p['C'], (90, 330), BL, 8)]),
    ('③ 원의 둘레 24π × 100/360 = 20π/3', []),
], '답 · 20π/3 cm')

p, C = g('b16', dict(D=(74, 42), B=(314, 127), A=(22, 181), C=(167, 301)), 'D-B D-C A-B A-C', ((167, 154), 147), 'A B C D')
p['T'] = (27, 302)
bprob('b16', '16 · 서술형', '접선과 현이 이루는 각, 반원에 대한 원주각')
bsol('b16', '16', [
    ('① 접선과 현 AC가 이루는 각\n→ [r]∠ABC = ∠ACT = 40°[/r]', [line(p['C'], p['B'], R, 4, True), wedge(p['B'], p['A'], p['C'], 50, R)]),
    ('② AB는 지름 → [b]∠ACB = 90°[/b]\n→ ∠BAC = 50°', [line(p['C'], p['B'], BL, 4, True), right(p['C'], p['A'], p['B'], 14, BL), wedge(p['A'], p['B'], p['C'], 40, BL)]),
    ('③ ∠CDB와 ∠CAB는 같은 호 BC에 대한 원주각\n→ ∠CDB = 50°', [wedge(p['D'], p['C'], p['B'], 40, G)]),
], '답 · 50°')

S.append(crops('자기 평가', None, [(6, (220, 2080, 2200, 2880))], [], bg=BG1, accent=V))
write('/home/user/outeq111/원의성질_대단원마무리_풀이.html', '원의 성질 대단원 마무리', S)
print('big', len(S))
for b in audit.report(FIG): print('BAD', b)
