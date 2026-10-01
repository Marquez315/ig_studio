import re
src=open('/mnt/user-data/uploads/index.html',encoding='utf-8').read()
def rep(old,new):
    global src
    assert src.count(old)==1,old[:60]
    src=src.replace(old,new)

# ---------- HTML ----------
rep('<div class="row" id="styles">','<div id="stylebox"><div class="row" id="styles">')
rep('<button id="rmx">🎲 Remix</button></div>','</div><div class="row" id="styles2"><button data-s="7">Feria</button><button data-s="8">Confeti</button><button data-s="9">Noche</button><button data-s="10">Cartel</button><button data-s="11">Canal</button><button data-s="12">Comic</button><button id="rmx">🎲 Remix</button></div></div>')
rep('<option value="">🎨 Paleta: según la foto</option>','<option value="">🎨 Paleta: automática (estilo / foto)</option><option value="foto">📷 Colores de la foto</option>')
rep('<div class="row"><select id="topic">','''<details style="margin:8px 0"><summary>🪧 Encabezado del cartel (estilos Feria a Comic)</summary>
  <div class="row"><input id="ev1" placeholder="Título grande (ej: SNCyT)"><input id="ev2" placeholder="Línea 2 (ej: 2026)"></div>
  <input id="sub" placeholder="Subtítulo (ej: Semana de la Ciencia y la Tecnología)"><input id="foot" placeholder="Pie (ej: Colegio Sargento Juan B. Cabral)" style="margin-top:6px">
  <div class="row"><input id="cta" value="¡Deslizá! >>"><input id="bye" value="¡Gracias por acompañarnos!"></div>
  <small style="color:var(--mu)">«Deslizá» va en todas las slides y «Gracias» en la última. Si dejás el título vacío, usa el de cada foto.</small></details>
  <div class="row"><select id="topic">''')
rep('<div class="card"><h2>3 · Stickers</h2>','''<div class="card"><h2>2b · Contexto y texto</h2>
  <textarea id="ctx" placeholder="Contá de qué se trata: qué pasó, dónde, quiénes participaron, qué aprendieron. Ej: Feria de ciencias del colegio. Los chicos mostraron robots y una transmisión en vivo."></textarea>
  <div class="row"><select id="struct"><option value="desc">📝 Describir las fotos</option><option value="story">📖 Contar una historia (inicio, nudo, cierre)</option><option value="info">🧠 Carrusel informativo (qué es, cómo, qué aprendimos)</option></select></div>
  <div id="pred" style="font-size:13px;color:var(--mu)"></div><div id="sugs" class="chips"></div>
  <div class="row"><input id="lw" placeholder="Enseñar a la app: palabras o frases, separadas por coma"><button id="lb" style="flex:none">🧠 Enseñar</button><button id="lc" style="flex:none">Olvidar</button></div>
  <small style="color:var(--mu)">Más contexto = mejor texto, con o sin IA. Las palabras que enseñes se asocian a la temática elegida arriba (o a la detectada) y mejoran el reconocimiento. También aprende cuando corregís la temática de una foto. Se guarda solo en este dispositivo.</small></div>
 <div class="card"><h2>3 · Stickers</h2>''')
rep('<div class="row"><button class="p" id="dl">⬇ Descargar PNG</button><button id="sh">📤 Compartir</button></div>','''<div class="row"><button class="p" id="dl">⬇ Descargar PNG</button><button id="sh">📤 Compartir</button></div>
  <div class="row" id="shr"><button data-n="ig">Instagram</button><button data-n="fb">Facebook</button><button data-n="wa">WhatsApp</button><button data-n="tg">Telegram</button><button data-n="x">X</button><button data-n="th">Threads</button></div>
  <small style="color:var(--mu)">En el celular, Instagram y Facebook abren el menú de compartir con las imágenes y el texto. WhatsApp, Telegram, X y Threads abren con el texto listo y descargan las imágenes para adjuntar. Ninguna red deja publicar sola desde una web.</small>''')
