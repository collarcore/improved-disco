import json,math
d=sorted(json.load(open('data/obcine.json')),key=lambda o:o['p'])
IDX={o['n']:i for i,o in enumerate(d)}
GEN=[('Njiva',15,.1,0),('Kozolec',100,1,2),('Čebelnjak',1100,8,8),('Gostilna',12e3,47,18),('Vinska klet',130e3,260,30),
('Žaga',1.4e6,1400,45),('Rudnik',20e6,7800,62),('Toplice',330e6,44e3,80),('Smučišče',5.1e9,260e3,100),
('Tovarna',75e9,1.6e6,120),('Pristanišče',1e12,10e6,142),('Nuklearka',14e12,65e6,163)]
TIERS=[(10,10),(25,100),(50,1e4),(100,1e6),(150,1e8),(200,1e10)]
# landmark: obcina, kind, target, value
LM=[('Solčava','gen',0,2),('Kostel','click',0,2),('Šentrupert','gen',1,3),('Bovec','gen',3,2),('Ankaran','glob',0,1.1),
('Mežica','gen',6,2),('Kobarid','gen',3,3),('Žirovnica','gen',2,3),('Radenci','gen',7,2),('Kranjska Gora','gen',8,2),
('Žiri','pct',0,.01),('Bohinj','glob',0,1.15),('Brda','gen',4,3),('Vipava','gen',4,2),('Moravske Toplice','gen',7,2),
('Cerklje na Gorenjskem','gen',8,2),('Bled','gen',3,2),('Metlika','gen',4,2),('Ribnica','gen',5,3),('Lendava','gen',6,2),
('Idrija','gen',6,3),('Rogaška Slatina','gen',7,3),('Ormož','gen',4,2),('Laško','gen',3,2),('Sežana','pct',0,.02),
('Kočevje','gen',5,2),('Trbovlje','gen',6,2),('Izola','gen',10,2),('Postojna','glob',0,1.25),('Piran','gen',10,2),
('Murska Sobota','gen',0,5),('Radovljica','gen',2,2),('Škofja Loka','glob',0,1.1),('Ptuj','kur',0,1),('Krško','gen',11,3),
('Kamnik','gen',8,2),('Nova Gorica','glob',0,1.1),('Velenje','gen',9,2),('Novo mesto','gen',9,3),('Celje','glob',0,1.25),
('Koper','gen',10,3),('Kranj','pct',0,.03),('Maribor','gen',4,3),('Ljubljana','glob',0,2)]
for l in LM: assert l[0] in IDX,l
regs={}
for o in d: regs[o['r']]=regs.get(o['r'],0)+1
