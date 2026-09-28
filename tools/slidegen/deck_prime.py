"""암호와 수: 소수(Prime Number)와 RSA 암호 — 학습지 보조 슬라이드 (중1, 교과서 그림 없음).
python3 deck_prime.py  →  저장소 루트에 HTML 생성"""
import os, re, html as H

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, '..', '..', '암호와수_소수와RSA암호.html')
R, BL, G, OR, PU = '#E4572E', '#1F6FB2', '#2E9E5B', '#D9822B', '#8E44AD'
COLORS = {'r': R, 'b': BL, 'g': G, 'o': '#B5651D', 'p': PU}
BG1, BG2, DARK, TEAL, PILL = '#F7F6F1', '#EEF4F4', '#1E2A3A', '#1F7A8C', '#FCE0C4'
FONT = "'Noto Sans KR','Apple SD Gothic Neo','Malgun Gothic','Nanum Gothic',sans-serif"
MONO = "Consolas,'D2Coding',monospace"


def rich(s):
    s = H.escape(s)
    s = re.sub(r'\[(\w)\](.*?)\[/\1\]', lambda m: f'<b style="color:{COLORS[m.group(1)]}">{m.group(2)}</b>', s)
    return s.replace('\n', '<br>')


def sec(inner, label='', title='', bg=BG1, notes=''):
    h = ''
    if label:
        h += f'<p style="position:absolute; left:96px; top:44px; font-size:30px; font-weight:700; color:{TEAL}">{H.escape(label)}</p>'
    if title:
        h += f'<p style="position:absolute; left:96px; top:90px; width:1728px; font-size:46px; font-weight:700; line-height:1.3">{rich(title)}</p>'
    a = f'<aside>{H.escape(notes)}</aside>' if notes else ''
    return (f'<section style="background:{bg}; color:{DARK}; font-family:{FONT}; padding:96px; display:flex; flex-direction:column">'
            f'{h}{inner}{a}</section>')


def B(n, kind='rise'):
    return f'data-build-in="{kind} {n}"'


def box(x, y, w, inner, n=None, bg='#FFFFFF', size=38, extra=''):
    b = B(n) if n else ''
    return (f'<div {b} style="position:absolute; left:{x}px; top:{y}px; width:{w}px; background:{bg}; border-radius:16px; '
            f'padding:24px 32px; font-size:{size}px; line-height:1.45; {extra}">{inner}</div>')


S = []

# 1. 표지 ----------------------------------------------------------------
S.append(f'<section style="background:{DARK}; color:#F7F6F1; font-family:{FONT}; padding:128px; display:flex; flex-direction:column">'
         '<div style="display:flex; flex-direction:column; justify-content:center; gap:32px; height:100%">'
         '<p style="font-size:34px; font-weight:700; color:#7CC6D2">암호와 수 · 9월 29일</p>'
         '<h1 style="font-size:116px; font-weight:900; line-height:1.15">소수(Prime Number)와<br>RSA 암호</h1>'
         '<p style="font-size:38px; color:#BFD8D5">수학적 규칙은 어떻게 인류의 비밀을 지킬까?</p></div></section>')

# 2. 탐구 질문: 곱하기 vs 되돌리기 ------------------------------------------
inner = (
    box(96, 200, 820, f'<p style="font-size:34px; color:{TEAL}; font-weight:700">문제 ①</p>'
        f'<p style="font-size:84px; font-weight:700; font-family:{MONO}">7 × 13 = <span {B(1,"pop")} style="color:{BL}">91</span></p>'
        f'<p {B(1)} style="font-size:32px; color:#4A5568">곱하기는 금방! (10초면 충분)</p>')
    + box(1004, 200, 820, f'<p style="font-size:34px; color:{TEAL}; font-weight:700">문제 ②</p>'
          f'<p style="font-size:84px; font-weight:700; font-family:{MONO}">91 = ? × ?</p>'
          f'<p {B(3)} style="font-size:32px; color:#4A5568">2? 3? 5? … 하나씩 나눠 봐야 해요</p>', n=2)
    + box(96, 560, 1728, rich('[r]곱하기[/r]는 쉽지만, 곱해진 수를 [r]다시 소인수분해[/r]하는 것은 어렵다.\n'
                              '→ 수가 수백 자리가 되면 [b]컴퓨터로도 매우 오래[/b] 걸린다. 이것이 암호의 비밀!'),
          n=4, bg=PILL, size=42)
    + box(96, 820, 1728, rich('[g]탐구 질문[/g]  수학적 규칙(소수와 소인수분해)은 어떻게 현대 인류의 비밀을 가장 안전하게 보호하는가?'),
          n=5, size=36, bg='#DDEFE3'))
