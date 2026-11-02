from pathlib import Path
import json,re
import pypdfium2 as pdf
from PIL import ImageChops,Image
R=Path(__file__).resolve().parents[1];B=Path('/Users/leo/Library/Containers/com.tencent.xinWeChat/Data/Documents/xwechat_files/yangshengkai_5bfb/temp/RWTemp/2026-09/b7aa62d6d3c6296cce2a579250839d17')
products=json.loads((R/'public/products.json').read_text());byid={p['id']:p for p in products}
files={'zx':'创意集装箱及苹果舱产品介绍.pdf','sc':'双层创意集装箱款式.pdf','meishu':'广东美墅产品画册.pdf','mengmeng':'美墅萌萌屋吊装产品介绍2026.pdf'}
docs={k:pdf.PdfDocument(str(B/f)) for k,f in files.items()};texts={k:(R/f'tmp/pdfs/{v}.txt').read_text().split('\f') for k,v in {'zx':'source-0','sc':'source-1','meishu':'meishu','mengmeng':'mengmeng'}.items()}
def crop(k,n,rect,out):
 im=docs[k][n-1].render(scale=1.5 if k!='sc' else 1).to_pil().convert('RGB');w,h=im.size;im=im.crop(tuple(round(v*(w if i%2==0 else h)) for i,v in enumerate(rect)));im.thumbnail((1800,1800));im.save(R/f'assets/source/{out}.jpg',quality=92)
zxpages=list(range(12,30))+list(range(31,50))+list(range(51,70));existing={58:'space38',59:'space28',62:'apple33'}
names=['Market 01','Market 02','Community','Office 01','Office 02','Resort','Ticket & Storage','Office 03','Café Duo','Office 04','Library','Mobile Home','Commercial Plaza','Café 01','Café 02','Café 03','Breakfast','Retail', 'Apple Office','Apple Lounge','Apple Station','Apple Stay','Apple Shop','Community Station','Stay 01','Tech 01','Outdoor Station','Showroom','Stay 03','Apple Rest','Apple Gallery','Apple Duo','Apple Mobile','Apple Studio','Apple Reception','Apple Camp','Self-service Shop','Retail 36','Stay 24','Stay 12','Kiosk 09','Sanitary 30','Office 36','Camp 27','Space 38','Space 28','Smoking Lounge','Studio 09','Apple 33','Apple Stay 33','Meeting 05','Lounge 78','Service 18','Service 56','Reading 36','Café 18']
assert len(names)==len(zxpages)
for n,name in zip(zxpages,names):
 code=f'ZX-{n:02}';pid=existing.get(n,'zx-'+str(n));t=texts['zx'][n-1]
 if pid in byid:p=byid[pid]
 else:
  dims=re.search(r'尺\s*寸\s*[：:]\s*([^\n]+)',t);dims=dims.group(1).strip() if dims else None
  if dims:dims=re.sub(r'\s+','',dims).replace('M','m').replace('x',' × ').replace('×',' × ')
  ar=re.search(r'面积\s*[：:]\s*([\d\s.]+)平',t);area=re.sub(r'\s','',ar.group(1)) if ar else None
  cat='Poslovni moduli' if n<30 or n in [51,55,67,69] else 'Apple kabine'
  p={'id':pid,'name':name,'category':cat,'area':area.replace('.',',')+' m²' if area else 'Na upit','areaLabel':'Površina prema katalogu' if area else 'Površina nije navedena','dimensions':dims,'image':pid,'description':'Modularni prostor iz kolekcije Zhongxin. Namena i završna konfiguracija određuju se prema odabranom projektu.','supplier':'Zhongxin','source':files['zx']+f' / PDF p.{n}'}
  crop('zx',n,(.017,.19,.604,.937) if n<50 else (.44,.177,.981,.969),pid);products.append(p);byid[pid]=p
 p['code']=code;p['aliases']=[code];p['sourceRefs']=[{'document':'zx','page':n}]
 if n==32:p['note']='Katalog prikazuje dve dimenzijske varijante. Konačnu varijantu i mere potvrditi pre ponude.';p['dimensions']=None
