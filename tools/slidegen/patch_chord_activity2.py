import sys, math, re
sys.path.insert(0, '/home/user/outeq111/tools/slidegen')
from lib import line, poly, wedge, right, text, dot, rich, FONT, R, BL, G
F = sys.argv[1]
s = open(F, encoding='utf-8').read()
s = s.replace('슬슬이', '술술이')

r = 200
def P(c, deg): return (c[0] + r*math.cos(math.radians(deg)), c[1] + r*math.sin(math.radians(deg)))
C1, C2 = (270, 330), (820, 330)
A1, B1, P1 = P(C1, 120), P(C1, 60), P(C1, 270)
A2, B2, P2 = P(C2, 150), P(C2, 30), P(C2, 270)
M2 = ((A2[0]+B2[0])/2, (A2[1]+B2[1])/2)
DK = '#1E2A3A'
def lab(p, t, dx, dy): return text((p[0]+dx, p[1]+dy), t, DK, 34)
base = (f'<circle cx="{C1[0]}" cy="{C1[1]}" r="{r}" fill="none" stroke="{DK}" stroke-width="4"/>'
        f'<circle cx="{C2[0]}" cy="{C2[1]}" r="{r}" fill="none" stroke="{DK}" stroke-width="4"/>'
        + dot(C1, DK, 6) + dot(C2, DK, 6) + lab(C1, 'O', 10, -10) + lab(C2, 'O', 10, -12)
        + lab(A1, 'A', -34, 28) + lab(B1, 'B', 10, 28) + lab(P1, 'P', -10, -14)
        + lab(A2, 'A', -36, 16) + lab(B2, 'B', 12, 16) + lab(P2, 'P', -10, -14)
        + text((C1[0], 630), '원주각 30°', DK, 32, 'middle') + text((C2[0], 630), '원주각 60°', DK, 32, 'middle'))
st1 = [line(P1, A1, R, 4), line(P1, B1, R, 4), wedge(P1, A1, B1, 60, R, 0.5), text((P1[0], P1[1]+95), '30°', R, 30, 'middle'),
       poly([C1, A1, B1], BL, 0.2, BL), wedge(C1, A1, B1, 34, BL, 0.5), text((C1[0], C1[1]+75), '60°', BL, 28, 'middle'),
       text(((C1[0]+A1[0])/2-28, (C1[1]+A1[1])/2), '1', BL, 32), text(((C1[0]+B1[0])/2+16, (C1[1]+B1[1])/2), '1', BL, 32),
       line(A1, B1, G, 6), text(((A1[0]+B1[0])/2, A1[1]+62), 'AB = 1', G, 32, 'middle')]
st2 = [line(P2, A2, R, 4), line(P2, B2, R, 4), wedge(P2, A2, B2, 60, R, 0.5), text((P2[0], P2[1]+95), '60°', R, 30, 'middle'),
       poly([C2, A2, B2], BL, 0.2, BL), wedge(C2, A2, B2, 30, BL, 0.5), text((C2[0], C2[1]+62), '120°', BL, 26, 'middle'),
       text(((C2[0]+A2[0])/2-10, (C2[1]+A2[1])/2-14), '1', BL, 32), text(((C2[0]+B2[0])/2+4, (C2[1]+B2[1])/2-14), '1', BL, 32)]
st3 = [line(A2, B2, G, 6), text((M2[0], M2[1]+40), 'AB < 1 + 1 = 2', G, 30, 'middle')]
st4 = [line(C2, M2, '#B5651D', 3, True), right(M2, C2, B2, 14, '#B5651D'), text((M2[0], M2[1]+80), '(실제 AB = √3 ≈ 1.73)', '#B5651D', 26, 'middle')]

box = 'position:absolute; left:96px; top:190px; width:1100px; height:660px'
def svg(inner, step=None):
    b = f' data-build-in="fade {step}"' if step else ''
    return f'<svg{b} style="{box}" viewBox="0 0 1100 660">{inner}</svg>'
txt = [
 '① 원주각 [r]30°[/r] → 중심각 [b]60°[/b]\nOA = OB = 1 → △OAB는 [b]정삼각형[/b]\n→ [g]AB = 1[/g]',
 '② 원주각을 2배인 [r]60°[/r]로 → 중심각 [b]120°[/b]\n정비례라면 AB = 2가 되어야 한다.',
 '③ 삼각형에서 두 변의 길이의 합은\n나머지 한 변의 길이보다 크다\n→ [g]AB < OA + OB = 1 + 1 = 2[/g]',
 '④ 실제로 AB = √3 ≈ 1.73 (2가 아니다)',
]
ps, y = '', 190
for i, t in enumerate(txt):
    ps += f'<p data-build-in="rise {i+1}" style="position:absolute; left:1230px; top:{y}px; width:600px; font-size:32px; line-height:1.4">{rich(t)}</p>'
    y += (t.count("\n")+1)*46 + 50
sec = ('<section style="background:#EEF4F4; color:#1E2A3A; font-family:' + FONT + '; padding:96px; display:flex; flex-direction:column">'
       '<p style="position:absolute; left:96px; top:44px; width:1700px; font-size:30px; font-weight:700; color:#1F7A8C">활동 2 · 해냄이의 말이 틀린 이유</p>'
       '<p style="position:absolute; left:96px; top:90px; width:1728px; font-size:40px; font-weight:700; line-height:1.3">“한 원에서 현 AB의 길이는 호 AB에 대한 원주각의 크기에 정비례해.”</p>'
       f'<div style="{box}; background:#FFFFFF; border-radius:16px"></div>' + svg(base) + svg(''.join(st1), 1) + svg(''.join(st2), 2) + svg(''.join(st3), 3) + svg(''.join(st4), 4) + ps +
       '<p data-build-in="pop 5" style="position:absolute; left:96px; top:880px; width:1500px; font-size:38px; font-weight:700; background:#FCE0C4; padding:18px 30px; border-radius:16px">원주각이 2배가 되어도 현의 길이는 2배가 아니다 → 정비례하지 않는다</p>'
       '<aside>반지름을 1로 두면 원주각 30°일 때 현의 길이가 1입니다. 원주각을 60°로 2배 하면, 정비례라면 현이 2여야 하지만 삼각형의 세 변 사이의 관계 때문에 2보다 작습니다(실제 √3). 참고로 2가 되는 것은 원주각 90°(지름)일 때입니다.</aside></section>')
i = s.index('활동 2 · 해냄이'); a = s.rfind('<section', 0, i); b = s.index('</section>', i) + 10
s = s[:a] + sec + s[b:]
open(F, 'w', encoding='utf-8').write(s)
print('ok', s.count('술술이'), s.count('슬슬이'))