S.append(sec(inner, '탐구 질문', '곱하기와 되돌리기, 어느 쪽이 더 쉬울까?', BG2,
             '학생들에게 먼저 7×13을 계산시키고, 다음에 91을 두 수의 곱으로 나타내게 해 시간 차이를 느끼게 한다.'))

# 3. 소수와 합성수 ------------------------------------------------------------
rows = ''
for n in range(1, 11):
    ds = [d for d in range(1, n+1) if n % d == 0]
    kind = '소수' if len(ds) == 2 else ('합성수' if len(ds) > 2 else '둘 다 아님')
    col = R if kind == '소수' else (BL if kind == '합성수' else '#6B7280')
    rows += (f'<tr><td style="font-weight:700">{n}</td><td>{", ".join(map(str, ds))}</td><td>{len(ds)}</td>'
             f'<td {B(2)} style="color:{col}; font-weight:700">{kind}</td></tr>')
table = (f'<table id="t3" {B(1)} style="position:absolute; left:96px; top:200px; width:940px; border-collapse:collapse; font-size:32px; text-align:center; background:#FFF; border-radius:16px">'
         '<tr style="background:#DCEBEE"><th style="padding:6px">수</th><th>약수</th><th>약수 개수</th><th>분류</th></tr>'
         f'{rows}</table>'
         '<style>#t3 td{padding:9px 8px;border-top:1px solid #E5E7EB}</style>')
inner = (table
         + box(1090, 200, 734, rich('[r]소수[/r]\n1보다 큰 자연수 중에서\n1과 자기 자신만을 약수로 가지는 수\n= 약수가 [r]딱 2개[/r]'), n=3, size=38)
         + box(1090, 520, 734, rich('[b]합성수[/b]\n1보다 큰 자연수 중에서 소수가 아닌 수\n= 약수가 [b]3개 이상[/b]'), n=4, size=38)
         + box(1090, 780, 734, rich('[o]1[/o]은 약수가 1개뿐!\n→ 소수도 합성수도 [o]아니다[/o]'), n=5, size=38, bg=PILL))
S.append(sec(inner, '개념 정리', '소수와 합성수', BG1))

