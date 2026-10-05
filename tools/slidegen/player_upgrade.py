"""슬라이드 플레이어 개선(포인터·확대·가독성)을 shell.html과 저장소 루트의 모든 덱 HTML에 넣는다.
python3 player_upgrade.py   (이미 들어간 파일은 새 버전으로 교체)

- 포인터: 큰 빨간 화살표 + 노란 후광(기본) / 레이저 점 / 보통 마우스.  P 키 또는 왼쪽 아래 [포인터] 버튼으로 바꿈
- 확대: 마우스 휠(또는 Z 키)로 마우스가 있는 곳을 확대, Esc·슬라이드 넘기면 원래대로
- 가독성: 방금 나온 풀이 단계에 노란 형광 표시, 교과서 그림 대비 살짝 올림, 회색 글씨 진하게
"""
import os, re, glob

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, '..', '..')

ARROW = ("<svg xmlns='http://www.w3.org/2000/svg' width='64' height='64' viewBox='0 0 64 64'>"
         "<path d='M6 4 L6 52 L18 41 L27 60 L36 56 L27 37 L44 37 Z' fill='%23E4572E' stroke='white' stroke-width='4' stroke-linejoin='round'/></svg>")
CUR = 'url("data:image/svg+xml;utf8,' + ARROW.replace('"', "'").replace('<', '%3C').replace('>', '%3E') + '") 6 4, auto'

CSS = """<style id="ptrkit">
#stage{overflow:hidden}
#stage>section{transition:transform .25s ease}
body.pm-big, body.pm-big *{cursor:%(cur)s !important}
body.pm-laser, body.pm-laser *{cursor:none !important}
#halo{position:fixed; left:0; top:0; width:120px; height:120px; margin:-60px 0 0 -60px; border-radius:50%%; pointer-events:none; z-index:50;
 background:radial-gradient(circle, rgba(255,214,0,.42) 0%%, rgba(255,214,0,.28) 55%%, rgba(255,214,0,0) 72%%); display:none}
body.pm-big #halo.on{display:block}
body.pm-laser #halo.on{display:block; width:34px; height:34px; margin:-17px 0 0 -17px; background:radial-gradient(circle, #FF2A2A 0%%, #FF2A2A 38%%, rgba(255,42,42,.45) 55%%, rgba(255,42,42,0) 75%%)}
#ptr{position:fixed; left:110px; bottom:8px; font:14px sans-serif; background:#333; color:#ddd; border:0; border-radius:6px; padding:6px 10px; opacity:.6; z-index:60}
#fs{z-index:60}
#toast{position:fixed; left:50%%; top:24px; transform:translateX(-50%%); background:rgba(20,20,20,.85); color:#fff; font:600 22px 'Noto Sans KR',sans-serif;
 padding:10px 22px; border-radius:10px; z-index:70; opacity:0; transition:opacity .3s; pointer-events:none}
#toast.show{opacity:1}
/* 가독성 */
section img{filter:contrast(1.12)}
section p.cur{background:#FFF1A8 !important; box-shadow:0 0 0 12px #FFF1A8; border-radius:6px}
[style*="color:#4A5568"]{color:#2D3748 !important}
[style*="color:#6B7280"]{color:#4B5563 !important}
</style>""" % {'cur': CUR}

JS = """<script id="ptrkitjs">
(function(){
 var MODES=['big','laser','plain'], NAMES={big:'큰 화살표 + 노란 원',laser:'레이저 점',plain:'보통 마우스'}, m=0;
 try{m=Math.max(0,MODES.indexOf(localStorage.getItem('pm')||'big'))}catch(e){}
 var halo=document.createElement('div');halo.id='halo';document.body.appendChild(halo);
 var toast=document.createElement('div');toast.id='toast';document.body.appendChild(toast);
 var btn=document.createElement('button');btn.id='ptr';btn.textContent='포인터';document.body.appendChild(btn);
 var tt;function say(s){toast.textContent=s;toast.classList.add('show');clearTimeout(tt);tt=setTimeout(function(){toast.classList.remove('show')},1400);}
 function setMode(k,quiet){m=k;MODES.forEach(function(x){document.body.classList.toggle('pm-'+x,x===MODES[m])});
   try{localStorage.setItem('pm',MODES[m])}catch(e){} if(!quiet)say('포인터: '+NAMES[MODES[m]]+'  (P 키로 바꾸기)');}
 setMode(m,true);
 btn.onclick=function(e){e.stopPropagation();setMode((m+1)%3);};
 var mx=-999,my=-999;
 addEventListener('pointermove',function(e){if(e.pointerType==='touch'){halo.classList.remove('on');return;}
   mx=e.clientX;my=e.clientY;halo.style.transform='translate('+mx+'px,'+my+'px)';halo.classList.add('on');});
 document.addEventListener('mouseleave',function(){halo.classList.remove('on')});
 // 확대
 var z=1,cur=null,st=document.getElementById('stage');
 function slideXY(){var r=st.getBoundingClientRect();return [(mx-r.left)/r.width*1920,(my-r.top)/r.height*1080];}
 function apply(){var s=S[i];if(cur&&cur!==s){cur.style.transform='';}cur=s;
   if(z<=1.001){z=1;s.style.transform='';return;}s.style.transform='scale('+z+')';}
 function zoomTo(nz){var s=S[i];if(z<=1.001&&nz>1){var p=slideXY();s.style.transformOrigin=p[0]+'px '+p[1]+'px';}z=Math.min(4,Math.max(1,nz));apply();}
 addEventListener('wheel',function(e){if(e.ctrlKey)return;e.preventDefault();zoomTo(e.deltaY<0?z*1.25:z/1.25);},{passive:false});
 addEventListener('keydown',function(e){if(/INPUT|TEXTAREA/.test(e.target.tagName))return;var k=e.key.toLowerCase();
   if(k==='p'){setMode((m+1)%3);}else if(k==='z'){zoomTo(z>1?1:2);}else if(e.key==='Escape'&&z>1){zoomTo(1);}},true);
 // 방금 나온 단계 강조 + 슬라이드 바뀌면 확대 해제
 var show0=show;
 show=function(){show0();if(cur&&cur!==S[i]){cur.style.transform='';z=1;}
   document.querySelectorAll('section p.cur').forEach(function(e){e.classList.remove('cur')});
   var g=G[i][step-1];if(g&&step>0)g.forEach(function(e){if(e.tagName==='P'&&!/background/.test(e.getAttribute('style')||''))e.classList.add('cur')});};
 show();
})();
</script>"""


def upgrade(path):
    h = open(path).read()
    h = re.sub(r'<style id="ptrkit">.*?</style>', '', h, flags=re.S)
    h = re.sub(r'<script id="ptrkitjs">.*?</script>', '', h, flags=re.S)
    assert '</style></head>' in h and h.rstrip().endswith('</script></body></html>'), path
    h = h.replace('</style></head>', '</style>' + CSS + '</head>', 1)
    h = h.rstrip()[:-len('</body></html>')] + JS + '</body></html>'
    open(path, 'w').write(h)


if __name__ == '__main__':
    files = [os.path.join(HERE, 'shell.html')] + sorted(glob.glob(os.path.join(ROOT, '*.html')))
    for f in files:
        upgrade(f); print('ok', os.path.basename(f))
