"""Bake the reference attractor into a linearly sampled distance atlas."""
from pathlib import Path
import sys

import numpy as np
from PIL import Image
from scipy.ndimage import gaussian_filter, distance_transform_edt

HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent / "fractal_handover" / "fractal_research_07"
sys.path.insert(0, str(SOURCE))
from geometry import maps

N = 96
EXTENT = 2.22


def vec(v):
    return "vec3(" + ",".join(f"{x:.10f}" for x in v) + ")"


def main():
    r, rotations, translations = maps()
    centres = np.zeros((1, 3))
    for _ in range(8):
        centres = np.concatenate([r * centres @ rotation.T + t
                                  for rotation, t in zip(rotations, translations)])
    # A finer grid reduces directional bias before sampling the final texture.
    fine = 3 * (N - 1) + 1
    coords = np.rint((centres + EXTENT) * ((fine-1)/(2*EXTENT))).astype(int)
    assert coords.min() > 0 and coords.max() < fine-1
    occupied = np.zeros((fine,) * 3, dtype=bool)
    occupied[tuple(coords[:, ::-1].T)] = True  # texture storage order z, y, x
    distance = distance_transform_edt(~occupied)[::3, ::3, ::3] * (2*EXTENT/(fine-1))
    density = gaussian_filter(np.exp(-(distance/.115)**2), 1.8)
    volume = np.stack([np.clip(distance / .80, 0, 1), np.clip(density, 0, 1),
                       np.zeros_like(distance)], axis=-1)
    tiles = np.rint(volume*255).astype(np.uint8).reshape(8, 12, N, N, 3)
    atlas = tiles.transpose(0, 2, 1, 3, 4).reshape(8*N, 12*N, 3)
    Image.fromarray(atlas[::-1]).save(HERE / "field.png")

    # Serialize the source's matrices by columns, as GLSL constructors require.
    matrices = ["mat3(" + ",".join(vec(col) for col in q.T) + ")" for q in rotations]
    fixed = np.linalg.solve(np.eye(3)-r*rotations[0], translations[0])
    constants = [
        f"const float ratio = {r:.12f};",
        f"const float tilt = {np.arctan2(rotations[0,0,2], rotations[0,0,0]):.12f};",
        f"const vec3 focus = {vec(fixed)};",
        "const mat3 Q[6] = mat3[6](" + ",\n".join(matrices) + ");",
        "const vec3 T[6] = vec3[6](" + ",".join(map(vec, translations)) + ");",
    ]
    (HERE / "reference.glsl").write_text("\n".join(constants) + "\n", encoding="utf8")
    print(f"{len(centres):,} word centres. Atlas {atlas.shape[1]} x {atlas.shape[0]}.")


if __name__ == "__main__":
    main()
