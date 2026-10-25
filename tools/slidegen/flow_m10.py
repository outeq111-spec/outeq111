"""중단원 마무리(204~206) 도전 문제 10: '풀이 흐름 정리' 순서도 슬라이드를 10 (2) 풀이 뒤에 넣는다.
주어진 것(회색 점선) → 성질(화살표 위 이유) → 알아낸 것 → (1) → (2). 클릭마다 한 칸씩 나오고 왼쪽 그림에 같은 색으로 표시.
사용: python3 tools/slidegen/flow_m10.py  (저장소 루트에서, 여러 번 돌려도 같은 결과)
덱을 다시 만들면(deck5.py) 이 스크립트 → page_labels.py 순서로 다시 실행."""
import re

F = '204-206_원주각_중단원마무리_풀이.html'
AFTER = '10 (2) 풀이'          # 이 제목의 슬라이드 뒤에 넣는다
MARK = 'data-flow="m10"'
R, BL, G, OR, PU = '#E4572E', '#1F6FB2', '#2E9E5B', '#D9822B', '#8E44AD'
ACC = '#B5651D'
FONT = "'Noto Sans KR','Apple SD Gothic Neo','Malgun Gothic','Nanum Gothic',sans-serif"
RT5 = '√<span style="text-decoration:overline">5</span>'

# 그림 좌표(교과서 그림 viewBox 400×384, deck5.py의 m10 snap 결과)
A, Gp, C, H = (226.4, 52.4), (226.1, 165.7), (340.2, 266.1), (339.9, 151.5)
O, D = (189.7, 209.1), (189.57, 265.75)
FX, FY, FW = 50, 200, 540                       # 그림 위치·너비
FH = FW * 384 / 400

def ln(a, b, c, w=4):
    return f'<line x1="{a[0]}" y1="{a[1]}" x2="{b[0]}" y2="{b[1]}" stroke="{c}" stroke-width="{w}" stroke-linecap="round"/>'
def rt(path, c):
    return f'<path d="{path}" fill="none" stroke="{c}" stroke-width="2.5"/>'
FIGSTEP = {   # 단계 -> 그림 위 표시 (10 (1)(2) 풀이와 같은 도형)
    2: [rt('M326.2,266.1 L326.2,252.1 L340.2,252.1', R), ln(C, H, R), rt('M217.2,62.9 L227.7,72.1 L236.9,61.6', BL), ln(A, H, BL)],
    3: [ln(A, Gp, R)],
    4: [ln(Gp, C, BL)],
    5: [f'<polygon points="{A[0]},{A[1]} {Gp[0]},{Gp[1]} {C[0]},{C[1]} {H[0]},{H[1]}" fill="{G}" fill-opacity="0.25" stroke="{G}" stroke-width="2.5"/>'],
    6: [f'<circle cx="{D[0]}" cy="{D[1]}" r="5" fill="{PU}"/>', f'<circle cx="{O[0]}" cy="{O[1]}" r="5" fill="{PU}"/>', ln(O, D, PU)],
    7: [ln(C, H, PU, 6)],
    8: [ln(A, Gp, OR, 7), ln(C, H, OR, 7)],
}

