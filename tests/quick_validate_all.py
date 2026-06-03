#!/usr/bin/env python3
from __future__ import annotations
import ast, hashlib, json, re, subprocess, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
REQ_FILES=['README.md','workflow_rules.md','install.md','dependencies.md','input_schema.md','output_schema.md','known_issues.md']
REQ_DIRS=['scripts','templates','examples','tests']
ALLOWED={'active','experimental','planned','deprecated'}
def _t(*parts): return ''.join(parts)
PRIVATE=[re.compile(p) for p in [re.escape(_t('/Users/','h','c')),re.escape(_t('/home/','c','h','j')),r'\b'+re.escape(_t('go','oxi'))+r'\b',r'\b'+re.escape(_t('de','ll'))+r'\b',re.escape(_t('CK','AP4')),re.escape(_t('DR','P1')),re.escape(_t('BEGIN ','OPEN','SSH')),re.escape(_t('PRIVATE',' KEY')),_t('api','[_-]?','key'),_t('pass','word'),_t('sec','ret')]]
EXCLUDE={'FINAL_RELEASE_AUDIT.md','FINAL_SANITIZATION_REPORT.md','RELEASE_VALIDATION.md','tests/quick_validate_all.py'}
def fail(msg): print('FAIL:',msg,file=sys.stderr); raise SystemExit(1)
def skill():
 p=ROOT/'SKILL.md';
 if not p.is_file(): fail('SKILL.md missing')
 t=p.read_text(errors='replace')
 if not t.startswith('---\n') or 'name:' not in t.split('---',2)[1] or 'description:' not in t.split('---',2)[1]: fail('SKILL.md metadata invalid')
def registry():
 p=ROOT/'references/module_registry.md'
 if not p.is_file(): fail('module_registry missing')
 rows=[]
 for line in p.read_text(errors='replace').splitlines():
  if not line.startswith('| ') or '---' in line or 'module_name' in line: continue
  cells=[c.strip() for c in line.strip('|').split('|')]
  if len(cells)==8: rows.append(cells)
 if not rows: fail('module_registry empty')
 for r in rows:
  if r[3] not in ALLOWED: fail(f'invalid status {r[3]} for {r[0]}')
 return rows
def modules(rows):
 for r in rows:
  if r[3]!='active': continue
  d=ROOT/'modules'/r[0]
  if not d.is_dir(): fail(f'active module dir missing {r[0]}')
  for f in REQ_FILES:
   if not (d/f).is_file(): fail(f'{r[0]} missing {f}')
  for sd in REQ_DIRS:
   if not (d/sd).is_dir(): fail(f'{r[0]} missing {sd}/')
def syntax():
 for p in list((ROOT/'scripts').rglob('*.py'))+list((ROOT/'tests').rglob('*.py')):
  ast.parse(p.read_text(errors='replace'),filename=str(p))
 for p in (ROOT/'scripts').rglob('*.sh'):
  pr=subprocess.run(['bash','-n',str(p)],capture_output=True,text=True)
  if pr.returncode: fail(f'shell syntax {p.relative_to(ROOT)}: {pr.stderr}')
def private():
 for p in ROOT.rglob('*'):
  if not p.is_file():
   continue
  rel=p.relative_to(ROOT).as_posix()
  if rel.startswith('.git/') or rel.startswith('_private_excluded_from_release/') or rel in EXCLUDE:
   continue
  text=p.read_text(errors='ignore')
  for pat in PRIVATE:
   if pat.search(text): fail(f'private pattern {pat.pattern} in {rel}')

def identity():
 pr=subprocess.run([sys.executable,str(ROOT/'tests/check_identity_leaks.py')],capture_output=True,text=True)
 if pr.returncode:
  fail('identity leak validation failed:\n'+pr.stdout+pr.stderr)
def templates():
 p=ROOT/'core/verified_template_manifest.json'
 if not p.is_file(): fail('verified_template_manifest missing')
 data=json.loads(p.read_text()).get('files',{})
 for rel,h in data.items():
  fp=ROOT/rel
  if not fp.is_file(): fail(f'verified template missing {rel}')
  if hashlib.sha256(fp.read_bytes()).hexdigest()!=h: fail(f'verified template changed {rel}')
def main():
 skill(); rows=registry(); modules(rows); syntax(); private(); identity(); templates(); print('quick_validate_all: OK')
if __name__=='__main__': main()
