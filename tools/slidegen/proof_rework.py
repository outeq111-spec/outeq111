"""증명(설명) 슬라이드를 '처음 주어진 그림'에서 시작하도록 고친다.
교과서 그림에서 보조선·각 표시·작도한 점을 지운 그림(proof_specs)을 바탕으로 깔고,
단계마다 지운 것들을 색으로 다시 그려 마지막에 교과서 그림이 완성되게 한다.

python3 proof_rework.py  → 저장소 루트의 세 HTML을 제자리 수정 (이미 고친 슬라이드는 건너뜀).
deck2.py / deck34.py로 덱을 다시 만든 뒤에도 이 스크립트를 한 번 더 돌리면 된다."""
import os, re, io, base64
from PIL import Image
import lib
from lib import line, wedge, right, arc, dot, R, BL, G, OR, DARK
import proof_specs as ps
from proof_base import circum

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')
MARK = 'data-proofbase'


def lab(p, s, size=30, c='#231F20'):
    return (f'<text x="{p[0]:.1f}" y="{p[1]:.1f}" font-size="{size}" font-family="Times New Roman,serif" fill="{c}" '
            f'text-anchor="middle" dominant-baseline="middle">{s}</text>')


def ital(p, s, c, size=28):
    return (f'<text x="{p[0]:.1f}" y="{p[1]:.1f}" font-size="{size}" font-family="Times New Roman,serif" font-style="italic" '
            f'font-weight="700" fill="{c}" text-anchor="middle" dominant-baseline="middle" stroke="#FFF" stroke-width="4" paint-order="stroke">{s}</text>')


def seg(a, b, c=DARK, w=2.6):
    return line(a, b, c, w)


INK = '#231F20'


def adds(name):
    """단계 번호 → 그 단계 SVG 앞에 더할 요소 (지운 보조선·점 다시 그리기)"""
    p = ps.P.get(name, {})
    if name == 'd2_5':
        return {2: ''.join(seg(p['O'], p[k], BL, 3) for k in 'ABCD')}
    if name == 'd3_2':
        return {1: seg(p['O'], p['B'], PUR, 3) + seg(p['O'], p['D'], PUR, 3) + dot(p['O'], INK, 4.5),
                -1: ital((168, 170), 'y', BL) + ital((207, 238), 'x', R)}   # -1: 1단계 SVG 뒤에 (글자는 부채꼴 위)
    if name == 'd3_7':
        c, r = circum(p['A'], p['B'], p['C'])
        solid = arc(c, r, p['C'], p['E'], p['B'], INK, 2.6).replace('stroke-opacity="0.85"', '')
        dash = arc(c, r, p['E'], p['C'], p['D'], INK, 2.6).replace('stroke-opacity="0.85"', 'stroke-dasharray="7 6"')
        return {2: solid + dash + seg(p['A'], p['E'], BL, 3) + seg(p['E'], p['C'], BL, 3) + dot(p['E'], INK, 4.5)
                + lab((p['E'][0], p['E'][1]-24), 'E') + dot(c, INK, 4.5) + lab((c[0], c[1]+26), 'O')}
    if name in ('d4_6', 'd4_7'):
        return {1: seg(p['C'], p['D'], BL, 4) + dot(p['D'], INK, 4.5) + lab((p['D'][0], p['D'][1]-24), 'D')}
    return {}


PUR = '#8E44AD'

TARGETS = [  # (파일, 슬라이드를 찾는 글귀, 그림 이름)
    ('195-197_원주각_2차시_원주각과호의길이.html', '길이가 같은 호에 대한 원주각의 크기가 같음을 설명해 보자', 'd2_5'),
    ('198-199_원주각의활용_1차시_원에내접하는사각형.html', '한 쌍의 대각의 크기의 합이 180°임을 설명해 보자', 'd3_2'),
    ('198-199_원주각의활용_1차시_원에내접하는사각형.html', '∠A = ∠DCE임을 설명하시오', 'd3_6'),
    ('198-199_원주각의활용_1차시_원에내접하는사각형.html', '원에 내접하는 사각형의 조건', 'd3_7'),
    ('200-203_원주각의활용_2차시_접선과현이이루는각.html', '경우 ① · ∠BAT가 직각', 'd4_5'),
    ('200-203_원주각의활용_2차시_접선과현이이루는각.html', '경우 ② · ∠BAT가 예각', 'd4_6'),
    ('200-203_원주각의활용_2차시_접선과현이이루는각.html', '경우 ③ ∠BAT가 둔각', 'd4_7'),
]


def uri(im):
    b = io.BytesIO(); im.save(b, 'PNG', optimize=True)
    return 'data:image/png;base64,' + base64.b64encode(b.getvalue()).decode()


def rework(sec, name):
    m = re.search(r'<img src="data:image/\w+;base64,([^"]+)"', sec)
    orig = Image.open(io.BytesIO(base64.b64decode(m.group(1)))).convert('RGB')
    os.makedirs(ps.OUTD, exist_ok=True)
    orig.save(os.path.join(ps.OUTD, name + '_orig.png'))
    base = ps.build(name, orig)
    base.save(os.path.join(ps.OUTD, name + '_base.png'))
    sec = sec[:m.start()] + f'<img {MARK}="{name}" src="{uri(base)}"' + sec[m.end():]
    add = adds(name)

    def sub(mm):
        n = int(mm.group(1))
        pre, post = add.get(n, ''), (add.get(-1, '') if n == 1 else '')
        return mm.group(0)[:mm.start(2)-mm.start(0)] + pre + mm.group(2) + post + '</svg>'
    return re.sub(r'<svg data-build-in="fade (\d+)"[^>]*>(.*?)</svg>', sub, sec, flags=re.S)


def main():
    for f in sorted(set(t[0] for t in TARGETS)):
        path = os.path.join(ROOT, f); h = open(path).read(); n = 0
        for ff, key, name in TARGETS:
            if ff != f: continue
            secs = [s for s in re.findall(r'<section.*?</section>', h, re.S) if key in s]
            assert len(secs) == 1, (f, key, len(secs))
            if MARK in secs[0]: continue
            h = h.replace(secs[0], rework(secs[0], name), 1); n += 1
        open(path, 'w').write(h)
        print(f, n, '장 수정')


if __name__ == '__main__':
    main()
