import re
from geo import SPEC
for fn in ['deck1.py','deck2.py']:
    s=open(fn).read()
    if "from geo import G" in s: continue
    s=s.replace("from lib import *","from lib import *\nfrom geo import G")
    if fn=='deck1.py':
        s=s.replace("p = dict(O=(263, 152), L1=(70, 138), L2=(70, 182), R1=(385, 88), R2=(345, 272))",
                    "p = dict(O=(255, 145), L1=(119, 116), L2=(119, 171), R1=(374, 81), R2=(337, 249))")
        a=s.index("c = (166, 164)"); b=s.index("S.append(crops('설명하기 ①'")
        s=s[:a]+'''p = dict(c1a=(30, 152), c1b=(135, 31), c2a=(80, 270), c2b=(287, 223))
p, C = G('bora', p)
def pb(u, v, k1, k2):
    m = ((u[0]+v[0])/2, (u[1]+v[1])/2); d = (-(v[1]-u[1]), v[0]-u[0]); n = (d[0]**2+d[1]**2)**0.5
    return (m[0]+d[0]/n*k1, m[1]+d[1]/n*k1), (m[0]+d[0]/n*k2, m[1]+d[1]/n*k2)
b1 = pb(p['c1a'], p['c1b'], -40, 210); b2 = pb(p['c2a'], p['c2b'], -40, 200)
Ob = inter(b1[0], b1[1], b2[0], b2[1])
S.append(solve('문제 5 · 보라의 방법', '현의 수직이등분선을 이용하기', 'bora', [
    ('① 두 현의 [r]수직이등분선[/r]을 그린다.', [line(b1[0], b1[1], R, 4, True), line(b2[0], b2[1], R, 4, True)]),
    ('② 현의 수직이등분선은 [b]원의 중심을 지난다[/b]', []),
    ('③ 두 직선이 만나는 점이 [b]원의 중심[/b]', [dot(Ob, BL, 7), text((Ob[0]+10, Ob[1]-10), 'O', BL, 26)])]))
p = dict(V=(177, 30), L=(41, 168), R=(311, 168), H1=(68, 85), H2=(282, 85), V2=(282, 254))
p, C = G('won', p)
Ow = inter(p['L'], p['R'], p['H1'], p['V2'])
S.append(solve('문제 5 · 원혁이의 방법', '원주각이 90°인 직각삼각형 이용하기', 'won', [
    ('① 원주각이 90°이면 그 현은 [b]지름[/b]', [line(p['L'], p['R'], BL, 5)]),
    ('② 다른 직각에서도 빗변을 그으면 또 하나의 [g]지름[/g]', [line(p['H1'], p['V2'], G, 5)]),
    ('③ 두 지름이 만나는 점이 [r]원의 중심[/r]', [dot(Ow, R, 7), text((Ow[0]+8, Ow[1]-10), 'O', R, 26)])]))

'''+s[b:]
    out=[]; lines=s.split('\n')
    for i,l in enumerate(lines):
        out.append(l)
        if re.search(r"(^|; )p = dict\(", l) and "G('" not in lines[i+1]:
            nxt='\n'.join(lines[i+1:i+8])
            m=re.search(r"'(%s)'" % '|'.join(SPEC), nxt)
            if m: out.append(f"p, C = G('{m.group(1)}', p)")
    s='\n'.join(out)
    s=re.sub(r"arc\((?:c|p\['O'\]), [\d.]+,", "arc(C[0], C[1],", s)
    open(fn,'w').write(s)
    print(fn, s.count("G('"), s.count("arc(C[0]"))
