from pathlib import Path
import pypdfium2 as pdf
from PIL import Image,ImageDraw
from pypdf import PdfReader
import json
R=Path(__file__).resolve().parents[1];p=R/'output/pdf/katalog-print.pdf';d=pdf.PdfDocument(str(p));assert len(d)==244
for start in range(0,len(d),36):
 board=Image.new('RGB',(1260,1782),'#ddd')
 for i,n in enumerate(range(start,min(start+36,len(d)))):
  im=d[n].render(scale=.5).to_pil().convert('RGB');im.thumbnail((210,297));board.paste(im,(i%6*210,i//6*297))
 board.save(R/f'tmp/pdfs/luxury-review-{start//36}.jpg')
for n in [1,2,3,5,6,9,40,100,200,244]:d[n-1].render(scale=1).to_pil().save(R/f'tmp/pdfs/luxury-page-{n}.png')
a=PdfReader(p);b=PdfReader(R/'output/pdf/katalog-digital.pdf');ta=[p.extract_text() for p in a.pages];tb=[p.extract_text() for p in b.pages];assert ta==tb
joined='\n'.join(ta)
for r in json.loads((R/'public/products.json').read_text()):assert r['code'] in joined,r['code']
print('244 pages rendered; both editions match; all 219 codes present')
