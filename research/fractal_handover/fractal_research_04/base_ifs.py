"""Six-map similarity experiment. Floating-point screening is not a certificate."""
from pathlib import Path
import csv
import json
import math
import numpy as np
from scipy.spatial import cKDTree
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent
DIGITS = np.exp(1j * np.arange(6) * np.pi / 3)
SIGNS = np.array([1, -1, 1, -1, 1, -1])


def maps(r, theta_degrees):
    return r * np.exp(1j * SIGNS * np.deg2rad(theta_degrees)), DIGITS


def centres(r, theta_degrees, depth):
    a, b = maps(r, theta_degrees)
    p = np.array([0j])
    for _ in range(depth):
        p = (a[:, None] * p[None, :] + b[:, None]).ravel()
    return p


def xy(z):
    return np.column_stack((z.real, z.imag))


def screen(r, theta_degrees, depth=3):
    """Cover each first-level piece by equal discs and test its contact graph.

    K lies in B(0,1/(1-r)). At depth n+1, tail-disc radius is
    r**(n+1)/(1-r). A positive centre distance minus twice that radius
    excludes a contact in exact arithmetic. Here it is numerical screening.
    An overlapping cover NEVER proves that pieces meet.
    """
    a, b = maps(r, theta_degrees)
    p = centres(r, theta_degrees, depth)
    branches = a[:, None] * p[None, :] + b[:, None]
    points = [xy(z) for z in branches]
    trees = [cKDTree(q) for q in points]
    tail = r ** (depth + 1) / (1-r)
    parent = list(range(6))
    def find(i):
        while parent[i] != i:
            parent[i] = parent[parent[i]]
            i = parent[i]
        return i
    min_gap = float('inf')
    edges = 0
    for i in range(6):
        for j in range(i+1, 6):
            distance = trees[i].query(points[j], k=1)[0].min()
            gap = float(distance - 2*tail)
            min_gap = min(min_gap, gap)
            if gap <= 1e-12:
                edges += 1
                parent[find(i)] = find(j)
    return {'r': float(r), 'theta_degrees': float(theta_degrees), 'depth': depth,
            'outer_graph_components': len({find(i) for i in range(6)}),
            'outer_graph_edges': edges,
            'minimum_pair_gap_lower_estimate': min_gap,
            'tail_disc_radius': tail,
            'similarity_dimension': math.log(6)/math.log(1/r)}


def make_scan():
    rows = []
    for r in np.linspace(.315, .395, 33):
        for theta in np.arange(0, 60.01, 2):
            rows.append(screen(float(r), float(theta), depth=3))
    with (ROOT/'parameter_scan.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]))
        w.writeheader(); w.writerows(rows)
    return rows


def make_gallery():
    rs = [.325, .35, .375]
    angles = [0, 10, 20, 30]
    fig, axes = plt.subplots(3,4,figsize=(13,10),facecolor='#F6F4EE')
    colors=['#0E6B7A']
    for row,r in enumerate(rs):
        for col,t in enumerate(angles):
            ax=axes[row,col]
            p=centres(r,t,7)
            ax.plot(p.real,p.imag,',',color=colors[0],alpha=.65,rasterized=True)
            ax.set_aspect('equal'); ax.axis('off')
            ax.set_title(f'r = {r:.3f}   |   angle = {t}°',fontsize=11,color='#173A42')
    fig.suptitle('Six copies, alternating turns',fontsize=23,fontweight='bold',color='#173A42',y=.98)
    fig.text(.5,.935,'The same six shrinking transformations repeat at every scale.',ha='center',fontsize=12,color='#173A42')
    fig.text(.5,.025,'Finite point approximations. Apparent connections are not proof of contact. No novelty claim.',ha='center',fontsize=11,color='#173A42')
    fig.subplots_adjust(top=.89,bottom=.075,wspace=.06,hspace=.13)
    fig.savefig(ROOT/'first_gallery.png',dpi=170,facecolor=fig.get_facecolor())
    plt.close(fig)


def main():
    rows=make_scan()
    rc=(math.sqrt(15)-math.sqrt(3))/6
    refined=[screen(r,t,depth=5) for r,t in [
        (1/3,0),(.35,10),(.35,20),(.35,30),
        (rc-.0005,30),(rc,30),(rc+.0005,30),(.375,10),(.375,20),(.375,30)]]
    result={'definition':'f_i(z) = r exp(i (-1)^i theta) z + exp(i pi i/3), i=0,...,5',
            'scan_count':len(rows),
            'screen_disconnected_count':sum(x['outer_graph_components']>1 for x in rows),
            'screen_unresolved_count':sum(x['outer_graph_components']==1 for x in rows),
            'special_angle_30_first_contact':rc,
            'refined':refined}
    (ROOT/'summary.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2),flush=True)
    make_gallery()


if __name__=='__main__':
    main()
