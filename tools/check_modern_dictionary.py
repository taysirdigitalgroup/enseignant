#!/usr/bin/env python3
"""Validate real pack data and the SQL used by Android; no Flutter required."""
import json,sqlite3,zlib,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
modern=ROOT/'assets/dictionary/modern.sqlite'
c=sqlite3.connect(f'file:{modern}?mode=ro',uri=True)
assert c.execute('PRAGMA integrity_check').fetchone()[0]=='ok'
meta=json.loads(c.execute("SELECT value FROM metadata WHERE key='modern'").fetchone()[0])
counts=meta['counts']
assert counts['entries']>400000 and counts['sources']['FranceTerme']>7000
assert c.execute('SELECT count(*) FROM entries').fetchone()[0]==counts['entries']
checked=0;references=0
for key,paragraphs,body,refs,source,url,licence in c.execute('SELECT id,paragraphs,body,refs,source,source_url,licence FROM entries'):
 ps=json.loads(zlib.decompress(paragraphs));plain=zlib.decompress(body).decode()
 assert plain=='\n\n'.join(p[0]['text'] for p in ps),(key,'rich/plain mismatch')
 assert ps and plain and url.startswith('https://') and licence
 assert source in ['Wiktionnaire','FranceTerme'] and key>=1000000000
 for ref in json.loads(refs):
  assert c.execute('SELECT 1 FROM entries WHERE id=?',(ref['id'],)).fetchone(),ref
  references+=1
 checked+=1
assert c.execute('SELECT count(*) FROM aliases a WHERE NOT EXISTS(SELECT 1 FROM entries e WHERE a.entry_id=e.id)').fetchone()[0]==0
base='SELECT id,headword,source FROM entries WHERE '
queries={
 'exact':"id IN (SELECT entry_id FROM aliases WHERE alias=?)",
 'word':"id IN (SELECT entry_id FROM aliases WHERE alias>=? AND alias<?)",
 'definitions':"id IN (SELECT docid FROM dictionary_fts WHERE dictionary_fts MATCH ?)",
}
for word in ['ordinateur','internet','smartphone','cybersecurite','intelligence artificielle','ecrivaient']:
 start=time.monotonic();rows=c.execute(base+queries['exact'],(word,)).fetchall()
 assert rows,(word,'not found')
 print(word,rows[:4],round(time.monotonic()-start,3),'s')
rows=c.execute(base+queries['definitions'],('intelligence* AND artificielle*',)).fetchall();assert len(rows)>10
assert c.execute(base+queries['word'],('cyber','cyber\uffff')).fetchone()
assert c.execute("SELECT count(*) FROM entries WHERE source='FranceTerme' AND category LIKE 'Terminologie · %'").fetchone()[0]==counts['sources']['FranceTerme']
print(json.dumps({'checkedArticles':checked,'checkedReferences':references,'counts':counts,'ftsResults':len(rows),'integrity':'ok'},ensure_ascii=False,indent=2))