# 4. 활동 1: 에라토스테네스의 체 (인터랙티브) ----------------------------------
cells = ''.join(f'<div class="sv" data-n="{n}">{n}</div>' for n in range(1, 51))
steps = [('1 지우기', 1), ('2의 배수', 2), ('3의 배수', 3), ('5의 배수', 5), ('7의 배수', 7), ('소수 ○', 0)]
btns = ''.join(f'<button class="svb" data-k="{i}">{i+1}. {t}</button>' for i, (t, _) in enumerate(steps))
inner = f'''
<style>
#sieve{{position:absolute; left:96px; top:190px; width:1100px; display:grid; grid-template-columns:repeat(10,1fr); gap:8px}}
#sieve .sv{{height:150px; background:#FFF; border-radius:12px; display:flex; align-items:center; justify-content:center; font-size:52px; font-weight:700; font-family:Arial,sans-serif; position:relative; cursor:pointer; user-select:none; transition:background .3s,color .3s}}
#sieve .sv.x{{color:#B8BEC7; background:#EEF0F2}}
#sieve .sv.x::after{{content:""; position:absolute; left:18%; right:18%; top:50%; height:5px; background:var(--c,#999); transform:rotate(-30deg); border-radius:3px}}
#sieve .sv.p{{color:{R}}}
#sieve .sv.p::before{{content:""; position:absolute; width:96px; height:96px; border:6px solid {R}; border-radius:50%}}
#sieve .sv.hit{{background:#FFF3C4}}
#svPanel{{position:absolute; left:1240px; top:190px; width:584px; display:flex; flex-direction:column; gap:14px}}
.svb{{font:700 32px {FONT}; padding:14px 20px; border:0; border-radius:12px; background:#DCEBEE; color:{DARK}; text-align:left; cursor:pointer}}
.svb.done{{background:{TEAL}; color:#FFF}}
#svMsg{{font-size:32px; line-height:1.45; background:{PILL}; padding:18px 24px; border-radius:14px; min-height:170px}}
</style>
<div id="sieve" class="ix">{cells}</div>
<div id="svPanel" class="ix">{btns}
<div id="svMsg">버튼을 차례로 눌러 보세요.<br>(숫자를 직접 눌러 지울 수도 있어요)</div>
<button class="svb" id="svReset" style="background:#E5E7EB; font-size:26px">처음부터</button></div>
<script>
(function(){{
 var C=['#6B7280','{BL}','{G}','{PU}','{OR}'], P=[1,2,3,5,7];
 var M=['1은 약수가 1개 → 소수가 아니므로 지워요.',
  '2는 남기고, 2의 배수(4, 6, 8, …)를 모두 지워요.',
  '3은 남기고, 3의 배수 중 남은 것(9, 15, 21, …)을 지워요.',
  '4는 이미 지워졌어요! 5는 남기고 5의 배수(25, 35)를 지워요.',
  '7은 남기고 7의 배수(49)를 지워요.<br>11×11=121 &gt; 50 이라 여기서 끝!',
  '남은 수가 모두 소수!<br>1~50의 소수는 <b style="color:{R}">15개</b>예요.'];
 var el=[].slice.call(document.querySelectorAll('#sieve .sv'));
 function cell(n){{return el[n-1];}}
 function run(k){{
  el.forEach(function(e){{e.classList.remove('hit');}});
  if(k<5){{var p=P[k];
    if(p===1){{cell(1).classList.add('x');cell(1).style.setProperty('--c',C[0]);}}
    else for(var m=2*p;m<=50;m+=p){{var e=cell(m);if(!e.classList.contains('x')){{e.classList.add('x','hit');e.style.setProperty('--c',C[k]);}}}}
  }} else el.forEach(function(e){{if(!e.classList.contains('x'))e.classList.add('p');}});
  document.querySelectorAll('.svb[data-k]')[k].classList.add('done');
  document.getElementById('svMsg').innerHTML=M[k];
 }}
 document.querySelectorAll('.svb[data-k]').forEach(function(b){{b.onclick=function(){{var k=+b.dataset.k;for(var j=0;j<=k;j++)if(!document.querySelectorAll('.svb[data-k]')[j].classList.contains('done'))run(j);}};}});
 el.forEach(function(e){{e.onclick=function(){{if(e.classList.contains('p'))return;e.classList.toggle('x');e.style.setProperty('--c','#6B7280');}};}});
 document.getElementById('svReset').onclick=function(){{el.forEach(function(e){{e.className='sv';}});document.querySelectorAll('.svb').forEach(function(b){{b.classList.remove('done');}});document.getElementById('svMsg').innerHTML='버튼을 차례로 눌러 보세요.<br>(숫자를 직접 눌러 지울 수도 있어요)';}};
 document.querySelectorAll('.ix').forEach(function(x){{x.addEventListener('click',function(e){{e.stopPropagation();}});}});
}})();
</script>'''
S.append(sec(inner, '활동 1 · 소수 찾기 게임', '에라토스테네스의 체로 1~50의 소수 찾기', BG1,
             '숫자판·버튼을 누르면 슬라이드가 넘어가지 않습니다. 다음 슬라이드는 → 키나 화면 왼쪽/오른쪽 여백 클릭.'))

