from pathlib import Path
import re,json
import pypdfium2 as pdf
R=Path(__file__).resolve().parents[1]
B=Path('/Users/leo/Library/Containers/com.tencent.xinWeChat/Data/Documents/xwechat_files/yangshengkai_5bfb/temp/RWTemp/2026-09/b7aa62d6d3c6296cce2a579250839d17')
files={'meishu':'广东美墅产品画册.pdf','mengmeng':'美墅萌萌屋吊装产品介绍2026.pdf'}
# Explicit model names in Serbian/Latin transliteration; never infer a model from its picture.
names={12:'Linglong 8 · 1',13:'Linglong 8 · 2',14:'Linglong Round · 1',15:'Linglong Round · 2',16:'Linglong Tall',17:'Tea House',18:'Ye Wu',19:'Lin Su',20:'Shu Sha',21:'Mushroom · 1',22:'Mushroom · 2',23:'Dao Xiang Ju',24:'Luo Xin',25:'Ai Chao',26:'Ye Ju',27:'Yi Ju',28:'Ling Xiao',29:'Honeycomb',30:'Yun Xiao',32:'Tu Yu',33:'Jian Ju · 1',34:'Jian Ju · 2',35:'Yuan Ye',36:'Geometry · 2',37:'Yun She',38:'Gui Chao · L',39:'Gui Chao · S',40:'Chun Shu',41:'Xie Yu Zhu',42:'Yuan Wang',43:'Ya Ju · 1',44:'Ya Ju · 2',45:'Qing She',46:'Ya Ge',47:'An Hei',48:'Shan She',50:'Su Xi',51:'Shui Wu',52:'Sydney · 1',53:'Sydney · 2',54:'Yu Su',56:'Bi Yu Ge',57:'Qing Feng',58:'Ben Xin',59:'Qi Yu',60:'Xing Su',66:'Fairytale Boat A',67:'Fairytale Boat B',68:'Fairytale Boat C',69:'Magic Tree A',70:'Magic Tree B',71:'Magic Tree C',72:'Gui Yu',73:'Jun Xi',74:'Lin Yin',75:'Lin Feng',76:'Noah',77:'Tropical House',78:'Fairytale Castle · 1',79:'Fairytale Castle · 2',80:'Fan Hua',81:'Oval Egg',82:'Acorn A',83:'Acorn B',84:'Acorn C',85:'Zhu Lang B',86:'Zhu Lang C',88:'Chinese Courtyard',89:'Ye Wu Courtyard',90:'Ya Ju Courtyard',91:'Zhu Xi Courtyard',92:'Qi Yu Courtyard',93:'Xiang Yun Courtyard'}
mn={8:'X3',9:'X5',10:'X6',11:'X7',12:'V6',13:'M9',14:'M18',15:'M25',16:'M28',17:'M31',20:'S3',21:'P3',22:'P5',23:'P6',24:'P7',28:'Ya Ju H',29:'Camp No. 2',30:'Lunar',31:'Egg',32:'Yun Ju H',33:'Shui An 1',34:'Sydney H',35:'Shui Wu H',36:'Fang She A',37:'Fang She B',38:'Jing Xi Ju',39:'Shu Sha H',40:'Yi Ju H',41:'Niao Chao H',42:'Chao Ju H',43:'Ya Qi · 4.0',44:'Ya Qi · 3.5',45:'Xiang Yun H',46:'BOX · 4',47:'Magic Box',48:'Shi Guang · M'}
def number(t,pattern):
 m=re.search(pattern,t,re.I);return m.group(1) if m else None
def fmt(v):return v.replace('.',',')+' m²' if v else 'Na upit'
def category(page):
 return 'Kuće u prirodi' if page<=30 else 'Savremene kuće' if page<=48 else 'Kuće uz vodu' if page<=54 else 'Azijski stil' if page<=60 else 'Novi koncepti' if page<=86 else 'Dvorišne celine'
