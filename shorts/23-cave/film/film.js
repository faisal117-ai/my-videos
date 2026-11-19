const VL=[[0.8, 5.747], [6.147, 9.538], [9.938, 19.133], [19.533, 27.144], [27.544, 30.163], [31.563, 33.526], [33.926, 38.313], [38.713, 41.604], [42.004, 48.299], [48.699, 51.457], [53.057, 57.028], [58.028, 64.705], [65.105, 73.035]],DUR=74.23,SPK={"m1": [[20.514, 27.144], [27.544, 30.163]], "m2": [[34.928, 38.313]], "m3": [[42.993, 48.299], [48.699, 51.457]]},EN=["Three men, trapped in a cave…", "No one knew they were there. How did they get out?", "“Only a deed done for Allah alone can save us now.”", "“I never let anyone drink before my old parents… I held their milk until dawn.”", "“If I did that for You… move this rock.”", "The rock moved… a little.", "“I left a sin, only out of fear of You.”", "It moved again… still not enough.", "“I grew a worker’s forgotten wage into a whole herd… and gave him all of it.”", "“If I did that for You… move this rock.”", "The rock rolled away… into the light.", "A good deed no one sees… Allah sees. Do one today, only for Him.", "Watch the full movies of Prophet Musa (AS) and Prophet Yusuf (AS), links below."],UR=["تین آدمی، ایک غار میں قید…", "کسی کو خبر نہ تھی کہ وہ وہاں ہیں۔ وہ باہر کیسے نکلے؟", "صرف وہ عمل ہمیں بچا سکتا ہے جو خالص اللہ کے لیے کیا ہو", "میں نے کبھی اپنے بوڑھے والدین سے پہلے کسی کو دودھ نہ پلایا… صبح تک دودھ لیے کھڑا رہا", "اگر میں نے یہ تیرے لیے کیا… تو یہ پتھر ہٹا دے", "پتھر تھوڑا سا ہٹا…", "میں نے صرف تیرے ڈر سے ایک گناہ چھوڑ دیا", "پتھر پھر ہٹا… مگر ابھی بھی راستہ نہ بنا", "میں نے ایک مزدور کی رہ جانے والی مزدوری کو پورا ریوڑ بنا دیا… اور سب اسے دے دیا", "اگر میں نے یہ تیرے لیے کیا… تو یہ پتھر ہٹا دے", "پتھر لڑھک گیا… اور وہ روشنی میں نکل آئے", "وہ نیکی جو کوئی نہیں دیکھتا… اللہ دیکھتا ہے۔ آج ایک نیکی صرف اسی کے لیے کریں", "حضرت موسیٰؑ اور حضرت یوسفؑ کی مکمل فلمیں دیکھیں، لنک نیچے"];
// Haq Stories: the three men in the cave (Sahih al-Bukhari 2272). Vertical 1080x1920.
// One world, four places side by side: A cave (x 0..2400), B parents' room (BX), C pasture (CX), D outside the cave (DX).
// Only ordinary men are shown. No prophet, no angel. Captions in English and Urdu.
const T=i=>VL[i][0], TE=i=>VL[i][1];
const BX=6000, CX=12000, DX=18000, FLOOR=1500;
const CUT=[0,T(1)-.15,T(2)-.15,T(3)-.15,T(4)-.15,T(6)-.15,T(7)-.15,T(8)-.15,T(9)-.15,T(10)-.15,T(10)+2.1,T(11)-.15,T(12)-.15,DUR].map(v=>Math.round(v*30));
const SC=['A','A','A','B','A','A','A','C','A','A','D','D','D'];
const R1=T(5)-.95, R2=T(7)-.55, R3=T(10)-.35;
const rockOpen=t=>.11*ease(seg(t,R1,R1+.7))+.13*ease(seg(t,R2,R2+.6))+.76*easeIO(seg(t,R3,R3+1.9));
const rockDrop=t=>{const u=seg(t,.9,1.45);return u<1?-2700*(1-u*u):-18*Math.sin(seg(t,1.45,1.75)*Math.PI)};
const shake=t=>{const k=(a)=>Math.max(0,1-(t-a)/.5)*(t>a?1:0);return (k(1.45)*18+k(R1+.2)*7+k(R2+.2)*8+k(R3+.3)*12)*Math.sin(t*61)};
const inLight=t=>Math.max(1-ease(seg(t,1.0,1.5)),rockOpen(t));