rep('</style>','.chips{display:flex;flex-wrap:wrap;gap:6px;margin:6px 0}.chips button{font-size:12px;padding:4px 10px;border-radius:99px}details>summary{cursor:pointer}\n</style>')

# ---------- JS: predicción ----------
rep("const guess=t=>{t=t||'';for(const k in TOP)if(TOP[k].rx.test(t))return k;return''};",
r"""let VOC={};try{VOC=JSON.parse(localStorage.igvoc||'{}')}catch(e){}
const saveVoc=()=>{try{localStorage.igvoc=JSON.stringify(VOC)}catch(e){}},norm=s=>(s||'').toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g,''),
STOP=new Set('el la los las un una unos unas de del al y e o u a en con por para que se su sus es son fue como mas muy pero sin sobre entre este esta estos estas ese esa eso lo le les me te mi tu nos hay ya no si tambien cada todo todos todas donde cuando quien mientras durante hacia desde hasta ser estar estan hizo hicieron'.split(' ')),
kws=t=>{const c={};(norm(t).match(/[a-z0-9]{4,}/g)||[]).forEach(w=>{if(!STOP.has(w))c[w]=(c[w]||0)+1});return Object.entries(c).sort((a,b)=>b[1]-a[1]).map(e=>e[0])};
const guess=t=>{t=t||'';const n=norm(t),sc={};for(const w in VOC)if(n.includes(w))sc[VOC[w]]=(sc[VOC[w]]||0)+2;for(const k in TOP)if(TOP[k].rx.test(t))sc[k]=(sc[k]||0)+1;const b=Object.entries(sc).sort((a,b)=>b[1]-a[1])[0];return b?b[0]:''};""")
rep("$('#topic').value||guess($('#theme').value)||'';","$('#topic').value||guess($('#theme').value+' '+$('#ctx').value)||'';")
rep("guess($('#theme').value)||'general'","guess($('#theme').value+' '+$('#ctx').value)||'general'")
rep("o.tp=t.value;o.man=1;o.auto=0;","o.tp=t.value;o.man=1;o.auto=0;if(o.tp&&o.note){kws(o.note).slice(0,4).forEach(w=>VOC[w]=o.tp);saveVoc()}")

NEWLOCAL=r"""function local(){const mt=mainTp(),T0=TOP[mt],cx=$('#ctx').value.trim(),th=$('#theme').value||T0.n.toLowerCase(),k=$('#kind').value,n=S.items.length,sc=$('#struct').value,O={proyecto:'Mirá lo que lograron en clase',tip:'Tip para tu clase',reto:'Desafío de programación',tutorial:'Paso a paso'},
sn=cx.split(/(?<=[.!?])\s+|\n+/).map(s=>s.trim()).filter(s=>s.length>3),cut=(s,m)=>{const w=s.replace(/[.!?]+$/,'').split(/\s+/);return w.slice(0,m).join(' ')+(w.length>m?'…':'')},
AR={story:['Todo empezó','Manos a la obra','Lo probamos','Lo logramos','Gracias'],info:['¿Qué es?','¿Cómo funciona?','¿Qué aprendimos?','Para probar','Compartimos']};
return{slides:S.items.map((o,i)=>{const t=TOP[tpx(o)||mt],a=n<2||i==0?0:i==n-1?4:1+Math.min(2,Math.floor((i-1)*3/Math.max(1,n-2))),ns=(o.note||'').split(/(?<=[.!?])\s+/)[0],
fr=ns?cut(ns,12):sn[i]?cut(sn[i],12):i==0?`${O[k]}: ${th}.`:i==n-1?'¿Lo probás en tu aula? Contanos cómo te va.':t.ph[(i-1)%5];
return{title:sc=='desc'?t.ti[i%6]:AR[sc][a],phrase:fr,emoji:t.em}}),
caption:`${sn.length?sn.slice(0,3).join(' '):`${O[k]}: ${th}.`} ${sn.length>1?'':T0.cp} ¿Te animás a probarlo en tu clase? ${T0.em}💡`.replace(/\s+/g,' '),hashtags:[...T0.tg,...kws(cx).slice(0,2).map(w=>'#'+w)]}}
function fill(r)"""
src,c=re.subn(r"function local\(\)\{.*?function fill\(r\)",lambda m:NEWLOCAL,src,count=1,flags=re.S);assert c==1
rep("const ins=`Tema: ${$('#theme').value||TOP[mt].n}.","const ins=`${CTXP()}Tema: ${$('#theme').value||TOP[mt].n}.")
rep("async function ai(p){","""const CTXP=()=>{const v=id=>$('#'+id).value.trim(),m={desc:'describí lo que se ve en cada foto',story:'contá una historia con inicio, nudo y cierre; cada slide avanza la historia',info:'armá un carrusel informativo: qué es, cómo funciona, qué aprendimos'};return(v('ctx')?`Contexto escrito por quien publica (es la fuente principal; usá sus datos y palabras): «${v('ctx')}». `:'')+(v('ev1')?`Evento o serie: ${v('ev1')} ${v('ev2')} ${v('sub')} ${v('foot')}. `:'')+`Estructura pedida: ${m[v('struct')]}. `};
async function ai(p){""")