# 5. 활동 1 정리 + Q1, Q2 -------------------------------------------------------
primes = [p for p in range(2, 51) if all(p % d for d in range(2, p))]
chips = ''.join(f'<span style="display:inline-block; width:92px; margin:6px; padding:8px 0; text-align:center; border:5px solid {R}; border-radius:50px; color:{R}; font-weight:700">{p}</span>' for p in primes)
inner = (box(96, 200, 1728, f'<p style="font-size:32px; font-weight:700; color:{TEAL}">1~50의 소수 (15개)</p><div style="font-size:40px; font-family:Arial">{chips}</div>', n=1)
         + box(96, 470, 850, rich('[g]Q1[/g] 소수 2개 고르기 (예시)\n첫 번째 소수 p = [b]7[/b]\n두 번째 소수 q = [b]13[/b]'), n=2, size=40)
         + box(974, 470, 850, rich('[g]Q2[/g] 두 소수의 곱\nN = p × q = 7 × 13 = [r]91[/r]'), n=3, size=40)
         + box(96, 760, 1728, rich('[o]선생님 생각[/o]  91을 받은 친구는 2, 3, 5, 7로 차례로 나눠 보면 금방 7 × 13을 찾아요.\n'
                                   '→ 작은 소수로 만든 N은 [r]쉽게 들킨다![/r]  그래서 실제 암호는 [r]아주 큰 소수[/r]를 써요.'),
               n=4, bg=PILL, size=38))
S.append(sec(inner, '활동 1 · 정리', '찾은 소수로 N 만들기', BG2))

# 6. 활동 2: 143 소인수분해 --------------------------------------------------
tries = [('2', '끝자리가 3 (홀수)', False), ('3', '각 자리 합 1+4+3 = 8, 3의 배수 아님', False),
         ('5', '끝자리가 0이나 5가 아님', False), ('7', '143 = 7 × 20 + 3, 나머지 3', False),
         ('11', '143 ÷ 11 = 13 !', True)]
trs = ''.join(f'<p {B(i+2)} style="font-size:38px; margin-bottom:14px">'
              f'<b style="display:inline-block; width:150px; font-family:{MONO}">÷ {d}</b>'
              f'<span style="color:{G if ok else R}; font-weight:700">{"○" if ok else "✕"}</span>  {H.escape(t)}</p>'
              for i, (d, t, ok) in enumerate(tries))
inner = (box(96, 200, 700, f'<p style="font-size:32px; font-weight:700; color:{TEAL}">곱하기 (정방향)</p>'
             f'<p style="font-size:76px; font-weight:700; font-family:{MONO}">11 × 13<br>= <span style="color:{BL}">143</span></p>'
             f'<p style="font-size:32px; color:#4A5568">계산 한 번이면 끝!</p>', n=1)
         + box(850, 200, 974, f'<p style="font-size:32px; font-weight:700; color:{TEAL}">소인수분해 (거꾸로) : 143 = ? × ?</p>'
               f'<p style="font-size:30px; color:#4A5568; margin-bottom:14px">작은 소수부터 하나씩 나눠 본다</p>{trs}')
         + box(96, 820, 1728, rich('거꾸로 가려면 [r]여러 번 시도[/r]해야 한다. 수가 커질수록 시도할 소수가 [r]엄청나게 많아진다.[/r]'),
               n=7, bg=PILL, size=40))
S.append(sec(inner, '활동 2 · AI 탐구', '11 × 13 = 143, 그런데 143을 거꾸로 분해하면?', BG1,
             '학습지 질문 예시(11×13=143)를 그대로 따라간다. 3의 배수 판정(자리 합)은 1학년에게 짚어 주기.'))

