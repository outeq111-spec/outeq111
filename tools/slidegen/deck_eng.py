"""원의 성질 영어 표현 — 용어·개념을 영어로 (그림은 SVG로 직접 그림, 교과서 그림 없음).
python3 deck_eng.py  →  저장소 루트에 HTML 생성"""
import os, re, math, html as H

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, '..', '..', '원의성질_영어로배우기.html')
R, BL, G, OR, PU = '#E4572E', '#1F6FB2', '#2E9E5B', '#D9822B', '#8E44AD'
COLORS = {'r': R, 'b': BL, 'g': G, 'o': '#B5651D', 'p': PU}
BG1, BG2, DARK, TEAL, PILL = '#F7F6F1', '#EEF4F4', '#1E2A3A', '#1F7A8C', '#FCE0C4'
FONT = "'Noto Sans KR','Apple SD Gothic Neo','Malgun Gothic','Nanum Gothic',sans-serif"
EN = "'Segoe UI','Helvetica Neue',Arial,sans-serif"


def rich(s):
    s = H.escape(s)
    s = re.sub(r'\[(\w)\](.*?)\[/\1\]', lambda m: f'<b style="color:{COLORS[m.group(1)]}">{m.group(2)}</b>', s)
    return s.replace('\n', '<br>')


def B(n, kind='rise'):
    return f'data-build-in="{kind} {n}"' if n else ''


def sec(inner, label='', title='', bg=BG1, notes=''):
    h = ''
    if label:
        h += f'<p style="position:absolute; left:96px; top:44px; font-size:30px; font-weight:700; color:{TEAL}">{H.escape(label)}</p>'
    if title:
        h += f'<p style="position:absolute; left:96px; top:90px; width:1728px; font-size:46px; font-weight:700; line-height:1.3">{rich(title)}</p>'
    a = f'<aside>{H.escape(notes)}</aside>' if notes else ''
    return (f'<section style="background:{bg}; color:{DARK}; font-family:{FONT}; padding:96px; display:flex; flex-direction:column">'
            f'{h}{inner}{a}</section>')


def box(x, y, w, inner, n=None, bg='#FFFFFF', size=38, extra=''):
    return (f'<div {B(n)} style="position:absolute; left:{x}px; top:{y}px; width:{w}px; background:{bg}; border-radius:16px; '
            f'padding:22px 32px; font-size:{size}px; line-height:1.45; {extra}">{inner}</div>')


# ---------- SVG (viewBox 820 x 700, y 아래로) ----------
CX, CY, RR = 410, 350, 270
def pt(deg, c=(CX, CY), r=RR):
    a = math.radians(deg); return (round(c[0] + r*math.cos(a), 1), round(c[1] - r*math.sin(a), 1))
def ln(a, b, c=DARK, w=4, dash=False):
    d = ' stroke-dasharray="12 8"' if dash else ''
    return f'<line x1="{a[0]}" y1="{a[1]}" x2="{b[0]}" y2="{b[1]}" stroke="{c}" stroke-width="{w}" stroke-linecap="round"{d}/>'
def circ(c=(CX, CY), r=RR, col=DARK, w=4, fill='none', op=1):
    return f'<circle cx="{c[0]}" cy="{c[1]}" r="{r}" fill="{fill}" fill-opacity="{op}" stroke="{col}" stroke-width="{w}"/>'
def dot(p, c=DARK, r=7):
    return f'<circle cx="{p[0]}" cy="{p[1]}" r="{r}" fill="{c}"/>'
def lab(p, s, dx=0, dy=0, c=DARK, size=40, it=True):
    st = 'italic' if it else 'normal'
    return (f'<text x="{p[0]+dx}" y="{p[1]+dy}" font-size="{size}" font-family="Times New Roman,serif" font-style="{st}" fill="{c}" '
            f'text-anchor="middle" dominant-baseline="middle" stroke="#FFF" stroke-width="6" paint-order="stroke">{H.escape(s)}</text>')
def tag(p, s, c, size=34, anchor='middle'):
    return (f'<text x="{p[0]}" y="{p[1]}" font-size="{size}" font-family="{EN}" font-weight="700" fill="{c}" text-anchor="{anchor}" '
            f'dominant-baseline="middle" stroke="#FFF" stroke-width="7" paint-order="stroke">{H.escape(s)}</text>')