# 순서도 칸: 이름 -> (단계, 가운데 x, 가운데 y, 너비, 높이, 종류/색, 글)
N = {
    'GB': (1, 1160, 175, 300, 62, 'given', 'BH는 원 O의 지름'),
    'GD': (1, 1745, 175, 230, 92, 'given', f'OD ⊥ BC<br>OD = {RT5} cm'),
    'GA': (1, 700, 360, 190, 62, 'given', 'AE ⊥ BC'),
    'GC': (1, 1395, 360, 190, 62, 'given', 'CF ⊥ AB'),
    'N1': (2, 920, 360, 210, 62, R, '∠BCH = 90°'),
    'N2': (2, 1170, 360, 210, 62, BL, '∠BAH = 90°'),
    'P1': (3, 810, 540, 210, 62, R, 'AG ∥ CH'),
    'P2': (4, 1282, 540, 210, 62, BL, 'AH ∥ GC'),
    'R1': (5, 1046, 720, 440, 68, 'res', '(1) □AGCH는 평행사변형'),
    'M':  (6, 1720, 360, 270, 92, PU, 'O는 BH의 중점<br>D는 BC의 중점'),
    'K':  (7, 1720, 540, 250, 92, PU, f'CH = 2OD<br>= 2{RT5} cm'),
    'ANS': (8, 1380, 930, 460, 74, 'res', f'(2) AG = CH = 2{RT5} cm'),
}
def top(k): n = N[k]; return n[2] - n[4] / 2
def bot(k): n = N[k]; return n[2] + n[4] / 2
def elbow(src, dst, midy):
    s, d = N[src], N[dst]
    return [(s[1], bot(src)), (s[1], midy), (d[1], midy), (d[1], top(dst))]
# 화살표: (단계, 점들, 색)
E = [
    (2, elbow('GB', 'N1', 268), R), (2, elbow('GB', 'N2', 268), BL),
    (3, elbow('GA', 'P1', 470), R), (3, elbow('N1', 'P1', 470), R),
    (4, elbow('N2', 'P2', 470), BL), (4, elbow('GC', 'P2', 470), BL),
    (5, elbow('P1', 'R1', 648), G), (5, elbow('P2', 'R1', 648), G),
    (6, [(1310, 175), (1600, 175), (1600, top('M'))], PU), (6, [(1745, bot('GD')), (1745, top('M'))], PU),
    (7, [(1720, bot('M')), (1720, top('K'))], PU),
    (8, elbow('R1', 'ANS', 850), OR), (8, [(1720, bot('K')), (1720, 850), (1380, 850), (1380, top('ANS'))], OR),
]
# 이유(성질) 꼬리표: (단계, x, y, 글, 색)
L = [
    (2, 1045, 268, '반원에 대한 원주각', '#4A5568'),
    (3, 810, 470, 'BC에 수직인 두 직선', R),
    (4, 1282, 470, 'AB에 수직인 두 직선', BL),
    (5, 1046, 648, '두 쌍의 대변이 각각 평행', G),
    (6, 1712, 250, '중심에서 현에 내린 수선', PU),
    (7, 1720, 450, '△BCH 중점연결정리', PU),
    (8, 1380, 850, '평행사변형의 대변', OR),
]

