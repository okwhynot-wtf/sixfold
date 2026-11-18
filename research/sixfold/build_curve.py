"""Pack the phase-09 contact chords for the phase-10 shrinking-loop family."""
from pathlib import Path
import sys

import numpy as np
from PIL import Image

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent/"fractal_research_09"))
from render_tunnels import loop_chords, maps


def main():
    path = loop_chords(*maps(), 7)
    segments = 24
    groups = (len(path)-2)//segments+1
    rows = []
    for i in range(groups):
        points = path[i*segments:i*segments+segments+1]
        lo, hi = points.min(0), points.max(0)
        points = np.pad(points, ((0,segments+1-len(points)),(0,0)), mode="edge")
        rows.append(np.vstack((lo,hi,points)))
    xyz = np.array(rows)
    assert np.abs(xyz).max() < 2.22
    words = np.rint((xyz/4.44+.5)*65535).astype(np.uint16)
    atlas = np.empty((groups*2, segments+3, 3), dtype=np.uint8)
    atlas[::2], atlas[1::2] = words >> 8, words & 255
    Image.fromarray(atlas[::-1]).save(HERE/"contact_curve.png")
    print(f"{len(path)-1} chords in {groups} bounding boxes")


if __name__ == "__main__":
    main()
