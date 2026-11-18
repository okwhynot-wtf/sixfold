"""Reproduce two native stills, exercise six camera modes and decode the six films.

Run scripts/download_films.py first. Pixel comparison is strict; other GPUs
may differ from the recorded Windows/Intel reference environment.
"""
import argparse
import hashlib
import importlib.metadata
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
from PIL import Image, ImageChops
import imageio_ffmpeg

root = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--receipt', type=Path, default=root / '.build/visuals-render-check.json')
args = parser.parse_args()
args.receipt.parent.mkdir(parents=True, exist_ok=True)
source = root / 'research/sixfold'
library = source / 'assets/2026-11-18-library'
recipe = json.loads((library / 'source/manifest.json').read_text())
files = ['sculpture.frag','gpu_renderer.py','palettes.json','reference.glsl','field.png','contact_curve.png']
signature = hashlib.sha256(b''.join((source / p).read_bytes() for p in files) + json.dumps([recipe['stills'],recipe['films']]).encode()).hexdigest()
assert signature == recipe['signature'], 'Current rendering source differs from the film/still recipes'
report = {'source_recipe_signature_matches': True, 'environment': {'python': sys.version.split()[0], 'platform': sys.platform,
          'packages': {p: importlib.metadata.version(p) for p in ['Pillow','moderngl','glcontext','imageio-ffmpeg']}}, 'renders': [], 'films': []}
with tempfile.TemporaryDirectory(prefix='sixfold-portability-') as temp:
    work = Path(temp)
    for p in source.iterdir():
        if p.is_file():
            shutil.copy2(p, work / p.name)
    sys.path.insert(0,str(work))
    from gpu_renderer import Renderer
    palettes = json.loads((work / 'palettes.json').read_text())
    for record in [recipe['stills'][0], recipe['stills'][2]]:
        render = Renderer(record['width'], record['height'], samples=4)
        report['environment']['gpu'] = {k: render.ctx.info[k] for k in ['GL_VENDOR','GL_RENDERER','GL_VERSION']}
        render.colours(palettes[record['palette']])
        frame = render.image(record['phase'], record['mode'], record['composition'])
        expected = Image.open(library / record['master']).convert('RGB')
        difference = ImageChops.difference(frame,expected)
        identical = difference.getbbox() is None
        assert identical, f'{record["id"]} differs from the archived master'
        frame.save(args.receipt.parent / (record['id'] + '-reproduced.png'))
        report['renders'].append({'id': record['id'], 'pixel_identical_to_master': identical})
        render.close()
        print('PASS reproduced', record['id'], 'pixel for pixel from a fresh directory', flush=True)
    render = Renderer(320,180)
    for mode in range(6):
        frame = render.image(.31,mode)
        assert frame.getbbox() is not None
    render.close()
    report['six_camera_modes_rendered'] = True
ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
manifest = json.loads((root / 'verification/visuals-edition-01.json').read_text())
for film in manifest['films']:
    path = root / film['path']
    if not path.is_file():
        raise SystemExit('Run python scripts/download_films.py before the film decode checks.')
    frames = imageio_ffmpeg.read_frames(str(path))
    metadata = next(frames)
    frames.close()
    duration = 48 if 'chromatic' in film['asset'] else 36
    aspect = film['asset'].split('-')[1]
    dimensions = {'landscape': (1920,1080), 'square':(1920,1920),'portrait':(1080,1920)}[aspect]
    assert metadata['size'] == dimensions
    assert metadata['fps'] == 30
    assert abs(metadata['duration'] - duration) < .05
    decoded = subprocess.run([ffmpeg,'-v','error','-xerror','-i',str(path),'-f','null','-'], capture_output=True, text=True)
    assert decoded.returncode == 0, decoded.stderr
    report['films'].append({'asset':film['asset'], 'size':list(metadata['size']), 'fps':metadata['fps'], 'duration':metadata['duration'], 'full_decode':'PASS'})
    print('PASS decoded', film['asset'], flush=True)
args.receipt.write_text(json.dumps(report,indent=2)+'\n', encoding='utf-8')
print('All visualisation checks passed.', flush=True)