# 7. 체험: 곱하기 기계 vs 분해 기계 (인터랙티브) -------------------------------
inner = f'''
<style>
.mc{{position:absolute; top:190px; width:840px; height:800px; background:#FFF; border-radius:18px; padding:32px 36px; box-sizing:border-box}}
.mc h3{{font-size:40px; color:{TEAL}; margin-bottom:20px}}
.mc input{{font:700 44px {MONO}; width:300px; padding:8px 14px; border:3px solid #CBD5E1; border-radius:10px}}
.mc button{{font:700 34px {FONT}; padding:12px 26px; border:0; border-radius:12px; background:{TEAL}; color:#FFF; cursor:pointer; margin-top:18px}}
.mc .out{{font-size:40px; margin-top:24px; line-height:1.5; word-break:break-all}}
.mc .ex{{font:28px {FONT}; color:#4A5568; margin-top:14px}}
.mc .ex span{{display:inline-block; background:#EEF4F4; border-radius:8px; padding:4px 12px; margin:4px; cursor:pointer; font-family:{MONO}}}
</style>
<div class="mc ix" style="left:96px">
 <h3>① 곱하기 기계</h3>
 <p style="font-size:38px">p = <input id="mp" value="11"></p>
 <p style="font-size:38px; margin-top:14px">q = <input id="mq" value="13"></p>
 <button id="mgo">곱하기</button>
 <div class="out" id="mout"></div>
 <div class="ex">예시 소수 누르기:<br><span data-p="101,103">101, 103</span><span data-p="1009,1013">1009, 1013</span><span data-p="100003,100019">100003, 100019</span><span data-p="1000003,1000033">1000003, 1000033</span></div>
</div>
<div class="mc ix" style="left:984px">
 <h3>② 소인수분해 기계</h3>
 <p style="font-size:38px">N = <input id="fn" value="143" style="width:520px"></p>
 <button id="fgo">분해하기</button>
 <div class="out" id="fout"></div>
 <p class="ex">2, 3, 5, 7, 11, … 차례로 나눠 보며 <b>나눠 본 횟수</b>를 셉니다.<br>
 ①에서 만든 N을 넣어 보세요. 자릿수가 늘면 횟수가 어떻게 될까요?</p>
</div>
<script>
(function(){{
 function isP(n){{if(n<2n)return false;for(var d=2n;d*d<=n;d++)if(n%d===0n)return false;return true;}}
 function big(s){{s=String(s).replace(/[^0-9]/g,'');return s?BigInt(s):0n;}}
 function mul(){{var p=big(mp.value),q=big(mq.value),o=document.getElementById('mout');
  var w=[];[p,q].forEach(function(x,i){{if(x<1000000000000n&&!isP(x))w.push((i?'q':'p')+'='+x+'는 소수가 아니에요!');}});
  o.innerHTML='N = '+p+' × '+q+'<br>= <b style="color:{BL}">'+(p*q)+'</b><br><span style="font-size:30px;color:#4A5568">('+String(p*q).length+'자리, 계산 1번)</span>'+(w.length?'<br><span style="font-size:30px;color:{R}">'+w.join('<br>')+'</span>':'');
  fn.value=String(p*q);}}
 function fac(){{var n=big(fn.value),o=document.getElementById('fout');
  if(n<2n){{o.innerHTML='2 이상의 수를 넣어 주세요.';return;}}
  if(n>=100000000000000n){{o.innerHTML='수가 너무 커요 (14자리까지).';return;}}
  var m=n,d=2n,c=0,f=[];
  while(d*d<=m){{c++;if(m%d===0n){{f.push(d);m/=d;}}else d+=(d===2n?1n:2n);}}
  if(m>1n)f.push(m);
  o.innerHTML='N = <b style="color:{R}">'+f.join(' × ')+'</b><br>나눠 본 횟수: <b style="color:{R}">'+c.toLocaleString()+'번</b>'+(f.length===1?'<br><span style="font-size:30px">(N은 소수예요)</span>':'');}}
 var mp=document.getElementById('mp'),mq=document.getElementById('mq'),fn=document.getElementById('fn');
 document.getElementById('mgo').onclick=mul;document.getElementById('fgo').onclick=fac;
 document.querySelectorAll('.mc .ex span').forEach(function(s){{s.onclick=function(){{var a=s.dataset.p.split(',');mp.value=a[0];mq.value=a[1];mul();}};}});
 document.querySelectorAll('.mc input').forEach(function(i){{i.addEventListener('keydown',function(e){{e.stopPropagation();if(e.key==='Enter')(i===fn?fac:mul)();}});}});
 document.querySelectorAll('.ix').forEach(function(x){{x.addEventListener('click',function(e){{e.stopPropagation();}});}});
 mul();fn.value='143';fac();
}})();
</script>'''
S.append(sec(inner, '활동 2 · 체험', '곱하기는 1번, 되돌리기는 몇 번?', BG2,
             '예시 소수 버튼을 차례로 누르고 ②에서 분해해 본다. 100003×100019 → 약 5만 번, 1000003×1000033 → 약 50만 번. 입력칸에서 타이핑 중에는 슬라이드가 넘어가지 않는다.'))