for n in range(2,54):
 code=f'SC-{n-1:02}';pid={8:'duplex72',12:'duplex96'}.get(n,'sc-'+str(n-1));t=texts['sc'][n-1];area=re.search(r'面积\s*[：:]\s*([\d.]+)',t).group(1)
 if pid in byid:p=byid[pid]
 else:
  p={'id':pid,'name':f'Duplex {n-1:02}','category':'Modularni objekti','area':area.replace('.',',')+' m²','areaLabel':'Građevinska površina','image':pid,'description':'Dvospratni modularni koncept sa prepoznatljivim arhitektonskim izrazom. Za ugostiteljski, prodajni ili višenamenski projekat.','supplier':'Zhongxin','source':files['sc']+f' / PDF p.{n}'}
  crop('sc',n,(0,.137,.622,.874),pid);products.append(p);byid[pid]=p
 p['code']=code;p['aliases']=[code,f'双层{n-1:02}',f'Duplex {n-1:02}'];p['sourceRefs']=[{'document':'sc','page':n}]
 # Two additional manufacturer views for the product detail.
 crop('sc',n,(.68,.34,.9,.88),pid+'-detail');p['gallery']=[pid+'-detail']
for p in products:
 if p['id'].startswith(('meishu-','mengmeng-')):
  k,n=p['id'].split('-');n=int(n);p['code']=('MS' if k=='meishu' else 'MM')+f'-{n:02}';p['sourceRefs']=[{'document':k,'page':n}];p['aliases']=[p['code']]
  if k=='meishu':
   p['aliases'].append(texts[k][n-1].strip().splitlines()[0].strip());crop(k,n,(.52,.17,.98,.56),p['id']+'-plan');crop(k,n,(.52,.588,.985,.976),p['id']+'-detail');p['gallery']=[p['id']+'-detail'];p['plan']=p['id']+'-plan'
  if k=='mengmeng' and n in [9,11,12]:p['sourceRefs'].append({'document':'meishu','page':{9:62,11:63,12:64}[n]})
for tag,name,area,rect in [('large','Shi Guang · L','57',(.035,.49,.25,.64)),('small','Shi Guang · S','25',(.477,.49,.641,.64))]:
 pid='mengmeng-shiguang-'+tag;crop('mengmeng',26,rect,pid)
 products.append({'id':pid,'name':name,'code':'MM-SG-'+tag.upper(),'aliases':['拾光'+('大' if tag=='large' else '小'),name],'category':'Gotove kabine','area':area+' m²','areaLabel':'Površina modela','image':pid,'source':files['mengmeng']+' / PDF p.26','sourceRefs':[{'document':'mengmeng','page':26,'variant':tag}],'supplier':'Meishu / Mengmengwu','description':'Dodatna veličina modela Shi Guang, prikazana u pregledu kolekcije.','note':'Model je prikazan u pregledu serije; detaljne mere i specifikacija nisu navedene.'})
# Meishu concept pages have no reliable isolated plan/interior panel: retain full model picture only.
for p in products:
 if p['id'].startswith('meishu-') and int(p['id'].split('-')[1])>=66:p.pop('plan',None);p.pop('gallery',None)
(R/'assets/catalog-products.json').write_text(json.dumps(products,ensure_ascii=False,indent=2))
coverage={k:sorted({r['page'] for p in products for r in p.get('sourceRefs',[]) if r['document']==k}) for k in docs}
assert coverage['zx']==zxpages
assert coverage['sc']==list(range(2,54))
(R/'assets/source-coverage.json').write_text(json.dumps({'models':len(products),'documents':files,'productPages':coverage,'notes':['X5/X7/V6 linked across both Meishu documents.','Shi Guang large/small included from overview page 26.','Company profiles, general claims and project case studies are not separate product models.']},ensure_ascii=False,indent=2))
print('COMPLETE',len(products),{k:len(v) for k,v in coverage.items()})
