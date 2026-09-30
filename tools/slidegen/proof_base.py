"""증명 슬라이드용 '처음 주어진 그림' 만들기: 교과서 그림에서 보조선·각 표시(결과)를 지운다.
keep(남길 선/원/점 근처)은 건드리지 않고, erase 영역의 잉크와 모든 색 잉크를 지운다."""
import numpy as np
from PIL import Image


class Eraser:
    def __init__(self, im):
        self.a = np.asarray(im.convert('RGB')).astype(float)
        h, w, _ = self.a.shape
        self.Y, self.X = np.mgrid[0:h, 0:w].astype(float)
        self.keep = np.zeros((h, w), bool)
        self.kill = np.zeros((h, w), bool)
        self.trims = []

    def _seg(self, a, b):
        ax, ay = a; bx, by = b; dx, dy = bx-ax, by-ay; L = dx*dx+dy*dy or 1
        t = np.clip(((self.X-ax)*dx + (self.Y-ay)*dy)/L, 0, 1)
        return np.hypot(self.X-(ax+t*dx), self.Y-(ay+t*dy))

    def _circ(self, c, r):
        return np.abs(np.hypot(self.X-c[0], self.Y-c[1]) - r)

    # 남길 것
    def keep_seg(self, a, b, w=2.6): self.keep |= self._seg(a, b) < w; return self
    def keep_circle(self, c, r, w=2.6): self.keep |= self._circ(c, r) < w; return self
    def keep_pt(self, p, r=6): self.keep |= np.hypot(self.X-p[0], self.Y-p[1]) < r; return self
    def keep_box(self, x0, y0, x1, y1): self.keep |= (self.X >= x0) & (self.X <= x1) & (self.Y >= y0) & (self.Y <= y1); return self

    # 지울 것
    def kill_seg(self, a, b, w=3.2): self.kill |= self._seg(a, b) < w; return self
    def kill_circle(self, c, r, w=3.2): self.kill |= self._circ(c, r) < w; return self
    def kill_pt(self, p, r=6): self.kill |= np.hypot(self.X-p[0], self.Y-p[1]) < r; return self
    def kill_box(self, x0, y0, x1, y1): self.kill |= (self.X >= x0) & (self.X <= x1) & (self.Y >= y0) & (self.Y <= y1); return self

    def kill_disk(self, p, r):
        '''각 표시(색·검정 모두)가 있는 꼭짓점 주변: 남길 선 밖은 모두 지움'''
        self.kill |= np.hypot(self.X-p[0], self.Y-p[1]) < r; return self

    def kill_sector(self, v, p1, p2, r):
        '''꼭짓점 v에서 두 반직선 v→p1, v→p2 사이(작은 쪽) 부채꼴 안: 각 표시 지우기 (바깥의 글자는 보존)'''
        a1 = np.arctan2(p1[1]-v[1], p1[0]-v[0]); a2 = np.arctan2(p2[1]-v[1], p2[0]-v[0])
        d = (a2 - a1) % (2*np.pi)
        if d > np.pi: a1, d = a2, 2*np.pi - d
        t = (np.arctan2(self.Y-v[1], self.X-v[0]) - a1) % (2*np.pi)
        self.kill |= (np.hypot(self.X-v[0], self.Y-v[1]) < r) & (t <= d); return self

    def trim_circle(self, p, r, c, rad, w=1.6):
        '''원 위의 점(검은 점)을 지우고 원의 선 굵기만 남김'''
        self.trims.append((p, r, c, rad, w)); return self

    def result(self, color=True):
        a = self.a.copy()
        sat = a.max(2) - a.min(2)
        hue = (np.abs(a[..., 0]-a[..., 1]) > 14) | (np.abs(a[..., 2]-a[..., 0]) > 14)
        sat = np.where(hue, np.maximum(sat, 29), sat)
        m = self.kill & ~self.keep
        a[m] = 255
        if color:
            col = sat > 28
            a[col & ~self.keep] = 255
            # 남길 선 위에 겹친 색 → 무채색 잉크로
            ck = col & self.keep
            v = a[ck].min(1)
            v = np.where(v > 150, 255, v)
            a[ck] = np.stack([v, v, v], 1)
        for p, r, c, rad, w in self.trims:
            m = (np.hypot(self.X-p[0], self.Y-p[1]) < r) & (self._circ(c, rad) > w)
            a[m] = 255
        return Image.fromarray(a.clip(0, 255).astype(np.uint8))


def circum(a, b, c):
    ax, ay = a; bx, by = b; cx, cy = c
    d = 2*(ax*(by-cy) + bx*(cy-ay) + cx*(ay-by))
    ux = ((ax*ax+ay*ay)*(by-cy) + (bx*bx+by*by)*(cy-ay) + (cx*cx+cy*cy)*(ay-by))/d
    uy = ((ax*ax+ay*ay)*(cx-bx) + (bx*bx+by*by)*(ax-cx) + (cx*cx+cy*cy)*(bx-ax))/d
    return (ux, uy), float(np.hypot(ax-ux, ay-uy))