def build(img):
    out = [f'<section {MARK} style="background:#EEF4F4; color:#1E2A3A; font-family:{FONT}; padding:96px; display:flex; flex-direction:column">',
           f'<p style="position:absolute; left:96px; top:44px; width:1300px; font-size:30px; font-weight:700; color:{ACC}">10 풀이 흐름 정리 · 주어진 것에서 답까지</p>',
           f'<img src="{img}" style="position:absolute; left:{FX}px; top:{FY}px; width:{FW}px; height:{FH:.1f}px; background:#FFFFFF; border-radius:14px">',
           # 범례
           f'<div style="position:absolute; left:{FX}px; top:{FY + FH + 40:.0f}px; width:{FW}px; font-size:24px; line-height:1.3; display:flex; flex-direction:column; gap:16px">'
           '<div><span style="display:inline-block; padding:4px 16px; background:#E6EAF0; border:3px dashed #8A94A6; border-radius:10px; font-weight:700">회색 점선</span> 문제에서 주어진 것</div>'
           f'<div><span style="display:inline-block; padding:4px 16px; background:#fff; border:4px solid {R}; border-radius:10px; font-weight:700">색 칸</span> 성질로 알아낸 것</div>'
           '<div><span style="display:inline-block; padding:2px 14px; background:#fff; border:2px solid #A0AEC0; border-radius:20px; font-size:22px">꼬리표</span> 화살표의 이유(성질)</div></div>']
    for k in sorted(FIGSTEP):
        out.append(f'<svg data-build-in="fade {k}" style="position:absolute; left:{FX}px; top:{FY}px; width:{FW}px; height:{FH:.1f}px" viewBox="0 0 400 384">{"".join(FIGSTEP[k])}</svg>')
    out.append('<svg style="position:absolute; left:0; top:0; width:1920px; height:1080px" viewBox="0 0 1920 1080"><defs>'
               + ''.join(f'<marker id="ah{c[1:]}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="5" markerHeight="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="{c}"/></marker>'
                         for c in (R, BL, G, PU, OR)) + '</defs></svg>')
    for st in sorted({e[0] for e in E}):
        paths = ''.join(f'<polyline points="{" ".join(f"{x},{y}" for x, y in pts)}" fill="none" stroke="{c}" stroke-width="4" '
                        f'stroke-linejoin="round" marker-end="url(#ah{c[1:]})"/>' for s, pts, c in E if s == st)
        out.append(f'<svg data-build-in="fade {st}" style="position:absolute; left:0; top:0; width:1920px; height:1080px" viewBox="0 0 1920 1080">{paths}</svg>')
    for st, x, y, t, c in L:
        out.append(f'<div data-build-in="fade {st}" style="position:absolute; left:{x}px; top:{y}px; transform:translate(-50%,-50%); white-space:nowrap; '
                   f'font-size:23px; font-weight:700; color:{c}; background:#fff; border:2px solid {c}; border-radius:20px; padding:2px 14px">{t}</div>')
    for k, (st, x, y, w, h, kind, t) in N.items():
        if kind == 'given':
            sty = 'background:#E6EAF0; border:3px dashed #8A94A6; color:#1E2A3A'
        elif kind == 'res':
            sty = f'background:#FCE0C4; border:4px solid {ACC}; color:#1E2A3A; font-size:32px'
        else:
            sty = f'background:#fff; border:4px solid {kind}; color:{kind}'
        anim = 'fade' if st == 1 else 'pop'
        out.append(f'<div class="fcn" data-build-in="{anim} {st}" style="position:absolute; left:{x - w / 2:.0f}px; top:{y - h / 2:.0f}px; width:{w}px; height:{h}px; '
                   f'display:flex; align-items:center; justify-content:center; text-align:center; font-size:28px; font-weight:700; line-height:1.25; '
                   f'border-radius:12px; {sty}"><span>{t}</span></div>')
    out.append('</section>')
    return ''.join(out)

# 방금 나온 칸 강조 (플레이어의 노란 형광과 같은 색)
CSS = '<style id="flowcss">section .fcn.cur{box-shadow:0 0 0 8px #FFF1A8,0 0 0 11px #E8C547}</style>'
JS = ('<script id="flowjs">(function(){var s0=show;show=function(){s0();'
      'document.querySelectorAll("section .fcn.cur").forEach(function(e){e.classList.remove("cur")});'
      'var g=G[i][step-1];if(g&&step>0)g.forEach(function(e){if(e.classList.contains("fcn"))e.classList.add("cur")});};show();})();</script>')

if __name__ == '__main__':
    h = open(F, encoding='utf-8').read()
    h = re.sub(r'<section ' + MARK + r'.*?</section>', '', h, flags=re.S)
    h = re.sub(r'<style id="flowcss">.*?</style>', '', h); h = re.sub(r'<script id="flowjs">.*?</script>', '', h, flags=re.S)
    secs = [m.start() for m in re.finditer(r'<section', h)] + [h.rfind('</div><button id="fs">')]
    k = next(j for j in range(len(secs) - 1) if f'>{AFTER}</p>' in h[secs[j]:secs[j + 1]])
    sec = h[secs[k]:secs[k + 1]]
    img = re.search(r'<img src="(data:image/png;base64,[^"]+)"', sec).group(1)
    h = h[:secs[k + 1]] + build(img) + h[secs[k + 1]:]
    h = h.replace('</head>', CSS + '</head>', 1).replace('</body>', JS + '</body>', 1)
    open(F, 'w', encoding='utf-8').write(h)
    print('inserted as slide', k + 2, 'of', h.count('<section'))
