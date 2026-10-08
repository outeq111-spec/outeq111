"""각 슬라이드 오른쪽 위에 '교과서 N쪽' 표시를 넣는다 (HTML 직접 패치, 여러 번 돌려도 같은 결과).
사용: python3 tools/slidegen/page_labels.py   (저장소 루트에서)  -- 덱을 다시 만들었다면 그 뒤에 다시 실행.
값: 슬라이드 번호(1부터) -> '교과서 쪽수' 문자열. 표지 등 표시 안 할 장은 생략."""
import re, sys

def rng(a, b, label): return {i: label for i in range(a, b + 1)}

R175 = '중2 복습'   # 2학년 교과서 175쪽 그림: 3학년 교과서 쪽수가 아니므로 쪽수 없이 표시
MAP = {
 '187-189_원과직선_중단원마무리_풀이.html': {**rng(2, 8, '187쪽'), **rng(9, 16, '188쪽'), **rng(17, 24, '189쪽')},
 '190-194_원주각_1차시_원주각과중심각.html': {**rng(2, 5, '190쪽'), **rng(6, 9, '191쪽'), **rng(10, 13, '192쪽'), 14: '192~193쪽',
                                      **rng(15, 21, '193쪽'), **rng(22, 28, '194쪽')},
 '195-197_원주각_2차시_원주각과호의길이.html': {2: '193쪽 복습', **rng(3, 9, '195쪽'), **rng(10, 16, '196쪽'), **rng(17, 19, '197쪽')},
 '198-199_원주각의활용_1차시_원에내접하는사각형.html': {**rng(2, 4, '198쪽'), **rng(5, 13, '199쪽')},
 '200-203_원주각의활용_2차시_접선과현이이루는각.html': {**rng(2, 6, '200쪽'), **rng(7, 9, '201쪽'), **rng(10, 16, '202쪽'),
                                          17: '203쪽', 18: '203쪽', 19: R175, 20: '203쪽', 21: '203쪽'},
 '204-206_원주각_중단원마무리_풀이.html': {**rng(2, 6, '204쪽'), **rng(7, 10, '205쪽'), 11: R175,
                                 **rng(12, 17, '205쪽'), **rng(18, 21, '206쪽'), 22: R175, **rng(23, 27, '206쪽')},
 '207-209_원의성질_대단원마무리_풀이.html': {**rng(2, 9, '207쪽'), 10: R175, **rng(11, 14, '207쪽'), **rng(15, 20, '208쪽'), 21: R175,
                                  **rng(22, 27, '208쪽'), **rng(28, 36, '209쪽')},
}
TAG = '<p class="pgno" '
STYLE = ('position:absolute; right:96px; top:40px; font-size:28px; font-weight:700; color:#4A5568; '
         'background:rgba(31,122,140,0.12); padding:4px 18px; border-radius:20px; white-space:nowrap')

def patch(path, labels):
    s = open(path, encoding='utf-8').read()
    s = re.sub(r'<p class="pgno" [^>]*>[^<]*</p>', '', s)            # 기존 표시 제거
    out, pos, k = [], 0, 0
    for m in re.finditer(r'<section[^>]*>', s):
        k += 1
        out.append(s[pos:m.end()]); pos = m.end()
        if k in labels:
            out.append(f'{TAG}style="{STYLE}">{labels[k] if labels[k].startswith("중2") else "교과서 " + labels[k]}</p>')
    out.append(s[pos:])
    open(path, 'w', encoding='utf-8').write(''.join(out))
    return k

if __name__ == '__main__':
    for f, lab in MAP.items():
        n = patch(f, lab)
        assert max(lab) <= n, (f, n, max(lab))
        print(f, n, '장 중', len(lab), '장에 표시')
