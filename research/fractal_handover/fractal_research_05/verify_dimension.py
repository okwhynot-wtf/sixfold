"""Separate implementation checks supporting the dimension certificate.

These are implementation checks. The mathematical argument is in RESEARCH_05.md.
"""
from pathlib import Path
import itertools
import json
import subprocess
import tempfile

import mpmath as mp
import numpy as np

from certify_dimension import (
    ROOT,Q,grid_maps,grid_centres,radial_geometry,sharp_family_certificate,validate_errors,
    interval,bounds,
)


def selected_centres(a,b,ids,depth):
    """Decode word indices directly; do not enumerate a complete level."""
    points=np.zeros((len(ids),3),dtype=np.int64)
    remaining=ids.astype(np.int64).copy()
    for _ in range(depth):
        digits=remaining%6
        remaining//=6
        points=(np.einsum('nij,nj->ni',a[digits],points)//Q)+b[digits]
    assert np.all(remaining==0)
    return points


def scalar_centre(a,b,index,depth):
    p=[0,0,0]
    for _ in range(depth):
        k=index%6;index//=6
        p=[sum(int(a[k,i,j])*p[j] for j in range(3))//Q+int(b[k,i]) for i in range(3)]
    return p


def checker_tests():
    rng=np.random.default_rng(20261117)
    tests=[]
    # Negative cells, exact-distance boundaries, diagonal and non-neighbour cells.
    examples=[(np.array([[0,0,0],[10,0,0]],dtype=np.int64),10),
              (np.array([[-10,-10,-10],[1,-10,-10]],dtype=np.int64),10),
              (np.array([[-1,-1,-1],[10,10,10]],dtype=np.int64),10),
              (np.array([[0,0,0],[0,0,0]],dtype=np.int64),1)]
    for _ in range(160):
        examples.append((rng.integers(-100,101,size=(rng.integers(2,30),3),dtype=np.int64),
                         int(rng.integers(1,40))))
    with tempfile.TemporaryDirectory() as directory:
        path=Path(directory)/'points.i64'
        for points,d in examples:
            expected=all(sum((int(points[i,k])-int(points[j,k]))**2 for k in range(3))>d*d
                         for i in range(len(points)) for j in range(i))
            points.astype('<i8').tofile(path)
            result=subprocess.run([str(ROOT/'verify_packing'),str(path),str(d)],
                                  capture_output=True,text=True)
            assert (result.returncode==0)==expected,(points,d,result.stderr)
            tests.append(expected)
        path.write_bytes(b'truncated')
        assert subprocess.run([str(ROOT/'verify_packing'),str(path),'10'],
                              capture_output=True).returncode!=0
    return {'brute_force_comparisons':len(tests),
            'valid_examples':sum(tests),'invalid_examples':len(tests)-sum(tests),
            'truncation_rejected':True}


def main():
    cert=json.loads((ROOT/'dimension_certificate.json').read_text())
    root=json.loads((ROOT/'positive_contact_certificate.json').read_text())
    a,b=grid_maps(root)
    assert a.tolist()==cert['a_grid'] and b.tolist()==cert['b_grid']
    radial_depth=cert['radial_geometry']['depth']
    all_points=grid_centres(a,b,radial_depth)
    radial=radial_geometry(all_points,radial_depth)
    assert radial==cert['radial_geometry']
    # Component bounds exclude overflow. Python arbitrary-precision scalar
    # arithmetic independently rechecks both extremal words and their norms.
    for which in ['minimum','maximum']:
        index=radial[f'{which}_norm_word_index']
        point=scalar_centre(a,b,index,radial_depth)
        assert sum(v*v for v in point)==radial[f'{which}_grid_norm_squared']
    del all_points
    checks=[]
    rng=np.random.default_rng(17)
    for rec in cert['results']:
        name=rec['name'];depth=rec['depth']
        ids=np.load(ROOT/f'{name}_words.npy')
        coords=np.fromfile(ROOT/f'{name}_centres.i64',dtype='<i8').reshape(-1,3)
        assert len(ids)==rec['count'] and len(np.unique(ids))==len(ids)
        direct=selected_centres(a,b,ids,depth)
        assert np.array_equal(direct,coords)
        sample=rng.choice(len(ids),300,replace=False)
        for i in sample:
            assert scalar_centre(a,b,int(ids[i]),depth)==coords[i].tolist()
        # Repeat the complete exact check, independently of kd-tree selection.
        verified=subprocess.run([str(ROOT/'verify_packing'),str(ROOT/f'{name}_centres.i64'),
                                 str(rec['required_centre_distance_grid_units'])],
                                check=True,capture_output=True,text=True)
        assert json.loads(verified.stdout)==rec['exact_pair_verification']
        checks.append({'name':name,'all_selected_word_centres_recomputed':len(ids),
                       'scalar_arbitrary_precision_integer_checks':len(sample),
                       'complete_pair_verification_reproduced':True})
    mp.iv.dps=90
    family=sharp_family_certificate(root)
    assert family['passed']
    assert float(family['derivative_norm_upper'])<.02
    error=validate_errors()
    # Check affine-in-height identity numerically via the independently
    # assembled word matrices in mpmath, rather than the interval AD class.
    mp.mp.dps=100
    r=mp.mpf(root['reference_r']);u=mp.mpf(root['reference_half_angle_tangent'])
    def point(h):
        m=mp.eye(3);v=mp.matrix([0,0,0])
        angle=2*mp.atan(u)
        for k in root['word']:
            phi=mp.pi*k/3;sgn=(-1)**k
            axis=mp.matrix([-mp.sin(phi),mp.cos(phi),0])
            skew=mp.matrix([[0,-axis[2],axis[1]],
                            [axis[2],0,-axis[0]],[-axis[1],axis[0],0]])
            rotation=mp.expm(sgn*angle*skew)
            v+=m*mp.matrix([mp.cos(phi),mp.sin(phi),sgn*h])
            m=m*(r*rotation)
        return mp.lu_solve(mp.eye(3)-m,v)
    p0,p1=point(0),point(1)
    affine=max(abs(x) for h in [mp.mpf('.7070'),mp.mpf('.7072')]
               for x in point(h)-(p0+h*(p1-p0)))
    assert affine<mp.mpf('1e-95')
    result={'packing_checker_tests':checker_tests(),'subsystem_checks':checks,
            'full_radial_enclosure_reproduced':True,
            'family_interval_certificate_at_90_digits':True,
            'family_derivative_norm_upper_90_digits':family['derivative_norm_upper'],
            'independent_exponential_height_affinity_residual':mp.nstr(affine,40),
            'error_bounds_rechecked':error,'passed':True}
    (ROOT/'dimension_verification.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2),flush=True)


if __name__=='__main__':
    main()