// ---------- A: the cave ----------
const rockPts=(()=>{const r=rng(31),a=[];for(let i=0;i<18;i++){const ang=i/18*Math.PI*2,rad=400*(0.86+r()*.22);a.push([Math.cos(ang)*rad,Math.sin(ang)*rad*1.08])}return a})();
function drawCave(x,t){const o=rockOpen(t),li=inLight(t);
 // light outside the mouth
 let g=x.createLinearGradient(0,600,0,1500);g.addColorStop(0,'#FFD79A');g.addColorStop(1,'#F3A35F');x.fillStyle=g;x.beginPath();x.ellipse(1720,1080,300,430,0,0,7);x.fill();
 // rock walls
 x.fillStyle='#2B1B25';x.beginPath();x.rect(-3000,-2500,8000,7000);x.ellipse(1720,1080,300,430,0,0,7,true);x.fill('evenodd');
 x.fillStyle='#382330';x.beginPath();x.moveTo(-3000,-2500);x.lineTo(5000,-2500);x.lineTo(5000,420);x.quadraticCurveTo(1700,560,900,470);x.quadraticCurveTo(300,420,-3000,560);x.closePath();x.fill();
 x.fillStyle='#24161F';x.beginPath();x.moveTo(-800,900);x.quadraticCurveTo(-200,820,200,980);x.lineTo(200,1600);x.lineTo(-800,1600);x.fill();
 x.fillStyle='#3F2733';x.beginPath();x.moveTo(1360,520);x.quadraticCurveTo(1460,700,1410,1080);x.quadraticCurveTo(1390,1350,1460,1520);x.lineTo(1330,1520);x.quadraticCurveTo(1260,1100,1360,520);x.fill();
 // floor
 x.fillStyle='#21141B';x.fillRect(-3000,FLOOR,8000,3000);
 // light beam through the gap, grows as the rock moves
 if(li>0.005){const a=.06+.30*li;x.save();const bg=x.createLinearGradient(1500,1000,200,1600);bg.addColorStop(0,`rgba(255,205,140,${a})`);bg.addColorStop(1,'rgba(255,205,140,0)');x.fillStyle=bg;
  x.beginPath();x.moveTo(1450,700+300*(1-li));x.lineTo(1470,1480);x.lineTo(-200,1640);x.lineTo(200,1100+300*(1-li));x.closePath();x.fill();x.restore()}
 // the rock
 const rx=1720+o*820,ry=1100+rockDrop(t);x.save();x.translate(rx,ry);x.rotate(o*1.6);x.fillStyle='#5E4C48';x.beginPath();rockPts.forEach((p,i)=>i?x.lineTo(p[0],p[1]):x.moveTo(p[0],p[1]));x.closePath();x.fill();
 x.fillStyle='rgba(0,0,0,.22)';x.beginPath();x.moveTo(-60,-380);x.quadraticCurveTo(260,-160,240,300);x.quadraticCurveTo(120,380,-120,400);x.quadraticCurveTo(160,100,-60,-380);x.fill();
 x.strokeStyle='rgba(255,210,160,.18)';x.lineWidth=10;x.beginPath();x.moveTo(-300,-230);x.quadraticCurveTo(-120,-370,120,-360);x.stroke();x.restore()}
function caveLedge(x){x.fillStyle='#170D13';x.beginPath();x.moveTo(-3000,1470);x.quadraticCurveTo(200,1420,700,1460);x.quadraticCurveTo(1100,1490,1500,1450);x.quadraticCurveTo(1800,1430,5000,1470);x.lineTo(5000,4500);x.lineTo(-3000,4500);x.closePath();x.fill()}
const SEAT={m1:[380,1],m2:[800,1],m3:[1220,-1]};
function seated(t,ch,id,spk,opts={}){const [sx,f]=SEAT[id],s=.9,shot=shotOf(t);let face=(id=='m3'&&shot>=9)?1:f;
 const look=(t>R3-.2||(t>1.4&&t<4))?.9*face:(opts.look??0);
 const p={x:sx,y:1490-235*s,s,face,noLegs:true,breath:t*1.9+sx,time:t,blink:blinkAt(t,[1.3+sx/900,4.1+sx/700,9.6,14.2+sx/600,22.7,31.1,39.8,48.6,57.2]),
  look,lookY:opts.lookY??.15,sad:t<R3?.55:.05,brow:t<R3?.4:.2,mouth:t<R3?-.2:.7,open:spk?talk(t,spk[0],spk[1],9):0,tilt:opts.tilt||0,hands:{},showH:{},tuck:{}};
 if(opts.dua){const d=ease(seg(t,opts.dua[0],opts.dua[0]+.6))*(1-ease(seg(t,opts.dua[1],opts.dua[1]+.5)));if(d>0){p.hands.l=[lerp(-80,-28,d)*1,lerp(205,120,d)];p.hands.r=[lerp(80,28,d),lerp(205,120,d)];p.showH={l:d>.3,r:d>.3};p.lookY=lerp(p.lookY,-.35,d)}}
 return p}
