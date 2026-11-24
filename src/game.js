{
/* ================= LANGUAGE =================
   Every string is written as a Slovenian/English pair: tr('…','…'). */
let LANG='sl';
const tr=(sl,en)=>LANG==='en'?en:sl;
const LOC=()=>LANG==='en'?'en-GB':'sl-SI';

/* ================= DATA ================= */
const RAW=/*DATA*/;
const MAPS=/*MAPS*/;
const O=RAW.map(([n,p,a,y,r,u])=>({n,p,a,y,r,u}));
/* key, Slovenian name, English name, map glyph */
const REG=[['Gorenjska','Gorenjska','Gorenjska','^'],['Goriška','Goriška','Goriška','%'],['Obalno-kraška','Obalno-kraška','Coastal-Karst','='],
 ['Primorsko-notran.','Primorsko-notranjska','Littoral-Inner Carniola','&'],['Osrednjeslovenska','Osrednjeslovenska','Central Slovenia','#'],['Zasavska','Zasavska','Central Sava','*'],
 ['Savinjska','Savinjska','Savinjska','+'],['Koroška','Koroška','Carinthia','Y'],['Podravska','Podravska','Drava','v'],['Pomurska','Pomurska','Mura','-'],
 ['Posavska','Posavska','Lower Sava','x'],['Jugovzhodna','Jugovzhodna Slovenija','Southeast Slovenia','T']];
const RI=Object.fromEntries(REG.map((r,i)=>[r[0],i]));O.forEach(o=>o.r=RI[o.r]);
const rname=i=>tr(REG[i][1],REG[i][2]);
const RN=REG.map((_,i)=>O.filter(o=>o.r===i).length);
const IDX=Object.fromEntries(O.map((o,i)=>[o.n,i]));
const TOTAL=O.reduce((s,o)=>s+o.p,0);
/* name sl, name en, base cost, base income, občine needed, plural sl, plural en */
const GEN=[['Njiva','Field',15,.1,0,'njive','fields'],['Kozolec','Hayrack',100,1,2,'kozolci','hayracks'],['Čebelnjak','Apiary',1100,8,8,'čebelnjaki','apiaries'],
 ['Gostilna','Inn',12e3,47,18,'gostilne','inns'],['Vinska klet','Wine cellar',130e3,260,30,'vinske kleti','wine cellars'],['Žaga','Sawmill',1.4e6,1400,45,'žage','sawmills'],
 ['Rudnik','Mine',20e6,7800,62,'rudniki','mines'],['Toplice','Spa',330e6,44e3,80,'toplice','spas'],['Smučišče','Ski resort',5.1e9,260e3,100,'smučišča','ski resorts'],
 ['Tovarna','Factory',75e9,1.6e6,125,'tovarne','factories'],['Pristanišče','Port',1e12,10e6,150,'pristanišča','ports'],['Elektrarna','Power plant',14e12,65e6,175,'elektrarne','power plants']];
const gname=k=>tr(GEN[k][0],GEN[k][1]);const gpl=k=>tr(GEN[k][5],GEN[k][6]);const gcostBase=k=>GEN[k][2];const gprod=k=>GEN[k][3];const greq=k=>GEN[k][4];
const TIERS=[[10,10,'boljše orodje','better tools'],[25,100,'zadruga','cooperative'],[50,1e4,'evropska sredstva','EU funds'],[100,1e6,'digitalizacija','digitalisation'],
 [150,1e8,'zelena preobrazba','green transition'],[200,1e10,'pametna specializacija','smart specialisation']];
const LM=[['Solčava','Logarska dolina','Logar Valley','gen',0,2],['Kostel','Grad Kostel','Kostel Castle','click',0,2],['Šentrupert','Dežela kozolcev','Land of Hayracks','gen',1,3],
 ['Bovec','Rafting na Soči','Rafting on the Soča','gen',3,2],['Ankaran','Najmlajša občina','Youngest municipality','glob',0,1.1],['Mežica','Podzemlje Pece','Underground Peca','gen',6,2],
 ['Kobarid','Hiša Franko','Hiša Franko','gen',3,3],['Žirovnica','Anton Janša','Anton Janša','gen',2,3],['Radenci','Radenska','Radenska','gen',7,2],['Kranjska Gora','Planica','Planica','gen',8,2],
 ['Žiri','Žirovski čevlji','Žiri shoes','pct',0,.01],['Bohinj','Triglavski narodni park','Triglav National Park','glob',0,1.15],['Brda','Briška rebula','Brda Rebula','gen',4,3],
 ['Vipava','Vipavski zelen','Vipava Zelen','gen',4,2],['Moravske Toplice','Prekmurske terme','Prekmurje spas','gen',7,2],['Cerklje na Gorenjskem','Krvavec','Krvavec','gen',8,2],
 ['Bled','Blejska kremšnita','Bled cream cake','gen',3,2],['Metlika','Metliška črnina','Metlika red wine','gen',4,2],['Ribnica','Suha roba','Woodenware','gen',5,3],
 ['Lendava','Nafta Lendava','Lendava oil','gen',6,2],['Idrija','Rudnik živega srebra','Mercury mine','gen',6,3],['Rogaška Slatina','Slatina','Mineral springs','gen',7,3],
 ['Ormož','Jeruzalem','Jeruzalem','gen',4,2],['Laško','Laško pivo','Laško beer','gen',3,2],['Sežana','Kobilarna Lipica','Lipica Stud Farm','pct',0,.02],
 ['Kočevje','Kočevski pragozd','Kočevje virgin forest','gen',5,2],['Trbovlje','Rudarska tradicija','Mining tradition','gen',6,2],['Izola','Ribiško pristanišče','Fishing harbour','gen',10,2],
 ['Postojna','Postojnska jama','Postojna Cave','glob',0,1.25],['Piran','Sečoveljske soline','Sečovlje salt pans','gen',10,2],['Murska Sobota','Prekmurska gibanica','Prekmurje layer cake','gen',0,5],
 ['Radovljica','Čebelarski muzej','Beekeeping museum','gen',2,2],['Škofja Loka','Škofjeloški pasijon','Škofja Loka Passion','glob',0,1.1],['Ptuj','Kurentovanje','Kurentovanje','kur',0,1],
 ['Krško','Jedrska elektrarna','Nuclear power plant','gen',11,3],['Kamnik','Velika planina','Velika planina','gen',8,2],['Nova Gorica','Trg Evrope','Europe Square','glob',0,1.1],
 ['Velenje','Gospodinjski aparati','Home appliances','gen',9,2],['Novo mesto','Avtomobili in zdravila','Cars and medicines','gen',9,3],['Celje','Celjski grofje','Counts of Celje','glob',0,1.25],
 ['Koper','Luka Koper','Port of Koper','gen',10,3],['Kranj','Prešernovo mesto',"Prešeren's town",'pct',0,.03],['Maribor','Stara trta','Old Vine','gen',4,3],['Ljubljana','Prestolnica','The capital','glob',0,2]]
 .map(([o,sl,en,kind,t,v])=>({id:'lm'+IDX[o],o:IDX[o],sl,en,kind,t,v}));
const lname=l=>tr(l.sl,l.en);
const LMAT=Object.fromEntries(LM.map(l=>[l.o,l]));
/* bell upgrades: id, sl, en, clicks needed, cost, click ×, +% of income per click */
const CLK=[['k1','Pritrkavanje','Bell chiming',50,200,2,0],['k2','Bronasti zvon','Bronze bell',500,2e4,2,.01],['k3','Zvonik na hribu','Hilltop belfry',2000,2e7,2,.01],
 ['k4','Veliki zvon','Great bell',6000,2e10,2,.02],['k5','Zvonovi vseh far','Bells of every parish',15000,2e13,2,.02]];
/* constitutional amendments, one chosen at each referendum */
const AM=[['a1','Cenejša proizvodnja','Producer subsidies','proizvodnja je 15 % cenejša','producers cost 15% less'],
 ['a2','Kurentova pravica',"Kurent's right",'kurent pride 2× pogosteje','the Kurent comes twice as often'],
 ['a3','Zakon o lokalni samoupravi','Local Self-Government Act','odklep občin je 20 % cenejši','unlocking municipalities costs 20% less'],
 ['a4','Začetni kapital','Seed capital','vsaka nova igra začne z 10 njivami, 10 kozolci in 5 čebelnjaki','each run starts with 10 fields, 10 hayracks and 5 apiaries'],
 ['a5','Pritrkovalska šola','Bell-chiming school','klik ×5','clicks ×5'],
 ['a6','Regionalni razvoj','Regional development','cela regija da ×1,5 namesto ×1,25','a complete region gives ×1.5 instead of ×1.25'],
 ['a7','Varstvo kulturne dediščine','Heritage protection','znamenitosti so pol cenejše','landmarks cost half'],
 ['a8','Volilna reforma','Electoral reform','vsak glas da +7 % namesto +5 %','each vote gives +7% instead of +5%'],
 ['a9','Zakon o delovnem času','Working Hours Act','med odsotnostjo poln dohodek do 12 h','full income while away, up to 12 h'],
 ['a10','Zvonovi ostanejo','The bells stay','izboljšave zvona ostanejo po referendumu','bell upgrades survive referendums'],
 ['a11','Dan dosežkov','Merit Day','vsak dosežek da +2 % namesto +1 %','each achievement gives +2% instead of +1%'],
 ['a12','Hitri začetek','Fast start','prvih 25 občin je brezplačnih','the first 25 municipalities are free']];
const amName=id=>{const a=AM.find(a=>a[0]===id);return tr(a[1],a[2])};const amDesc=id=>{const a=AM.find(a=>a[0]===id);return tr(a[3],a[4])};
/* seasonal events from the real calendar: [month, day] ranges, wrapping over new year */
const EV=[{id:'pust',sl:'Pust',en:'Carnival',from:[2,1],to:[2,29],dsl:'kurent pride 2× pogosteje',den:'the Kurent comes twice as often',kur:.5},
 {id:'kultura',sl:'Prešernov dan',en:'Prešeren Day',from:[2,8],to:[2,8],dsl:'klik ×3',den:'clicks ×3',click:3},
 {id:'zima',sl:'Smučarska sezona',en:'Ski season',from:[12,1],to:[3,15],dsl:'smučišča ×2',den:'ski resorts ×2',gm:{8:2}},
 {id:'drzava',sl:'Dan državnosti',en:'Statehood Day',from:[6,24],to:[6,26],dsl:'vse ×1,25',den:'everything ×1.25',glob:1.25},
 {id:'poletje',sl:'Turistična sezona',en:'Tourist season',from:[7,1],to:[8,31],dsl:'toplice in pristanišča ×2',den:'spas and ports ×2',gm:{7:2,10:2}},
 {id:'trgatev',sl:'Trgatev',en:'Grape harvest',from:[9,15],to:[10,15],dsl:'vinske kleti ×2',den:'wine cellars ×2',gm:{4:2}},
 {id:'martin',sl:'Martinovanje',en:"St Martin's month",from:[11,1],to:[11,30],dsl:'vinske kleti ×3, gostilne ×2',den:'wine cellars ×3, inns ×2',gm:{4:3,3:2}},
 {id:'bozic',sl:'Božič in novo leto',en:'Christmas and New Year',from:[12,20],to:[1,6],dsl:'klik ×2',den:'clicks ×2',click:2}];
/* the week in a Slovenian village: one bonus per day, so every player meets them all */
const WEEK=[
 {id:'d0',sl:'Nedeljska maša',en:'Sunday mass',dsl:'klik ×3, zvonjenje se polni 2× hitreje',den:'clicks ×3, the ringing meter fills twice as fast',click:3,fill:2},
 {id:'d1',sl:'Tržni dan',en:'Market day',dsl:'njive, kozolci in čebelnjaki ×3',den:'fields, hayracks and apiaries ×3',gm:{0:3,1:3,2:3}},
 {id:'d2',sl:'Obrtni dan',en:'Crafts day',dsl:'žage in rudniki ×2',den:'sawmills and mines ×2',gm:{5:2,6:2}},
 {id:'d3',sl:'Delavnik',en:'Shift day',dsl:'tovarne, pristanišča in elektrarne ×2',den:'factories, ports and power plants ×2',gm:{9:2,10:2,11:2}},
 {id:'d4',sl:'Izletniki',en:'Day trippers',dsl:'toplice in smučišča ×2',den:'spas and ski resorts ×2',gm:{7:2,8:2}},
 {id:'d5',sl:'Petek v gostilni',en:'Friday at the inn',dsl:'gostilne in vinske kleti ×2',den:'inns and wine cellars ×2',gm:{3:2,4:2}},
 {id:'d6',sl:'Gasilska veselica',en:"Firefighters' party",dsl:'vse ×1,1, kurent pogosteje',den:'everything ×1.1, the Kurent comes more often',glob:1.1,kur:.6}];
const PDIV=20000,GROW=1.15;

/* ================= STATE ================= */
const KEY='obcine-v2',VERSION=4;
const fresh=()=>({v:VERSION,sit:15,life:0,all:0,n:0,own:GEN.map(()=>0),ups:[],clicks:0,kur:0,t0:Date.now(),save:Date.now(),votes:0,refs:0,ach:[],achT:{},log:[],won:0,amt:1,sound:1,light:0,
 lang:null,amends:[],first:Date.now(),play:0,mile:[],evSeen:{},days:[]});
/* saves carry a version; each step upgrades an older shape */
function migrate(s){if(!s||!Array.isArray(s.own))return null;const v=s.v||2,first=s.first||s.t0;s=Object.assign(fresh(),s);
 if(v<3){s.first=first||Date.now()}
 /* v4: new unlock prices and the ringing meter; nothing in the save needs converting */
 s.v=VERSION;
 s.own=GEN.map((_,k)=>s.own[k]||0);return s}
let S=fresh();
try{const s=migrate(JSON.parse(localStorage.getItem(KEY)||'null'));if(s)S=s}catch(e){}
LANG=S.lang||'sl';
const has=id=>S.ups.includes(id);
const am=id=>S.amends.includes(id);
let kurUntil=0,clkUntil=0,kurNext=Date.now()+90e3,kurPos=null,kurGone=0,hover=-1,regPage=null,achPage=0,refArm=0,refPick=null,resetArm=0,flash='';

/* ================= CALENDAR ================= */
let evCache={key:'',list:[]};
function eventsNow(){const d=new Date(window.__date||Date.now());const key=d.toDateString();if(key===evCache.key)return evCache.list;
 const md=(d.getMonth()+1)*100+d.getDate();const inR=e=>{const a=e.from[0]*100+e.from[1],b=e.to[0]*100+e.to[1];return a<=b?md>=a&&md<=b:md>=a||md<=b};
 evCache={key,list:[WEEK[d.getDay()],...EV.filter(inR)]};return evCache.list}
const holidaysNow=()=>eventsNow().slice(1);
const evFill=()=>eventsNow().reduce((m,e)=>m*(e.fill||1),1);
const evName=e=>tr(e.sl,e.en),evDesc=e=>tr(e.dsl,e.den);
const evGen=k=>eventsNow().reduce((m,e)=>m*((e.gm&&e.gm[k])||1),1);
const evGlob=()=>eventsNow().reduce((m,e)=>m*(e.glob||1),1);
const evClick=()=>eventsNow().reduce((m,e)=>m*(e.click||1),1);
const evKur=()=>eventsNow().reduce((m,e)=>m*(e.kur||1),1);

/* ================= ECONOMY ================= */
const ocost=i=>am('a12')&&i<25?0:Math.ceil((30*1.15**i*Math.exp(.12*i*(211-i)/211)+200*(i+1)**4)*Math.exp(.18*Math.max(0,i-140))*(am('a3')?.8:1));
const lmcost=l=>ocost(l.o)*3*(am('a7')?.5:1)||Math.ceil((30*1.15**l.o)*3);
function pop(){let p=0;for(let i=0;i<S.n;i++)p+=O[i].p;return p}
function regCount(){const c=REG.map(()=>0);for(let i=0;i<S.n;i++)c[O[i].r]++;return c}
const regsDone=()=>regCount().filter((c,i)=>c===RN[i]).length;
const REGB=()=>am('a6')?1.5:1.25;
const VOTEP=()=>am('a8')?.07:.05;
const ACHP=()=>am('a11')?.02:.01;
function genMult(k){let m=1;TIERS.forEach((t,ti)=>{if(has('t'+k+'_'+ti))m*=2});LM.forEach(l=>{if(l.kind==='gen'&&l.t===k&&has(l.id))m*=l.v});return m*evGen(k)}
const globUp=()=>LM.reduce((m,l)=>l.kind==='glob'&&has(l.id)?m*l.v:m,1);
const popMult=()=>1+pop()/PDIV;
const regMult=()=>REGB()**regsDone();
const achMult=()=>1+ACHP()*S.ach.length;
const voteMult=()=>1+VOTEP()*S.votes;
/* Kurent: comes every 4-8 min, stays 13 s. Catching him gives one of
   ×3 income for 30 s (50 %), a doughnut worth 3 min of income, at most 10 % of your tolars (30 %),
   or clicks ×7 for 10 s (20 %). Ptuj's landmark: he comes 25 % more often and boosts last 1.5× longer.
   An attentive player gains roughly +20-25 % from him overall. */
const KC={every:[240e3,480e3],stay:13e3,mult:3,multS:30e3,krofS:180,krofBank:.1,click:7,clickS:10e3,ptujEvery:.75,ptujLong:1.5};
const kurMult=()=>Date.now()<kurUntil?KC.mult:1;
const allMult=()=>popMult()*regMult()*achMult()*voteMult()*globUp()*evGlob();
const genIps=k=>S.own[k]*gprod(k)*genMult(k)*allMult();
function baseIps(){let s=0;for(let k=0;k<GEN.length;k++)s+=S.own[k]*gprod(k)*genMult(k);return s*allMult()}
/* ringing meter: every ring fills it, it drains once you pause, and it multiplies all income
   up to the current bell's cap (handbell ×1.5 … bells of every parish ×5) */
const METER_CAP=[1.5,2,2.5,3,4,5],FILL=.025,GRACE=5000,DRAIN_S=45;
let meter=0,lastRingT=0;
const meterCap=()=>METER_CAP[bellTier()];
const meterMult=()=>1+meter*(meterCap()-1);
const ips=()=>baseIps()*kurMult()*meterMult();
function clickVal(){let cm=am('a5')?5:1,pct=0;CLK.forEach(c=>{if(has(c[0])){cm*=c[5];pct+=c[6]}});LM.forEach(l=>{if(!has(l.id))return;if(l.kind==='click')cm*=l.v;if(l.kind==='pct')pct+=l.v});
 return (cm*evClick()+pct*baseIps())*(Date.now()<clkUntil?KC.click:1)*kurMult()*meterMult()}
const GD=()=>am('a1')?.85:1;
const gcost=(k,a)=>gcostBase(k)*GD()*GROW**S.own[k]*(GROW**a-1)/(GROW-1);
const gmax=k=>Math.max(0,Math.floor(Math.log(S.sit*(GROW-1)/(gcostBase(k)*GD()*GROW**S.own[k])+1)/Math.log(GROW)));
const votesTotal=()=>Math.floor(Math.cbrt(S.all/1e9));
const votesGain=()=>Math.max(0,votesTotal()-S.votes);
function upgrades(){const L=[];
 GEN.forEach((g,k)=>TIERS.forEach((t,ti)=>{if(S.own[k]>=t[0]&&!has('t'+k+'_'+ti))L.push({id:'t'+k+'_'+ti,name:gname(k)+': '+tr(t[2],t[3]),desc:gpl(k)+' ×2',cost:gcostBase(k)*t[1]})}));
 LM.forEach(l=>{if(l.o<S.n&&!has(l.id))L.push({id:l.id,name:lname(l),desc:lmDesc(l)+' · '+ab(O[l.o].n,16),cost:lmcost(l)})});
 CLK.forEach(c=>{if(S.clicks>=c[3]&&!has(c[0]))L.push({id:c[0],name:tr(c[1],c[2]),desc:tr('klik','clicks')+' ×'+c[5]+(c[6]?', +'+pc(c[6]*100)+tr(' dohodka na klik',' of income per click'):'')+tr(', nov zvok',', new sound'),cost:c[4]})});
 return L.sort((a,b)=>a.cost-b.cost)}
function lmDesc(l){const v=xv(l.v);return l.kind==='gen'?gpl(l.t)+' '+v:l.kind==='glob'?tr('vse ','everything ')+v:l.kind==='click'?tr('klik ','clicks ')+v:l.kind==='pct'?tr('klik +','clicks +')+pc(Math.round(l.v*100))+tr(' dohodka',' of income'):tr('kurent pogosteje, učinki 1,5× dlje','Kurent more often, effects last 1.5× longer')}

/* ================= FORMAT ================= */
function fmt(x,dec){if(!isFinite(x))return '∞';if(x<1e6)return x.toLocaleString(LOC(),{maximumFractionDigits:dec&&x<100?1:0,useGrouping:'always'});
 const sf=LANG==='en'?['M','B','T','Qa','Qi','Sx','Sp','Oc']:['mio','mrd','bil','bld','tril','trld','kvad','kvadd'];let k=Math.floor(Math.log10(x)/3)-2;
 if(Math.round(x/10**(3*k+6)*100)/100>=1000)k++;if(k>=sf.length)return x.toExponential(2).replace('.',LANG==='en'?'.':',');
 return (x/10**(3*k+6)).toLocaleString(LOC(),{minimumFractionDigits:2,maximumFractionDigits:2})+' '+sf[k]}
const num=x=>x.toLocaleString(LOC(),{useGrouping:'always'});
const xv=v=>'×'+v.toLocaleString(LOC(),{maximumFractionDigits:2});
const xf=v=>'×'+v.toLocaleString(LOC(),{minimumFractionDigits:2,maximumFractionDigits:2});
const pc=n=>(typeof n==='number'?n.toLocaleString(LOC(),{maximumFractionDigits:1}):n)+(LANG==='en'?'%':' %');
const dur=s=>{s=Math.max(0,Math.round(s));if(s<60)return s+' s';const m=Math.floor(s/60);if(m<60)return m+' min';const h=Math.floor(m/60);
 return h<48?h+' h '+(m%60)+' min':Math.floor(h/24)+tr(' dni',' days')};
const obc=n=>LANG==='en'?(n===1?'municipality':'municipalities'):n%100===1?'občino':n%100===2?'občini':n%100===3||n%100===4?'občine':'občin';
const MO=()=>tr(' (MO)',' (city)');
const L=s=>[...s].length;
const SHORT=Object.assign({"Sveta Trojica v Slovenskih goricah": ["Sv. Trojica v Slov. goricah", "Sv. Trojica v Sl. gor.", "Sv. Trojica"], "Sveti Andraž v Slovenskih goricah": ["Sv. Andraž v Slov. goricah", "Sv. Andraž v Sl. gor.", "Sv. Andraž"], "Sveti Jurij v Slovenskih goricah": ["Sv. Jurij v Slov. goricah", "Sv. Jurij v Sl. gor.", "Sv. Jurij v S. g."], "Miklavž na Dravskem polju": ["Miklavž na Drav. polju", "Miklavž na D. p.", "Miklavž"], "Sveti Jurij ob Ščavnici": ["Sv. Jurij ob Ščavnici", "Sv. Jurij ob Šč.", "Sv. Jurij o. Š."], "Dobrova-Polhov Gradec": ["Dobrova-Polh. Gradec", "Dobrova-P. G."], "Cerklje na Gorenjskem": ["Cerklje na Gor.", "Cerklje n. G."], "Kostanjevica na Krki": ["Kostanjevica n. K.", "Kostanj. n. K."], "Gorenja vas-Poljane": ["Gor. vas-Poljane", "G. vas-Poljane"], "Slovenska Bistrica": ["Slov. Bistrica", "Sl. Bistrica"], "Šmartno pri Litiji": ["Šmartno pri Lit.", "Šmartno p. L."], "Miren-Kostanjevica": ["Miren-Kostanj.", "Miren-K."], "Lovrenc na Pohorju": ["Lovrenc na Poh.", "Lovrenc n. P."], "Ribnica na Pohorju": ["Ribnica na Poh.", "Ribnica n. P."], "Slovenske Konjice": ["Slov. Konjice", "Sl. Konjice"], "Ravne na Koroškem": ["Ravne na Kor.", "Ravne n. K."], "Šmarje pri Jelšah": ["Šmarje pri J.", "Šmarje p. J."], "Dol pri Ljubljani": ["Dol pri Lj.", "Dol p. Lj."], "Dolenjske Toplice": ["Dol. Toplice", "Dol. Topl."], "Šmarješke Toplice": ["Šmarj. Toplice", "Šm. Toplice"], "Mokronog-Trebelno": ["Mokronog-Treb.", "Mokronog-T."], "Rečica ob Savinji": ["Rečica ob Sav.", "Rečica o. S."], "Središče ob Dravi": ["Središče ob Dr.", "Središče o. D."], "Bistrica ob Sotli": ["Bistrica ob S.", "Bistrica o. S."], "Ilirska Bistrica": ["Il. Bistrica", "Il. Bistr."], "Šempeter-Vrtojba": ["Šempeter-Vrt.", "Šempeter-V."], "Moravske Toplice": ["Mor. Toplice", "Mor. Topl."], "Selnica ob Dravi": ["Selnica ob Dr.", "Selnica o. D."], "Črna na Koroškem": ["Črna na Kor.", "Črna n. K."], "Zagorje ob Savi": ["Zagorje o. S.", "Zagorje"], "Rogaška Slatina": ["Rog. Slatina", "R. Slatina"], "Hrpelje-Kozina": ["Hrpelje-Koz.", "Hrpelje-K."], "Jugovzhodna Slovenija": ["Jugovzhodna Slov.", "Jugovzhodna"], "Primorsko-notranjska": ["Primorsko-notr.", "Prim.-notr."], "Osrednjeslovenska": ["Osrednjeslov.", "Osr.-slov."]},{"Littoral-Inner Carniola":["Littoral-Inner C.","Litt.-Inner C."],"Southeast Slovenia":["SE Slovenia"],"Central Slovenia":["Central Slov."],"Coastal-Karst":["Coastal-K."]});
const SMALLW=new Set(['v','na','ob','pri','pod','nad','in','of','the']);
/* fit a proper name into w characters: full name, then official-style short forms, then initials */
function ab(s,w){if(L(s)<=w)return s;for(const v of SHORT[s]||[])if(L(v)<=w)return v;
 const ws=s.split(' ');for(let i=ws.length-1;i>0;i--){if(SMALLW.has(ws[i])||L(ws[i])<=3)continue;ws[i]=[...ws[i]][0]+'.';const r=ws.join(' ');if(L(r)<=w)return r}
 return cut(ws.join(' '),w)}
const esc=s=>String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
const padR=(s,w)=>s+' '.repeat(Math.max(0,w-L(s)));
const padL=(s,w)=>' '.repeat(Math.max(0,w-L(s)))+s;
const TRUNC=window.__trunc=[];const cut=(s,w)=>{if(L(s)<=w)return s;TRUNC.push(s);return [...s].slice(0,Math.max(0,w-1)).join('')+'~'};
/* wrap a list of items, keeping each item whole when it fits on a line */
function wrapItems(items,sep,w){const out=[];let cur='';for(const it of items){const add=cur?cur+sep+it:it;if(L(add)<=w){cur=add;continue}if(cur)out.push(cur);
 if(L(it)<=w)cur=it;else{const ws=wrap(it,w);out.push(...ws.slice(0,-1));cur=ws[ws.length-1]}}if(cur)out.push(cur);return out}
/* wrap at spaces; never split a number from its unit */
function wrap(s,w){s=s.replace(/(\d) (%|SIT|km²|s\b|min\b|h\b|preb\.|res\.|dni\b|days\b)/g,'$1\u00a0$2').replace(/ ×/g,'\u00a0×');const out=[];let line='';
 for(const word of s.split(' ')){if(L(line)+L(word)+(line?1:0)>w){if(line)out.push(line);line=word}else line=line?line+' '+word:word}
 if(line)out.push(line);return out.map(l=>l.replace(/\u00a0/g,' '))}

/* ================= TEXT UI ENGINE =================
   a "line" is an array of segments: a string, or {t, a:action, c:css class, hid:hidden from screen readers,
   head:heading for screen readers, lab:accessible label, raw:html} */
const sl=g=>L(typeof g==='string'?g:g.t);
function seg(g){if(typeof g==='string')return esc(g);if(g.raw)return g.raw;const t=esc(g.t);
 if(g.a)return `<span class="b${g.c?' '+g.c:''}" data-a="${g.a}"`+(g.hid?' aria-hidden="true"':` role="button" tabindex="0" aria-label="${esc(g.lab||g.t.replace(/[\[\]()]/g,'').trim())}"`)+`>${t}</span>`;
 const at=(g.c?` class="${g.c}"`:'')+(g.hid?' aria-hidden="true"':'')+(g.head?' role="heading" aria-level="2"':'');return at?`<span${at}>${t}</span>`:t}
function fit(line,w){let h='',l=0;for(const g of line){const n=sl(g);if(l+n>w){TRUNC.push(line.map(x=>typeof x==='string'?x:x.t).join(''));if(typeof g==='string'){h+=esc([...g].slice(0,w-l).join(''));l=w}break}h+=seg(g);l+=n}return h+' '.repeat(w-l)}
const btn=(t,a,on=true,lab)=>on?{t:'['+t+']',a,lab}:{t:'('+t.trim().toLowerCase()+')'};
const two=(a,b,w)=>{const la=a.reduce((s,g)=>s+sl(g),0),lb=b.reduce((s,g)=>s+sl(g),0);return [...a,' '.repeat(Math.max(1,w-la-lb)),...b]};
const lr=(a,b,w)=>two([a],[b],w);
const H=t=>({t,hid:true});
function box(title,lines,w,right=[]){const inner=w-4;
 const tl=[H('+-'),{t:'[ ',c:'bold',hid:true},{t:title,c:'bold',head:true},{t:' ]',c:'bold',hid:true}],tr2=[...right,H('-+')];
 const used=tl.reduce((s,g)=>s+sl(g),0)+tr2.reduce((s,g)=>s+sl(g),0);
 let h=fit([...tl,H('-'.repeat(Math.max(0,w-used))),...tr2],w)+'\n';
 for(const ln of lines)h+=seg(H('| '))+fit(Array.isArray(ln)?ln:[ln],inner)+seg(H(' |'))+'\n';
 return h+seg(H('+'+'-'.repeat(w-2)+'+'))}
const bar=(f,w)=>{const k=Math.round(Math.max(0,Math.min(1,f))*w);return '['+'#'.repeat(k)+'.'.repeat(w-k)+']'};

/* ================= BIG DIGITS / BANNERS ================= */
const FIG={big:{"0": ["  ___  ", " / _ \\ ", "| | | |", "| |_| |", " \\___/ ", "       "], "1": [" _ ", "/ |", "| |", "| |", "|_|", "   "], "2": [" ____  ", "|___ \\ ", "  __) |", " / __/ ", "|_____|", "       "], "3": [" _____ ", "|___ / ", "  |_ \\ ", " ___) |", "|____/ ", "       "], "4": [" _  _   ", "| || |  ", "| || |_ ", "|__   _|", "   |_|  ", "        "], "5": [" ____  ", "| ___| ", "|___ \\ ", " ___) |", "|____/ ", "       "], "6": ["  __   ", " / /_  ", "| '_ \\ ", "| (_) |", " \\___/ ", "       "], "7": [" _____ ", "|___  |", "   / / ", "  / /  ", " /_/   ", "       "], "8": ["  ___  ", " ( _ ) ", " / _ \\ ", "| (_) |", " \\___/ ", "       "], "9": ["  ___  ", " / _ \\ ", "| (_) |", " \\__, |", "   /_/ ", "       "], ".": ["   ", "   ", "   ", " _ ", "(_)", "   "], ",": ["   ", "   ", "   ", " _ ", "( )", "|/ "], "-": ["       ", "       ", " _____ ", "|_____|", "       ", "       "], "+": ["       ", "   _   ", " _| |_ ", "|_   _|", "  |_|  ", "       "], "e": ["      ", "  ___ ", " / _ \\", "|  __/", " \\___|", "      "]},small:{"0": ["  __  ", " /  \\ ", "| () |", " \\__/ ", "      "], "1": [" _ ", "/ |", "| |", "|_|", "   "], "2": [" ___ ", "|_  )", " / / ", "/___|", "     "], "3": [" ____", "|__ /", " |_ \\", "|___/", "     "], "4": [" _ _  ", "| | | ", "|_  _|", "  |_| ", "      "], "5": [" ___ ", "| __|", "|__ \\", "|___/", "     "], "6": ["  __ ", " / / ", "/ _ \\", "\\___/", "     "], "7": [" ____ ", "|__  |", "  / / ", " /_/  ", "      "], "8": [" ___ ", "( _ )", "/ _ \\", "\\___/", "     "], "9": [" ___ ", "/ _ \\", "\\_, /", " /_/ ", "     "], ".": ["   ", "   ", " _ ", "(_)", "   "], ",": ["   ", "   ", " _ ", "( )", "|/ "], "-": ["     ", " ___ ", "|___|", "     ", "     "], "+": ["   _   ", " _| |_ ", "|_   _|", "  |_|  ", "       "], "e": ["     ", " ___ ", "/ -_)", "\\___|", "     "]}};
function big(str,f){const F=FIG[f];const h=F['0'].length;const r=Array(h).fill('');for(const ch of [...str]){const g=F[ch];if(!g)continue;for(let i=0;i<h;i++)r[i]+=(r[i]?' ':'')+g[i]}return r}
const BAN_BIG=['               \\/','  ___  ____   ____ ___ _   _ _____',' / _ \\| __ ) / ___|_ _| \\ | | ____|','| | | |  _ \\| |    | ||  \\| |  _|','| |_| | |_) | |___ | || |\\  | |___',' \\___/|____/ \\____|___|_| \\_|_____|'];
const BAN_SMALL=['             \\/','  ___  ___  ___ ___ _  _ ___',' / _ \\| _ )/ __|_ _| \\| | __|','| (_) | _ \\ (__ | || .` | _|',' \\___/|___/\\___|___|_|\\_|___|'];
const BRAVO=[' ___ ___    ___   _____  _ ','| _ ) _ \\  /_\\ \\ / / _ \\| |','| _ \\   / / _ \\ V / (_) |_|','|___/_|_\\/_/ \\_\\_/ \\___/(_)'];

/* ================= AUDIO =================
   Bells are additive: a church bell's overtones sit near 0.5 (hum), 1 (prime),
   1.2 (minor-third tierce), 1.5 (quint), 2 (nominal) and higher. Bigger bells
   are lower, ring longer, and keep more of the hum. */
let ac,master,echoIn;
function audio(){if(ac)return ac;ac=new (window.AudioContext||window.webkitAudioContext)();master=ac.createDynamicsCompressor();master.threshold.value=-18;master.ratio.value=4;master.connect(ac.destination);
 echoIn=ac.createGain();const d=ac.createDelay(1);d.delayTime.value=.31;const fb=ac.createGain();fb.gain.value=.38;const lp=ac.createBiquadFilter();lp.type='lowpass';lp.frequency.value=1800;
 echoIn.connect(d);d.connect(lp);lp.connect(fb);fb.connect(d);lp.connect(master);return ac}
/* at most MAXV bells ring at once; a new strike fades out the oldest instead of being dropped */
const MAXV=10,voices=[],jvoices=[];let gestured=false;
function tone(f,{p=[[1,1,1]],dur=.7,vol=.05,when=0,echo=0,jingle=false}={}){if(!S.sound||!gestured)return;try{const a=audio();if(a.state==='suspended')a.resume();
 const now=a.currentTime;const pool=jingle?jvoices:voices,cap=jingle?8:MAXV;for(let i=pool.length-1;i>=0;i--)if(pool[i].end<now)pool.splice(i,1);
 while(pool.length>=cap){const v=pool.shift();v.g.gain.cancelScheduledValues(now);v.g.gain.setValueAtTime(Math.max(v.g.gain.value,.0001),now);v.g.gain.exponentialRampToValueAtTime(.0001,now+.06);v.os.forEach(o=>{try{o.stop(now+.07)}catch(e){}})}
 const t0=now+when;const g=a.createGain();g.gain.setValueAtTime(.0001,t0);g.gain.exponentialRampToValueAtTime(vol,t0+.004);g.gain.exponentialRampToValueAtTime(.0001,t0+dur);const os=[];
 for(const [r,amp,dm] of p){const o=a.createOscillator(),og=a.createGain();o.frequency.value=f*r;og.gain.setValueAtTime(amp,t0);og.gain.exponentialRampToValueAtTime(.0001,t0+dur*(dm||1));o.connect(og);og.connect(g);o.start(t0);o.stop(t0+dur+.05);os.push(o)}
 g.connect(master);if(echo){const e=a.createGain();e.gain.value=echo;g.connect(e);e.connect(echoIn)}
 pool.push({g,os,end:t0+dur})}catch(e){}}
/* browsers only allow sound after the player has touched the page; sounds before that are skipped, not queued */
for(const ev of ['pointerdown','keydown'])addEventListener(ev,()=>{gestured=true},{capture:true});
const HAND=[[1,1,1],[2.76,.35,.45],[5.4,.12,.25]];
const CHURCH=[[.5,.45,1.5],[1,1,1],[1.2,.55,.8],[1.5,.3,.7],[2,.6,.55],[2.5,.18,.4],[3,.15,.3],[4,.08,.2]];
const GREAT=[[.5,.85,1.6],[.502,.4,1.6],[1,1,1],[1.004,.45,1],[1.2,.6,.85],[1.5,.3,.7],[2,.55,.6],[2.51,.18,.4],[3,.15,.3]];
/* bell tiers: base handbell, then each click upgrade */
const BELLS=[
 {sl:'zvonček',en:'handbell',glyph:'o',notes:[1568],p:HAND,dur:.5,vol:.045},
 {sl:'pritrkavanje',en:'bell chiming',glyph:'o',notes:[1568,1319,1175],p:HAND,dur:.55,vol:.045},
 {sl:'bronasti zvon',en:'bronze bell',glyph:'O',notes:[784,659,587],p:CHURCH,dur:1.6,vol:.05},
 {sl:'zvonik na hribu',en:'hilltop belfry',glyph:'O',notes:[523,440,392],p:CHURCH,dur:2.2,vol:.055,echo:.5},
 {sl:'veliki zvon',en:'great bell',glyph:'@',notes:[262,220,196],p:GREAT,dur:3.4,vol:.06,echo:.45},
 {sl:'zvonovi vseh far',en:'bells of every parish',glyph:'@',notes:[262,220,196],p:GREAT,dur:3.4,vol:.05,echo:.45,all:true}];
/* pritrkavanje: a slovenian bell-striking pattern over three bells (0 = highest) */
const PRITRK=[0,1,2,1,0,1,2,2,0,2,1,2];
const bellTier=()=>CLK.reduce((k,c,i)=>has(c[0])?i+1:k,0);
const bellName=()=>{const b=BELLS[bellTier()];return tr(b.sl,b.en)};
let strike=0;
function bellSound(){const B=BELLS[bellTier()];const note=B.notes.length>1?B.notes[PRITRK[strike++%PRITRK.length]]:B.notes[0]*(1+(Math.random()-.5)*.01);
 tone(note,{p:B.p,dur:B.dur,vol:B.vol,echo:B.echo});
 if(B.all){const other=[[784,CHURCH,1.6],[523,CHURCH,2.2],[1568,HAND,.5]][strike%3];tone(other[0]*(PRITRK[strike%12]===0?1:.89),{p:other[1],dur:other[2],vol:.03,when:.09,echo:.4})}
 const now=Date.now();
 if(now<clkUntil)for(let i=0;i<3;i++)tone(2400+Math.random()*1800,{p:HAND,dur:.18,vol:.03,when:i*.045,jingle:true});
 else if(now<kurUntil)for(let i=0;i<2;i++)tone(900+Math.random()*500,{p:HAND,dur:.3,vol:.03,when:i*.06,jingle:true})}
function ding(f=880,v=.06,d=.7){tone(f,{p:HAND,dur:d,vol:v})}
function fanfare(){[[784,0],[988,.12],[1175,.24],[1568,.36]].forEach(([f,w])=>tone(f,{p:CHURCH,dur:1.4,vol:.045,when:w,echo:.3}))}
function regionChime(){[[392,0],[523,.18],[659,.36],[784,.54]].forEach(([f,w])=>tone(f,{p:CHURCH,dur:2.2,vol:.05,when:w,echo:.4}))}

/* ================= LOG ================= */
function log(m){const d=new Date();S.log.unshift(String(d.getHours()).padStart(2,'0')+':'+String(d.getMinutes()).padStart(2,'0')+' '+m);S.log=S.log.slice(0,40);
 const sr=document.getElementById('srlog');if(sr)sr.textContent=m}

/* ================= TOASTS ================= */
const toastQ=[];let toastTimer=0;
const CUP=['\\~~~~~/',' \\   / ','  | |  ',' _|_|_ '];
const ART={ach:CUP,reg:['  /\\  ',' /  \\ ','/____\\','  ||  '],ev:[' \\ | / ','-- * --',' / | \\ ','       '],ref:['.-----.','| [X] |','|_____|','       ']};
const ach4=n=>LANG==='en'?(n===1?'achievement':'achievements'):n===1?'dosežek':n===2?'dosežka':n<5?'dosežki':'dosežkov';
function toast(kind,title,text,sound){
 if(toastQ.length>=3&&kind==='ach'){const l=toastQ[toastQ.length-1];if(l.more)l.more++;else toastQ.push({kind:'ach',more:1});const m=toastQ[toastQ.length-1];
  m.title=tr('in še ','and ')+m.more+' '+tr('','more ')+ach4(m.more);m.text=tr('Vse najdeš v panelu Dosežki.','You will find them all under Achievements.');return}
 toastQ.push({kind,title,text});if(sound)sound();if(toastQ.length===1)showToast()}
function showToast(){const el=document.getElementById('toast');const q=toastQ[0];if(!q){el.hidden=true;return}
 const w=toastCol().w;const iw=w-4;const art=ART[q.kind]||['','','',''];const aw=Math.max(...art.map(L))+2;
 const tx=[...wrap(q.title,iw-aw),...wrap(q.text,iw-aw)];const rows=Math.max(art.length,tx.length);const lines=[''];
 for(let i=0;i<rows;i++)lines.push([H(padR(art[i]||'',aw)),tx[i]||'']);lines.push('');lines.push(padL(tr('[ v redu ]','[ OK ]'),iw));
 const T={ach:tr('DOSEŽEK','ACHIEVEMENT'),reg:tr('CELA REGIJA','REGION COMPLETE'),ev:tr('PRAZNIK','EVENT'),ref:tr('REFERENDUM','REFERENDUM')}[q.kind]||tr('NOVO','NEW');
 el.innerHTML=box(T,lines,w);el.hidden=false;placeToast();el.classList.remove('pop');void el.offsetWidth;el.classList.add('pop');
 clearTimeout(toastTimer);toastTimer=setTimeout(nextToast,3500)}
function nextToast(){toastQ.shift();showToast()}
/* the pop-up borrows one column: the right one on 3 columns, else the left/only one */
function toastCol(){const cs=document.querySelectorAll('#cols .col');const three=MODE.startsWith('3');return {el:cs[three?2:0],w:three?W.c:W.a}}
function placeToast(){const el=document.getElementById('toast');if(el.hidden)return;
 const cols=document.getElementById('cols').getBoundingClientRect();const lh=parseFloat(getComputedStyle(document.body).lineHeight)||16;
 const host=toastCol().el;const x=host?host.getBoundingClientRect().left:cols.left;
 const d=document.getElementById('dock');const db=d.hidden?0:d.getBoundingClientRect().height;
 let bottom=db?db-1:lh;if(!db){const top=innerHeight-bottom-el.offsetHeight;const rootTop=document.getElementById('root').getBoundingClientRect().top;const off=((top-rootTop)%lh+lh)%lh;bottom+=off}
 el.style.left=Math.max(0,x)+'px';el.style.bottom=bottom+'px'}

/* ================= ACHIEVEMENTS =================
   [id, name(), description(), test()] */
const ACH=[];
[1,10,25,50,75,100,125,150,175,200,212].forEach(k=>ACH.push(['o'+k,()=>k===1?tr('Prva občina','First municipality'):k===212?tr('Vsa Slovenija','All of Slovenia'):k+' '+obc(k),
 ()=>tr('odkleni '+k+' '+obc(k),'unlock '+k+' '+obc(k)),()=>S.n>=k]));
REG.forEach((r,i)=>ACH.push(['r'+i,()=>tr('Cela regija: ','Region complete: ')+rname(i),()=>tr('odkleni vse občine regije','unlock every municipality in the region'),()=>regCount()[i]===RN[i]]));
[[100,'Mežnar','Sexton'],[1000,'Zvonar','Bell-ringer'],[10000,'Pritrkovalec','Chimer'],[50000,'Zvon se ne ustavi','The bell never stops']].forEach(([k,s,e])=>ACH.push(['c'+k,()=>tr(s,e),()=>num(k)+tr(' klikov na zvon',' bell rings'),()=>S.clicks>=k]));
[[1,'Pust je tu','Carnival is here'],[10,'Kurentova druščina',"Kurent's company"],[50,'Zima je pregnana','Winter is chased away']].forEach(([k,s,e])=>ACH.push(['k'+k,()=>tr(s,e),()=>tr('ujemi kurenta ','catch the Kurent ')+k+'×',()=>S.kur>=k]));
GEN.forEach((g,k)=>ACH.push(['g'+k,()=>gname(k)+' ×50',()=>tr('zgradi 50 enot: ','own 50 ')+gpl(k),()=>S.own[k]>=50]));
[[1e6,'Milijonar','Millionaire'],[1e9,'Milijardar','Billionaire'],[1e12,'Bilijonar','Trillionaire'],[1e15,'Državni proračun','State budget'],[1e18,'Evropski proračun','EU budget']]
 .forEach(([k,s,e])=>ACH.push(['l'+k,()=>tr(s,e),()=>tr('skupaj zaslužiš ','earn ')+fmt(k)+' SIT'+tr('',' in total'),()=>S.all>=k]));
ACH.push(['ref1',()=>tr('Ljudstvo je odločilo','The people have spoken'),()=>tr('razpiši referendum','call a referendum'),()=>S.refs>=1],
 ['ref5',()=>tr('Večni referendum','Eternal referendum'),()=>tr('razpiši 5 referendumov','call 5 referendums'),()=>S.refs>=5],
 ['am1',()=>tr('Ustavna sprememba','Constitutional change'),()=>tr('sprejmi prvi amandma','adopt your first amendment'),()=>S.amends.length>=1],
 ['am12',()=>tr('Nova ustava','A new constitution'),()=>tr('sprejmi vseh 12 amandmajev','adopt all 12 amendments'),()=>S.amends.length>=AM.length],
 ['ev',()=>tr('Praznično','Festive'),()=>tr('igraj med praznikom','play during a holiday'),()=>holidaysNow().length>0],
 ['wk7',()=>tr('Cel teden','A whole week'),()=>tr('igraj vseh 7 dni v tednu','play on all 7 days of the week'),()=>S.days.length>=7],
 ['mtr',()=>tr('Polno zvonjenje','Full peal'),()=>tr('napolni zvonjenje do konca','fill the ringing meter to the top'),()=>meter>=1],
 ['tri',()=>tr('Na vrhu','On top'),()=>tr('skrivnost: natipkaj ime gore','secret: type the name of a mountain'),()=>S.ach.includes('tri')]);
function gotAch(a){S.ach.push(a[0]);S.achT[a[0]]=Date.now();log('*** '+tr('dosežek: ','achievement: ')+a[1]()+' (+'+pc(ACHP()*100)+')');
 toast('ach',a[1](),a[2]()+'. '+tr('Dohodek +','Income +')+pc(ACHP()*100)+'.',fanfare);const i=ACH.indexOf(a);if(i>=0)achPage=Math.floor(i/6)}
function checkAch(){for(const a of ACH){if(a[0]==='tri'||S.ach.includes(a[0]))continue;if(a[4]===undefined&&a[3]())gotAch(a)}}

/* ================= PLAYTEST STATS ================= */
const MILES=[10,25,50,75,100,125,150,175,200,212];
function mark(kind,val){S.mile.push({k:kind,v:val,run:S.refs+1,play:Math.round(S.play),wall:Date.now()-S.first})}
function statsText(){const lines=[];const days=ms=>(ms/864e5).toLocaleString(LOC(),{maximumFractionDigits:1});
 lines.push(tr('Občine kliker: statistika za testiranje','Občine clicker: playtest stats')+' (v'+VERSION+', '+new Date().toLocaleDateString('sv')+')');
 lines.push(tr('igranje z odprto stranjo: ','played with the page open: ')+dur(S.play)+' · '+tr('od prve igre: ','since first start: ')+days(Date.now()-S.first)+tr(' dni',' days'));
 lines.push(tr('zdaj: ','now: ')+S.n+'/212 · '+tr('referendumi ','referendums ')+S.refs+' · '+tr('glasovi ','votes ')+S.votes+' · '+tr('dosežki ','achievements ')+S.ach.length+'/'+ACH.length+' · '+tr('kliki ','clicks ')+num(S.clicks)+' · '+tr('kurent ','Kurent ')+S.kur);
 if(S.amends.length)lines.push(tr('amandmaji: ','amendments: ')+S.amends.map(amName).join(', '));
 lines.push(tr('mejniki (igra · igranje · koledar):','milestones (run · played · calendar):'));
 for(const m of S.mile)lines.push('  '+(m.k==='o'?padR(m.v+' '+obc(m.v),18):padR(tr('referendum +','referendum +')+m.v,18))+' #'+m.run+' · '+dur(m.play)+' · '+days(m.wall)+tr(' dni',' days'));
 return lines.join('\n')}

/* ================= ACTIONS ================= */
function unlock(quiet){if(S.n>=O.length)return false;const c=ocost(S.n);if(S.sit<c)return false;S.sit-=c;const o=O[S.n];const rc0=regCount()[o.r];S.n++;
 if(MILES.includes(S.n)&&!S.mile.some(m=>m.k==='o'&&m.v===S.n&&m.run===S.refs+1))mark('o',S.n);
 if(!quiet)log(tr('odklenjena ','unlocked ')+o.n+' ('+num(o.p)+tr(' preb.)',' res.)'));
 if(rc0+1===RN[o.r]){log(tr('cela regija ','region complete: ')+rname(o.r)+': '+tr('vse ','everything ')+xv(REGB()));
  toast('reg',rname(o.r),tr('Vseh '+RN[o.r]+' občin je tvojih. Dohodek ','All '+RN[o.r]+' municipalities are yours. Income ')+xv(REGB())+'.',regionChime)}
 GEN.forEach((g,k)=>{if(greq(k)===S.n)log(tr('nova proizvodnja: ','new producer: ')+gname(k))});
 if(LMAT[S.n-1])log(tr('znamenitost: ','landmark: ')+lname(LMAT[S.n-1])+' ('+o.n+')');
 if(S.n===O.length&&!S.won){S.won=Date.now();log('*** '+tr('vsa Slovenija je tvoja','all of Slovenia is yours')+' ***');regionChime();setTimeout(fanfare,900)}
 if(!quiet)ding(660,.05);regPage=null;return true}
function buyGen(k){if(S.n<greq(k))return;let a=S.amt==='max'?gmax(k):S.amt;if(a<1)return;const c=gcost(k,a);if(S.sit<c)return;S.sit-=c;S.own[k]+=a;ding(990,.03,.3)}
function buyUp(id){const u=upgrades().find(u=>u.id===id);if(!u||S.sit<u.cost)return;S.sit-=u.cost;S.ups.push(id);log(tr('kupljeno: ','bought: ')+u.name+' ('+u.desc.split(' · ')[0]+')');
 if(id[0]==='k'){strike=0;toast('new',bellName().toUpperCase(),tr('Tvoj zvon zdaj zveni drugače. Pozvoni!','Your bell sounds different now. Ring it!'),null);bellSound()}else ding(1175,.05)}
let swing=0,pslot=0;const parts=[];
function ring(){meter=Math.min(1,meter+FILL*evFill());lastRingT=Date.now();const v=clickVal();S.sit+=v;S.life+=v;S.all+=v;S.clicks++;swing=6;
 pslot=(pslot+1)%6;parts.push({t:'+'+fmt(v,1),x:pslot%2?.75:.25,age:0,y0:6+Math.floor(pslot/2)});if(parts.length>8)parts.shift();bellSound()}
const kurLm=LM.find(l=>l.kind==='kur');
function catchKurent(){if(!kurPos)return;kurPos=null;kurGone=0;S.kur++;const lx=has(kurLm.id)?KC.ptujLong:1;const r=Math.random();
 if(r<.5){const ms=KC.multS*lx;kurUntil=Date.now()+ms;log(tr('kurentovanje! dohodek ×','Kurentovanje! income ×')+KC.mult+tr(' za ',' for ')+ms/1000+' s')}
 else if(r<.8){const g=Math.min(S.sit*KC.krofBank,baseIps()*KC.krofS)+13;S.sit+=g;S.life+=g;S.all+=g;log(tr('pustni krof: +','carnival doughnut: +')+fmt(g)+' SIT')}
 else{const ms=KC.clickS*lx;clkUntil=Date.now()+ms;log(tr('zvonci! klik ×','jingle bells! clicks ×')+KC.click+tr(' za ',' for ')+ms/1000+' s')}
 ding(523,.06);ding(784,.05);drawMap(true)}
function offerAmendments(){const left=AM.map(a=>a[0]).filter(id=>!am(id));for(let i=left.length-1;i>0;i--){const j=Math.floor(Math.random()*(i+1));[left[i],left[j]]=[left[j],left[i]]}return left.slice(0,3)}
function referendum(pick){const g=votesGain();if(g<1)return;mark('r',g);
 const keep={all:S.all,votes:S.votes+g,refs:S.refs+1,ach:S.ach,achT:S.achT,sound:S.sound,light:S.light,lang:S.lang,amt:S.amt,kur:S.kur,clicks:S.clicks,log:S.log,
  amends:pick?[...S.amends,pick]:S.amends,first:S.first,play:S.play,mile:S.mile,evSeen:S.evSeen,days:S.days};
 const bells=S.ups.filter(id=>id[0]==='k');S=Object.assign(fresh(),keep);
 if(am('a10'))S.ups=bells;if(am('a4')){S.own[0]=10;S.own[1]=10;S.own[2]=5}
 log(tr('referendum: +','referendum: +')+g+tr(' glasov. Nova Slovenija se začne.',' votes. A new Slovenia begins.'));
 if(pick)toast('ref',amName(pick),amDesc(pick)+'.',fanfare);
 kurUntil=clkUntil=0;regPage=null;refPick=null;save();full()}
function save(){S.save=Date.now();try{localStorage.setItem(KEY,JSON.stringify(S))}catch(e){}}

/* ================= LAYOUT ================= */
let MODE='',W={},PW={},HW=80,cache={};
function layout(){const vw=document.documentElement.clientWidth-16;const mz=document.getElementById('measure');
 const cw=f=>{document.body.style.fontSize=f+'px';return mz.getBoundingClientRect().width/100};
 let mode,f;
 for(f of [14,13]){const c=Math.floor(vw/cw(f));if(c>=175){mode='3';W={a:41,b:88,c:Math.min(48,c-133)};break}}
 if(!mode)for(f of [14,13,12]){const c=Math.floor(vw/cw(f));if(c>=131){mode='2';W={a:41,b:88};break}}
 if(!mode){for(f of [14,13,12,11,10]){const c=Math.floor(vw/cw(f));if(c>=48||f===10){const a=Math.max(49,Math.min(c,c>=89?89:63));mode='1';W={a:a-(a%2?0:1)};break}}}
 document.body.style.fontSize=f+'px';
 const key=mode+JSON.stringify(W);if(key===MODE)return;MODE=key;
 let cols;
 if(mode==='3')cols=[['bell','stat','ref','set'],['next','map','gen','log'],['ups','reg','list','ach']];
 else if(mode==='2')cols=[['bell','stat','ups','reg','ref','set'],['next','map','gen','list','ach','log']];
 else cols=[['bell','next','map','gen','ups','stat','reg','list','ach','ref','log','set']];
 const wOf=ci=>mode==='1'?W.a:mode==='2'?(ci===0?W.a:W.b):[W.a,W.b,W.c][ci];
 document.getElementById('cols').innerHTML=cols.map((c,ci)=>`<div class="col">${c.map(id=>`<pre id="p-${id}"></pre>`).join('')}</div>`).join('');
 PW={};cols.forEach((c,ci)=>c.forEach(id=>PW[id]=wOf(ci)));
 HW=mode==='3'?W.a+W.b+W.c+4:mode==='2'?W.a+W.b+2:W.a;
 cache={};PH={};for(const k in lineCache)delete lineCache[k];drawMap(true)}

/* ================= PANELS ================= */
function headStatus(w){if(S.n>=O.length)return '*** '+tr('VSA SLOVENIJA JE TVOJA','ALL OF SLOVENIA IS YOURS')+' ***   212/212';const c=ocost(S.n),f=c?Math.min(1,S.sit/c):1,v=ips();
 const tail=' '+pc(Math.floor(f*100))+(f<1&&v>0?' · '+tr('še ~','~')+dur((c-S.sit)/v):' · '+tr('lahko odkleneš','ready'));const head=tr('občine ','')+S.n+'/212 · '+tr('naslednja: ','next: ')+ab(O[S.n].n,16)+' ';
 const bw=Math.max(6,Math.min(30,w-L(head)-L(tail)-2));return L(head)+bw+2+L(tail)<=w?head+bar(f,bw)+tail:tr('naslednja: ','next: ')+ab(O[S.n].n,w-11-L(tail))+tail}
function headEvents(w){const ev=eventsNow();return wrapItems(ev.map((e,i)=>(i?'':tr('* danes: ','* today: '))+evName(e)+' ('+evDesc(e)+')'),' · ',w)}
function pHead(){const w=HW;const ban=w>=70?BAN_BIG:BAN_SMALL;const s=fmt(Math.floor(S.sit));const m=s.match(/^([\d.,]+)\s*([^\d]*)$/);let dg=big(m?m[1]:s,w>=70?'big':'small');if(Math.max(...dg.map(L))+6>w)dg=big(m?m[1]:s,'small');
 {const base=dg.length-2,u=m&&m[2]?m[2]:'';dg=dg.map((r,i)=>r+(i===base&&u?' '+u:' '.repeat(u?L(u)+1:0)))}
 const unit=tr('tolarji','tolars');const rate='+'+fmt(ips(),1)+' SIT/s';const sub=tr('212 občin, od Osilnice do Ljubljane','212 municipalities, from Osilnica to Ljubljana');const lines=[];
 if(w>=100){const left=[...ban,'',sub];const right=[unit,'',...dg,'',rate];const rows=Math.max(left.length,right.length);const rw=Math.max(34,...right.map(L))+2;
  for(let i=0;i<rows;i++){const r=padL(right[i]||'',rw);lines.push(i>=2&&i<2+dg.length?{h:esc(padR(left[i]||'',w-rw))+'<b>'+esc(r)+'</b>'}:padR(left[i]||'',w-rw)+r)}}
 else lines.push(...ban,'',...wrap(sub,w),'',unit,'',...dg.map(d=>({h:'<b>'+esc(padR(d,w))+'</b>'})),'',rate);
 lines.push('='.repeat(w));lines.push(cut(headStatus(w),w));lines.push(...headEvents(w));
 return lines.map(l=>typeof l==='object'?l.h:esc(padR(l,w))).join('\n')}
function srSummary(){const n=S.n<O.length?O[S.n]:null;
 return tr('Tolarji: ','Tolars: ')+fmt(Math.floor(S.sit))+'. '+tr('Na sekundo: ','Per second: ')+fmt(ips(),1)+'. '+tr('Občine: ','Municipalities: ')+S.n+tr(' od 212.',' of 212.')+
  (n?' '+tr('Naslednja: ','Next: ')+n.n+', '+tr('cena ','cost ')+fmt(ocost(S.n))+' SIT.':'')}
const BELL=['          +','          |','         /^\\','        /   \\','       /_____\\','       | ___ |','       ||%%%||','       ||_%_||','       |     |','       |  _  |','       | | | |','   ____|_|_|_|____'];
function pBell(w){const iw=w-4;const bg=BELLS[bellTier()].glyph;const sw=swing>0?(swing%2?'/'+bg+')':'('+bg+'\\'):'('+bg+')';const cl=swing>0?(swing%2?'/':'\\'):'|';
 const art=BELL.map(l=>l.replace('%%%',sw).replace('%',cl));const aw=Math.max(...art.map(L));const AX=10;const off=Math.floor((iw-1)/2)-AX;
 const grid=art.map(l=>[...padR(' '.repeat(off)+l,iw)]);
 for(const p of parts){const y=p.y0-Math.floor(p.age/2);if(y<0)continue;const x=p.x<.5?Math.max(0,off-L(p.t)-1-Math.floor(p.x*4)):Math.min(iw-L(p.t),off+aw+1+Math.floor((p.x-.5)*4));
  [...p.t].forEach((ch,j)=>{if(grid[y][x+j]!==undefined)grid[y][x+j]=ch})}
 const lines=grid.map(r=>[{t:r.join(''),a:'ring',c:'bell',hid:true}]);
 lines.push(['']);
 const lbl=tr('[  Z V O N I  ]','[  R I N G  ]');lines.push([' '.repeat(off+AX-Math.floor(L(lbl)/2)),{t:lbl,a:'ring',c:'ring',lab:tr('Pozvoni','Ring the bell')}]);
 lines.push(['']);{const x=xf(meterMult()),lab=tr('zvonjenje ','ringing ');lines.push([lab,H(bar(meter,iw-L(lab)-L(x)-3)),' ',x])}
 lines.push(lr(tr('zvon','bell'),bellName()+' (max '+xv(meterCap())+')',iw));lines.push(lr(tr('en klik','per click'),fmt(clickVal(),1)+' SIT',iw));
 const now=Date.now();
 if(now<kurUntil)lines.push(lr(tr('KURENTOVANJE ×','KURENT ×')+KC.mult,Math.ceil((kurUntil-now)/1000)+' s',iw));
 if(now<clkUntil)lines.push(lr(tr('ZVONCI: klik ×','JINGLES: click ×')+KC.click,Math.ceil((clkUntil-now)/1000)+' s',iw));
 return box(tr('ZVONIK','BELL TOWER'),lines,w,[tr('[preslednica]','[space]')])}
function pStat(w){const iw=w-4;const p=pop();const rd=regsDone();const tl=[];
 const row=(a,b)=>tl.push(lr(a,b,iw));
 row(tr('tolarji','tolars'),fmt(Math.floor(S.sit)));row(tr('na sekundo','per second'),fmt(ips(),1));row(tr('na klik','per click'),fmt(clickVal(),1));row(tr('občine','municipalities'),S.n+'/212');row(tr('prebivalci','residents'),num(p));
 tl.push(two([H(bar(p/TOTAL,iw-9))],[pc(p/TOTAL*100)],iw));tl.push('');
 tl.push(tr('množitelji:','multipliers:'));
 row(tr('  prebivalci (1 na ','  residents (1 per ')+num(PDIV)+')',xf(popMult()));row(tr('  cele regije (','  complete regions (')+rd+'/12)',xf(regMult()));row(tr('  znamenitosti','  landmarks'),xf(globUp()));
 row(tr('  zvonjenje','  ringing'),xf(meterMult()));row(tr('  dosežki (','  achievements (')+S.ach.length+')',xf(achMult()));row(tr('  glasovi (','  votes (')+S.votes+')',xf(voteMult()));
 if(evGlob()>1)row(tr('  dan / praznik','  day / holiday'),xf(evGlob()));if(kurMult()>1)row('  '+tr('kurent','Kurent'),xf(KC.mult));
 row(tr('  skupaj','  total'),xf(allMult()*kurMult()*meterMult()));tl.push('');
 row(tr('čas te igre','this run'),dur((Date.now()-S.t0)/1000));row(tr('vsega zasluženo','earned in total'),fmt(S.all));
 return box(tr('STANJE','STATUS'),tl,w)}
function ipsAfterUnlock(){const o=O[S.n];const rc=regCount();const done=rc[o.r]+1===RN[o.r];return (1+(pop()+o.p)/PDIV)/popMult()*(done?REGB():1)}
function pNext(w){const iw=w-4;const ls=[];const T=tr('NASLEDNJA OBČINA','NEXT MUNICIPALITY');
 if(S.n>=O.length){BRAVO.forEach(l=>ls.push(H(' '.repeat(Math.max(0,Math.floor((iw-L(l))/2)))+l)));ls.push('');
  wrap(tr('Vseh 212 občin in '+num(TOTAL)+' prebivalcev je tvojih. Čas te igre: ','All 212 municipalities and '+num(TOTAL)+' residents are yours. This run took ')+dur((S.won-S.t0)/1000)+'.',iw).forEach(l=>ls.push(l));
  wrap(tr('Razpiši referendum: dobiš glasove in začneš znova, hitreje.','Call a referendum: you get votes and start again, faster.'),iw).forEach(l=>ls.push(l));return box(T,ls,w,['[N]'])}
 const o=O[S.n],c=ocost(S.n),can=S.sit>=c,v=ips();
 {const id='#'+String(S.n+1).padStart(3,'0')+'  ',mo=o.u?MO():'';const rg=ab(rname(o.r),Math.max(10,iw-L(id)-L(mo)-L(o.n)-2));
  ls.push(lr(id+ab(o.n,iw-L(id)-L(mo)-L(rg)-2).toUpperCase()+mo,rg,iw))}
 ls.push(num(o.p)+tr(' prebivalcev',' residents')+' · '+o.a+' km² · '+tr('občina od ','since ')+(o.y||'?'));
 ls.push(tr('po odklepu: dohodek +','after unlocking: income +')+pc((ipsAfterUnlock()-1)*100));
 const extra=[];GEN.forEach((g,k)=>{if(greq(k)===S.n+1)extra.push(tr('odpre ','opens ')+gname(k).toLowerCase())});if(LMAT[S.n])extra.push(tr('znamenitost: ','landmark: ')+lname(LMAT[S.n]));
 const rc=regCount();if(rc[o.r]+1===RN[o.r])extra.push(tr('dokonča regijo','completes the region'));
 wrap(extra.length?'+ '+extra.join(' · '):'',iw).slice(0,2).forEach(l=>ls.push(l));if(extra.length<1)ls.push('');
 ls.push('');
 let k=0,s=S.sit;while(S.n+k<O.length&&s>=ocost(S.n+k)){s-=ocost(S.n+k);k++}
 if(can)ls.push([btn(tr(' ODKLENI · ',' UNLOCK · ')+(c?fmt(c)+' SIT ':tr('zastonj ','free ')),'unlock',true,tr('Odkleni ','Unlock ')+o.n),...(k>1?['  ',btn(tr(' VSE MOŽNE (',' ALL (')+k+') ','all')]:[])]);
 else ls.push(tr('cena ','cost ')+fmt(c)+' SIT'+(v>0?' · '+tr('še ~','~')+dur((c-S.sit)/v)+tr('',' to go'):''));
 const g=votesGain();if(g>=Math.max(10,S.votes)&&(S.n>=150||(!can&&v>0&&(c-S.sit)/v>3600)))ls.push(wrap(tr('referendum se splača: +'+g+' glasov','a referendum pays off now: +'+g+' votes'),iw)[0]);else ls.push('');
 const nx=[1,2,3].map(k=>O[S.n+k]).filter(Boolean).map(q=>q.n);
 {let s=tr('sledijo: ','next up: ');if(!nx.length)s+=tr('Ljubljana je zadnja.','Ljubljana is the last.');else{let k=0;for(const q of nx){const add=(k?', ':'')+q;if(L(s+add)+2>iw)break;s+=add;k++}if(k<nx.length||S.n+4<O.length)s+=' …'}ls.push(s)}
 return box(T,ls,w,['[N]'])}
function mapFor(w){return w-4>=MAPS.big.W?MAPS.big:MAPS.small}
const KUR=['\\  /','(oo)','/##\\'];
function mapGridHTML(M,iw){const n=S.n;const pad=Math.floor((iw-M.W)/2);let h='';
 for(let y=0;y<M.H;y++){let row='| '+' '.repeat(pad);for(let x=0;x<M.W;x++){
  if(kurPos&&y>=kurPos[1]&&y<kurPos[1]+3&&x>=kurPos[0]&&x<kurPos[0]+4){row+=`<span class="kur" data-a="kurent">${esc(KUR[y-kurPos[1]][x-kurPos[0]])}</span>`;continue}
  const i=M.g[y][x];if(i===-2){row+='~';continue}if(i<0){row+=' ';continue}
  const seat=M.s[i]&&M.s[i][0]===x&&M.s[i][1]===y;let ch,cls='c'+i;
  if(i<n)ch=seat?(O[i].n==='Ljubljana'?'@':O[i].u?'O':'o'):REG[O[i].r][3];else if(i===n){ch='?';cls+=' q'}else ch='.';
  row+=`<i class="${cls}">${esc(ch)}</i>`}
  h+=row+' '.repeat(iw-pad-M.W)+' |\n'}
 return h}
let mapKey='';
function drawMap(force){const w=PW.map;if(!w)return;const el=document.getElementById('p-map');if(!el)return;const M=mapFor(w);const k=S.n+'|'+(kurPos?kurPos.join():'')+'|'+w+'|'+LANG;
 if(!force&&k===mapKey)return;mapKey=k;const iw=w-4;const T=tr('ZEMLJEVID','MAP');const right='[ '+S.n+'/212 ]';
 el.innerHTML=fit([H('+-'),{t:'[ ',c:'bold',hid:true},{t:T,c:'bold',head:true},{t:' ]',c:'bold',hid:true},H('-'.repeat(w-L('+-[ '+T+' ]')-L(right)-2)),right,H('-+')],w)+'\n'+seg(H('| '+' '.repeat(iw)+' |'))+'\n'+
  `<span id="mapgrid" aria-hidden="true">${mapGridHTML(M,iw)}</span><span id="mapinfo"></span>`+seg(H('+'+'-'.repeat(w-2)+'+'));
 mapInfo(true)}
let infoKey='';
function mapInfo(force){const w=PW.map;const el=document.getElementById('mapinfo');if(!el)return;const iw=w-4;const i=hover;
 let a,b;if(i<0){a=tr('premakni miško ali tapni občino.','hover over or tap a municipality.');b=tr('o sedež  O mestna občina  @ Ljubljana  ? naslednja  . zaklenjena','o seat  O city municipality  @ Ljubljana  ? next  . locked')}
 else{const o=O[i];const known=i<=S.n+2;const mo=o.u&&known?MO():'';const res=tr(' preb.',' res.');
  a=(known?o.n:'??????')+mo+' · '+num(o.p)+res+' · '+o.a+' km² · '+rname(o.r);if(L(a)>iw)a=(known?ab(o.n,18):'??????')+mo+' · '+num(o.p)+res+' · '+o.a+' km² · '+ab(rname(o.r),14);
  b=i<S.n?tr('odklenjena · #','unlocked · #')+(i+1)+(LMAT[i]?' · '+tr('znamenitost: ','landmark: ')+lname(LMAT[i]):''):i===S.n?tr('naslednja · ','next · ')+fmt(ocost(i))+' SIT':tr('zaklenjena · #','locked · #')+(i+1)}
 const k=a+b+!!kurPos;if(!force&&k===infoKey)return;infoKey=k;
 const bl=i<0?wrapItems(b.split('  '),'  ',iw):wrap(b,iw);
 const aw=wrap(a,iw);const lines=['',...aw.slice(0,2),...bl.slice(0,3-Math.min(2,aw.length))];while(lines.length<4)lines.push('');
 el.innerHTML=lines.map(l=>seg(H('| '))+esc(padR(cut(l,iw),iw))+seg(H(' |'))+'\n').join('')+
  (kurPos?`<span class="sr" data-a="kurent" role="button" tabindex="0">${esc(tr('Kurent je na zemljevidu. Ujemi ga.','The Kurent is on the map. Catch him.'))}</span>`:'')}
function bestGen(){let best=-1,bv=Infinity;GEN.forEach((g,k)=>{if(S.n<greq(k))return;const v=gcost(k,1)/(gprod(k)*genMult(k));if(v<bv){bv=v;best=k}});return best}
function pGen(w){const iw=w-4;const ls=[];const wide=iw>=70;const bg=bestGen();
 GEN.forEach((g,k)=>{if(S.n<greq(k)){if(k>0&&S.n>=greq(k-1))ls.push(lr('???',tr(' odpre se pri ',' opens at ')+greq(k)+' '+obc(greq(k)),iw));return}
  const a=S.amt==='max'?Math.max(1,gmax(k)):S.amt;const c=gcost(k,a);const can=S.sit>=c&&(S.amt!=='max'||gmax(k)>0);
  const each=gprod(k)*genMult(k)*allMult()*kurMult();const label=S.amt===1?tr(' KUPI ',' BUY '):tr(' KUPI ',' BUY ')+a+' ';const lab=tr('Kupi ','Buy ')+(a>1?a+' ':'')+gname(k);
  const nm=gname(k)+(k===bg?' *':'');
  if(wide)ls.push([padR(nm,13),padL(String(S.own[k]),5),'  ',padL(fmt(genIps(k)*kurMult(),1)+'/s',14),'  ',padL('+'+fmt(each,1)+'/s',13),'  ',padL(fmt(c),12),'  ',btn(label,'g'+k,can,lab)]);
  else{ls.push(lr(nm+'  ×'+S.own[k],fmt(genIps(k)*kurMult(),1)+'/s',iw));ls.push(two([tr('  cena ','  cost ')+fmt(c)],[btn(label,'g'+k,can,lab)],iw))}});
 ls.push('');ls.push(tr('* najboljše razmerje med ceno in dohodkom','* best price for the income'));
 if(wide)ls.unshift([padR('',13),padL(tr('kos','own'),5),'  ',padL(tr('skupaj','total'),14),'  ',padL(tr('vsak','each'),13),'  ',padL(tr('cena','cost'),12)]);
 const right=[];[1,10,100,'max'].forEach(a=>right.push({t:'['+(a==='max'?'MAX':'×'+a)+']',a:'amt'+a,c:S.amt===a?'on':'',lab:tr('kupuj po ','buy ')+(a==='max'?tr('največ','max'):a)}));
 return box(tr('PROIZVODNJA','PRODUCTION'),ls,w,right)}
function pUps(w){const iw=w-4;const U=upgrades();const ls=[];const max=MODE.startsWith('3')?9:6;
 if(!U.length)ls.push(tr('ni novih izboljšav.','no new upgrades.'));
 U.slice(0,max).forEach(u=>{const can=S.sit>=u.cost;const nw=wrap(u.name,iw-L(fmt(u.cost))-2);nw.forEach((l,j)=>ls.push(j===0?lr(l,fmt(u.cost),iw):l));
  const d=wrap(u.desc,iw-10);d.forEach((l,j)=>ls.push(j===d.length-1?two(['  '+l],[btn(tr(' KUPI ',' BUY '),'u'+u.id,can,tr('Kupi ','Buy ')+u.name)],iw):['  '+l]))});
 if(U.length>max)ls.push(tr('… in še ','… and ')+(U.length-max)+tr('',' more'));
 const nextLm=LM.find(l=>l.o>=S.n);if(nextLm){ls.push('');wrap(tr('naslednja znamenitost: čez ','next landmark: in ')+(nextLm.o-S.n+1)+' '+obc(nextLm.o-S.n+1),iw).forEach(l=>ls.push(l))}
 const aff=U.filter(u=>u.cost<=S.sit).length;return box(tr('IZBOLJŠAVE','UPGRADES'),ls,w,aff>1?[btn(tr(' KUPI VSE ',' BUY ALL '),'upall')]:['[ '+tr('kupljenih ','owned ')+S.ups.length+' ]'])}
function pReg(w){const iw=w-4;const rc=regCount();const ls=[];const bw=Math.max(8,iw-31);
 REG.forEach((r,i)=>{const done=rc[i]===RN[i];const nm=ab(rname(i),iw-bw-12);ls.push([r[3]+' '+padR(nm,iw-bw-12),H(bar(rc[i]/RN[i],bw-2)),' ',done?{t:padL(xv(REGB()),8),c:'bold'}:padL(rc[i]+'/'+RN[i],8)])});
 return box(tr('REGIJE','REGIONS'),ls,w,['[ '+tr('cela = ','complete = ')+xv(REGB())+' ]'])}
function pList(w){const iw=w-4;const rows=MODE.startsWith('1')?10:16;if(regPage===null)regPage=Math.max(0,Math.min(O.length-rows,S.n-Math.floor(rows/2)));
 const ls=[];for(let i=regPage;i<Math.min(O.length,regPage+rows);i++){const o=O[i];const known=i<=S.n+2;
  const nm='?'.repeat(Math.min(12,L(o.n)));const mark=i<S.n?'x':i===S.n?'>':' ';const lm=LMAT[i]&&known?' *':'';const mo=o.u?MO():'';
  const pre=mark+' '+String(i+1).padStart(3,'0')+' ',room=iw-11-L(pre);const nmF=known?ab(o.n,room-L(mo)-L(lm))+mo+lm:nm;
  const line=padR(pre+nmF,iw-10)+padL(num(o.p),10);ls.push(i===S.n?[{t:line,c:'on'}]:line)}
 ls.push('');ls.push(two([btn('<<','pg-'+rows,true,tr('nazaj za stran','previous page')),' ',btn('<','pg-1',true,tr('nazaj','back')),' ',btn('>','pg1',true,tr('naprej','forward')),' ',btn('>>','pg'+rows,true,tr('naprej za stran','next page'))],
  [btn(tr(' NASLEDNJA ',' NEXT '),'pg0')],iw));
 ls.push(tr('x odklenjena  > naslednja  * znamenitost','x unlocked  > next  * landmark'));
 return box(tr('REGISTER OBČIN','MUNICIPALITY REGISTER'),ls,w,['[ '+(regPage+1)+'-'+Math.min(O.length,regPage+rows)+' ]'])}
function pAch(w){const iw=w-4;const per=6;const pages=Math.ceil(ACH.length/per);achPage=(achPage+pages)%pages;const ls=[];
 ls.push(lr(tr('dobljeno ','earned ')+S.ach.length+'/'+ACH.length,'+'+pc(Math.round(ACHP()*100*S.ach.length))+tr(' dohodka',' income'),iw));ls.push([H(bar(S.ach.length/ACH.length,iw-2))]);ls.push('');
 const isNew=id=>S.achT[id]&&Date.now()-S.achT[id]<6e5;
 ACH.slice(achPage*per,achPage*per+per).forEach(a=>{const got=S.ach.includes(a[0]);const nw=got&&isNew(a[0]);
  wrap((got||a[0]!=='tri'?a[1]():'???'),iw-4).forEach((l,j)=>ls.push(j?'    '+l:nw?[{t:'[!] '+l,c:'bold'}]:(got?'[x] ':'[ ] ')+l));wrap(a[2](),iw-4).forEach(l=>ls.push('    '+l))});
 ls.push('');ls.push(two([btn('<','ach-1',true,tr('prejšnja stran','previous page')),' ',btn('>','ach1',true,tr('naslednja stran','next page'))],[(achPage+1)+'/'+pages],iw));
 const nNew=S.ach.filter(isNew).length;return box(tr('DOSEŽKI','ACHIEVEMENTS'),ls,w,nNew?[{t:'[ '+tr('novih: ','new: ')+nNew+' ]',c:'bold'}]:[])}
function pRef(w){const iw=w-4;const g=votesGain();const ls=[];
 ls.push(lr(tr('glasovi','votes'),S.votes+' (+'+pc(Math.round(S.votes*VOTEP()*100))+')',iw));ls.push(lr(tr('referendumi','referendums'),String(S.refs),iw));
 ls.push(lr(tr('ob referendumu dobiš','a referendum now gives'),'+'+g,iw));ls.push(lr(tr('naslednji glas pri','next vote at'),fmt((votesTotal()+1)**3*1e9),iw));ls.push('');
 if(refPick){wrap(tr('Izberi ustavni amandma. Velja za vedno.','Choose a constitutional amendment. It lasts forever.'),iw).forEach(l=>ls.push(l));ls.push('');
  refPick.forEach(id=>{wrap(amName(id),iw).forEach(l=>ls.push([{t:l,c:'bold'}]));const d=wrap(amDesc(id),iw-14);d.forEach((l,j)=>ls.push(j===d.length-1?two(['  '+l],[btn(tr(' SPREJMI ',' ADOPT '),'am'+id,true,tr('Sprejmi ','Adopt ')+amName(id))],iw):'  '+l))});
  ls.push('');ls.push([btn(tr(' PREKLIČI ',' CANCEL '),'refno')]);return box('REFERENDUM',ls,w)}
 wrap(tr('Vsak glas da +'+pc(VOTEP()*100)+' dohodka. Referendum ponastavi tolarje, občine, proizvodnjo in izboljšave. Glasovi, dosežki in amandmaji ostanejo.',
  'Each vote gives +'+pc(VOTEP()*100)+' income. A referendum resets tolars, municipalities, production and upgrades. Votes, achievements and amendments stay.'),iw).forEach(l=>ls.push(l));ls.push('');
 if(Date.now()<refArm)ls.push([btn(tr(' RES? DA ',' SURE? YES '),'refyes'),' ',btn(tr(' NE ',' NO '),'refno')]);else ls.push([btn(tr(' RAZPIŠI REFERENDUM ',' CALL A REFERENDUM '),'ref',g>=1)]);
 ls.push('');ls.push(tr('amandmaji: ','amendments: ')+S.amends.length+'/'+AM.length);S.amends.forEach(id=>wrap('- '+amName(id)+': '+amDesc(id),iw-2).forEach((l,j)=>ls.push(j?'  '+l:l)));
 return box('REFERENDUM',ls,w)}
function pLog(w){const iw=w-4;const n=MODE.startsWith('1')?6:8;const ls=[];for(const e of S.log){const ws=wrap(e,iw-6);ws.forEach((l,j)=>ls.push(j?'      '+l:l));if(ls.length>=n)break}
 ls.length=Math.min(ls.length,n);while(ls.length<n)ls.push('');return box(tr('DNEVNIK','LOG'),ls,w)}
function pSet(w){const iw=w-4;const ls=[];
 ls.push([btn(S.sound?tr(' zvok: vklopljen ',' sound: on '):tr(' zvok: izklopljen ',' sound: off '),'snd'),' ',btn(S.light?tr(' tema: svetla ',' theme: light '):tr(' tema: temna ',' theme: dark '),'thm')]);
 ls.push([btn(LANG==='en'?' language: English ':' jezik: slovenščina ','lng',true,LANG==='en'?'Preklopi v slovenščino':'Switch to English')]);
 ls.push('');ls.push(tr('tipke:','keys:'));ls.push(tr('  [preslednica]  pozvoni','  [space]  ring the bell'));ls.push(tr('  [N]  odkleni naslednjo občino','  [N]  unlock the next municipality'));ls.push('');
 wrap(tr('Prenos igre: igra se shranjuje samo v tem brskalniku. Za prenos na drug telefon ali računalnik jo tu kopiraj, tam pa prilepi.',
  'Moving your game: it is saved only in this browser. To continue on another phone or computer, copy it here and paste it there.'),iw).forEach(l=>ls.push(l));
 ls.push([btn(tr(' kopiraj igro ',' copy game '),'exp'),' ',btn(tr(' naloži ',' load '),'imp')]);
 ls.push(['> ',{t:'                    ',raw:`<input id="impin" aria-label="${esc(tr('Prilepi shranjeno igro','Paste a saved game'))}" placeholder="${esc(tr('prilepi tukaj','paste here'))}">`}]);
 wrap(flash||'',iw).forEach(l=>ls.push(l));if(!flash)ls.push('');
 wrap(tr('Za testerje: kopiraj statistiko in jo pošlji razvijalcu.','For playtesters: copy your stats and send them to the developer.'),iw).forEach(l=>ls.push(l));
 ls.push([btn(tr(' kopiraj statistiko ',' copy stats '),'stats')]);ls.push('');
 ls.push([Date.now()<resetArm?btn(tr(' RES IZBRIŠEM VSE? ',' REALLY DELETE ALL? '),'rstyes'):btn(tr(' začni čisto od začetka ',' start over from scratch '),'rst')]);ls.push('');
 wrap(tr('Podatki: seznam občin na slovenski Wikipediji. Zemljevid je približek iz središč občin.','Data: list of municipalities on Slovenian Wikipedia. The map is approximated from municipal seats.'),iw).forEach(l=>ls.push(l));
 return box(tr('NASTAVITVE','SETTINGS'),ls,w)}

/* ================= RENDER ================= */
const PAN={bell:pBell,stat:pStat,next:pNext,gen:pGen,ups:pUps,reg:pReg,list:pList,ach:pAch,ref:pRef,log:pLog,set:pSet};
let PH={};
function padPanel(id,html){const p=id.slice(2);if(!PW[p]||p==='map')return html;const rows=html.split('\n');const n=rows.length;
 if(n>=(PH[id]||0)){PH[id]=n;return html}const blank=seg(H('| '))+' '.repeat(PW[p]-4)+seg(H(' |'));return [...rows.slice(0,-1),...Array(PH[id]-n).fill(blank),rows[n-1]].join('\n')}
/* panels update line by line: only lines whose content changed are replaced, so a button
   that didn't change stays the same element (keeps hover, focus and a press in progress) */
const lineCache={};
function put(id,html){html=padPanel(id,html);if(cache[id]===html)return;const el=document.getElementById(id);if(!el)return;
 const act=document.activeElement;const inp=el.querySelector('#impin');
 const rows=html.split('\n'),old=lineCache[id];
 if(old&&old.length===rows.length&&el.children.length===rows.length){for(let i=0;i<rows.length;i++)if(rows[i]!==old[i]&&!(inp&&el.children[i].contains(inp)))el.children[i].innerHTML=rows[i]}
 else{const fa=act&&el.contains(act)&&act.dataset?act.dataset.a:null;el.innerHTML=rows.map(r=>'<span class="ln">'+r+'</span>').join('\n');
  /* keep the paste box itself (its text and focus) across a full redraw */
  if(inp){const ni=el.querySelector('#impin');if(ni){ni.replaceWith(inp);if(act===inp)inp.focus({preventScroll:true})}}
  if(fa){const n=el.querySelector(`[data-a="${fa}"]`);if(n)n.focus({preventScroll:true})}}
 lineCache[id]=rows;cache[id]=html}
let lastTitle='';function title(){const s=(kurPos?(Date.now()%1000<500?'(!) KURENT · ':'(.) KURENT · '):'')+fmt(Math.floor(S.sit))+' SIT · Občine';if(s!==lastTitle){document.title=s;lastTitle=s}}
let srKey='';function sr(){const s=srSummary();if(s!==srKey){document.getElementById('srsum').textContent=s;srKey=s}}
const FAST={bell:1};let lastSlow=0;
function render(force){const now=performance.now();const slow=force||now-lastSlow>250;if(slow)lastSlow=now;
 put('head',pHead());title();sr();renderDock();for(const id in PAN)if(PW[id]&&(slow||FAST[id]))put('p-'+id,PAN[id](PW[id]));drawMap();mapInfo()}
function full(){cache={};for(const k in lineCache)delete lineCache[k];mapKey='';infoKey='';render(true)}
let dockHTML='',bellSeen=true;const bellIO=new IntersectionObserver(es=>{for(const e of es)bellSeen=e.isIntersecting});let bellObserved=null;
function renderDock(){const d=document.getElementById('dock');const be=document.getElementById('p-bell');if(be&&be!==bellObserved){bellIO.disconnect();bellIO.observe(be);bellObserved=be}
 const on=MODE.startsWith('1')&&!bellSeen;d.hidden=!on;document.body.classList.toggle('docked',on);if(!on)return;
 const w=PW.bell||49;const left=tr('tolarji ','tolars ')+fmt(Math.floor(S.sit));const right='+'+fmt(ips(),1)+'/s';const btnT=tr('[  Z V O N I  ]','[  R I N G  ]');
 const mx=xf(meterMult()),mlab=tr('zvonjenje ','ringing ');
 const top=esc('+'+'-'.repeat(w-2)+'+')+'\n'+esc('| '+padR(left,w-L(right)-4)+right+' |')+'\n'+esc('| '+mlab+bar(meter,w-L(mlab)-L(mx)-7)+' '+mx+' |')+'\n';
 const btn_='<span class="b ring" data-a="ring" role="button" tabindex="0" aria-label="'+esc(tr('Pozvoni','Ring the bell'))+'">'+esc(' '.repeat(w))+'\n'+esc(padR(' '.repeat(Math.floor((w-L(btnT))/2))+btnT,w))+'\n'+esc(' '.repeat(w))+'</span>';
 if(btn_!==dockHTML){d.innerHTML='<span aria-hidden="true" id="dockstat"></span>'+btn_;dockHTML=btn_}
 const ds=document.getElementById('dockstat');if(ds.innerHTML!==top)ds.innerHTML=top;placeToast()}

/* ================= INPUT ================= */
function copy(text,ok){try{navigator.clipboard.writeText(text).then(()=>flash=ok,()=>flash=tr('kopiranje ni uspelo.','copying failed.'))}catch(e){flash=tr('kopiranje ni uspelo.','copying failed.')}}
function act(a){if(!a)return;
 if(a==='ring')return ring();
 if(a==='unlock'){unlock();return}
 if(a==='all'){let k=0;const f=S.n;while(unlock(true))k++;if(k){log(tr('odklenjenih ','unlocked ')+k+': '+O[f].n+(k>1?' … '+O[S.n-1].n:''));ding(660,.05)}return}
 if(a==='kurent')return catchKurent();
 if(a.startsWith('amt')){S.amt=a==='amtmax'?'max':+a.slice(3);return}
 if(/^g\d+$/.test(a))return buyGen(+a.slice(1));
 if(a==='upall'){let k=0;for(const u of upgrades()){if(u.cost<=S.sit){S.sit-=u.cost;S.ups.push(u.id);k++}}if(k){log(tr('kupljenih izboljšav: ','upgrades bought: ')+k);ding(1175,.05)}return}
 if(a.startsWith('ama'))return referendum(a.slice(2));
 if(a[0]==='u')return buyUp(a.slice(1));
 if(a.startsWith('pg')){const v=+a.slice(2);const rows=MODE.startsWith('1')?10:16;if(v===0)regPage=null;else regPage=Math.max(0,Math.min(O.length-rows,(regPage===null?Math.max(0,Math.min(O.length-rows,S.n-Math.floor(rows/2))):regPage)+v));return}
 if(a.startsWith('ach'))return achPage+=+a.slice(3);
 if(a==='ref'){const offer=offerAmendments();if(offer.length)refPick=offer;else refArm=Date.now()+5000;return}
 if(a==='refno'){refArm=0;refPick=null;return}if(a==='refyes'){refArm=0;return referendum(null)}
 if(a==='snd'){S.sound=S.sound?0:1;return}
 if(a==='thm'){S.light=S.light?0:1;document.documentElement.classList.toggle('light',!!S.light);return}
 if(a==='lng'){LANG=S.lang=LANG==='en'?'sl':'en';document.documentElement.lang=LANG;PH={};full();return}
 if(a==='exp')return copy(btoa(unescape(encodeURIComponent(JSON.stringify(S)))),tr('igra je kopirana. prilepi jo na drugi napravi.','game copied. paste it on the other device.'));
 if(a==='stats')return copy(statsText(),tr('statistika je kopirana.','stats copied.'));
 if(a==='imp'){const v=(document.getElementById('impin')||{}).value||'';try{const s=migrate(JSON.parse(decodeURIComponent(escape(atob(v.trim())))));if(!s)throw 0;S=s;flash=tr('igra naložena.','game loaded.');save();full()}catch(e){flash=tr('to ni veljavna shranjena igra.','that is not a valid saved game.')}return}
 if(a==='rst'){resetArm=Date.now()+4000;return}
 if(a==='rstyes'){const keep={sound:S.sound,light:S.light,lang:S.lang};S=Object.assign(fresh(),keep);resetArm=0;log(tr('nova igra. pozvoni!','new game. ring the bell!'));save();full();return}}
const target=e=>{let t=e.target.closest&&e.target.closest('[data-a]');if(!t&&e.clientX!=null){const el=document.elementFromPoint(e.clientX,e.clientY);t=el&&el.closest&&el.closest('[data-a]')}return t};
let downA=null;
document.addEventListener('pointerdown',e=>{const t=target(e);if(!t){downA=null;return}if(e.pointerType==='mouse')e.preventDefault();
 if(t.dataset.a==='ring'||t.dataset.a==='kurent'){e.preventDefault();downA=null;act(t.dataset.a);render(true);return}downA=t.dataset.a});
document.addEventListener('pointerup',e=>{if(!downA)return;const a=downA;downA=null;const el=document.elementFromPoint(e.clientX,e.clientY);const t=el&&el.closest&&el.closest('[data-a]');
 if(t&&t.dataset.a===a){act(a);render(true)}});
document.addEventListener('pointercancel',()=>{downA=null});
document.getElementById('toast').addEventListener('click',()=>nextToast());
/* clicks without a pointer (screen readers, keyboard-synthesised) */
document.addEventListener('click',e=>{if(e.detail!==0)return;const t=e.target.closest&&e.target.closest('[data-a]');if(!t)return;act(t.dataset.a);render(true)});
let typed='';
document.addEventListener('keydown',e=>{if(e.target.id==='impin')return;
 if((e.key==='Enter'||e.key===' ')&&e.target.dataset&&e.target.dataset.a){e.preventDefault();if(!e.repeat){act(e.target.dataset.a);render(true)}return}
 if(e.code==='Space'){e.preventDefault();if(!e.repeat){ring();render(true)}return}
 if(e.key==='n'||e.key==='N'){unlock();render(true)}
 typed=(typed+e.key.toLowerCase()).slice(-7);if(typed==='triglav'&&!S.ach.includes('tri'))gotAch(ACH.find(a=>a[0]==='tri'))});
document.addEventListener('mouseover',e=>{const c=e.target.closest&&e.target.closest('#mapgrid i');if(!c)return;const i=+c.className.match(/c(\d+)/)[1];
 if(i!==hover){hover=i;document.getElementById('hov').textContent=`#mapgrid .c${i}{background:var(--fg);color:var(--bg)}`;mapInfo()}});
document.addEventListener('mouseout',e=>{if(e.target.closest&&e.target.closest('#mapgrid')&&!(e.relatedTarget&&e.relatedTarget.closest&&e.relatedTarget.closest('#mapgrid'))){hover=-1;document.getElementById('hov').textContent='';mapInfo()}});

/* ================= LOOP ================= */
function spawnKurent(){const M=mapFor(PW.map||48);const cells=[];for(let y=0;y<M.H-3;y++)for(let x=0;x<M.W-4;x++)if(M.g[y][x]>=0&&M.g[y+2][x+3]>=0)cells.push([x,y]);
 if(!cells.length)return;kurPos=cells[Math.floor(Math.random()*cells.length)];kurGone=Date.now()+KC.stay;drawMap(true);ding(392,.05,.4);setTimeout(()=>ding(392,.05,.4),180)}
function eventToasts(){const d=new Date(window.__date||Date.now());const md=(d.getMonth()+1)*100+d.getDate();
 const day=WEEK[d.getDay()];if(!S.days.includes(d.getDay()))S.days.push(d.getDay());const dk=d.toDateString();
 if(S.evSeen.day!==dk){S.evSeen.day=dk;toast('ev',tr('Danes: ','Today: ')+evName(day),evDesc(day)+'.',null);log(tr('danes: ','today: ')+evName(day)+' ('+evDesc(day)+')')}
 for(const e of holidaysNow()){const y=d.getFullYear()-(md<e.from[0]*100+e.from[1]?1:0);if(S.evSeen[e.id]!==y){S.evSeen[e.id]=y;toast('ev',evName(e),evDesc(e)+'.',regionChime);log(tr('praznik: ','event: ')+evName(e)+' ('+evDesc(e)+')')}}}
let last=performance.now(),saveT=0,achT=0,partT=0,evT=0;
function tick(){const now=performance.now(),dt=Math.min(3600,(now-last)/1000);last=now;if(Date.now()-lastRingT>GRACE)meter=Math.max(0,meter-dt/DRAIN_S);const g=ips()*dt;S.sit+=g;S.life+=g;S.all+=g;S.play+=dt;
 if((partT+=dt)>.08){partT=0;parts.forEach(p=>p.age++);while(parts.length&&parts[0].age>14)parts.shift();if(swing>0)swing--}
 const t=Date.now();
 if(!kurPos&&t>kurNext&&S.n>=3){spawnKurent();kurNext=t+(KC.every[0]+Math.random()*(KC.every[1]-KC.every[0]))*(has(kurLm.id)?KC.ptujEvery:1)*(am('a2')?.5:1)*evKur()}
 if(kurPos&&t>kurGone){kurPos=null;drawMap(true)}
 if((achT+=dt)>1){achT=0;checkAch()}
 if((evT+=dt)>60){evT=0;eventToasts()}
 if((saveT+=dt)>5){saveT=0;save()}
 render()}

/* ================= TEST HOOK ================= */
window.__dbg={get meter(){return meter},get voices(){return voices.length},get jvoices(){return jvoices.length},boost(k,ms){if(k==='kur')kurUntil=Date.now()+ms;else clkUntil=Date.now()+ms},spawn(){spawnKurent()}};

/* ================= START ================= */
document.documentElement.classList.toggle('light',!!S.light);document.documentElement.lang=LANG;
{const away=(Date.now()-S.save)/1000;if(away>60&&baseIps()>0){const full_=am('a9');const g=baseIps()*Math.min(away,(full_?12:8)*3600)*(full_?1:.5);S.sit+=g;S.life+=g;S.all+=g;
 log(tr('med odsotnostjo (','while away (')+dur(away)+'): +'+fmt(g)+' SIT')}}
if(!S.log.length)log(tr('dobrodošli. pozvoni, kupi njivo, odkleni Osilnico.','welcome. ring the bell, buy a field, unlock Osilnica.'));
const ro=new ResizeObserver(()=>{layout();render();placeToast()});ro.observe(document.documentElement);
(document.fonts?document.fonts.ready:Promise.resolve()).then(()=>{MODE='';layout();full()});
layout();full();setInterval(tick,100);setTimeout(eventToasts,1500);
addEventListener('visibilitychange',()=>{if(document.hidden)save()});addEventListener('pagehide',save);
}
