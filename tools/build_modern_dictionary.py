#!/usr/bin/env python3
"""Build the offline French reference pack. Python stdlib only; no network at build time."""
import gzip,json,sqlite3,zlib,unicodedata,re,hashlib,sys,xml.etree.ElementTree as ET
from pathlib import Path
from urllib.parse import quote
ROOT=Path(__file__).resolve().parents[1]
SOURCES=Path(sys.argv[1]) if len(sys.argv)>1 else ROOT.parent/'dictionary_sources'
OUT=ROOT/'assets/dictionary/modern.sqlite'
def norm(s):
 s=s.lower().replace('œ','oe').replace('æ','ae').replace('’',"'").replace('−','-').replace('–','-')
 return re.sub(r'\s+',' ',''.join(c for c in unicodedata.normalize('NFD',s) if not unicodedata.combining(c))).strip()
def ident(key): return 1000000000+int.from_bytes(hashlib.sha256(key.encode()).digest()[:7],'big')
def compact(x):return json.dumps(x,ensure_ascii=False,separators=(',',':'))
def packed(x):return zlib.compress(x.encode(),9)
def txt(e):return ' '.join(''.join(e.itertext()).split()) if e is not None else ''
OUT.unlink(missing_ok=True)
db=sqlite3.connect(OUT)
db.executescript('''PRAGMA journal_mode=OFF; PRAGMA synchronous=OFF; PRAGMA temp_store=FILE;
CREATE TABLE staging(id INTEGER PRIMARY KEY,word TEXT UNIQUE,sections TEXT);
CREATE TABLE pending(alias TEXT,target TEXT);
CREATE TABLE entries(id INTEGER PRIMARY KEY,headword TEXT,normalized TEXT,wordkey TEXT,letter TEXT,category TEXT,start_page INTEGER,end_page INTEGER,y REAL,paragraphs BLOB,body BLOB,refs TEXT,preview TEXT,search_body TEXT,source TEXT,source_url TEXT,licence TEXT,publication TEXT);
CREATE TABLE aliases(alias TEXT,entry_id INTEGER,PRIMARY KEY(alias,entry_id)) WITHOUT ROWID;
CREATE TABLE metadata(key TEXT PRIMARY KEY,value TEXT);
''')
counts={'frenchRecords':0,'lexicalRecords':0,'inflectedRecords':0,'senses':0}
with gzip.open(SOURCES/'fr-extract.jsonl.gz','rt') as stream:
 for line in stream:
  row=json.loads(line)
  if row.get('lang_code')!='fr':continue
  counts['frenchRecords']+=1
  word=row.get('word','').strip(); senses=row.get('senses',[])
  if not word:continue
  lexical=[s for s in senses if not s.get('form_of') and 'form-of' not in s.get('tags',[]) and s.get('glosses')]
  if not lexical:
   targets={v['word'] for s in senses for v in s.get('form_of',[]) if v.get('word')}
   if targets:
    db.executemany('INSERT INTO pending VALUES(?,?)',[(norm(word),w) for w in targets]);counts['inflectedRecords']+=1
    continue
   lexical=[s for s in senses if s.get('glosses')]
  if not lexical:continue
  section={'pos':row.get('pos_title',row.get('pos','Emploi')),'senses':[]}
  for sense in lexical:
   tags=list(dict.fromkeys(sense.get('raw_tags',[])+sense.get('tags',[])+sense.get('topics',[])))
   section['senses'].append({'glosses':sense['glosses'],'labels':tags})
   counts['senses']+=1
  section['etymology']=row.get('etymology_texts',[])
  section['ipa']=list(dict.fromkeys(s['ipa'] for s in row.get('sounds',[]) if s.get('ipa')))
  for relation in ['synonyms','antonyms','hypernyms','hyponyms','related','derived']:
   values=list(dict.fromkeys(v['word'] for v in row.get(relation,[]) if v.get('word')))
   if values:section[relation]=values
  key=ident('wiktionnaire:'+word)
  old=db.execute('SELECT word,sections FROM staging WHERE id=?',(key,)).fetchone()
  assert old is None or old[0]==word, ('Identifier collision',word,old[0])
  sections=json.loads(old[1]) if old else []
  sections.append(section)
  if old:db.execute('UPDATE staging SET sections=? WHERE id=?',(compact(sections),key))
  else:db.execute('INSERT INTO staging VALUES(?,?,?)',(key,word,compact(sections)))
  db.execute('INSERT OR IGNORE INTO aliases VALUES(?,?)',(norm(word),key))
  db.executemany('INSERT OR IGNORE INTO aliases VALUES(?,?)',[(norm(f['form']),key) for f in row.get('forms',[]) if f.get('form') and f['form']!='-'])
  counts['lexicalRecords']+=1
  if counts['frenchRecords']%50000==0:print(counts,flush=True);db.commit()
