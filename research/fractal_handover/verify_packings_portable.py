"""Portable exact verification of the supplied separated-subsystem data.

Uses Python integers and NumPy; no C++ compiler is needed. The original C++
checker remains in phase 05. This implementation rechecks its recorded pair
counts and integer distance minima as well as the word-centre correspondence.
"""
from pathlib import Path
from fractions import Fraction
import argparse
import hashlib
import itertools
import json
import sys


def exact_pairs(coordinates,distance):
    cells={};checks=0;minimum=None;threshold=distance*distance
    offsets=list(itertools.product((-1,0,1),repeat=3))
    for row in coordinates:
        p=tuple(int(v) for v in row)
        cell=tuple(v//distance for v in p)
        for dx,dy,dz in offsets:
            for q in cells.get((cell[0]+dx,cell[1]+dy,cell[2]+dz),()):
                squared=(p[0]-q[0])**2+(p[1]-q[1])**2+(p[2]-q[2])**2
                checks+=1
                minimum=squared if minimum is None else min(minimum,squared)
                if squared<=threshold:raise ValueError('Exact packing separation failed')
        cells.setdefault(cell,[]).append(p)
    return {'passed':True,'points':len(coordinates),'cell_width':distance,
            'checked_pairs':checks,'minimum_checked_distance_squared':minimum,
            'threshold_distance_squared':threshold}


def checker_checks(np):
    examples=[([[0,0,0],[10,0,0]],10),
              ([[-10,-10,-10],[1,-10,-10]],10),
              ([[-1,-1,-1],[10,10,10]],10),
              ([[0,0,0],[0,0,0]],1)]
    rng=np.random.default_rng(20261117)
    for _ in range(30):
        examples.append((rng.integers(-70,71,size=(int(rng.integers(2,25)),3)).tolist(),
                         int(rng.integers(1,35))))
    for points,d in examples:
        expected=all(sum((points[i][k]-points[j][k])**2 for k in range(3))>d*d
                     for i in range(len(points)) for j in range(i))
        try:exact_pairs(points,d);actual=True
        except ValueError:actual=False
        assert actual==expected
    return len(examples)


def main():
    if not __debug__:raise RuntimeError('Run without -O: the scientific checks use assertions')
    parser=argparse.ArgumentParser()
    parser.add_argument('--phase-dir',type=Path,default=Path(__file__).resolve().parent/'fractal_research_05')
    args=parser.parse_args();root=args.phase_dir.resolve()
    sys.path.insert(0,str(root))
    import numpy as np
    import mpmath as mp
    from certify_dimension import (Q,grid_maps,grid_centres,radial_geometry,
                                   sharp_family_certificate,validate_errors,
                                   dimension_interval,ceil_fraction,PACKING_BOUND)
    from verify_dimension import selected_centres,scalar_centre
    cert=json.loads((root/'dimension_certificate.json').read_text())
    parameters=json.loads((root/'positive_contact_certificate.json').read_text())
    mp.iv.dps=90
    family=sharp_family_certificate(parameters)
    assert family['passed']
    error=validate_errors()
    a,b=grid_maps(parameters)
    assert a.tolist()==cert['a_grid'] and b.tolist()==cert['b_grid']
    depth=cert['radial_geometry']['depth']
    points=grid_centres(a,b,depth)
    assert radial_geometry(points,depth)==cert['radial_geometry']
    del points
    results=[]
    rng=np.random.default_rng(17)
    for rec in cert['results']:
        name=rec['name']
        ipath=root/f'{name}_words.npy';cpath=root/f'{name}_centres.i64'
        assert hashlib.sha256(ipath.read_bytes()).hexdigest()==rec['word_indices_sha256']
        assert hashlib.sha256(cpath.read_bytes()).hexdigest()==rec['coordinates_sha256']
        indices=np.load(ipath,allow_pickle=False)
        coordinates=np.fromfile(cpath,dtype='<i8').reshape(-1,3)
        assert len(indices)==rec['count'] and len(np.unique(indices))==len(indices)
        assert np.array_equal(selected_centres(a,b,indices,rec['depth']),coordinates)
        for index in rng.choice(len(indices),300,replace=False):
            assert scalar_centre(a,b,int(indices[index]),rec['depth'])==coordinates[index].tolist()
        radius=ceil_fraction(Q*(PACKING_BOUND*Fraction(rec['r_upper'])**rec['depth']
                                 +Fraction(rec['centre_error_bound'])))
        assert radius==rec['enclosing_radius_grid_units']
        distance=2*radius+1
        assert distance==rec['required_centre_distance_grid_units']
        checked=exact_pairs(coordinates,distance)
        assert checked==rec['exact_pair_verification']
        bounds=dimension_interval(len(indices),rec['depth'],Fraction(rec['r_lower']),Fraction(rec['r_upper']))
        assert mp.mpf(bounds['lower'])>mp.mpf('2.1970')
        assert mp.mpf(bounds['upper'])<mp.mpf('2.4150')
        results.append({'name':name,'word_centres_recomputed':len(indices),
                        'exact_pair_checks':checked,'dimension_bounds':bounds})
    result={'passed':True,'implementation':'Portable Python integer cell-neighbour checker',
            'brute_force_comparison_cases':checker_checks(np),
            'family_interval_proof_repeated':True,'radial_enclosure_reproduced':True,
            'error_bounds_rechecked':error,'results':results}
    print(json.dumps(result,indent=2),flush=True)


if __name__=='__main__':main()