def arcp(deg1, deg2, c=R, w=12, cen=(CX, CY), r=RR):
    """deg1 → deg2 반시계(수학 방향) 호"""
    d = (deg2 - deg1) % 360
    s, e = pt(deg1, cen, r), pt(deg2, cen, r)
    return (f'<path d="M{s[0]},{s[1]} A{r},{r} 0 {1 if d > 180 else 0} 0 {e[0]},{e[1]}" fill="none" stroke="{c}" '
            f'stroke-width="{w}" stroke-linecap="round" stroke-opacity="0.85"/>')
def sector(deg1, deg2, c, op=0.25, cen=(CX, CY), r=RR):
    d = (deg2 - deg1) % 360; s, e = pt(deg1, cen, r), pt(deg2, cen, r)
    return (f'<path d="M{cen[0]},{cen[1]} L{s[0]},{s[1]} A{r},{r} 0 {1 if d > 180 else 0} 0 {e[0]},{e[1]} Z" fill="{c}" fill-opacity="{op}" '
            f'stroke="{c}" stroke-width="3"/>')
def segm(deg1, deg2, c, op=0.25, cen=(CX, CY), r=RR):
    d = (deg2 - deg1) % 360; s, e = pt(deg1, cen, r), pt(deg2, cen, r)
    return (f'<path d="M{s[0]},{s[1]} A{r},{r} 0 {1 if d > 180 else 0} 0 {e[0]},{e[1]} Z" fill="{c}" fill-opacity="{op}" '
            f'stroke="{c}" stroke-width="3"/>')
def _ang(v, p): return math.atan2(p[1]-v[1], p[0]-v[0])
def wedge(v, p1, p2, r=50, c=R, op=0.4):
    a1, a2 = _ang(v, p1), _ang(v, p2)
    d = (a2 - a1) % (2*math.pi)
    if d > math.pi: a1, a2 = a2, a1; d = 2*math.pi - d
    s = (v[0]+r*math.cos(a1), v[1]+r*math.sin(a1)); e = (v[0]+r*math.cos(a2), v[1]+r*math.sin(a2))
    return (f'<path d="M{v[0]:.1f},{v[1]:.1f} L{s[0]:.1f},{s[1]:.1f} A{r},{r} 0 0 1 {e[0]:.1f},{e[1]:.1f} Z" fill="{c}" '
            f'fill-opacity="{op}" stroke="{c}" stroke-width="3"/>')
def right(v, p1, p2, s=22, c=DARK):
    def u(p):
        dx, dy = p[0]-v[0], p[1]-v[1]; n = math.hypot(dx, dy); return dx/n, dy/n
    u1, u2 = u(p1), u(p2)
    a = (v[0]+u1[0]*s, v[1]+u1[1]*s); b = (a[0]+u2[0]*s, a[1]+u2[1]*s); cc = (v[0]+u2[0]*s, v[1]+u2[1]*s)
    return f'<path d="M{a[0]:.1f},{a[1]:.1f} L{b[0]:.1f},{b[1]:.1f} L{cc[0]:.1f},{cc[1]:.1f}" fill="none" stroke="{c}" stroke-width="3"/>'
def tick(a, b, c=DARK, n=1):
    m = ((a[0]+b[0])/2, (a[1]+b[1])/2); dx, dy = b[0]-a[0], b[1]-a[1]; L = math.hypot(dx, dy); ux, uy = dx/L, dy/L
    out = ''
    for k in range(n):
        o = (k - (n-1)/2) * 10
        cx, cy = m[0]+ux*o, m[1]+uy*o
        out += ln((cx-uy*14, cy+ux*14), (cx+uy*14, cy-ux*14), c, 4)
    return out
def mid(a, b): return ((a[0]+b[0])/2, (a[1]+b[1])/2)
def along(a, b, t): return (a[0]+(b[0]-a[0])*t, a[1]+(b[1]-a[1])*t)


def fig(layers, x=96, y=190, w=820, h=700):
    """layers: [(n, svg문자열)] — n=0은 처음부터 보임"""
    body = ''.join(f'<g {B(n, "fade")}>{s}</g>' if n else s for n, s in layers)
    return (f'<svg style="position:absolute; left:{x}px; top:{y}px; width:{w}px; height:{h}px; background:#FFF; border-radius:18px" '
            f'viewBox="0 0 820 700">{body}</svg>')


