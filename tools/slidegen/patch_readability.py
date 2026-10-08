"""가독성·수식 글꼴 패치 (HTML 직접 패치). 사용: python3 tools/slidegen/patch_readability.py 파일.html  (저장소 루트에서)
 1) 풀이 단계 글자 크기 키우고(40→44, 36→40px) 단계 간격은 원래대로 두고 위치를 다시 계산(크롬으로 높이 측정)
 2) 본문 속 변수 x, y를 수학 기울임체(Times 계열 italic)로 표시: <i class="mv">x</i>
 덱을 다시 만들면 이 패치도 다시 실행 (한 번 적용한 파일에 다시 돌려도 안전: 이미 적용되면 건너뜀)."""
import re, sys, json, subprocess, os, tempfile

CHROME = '/opt/pw-browsers/chromium-1194/chrome-linux/chrome'
BUMP = {40: 44, 36: 40, 32: 36}
CSS = ('<style id="mvcss">i.mv{font-family:"Times New Roman","STIX Two Text","Noto Serif KR",serif;font-style:italic;'
       'font-weight:400;font-size:1.14em;padding:0 .05em;letter-spacing:0}b i.mv,.bold i.mv{font-weight:700}section p[data-build-in]{word-break:keep-all}</style>')

def italicize(h):
    out = []; pos = 0
    for m in re.finditer(r'<section.*?</section>', h, flags=re.S):
        out.append(h[pos:m.start()]); pos = m.end()
        sec = m.group(0)
        if '<script' in sec:                       # 드래그 슬라이드는 그대로
            out.append(sec); continue
        parts = re.split(r'(<svg.*?</svg>|<[^>]+>)', sec, flags=re.S)
        for i, t in enumerate(parts):
            if i % 2 == 0:                          # 글자 부분만
                t = re.sub(r'(?<![A-Za-z가-힣])([xy])(?![A-Za-z가-힣])', r'<i class="mv">\1</i>', t)
                parts[i] = re.sub(r'(?<=\S) = (?=\S)', '&nbsp;=&nbsp;', t)       # '= 65'가 줄 끝에서 혼자 떨어지지 않게
        out.append(''.join(parts))
    out.append(h[pos:])
    return ''.join(out)

MEASURE = r'''
var res=[];
document.querySelectorAll('section').forEach(function(s,si){
 s.style.setProperty('display','block','important');s.style.visibility='hidden';
 var ps=[].filter.call(s.querySelectorAll('p[data-build-in]'),function(p){
   var f=parseInt(p.style.fontSize);return (f==40||f==36||f==32)&&p.style.fontWeight!=='700'&&!p.style.background;});
 if(!ps.length)return;
 var tops=ps.map(function(p){return parseFloat(p.style.top);}),hs0=ps.map(function(p){return p.offsetHeight;});
 var gaps=[];for(var i=0;i<ps.length-1;i++)gaps.push(Math.max(30,tops[i+1]-(tops[i]+hs0[i])));
 var ans0=[].filter.call(s.querySelectorAll('p[data-build-in]'),function(p){return p.style.background;})[0];
 var lim=ans0?Math.max(parseFloat(ans0.style.top),940)-24:1040;
 var r,bot,cands=[4,2,0,-2];
 for(var c=0;c<cands.length;c++){
  var d=cands[c],y=tops[0];r=[];bot=0;function f(k){return parseInt(k)+d;}
  ps.forEach(function(p,i){p.style.fontSize=(i<ps.length&&p.dataset.f0?p.dataset.f0:(p.dataset.f0=parseInt(p.style.fontSize)))+'px';});
  ps.forEach(function(p,i){p.style.fontSize=f(p.dataset.f0)+'px';});
  ps.forEach(function(p,i){r.push([Math.round(y),f(p.dataset.f0)]);bot=y+p.offsetHeight;y=bot+(i<gaps.length?gaps[i]:0);});
  if(bot<=lim)break;
 }
 var ans=[].filter.call(s.querySelectorAll('p[data-build-in]'),function(p){return p.style.background;})[0],at=null;
 if(ans){at=parseFloat(ans.style.top);if(bot+24>at)at=Math.min(bot+24,940);}
 res.push([si,r,Math.round(bot),at]);
});
document.title='RES'+JSON.stringify(res);
'''

def layout(h):
    tmp = tempfile.mkdtemp(); f = os.path.join(tmp, 't.html')
    open(f, 'w', encoding='utf-8').write(h.replace('</body>', '<script>window.addEventListener("load",function(){' + MEASURE + '});</script></body>'))
    out = subprocess.run([CHROME, '--headless', '--no-sandbox', '--disable-gpu', '--virtual-time-budget=4000', '--dump-dom', 'file://' + f],
                         capture_output=True, text=True).stdout
    m = re.search(r'<title>RES(.*?)</title>', out, flags=re.S)
    import html as H
    return json.loads(H.unescape(m.group(1)))

def apply_layout(h, res):
    secs = list(re.finditer(r'<section.*?</section>', h, flags=re.S)); new = []; pos = 0; warn = []
    d = {x[0]: (x[1], x[2], x[3]) for x in res}
    for si, m in enumerate(secs):
        new.append(h[pos:m.start()]); pos = m.end(); sec = m.group(0)
        if si in d:
            r, ybot, atop = d[si]; k = [0]
            def rep(pm):
                st = pm.group(0)
                if 'data-build-in' not in st: return st
                mm = re.search(r'font-size:(\d+)px', st)
                if not mm or int(mm.group(1)) not in BUMP or 'font-weight:700' in st or 'background' in st: return st
                top, fs = r[k[0]]; k[0] += 1
                st = re.sub(r'top:[\d.]+px', f'top:{top}px', st, 1)
                return re.sub(r'font-size:\d+px', f'font-size:{fs}px', st, 1)
            sec = re.sub(r'<p [^>]*>', rep, sec)
            if atop is not None:
                sec = re.sub(r'(<p [^>]*?)top:[\d.]+px((?:(?!</p>).)*?font-weight:700; background)', lambda mm: f'{mm.group(1)}top:{round(atop)}px{mm.group(2)}', sec, 1, flags=re.S)
            if ybot > 1040: warn.append((si + 1, ybot))
        new.append(sec)
    new.append(h[pos:])
    return ''.join(new), warn

if __name__ == '__main__':
    p = sys.argv[1]; h = open(p, encoding='utf-8').read()
    if 'id="mvcss"' in h: print('already patched'); sys.exit()
    h = italicize(h)
    h = h.replace('left:1230px; top:', 'left:1215px; top:').replace('width:600px; font-size:32px', 'width:625px; font-size:32px')  # 활동 2 풀이 글
    h = h.replace('font-size:30px; line-height:1.5; color:#4A5568','font-size:36px; line-height:1.5; color:#4A5568')  # 드래그 슬라이드 안내 글
    res = layout(h)
    h, warn = apply_layout(h, res)
    h = h.replace('</head>', CSS + '</head>', 1)
    open(p, 'w', encoding='utf-8').write(h)
    print('patched', len(res), 'slides; overflow warnings:', warn)