function shotOf(t){const f=Math.round(t*30);let s=0;for(let i=0;i<CUT.length-1;i++)if(f>=CUT[i])s=i;return s}

// ---------- B: the parents' room at night, turning to dawn ----------
function drawRoomB(x,t){const d=ease(seg(t,T(3),TE(3)));const wall=`rgb(${lerp(44,112,d)|0},${lerp(36,74,d)|0},${lerp(64,58,d)|0})`;
 x.fillStyle=wall;x.fillRect(BX-2500,-2500,6000,7000);
 const wg=x.createLinearGradient(0,760,0,1120);wg.addColorStop(0,d>.5?'#FFC98A':'#1E2A55');wg.addColorStop(1,d>.5?'#F59A5E':'#3B3F7A');x.fillStyle=wg;x.fillRect(BX+980,760,240,330);
 x.fillStyle=`rgb(${lerp(70,120,d)|0},${lerp(50,80,d)|0},${lerp(60,60,d)|0})`;x.fillRect(BX+1100-6,760,12,330);x.fillRect(BX+980,920,240,10);
 x.fillStyle='#2A1C1A';x.fillRect(BX-2500,FLOOR,6000,3000);
 // oil lamp on a ledge (flame shape, not a ball)
 x.fillStyle='#4A3328';x.fillRect(BX+40,1250,170,22);x.fillStyle='#8C6A3E';x.beginPath();x.ellipse(BX+125,1238,46,16,0,0,7);x.fill();
 const fl=1+.08*Math.sin(t*13);x.fillStyle=`rgba(255,196,110,${lerp(.95,.4,d)})`;x.beginPath();x.moveTo(BX+125,1190-18*fl);x.quadraticCurveTo(BX+142,1215,BX+125,1228);x.quadraticCurveTo(BX+108,1215,BX+125,1190-18*fl);x.fill();
 x.save();x.globalCompositeOperation='lighter';const lg=x.createRadialGradient(BX+125,1210,10,BX+125,1210,520);lg.addColorStop(0,`rgba(255,170,90,${lerp(.28,.08,d)})`);lg.addColorStop(1,'rgba(255,170,90,0)');x.fillStyle=lg;x.fillRect(BX-500,700,1300,1000);x.restore()}
function cushion(x){x.fillStyle='#5B3A34';x.beginPath();x.roundRect(BX+190,1400,560,140,40);x.fill();x.fillStyle='#4A2E2A';x.fillRect(BX-2500,1520,6000,3000)}
function elder(t,ch,ex,tilt){const s=.6;return {x:ex,y:1440-235*s,s,face:1,noLegs:true,breath:t*1.2+ex,time:t,blink:1,tilt,headY:16,sad:.2,mouth:.2,look:.2,lookY:.6}}
function son(t){const s=.6,p={x:BX+960,y:standY(FLOOR,s),s,face:-1,breath:t*2,time:t,blink:blinkAt(t,[T(3)+2.4,T(3)+6.1]),look:-.8,lookY:.55,sad:.35,brow:.4,mouth:.4,
  hands:{l:[-112,128],r:[-34,132]},showH:{l:true,r:true},tuck:{l:true,r:true},headY:kf(t,[[T(3),0],[TE(3),10]])};return p}
function bowl(x,c,s){x.save();x.translate(c[0],c[1]);x.scale(s,s);x.fillStyle='#C9A077';x.beginPath();x.moveTo(-74,-6);x.quadraticCurveTo(0,86,74,-6);x.closePath();x.fill();x.fillStyle='#F7F1E4';x.beginPath();x.ellipse(0,-6,72,14,0,0,7);x.fill();x.restore()}

