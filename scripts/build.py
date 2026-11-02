from pathlib import Path
from PIL import Image
import json
root=Path(__file__).resolve().parents[1]
products=json.loads((root/'assets/catalog-products.json').read_text())
for p in products:
 p.setdefault('areaLabel','Površina prema katalogu')
 for key in [p['image']]+p.get('gallery',[])+([p['plan']] if p.get('plan') else []):
  dest=root/f'public/images/{key}.webp';src=root/f'assets/source/{key}.jpg'
  if not dest.exists() or src.stat().st_mtime>dest.stat().st_mtime:
   im=Image.open(src).convert('RGB');im.thumbnail((1800,1800));im.save(dest,quality=88)
 # Maintain old id-based image paths.
 if p['image']!=p['id']:
  import shutil
  shutil.copy2(root/f'public/images/{p["image"]}.webp',root/f'public/images/{p["id"]}.webp')
(root/'public/products.json').write_text(json.dumps(products,ensure_ascii=False,indent=2))
print('Built',len(products),'models')
