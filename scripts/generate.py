"""Generate reference word centres using the preserved six-map implementation."""

import argparse
from pathlib import Path
import sys

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "research/fractal_handover/fractal_research_07"
sys.path.insert(0, str(SOURCE))
from geometry import maps


def centres(depth):
    scale, rotations, translations = maps()
    points = np.zeros((1, 3))
    for _ in range(depth):
        points = np.concatenate([
            scale * points @ rotation.T + translation
            for rotation, translation in zip(rotations, translations)
        ])
    return points, scale


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--depth", type=int, choices=range(9), default=5)
    parser.add_argument("--output", type=Path, default=Path(".build/sixfold.csv"))
    args = parser.parse_args()
    points, scale = centres(args.depth)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    np.savetxt(args.output, points, delimiter=",", header="x,y,z", comments="",
               fmt="%.17g")
    print(f"Saved {len(points):,} reference centres to {args.output}.")
    print(f"Geometric tail scale 2.14*r^n = {2.14 * scale**args.depth:.8g}.")
    print("Coordinates use floating-point maps; rounding error is additional.")


if __name__ == "__main__":
    main()