# ---------- JS: estilos nuevos ----------
NS=r"""const FN='system-ui,sans-serif',FB='"Arial Black","Segoe UI Black",system-ui,sans-serif';
const hd=(o,i,n)=>{const v=id=>$('#'+id).value.trim(),l=n>1&&i==n-1;return{h1:v('ev1')||o.title||' ',h2:v('ev2'),sub:v('sub'),foot:v('foot'),c:n>1?(l?v('bye'):v('cta')):'',l}};
function cw(o,d){if(!S.pal)return d;const s=pl(o).slice().sort((a,b)=>lum(a)-lum(b)),B=s[0],q=[...s].sort((a,b)=>Math.abs(lum(b)-lum(B))-Math.abs(lum(a)-lum(B)));return{a:B,b:s[1],t:lum(B)>.5?[22,18,31]:[255,255,255],u:q[0],v:q[1],w:s[2]}}
function fit(x,t,w,s,wt,f){for(;s>18;s-=3){x.font=`${wt} ${s}px ${f}`;if(x.measureText(t).width<=w)break}return s}
function gbg(x,W,H,a,b,k=.3){const g=x.createLinearGradient(0,0,W*k,H);g.addColorStop(0,rgb(a));g.addColorStop(1,rgb(b));x.fillStyle=g;x.fillRect(0,0,W,H)}
function pill(x,t,cx,cy,s,bg,fg,L,rd){const W=x.canvas.width;s=fit(x,t,W*.88,s,800,FN);x.save();x.font=`800 ${s}px ${FN}`;const w=x.measureText(t).width+s*1.5,h=s*1.9;if(L!=null)cx=L+w/2;x.fillStyle=rgb(bg);if(rd==null){x.shadowColor='#0004';x.shadowBlur=14;x.shadowOffsetY=5}x.beginPath();x.roundRect(cx-w/2,cy-h/2,w,h,rd==null?h/2:rd);x.fill();x.shadowColor='transparent';if(rd!=null){x.lineWidth=5;x.strokeStyle='#111';x.stroke()}x.fillStyle=rgb(fg);x.textAlign='center';x.textBaseline='middle';x.fillText(t,cx,cy+s*.05);x.restore();return h}
function ttl(x,E,W,s,y,c1,c2,left,g2){const X=left?W*.07:W/2;x.save();x.textAlign=left?'left':'center';x.textBaseline='alphabetic';x.shadowColor='#0005';x.shadowBlur=s*.1;x.shadowOffsetY=s*.06;const a=fit(x,E.h1,W*.86,s,900,FB);y+=a*.85;x.font=`900 ${a}px ${FB}`;let f=rgb(c1);if(g2){f=x.createLinearGradient(0,y-a*.8,0,y);f.addColorStop(0,rgb(c1));f.addColorStop(1,rgb(g2))}x.fillStyle=f;x.fillText(E.h1,X,y);if(E.h2){const b=fit(x,E.h2,W*.86,s,900,FB);y+=b*.98;x.font=`900 ${b}px ${FB}`;x.fillStyle=rgb(c2);x.fillText(E.h2,X,y)}x.restore();return y}
function ph(x,o,X,Y,w,h,r,b,bc,rot,sh,cp){const W=x.canvas.width;x.save();x.translate(X+w/2,Y+h/2);x.rotate(rot);if(sh){x.shadowColor='#0007';x.shadowBlur=34;x.shadowOffsetY=12}x.fillStyle=rgb(bc);x.beginPath();x.roundRect(-w/2,-h/2,w,h,r);x.fill();x.shadowColor='transparent';cover(x,o,-w/2+b,-h/2+b,w-2*b,h-2*b,Math.max(.5,r-b));
if(cp&&o.title){const ix=-w/2+b,iw=w-2*b,iy=h/2-b,g=x.createLinearGradient(0,iy-h*.4,0,iy);g.addColorStop(0,'#0000');g.addColorStop(1,'#000d');x.fillStyle=g;x.fillRect(ix,iy-h*.4,iw,h*.4);x.fillStyle='#fff';x.textAlign='left';x.textBaseline='alphabetic';const pf=o.phrase?fit(x,o.phrase,iw-56,W*.034,500,FN):0,ok=pf>=W*.026;if(ok){x.font=`500 ${pf}px ${FN}`;x.fillText(o.phrase,ix+28,iy-24)}const tf=fit(x,o.title,iw-56,W*.056,800,FN);x.font=`800 ${tf}px ${FN}`;x.fillText(o.title,ix+28,iy-24-(ok?pf*1.5:0))}x.restore()}
const NS=[
// 7 Feria
(x,o,i,n,W,H,R,p,E)=>{const c=cw(o,{a:[16,118,128],b:[9,45,78],t:[255,205,90],u:[255,255,255],v:[255,107,107],w:[255,197,49]}),s=Math.min(W*.14,H*.105);gbg(x,W,H,c.a,c.b);let y=ttl(x,E,W,s,H*.03,c.t,c.u,0,S.pal?null:[255,150,50]);if(E.sub){const h=pill(x,E.sub,W/2,y+s*.38,W*.026,c.v,[255,255,255]);y+=s*.38+h/2}ph(x,o,W*.08,y+W*.04,W*.84,Math.max(240,H-(E.c?W*.17:W*.06)-y-W*.04),10,14,[255,255,255],R()*.04-.02,1,1);if(E.c)pill(x,E.c,W/2,H-W*.085,W*.032,c.w,[58,42,0])},
// 8 Confeti
(x,o,i,n,W,H,R,p,E)=>{const c=cw(o,{a:[104,48,176],b:[226,52,144],t:[255,230,0],u:[25,224,255],v:[255,255,255],w:[255,230,0]}),s=Math.min(W*.14,H*.105),K=[[25,224,255],[255,230,0],[255,140,60],[255,255,255],[120,255,160]];gbg(x,W,H,c.a,c.b,.2);x.save();x.globalAlpha=.75;for(let k=0;k<34;k++){const px=R()*W,py=R()*H,r=10+R()*26;x.fillStyle=rgb(K[k%5]);x.beginPath();if(k%3==2){x.moveTo(px,py-r);x.lineTo(px+r,py+r);x.lineTo(px-r,py+r)}else x.arc(px,py,r,0,7);x.fill()}x.restore();let y=ttl(x,E,W,s,H*.03,c.t,c.u,0);if(E.sub){const h=pill(x,E.sub,W/2,y+s*.38,W*.026,c.v,c.a);y+=s*.38+h/2}ph(x,o,W*.07,y+W*.04,W*.86,Math.max(240,H-(E.c?W*.17:W*.06)-y-W*.04),6,20,c.w,-R()*.03,1,1);if(E.c)pill(x,E.c,W/2,H-W*.085,W*.032,c.w,[40,20,70])},
// 9 Noche
(x,o,i,n,W,H,R,p,E)=>{const c=cw(o,{a:[8,18,48],b:[10,28,70],t:[255,255,255],u:[59,107,255],v:[59,107,255],w:[160,170,200]});gbg(x,W,H,c.a,c.b,0);x.fillStyle=rgb(c.u);x.fillRect(W*.07,H*.03,W*.09,10);const T=(E.h1+' '+E.h2).trim().toUpperCase(),s=fit(x,T,W*.86,W*.085,900,FB);x.textAlign='left';x.textBaseline='alphabetic';x.fillStyle=rgb(c.t);x.font=`900 ${s}px ${FB}`;let y=H*.03+s*1.45;x.fillText(T,W*.07,y);if(E.sub){const f=fit(x,E.sub,W*.86,W*.03,500,FN);x.font=`500 ${f}px ${FN}`;x.fillStyle=rgb(c.u);y+=f*1.5;x.fillText(E.sub,W*.07,y)}const bt=H-W*.27;ph(x,o,W*.07,y+W*.035,W*.86,Math.max(240,bt-y-W*.035),30,7,c.u,0,0);x.textAlign='center';x.fillStyle=rgb(c.t);const tt=E.l&&E.c?E.c:o.title||'',tf=fit(x,tt,W*.84,W*.05,800,FN);x.font=`800 ${tf}px ${FN}`;x.fillText(tt,W/2,bt+W*.075);if(o.phrase&&!E.l){const pf=fit(x,o.phrase,W*.84,W*.03,500,FN);x.font=`500 ${pf}px ${FN}`;x.fillStyle=rgb(c.w);x.fillText(o.phrase,W/2,bt+W*.075+tf*.9)}if(E.foot){const f=fit(x,E.foot,W*.7,W*.026,500,FN);x.font=`500 ${f}px ${FN}`;x.fillStyle=rgb(c.w);x.fillText(E.foot,W/2,H-W*.04)}if(n>1){x.strokeStyle=rgb(c.u);x.lineWidth=4;x.beginPath();x.arc(W*.9,H-W*.07,W*.035,0,7);x.stroke();x.font=`700 ${W*.03}px ${FN}`;x.fillStyle=rgb(c.u);x.textBaseline='middle';x.fillText(i+1,W*.9,H-W*.07)}},
// 10 Cartel
(x,o,i,n,W,H,R,p,E)=>{const c=cw(o,{a:[255,122,26],b:[214,40,48],t:[255,255,255],u:[48,24,12],v:[255,255,255],w:[255,197,49]}),s=Math.min(W*.16,H*.12),bh=W*.19;gbg(x,W,H,c.a,c.b,.2);let y=H*.025;if(E.sub){const h=pill(x,E.sub.toUpperCase(),0,y+W*.03,W*.019,c.v,c.b,W*.07);y+=W*.045+h/2}y=ttl(x,E,W,s,y,c.t,c.u,1);ph(x,o,W*.07,y+W*.04,W*.86,Math.max(240,H-bh-W*.035-y-W*.04),36,10,[255,255,255],0,1,1);x.fillStyle=rgb(c.w);x.fillRect(0,H-bh,W,bh);x.fillStyle=rgb(c.u);x.textAlign='left';x.textBaseline='middle';const tx=E.foot||o.title||'',f=fit(x,tx,W*.6,W*.032,800,FN);x.font=`800 ${f}px ${FN}`;x.fillText(tx,W*.07,H-bh/2);if(E.c){const g=fit(x,E.c,W*.28,W*.034,800,FN);x.font=`800 ${g}px ${FN}`;x.textAlign='right';x.fillText(E.c,W*.93,H-bh/2)}},
// 11 Canal
(x,o,i,n,W,H,R,p,E)=>{const c=cw(o,{a:[142,15,26],b:[84,8,18],t:[255,255,255],u:[255,200,200],v:[226,40,40],w:[50,4,10]}),m=W*.07,B=W*.17,bh=W*.2,y0=H*.025;gbg(x,W,H,c.a,c.b,0);x.fillStyle=rgb(c.v);x.beginPath();x.roundRect(m,y0,B,B,B*.22);x.fill();x.fillStyle='#fff';x.beginPath();x.moveTo(m+B*.38,y0+B*.3);x.lineTo(m+B*.38,y0+B*.7);x.lineTo(m+B*.7,y0+B*.5);x.fill();const T=(E.h1+' '+E.h2).trim().toUpperCase(),s=fit(x,T,W*.66,W*.08,900,FB),X=m+B+W*.04;x.textAlign='left';x.textBaseline='alphabetic';x.font=`900 ${s}px ${FB}`;x.fillStyle=rgb(c.t);x.fillText(T,X,y0+B*.5);if(E.sub){const f=fit(x,E.sub,W*.66,W*.03,500,FN);x.font=`500 ${f}px ${FN}`;x.fillStyle=rgb(c.u);x.fillText(E.sub,X,y0+B*.5+f*1.6)}const y=y0+B+W*.035;ph(x,o,m,y,W*.86,Math.max(240,H-bh-W*.03-y),4,7,[255,255,255],0,1,0);x.fillStyle=rgb(c.w);x.fillRect(0,H-bh,W,bh);x.textAlign='center';x.fillStyle='#fff';x.textBaseline='middle';const tt=E.l&&E.c?E.c:o.title||'',tf=fit(x,tt,W*.86,W*.055,800,FN);x.font=`800 ${tf}px ${FN}`;x.fillText(tt,W/2,H-bh*.6);if(E.foot){const g=fit(x,E.foot,W*.8,W*.026,500,FN);x.font=`500 ${g}px ${FN}`;x.fillStyle=rgb(c.u);x.fillText(E.foot,W/2,H-bh*.22)}},
// 12 Comic
(x,o,i,n,W,H,R,p,E)=>{const c=cw(o,{a:[255,233,77],b:[255,233,77],t:[17,17,17],u:[215,38,61],v:[255,255,255],w:[30,70,200]}),s=Math.min(W*.13,H*.1),m=W*.07;gbg(x,W,H,c.a,c.b,0);x.fillStyle='#0002';for(let gx=0;gx<9;gx++)for(let gy=0;gy<7;gy++){x.beginPath();x.arc(W-gx*34-20,gy*34+24,Math.max(2,15-gx*1.6-gy*.4),0,7);x.fill()}let y=ttl(x,E,W,s,H*.03,c.t,c.u,1);if(E.sub){const h=pill(x,E.sub.toUpperCase(),0,y+W*.05,W*.026,c.v,c.t,m,6);y+=W*.05+h/2}const bt=H-W*.26,top=y+W*.04,ph_=Math.max(240,bt-top);x.fillStyle='#111';x.beginPath();x.roundRect(m+14,top+14,W*.86,ph_,8);x.fill();ph(x,o,m,top,W*.86,ph_,8,10,[17,17,17],0,0,0);const a=E.foot||'',b=E.l&&E.c?E.c:o.title||'';if(a)pill(x,a.toUpperCase(),W/2,H-W*.17,W*.028,c.u,[255,255,255],null,6);if(b)pill(x,b.toUpperCase(),W/2,H-W*.075,W*.028,c.w,[255,255,255],null,6)}
];
function mk(i){"""
rep("function mk(i){",NS)
rep("if(S.style==0){cover(x,o,0,0,W,H);","if(S.style>6)NS[S.style-7](x,o,i,n,W,H,R,p,hd(o,i,n));else if(S.style==0){cover(x,o,0,0,W,H);")
rep("function render(){const b=$('#slides');","function render(){pred();const b=$('#slides');")
rep("$('#styles').onclick=","$('#stylebox').onclick=")
rep("querySelectorAll('#styles [data-s]')","querySelectorAll('#stylebox [data-s]')")