print('French extraction done',counts,flush=True)
db.execute('CREATE INDEX pending_target ON pending(target)')
db.execute('INSERT OR IGNORE INTO aliases SELECT p.alias,s.id FROM pending p JOIN staging s ON s.word=p.target')
counts['unresolvedForms']=db.execute('SELECT count(*) FROM pending p WHERE NOT EXISTS(SELECT 1 FROM staging s WHERE s.word=p.target)').fetchone()[0]
labels={'synonyms':'Synonymes','antonyms':'Antonymes','hypernyms':'Termes génériques','hyponyms':'Termes spécifiques','related':'Mots apparentés','derived':'Dérivés'}
def insert(key,word,category,paragraphs,source,url,licence,date,refs=[]):
 text='\n\n'.join(p[0]['text'] for p in paragraphs)
 n=norm(word);letter=n[:1].upper()
 if not 'A'<=letter<='Z':letter='#'
 db.execute('INSERT INTO entries VALUES('+','.join('?'*18)+')',(key,word,n,word,letter,category,0,0,0,packed(compact(paragraphs)),packed(text),compact(refs),text[:300],norm(text),source,url,licence,date))
 db.execute('INSERT OR IGNORE INTO aliases VALUES(?,?)',(n,key))
def p(text,bold=False,italic=False):return [{'text':text,'bold':bold,'italic':italic}]
for key,word,raw in db.execute('SELECT id,word,sections FROM staging'):
 sections=json.loads(raw);paragraphs=[]
 for section in sections:
  paragraphs.append(p(section['pos'],True))
  if section['ipa']:paragraphs.append(p('Prononciation : '+' · '.join(section['ipa'])))
  for i,sense in enumerate(section['senses'],1):
   label=' ['+', '.join(sense['labels'])+']' if sense['labels'] else ''
   paragraphs.append(p(str(i)+'.'+label+' '+' → '.join(sense['glosses'])))
  for text in section['etymology']:paragraphs.append(p('Étymologie : '+text,italic=True))
  for relation,label in labels.items():
   if section.get(relation):paragraphs.append(p(label+' : '+' ; '.join(section[relation])))
 refs=[]
 for section in sections:
  for relation in labels:
   for target in section.get(relation,[]):
    if len(refs)>=100:break
    found=db.execute('SELECT id FROM staging WHERE word=?',(target,)).fetchone()
    if found and found[0]!=key and not any(r['id']==found[0] for r in refs):refs.append({'id':found[0],'headword':target,'page':0,'category':'Wiktionnaire','preview':labels[relation]})
 insert(key,word,' / '.join(dict.fromkeys(s['pos'] for s in sections)),paragraphs,'Wiktionnaire','https://fr.wiktionary.org/wiki/'+quote(word,safe='')+'#fr','CC BY-SA 4.0','Dump du 01/10/2026',refs)
