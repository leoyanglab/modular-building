from pathlib import Path
from collections import OrderedDict
from PIL import Image
import io,json,math
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import HexColor
from reportlab.lib.utils import ImageReader
R=Path(__file__).resolve().parents[1];data=json.loads((R/'public/products.json').read_text());byid={p['id']:p for p in data}
for name,file in [('Sans','Arial.ttf'),('Bold','Arial Bold.ttf'),('Serif','Georgia.ttf'),('Italic','Georgia Italic.ttf')]:pdfmetrics.registerFont(TTFont(name,'/System/Library/Fonts/Supplemental/'+file))
W,H=595.276,841.89;dark='#202622';paper='#f3f0e9';gold='#b99e71';gray='#777a70'
order=['Svemirske kapsule','Apple kabine','Gotove kabine','Kuće u prirodi','Savremene kuće','Kuće uz vodu','Azijski stil','Novi koncepti','Dvorišne celine','Modularni objekti','Poslovni moduli']
groups=OrderedDict((k,[p for p in data if p['category']==k]) for k in order)
features={'meishu-12','meishu-18','meishu-33','meishu-37','meishu-38','meishu-43','meishu-51','sc-36'}
lead={'Svemirske kapsule':'mengmeng-11','Apple kabine':'apple33','Gotove kabine':'mengmeng-36','Kuće u prirodi':'meishu-12','Savremene kuće':'meishu-38','Kuće uz vodu':'meishu-51','Azijski stil':'meishu-58','Novi koncepti':'meishu-76','Dvorišne celine':'meishu-89','Modularni objekti':'sc-36','Poslovni moduli':'zx-15'}
starts={};page=5
for k,ps in groups.items():starts[k]=page;page+=1+len(ps)+sum(p['id'] in features for p in ps)
total=page+1
assert total%4==0,total