def cards(items, x=960, y=190, w=864, gap=16, en_size=46):
    """items: (n, 한국어, English, 발음, 색)"""
    out = f'<div style="position:absolute; left:{x}px; top:{y}px; width:{w}px; display:flex; flex-direction:column; gap:{gap}px">'
    for n, ko, en, pr, c in items:
        out += (f'<div {B(n)} style="background:#FFF; border-radius:14px; padding:12px 26px; border-left:12px solid {c}">'
                f'<p style="font-size:28px; color:#4A5568">{rich(ko)}</p>'
                f'<p style="font-size:{en_size}px; font-weight:700; color:{c}; font-family:{EN}; line-height:1.2">{H.escape(en)}'
                f'<span style="font-size:26px; font-weight:400; color:#6B7280; font-family:{FONT}; margin-left:18px">{H.escape(pr)}</span></p></div>')
    return out + '</div>'


def sentence(en, ko, n, y=900, x=96, w=1728):
    return (f'<div {B(n)} style="position:absolute; left:{x}px; top:{y}px; width:{w}px; background:{PILL}; border-radius:16px; padding:16px 30px">'
            f'<p style="font-size:38px; font-weight:700; font-family:{EN}; line-height:1.3">{rich(en)}</p>'
            f'<p style="font-size:28px; color:#4A5568; margin-top:4px">{rich(ko)}</p></div>')


S = []
O = (CX, CY)

# 1. 표지 ------------------------------------------------------------------
S.append(f'<section style="background:{DARK}; color:#F7F6F1; font-family:{FONT}; padding:128px; display:flex; flex-direction:column">'
         '<div style="display:flex; flex-direction:column; justify-content:center; gap:32px; height:100%">'
         '<p style="font-size:34px; font-weight:700; color:#7CC6D2">Ⅵ. 원의 성질 · 영어로 배우기</p>'
         f'<h1 style="font-size:120px; font-weight:900; line-height:1.1; font-family:{EN}">Properties of Circles</h1>'
         '<p style="font-size:40px; color:#BFD8D5">원의 성질에서 쓰는 용어와 개념을 영어로 말해 보자</p></div></section>')

# 2. 원의 각 부분 (1) --------------------------------------------------------
A, Bd1, Bd2 = pt(35), pt(160), pt(340)
layers = [(0, circ()),
          (1, circ(col=R, w=10) + tag(pt(118, r=RR+40), 'circumference', R)),
          (2, dot(O) + lab(O, 'O', -8, -34)),
          (3, ln(O, A, BL, 7) + dot(A) + tag(along(O, A, 0.55), 'radius', BL, anchor='end') ),
          (4, ln(Bd1, Bd2, G, 7) + dot(Bd1) + dot(Bd2) + tag(along(Bd1, Bd2, 0.25), 'diameter', G))]
layers[3] = (3, ln(O, A, BL, 7) + dot(A) + tag((along(O, A, 0.55)[0]-10, along(O, A, 0.55)[1]-30), 'radius', BL))
layers[4] = (4, ln(Bd1, Bd2, G, 7) + dot(Bd1) + dot(Bd2) + tag((along(Bd1, Bd2, 0.3)[0], along(Bd1, Bd2, 0.3)[1]+40), 'diameter', G))
inner = fig(layers) + cards([
    (1, '원 / 원주 (원의 둘레)', 'circle / circumference', '서클 / 서컴퍼런스', R),
    (2, '원의 중심', 'center', '센터', DARK),
    (3, '반지름 (복수: radii)', 'radius', '레이디어스', BL),
    (4, '지름', 'diameter', '다이애미터', G)])
inner += sentence('The [g]diameter[/g] of a circle is twice its [b]radius[/b].', '원의 지름은 반지름의 2배이다.', 5)
S.append(sec(inner, 'Parts of a Circle ①', '원의 각 부분을 영어로 (1)', BG2,
             '발음은 한글로 적은 대략값. radius의 복수형은 radii(레이디아이).'))

# 3. 원의 각 부분 (2) --------------------------------------------------------
A, Bp = pt(205), pt(335)
C1, C2 = pt(60), pt(120)
layers = [(0, circ() + dot(O) + lab(O, 'O', 0, 30)),
          (1, arcp(60, 120, R, 14) + dot(C1) + dot(C2) + lab(C1, 'A', 22, -22) + lab(C2, 'B', -22, -22) + tag(pt(90, r=RR+36), 'arc AB', R)),
          (2, ln(A, Bp, BL, 7) + dot(A) + dot(Bp) + lab(A, 'C', -26, 18) + lab(Bp, 'D', 26, 18) + tag((mid(A, Bp)[0], mid(A, Bp)[1]+34), 'chord CD', BL)),
          (3, ln(along(pt(150), pt(10), -0.25), along(pt(150), pt(10), 1.25), G, 5) + tag(along(pt(150), pt(10), 1.12), 'secant', G)),
          (4, sector(60, 120, PU, 0.3) + ln(O, C1, PU, 3) + ln(O, C2, PU, 3) + wedge(O, C1, C2, 44, OR, 0.6)),
          (5, segm(205, 335, OR, 0.35))]