# ---------- JS: compartir ----------
rep("$('#dl').onclick=async()=>{for(const f of await exp()){const a=document.createElement('a');a.href=URL.createObjectURL(f);a.download=f.name;a.click();await new Promise(r=>setTimeout(r,250))}};",
"async function dlF(fs){for(const f of fs){const a=document.createElement('a');a.href=URL.createObjectURL(f);a.download=f.name;a.click();await new Promise(r=>setTimeout(r,250))}}$('#dl').onclick=async()=>dlF(await exp());")

TAIL=r"""function pred(){const mt=mainTp(),tx=$('#ctx').value+' '+S.items.map(o=>o.note||'').join(' '),k=kws(tx).slice(0,8),have=norm(tx),
sg=[...new Set([...Object.keys(VOC).filter(w=>VOC[w]==mt),...kws(TOP[mt].ph.join(' ')),...TOP[mt].tg.map(h=>norm(h.slice(1))),'feria de ciencias','trabajo en equipo','estudiantes','docentes','familias','primera vez','muestra'])].filter(w=>!have.includes(norm(w))).slice(0,12);
$('#pred').innerHTML=`🔮 Detecté: <b>${esc(TOP[mt].n)}</b>${k.length?' · palabras clave: '+esc(k.join(', ')):''}`;$('#sugs').innerHTML=sg.map(w=>`<button data-w="${esc(w)}">+ ${esc(w)}</button>`).join('')}
const redo=()=>{if(S.items.length){fill(local());list();render();st('Textos base actualizados con tu contexto. Tocá ✨ para mejorarlos con IA.')}};
$('#sugs').onclick=e=>{const w=e.target.dataset.w;if(!w)return;const c=$('#ctx');c.value=(c.value.trim()?c.value.trim().replace(/[.,]$/,'')+', ':'')+w;pred()};
let tm;$('#ctx').oninput=()=>{clearTimeout(tm);tm=setTimeout(pred,200)};$('#ctx').onchange=$('#struct').onchange=redo;
$('#lb').onclick=()=>{const t=$('#topic').value||mainTp(),ws=$('#lw').value.split(',').map(s=>norm(s).trim()).filter(s=>s.length>2);if(!ws.length)return st('Escribí al menos una palabra.');ws.forEach(w=>VOC[w]=t);saveVoc();$('#lw').value='';st('Aprendí '+ws.length+' palabra(s) para «'+TOP[t].n+'».');redo()};
$('#lc').onclick=()=>{VOC={};saveVoc();st('Olvidé lo aprendido.');pred()};
['ev1','ev2','sub','foot','cta','bye'].forEach(k=>$('#'+k).oninput=()=>{clearTimeout(S.tm);S.tm=setTimeout(render,150)});
const SH={ig:['Instagram','https://www.instagram.com/'],fb:['Facebook','https://www.facebook.com/'],wa:['WhatsApp',t=>'https://wa.me/?text='+encodeURIComponent(t)],tg:['Telegram',t=>'https://t.me/share/url?url=%20&text='+encodeURIComponent(t)],x:['X',t=>'https://twitter.com/intent/tweet?text='+encodeURIComponent(t.slice(0,270))],th:['Threads',t=>'https://www.threads.net/intent/post?text='+encodeURIComponent(t.slice(0,480))]};
$('#shr').onclick=async e=>{const k=e.target.dataset.n;if(!k)return;if(!S.items.length)return st('Primero subí fotos o videos.');const[nm,u]=SH[k],cap=$('#cap').value,txt=typeof u=='function';
if(navigator.clipboard)navigator.clipboard.writeText(cap).catch(()=>{});if(txt)open(u(cap),'_blank','noopener');
const f=await exp();if(!txt&&navigator.canShare&&navigator.canShare({files:f})){navigator.share({files:f,text:cap}).catch(()=>{});return st('Elegí '+nm+' en el menú de compartir. El texto también quedó copiado.')}
await dlF(f);if(txt)st('Imágenes descargadas: adjuntalas en '+nm+'. El texto también quedó copiado.');else $('#st').innerHTML='Imágenes descargadas y texto copiado ✔ <a href="'+u+'" target="_blank" rel="noopener">Abrir '+nm+'</a> y subilas desde tu galería.'};
sbuild();render();
</script>"""
rep("sbuild();render();\n</script>",TAIL)
open('/mnt/user-data/outputs/index.html','w',encoding='utf-8').write(src)
sw=open('/mnt/user-data/uploads/sw.js').read().replace('igstudio-v3','igstudio-v4')
open('/mnt/user-data/outputs/sw.js','w').write(sw)
print(len(src))
