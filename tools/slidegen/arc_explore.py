"""원주각 2차시 생각톡 탐구용 인터랙티브 슬라이드: 시계 둘레의 점 A, B, C, D, P를 눈금에 맞춰 끌면서
호의 길이(칸 수)와 원주각 ∠APB, ∠CPD를 실시간으로 비교."""
FONT = "'Noto Sans KR','Apple SD Gothic Neo','Malgun Gothic','Nanum Gothic',sans-serif"
BG1, DARK, TEAL = '#F7F6F1', '#1E2A3A', '#1F7A8C'


def arc_explore_slide():
    return ('<section style="background:' + BG1 + '; color:' + DARK + '; font-family:' + FONT + '; padding:96px; display:flex; flex-direction:column">'
    '<p style="position:absolute; left:96px; top:44px; width:1700px; font-size:30px; font-weight:700; color:' + TEAL + '">생각톡 · 직접 움직여 보기</p>'
    '<p style="position:absolute; left:96px; top:90px; width:1728px; font-size:40px; font-weight:700">시계 둘레의 점을 움직이며 호의 길이와 원주각의 크기를 비교해 보자.</p>'
    '''<div class="ix" style="position:absolute; left:96px; top:180px; width:1000px; height:820px; background:#FFFFFF; border-radius:16px">
<svg id="ax" viewBox="0 0 1000 820" width="1000" height="820" style="touch-action:none; user-select:none; -webkit-user-select:none">
 <circle cx="500" cy="420" r="330" fill="#FFFFFF" stroke="#8FCBE8" stroke-width="22"/>
 <circle cx="500" cy="420" r="318" fill="none" stroke="#1E2A3A" stroke-width="3"/>
 <g id="axTicks"></g>
 <g id="axCen" style="display:none">
  <path id="axWOab" fill="#E4572E" fill-opacity="0.25" stroke="#E4572E" stroke-width="3"/>
  <path id="axWOcd" fill="#1F6FB2" fill-opacity="0.25" stroke="#1F6FB2" stroke-width="3"/>
  <line id="axOA" stroke="#E4572E" stroke-width="3" stroke-dasharray="10 7"/><line id="axOB" stroke="#E4572E" stroke-width="3" stroke-dasharray="10 7"/>
  <line id="axOC" stroke="#1F6FB2" stroke-width="3" stroke-dasharray="10 7"/><line id="axOD" stroke="#1F6FB2" stroke-width="3" stroke-dasharray="10 7"/>
  <text id="axTOab" font-size="30" font-weight="700" font-family="Arial" fill="#E4572E" text-anchor="middle" stroke="#FFF" stroke-width="6" paint-order="stroke"></text>
  <text id="axTOcd" font-size="30" font-weight="700" font-family="Arial" fill="#1F6FB2" text-anchor="middle" stroke="#FFF" stroke-width="6" paint-order="stroke"></text>
 </g>
 <path id="axArcAB" fill="none" stroke="#E4572E" stroke-width="14" stroke-linecap="round" opacity="0.8"/>
 <path id="axArcCD" fill="none" stroke="#1F6FB2" stroke-width="14" stroke-linecap="round" opacity="0.8"/>
 <path id="axWab" fill="#E4572E" fill-opacity="0.35" stroke="#E4572E" stroke-width="3"/>
 <path id="axWcd" fill="#1F6FB2" fill-opacity="0.35" stroke="#1F6FB2" stroke-width="3"/>
 <line id="axPA" stroke="#1E2A3A" stroke-width="4"/><line id="axPB" stroke="#1E2A3A" stroke-width="4"/>
 <line id="axPC" stroke="#1E2A3A" stroke-width="4"/><line id="axPD" stroke="#1E2A3A" stroke-width="4"/>
 <circle cx="500" cy="420" r="8" fill="#1E2A3A"/>
 <g id="axPts"></g>
</svg></div>
<div class="ix" style="position:absolute; left:1150px; top:190px; width:680px; display:flex; flex-direction:column; gap:22px">
 <div style="display:grid; grid-template-columns:auto auto; gap:10px 28px; font-size:40px; align-items:baseline">
  <span>호 <b style="color:#E4572E">AB</b> = <b id="axLab" style="color:#E4572E"></b></span><span>∠APB = <b id="axVab" style="color:#E4572E"></b></span>
  <span>호 <b style="color:#1F6FB2">CD</b> = <b id="axLcd" style="color:#1F6FB2"></b></span><span>∠CPD = <b id="axVcd" style="color:#1F6FB2"></b></span>
 </div>
 <p style="font-size:30px; line-height:1.5; color:#4A5568">· 점 A, B, C, D, P를 끌어 보세요. 시계 눈금(1시간 = 한 칸)에 맞춰 움직여요.<br>· 호의 길이는 점 P가 없는 쪽 호의 칸 수예요.</p>
 <div style="display:flex; gap:14px; flex-wrap:wrap">
  <button class="axb" id="axReset">교과서 그림</button>
  <button class="axb" id="axDouble">호 CD를 2칸으로</button>
  <button class="axb" id="axCenB">중심각 보기</button>
 </div>
 <p id="axMsg" style="font-size:34px; line-height:1.45; font-weight:700; background:#FCE0C4; padding:18px 26px; border-radius:14px"></p>
</div>
<style>.axb{font:700 28px ''' + FONT + '''; padding:12px 20px; border:0; border-radius:12px; background:#DCEBEE; color:#1E2A3A; cursor:pointer}.axb.on{background:#1F7A8C; color:#FFF}</style>
<script>
(function(){
 var cx=500,cy=420,r=318,NS='http://www.w3.org/2000/svg',s=document.getElementById('ax');
 var init={A:9,B:8,C:5,D:4,P:0}, h={}, drag=null, cen=false;
 var col={A:'#1E2A3A',B:'#1E2A3A',C:'#1E2A3A',D:'#1E2A3A',P:'#E4572E'};
 function pt(hr,rr){var a=(hr*30-90)*Math.PI/180;rr=rr||r;return [cx+rr*Math.cos(a),cy+rr*Math.sin(a)];}
 function el(t,a){var e=document.createElementNS(NS,t);for(var k in a)e.setAttribute(k,a[k]);return e;}
 var tk=document.getElementById('axTicks');
 for(var m=0;m<60;m++){var big=m%5===0,a=pt(m/5,r-2),b=pt(m/5,r-(big?30:14));tk.appendChild(el('line',{x1:a[0],y1:a[1],x2:b[0],y2:b[1],stroke:'#1E2A3A','stroke-width':big?5:2}));}
 for(var k=1;k<=12;k++){var q=pt(k,r-62),t=el('text',{x:q[0],y:q[1]+13,'font-size':38,'font-family':'Arial','text-anchor':'middle',fill:'#6B7280'});t.textContent=k;tk.appendChild(t);}
 var G={},pg=document.getElementById('axPts');
 ['A','B','C','D','P'].forEach(function(n){var g=el('g',{style:'cursor:grab'});g.appendChild(el('circle',{r:32,fill:n==='P'?'#E4572E':'#1F6FB2','fill-opacity':0.18}));
   g.appendChild(el('circle',{r:11,fill:col[n]}));var t=el('text',{'font-size':46,'font-family':'Times New Roman','text-anchor':'middle',fill:col[n]});t.textContent=n;g.appendChild(t);pg.appendChild(g);G[n]=g;});
 function set(id,a,b){var e=document.getElementById(id);e.setAttribute('x1',a[0]);e.setAttribute('y1',a[1]);e.setAttribute('x2',b[0]);e.setAttribute('y2',b[1]);}
 // X에서 Y까지 P가 없는 쪽 호: [시작, 칸 수] (시계 방향)
 function arc(x,y){var cw=((h[y]-h[x])%12+12)%12, pp=((h.P-h[x])%12+12)%12; return pp<cw?[h[y],12-cw]:[h[x],cw];}
 function arcPath(st,n,rr){var a=pt(st,rr),b=pt(st+n,rr);return 'M'+a[0]+','+a[1]+' A'+rr+','+rr+' 0 '+(n>6?1:0)+' 1 '+b[0]+','+b[1];}
 function wedge(v,u,w,rad){var a=Math.atan2(u[1]-v[1],u[0]-v[0]),b=Math.atan2(w[1]-v[1],w[0]-v[0]),d=(b-a+2*Math.PI)%(2*Math.PI);
   if(d>Math.PI){var x=a;a=b;b=x;d=2*Math.PI-d;}
   return 'M'+v[0]+','+v[1]+' L'+(v[0]+rad*Math.cos(a))+','+(v[1]+rad*Math.sin(a))+' A'+rad+','+rad+' 0 '+(d>Math.PI?1:0)+' 1 '+(v[0]+rad*Math.cos(b))+','+(v[1]+rad*Math.sin(b))+' Z';}
 function secW(st,n,rad){var a=pt(st,rad),b=pt(st+n,rad);return 'M'+cx+','+cy+' L'+a[0]+','+a[1]+' A'+rad+','+rad+' 0 '+(n>6?1:0)+' 1 '+b[0]+','+b[1]+' Z';}
 function draw(){
  var P={};['A','B','C','D','P'].forEach(function(n){P[n]=pt(h[n]);var l=pt(h[n],r+52);G[n].setAttribute('transform','translate('+P[n][0]+','+P[n][1]+')');
    var t=G[n].querySelector('text');t.setAttribute('x',l[0]-P[n][0]);t.setAttribute('y',l[1]-P[n][1]+15);});
  var ab=arc('A','B'),cd=arc('C','D');
  document.getElementById('axArcAB').setAttribute('d',arcPath(ab[0],ab[1],r));
  document.getElementById('axArcCD').setAttribute('d',arcPath(cd[0],cd[1],r));
  set('axPA',P.P,P.A);set('axPB',P.P,P.B);set('axPC',P.P,P.C);set('axPD',P.P,P.D);
  document.getElementById('axWab').setAttribute('d',wedge(P.P,P.A,P.B,90));
  document.getElementById('axWcd').setAttribute('d',wedge(P.P,P.C,P.D,130));
  var O=[cx,cy];set('axOA',O,P.A);set('axOB',O,P.B);set('axOC',O,P.C);set('axOD',O,P.D);
  document.getElementById('axWOab').setAttribute('d',secW(ab[0],ab[1],60));
  document.getElementById('axWOcd').setAttribute('d',secW(cd[0],cd[1],80));
  var m1=pt(ab[0]+ab[1]/2,120),m2=pt(cd[0]+cd[1]/2,140),t1=document.getElementById('axTOab'),t2=document.getElementById('axTOcd');
  t1.setAttribute('x',m1[0]);t1.setAttribute('y',m1[1]+10);t1.textContent=30*ab[1]+'°';t2.setAttribute('x',m2[0]);t2.setAttribute('y',m2[1]+10);t2.textContent=30*cd[1]+'°';
  document.getElementById('axCen').style.display=cen?'':'none';
  var x=15*ab[1],y=15*cd[1];
  document.getElementById('axLab').textContent=ab[1]+'칸';document.getElementById('axLcd').textContent=cd[1]+'칸';
  document.getElementById('axVab').textContent=x+'°';document.getElementById('axVcd').textContent=y+'°';
  var msg;
  if(ab[1]===cd[1])msg='호 AB = 호 CD (각각 '+ab[1]+'칸)<br>→ ∠APB = ∠CPD = '+x+'°  <span style="color:#2E9E5B">같다!</span>';
  else msg='호의 길이가 다르면 원주각도 달라요.<br>'+ab[1]+'칸 : '+cd[1]+'칸 = '+x+'° : '+y+'°';
  if(cen)msg+='<br><span style="font-size:28px; font-weight:400">중심각은 한 칸에 30°, 원주각은 그 ½인 15°</span>';
  document.getElementById('axMsg').innerHTML=msg;
 }
 function reset(){for(var k in init)h[k]=init[k];draw();}
 function loc(e){var b=s.getBoundingClientRect();return [(e.clientX-b.left)*1000/b.width,(e.clientY-b.top)*820/b.height];}
 s.addEventListener('pointerdown',function(e){e.preventDefault();var q=loc(e),best=null,bd=60;
   for(var n in h){var p=pt(h[n]),d=Math.hypot(p[0]-q[0],p[1]-q[1]);if(d<bd){bd=d;best=n;}}
   if(best){drag=best;s.setPointerCapture(e.pointerId);}});
 s.addEventListener('pointermove',function(e){if(!drag)return;var q=loc(e),a=Math.atan2(q[1]-cy,q[0]-cx)*180/Math.PI+90;
   var hr=((Math.round(a/30))%12+12)%12;for(var n in h)if(n!==drag&&h[n]===hr)return;if(h[drag]!==hr){h[drag]=hr;draw();}});
 s.addEventListener('pointerup',function(){drag=null;});
 document.getElementById('axReset').onclick=reset;
 document.getElementById('axDouble').onclick=function(){reset();h.C=6;draw();};
 document.getElementById('axCenB').onclick=function(){cen=!cen;this.classList.toggle('on',cen);draw();};
 document.querySelectorAll('.ix').forEach(function(x){x.addEventListener('click',function(e){e.stopPropagation();});});
 reset();
})();
</script>'''
    '<aside>교과서 그림과 같은 위치(A=9시, B=8시, C=5시, D=4시, P=12시)에서 시작. 점을 끌면 시계 눈금(1시간)에 맞춰 이동한다. '
    '"호 CD를 2칸으로"를 누르면 호의 길이가 2배일 때 원주각도 2배임을 볼 수 있다. 다음 슬라이드는 → 키나 그림 밖 여백 클릭.</aside>'
    '</section>')