inner = fig(layers) + cards([
    (1, '호 AB', 'arc AB', '아크', R),
    (2, '현 CD', 'chord CD', '코드', BL),
    (3, '할선 (원과 두 점에서 만나는 직선)', 'secant (line)', '시컨트', G),
    (4, '부채꼴 / 중심각', 'sector / central angle', '섹터 / 센트럴 앵글', PU),
    (5, '활꼴 (현과 호로 둘러싸인 부분)', 'segment', '세그먼트', OR)], en_size=42, gap=12)
S.append(sec(inner, 'Parts of a Circle ②', '원의 각 부분을 영어로 (2)', BG2,
             'segment는 "선분(line segment)"이라는 뜻도 있어서, 활꼴을 분명히 말할 때는 circular segment라고 한다.'))

# 4. 현의 성질 ---------------------------------------------------------------
d = 150; al = math.degrees(math.acos(d/RR))
A, Bp = pt(270+al), pt(270-al)
M = mid(A, Bp)
C, D = pt(110+al), pt(110-al); N = mid(C, D)
layers = [(0, circ() + dot(O) + lab(O, 'O', -30, -10) + ln(A, Bp, DARK, 5) + dot(A) + dot(Bp) + lab(A, 'A', 26, 16) + lab(Bp, 'B', -26, 16)),
          (1, ln(O, M, R, 6) + right(M, O, A, c=R) + dot(M, R) + lab(M, 'M', 0, 34, R)),
          (2, tick(A, M, BL) + tick(M, Bp, BL) + ln(A, M, BL, 7) + ln(M, Bp, BL, 7) + dot(M, R) + dot(A) + dot(Bp)),
          (4, ln(C, D, DARK, 5) + dot(C) + dot(D) + lab(C, 'C', -26, -12) + lab(D, 'D', 22, -22) + ln(O, N, G, 6) + right(N, O, C, c=G)
              + dot(N, G) + lab(N, 'N', 26, 20, G) + tick(O, M, R, 2) + tick(O, N, G, 2))]
inner = fig(layers) + cards([
    (1, '수선 (수직인 선) / 수직이다', 'perpendicular', '퍼펜디큘러', R),
    (2, '이등분하다 / 수직이등분선', 'bisect / perpendicular bisector', '바이섹트 / 바이섹터', BL),
    (4, '중심에서 같은 거리에 있는', 'equidistant from the center', '이퀴디스턴트', G)], en_size=40)
inner += sentence('The [r]perpendicular[/r] from the center to a chord [b]bisects[/b] the chord.',
                  '원의 중심에서 현에 내린 수선은 그 현을 이등분한다.  (AM = BM)', 3, y=640, x=960, w=864)
inner += sentence('Chords [g]equidistant[/g] from the center are equal in length.',
                  '중심에서 같은 거리에 있는 두 현의 길이는 같다.  (OM = ON 이면 AB = CD)', 5, y=880, x=96, w=1728)
S.append(sec(inner, 'Chords', '현의 성질을 영어로', BG1))

# 5. 접선 --------------------------------------------------------------------
T = pt(320); u = (math.cos(math.radians(50)), -math.sin(math.radians(50)))
L1 = (T[0]-u[0]*340, T[1]-u[1]*340); L2 = (T[0]+u[0]*300, T[1]+u[1]*300)
layers = [(0, circ() + dot(O) + lab(O, 'O', -30, -10)),
          (1, ln(L1, L2, R, 6) + tag((L2[0]-40, L2[1]+10), 'tangent', R, anchor='end')),
          (2, dot(T, BL, 11) + lab(T, 'T', 34, 20, BL)),
          (3, ln(O, T, G, 6) + right(T, O, L2, 26, G))]
inner = fig(layers) + cards([
    (1, '접선 (원과 한 점에서만 만나는 직선)', 'tangent (line)', '탠전트', R),
    (2, '접점', 'point of tangency', '포인트 오브 탠전시', BL),
    (2, '원에 접한다', 'is tangent to the circle', '', BL),
    (3, '반지름에 수직', 'perpendicular to the radius', '', G)], en_size=42)
