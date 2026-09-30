"""증명 슬라이드 7장: 원래 그림(figs 폴더 or HTML에서 추출) → 처음 주어진 그림(assets/proofbase/*.png)."""
import os
from PIL import Image
from proof_base import Eraser, circum

HERE = os.path.dirname(os.path.abspath(__file__))
OUTD = os.path.join(HERE, 'assets', 'proofbase')

# 점 좌표 (그림 픽셀 단위, 기존 오버레이의 snap 결과)
P = {
 'd2_5': dict(O=(187.5, 192.1), A=(56.1, 282.3), B=(135.8, 342.9), C=(239.3, 342.8), D=(319.0, 282.2), P=(85.8, 69.4), Q=(289.4, 69.5)),
 'd3_2': dict(O=(187.5, 203.7), A=(116.0, 61.1), B=(63.4, 303.9), C=(311.5, 304.0), D=(339.9, 156.6)),
 'd3_7': dict(A=(55.0, 124.8), B=(55.5, 304.6), C=(329.1, 286.4), D=(330.2, 142.7), E=(159.1, 57.3)),
 'd4_6': dict(A=(194.3, 354.8), D=(195.1, 59.4), C=(49.4, 235.3), B=(289.4, 94.0)),
 'd4_7': dict(A=(195.8, 351.8), D=(196.0, 56.6), C=(50.9, 232.4), B=(85.3, 106.3)),
}


def build(name, im):
    e = Eraser(im)
    p = P.get(name, {})
    if name == 'd2_5':
        c, r = circum(p['A'], p['B'], p['D'])
        e.keep_circle(c, r)
        for a, b in [('P', 'A'), ('P', 'B'), ('Q', 'C'), ('Q', 'D')]: e.keep_seg(p[a], p[b])
        e.keep_pt(p['O'], 5).keep_box(170, 140, 205, 178)          # 점 O와 글자 O
        for k in 'ABCD': e.kill_seg(p['O'], p[k])
        e.kill_sector(p['P'], p['A'], p['B'], 55).kill_sector(p['Q'], p['C'], p['D'], 55).kill_disk(p['O'], 42)
    elif name == 'd3_2':
        c, r = circum(p['A'], p['B'], p['C'])
        e.keep_circle(c, r)
        for a, b in [('A', 'B'), ('B', 'C'), ('C', 'D'), ('D', 'A')]: e.keep_seg(p[a], p[b])
        e.keep_pt(p['O'], 5).keep_box(198, 158, 226, 186)
        e.kill_seg(p['O'], p['B']).kill_seg(p['O'], p['D'])
        e.kill_box(155, 155, 180, 185).kill_box(192, 222, 222, 252)   # 글자 y, x
        e.kill_disk(p['O'], 38)
    elif name == 'd3_7':
        c, r = circum(p['A'], p['B'], p['C'])
        for a, b in [('A', 'B'), ('B', 'C'), ('C', 'D'), ('D', 'A')]: e.keep_seg(p[a], p[b])
        e.kill_circle(c, r, 3.6).kill_seg(p['A'], p['E']).kill_seg(p['E'], p['C'])
        e.kill_box(140, 5, 180, 45).kill_disk(p['E'], 42).kill_sector(p['D'], p['A'], p['C'], 38)  # 글자 E, 각 표시
        e.kill_box(int(c[0])-16, int(c[1])-16, int(c[0])+16, int(c[1])+48)  # 점 O와 글자 O
    elif name in ('d4_6', 'd4_7'):
        c = ((p['A'][0]+p['D'][0])/2, (p['A'][1]+p['D'][1])/2); r = abs(p['A'][1]-p['D'][1])/2
        e.keep_circle(c, r).keep_seg((0, p['A'][1]), (390, p['A'][1]))
        for a, b in [('A', 'B'), ('B', 'C'), ('C', 'A')]: e.keep_seg(p[a], p[b])
        e.keep_pt(c, 6).keep_box(c[0]+6, c[1]-22, c[0]+34, c[1]+16)    # 점 O와 글자 O
        e.kill_seg(p['A'], p['D'], 4).kill_seg(p['C'], p['D'], 4)
        e.kill_box(p['D'][0]-18, 5, p['D'][0]+18, p['D'][1]-3)         # 글자 D
        (e.kill_sector(p['C'], p['D'], p['A'], 38) if name == 'd4_6' else e.kill_sector(p['C'], p['B'], p['A'], 38))
        (e.kill_sector(p['A'], p['D'], (390, p['A'][1]), 46) if name == 'd4_6' else e.kill_sector(p['A'], p['B'], (390, p['A'][1]), 46))
        e.trim_circle(p['D'], 7, c, r)
    elif name == 'd3_6':
        A, B, C, D = (108.6, 56.5), (68, 266), (272.8, 266.0), (266, 80)
        e.keep_circle(*circum(A, B, C))
        e.kill_sector(A, B, D, 36).kill_sector(C, D, (400, 266), 36)
        for a, b in [((108.6, 56.5), (68, 266)), ((108.6, 56.5), (266, 80)), ((266, 80), (272.8, 266.0)), ((0, 266), (400, 266))]: e.keep_seg(a, b)
    elif name == 'd4_5':
        A, B, C = (194.8, 347.3), (194.6, 51.9), (49.5, 228.1)
        e.keep_circle(((A[0]+B[0])/2, (A[1]+B[1])/2), (A[1]-B[1])/2).keep_seg((0, A[1]), (390, A[1]))
        for a, b in [(A, B), (B, C), (C, A)]: e.keep_seg(a, b)
        e.kill_sector(C, B, A, 30).kill_sector(A, B, (390, A[1]), 32)
    return e.result()
