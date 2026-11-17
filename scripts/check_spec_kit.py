#!/usr/bin/env python3
"""Checks only the specification kit. Does NOT validate or build the application."""
from pathlib import Path
import json,sys,re,hashlib
ROOT=Path(__file__).resolve().parent.parent
required = [
 'AGENTS.md','CONTEXT.md','README.md','prompts/SYSTEM.md','prompts/CONTEXT.md',
 'docs/architecture/MASTER_ARCHITECTURE.md','docs/requirements/REQUIREMENTS.md',
 'docs/core/TELEMETRY_POLICY.md','docs/infrastructure/DB_BOOTSTRAP.md',
 'docs/quality/GATES.md','docs/quality/TELEMETRY_CASES.md',
 'docs/plan/BUILD_ORDER.md','.kilo/commands/oap-start.md',
 '.kilo/commands/oap-build-all.md','.kilo/agents/oap-lead.md','kilo.jsonc','.env.example'
]
fail=[]
for p in required:
    path=ROOT/p
    if not path.is_file():fail.append('MISSING: '+p)
    elif len(path.read_text(encoding='utf8').strip())<100:fail.append('TOO_SHORT: '+p)
required_terms = {
'docs/core/TELEMETRY_POLICY.md':['on_change','storageDatapoint','max_samples','Attribute','Node-RED','restart'],
 'docs/infrastructure/DB_BOOTSTRAP.md':['docker compose','db-bootstrap','postgis','volumen','idempotente'],
'docs/plan/BUILD_ORDER.md':['S00','S09','G4','G9'],
'AGENTS.md':['.venv','Django','MQTT','Gates' if False else 'gates'],
}
for name,terms in required_terms.items():
    p=ROOT/name
    if p.exists():
        s=p.read_text(encoding='utf8').lower()
        for term in terms:
            if term.lower() not in s:fail.append(f'MISSING_TERM {name}: {term}')
plugins=ROOT/'docs/plugins'
found=[p for p in plugins.iterdir() if p.is_dir()] if plugins.is_dir() else []
if len(found)<16:fail.append(f'Expected >=16 plugin specs, found {len(found)}')
for d in found:
    for name in ['SPEC.md','ACCEPTANCE.md','MANIFEST.md']:
        if not (d/name).is_file():fail.append(f'Plugin {d.name} missing {name}')
mds=list(ROOT.rglob('*.md'))
if len(mds)<85:fail.append(f'Expected >=85 Markdown files, found {len(mds)}')
if (ROOT/'manifest.json').exists():
    manifest=json.loads((ROOT/'manifest.json').read_text(encoding='utf8'))
    for item in manifest['files']:
        p=ROOT/item['path']
        if not p.is_file():fail.append('MANIFEST MISSING '+item['path'])
        elif hashlib.sha256(p.read_bytes()).hexdigest()!=item['sha256']:fail.append('HASH MISMATCH '+item['path'])
print(f'OAP SPEC KIT: {len(mds)} markdown files, {len(found)} plugin specification directories')
print('SPEC VALIDATION STATUS:', 'PASS' if not fail else 'FAIL')
for f in fail:print(' -',f)
print('APPLICATION STATUS: NOT TESTED BY THIS SCRIPT')
sys.exit(1 if fail else 0)