# 8. 자릿수가 커지면 -----------------------------------------------------------
rows = [('3자리', '11 × 13 = 143', '5번'), ('10자리', '두 소수가 각각 5자리', '약 5만 번'),
        ('20자리', '두 소수가 각각 10자리', '약 50억 번'), ('617자리', '실제 RSA 암호 (2048비트)', '1 뒤에 0이 300개 넘게…')]
trs = ''.join(f'<tr {B(i+1)}><td style="font-weight:700">{a}</td><td>{b}</td><td style="color:{R}; font-weight:700">{c}</td></tr>' for i, (a, b, c) in enumerate(rows))
inner = (f'<table id="t8" style="position:absolute; left:96px; top:200px; width:1728px; border-collapse:collapse; font-size:40px; text-align:center; background:#FFF">'
         f'<tr style="background:#DCEBEE"><th style="padding:14px">N의 크기</th><th>예</th><th>하나씩 나눠 보면</th></tr>{trs}</table>'
         '<style>#t8 td{padding:14px 10px;border-top:1px solid #E5E7EB}</style>'
         + box(96, 700, 1728, rich('컴퓨터는 더 똑똑한 방법을 쓰지만, 지금까지 분해에 성공한 가장 큰 RSA 도전 수는 [b]250자리[/b] (2020년)예요.\n'
                                   '→ 600자리가 넘는 N은 [r]현재 컴퓨터로는 사실상 분해할 수 없다.[/r]'), n=5, bg=PILL, size=38))
S.append(sec(inner, '활동 2 · 정리', '숫자가 수백 자리가 되면 왜 컴퓨터로도 못 풀까?', BG1,
             '횟수는 "√N까지 홀수로 나눠 보기" 기준 대략값. 학습지 "탐구한 핵심 내용 정리하기" 칸에 쓸 내용.'))

# 9. RSA 한눈에 (자물쇠 비유) --------------------------------------------------
lock = ('<svg viewBox="0 0 120 140" width="150" height="175"><path d="M30 60 V38 a30 30 0 0 1 60 0 V{v}" fill="none" stroke="{c}" stroke-width="12" stroke-linecap="round"/>'
        '<rect x="12" y="60" width="96" height="74" rx="12" fill="{c}"/><circle cx="60" cy="92" r="10" fill="#FFF"/><rect x="55" y="96" width="10" height="22" fill="#FFF"/></svg>')
inner = (box(96, 200, 540, f'<div style="text-align:center">{lock.format(v=46, c=BL)}</div>'
             + rich('[b]공개 열쇠 N[/b]\n= 열린 자물쇠\n누구에게나 나눠 준다\n(누구나 잠글 수 있음)'), n=1, size=36, extra='text-align:center')
         + box(690, 200, 540, f'<div style="text-align:center">{lock.format(v=60, c=DARK)}</div>'
               + rich('메시지를 N으로 [o]잠가서[/o]\n보낸다\n(중간에 누가 봐도\n알 수 없음)'), n=2, size=36, extra='text-align:center')
         + box(1284, 200, 540, '<div style="text-align:center"><svg viewBox="0 0 160 140" width="190" height="175"><circle cx="45" cy="70" r="32" fill="none" stroke="#E4572E" stroke-width="14"/>'
               '<path d="M77 70 H150 M125 70 V96 M145 70 V90" stroke="#E4572E" stroke-width="14" stroke-linecap="round"/></svg></div>'
               + rich('[r]비밀 열쇠 p, q[/r]\n= 자물쇠를 여는 열쇠\n나만 안다\n(N을 분해해야 얻음)'), n=3, size=36, extra='text-align:center')
         + box(96, 760, 1728, rich('N은 모두에게 공개해도 괜찮다 → N을 p × q로 [r]분해할 수 없으니까![/r]\n'
                                   '예) 주소창의 자물쇠 표시(https), 인터넷 뱅킹, 전자 서명'), n=4, bg=PILL, size=38))