inner += sentence('A [r]tangent[/r] is [g]perpendicular to the radius[/g] at the [b]point of tangency[/b].',
                  '원의 접선은 접점을 지나는 반지름에 수직이다.  (OT ⊥ l)', 4)
S.append(sec(inner, 'Tangents', '접선과 접점', BG2, 'tangent는 라틴어 tangere(닿다)에서 온 말.'))

# 6. 접선의 길이 + 내접원 -------------------------------------------------------
c2, r2 = (520, 350), 190; P = (90, 350)
dd = c2[0] - P[0]; t = math.degrees(math.acos(r2/dd))
TA, TB = pt(180-t, c2, r2), pt(180+t, c2, r2)
layers = [(0, circ(c2, r2) + dot(c2) + lab(c2, 'O', 28, 0) + dot(P) + lab(P, 'P', -30, 0)),
          (1, ln(P, along(P, TA, 1.3), R, 5) + ln(P, along(P, TB, 1.3), R, 5) + dot(TA) + dot(TB) + lab(TA, 'A', 4, -34) + lab(TB, 'B', 4, 36)),
          (2, ln(P, TA, BL, 9) + ln(P, TB, BL, 9) + tick(P, TA, BL, 2) + tick(P, TB, BL, 2) + dot(TA) + dot(TB) + dot(P)
              + right(TA, c2, P, 20, G) + right(TB, c2, P, 20, G) + ln(c2, TA, G, 3, True) + ln(c2, TB, G, 3, True))]
inner = fig(layers) + cards([
    (1, '원 밖의 한 점', 'an external point', '익스터널 포인트', R),
    (2, '접선의 길이 (PA, PB)', 'length of a tangent (segment)', '', BL),
    (3, '삼각형의 내접원 / 내심', 'inscribed circle (incircle) / incenter', '인서클 / 인센터', G),
    (4, '삼각형의 외접원 / 외심', 'circumscribed circle (circumcircle) / circumcenter', '서컴서클 / 서컴센터', PU)], en_size=36, gap=12)
inner += sentence('The two [b]tangent segments[/b] from an [r]external point[/r] are equal in length.',
                  '원 밖의 한 점에서 그은 두 접선의 길이는 같다.  (PA = PB)', 2, y=720, x=960, w=864)
S.append(sec(inner, 'Tangent Segments', '접선의 길이', BG1,
             'incircle: 삼각형의 세 변에 모두 접하는 원. circumcircle: 삼각형의 세 꼭짓점을 모두 지나는 원. in-(안), circum-(둘레).'))

# 7. 원주각과 중심각 ------------------------------------------------------------
A, Bp, P = pt(215), pt(325), pt(110)
layers = [(0, circ() + dot(O) + lab(O, 'O', 30, -8) + dot(A) + dot(Bp) + lab(A, 'A', -24, 22) + lab(Bp, 'B', 24, 22)),
          (1, arcp(215, 325, R, 14) + tag(pt(270, r=RR+36), 'arc AB', R)),
          (2, ln(P, A, BL, 5) + ln(P, Bp, BL, 5) + wedge(P, A, Bp, 70, BL, 0.4) + dot(P) + lab(P, 'P', -8, -32)),
          (3, ln(O, A, G, 5) + ln(O, Bp, G, 5) + wedge(O, A, Bp, 60, G, 0.45))]
inner = fig(layers) + cards([
    (1, '호 AB에 대한 (호 AB를 마주 보는)', 'subtended by arc AB', '섭텐디드', R),
    (2, '원주각 ∠APB', 'inscribed angle', '인스크라이브드 앵글', BL),
    (3, '중심각 ∠AOB', 'central angle', '센트럴 앵글', G)])
inner += sentence('An [b]inscribed angle[/b] is [r]half[/r] the [g]central angle[/g] subtended by the same arc.',
                  '한 호에 대한 원주각의 크기는 그 호에 대한 중심각의 크기의 1/2이다.  (∠APB = ½∠AOB)', 4)
S.append(sec(inner, 'Inscribed Angles', '원주각과 중심각', BG2,
             'inscribe = in(안에) + scribe(쓰다, 그리다). 원 "안에 그려진" 각. "subtend"는 "(호·현이 각을) 마주 보다".'))

