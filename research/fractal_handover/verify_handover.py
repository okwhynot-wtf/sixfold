"""Verify package integrity and current mathematical implementation checks.

Runs checks in a temporary copy so supplied certificates remain untouched.
No C++ compiler, browser, account, or network access is needed after installing
the pinned Python dependencies. Analytic proofs still require human review.
"""
from pathlib import Path
import argparse
import hashlib
import json
import os
import platform
import shutil
import subprocess
import sys
import tempfile
import time

ROOT=Path(__file__).resolve().parent


def digest(path):
    h=hashlib.sha256()
    with path.open('rb') as source:
        for part in iter(lambda:source.read(1024*1024),b''):h.update(part)
    return h.hexdigest()


def manifest_check():
    manifest=json.loads((ROOT/'MANIFEST.json').read_text())
    total=0
    for item in manifest['files']:
        path=ROOT/item['path']
        assert path.resolve().is_relative_to(ROOT)
        assert path.is_file(),f'Missing file: {item["path"]}'
        assert path.stat().st_size==item['bytes'],f'Changed size: {item["path"]}'
        assert digest(path)==item['sha256'],f'Hash mismatch: {item["path"]}'
        total+=item['bytes']
    return {'passed':True,'files_checked':len(manifest['files']),'bytes_checked':total}


def command_check(label,script,*arguments):
    started=time.perf_counter()
    env=os.environ.copy();env.pop('PYTHONOPTIMIZE',None)
    result=subprocess.run([sys.executable,str(script),*map(str,arguments)],cwd=script.parent,
                          capture_output=True,text=True,encoding='utf-8',errors='replace',env=env)
    if result.returncode:
        raise RuntimeError(f'{label} failed\n{result.stdout}\n{result.stderr}')
    try:data=json.loads(result.stdout)
    except json.JSONDecodeError:data={'output':result.stdout}
    if isinstance(data,dict) and 'passed' in data:assert data['passed']
    print(f'PASS: {label}',flush=True)
    return {'label':label,'passed':True,'seconds':round(time.perf_counter()-started,3),
            'details':data}


def main():
    if not __debug__:raise RuntimeError('Do not use python -O: assertions are required')
    parser=argparse.ArgumentParser()
    parser.add_argument('--manifest-only',action='store_true')
    parser.add_argument('--historical',action='store_true',help='Also rerun the phase-03 negative-certificate checks')
    parser.add_argument('--json-output',type=Path,help='Optional path for a verification receipt')
    args=parser.parse_args()
    started=time.perf_counter()
    integrity=manifest_check()
    print(f'PASS: SHA-256 manifest ({integrity["files_checked"]} files)',flush=True)
    checks=[]
    if not args.manifest_only:
        with tempfile.TemporaryDirectory(prefix='fractal_handover_') as scratch:
            scratch=Path(scratch)
            for phase in [3,4,5,6,7]:
                name=f'fractal_research_{phase:02}'
                shutil.copytree(ROOT/name,scratch/name,ignore=shutil.ignore_patterns('__pycache__','*.pyc','verify_packing','verify_packing.exe'))
            checks.append(command_check('Contact symmetries and independent geometry',scratch/'fractal_research_04/verify_positive_contact.py'))
            checks.append(command_check('Hausdorff lower bounds and both exact integer packings',ROOT/'verify_packings_portable.py','--phase-dir',scratch/'fractal_research_05'))
            checks.append(command_check('OSC obstruction and complete first-level pair classification',scratch/'fractal_research_06/verify_obstruction.py'))
            checks.append(command_check('Assouad theorem parameter premises',scratch/'fractal_research_07/certify_assouad.py'))
            checks.append(command_check('Independent rotation and cancellation checks',scratch/'fractal_research_07/verify_assouad.py'))
            if args.historical:
                checks.append(command_check('Historical phase-03 exclusions',scratch/'fractal_research_03/verify_results.py'))
    result={'passed':True,'python':platform.python_version(),'platform':platform.platform(),
            'integrity':integrity,'checks':checks,'elapsed_seconds':round(time.perf_counter()-started,3),
            'scope':'Reproduced numerical/symbolic/interval/integer checks. Published theorems and analytic deductions require separate mathematical review.'}
    if args.json_output:
        args.json_output.parent.mkdir(parents=True,exist_ok=True)
        args.json_output.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print('All requested checks passed. See HANDOVER.md for proof scope and open questions.',flush=True)


if __name__=='__main__':main()