// ---------- C: the pasture, the herd grows ----------
const HERD=(()=>{const r=rng(77),a=[];for(let i=0;i<18;i++)a.push({x:CX+520+r()*1150,y:1450+r()*130,s:.55+r()*.3,camel:r()<.3,f:r()<.5?1:-1,ph:r()*6});return a.sort((p,q)=>p.y-q.y)})();
function sheep(x,a,t){const b=Math.sin(t*2+a.ph)*3;x.save();x.translate(a.x,a.y);x.scale(a.s*a.f,a.s);x.fillStyle='#3A2E2A';for(const lx of [-40,-15,18,42])x.fillRect(lx,-30,10,70);x.fillStyle='#F2EADA';x.beginPath();x.ellipse(0,-70+b,82,52,0,0,7);x.fill();x.fillStyle='#3A2E2A';x.beginPath();x.ellipse(82,-92+b,26,20,.3,0,7);x.fill();x.restore()}
function camel(x,a,t){const b=Math.sin(t*1.6+a.ph)*3;x.save();x.translate(a.x,a.y);x.scale(a.s*a.f,a.s);x.fillStyle='#8A6740';for(const lx of [-70,-40,40,70])x.fillRect(lx,-120,14,160);x.fillStyle='#C49A63';x.beginPath();x.moveTo(-110,-120);x.quadraticCurveTo(-90,-260+b,-10,-200);x.quadraticCurveTo(30,-290+b,90,-140);x.lineTo(150,-210);x.lineTo(185,-300+b);x.lineTo(225,-290+b);x.lineTo(200,-260);x.lineTo(130,-120);x.quadraticCurveTo(0,-90,-110,-120);x.fill();x.restore()}
function drawPasture(x,t){const g=x.createLinearGradient(0,0,0,1500);g.addColorStop(0,'#7FB2D9');g.addColorStop(1,'#F6D9A6');x.fillStyle=g;x.fillRect(CX-2500,-2500,6000,4100);
 x.fillStyle='#B99A6A';x.beginPath();x.moveTo(CX-2500,1300);x.quadraticCurveTo(CX+200,1180,CX+900,1290);x.quadraticCurveTo(CX+1500,1360,CX+2400,1250);x.lineTo(CX+3500,1250);x.lineTo(CX+3500,1600);x.lineTo(CX-2500,1600);x.fill();
 x.fillStyle='#8E8A4E';x.fillRect(CX-2500,1520,6000,3000);
 const n=Math.round(lerp(2,18,ease(seg(t,T(8)+.4,T(8)+5.2))));for(let i=0;i<n;i++){const a=HERD[i];(a.camel?camel:sheep)(x,a,t)}}
const workerW=makeWalk({pts:[[CX+1500,1540],[CX+760,1540]],t0:T(8)+.3,t1:T(8)+3.6,steps:6,s:.55});
function owner(t){const s=.55,g=ease(seg(t,T(8)+3.8,T(8)+4.6)),p={x:CX+260,y:standY(1540,s),s,face:1,breath:t*2,time:t,blink:blinkAt(t,[T(8)+1.2,T(8)+5]),look:.8,lookY:.1,mouth:.6,open:talk(t,SPK.m3[0][0],SPK.m3[0][1],9),sad:0,brow:.3,hands:{},showH:{}};
 if(g>0){p.hands.r=[lerp(100,190,g),lerp(205,95,g)];p.showH.r=g>.4}return p}
function worker(t){const w=workerW.at(t),p={x:w.c[0],y:standY(w.c[1],w.s),s:w.s,face:-1,breath:t*2,time:t,blink:blinkAt(t,[T(8)+4.4]),look:-.6,lookY:.1,mouth:kf(t,[[T(8)+3.8,.1],[T(8)+4.6,.8]]),open:kf(t,[[T(8)+4,0],[T(8)+4.6,.5],[T(8)+6,.3]])*0,brow:.5};return walkPose(p,w)}

// ---------- D: outside the cave at sunrise ----------
const outW=[0,1,2].map(i=>makeWalk({pts:[[DX+520,1560],[DX+1080+i*250,1560]],t0:T(10)+2.3+i*.8,t1:T(10)+6.2+i*.8,steps:7,s:.42}));
function drawOutside(x,t){const g=x.createLinearGradient(0,0,0,1560);g.addColorStop(0,'#3E4C86');g.addColorStop(.55,'#E99A6B');g.addColorStop(1,'#FFD7A1');x.fillStyle=g;x.fillRect(DX-2500,-2500,6000,4100);
 x.save();x.globalCompositeOperation='lighter';const sg=x.createRadialGradient(DX+1500,1450,20,DX+1500,1450,700);sg.addColorStop(0,'rgba(255,220,150,.55)');sg.addColorStop(1,'rgba(255,220,150,0)');x.fillStyle=sg;x.fillRect(DX+600,700,1800,1000);x.restore();
 x.fillStyle='#6B4A44';x.beginPath();x.moveTo(DX-2500,700);x.quadraticCurveTo(DX+200,600,DX+800,900);x.quadraticCurveTo(DX+1000,1200,DX+1050,1560);x.lineTo(DX-2500,1560);x.fill();
 x.fillStyle='#1E1218';x.beginPath();x.ellipse(DX+520,1340,150,230,0,0,7);x.fill();
 x.fillStyle='#7A5A50';x.beginPath();x.ellipse(DX+1180,1420,170,150,.2,0,7);x.fill();
 x.fillStyle='#9C7A5C';x.fillRect(DX-2500,1560,6000,3000)}