# 8. 같은 호 / 반원 -------------------------------------------------------------
A, Bp = pt(215), pt(325)
Ps = [pt(70), pt(110), pt(150)]
lay = [(0, circ() + dot(A) + dot(Bp) + lab(A, 'A', -24, 22) + lab(Bp, 'B', 24, 22) + arcp(215, 325, R, 10))]
cols = [BL, PU, G]
for i, (Pp, c) in enumerate(zip(Ps, cols)):
    lay.append((1, ln(Pp, A, c, 4) + ln(Pp, Bp, c, 4) + wedge(Pp, A, Bp, 60, c, 0.4) + dot(Pp) + lab(Pp, 'PQR'[i], 0, -32)))
left = fig(lay, x=96, w=820)
Ad, Bdd, Q = pt(180, (410, 400), 280), pt(0, (410, 400), 280), pt(120, (410, 400), 280)
right_fig = fig([(0, circ((410, 400), 280) + dot((410, 400)) + lab((410, 400), 'O', 0, 34)),
                 (2, segm(0, 180, OR, 0.18) + ln(Ad, Bdd, G, 6) + dot(Ad) + dot(Bdd) + lab(Ad, 'A', -26, 0) + lab(Bdd, 'B', 26, 0)
                  + tag((560, 460), 'diameter', G)),
                 (3, ln(Q, Ad, BL, 5) + ln(Q, Bdd, BL, 5) + right(Q, Ad, Bdd, 30, R) + dot(Q) + lab(Q, 'P', -8, -32) + tag((520, 160), '90°', R))],
                x=1004, w=820)
inner = left + right_fig
inner += sentence('Inscribed angles subtended by the [r]same arc[/r] are [b]equal[/b].', '한 호에 대한 원주각의 크기는 모두 같다.', 1, y=900, x=96, w=860)
inner += sentence('An angle inscribed in a [o]semicircle[/o] is a [r]right angle[/r].', '반원에 대한 원주각의 크기는 90°이다.', 4, y=900, x=984, w=840)
S.append(sec(inner, 'Same Arc · Semicircle', '같은 호에 대한 원주각 / 반원에 대한 원주각', BG1,
             'semicircle = semi(반) + circle. 반원에 대한 원주각이 직각이라는 성질을 "탈레스 정리(Thales\' theorem)"라고도 한다.'))

# 9. 원에 내접하는 사각형 -----------------------------------------------------------
A, Bq, Cq, Dq = pt(120), pt(215), pt(330), pt(40)
E = along(Bq, Cq, 1.3)
layers = [(0, circ() + f'<polygon points="{A[0]},{A[1]} {Bq[0]},{Bq[1]} {Cq[0]},{Cq[1]} {Dq[0]},{Dq[1]}" fill="{BL}" fill-opacity="0.08" stroke="{DARK}" stroke-width="5"/>'
              + ''.join(dot(p) for p in (A, Bq, Cq, Dq)) + lab(A, 'A', -18, -30) + lab(Bq, 'B', -30, 14) + lab(Cq, 'C', 0, 38) + lab(Dq, 'D', 28, -18)),
          (2, wedge(A, Bq, Dq, 60, R, 0.45) + wedge(Cq, Bq, Dq, 60, BL, 0.45) + tag((A[0]+22, A[1]+88), 'x', R) + tag((Cq[0]-80, Cq[1]-50), 'y', BL)),
          (4, ln(Cq, E, DARK, 4, True) + dot(E) + lab(E, 'E', 26, 10) + wedge(Cq, Dq, E, 54, R, 0.45) + tag((Cq[0]+72, Cq[1]-50), 'x', R))]
inner = fig(layers, w=700, h=597) + cards([
    (1, '원에 내접하는 사각형', 'cyclic quadrilateral', '사이클릭 쿼드러래터럴', PU),
    (2, '대각 (마주 보는 각)', 'opposite angles', '아퍼짓 앵글스', BL),
    (3, '합이 180°인 (보각인)', 'supplementary', '서플리멘터리', R),
    (4, '외각 / 내대각', 'exterior angle / interior opposite angle', '익스티리어 앵글', OR)], en_size=38, gap=12)
inner += sentence('The [b]opposite angles[/b] of a cyclic quadrilateral are [r]supplementary[/r].  (x + y = 180°)',
                  '원에 내접하는 사각형의 한 쌍의 대각의 크기의 합은 180°이다.', 3, y=790)
inner += sentence('An [o]exterior angle[/o] equals the [o]interior opposite angle[/o].  (∠DCE = ∠A)',
                  '원에 내접하는 사각형의 한 외각의 크기는 그 내대각의 크기와 같다.', 5, y=930)
