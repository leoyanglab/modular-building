from pathlib import Path
import json,hashlib
R=Path(__file__).resolve().parents[1];target=R/'public/_pdf';target.mkdir(exist_ok=True)
# The large print edition is served as a single PDF through the Worker.
manifest={}
for kind in ['digital','print']:
 f=R/f'output/pdf/katalog-{kind}.pdf';b=f.read_bytes();sha=hashlib.sha256(b).hexdigest();parts=[]
 for i,start in enumerate(range(0,len(b),4*1024*1024)):
  name=f'{kind}-{sha[:12]}-{i}.bin';part=b[start:start+4*1024*1024];(target/name).write_bytes(part);parts.append({'path':'/_pdf/'+name,'size':len(part)})
 manifest[f'/downloads/katalog-{kind}.pdf']={'size':len(b),'sha256':sha,'parts':parts}
 old=R/f'public/downloads/katalog-{kind}.pdf'
 if old.exists():old.unlink()
(R/'src/pdf-manifest.json').write_text(json.dumps(manifest,indent=2))
keep={p['path'].split('/')[-1] for m in manifest.values() for p in m['parts']}
for f in target.glob('*.bin'):
 if f.name not in keep:f.unlink()
print({k:v['size'] for k,v in manifest.items()})
