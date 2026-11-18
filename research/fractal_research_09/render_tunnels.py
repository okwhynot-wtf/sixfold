"""Render the reference geometry and two loops via certified contact chains."""
from functools import lru_cache
import json
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import patheffects
from matplotlib.patches import Circle
from matplotlib.colors import to_rgb
import numpy as np
from scipy.ndimage import gaussian_filter, maximum_filter

from verify_tunnels import ROOT, PHASE5, grid_centres

PHASE7 = ROOT.parent / "fractal_handover/fractal_research_07"
sys.path.insert(0, str(PHASE7))
from geometry import maps, word_map


def loop_chords(r, rotations, translations, levels):
    data = json.loads((PHASE7 / "positive_contact_certificate.json").read_text())
    forward, partner = tuple(data["word"]), tuple(data["partner_word"])
    def permute(word, k):
        return tuple((digit+k) % 6 for digit in word)
    def shift(word):
        return word[1:]+word[:1]
    @lru_cache(maxsize=None)
    def fixed(word):
        matrix, offset = word_map(word, r, rotations, translations)
        return np.linalg.solve(np.eye(3)-matrix, offset)
    cells = []
    def refine(left, right, matrix, offset, depth):
        if depth == 0:
            cells.append([offset+matrix@fixed(left), offset+matrix@fixed(right)])
            return
        first, last = left[0], right[0]
        step = 1 if (last-first) % 6 <= 3 else -1
        k, incoming = first, left
        while True:
            nxt = (k+step) % 6
            if k == last:
                outgoing = right
            elif step == 1:
                outgoing, next_incoming = permute(forward, k), permute(partner, k)
            else:
                outgoing, next_incoming = permute(partner, nxt), permute(forward, nxt)
            assert incoming[0] == outgoing[0] == k
            refine(shift(incoming), shift(outgoing), r*matrix@rotations[k],
                   offset+matrix@translations[k], depth-1)
            if k == last:
                break
            k, incoming = nxt, next_incoming
    for j in range(6):
        refine(permute(partner, j-1), permute(forward, j), np.eye(3), np.zeros(3), levels)
    edges = np.asarray(cells)
    assert np.max(np.linalg.norm(edges[:,1] - np.roll(edges[:,0], -1, axis=0), axis=1)) < 1e-12
    return np.vstack((edges[:,0], edges[0,0]))


PAPER = "#101d28"
WHITE = "#f1f5f5"
MUTED = "#b6c8d0"
COLOURS = ["#edac60", "#4d6978", "#63808c", "#51b9bb", "#5b7887", "#496675"]
TAG = ["#ffcb86", "#87e2df"]
OUTLINE = [patheffects.withStroke(linewidth=2.7, foreground="#10212b")]


def cloud(points, labels, basis, bounds, width=1000):
    xmin, xmax, ymin, ymax = bounds
    height = round(width*(ymax-ymin)/(xmax-xmin))
    view = points @ basis.T
    x = np.rint((view[:,0]-xmin)/(xmax-xmin)*(width-1)).astype(int)
    y = np.rint((ymax-view[:,1])/(ymax-ymin)*(height-1)).astype(int)
    inside = (x>=0) & (x<width) & (y>=0) & (y<height)
    order = np.flatnonzero(inside)
    order = order[np.argsort(view[order,2])]
    pixel = np.zeros((height,width), dtype=np.int32)
    np.maximum.at(pixel.ravel(), y[order]*width+x[order], np.arange(1,len(order)+1))
    rank = maximum_filter(pixel, size=2)
    mask = rank>0
    idx = order[rank[mask]-1]
    depth = view[idx,2]
    # A smoothed visible-depth gradient lights the small protrusions while
    # retaining the six piece labels from the actual frontmost points.
    depth_map = np.zeros((height, width))
    depth_map[mask] = depth
    weight = gaussian_filter(mask.astype(float), 2.2)
    smooth = gaussian_filter(depth_map, 2.2)/np.maximum(weight, .001)
    dy, dx = np.gradient(smooth, (ymax-ymin)/height, (xmax-xmin)/width)
    directional = (.37*dx[mask]+.48*dy[mask]+.80)/np.sqrt(1+dx[mask]**2+dy[mask]**2)
    shade = .69+.26*(depth-depth.min())/(depth.max()-depth.min())+.20*directional
    palette = np.array([to_rgb(colour) for colour in COLOURS])
    output = np.empty((height,width,3), dtype=np.uint8)
    output[:] = np.rint(255*np.array(to_rgb(PAPER)))
    output[mask] = np.clip(255*(palette[labels[idx]]*shade[:,None]),0,255)
    return output


