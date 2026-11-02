#!/usr/bin/env python3
"""Contrôles du fonds embarqué, des crédits, des renvois et des données de carte."""
import json,re,hashlib,struct,unicodedata
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];folder=ROOT/'assets/documentation'
p=json.loads((folder/'senegal.json').read_text());articles=p['articles'];by_id={a['id']:a for a in articles}
assert len(by_id)==len(articles)==72
assert {a['subject'] for a in articles}=={'geo','history'}
assert sum(a['subject']=='geo' for a in articles)==40
assert sum(a['subject']=='history' for a in articles)==32
allowed={'p','h2','image','table','note','bullets'};images_used=set()
for a in articles:
 assert all(a[k] for k in ['id','subject','group','title','summary','objectives','blocks','sources','takeaways','activity'])
 assert a['activity']['task'] and a['activity']['answer']
 assert all(s in p['sources'] for s in a['sources'])
 assert all(r in by_id for r in a['related'])
 for b in a['blocks']:
  assert b['type'] in allowed
  if b['type']=='image':assert b['image'] in p['images'];assert b['caption'];images_used.add(b['image'])
  elif b['type']=='table':assert all(len(row)==len(b['headers']) for row in b['rows'])
  elif b['type']=='bullets':assert b['items']
  else:assert b['text'].strip()
for key,s in p['sources'].items():
 assert s['url'].startswith('https://') and all(s[k] for k in ['title','publisher','date','note','accessed']),key
for key,image in p['images'].items():
 path=ROOT/image['asset'];assert path.is_file() and path.stat().st_size>1000,key
 assert all(image[k] for k in ['author','licence','source','licenceUrl','changes']),key
 assert image['source'].startswith('https://commons.wikimedia.org/'),key
 assert image['licence'].startswith('CC') or image['licence']=='Public domain',key
assert images_used==set(p['images'])
assert len(p['map']['features'])==14
assert {f['article'] for f in p['map']['features']}=={a['id'] for a in articles if a['group']=='Les 14 régions'}
for f in p['map']['features']:
 for polygon in f['polygons']:
  for ring in polygon:
   assert ring[0]==ring[-1] and len(ring)>=4
   assert all(-17.7<x<-11.2 and 12.2<y<16.8 for x,y in ring)
for key in ['timeline','glossary']:
 assert all(row['article'] in by_id for row in p[key])
assert len(p['timeline'])==59 and len(p['glossary'])==90
assert len({g['term'] for g in p['glossary']})==90
# Correspondance des déclarations Flutter avec les nouveaux actifs (pas de répertoire récursif implicite).
pubspec=(ROOT/'pubspec.yaml').read_text();assert '    - assets/documentation/' in pubspec and '    - assets/documentation/images/' in pubspec
main=(ROOT/'lib/main.dart').read_text();assert main.index("tooltip:'Dictionnaire de poche'")<main.index("tooltip:'Documentation & Référence'")<main.index("tooltip:'Réglages et informations'")
assert '3.0 IGO' in p['map']['licence']
result={'articles':len(articles),'geography':40,'history':32,'regions':14,'sources':len(p['sources']),'images':len(p['images']),'timeline':len(p['timeline']),'glossary':len(p['glossary']),'dataBytes':(folder/'senegal.json').stat().st_size,'imageBytes':sum((ROOT/i['asset']).stat().st_size for i in p['images'].values()),'sha256':hashlib.file_digest(open(folder/'senegal.json','rb'),'sha256').hexdigest(),'validation':'OK — structure, renvois, carte, assets et crédits'}
print(json.dumps(result,ensure_ascii=False,indent=2))