S.append(sec(inner, 'Cyclic Quadrilaterals', '원에 내접하는 사각형', BG2,
             'quadrilateral = quadri(4) + lateral(변). "a quadrilateral inscribed in a circle"이라고도 말한다.'))

# 10. 접선과 현이 이루는 각 -----------------------------------------------------------
T = pt(270); X1, X2 = (T[0]-360, T[1]), (T[0]+360, T[1])
A = pt(30); P = pt(150)
layers = [(0, circ() + dot(O) + lab(O, 'O', -26, -18)),
          (1, ln(X1, X2, R, 6) + dot(T) + lab(T, 'T', 0, 36) + lab((X2[0]-30, X2[1]), 'X', 0, -30)
              + ln(T, A, BL, 6) + dot(A) + lab(A, 'A', 28, -8) + wedge(T, X2, A, 70, R, 0.45)),
          (2, arcp(270, 30, OR, 14)),
          (3, ln(P, T, G, 5) + ln(P, A, G, 5) + wedge(P, T, A, 64, G, 0.45) + dot(P) + lab(P, 'P', -26, -20))]
inner = fig(layers, w=700, h=597) + cards([
    (1, '접선과 현이 이루는 각 ∠ATX', 'the angle between a tangent and a chord', '', R),
    (2, '그 각의 내부에 있는 호', 'the arc inside the angle (arc TA)', '', OR),
    (3, '그 호에 대한 원주각 ∠TPA', 'the inscribed angle on the other side', '', G)], en_size=36)
inner += sentence('The angle between a [r]tangent[/r] and a [b]chord[/b] equals the [g]inscribed angle[/g] in the alternate segment.',
                  '원의 접선과 그 접점을 지나는 현이 이루는 각의 크기는 그 각의 내부에 있는 호에 대한 원주각의 크기와 같다.  (∠ATX = ∠TPA)', 4, y=820)
S.append(sec(inner, 'Tangent–Chord Angle', '접선과 현이 이루는 각', BG1,
             '영어권에서는 "alternate segment theorem(교대 활꼴 정리)"이라 부른다. alternate segment = 현 TA의 반대쪽 활꼴(점 P가 있는 쪽).'))

# 11. 기호 읽기 ------------------------------------------------------------------------
ov = lambda s: f'<span style="text-decoration:overline">{s}</span>'
arcsym = lambda s: f'<span style="display:inline-block; border-top:3px solid {DARK}; border-radius:50% 50% 0 0 / 16px 16px 0 0; padding:4px 4px 0; line-height:1">{s}</span>'
rows = [(f'∠APB = 40°', 'Angle APB is forty degrees.'),
        (ov('AB'), 'segment AB'),
        (arcsym('AB'), 'arc AB'),
        ('AB = 6 cm', 'AB is six centimeters (long).'),
        (f'{ov("AB")} ⊥ {ov("CD")}', 'AB is perpendicular to CD.'),
        (f'{ov("AB")} ∥ {ov("CD")}', 'AB is parallel to CD.'),
        ('△ABC ≡ △DEF', 'Triangle ABC is congruent to triangle DEF.'),
        ('∠x + ∠y = 180°', 'Angle x plus angle y equals one hundred eighty degrees.')]
trs = ''.join(f'<tr {B(i+1)}><td style="font-family:Times New Roman,serif; font-size:44px; padding-top:16px">{a}</td>'
              f'<td style="font-family:{EN}; text-align:left; font-weight:600">{H.escape(b)}</td></tr>' for i, (a, b) in enumerate(rows))
inner = (f'<table id="t11" style="position:absolute; left:96px; top:190px; width:1728px; border-collapse:collapse; font-size:38px; text-align:center; background:#FFF">'
         f'<tr style="background:#DCEBEE"><th style="padding:12px; width:520px">기호</th><th style="text-align:left">영어로 읽기</th></tr>{trs}</table>'
         '<style>#t11 td{padding:10px 24px;border-top:1px solid #E5E7EB}</style>')
S.append(sec(inner, 'Reading Math', '기호를 영어로 읽어 보자', BG2,
             '각도는 degree(s), ≡ 합동은 congruent(컹그루언트), ∽ 닮음은 similar. 이등변삼각형은 isosceles triangle(아이사슬리즈).'))