desc={'Kuće u prirodi':'Organske forme i prepoznatljiva silueta za odmor u prirodi.','Savremene kuće':'Savremena arhitektura za privatni odmor ili turistički smeštaj.','Kuće uz vodu':'Koncept boravka uz vodu, sa pogledom ka prirodnom okruženju.','Azijski stil':'Arhitektonski koncept inspirisan savremenim azijskim stilom.','Novi koncepti':'Idejni model za turistički smeštaj sa posebnim karakterom.','Dvorišne celine':'Kompozicija objekata i otvorenog prostora za celovit projekat.','Gotove kabine':'Fabrički pripremljena kabina iz kolekcije za transport i podizanje dizalicom.','Svemirske kapsule':'Kapsula iz kolekcije Mengmengwu za odmor i turistički smeštaj.','Apple kabine':'Apple kabina iz kolekcije Mengmengwu sa modularnim rasporedom.'}
records=[]
for key,mapping in [('meishu',names),('mengmeng',mn)]:
 text=(R/f'tmp/pdfs/{key}.txt').read_text().split('\f');d=pdf.PdfDocument(str(B/files[key]))
 for page,name in mapping.items():
  t=text[page-1];cat=category(page) if key=='meishu' else ('Svemirske kapsule' if page<18 else 'Apple kabine' if page<25 else 'Gotove kabine')
  interior=number(t,r'Interior\s+(?:Floor\s+)?Area\s*[：:]\s*([\d.]+)')
  area=number(t,r'Product\s+Area\s*[：:]\s*([\d.]+)') if key=='mengmeng' else None
  footprint=number(t,r'Building projection area\s*[：:]\s*([\d.]+)')
  dim=number(t,r'(?:Dimensions[^：:\n]*[：:]\s*)([^\n]+)')
  if dim:
   dim=re.split(r'\s{3,}',dim)[0].strip();dim=dim if re.search(r'\d',dim) else None
   if dim:dim=re.sub(r'\([LWH]\)','',dim).replace('x',' × ').replace('.',',').strip()
  weight=number(t,r'Approximate Total Weight\s*[：:]\s*([\d.]+)')
  note=''
  if key=='mengmeng' and page==12:note='Razlika u izvorima: detaljni list navodi 37 m² i visinu 5,1 m; drugi katalog navodi 38 m² i 5,2 m. Potvrditi pre ponude.'
  if key=='mengmeng' and page==15:note='Detaljni list navodi 25 m², pregled serije 21 m². Za ponudu je potrebna potvrda proizvođača.'
  if key=='mengmeng' and page==17:note='Model je označen kao M31 u kineskom naslovu i pregledu, a kao M25 u engleskom naslovu detaljnog lista. Potvrditi oznaku.'
  if key=='mengmeng' and page in [20,23,45]:
   note='Podaci o dimenzijama ili rasporedu nisu potpuno usklađeni u izvornom listu. Konačne mere i konfiguraciju potvrditi pre ponude.';dim=None
  if key=='meishu' and page==52:note='Izvor navodi unutrašnju površinu veću od projekcione površine; obe vrednosti treba proveriti pre ponude.'
  pid=f'{key}-{page}'; im=d[page-1].render(scale=1.6 if key=='meishu' else 1).to_pil().convert('RGB');w,h=im.size
  # Isolate the product photo panel, preserving supplier watermarks.
  im=im.crop((0,0,int(w*.5),h)) if key=='meishu' else im.crop((round(w*548/1536),0,w,h))
  im.thumbnail((1800,1800));im.save(R/f'assets/source/{pid}.jpg',quality=92)
  r={'id':pid,'name':name,'category':cat,'area':fmt(area or interior or footprint),'areaLabel':'Površina modela' if area else 'Unutrašnja površina' if interior else 'Projekciona površina' if footprint else 'Površina nije navedena','interior':fmt(interior) if interior else None,'footprint':fmt(footprint) if footprint else None,'dimensions':dim,'weight':weight+' t' if weight else None,'note':note,'image':pid,'source':files[key]+f' / PDF p.{page}','supplier':'Meishu / Mengmengwu','description':desc[cat]}
  if key=='mengmeng' and page in [9,11,12]:r['source']+=f'; 广东美墅产品画册.pdf / PDF p.{ {9:62,11:63,12:64}[page]}'
  if key=='meishu' and page in [42,45,51]:r['terrace']={42:'113,2 m²',45:'24,2 m²',51:'64,6 m²'}[page]
  records.append(r)
(R/'assets/meishu-products.json').write_text(json.dumps(records,ensure_ascii=False,indent=2))
print('Imported',len(records),'distinct model records',flush=True)
