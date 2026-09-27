#!/bin/bash
# usage: shots.sh file.html N outprefix
F=$1; N=$2; P=$3; C=/opt/pw-browsers/chromium-1194/chrome-linux/chrome
for ((i=0;i<N;i++)); do
 sed "s#fit();show();#fit();i=$i;step=99;show();document.querySelectorAll('[data-build-in]').forEach(e=>{e.style.transition='none';e.classList.remove('hid')});#" "$F" > /tmp/claude-0/-home-user-outeq111/d86e19ab-ec80-5ac1-a09b-c4db87ef5a17/t.html
 $C --headless --no-sandbox --disable-gpu --hide-scrollbars --window-size=960,540 --screenshot=${P}_$i.png file:///tmp/claude-0/-home-user-outeq111/d86e19ab-ec80-5ac1-a09b-c4db87ef5a17/t.html >/dev/null 2>&1
done
python3 -c "
from PIL import Image
import sys
N=$N; ims=[Image.open(f'${P}_{i}.png') for i in range(N)]
for s in range(0,N,6):
  c=Image.new('RGB',(960*2,540*3),'white')
  for k,im in enumerate(ims[s:s+6]): c.paste(im,((k%2)*960,(k//2)*540))
  c.save(f'${P}_sheet{s//6}.png')
"
