"""생각톡 탐구용 인터랙티브 슬라이드: 원 위의 점 P(와 A, B)를 끌어 ∠APB, ∠AOB를 실시간으로 관찰."""
from lib import FONT, BG1, DARK, TEAL

def explore_slide():
    return ('<section style="background:' + BG1 + '; color:' + DARK + '; font-family:' + FONT + '; padding:96px; display:flex; flex-direction:column">'
    '<p style="position:absolute; left:96px; top:44px; width:1700px; font-size:30px; font-weight:700; color:' + TEAL + '">생각톡 · 직접 움직여 보기</p>'
    '<p style="position:absolute; left:96px; top:90px; width:1728px; font-size:40px; font-weight:700">점 P를 끌어 원 위에서 움직여 보자. ∠APB의 크기는 어떻게 될까?</p>'
    '''<div class="ix" style="position:absolute; left:96px; top:180px; width:1000px; height:820px; background:#FFFFFF; border-radius:16px">
<svg id="ixs" viewBox="0 0 1000 820" width="1000" height="820" style="touch-action:none; cursor:default">
 <circle cx="500" cy="420" r="330" fill="none" stroke="#1E2A3A" stroke-width="5"/>
 <path id="ixArcAB" fill="none" stroke="#E4572E" stroke-width="12" stroke-linecap="round" opacity="0.8"/>
 <path id="ixWO" fill="#1F6FB2" fill-opacity="0.35" stroke="#1F6FB2" stroke-width="3"/>
 <path id="ixWP" fill="#E4572E" fill-opacity="0.4" stroke="#E4572E" stroke-width="3"/>
 <line id="ixOA" stroke="#1F6FB2" stroke-width="4"/><line id="ixOB" stroke="#1F6FB2" stroke-width="4"/>
 <line id="ixPA" stroke="#1E2A3A" stroke-width="4"/><line id="ixPB" stroke="#1E2A3A" stroke-width="4"/>
 <circle cx="500" cy="420" r="8" fill="#1E2A3A"/><text x="515" y="410" font-size="40" font-family="Times New Roman" fill="#1E2A3A">O</text>
 <text id="ixTO" font-size="36" font-weight="700" font-family="Arial" fill="#1F6FB2" text-anchor="middle"></text>
 <text id="ixTP" font-size="36" font-weight="700" font-family="Arial" fill="#E4572E" text-anchor="middle"></text>
 <g id="ixA"><circle r="30" fill="#1F6FB2" fill-opacity="0.15"/><circle r="10" fill="#1E2A3A"/><text font-size="44" font-family="Times New Roman" fill="#1E2A3A">A</text></g>
 <g id="ixB"><circle r="30" fill="#1F6FB2" fill-opacity="0.15"/><circle r="10" fill="#1E2A3A"/><text font-size="44" font-family="Times New Roman" fill="#1E2A3A">B</text></g>
 <g id="ixP" style="cursor:grab"><circle r="34" fill="#E4572E" fill-opacity="0.25"/><circle r="12" fill="#E4572E"/><text font-size="44" font-family="Times New Roman" fill="#E4572E">P</text></g>
</svg></div>
<div class="ix" style="position:absolute; left:1150px; top:220px; width:680px; display:flex; flex-direction:column; gap:28px">
 <p style="font-size:44px">∠APB = <b id="ixVP" style="color:#E4572E"></b></p>
 <p style="font-size:44px">∠AOB = <b id="ixVO" style="color:#1F6FB2"></b></p>
 <p style="font-size:34px; line-height:1.5; color:#4A5568">· 빨간 점 <b style="color:#E4572E">P</b>를 끌어 보세요.<br>· 점 A, B도 끌어서 호 AB를 바꿀 수 있어요.<br>· P가 호 AB(빨간 호) 위로 가면 원주각이 아니에요.</p>
 <p id="ixMsg" style="font-size:36px; font-weight:700; background:#FCE0C4; padding:18px 26px; border-radius:14px"></p>
</div>
<script>
(function(){
 var cx=500,cy=420,r=330, t={A:215,B:325,P:95}, drag=null, s=document.getElementById('ixs');
 function pt(a){a=a*Math.PI/180;return [cx+r*Math.cos(a),cy+r*Math.sin(a)];}
 function ang(u,v,w){var a=Math.atan2(u[1]-v[1],u[0]-v[0]),b=Math.atan2(w[1]-v[1],w[0]-v[0]),d=Math.abs(a-b)*180/Math.PI;return d>180?360-d:d;}
 function set(id,a,b){var e=document.getElementById(id);e.setAttribute('x1',a[0]);e.setAttribute('y1',a[1]);e.setAttribute('x2',b[0]);e.setAttribute('y2',b[1]);}
 function onArcAB(tp){var d=(t.B-t.A+360)%360,q=(tp-t.A+360)%360;return q<d;}
 function wedge(v,u,w,rad,big){var a=Math.atan2(u[1]-v[1],u[0]-v[0]),b=Math.atan2(w[1]-v[1],w[0]-v[0]);var d=(b-a+2*Math.PI)%(2*Math.PI);
   if(!big&&d>Math.PI){var x=a;a=b;b=x;d=2*Math.PI-d;}
   return 'M'+v[0]+','+v[1]+' L'+(v[0]+rad*Math.cos(a))+','+(v[1]+rad*Math.sin(a))+' A'+rad+','+rad+' 0 '+(d>Math.PI?1:0)+' 1 '+(v[0]+rad*Math.cos(b))+','+(v[1]+rad*Math.sin(b))+' Z';}
 function draw(){
  var A=pt(t.A),B=pt(t.B),P=pt(t.P),O=[cx,cy];
  ['A','B','P'].forEach(function(k){var p=pt(t[k]),g=document.getElementById('ix'+k);g.setAttribute('transform','translate('+p[0]+','+p[1]+')');
    var tx=g.querySelector('text');tx.setAttribute('x',(p[0]-cx)*0.16-14);tx.setAttribute('y',(p[1]-cy)*0.16+14);});
  set('ixOA',O,A);set('ixOB',O,B);set('ixPA',P,A);set('ixPB',P,B);
  var d=(t.B-t.A+360)%360, big=d>180;
  document.getElementById('ixArcAB').setAttribute('d','M'+A[0]+','+A[1]+' A'+r+','+r+' 0 '+(big?1:0)+' 1 '+B[0]+','+B[1]);
  var cen=d, ins=cen/2;
  document.getElementById('ixWO').setAttribute('d',wedge(O,A,B,60,true));
  var bad=onArcAB(t.P);
  document.getElementById('ixWP').setAttribute('d',bad?'':wedge(P,A,B,70,false));
  var mid=(t.A+d/2)*Math.PI/180, tO=document.getElementById('ixTO');
  tO.setAttribute('x',cx+105*Math.cos(mid));tO.setAttribute('y',cy+105*Math.sin(mid)+12);tO.textContent=Math.round(cen)+'°';
  var tP=document.getElementById('ixTP'),mA=Math.atan2((A[1]+B[1])/2-P[1],(A[0]+B[0])/2-P[0]);
  tP.setAttribute('x',P[0]+115*Math.cos(mA));tP.setAttribute('y',P[1]+115*Math.sin(mA)+12);tP.textContent=bad?'':Math.round(ins)+'°';
  document.getElementById('ixVO').textContent=Math.round(cen)+'°';
  document.getElementById('ixVP').textContent=bad?'—':Math.round(ang(A,P,B))+'°';
  document.getElementById('ixMsg').innerHTML=bad?'P가 호 AB 위에 있어요. 호 AB 밖으로 옮겨 보세요.':'∠APB = ½ × ∠AOB = ½ × '+Math.round(cen)+'° = '+Math.round(ins)+'°';
 }
 function loc(e){var b=s.getBoundingClientRect();return [(e.clientX-b.left)*1000/b.width,(e.clientY-b.top)*820/b.height];}
 s.addEventListener('pointerdown',function(e){var q=loc(e),best=null,bd=60;['P','A','B'].forEach(function(k){var p=pt(t[k]),dd=Math.hypot(p[0]-q[0],p[1]-q[1]);if(dd<bd){bd=dd;best=k;}});
   if(best){drag=best;s.setPointerCapture(e.pointerId);}});
 s.addEventListener('pointermove',function(e){if(!drag)return;var q=loc(e),a=Math.atan2(q[1]-cy,q[0]-cx)*180/Math.PI;a=(a+360)%360;
   if(drag!=='P'){var o=t[drag==='A'?'B':'A'],g=(a-o+360)%360;if(g<20||g>340)return;}t[drag]=a;draw();});
 s.addEventListener('pointerup',function(){drag=null;});
 document.querySelectorAll('.ix').forEach(function(el){el.addEventListener('click',function(e){e.stopPropagation();});});
 draw();
})();
</script>'''
    '<aside>교실 화면에서 선생님이 직접 끌거나, 학생이 나와서 움직여 보게 하세요. 클릭으로 다음 슬라이드로 넘어가려면 그림 밖을 누르거나 → 키를 쓰세요.</aside>'
    '</section>')
