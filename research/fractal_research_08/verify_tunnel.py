"""Certify an axial through-hole using the verified phase-05 grid."""
import argparse
from fractions import Fraction
import json
from pathlib import Path
import sys

import numpy as np

ROOT = Path(__file__).resolve().parent
PHASE5 = ROOT.parent / "fractal_handover/fractal_research_05"
sys.path.insert(0, str(PHASE5))
from certify_dimension import grid_centres


def check():
    data = json.loads((PHASE5 / "dimension_certificate.json").read_text())
    q = data["Q"]
    a, b = np.array(data["a_grid"], dtype=np.int64), np.array(data["b_grid"], dtype=np.int64)
    centres = grid_centres(a, b, 8)
    piece = centres[:6**7]
    assert np.max(np.abs(piece)) < 3*q and 18*q*q < 2**63
    least_x = int(piece[:, 0].min())
    squared = int(np.min(np.sum(piece[:, :2]**2, axis=1)))
    assert least_x == 3049454 and squared == 97951509407090
    # Phase 05 bounds the displacement of the finite centres for the entire
    # family, as well as every point of the infinite tail.
    family = next(item for item in data["results"] if item["name"] == "whole_family")
    tail = (Fraction(data["packing_ball_bound"])*Fraction(family["r_upper"])**8
            + Fraction(family["centre_error_bound"]))
    assert squared > (q*(Fraction("0.0122")+tail))**2
    # W begins with 01. Check that the certified contact is on the positive
    # half of the axis at azimuth 30 degrees, so principal arguments fit together.
    assert Fraction(int(piece[6**6 : 2*6**6, 0].min()), q) > tail
    print("All family members avoid the vertical cylinder of radius 0.0122.")
    print("Every point of piece 0 avoids the radial half-plane x<=0, y=0.")
    return centres/q


def render(points):
    from PIL import Image, ImageDraw, ImageFont
    from matplotlib import font_manager
    from scipy.ndimage import maximum_filter
    from render_dimension import PALETTE, point_image

    size = 480
    labels = np.arange(len(points))//6**7
    paper, bright, muted = (9, 21, 32), (234, 242, 241), (158, 186, 197)
    canvas = Image.new("RGB", (3*size+64, size+150), paper)
    draw = ImageDraw.Draw(canvas)
    def font(pt):
        return ImageFont.truetype(font_manager.findfont("DejaVu Sans"), pt)
    def axial_view(half_width, mark=False):
        scale = (size-1)/(2*half_width)
        mask = (np.abs(points[:, :2]) < half_width).all(axis=1)
        visible = np.flatnonzero(mask)
        order = visible[np.argsort(points[visible, 2])]
        xy = np.rint((points[order, :2]+half_width)*scale).astype(int)
        pix = (size-1-xy[:,1])*size+xy[:,0]
        ranks = np.zeros(size*size, np.int32)
        np.maximum.at(ranks, pix, np.arange(1, len(order)+1, dtype=np.int32))
        ranks = maximum_filter(ranks.reshape(size, size), size=2)
        mask = ranks > 0
        chosen = order[ranks[mask]-1]
        pixels = np.empty((size,size,3), dtype=np.uint8)
        pixels[:] = paper
        shade = .76 + .22*points[chosen, 2]/2.14
        pixels[mask] = np.clip(PALETTE[labels[chosen]]*shade[:,None], 0, 255)
        img = Image.fromarray(pixels)
        if mark:
            pen = ImageDraw.Draw(img)
            c, radius = (size-1)/2, .0122*scale
            pen.ellipse((c-radius,c-radius,c+radius,c+radius), outline=bright, width=2)
        return img
    views = [point_image(points, labels, size=size), axial_view(2.14), axial_view(.075, True)]
    headings = ["Oblique view", "Looking down the axis", "Centre enlarged"]
    notes = ["Colours identify the six largest copies.", "The full width shown is 4.28 units.",
             "The white circle marks radius 0.0122."]
    for j, img in enumerate(views):
        x = 16 + j*(size+16)
        draw.text((x,15), headings[j], font=font(24), fill=bright)
        canvas.paste(img, (x,59))
        draw.text((x, size+75), notes[j], font=font(16), fill=muted)
    draw.text((16, size+112), "Reference member   /   Depth-eight centres   /   The certificate bounds the entire infinite tail.",
              font=font(15), fill=muted)
    canvas.save(ROOT / "reference_tunnel.png")


if __name__ == "__main__":
    if not __debug__:
        raise RuntimeError("Assertions must be enabled")
    parser = argparse.ArgumentParser()
    parser.add_argument("--render", action="store_true")
    args = parser.parse_args()
    points = check()
    if args.render:
        render(points)
