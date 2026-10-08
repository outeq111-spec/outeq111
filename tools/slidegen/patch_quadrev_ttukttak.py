"""원주각의 활용 2차시: '활동 1 · 뚝딱이' 앞에 사각형 관계 복습 슬라이드(중단원 마무리의 quadrev와 같은 것)를 넣는다."""
import sys
F = sys.argv[1] if len(sys.argv) > 1 else '원주각의활용_2차시_접선과현이이루는각.html'
src = open('원주각_중단원마무리_풀이.html', encoding='utf-8').read()
i = src.index('복습 · 여러 가지 사각형'); a = src.rfind('<section', 0, i); b = src.index('</section>', i) + 10
q = src[a:b]
t0 = q.index('font-size:40px; font-weight:700">') + len('font-size:40px; font-weight:700">'); t1 = q.index('</p>', t0)
q = q[:t0] + '마름모 중에 원에 내접하는 것이 있을까? 정사각형까지 따라가 보자.' + q[t1:]
s = open(F, encoding='utf-8').read()
if '정사각형까지 따라가 보자' not in s:
    i = s.index('활동 1 · 뚝딱이'); a = s.rfind('<section', 0, i)
    s = s[:a] + q + s[a:]
    open(F, 'w', encoding='utf-8').write(s)
print('ok')
