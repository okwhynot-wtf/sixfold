"""An exact product construction, rendered using finite point samples."""
from pathlib import Path
import json
import math
import numpy as np
from base_ifs import centres
from continue_research import render_points

ROOT=Path(__file__).resolve().parent


def product_points(depth=7,interior_samples=5,height=.32):
    rc=(math.sqrt(15)-math.sqrt(3))/6
    z=centres(rc,30,depth)
    rng=np.random.default_rng(20261117)
    points=[]
    for j in range(interior_samples+2):
        vertical=np.full(len(z),-height if j==0 else height) if j<2 else rng.uniform(-height,height,len(z))
        points.append(np.column_stack((z.real,z.imag,vertical)))
    return np.concatenate(points)


def main():
    rc=(math.sqrt(15)-math.sqrt(3))/6
    intervals=sorted([(j*(1-rc)-rc,j*(1-rc)+rc) for j in (-1,0,1)])
    assert abs(intervals[0][0]+1)<1e-14 and abs(intervals[-1][1]-1)<1e-14
    assert all(intervals[k][1]>=intervals[k+1][0] for k in (0,1))
    p=product_points()
    render_points(p,ROOT/'extruded_gear.png',yaw_degrees=-22,pitch_degrees=28,size=1800)
    export=product_points(depth=6,interior_samples=3)
    with (ROOT/'extruded_gear.ply').open('w') as f:
        f.write('ply\nformat ascii 1.0\ncomment Finite sample of K x interval; not a watertight surface\n')
        f.write(f'element vertex {len(export)}\nproperty float x\nproperty float y\nproperty float z\nend_header\n')
        np.savetxt(f,export,fmt='%.8f')
    result={'construction':'K_30_degree_first_contact x [-0.32,0.32]',
        'scale':rc,'similarity_maps':18,'dimension':1+math.log(6)/math.log(1/rc),
        'height_half_extent':.32,'render_points':len(p),'export_points':len(export),
        'vertical_intervals_at_unit_height':intervals,
        'status':'Product construction: exact self-similarity and dimension from planar OSC case; not a novelty claim.'}
    (ROOT/'extrusion_checks.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':
    main()
