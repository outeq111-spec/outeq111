"""원주각의 활용 2차시 생각톡 탐구용 인터랙티브 슬라이드: 원 위의 점 B(와 C)를 끌어
접선과 현이 이루는 각 ∠BAT와 원주각 ∠BCA를 실시간으로 비교 (교과서의 컴퓨터 프로그램 화면 재현)."""
FONT = "'Noto Sans KR','Apple SD Gothic Neo','Malgun Gothic','Nanum Gothic',sans-serif"
BG1, DARK, TEAL = '#F7F6F1', '#1E2A3A', '#1F7A8C'


def tangent_explore_slide():
    return ('<section style="background:' + BG1 + '; color:' + DARK + '; font-family:' + FONT + '; padding:96px; display:flex; flex-direction:column">'
    '<p style="position:absolute; left:96px; top:44px; width:1700px; font-size:30px; font-weight:700; color:' + TEAL + '">생각톡 · 직접 움직여 보기</p>'
    '<p style="position:absolute; left:96px; top:90px; width:1728px; font-size:40px; font-weight:700">점 B를 원 위에서 움직이며 ∠BCA와 ∠BAT의 크기를 비교해 보자.</p>'
    '''<div class="ix" style="position:absolute; left:96px; top:180px; width:1000px; height:820px; background:#FFFFFF; border-radius:16px">
<svg id="tx" viewBox="0 0 1000 820" width="1000" height="820" style="touch-action:none; user-select:none; -webkit-user-select:none">
 <path id="txArc" fill="none" stroke="#2E9E5B" stroke-width="14" stroke-linecap="round" opacity="0.75" style="display:none"/>
 <circle cx="500" cy="390" r="300" fill="none" stroke="#1E2A3A" stroke-width="5"/>
 <line x1="90" y1="690" x2="950" y2="690" stroke="#1E2A3A" stroke-width="5"/>
 <path id="txWA" fill="#E4572E" fill-opacity="0.35" stroke="#E4572E" stroke-width="3"/>
 <path id="txWC" fill="#1F6FB2" fill-opacity="0.35" stroke="#1F6FB2" stroke-width="3"/>
 <path id="txRA" fill="none" stroke="#E4572E" stroke-width="4"/><path id="txRC" fill="none" stroke="#1F6FB2" stroke-width="4"/>
 <line id="txAB" stroke="#1E2A3A" stroke-width="4"/><line id="txBC" stroke="#1E2A3A" stroke-width="4"/><line id="txCA" stroke="#1E2A3A" stroke-width="4"/>
 <text id="txTA" font-size="30" font-weight="700" font-family="Arial" fill="#E4572E" text-anchor="middle" stroke="#FFF" stroke-width="6" paint-order="stroke"></text>
 <text id="txTC" font-size="30" font-weight="700" font-family="Arial" fill="#1F6FB2" text-anchor="middle" stroke="#FFF" stroke-width="6" paint-order="stroke"></text>
 <circle cx="500" cy="390" r="7" fill="#1E2A3A"/><text x="514" y="380" font-size="40" font-family="Times New Roman" fill="#1E2A3A">O</text>
 <circle cx="500" cy="690" r="10" fill="#1E2A3A"/><text x="500" y="742" font-size="44" font-family="Times New Roman" fill="#1E2A3A" text-anchor="middle">A</text>
 <circle cx="860" cy="690" r="8" fill="#1E2A3A"/><text x="860" y="742" font-size="44" font-family="Times New Roman" fill="#1E2A3A" text-anchor="middle">T</text>
 <g id="txB" style="cursor:grab"><circle r="34" fill="#E4572E" fill-opacity="0.22"/><circle r="12" fill="#E4572E"/><text font-size="46" font-family="Times New Roman" fill="#E4572E" text-anchor="middle">B</text></g>
 <g id="txC" style="cursor:grab"><circle r="30" fill="#1F6FB2" fill-opacity="0.18"/><circle r="10" fill="#1E2A3A"/><text font-size="46" font-family="Times New Roman" fill="#1E2A3A" text-anchor="middle">C</text></g>
</svg></div>
<div class="ix" style="position:absolute; left:1150px; top:190px; width:680px; display:flex; flex-direction:column; gap:22px">
 <p style="font-size:46px">∠BAT = <b id="txVA" style="color:#E4572E"></b></p>
 <p style="font-size:46px">∠BCA = <b id="txVC" style="color:#1F6FB2"></b></p>
 <p style="font-size:30px; line-height:1.5; color:#4A5568">· 빨간 점 <b style="color:#E4572E">B</b>를 원 위에서 끌어 보세요.<br>· 점 C도 움직일 수 있어요.<br>· 직선 AT는 점 A에서의 접선이에요.</p>
 <div style="display:flex; gap:14px; flex-wrap:wrap">
  <button class="txb" data-f="0">[그림 1]</button><button class="txb" data-f="1">[그림 2]</button><button class="txb" data-f="2">[그림 3]</button>
  <button class="txb" id="txArcB">호 AB 보기</button>
 </div>
 <p id="txMsg" style="font-size:34px; line-height:1.45; font-weight:700; background:#FCE0C4; padding:18px 26px; border-radius:14px"></p>
</div>
<style>.txb{font:700 28px ''' + FONT + '''; padding:12px 20px; border:0; border-radius:12px; background:#DCEBEE; color:#1E2A3A; cursor:pointer}.txb.on{background:#1F7A8C; color:#FFF}</style>
<script>
(function(){
 // 각 φ: 점 A(맨 아래)에서 시작해 T 쪽(오른쪽)으로 도는 각. B는 φB, C는 φC (φB < φC 이어야 C가 ∠BAT 밖의 호 위)
 var cx=500,cy=390,r=300,s=document.getElementById('tx'),A=[500,690],T=[860,690];
 var figs=[[180,290],[140.04,290],[224.4,290]], st={B:180,C:290}, drag=null, showArc=false;
 function pt(f){var a=(90-f)*Math.PI/180;return [cx+r*Math.cos(a),cy+r*Math.sin(a)];}
 function set(id,a,b){var e=document.getElementById(id);e.setAttribute('x1',a[0]);e.setAttribute('y1',a[1]);e.setAttribute('x2',b[0]);e.setAttribute('y2',b[1]);}
 function ang(u,v,w){var a=Math.atan2(u[1]-v[1],u[0]-v[0]),b=Math.atan2(w[1]-v[1],w[0]-v[0]),d=Math.abs(a-b)*180/Math.PI;return d>180?360-d:d;}
 function wedge(v,u,w,rad){var a=Math.atan2(u[1]-v[1],u[0]-v[0]),b=Math.atan2(w[1]-v[1],w[0]-v[0]),d=(b-a+2*Math.PI)%(2*Math.PI);
   if(d>Math.PI){var x=a;a=b;b=x;d=2*Math.PI-d;}
   return 'M'+v[0]+','+v[1]+' L'+(v[0]+rad*Math.cos(a))+','+(v[1]+rad*Math.sin(a))+' A'+rad+','+rad+' 0 0 1 '+(v[0]+rad*Math.cos(b))+','+(v[1]+rad*Math.sin(b))+' Z';}
 function rmark(v,u,w,sz){function n(p){var dx=p[0]-v[0],dy=p[1]-v[1],l=Math.hypot(dx,dy);return [dx/l,dy/l];}var a=n(u),b=n(w);
   return 'M'+(v[0]+a[0]*sz)+','+(v[1]+a[1]*sz)+' L'+(v[0]+(a[0]+b[0])*sz)+','+(v[1]+(a[1]+b[1])*sz)+' L'+(v[0]+b[0]*sz)+','+(v[1]+b[1]*sz);}
 function mid(v,u,w,rad){var a=Math.atan2(u[1]-v[1],u[0]-v[0]),b=Math.atan2(w[1]-v[1],w[0]-v[0]);var x=Math.cos(a)+Math.cos(b),y=Math.sin(a)+Math.sin(b),l=Math.hypot(x,y)||1;return [v[0]+rad*x/l,v[1]+rad*y/l];}
 function place(id,p){var g=document.getElementById(id),t=g.querySelector('text');g.setAttribute('transform','translate('+p[0]+','+p[1]+')');
   var dx=p[0]-cx,dy=p[1]-cy,l=Math.hypot(dx,dy);t.setAttribute('x',dx/l*50);t.setAttribute('y',dy/l*50+15);}
 function draw(){
  var B=pt(st.B),C=pt(st.C);place('txB',B);place('txC',C);
  set('txAB',A,B);set('txBC',B,C);set('txCA',C,A);
  var va=ang(B,A,T),vc=ang(B,C,A),right=Math.abs(va-90)<0.005;
  document.getElementById('txWA').setAttribute('d',right?'':wedge(A,B,T,70));
  document.getElementById('txWC').setAttribute('d',Math.abs(vc-90)<0.005?'':wedge(C,B,A,60));
  document.getElementById('txRA').setAttribute('d',right?rmark(A,B,T,28):'');
  document.getElementById('txRC').setAttribute('d',Math.abs(vc-90)<0.005?rmark(C,B,A,24):'');
  var ma=mid(A,B,T,110),mc=mid(C,B,A,100);
  var tA=document.getElementById('txTA'),tC=document.getElementById('txTC');
  tA.setAttribute('x',ma[0]);tA.setAttribute('y',Math.min(ma[1]+10,676));tA.textContent=va.toFixed(2)+'°';
  tC.setAttribute('x',mc[0]);tC.setAttribute('y',mc[1]+10);tC.textContent=vc.toFixed(2)+'°';
  var s0=pt(0),s1=pt(st.B);
  var ap=document.getElementById('txArc');ap.style.display=showArc?'':'none';
  ap.setAttribute('d','M'+s0[0]+','+s0[1]+' A'+r+','+r+' 0 '+(st.B>180?1:0)+' 0 '+s1[0]+','+s1[1]);
  document.getElementById('txVA').textContent=va.toFixed(2)+'°';document.getElementById('txVC').textContent=vc.toFixed(2)+'°';
  var kind=va<89.995?'예각':(va>90.005?'둔각':'직각');
  document.getElementById('txMsg').innerHTML='∠BAT가 '+kind+'일 때<br>∠BAT = ∠BCA = '+va.toFixed(2)+'°'+
    (showArc?'<br><span style="font-size:28px; font-weight:400">두 각 모두 <b style="color:#2E9E5B">호 AB</b>(∠BAT 안쪽의 호)와 관련된 각이에요.</span>':'');
 }
 function loc(e){var b=s.getBoundingClientRect();return [(e.clientX-b.left)*1000/b.width,(e.clientY-b.top)*820/b.height];}
 function phi(q){var a=Math.atan2(-(q[1]-cy),q[0]-cx)*180/Math.PI;return ((a+90)%360+360)%360;}
 s.addEventListener('pointerdown',function(e){e.preventDefault();var q=loc(e),best=null,bd=60;
   ['B','C'].forEach(function(n){var p=pt(st[n]),d=Math.hypot(p[0]-q[0],p[1]-q[1]);if(d<bd){bd=d;best=n;}});
   if(best){drag=best;s.setPointerCapture(e.pointerId);}});
 s.addEventListener('pointermove',function(e){if(!drag)return;var f=phi(loc(e));
   if(drag==='B')st.B=Math.max(8,Math.min(f,st.C-8));else st.C=Math.max(st.B+8,Math.min(f,352));draw();});
 s.addEventListener('pointerup',function(){drag=null;});
 document.querySelectorAll('.txb[data-f]').forEach(function(b){b.onclick=function(){var f=figs[+b.dataset.f];st.B=f[0];st.C=f[1];draw();};});
 document.getElementById('txArcB').onclick=function(){showArc=!showArc;this.classList.toggle('on',showArc);draw();};
 document.querySelectorAll('.ix').forEach(function(x){x.addEventListener('click',function(e){e.stopPropagation();});});
 draw();
})();
</script>'''
    '<aside>[그림 1]~[그림 3] 버튼은 교과서 화면과 같은 각(90°, 70.02°, 112.20°)으로 맞춘다. B를 천천히 돌리며 두 각이 항상 같음을 확인하고, '
    '"호 AB 보기"로 두 각이 모두 호 AB와 관련 있음을 예고한다. 점 C는 ∠BAT 바깥쪽 호 위에서만 움직인다. 다음 슬라이드는 → 키나 그림 밖 여백 클릭.</aside>'
    '</section>')