# 12. 단어 속 뜻 -------------------------------------------------------------------------
roots = [('tangent', 'tang- = 닿다 (라틴어)', '원에 닿는 선 → 접선', R),
         ('secant', 'sec- = 자르다', '원을 자르는 선 → 할선', G),
         ('diameter', 'dia- = 가로질러 + meter = 재다', '가로질러 잰 길이 → 지름', BL),
         ('circumference', 'circum- = 둘레 + fer = 나르다', '둘레를 도는 길이 → 원주', PU),
         ('inscribed', 'in- = 안 + scribe = 쓰다·그리다', '안에 그린 → 내접하는, 원주각', OR),
         ('bisect', 'bi- = 둘 + sect = 자르다', '둘로 자르다 → 이등분하다', R),
         ('semicircle', 'semi- = 반', '반쪽 원 → 반원', G),
         ('chord', 'chord = (악기의) 줄', '호에 걸린 줄 → 현(絃)', BL)]
cells = ''.join(box(96 + (i % 2) * 874, 190 + (i // 2) * 205, 854,
                    f'<p style="font-family:{EN}; font-size:44px; font-weight:700; color:{c}">{a}</p>'
                    f'<p style="font-size:30px">{H.escape(b)}  →  <b>{H.escape(d)}</b></p>', n=i+1, size=30) for i, (a, b, d, c) in enumerate(roots))
S.append(sec(cells, 'Word Roots', '영어 단어 속에 뜻이 숨어 있다', BG1,
             '"현(絃)"도 한자로 악기 줄이라는 뜻이라 chord와 뜻이 같다는 점을 짚어 주면 좋다.'))

# 13. 퀴즈 1: 한국어 → 영어 -----------------------------------------------------------
qs = [('현', 'chord'), ('접선', 'tangent'), ('원주각', 'inscribed angle'), ('중심각', 'central angle'), ('지름', 'diameter'),
      ('반지름', 'radius'), ('호', 'arc'), ('접점', 'point of tangency'), ('부채꼴', 'sector'), ('원에 내접하는 사각형', 'cyclic quadrilateral')]
cells = ''.join(f'<div style="position:absolute; left:{96 + (i % 2) * 874}px; top:{190 + (i // 2) * 160}px; width:854px; height:140px; background:#FFF; '
                f'border-radius:16px; display:flex; align-items:center; padding:0 30px; gap:24px">'
                f'<span style="font-size:36px; font-weight:700; min-width:400px">{i+1}. {H.escape(k)}</span>'
                f'<span {B(i+1, "pop")} style="font-size:42px; font-weight:700; color:{R}; font-family:{EN}">{H.escape(e)}</span></div>'
                for i, (k, e) in enumerate(qs))
S.append(sec(cells, 'Quiz ①', '영어로 말해 보자!', BG2, '한 번 클릭할 때마다 답이 하나씩 나온다.'))

# 14. 퀴즈 2: 빈칸 --------------------------------------------------------------------
fills = [('An inscribed angle is ____ the central angle subtended by the same arc.', 'half'),
         ('A tangent is ____ to the radius at the point of tangency.', 'perpendicular'),
         ('The perpendicular from the center to a chord ____ the chord.', 'bisects'),
         ('An angle inscribed in a ____ is a right angle.', 'semicircle'),
         ('The opposite angles of a cyclic quadrilateral are ____.', 'supplementary'),
         ('The two tangent segments from an external point are ____ in length.', 'equal')]
cells = ''
for i, (s, a) in enumerate(fills):
    pre, post = s.split('____')
    cells += (f'<div style="position:absolute; left:96px; top:{190 + i * 140}px; width:1728px; height:122px; background:#FFF; border-radius:16px; '
              f'display:flex; align-items:center; padding:0 32px; font-family:{EN}; font-size:40px">'
              f'<span style="font-weight:700; color:{TEAL}; margin-right:20px">{i+1}.</span>{H.escape(pre)}'
              f'<span style="display:inline-block; min-width:220px; border-bottom:4px solid {DARK}; text-align:center; margin:0 10px">'
              f'<b {B(i+1, "pop")} style="color:{R}">{H.escape(a)}</b></span>{H.escape(post)}</div>')
S.append(sec(cells, 'Quiz ②', '빈칸에 알맞은 단어는?', BG1))

shell = open(os.path.join(HERE, 'shell.html')).read()
open(OUT, 'w').write(shell.replace('%%TITLE%%', '원의 성질 - 영어로 배우기').replace('%%SLIDES%%', '\n'.join(S)))
print(OUT, len(S))