function walker(t,i,ch){const w=outW[i].at(t),p={x:w.c[0],y:standY(w.c[1],w.s),s:w.s,face:1,breath:t*2+i,time:t,blink:blinkAt(t,[T(10)+4+i,T(11)+2+i]),look:.6,lookY:-.1,mouth:.8,brow:.2};
 if(t<outW[i].U.length&&0){}return walkPose(p,w)}

// ---------- captions (screen space) ----------
function wrap(x,txt,maxW){const w=txt.split(' '),out=[];let line='';for(const q of w){const tst=line?line+' '+q:q;if(x.measureText(tst).width>maxW&&line){out.push(line);line=q}else line=tst}out.push(line);return out}
function captions(t){const x=ctx;x.setTransform(1,0,0,1,0,0);let i=-1;for(let k=0;k<VL.length;k++){const end=k+1<VL.length?VL[k+1][0]-.1:DUR;if(t>=VL[k][0]-.15&&t<end)i=k}
 x.save();x.fillStyle='rgba(245,234,214,.72)';x.font='700 26px Inter, Arial';x.textAlign='center';x.letterSpacing='8px';x.fillText('HAQ · STORIES',W/2,200);x.restore();
 const sh=x.createLinearGradient(0,0,0,760);sh.addColorStop(0,'rgba(10,5,18,.55)');sh.addColorStop(1,'rgba(10,5,18,0)');x.fillStyle=sh;x.fillRect(0,0,W,760);
 if(i<0)return;const a=clamp((t-VL[i][0]+.15)/.35);x.save();x.globalAlpha=a;x.textAlign='center';
 x.font='600 66px Cg';x.fillStyle='#F7EBD7';x.shadowColor='rgba(0,0,0,.85)';x.shadowBlur=18;const ls=wrap(x,EN[i],940);ls.forEach((l,k)=>x.fillText(l,W/2,300+k*74));
 let y=300+ls.length*74+10;x.shadowBlur=0;x.font='40px Nq';x.direction='rtl';const us=wrap(x,UR[i],900);const bh=us.length*78+24;x.fillStyle='rgba(0,0,0,.38)';x.beginPath();x.roundRect(70,y-14,W-140,bh,18);x.fill();
 x.fillStyle='#FFF3DC';us.forEach((l,k)=>x.fillText(l,W/2,y+52+k*78));x.direction='ltr';y+=bh+30;
 if(i>=2&&i<=10){x.font='700 26px Inter, Arial';x.letterSpacing='4px';x.strokeStyle='#F2B04A';x.lineWidth=3;x.fillStyle='rgba(0,0,0,.35)';const txt='SAHIH AL-BUKHARI 2272',w=x.measureText(txt).width+50;x.beginPath();x.roundRect(W/2-w/2,y,w,52,26);x.fill();x.stroke();x.fillStyle='#F2B04A';x.fillText(txt,W/2,y+35)}
 if(i==12){x.font='700 36px Inter, Arial';x.letterSpacing='2px';const txt='Full movies ↓',w=x.measureText(txt).width+80;x.fillStyle='#F2B04A';x.beginPath();x.roundRect(W/2-w/2,y,w,74,37);x.fill();x.fillStyle='#120B08';x.fillText(txt,W/2,y+50)}
 x.restore()}