S.append(sec(inner, 'RSA 암호의 아이디어', '공개 열쇠는 모두에게, 비밀 열쇠는 나만', BG2,
             'RSA: 1977년 리베스트·샤미르·애들먼이 만든 공개 열쇠 암호. 실제 잠그고 여는 계산은 고등 수준이므로 비유로만 설명.'))

# 10. 활동 3 안내 + 두 자리 소수 + 판정법 ------------------------------------------
two = [p for p in range(11, 100) if all(p % d for d in range(2, p))]
chips = ''.join(f'<span style="display:inline-block; width:84px; margin:5px; padding:6px 0; text-align:center; background:#FDECEA; border-radius:10px; color:{R}; font-weight:700">{p}</span>' for p in two)
inner = (box(96, 190, 900, rich('[g]1[/g] 나만 아는 비밀 소수 p, q 고르기\n[g]2[/g] N = p × q 계산해서 짝에게 [b]N만[/b] 전달\n[g]3[/g] 짝의 N을 소인수분해해서 p, q 찾기!'), size=38)
         + box(1030, 190, 794, f'<p style="font-size:30px; font-weight:700; color:{TEAL}">두 자리 소수 (21개)</p><div style="font-size:34px; font-family:Arial">{chips}</div>', n=1)
         + box(96, 470, 900, rich('[o]만들 때 팁[/o]\n· 고른 수가 정말 소수인지 확인!\n· 곱셈은 두 번 검산!\n· 두 자리 소수를 쓰면 짝이 고생해요 😎'), n=2, size=36, bg=PILL)
         + box(96, 790, 1728, rich('[b]풀 때 팁[/b]  작은 소수부터 나눠 본다.  '
                                   '[r]2[/r]: 끝자리 짝수   [r]3[/r]: 각 자리 합이 3의 배수   [r]5[/r]: 끝자리 0, 5   → 그다음 7, 11, 13, 17, …\n'
                                   'N이 네 자리 이하면 [r]97[/r]까지만 나눠 보면 반드시 찾을 수 있어요.'), n=3, size=34))
S.append(sec(inner, '활동 3 · 짝 활동', '짝과 함께 비밀 자물쇠 만들기', BG1,
             'N이 네 자리 이하(10000 미만)면 작은 쪽 소수는 100 미만이므로 97까지 시도하면 된다. 풀기 어려워하면 활동 2의 분해 기계로 확인.'))

# 11. 활동 4: 성찰 + 러닝페이퍼 아이디어 -------------------------------------------
ideas = [('매미와 소수', '13년·17년마다 나타나는 매미는 왜 소수 주기일까?'),
         ('소수는 끝이 있을까?', '유클리드가 증명한 "소수는 무한히 많다"'),
         ('가장 큰 소수 찾기', '메르센 소수와 컴퓨터로 소수를 찾는 사람들'),
         ('양자 컴퓨터와 암호', '양자 컴퓨터가 생기면 RSA는 어떻게 될까?')]
cards = ''.join(box(96 + (i % 2) * 874, 520 + (i // 2) * 200, 854, rich(f'[p]{a}[/p]\n{b}'), n=i+2, size=32) for i, (a, b) in enumerate(ideas))
inner = (box(96, 190, 1728, rich('[g]한 문장 정리 예시[/g]\n"소수는 [r]곱하기는 쉽지만 소인수분해는 매우 어렵다는 성질[/r] 덕분에 '
                                 '인터넷 속 우리의 비밀을 지켜 주는 [r]자물쇠의 재료[/r]이다."'), n=1, size=38, bg=PILL)
         + f'<p {B(2)} style="position:absolute; left:96px; top:455px; font-size:34px; font-weight:700; color:{TEAL}">러닝페이퍼 수학 탐구 주제 아이디어</p>'
         + cards)
S.append(sec(inner, '활동 4 · 성찰 일지', '오늘 배운 것을 한 문장으로', BG2))

shell = open(os.path.join(HERE, 'shell.html')).read()
open(OUT, 'w').write(shell.replace('%%TITLE%%', '암호와 수 - 소수와 RSA 암호').replace('%%SLIDES%%', '\n'.join(S)))
print(OUT, len(S))