db.commit();print('Lexical entries materialized',flush=True)
root=ET.parse(SOURCES/'FranceTerme.xml').getroot();active={a.get('id') for a in root.findall('Article') if a.get('annule')!='1' and a.get('publie')=='1'}
for a in root.findall('Article'):
 if a.get('id') not in active:continue
 term=a.find('Terme');word=term.get('Terme','') if term is not None else ''
 if not word:continue
 key=ident('franceterme:'+a.get('id'));domain=' / '.join(txt(v) for v in a.findall('Domaine/*'))
 paragraphs=[p('Domaine : '+domain,True),p(txt(a.find('Definition')) or 'La source FranceTerme ne fournit pas de définition pour cette notice. Les équivalents et les renvois disponibles sont reproduits ci-dessous.')]
 if txt(a.find('Notes')):paragraphs.append(p('Notes : '+txt(a.find('Notes'))))
 for e in a.findall('Equivalent'):paragraphs.append(p('Équivalent ('+e.get('langue','')+') : '+txt(e)))
 variants=[txt(v) for v in a.findall('.//variante')]
 if variants:paragraphs.append(p('Variantes : '+' ; '.join(variants)))
 refs=[]
 for v in a.findall('Voir/A'):
  match=re.search(r'FIC_ID=(\d+)',v.get('href',''))
  if match and match[1] in active:refs.append({'id':ident('franceterme:'+match[1]),'headword':txt(v),'page':0,'category':'FranceTerme','preview':'Voir aussi'})
 insert(key,word,'Terminologie · '+(domain or 'Général'),paragraphs,'FranceTerme','https://www.culture.fr/franceterme/terme/'+a.get('numero',''),'Licence Ouverte 2.0',txt(a.find('DatePub')),refs)
 db.executemany('INSERT OR IGNORE INTO aliases VALUES(?,?)',[(norm(v),key) for v in variants+[txt(e.find('Equi_prop')) for e in a.findall('Equivalent')] if v])
print('Building search index',flush=True)
db.executescript("DROP TABLE pending; DROP TABLE staging; CREATE INDEX entries_normalized ON entries(normalized,id); CREATE INDEX entries_source ON entries(source,normalized); CREATE VIRTUAL TABLE dictionary_fts USING fts4(normalized,search_body,content='entries',tokenize=simple); INSERT INTO dictionary_fts(dictionary_fts) VALUES('rebuild');")
counts.update({'entries':db.execute('SELECT count(*) FROM entries').fetchone()[0],'sources':dict(db.execute('SELECT source,count(*) FROM entries GROUP BY source')),'aliases':db.execute('SELECT count(*) FROM aliases').fetchone()[0]})
from collections import Counter
categories=Counter()
for category,source,count in db.execute('SELECT category,source,count(*) FROM entries GROUP BY category,source'):
 for value in set(category.split(' / ') if source=='Wiktionnaire' else [category.split(' / ')[0]]):categories[value]+=count
counts['franceTermeWithoutDefinition']=sum(1 for a in root.findall('Article') if a.get('id') in active and not txt(a.find('Definition')))
meta={'databaseLicence':'CC BY-SA 4.0 ; notices FranceTerme également sous Licence Ouverte 2.0.','version':'2.1.0','builtAt':'2026-10-31','counts':counts,'letters':dict(db.execute('SELECT letter,count(*) FROM entries GROUP BY letter ORDER BY letter')),'categories':dict(sorted(categories.items())),'sources':[{'name':'Wiktionnaire','url':'https://fr.wiktionary.org','extraction':'https://kaikki.org/frwiktionary/','dumpDate':'2026-10-01','licence':'CC BY-SA 4.0','licenceUrl':'https://creativecommons.org/licenses/by-sa/4.0/','credit':'Contributeurs du Wiktionnaire ; extraction Wiktextract / Tatu Ylonen / Kaikki.org.','changes':'Français uniquement ; regroupement des emplois par graphie ; formes fléchies reliées aux lemmes ; normalisation de recherche ; citations et médias exclus.'},{'name':'FranceTerme','url':'https://www.culture.fr/franceterme','download':'https://www.franceterme.culture.gouv.fr/public/FranceTerme.xml','licence':'Licence Ouverte 2.0','licenceUrl':'https://www.etalab.gouv.fr/licence-ouverte-open-licence/','credit':'Ministère de la Culture ; Commission d’enrichissement de la langue française.','changes':'Articles publiés non annulés ; indexation des variantes et équivalents ; mise en forme.'}],'sha256':{f:hashlib.file_digest(open(SOURCES/f,'rb'),'sha256').hexdigest() for f in ['fr-extract.jsonl.gz','FranceTerme.xml']}}
db.execute('INSERT INTO metadata VALUES(?,?)',('modern',compact(meta)));db.commit();db.execute('VACUUM');assert db.execute('PRAGMA integrity_check').fetchone()[0]=='ok';db.close()
(ROOT/'assets/dictionary/modern_metadata.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(counts,ensure_ascii=False),flush=True)