// ---------- cameras: one per shot ----------
FILM={dur:DUR,cuts:CUT,fadeIn:.4,fadeOut:.8,
 cam(s,u,t){const sk=shake(t);const C=[
  {x:900+sk,y:lerp(840,820,ease(u)),z:lerp(.58,.62,u)},
  {x:lerp(760,840,u)+sk,y:1110,z:lerp(1.25,1.4,ease(u))},
  {x:800,y:960,z:lerp(.92,1.0,u)},
  {x:lerp(BX+560,BX+640,u),y:860,z:lerp(.78,.84,u)},
  {x:lerp(420,950,ease(seg(u,.5,1)))+sk,y:lerp(1100,900,ease(seg(u,.5,1))),z:lerp(1.35,.8,ease(seg(u,.5,1)))},
  {x:800+sk,y:1110,z:lerp(1.4,1.5,u)},
  {x:lerp(1250,1420,u)+sk,y:900,z:lerp(.82,.76,u)},
  {x:lerp(CX+760,CX+900,u),y:820,z:lerp(.52,.56,u)},
  {x:1220+sk,y:1110,z:lerp(1.4,1.5,u)},
  {x:lerp(1000,1350,ease(u))+sk,y:lerp(880,800,ease(u)),z:lerp(.68,.55,ease(u))},
  {x:lerp(DX+700,DX+900,u),y:930,z:lerp(.64,.6,u)},
  {x:lerp(DX+900,DX+1000,u),y:870,z:lerp(.56,.5,u)},
  {x:DX+1000,y:850,z:lerp(.5,.47,u)}];
  const c=C[s];c.b=[0,0,0];return c},
 warm(t){const s=shotOf(t);return s>=10?1:s==3?ease(seg(t,T(3),TE(3)))*.6:s==7?.5:clamp(rockOpen(t)*1.2)},
 draw(t,cam,s){const sc=SC[s];let bg=layer('bg',cam),a=layer('act',cam),fg=layer('fg',cam);
  if(sc=='A'){drawCave(bg,t);const dark=.62-.5*inLight(t);
   const d1=(s==4)?[T(4)-.1,TE(4)+.4]:null,d2=(s==5)?[T(6),TE(6)]:null,d3=(s==8)?[T(9)-.1,TE(9)+.6]:null;
   actor(a,'m1',MAN1,seated(t,MAN1,'m1',s==4?SPK.m1[1]:null,{dua:d1,look:s==2?.5:0}),cam,'rgba(255,190,130,1)',1);
   actor(a,'m2',MAN2,seated(t,MAN2,'m2',s==5?SPK.m2[0]:null,{dua:d2,look:s==2?.6:0}),cam,'rgba(255,190,130,1)',1);
   actor(a,'m3',MAN3,seated(t,MAN3,'m3',s==8?SPK.m3[1]:null,{dua:d3,look:s==2?-.6:-.2}),cam,'rgba(255,190,130,1)',1);
   caveLedge(fg);comp([['bg',1.5],['act',0],['fg',2]]);ctx.setTransform(1,0,0,1,0,0);ctx.fillStyle=`rgba(8,4,14,${clamp(dark)})`;ctx.fillRect(0,0,W,H)}
  else if(sc=='B'){drawRoomB(bg,t);actor(a,'e1',ELDER1,elder(t,ELDER1,BX+330,.22),cam,'rgba(255,170,110,1)',-1);actor(a,'e2',ELDER2,elder(t,ELDER2,BX+600,.18),cam,'rgba(255,170,110,1)',-1);
   cushion(fg);const sp=actor(a,'son',MAN1,son(t),cam,'rgba(255,190,130,1)',-1);const hl=h2w(sp,'l'),hr=h2w(sp,'r');bowl(a,[(hl[0]+hr[0])/2,(hl[1]+hr[1])/2-6],.6);
   comp([['bg',1],['fg',1],['act',0]])}
  else if(sc=='C'){drawPasture(bg,t);actor(a,'owner',MAN3,owner(t),cam);actor(a,'worker',WORKER,worker(t),cam);softShadow(bg,CX+260,1545,70,10);comp([['bg',1],['act',0]])}
  else{drawOutside(bg,t);[MAN1,MAN2,MAN3].forEach((ch,i)=>{const p=walker(t,i,ch);softShadow(a,p.x,1563,60,9);actor(a,'w'+i,ch,p,cam)});comp([['bg',1],['act',0]])}
  captions(t)},
 plants(){return {worker:workerW.plants(),w0:outW[0].plants(),w1:outW[1].plants(),w2:outW[2].plants()}}};
say(1.45,'rockfall');say(R1+.15,'rockmove');say(R2+.15,'rockmove');say(R3+.2,'rockroll');
for(const tt of [T(1)+.2,T(1)+1.0,T(1)+1.8,T(1)+2.6])say(tt,'heart');for(const tt of [R1-.8,R2-.6,R3-1.0,R3-.4])say(tt,'heart');