def build(printing):
 out=R/'output/pdf'/('katalog-print.pdf' if printing else 'katalog-digital.pdf');c=canvas.Canvas(str(out),pagesize=(W,H),pageCompression=1);c.setTitle('Arhitektura odmora | Kompletna kolekcija');c.setAuthor('Modularni prostori');c.setSubject('219 modela | Arhitektonska kolekcija | Srpski, latinica');n=0; cache={}
 def rect(x,y,w,h,col):c.setFillColor(HexColor(col));c.rect(x,H-y-h,w,h,stroke=0,fill=1)
 def text(s,x,y,size=11,font='Sans',col=dark):c.setFillColor(HexColor(col));c.setFont(font,size);c.drawString(x,H-y-size,s)
 def para(s,x,y,width,size=11,leading=17,col=gray):
  line=''
  for word in s.split():
   test=(line+' '+word).strip()
   if pdfmetrics.stringWidth(test,'Sans',size)>width and line:text(line,x,y,size,col=col);y+=leading;line=word
   else:line=test
  if line:text(line,x,y,size,col=col);y+=leading
  return y
 def photo(key,x,y,w,h):
  if key not in cache:
   im=Image.open(R/f'assets/source/{key}.jpg').convert('RGB');im.thumbnail((1500,1500) if printing else (950,950));buf=io.BytesIO();im.save(buf,'JPEG',quality=85 if printing else 67,optimize=True);buf.seek(0);cache[key]=(ImageReader(buf),im.size)
  reader,(iw,ih)=cache[key];scale=min(w/iw,h/ih);ww=iw*scale;hh=ih*scale;c.drawImage(reader,x+(w-ww)/2,H-y-(h+hh)/2,ww,hh)
 def start(label,black=False):
  nonlocal n;n+=1;rect(0,0,W,H,dark if black else paper);text('MODULARNI PROSTORI',32,26,8,'Bold',gold);text(label,335,27,7,col='#c6c2b6' if black else gray);rect(32,53,W-64,.6,gold)
 def footer(black=False):
  text('ARHITEKTURA ODMORA / 2026',32,810,7,col=gold if black else gray);text(f'{n:03} / {total}',500,810,7,col=gold if black else gray);c.showPage()
 start('ARHITEKTONSKA KOLEKCIJA',True)
 text('Arhitektura',32,97,51,'Serif',paper);text('odmora.',32,158,59,'Italic',gold)
 photo('meishu-38',0,267,W,460)
 rect(32,743,45,1,gold);text('219 MODELA / JEDNA VIZIJA PROSTORA',92,736,9,'Sans',paper);footer(True)
 start('VIZIJA',True)
 text('Mesto koje',32,90,43,'Serif',paper);text('ostaje u sećanju.',32,143,43,'Italic',gold)
 para('Dobar prostor ima više od jasne funkcije. On otvara pogled, stvara osećaj pripadnosti i daje karakter celoj destinaciji.',32,225,490,15,24,'#d1d0c3')
 photo('meishu-37',32,331,325,385);rect(384,355,1,339,gold)
 for y,title,desc in [(367,'01 / LOKACIJA','Polazna tačka svake ideje.'),(471,'02 / ARHITEKTURA','Forma u dijalogu sa okruženjem.'),(583,'03 / DOŽIVLJAJ','Prostor koji se pamti.')]:
  text(title,402,y,8,'Bold',gold);para(desc,402,y+28,154,12,19,paper)
 footer(True)
 start('VODIČ KROZ KOLEKCIJU')
 text('Jedanaest poglavlja.',32,91,36,'Serif');text('Bez izostavljenih modela.',32,139,24,'Italic',gold)
 for i,(cat,ps) in enumerate(groups.items()):
  y=220+i*44;text(f'{i+1:02}',32,y,10,col=gold);text(cat,74,y-2,14,'Serif');text(f'{len(ps)} modela',394,y,9,col=gray);text(f'{starts[cat]:03}',518,y,10);rect(74,y+29,490,.5,'#d6cbbb')
  c.linkRect('',f'group-{i}',(32,H-y-31,561,H-y+5),relative=0,thickness=0)
 footer()
 start('O OVOM IZDANJU')
 text('Kompletna kolekcija.',32,92,35,'Serif');text('Četiri izvorna kataloga.',32,137,26,'Italic',gold)
 para('Ovo izdanje obuhvata sve identifikovane modele iz dostavljenih produktnih materijala, uključujući varijante prikazane samo u pregledima serija.',32,211,520,12,20)
 for y,title,desc in [(320,'Zhongxin / kabine i poslovni moduli','56 produktnih i referentnih prikaza iz kolekcije kreativnih kontejnera i Apple kabina.'),(406,'Zhongxin / dvospratni objekti','Svih 52 modela iz serije, sa oznakama SC-01 do SC-52.'),(492,'Meishu / Mengmengwu','Modeli iz arhitektonske kolekcije i kataloga za transport dizalicom. X5, X7 i V6 povezani su kroz oba izvora.'),(598,'Podaci ostaju proverljivi','Oznake ove prezentacije olakšavaju identifikaciju. Površina modela, unutrašnja površina i projekciona površina prikazane su odvojeno.')]:
  text(title,32,y,13,'Bold');para(desc,32,y+27,515,11,18)
 para('Fotografije i vizualizacije su prikazi proizvođača. Nisu predstavljeni kao projekti realizovani u Srbiji.',32,747,520,9,14)
 footer()
 for ix,(cat,ps) in enumerate(groups.items()):
  start(f'POGLAVLJE {ix+1:02}',True);c.bookmarkPage(f'group-{ix}');c.addOutlineEntry(cat,f'group-{ix}',0)
  text(f'{ix+1:02}',32,81,64,'Serif',gold)
  sz=39
  while pdfmetrics.stringWidth(cat,'Serif',sz)>530:sz-=1
  text(cat,32,169,sz,'Serif',paper);text(f'{len(ps)} MODELA / OD IDEJE DO DESTINACIJE',32,231,9,col=gold)
  photo(byid[lead[cat]]['image'],0,293,W,451)
  text('Oblik. Proporcija. Karakter.',32,766,16,'Italic',paper);footer(True)
  for p in ps:
   black=False;start(cat.upper());c.bookmarkPage(p['id']);c.addOutlineEntry(p['name']+' / '+p['code'],p['id'],1)
   text(p['code'],32,78,9,'Bold',gold);sz=37
   while pdfmetrics.stringWidth(p['name'],'Serif',sz)>527:sz-=1
   text(p['name'],32,100,sz,'Serif')
   # Large, undistorted product plate: complete architecture is kept in frame.
   rect(20,156,W-40,430,'#e4e0d7');photo(p['image'],20,156,W-40,430)
   text('PROSTOR / KONCEPT',32,610,8,'Bold',gold)
   para(p['description'],32,631,518,11,17)
   specs=[(p.get('areaLabel','Površina'),p['area'])]
   for label,key in [('Unutrašnja','interior'),('Projekciona','footprint'),('Terasa','terrace'),('Dimenzije D × Š × V','dimensions'),('Približna masa','weight')]:
    if p.get(key) and p.get(key)!=p['area']:specs.append((label,p[key]))
   # Two tidy columns, up to three rows; numerical labels never run into copy.
   for j,(label,value) in enumerate(specs):
    x=32+(j%2)*273;y=689+(j//2)*26;text(label, x,y,7,col=gray);text(value,x,y+10,9,'Bold')
   end_y=689+math.ceil(len(specs)/2)*26
   if p.get('note'):
    end_y=para(p['note'],32,max(752,end_y+4),530,7,10)
    assert end_y<802,(p['id'],end_y)
   else:text((p.get('supplier') or 'Zhongxin')+' / prikaz iz kataloga proizvođača',32,788,7,col=gray)
   footer()
   if p['id'] in features:
    start('ARHITEKTURA / DETALJI',True)
    text(p['name'],32,91,35,'Serif',paper);text('Pogled izbliza.',32,138,28,'Italic',gold)
    photo(p['gallery'][0],32,210,531,329)
    rect(32,571,531,.6,gold);text('OD SPOLJAŠNJE FORME',32,594,10,'Bold',gold);text('DO DOŽIVLJAJA PROSTORA',32,614,10,'Bold',gold)
    para('Dodatni prikazi iz istog produktnog lista dopunjuju razumevanje odabranog modela. Raspored, završne obrade i oprema potvrđuju se za konkretnu konfiguraciju.',32,652,475,13,21,'#d4d2c6')
    text('MODEL / '+p['code'],32,773,8,col=gold);footer(True)
 start('OD IDEJE DO PROJEKTA',True)
 text('Vaša lokacija.',32,99,43,'Serif',paper);text('Sledeće poglavlje.',32,151,40,'Italic',gold)
 for y,num,title,desc in [(266,'01','Namena i kapacitet','Odaberite model, broj jedinica i način korišćenja.'),(365,'02','Parcela i pristup','Proverite teren, transport, temeljenje i priključke.'),(464,'03','Konfiguracija','Definišite raspored, materijale i obim opreme.'),(563,'04','Ponuda i realizacija','Potvrdite cenu, transport, uvozne troškove i rokove.')]:
  text(num,32,y,26,'Serif',gold);text(title,96,y,19,'Serif',paper);para(desc,96,y+35,456,11,18,'#c5c6ba')
 para('Uslove za konkretnu parcelu i dokumentaciju proverite sa lokalnim projektantom i nadležnim organom. Podaci iz kataloga nisu potvrda podobnosti za konkretnu lokaciju.',32,733,520,9,14,'#c5c6ba');footer(True)
 start('POČNIMO OD VAŠE IDEJE',True)
 photo('meishu-43',32,80,531,413)
 text('Mesto za vašu viziju.',32,542,34,'Serif',paper);text('modular.bool.win',32,602,26,'Serif',gold)
 c.linkURL('https://modular.bool.win',(32,H-639,360,H-592),relative=0)
 para('Istražite kompletnu kolekciju i pripremite opis projekta. Brend, kontakt podaci i komercijalni uslovi ostaju u pripremi.',32,672,500,11,18,'#c6c5bb')
 text('ARHITEKTURA ODMORA / KONCEPT IZDANJE',32,761,8,col=gold);footer(True)
 assert n==total,(n,total);c.save();print(out.name,n,out.stat().st_size,flush=True)
for printing in [False,True]:build(printing)
(R/'output/pdf/catalog-meta.json').write_text(json.dumps({'pages':total,'models':len(data),'chapters':len(groups)}))