def main():
    grid = json.loads((PHASE5 / "dimension_certificate.json").read_text())
    centres = grid_centres(np.array(grid["a_grid"]), np.array(grid["b_grid"]), 8)/grid["Q"]
    labels = np.arange(len(centres))//6**7
    r, rotations, translations = maps()
    base = loop_chords(r, rotations, translations, 7)
    selected = (0, 3)
    loops = [r*base @ rotations[k].T + translations[k] for k in selected]
    direction = np.array([-1.,0,1])/np.sqrt(2)
    axial = np.array([[1/np.sqrt(2),0,1/np.sqrt(2)], [0,1,0], direction])
    # The winding diagnostic checks the displayed approximations separately.
    for i, loop in enumerate(loops):
        for j, k in enumerate(selected):
            projected = (loop-translations[k]) @ axial[:2].T
            angles = np.unwrap(np.arctan2(projected[:,1], projected[:,0]))
            assert np.isclose((angles[-1]-angles[0])/(2*np.pi), int(i==j))

    toward_viewer = np.array([.10,-1,.46])
    toward_viewer /= np.linalg.norm(toward_viewer)
    horizontal = np.cross([0,0,1], toward_viewer)
    horizontal /= np.linalg.norm(horizontal)
    oblique = np.array([horizontal, np.cross(toward_viewer, horizontal), toward_viewer])
    fig = plt.figure(figsize=(14,7.7),dpi=150,facecolor=PAPER)
    fig.text(.045,.928,"Two tunnels in opposite lobes",color=WHITE,fontsize=27,weight="semibold")
    fig.text(.046,.876,"Reference shape  /  The two marked passages run parallel at 45° to vertical.",
             color=MUTED,fontsize=12)
    bounds = (-2.25,2.25,-2.0,2.0)
    for n, (basis, heading) in enumerate(((oblique,"Side view"), (axial,"Looking down both passages"))):
        ax = fig.add_axes([.024+.49*n,.177,.474,.625],facecolor=PAPER)
        ax.set_title(heading,fontsize=15,color=WHITE,pad=9,loc="left")
        ax.imshow(cloud(centres, labels, basis, bounds),extent=bounds,interpolation="nearest")
        ax.set(xlim=bounds[:2], ylim=bounds[2:],aspect="equal")
        ax.axis("off")
        for i,k in enumerate(selected):
            centre = translations[k] @ basis[:2].T
            label = "A" if i==0 else "B"
            if n == 0:
                delta = direction @ basis[:2].T
                length = 1.29
                p, q = centre-length*delta, centre+length*delta
                ax.plot([p[0],q[0]],[p[1],q[1]],color=WHITE,linewidth=1.2,
                        dashes=(4,3),path_effects=OUTLINE)
                ax.plot(*centre,marker="o",ms=5,mec=PAPER,mew=1.1,mfc=WHITE)
                tag_pos = p if i==0 else q
                ax.text(tag_pos[0]+(.06 if i==0 else -.06), tag_pos[1],
                        label, ha="left" if i==0 else "right", va="center",
                        color=TAG[i], weight="bold", fontsize=15,path_effects=OUTLINE)
            else:
                path = loops[i] @ basis[:2].T
                ax.plot(*path.T,color=WHITE,linewidth=.82,alpha=.92,path_effects=OUTLINE)
                ax.add_patch(Circle(centre,.105,fill=False,edgecolor=TAG[i],linewidth=1.7))
                ax.annotate(label, centre+np.array([.078,.078]), xytext=(11,11),
                            textcoords="offset points", color=WHITE, fontsize=10, weight="bold",
                            path_effects=OUTLINE, arrowprops=dict(arrowstyle="-",
                            color=WHITE, lw=.8, shrinkA=1, shrinkB=1))
    fig.text(.052,.14,"Dashed lines follow the tunnel centres.",color=MUTED,fontsize=11)
    fig.text(.531,.14,"Rings mark the guaranteed clear radius of 0.105.",color=MUTED,fontsize=11)
    fig.text(.531,.103,"White paths trace the two loops at finite resolution.",color=MUTED,fontsize=11)
    fig.text(.052,.051,"A   amber  /  upper lobe                 B   teal  /  opposite lower lobe",
             color=WHITE,fontsize=11)
    fig.savefig(ROOT/"opposite_tunnels.png",facecolor=fig.get_facecolor())
    plt.close(fig)
    print(len(base)-1,"verified contact-chain chords per plotted loop")


if __name__ == "__main__":
    main()
