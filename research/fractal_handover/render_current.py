"""Reproduce the current images with portable font selection.

Original phase renderers are preserved unchanged. This wrapper supplies a
bundled Matplotlib font when a Linux-specific font path is unavailable.
"""
from pathlib import Path
import argparse
import runpy
import sys
from PIL import ImageFont
from matplotlib import font_manager

ROOT=Path(__file__).resolve().parent


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--phase',choices=['05','07','both'],default='both')
    args=parser.parse_args()
    original=ImageFont.truetype
    fallback=font_manager.findfont(font_manager.FontProperties(family='DejaVu Sans'))
    def portable(font,size=10,*a,**kw):
        if isinstance(font,(str,Path)) and not Path(font).exists():font=fallback
        return original(font,size,*a,**kw)
    ImageFont.truetype=portable
    for phase,script in [('05','render_dimension.py'),('07','render_shared_zoom.py')]:
        if args.phase not in ['both',phase]:continue
        folder=ROOT/f'fractal_research_{phase}'
        sys.path.insert(0,str(folder))
        # Run each renderer in its own module/import context. The current
        # scripts use compatible geometry, and only phase 07 imports it.
        runpy.run_path(str(folder/script),run_name='__main__')
        sys.path.pop(0)
    print('Rendered current figures. Rerendering changes image files; keep a separate copy if preserving manifest integrity.')


if __name__=='__main__':main()
