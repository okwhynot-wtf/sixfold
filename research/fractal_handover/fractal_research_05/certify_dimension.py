"""Certified separated subsystems inside the connected spatial attractor.

The kd-tree proposes a packing only. verify_packing.cpp checks all possibly
close pairs using exact integers and a complete cell-neighbour enumeration.
"""
from pathlib import Path
from fractions import Fraction
import argparse
import hashlib
import json
import math
import subprocess
import time

import mpmath as mp
import numpy as np
from scipy.spatial import cKDTree

from certify_witness import (
    interval, bounds, midpoint, magnitude, residual_dual,
    contraction_certificate,
)

ROOT = Path(__file__).resolve().parent
Q = 2**29
BOUND = Fraction(5, 2)
PACKING_BOUND = Fraction(107, 50)
GRID_ERROR = Fraction(1, 10**6)
mp.mp.dps = 100
mp.iv.dps = 70


def serial(x):
    # Decimal endpoints are output for diagnostics. Proof decisions use the
    # interval objects, never rounded diagnostic endpoints.
    return [mp.nstr(v, 45) for v in bounds(x)]


def sharp_family_certificate(data):
    """Use the EXACT affine dependence on h before interval multiplication.

    F(x0,h) = F(x0,h0) + F_h(x0)*(h-h0), since the word matrix is
    independent of h and every translation is affine in h. Multiplying C
    into F_h before multiplying the height interval avoids lost correlation.
    """
    centre = [data['reference_r'], data['reference_half_angle_tangent']]
    radii = [mp.mpf('.000007'), mp.mpf('.00006')]
    x0 = [interval(v) for v in centre]
    box = [interval(mp.mpf(centre[i])-radii[i],
                    mp.mpf(centre[i])+radii[i]) for i in range(2)]
    h = interval('.7070', '.7072')
    h0 = 1/mp.iv.sqrt(2)
    fbase = residual_dual(*x0, h0)
    fzero = residual_dual(*x0, interval(0))
    fone = residual_dual(*x0, interval(1))
    slope = [fone[i].v-fzero[i].v for i in range(2)]
    jac0 = mp.matrix([[midpoint(v.d[j]) for j in range(2)] for v in fbase])
    inverse = jac0**-1
    c = [[interval(mp.nstr(inverse[i,j],55)) for j in range(2)] for i in range(2)]
    domain = residual_dual(*box, h)
    remainder = [[interval(int(i==j))-sum(c[i][k]*domain[k].d[j]
                     for k in range(2)) for j in range(2)] for i in range(2)]
    image = []
    for i in range(2):
        offset = sum(c[i][k]*fbase[k].v for k in range(2))
        height_slope = sum(c[i][k]*slope[k] for k in range(2))
        value = x0[i]-offset-height_slope*(h-h0)
        value += sum(remainder[i][j]*interval(-radii[j],radii[j]) for j in range(2))
        image.append(value)
    norm = max(sum(magnitude(v) for v in row) for row in remainder)
    margins = [min(bounds(image[i])[0]-bounds(box[i])[0],
                   bounds(box[i])[1]-bounds(image[i])[1]) for i in range(2)]
    assert norm < 1 and min(margins) > 0
    # This tighter box is inside the previously certified family box, so
    # uniqueness identifies the same connected family, not a second branch.
    assert all(v < mp.mpf('.001') for v in radii)
    rlo, rhi = Fraction('0.476171'), Fraction('0.476186')
    assert interval(str(rlo.numerator))/rlo.denominator < box[0]
    assert box[0] < interval(str(rhi.numerator))/rhi.denominator
    return {
        'passed': True, 'centre': centre, 'radii': [str(v) for v in radii],
        'height_interval': ['.7070', '.7072'],
        'parameter_box_diagnostic': [serial(v) for v in box],
        'image_diagnostic': [serial(v) for v in image],
        'derivative_norm_upper': mp.nstr(norm,45),
        'strict_inclusion_margins': [mp.nstr(v,45) for v in margins],
        'preconditioner': [[mp.nstr(midpoint(v),55) for v in row] for row in c],
        'preconditioned_height_slope': [serial(sum(c[i][k]*slope[k] for k in range(2)))
                                         for i in range(2)],
        'outward_rational_r_bounds': [str(rlo), str(rhi)],
    }


def grid_value(x):
    lo, hi = bounds(x)
    n = int(mp.nint((lo+hi)*Q/2))
    assert mp.mpf(n-1)/Q <= lo and hi <= mp.mpf(n+1)/Q
    return n


def grid_maps(data):
    centre = [mp.mpf(data['reference_r']), mp.mpf(data['reference_half_angle_tangent'])]
    r,u = [interval(v-mp.mpf('1e-25'), v+mp.mpf('1e-25')) for v in centre]
    h = 1/mp.iv.sqrt(2)
    cosine = (1-u*u)/(1+u*u)
    sine = 2*u/(1+u*u)
    aa,bb = [],[]
    for k in range(6):
        phi = mp.iv.pi*k/3
        sign = 1 if k%2==0 else -1
        x,y = -mp.iv.sin(phi), mp.iv.cos(phi)
        w,s = 1-cosine, sign*sine
        rot = [[cosine+x*x*w, x*y*w, y*s],
               [y*x*w, cosine+y*y*w, -x*s],
               [-y*s, x*s, cosine]]
        aa.append([[grid_value(r*v) for v in row] for row in rot])
        bb.append([grid_value(mp.iv.cos(phi)),grid_value(mp.iv.sin(phi)),grid_value(sign*h)])
    return np.array(aa,dtype=np.int64),np.array(bb,dtype=np.int64)


def grid_centres(a,b,depth):
    p = np.zeros((1,3),dtype=np.int64)
    for _ in range(depth):
        assert np.abs(p).max(initial=0) < 3*Q
        p = np.concatenate([(p@a[k].T)//Q+b[k] for k in range(6)],axis=0)
    return p


def rational_interval(x):
    return interval(x.numerator)/x.denominator


def ceil_fraction(x):
    return (x.numerator+x.denominator-1)//x.denominator


def dimension_interval(count, depth, rlo, rhi):
    lo = mp.iv.log(count)/(depth*mp.iv.log(1/rational_interval(rlo)))
    hi = mp.iv.log(6)/mp.iv.log(1/rational_interval(rhi))
    return {'lower':mp.nstr(bounds(lo)[0],40),
            'upper':mp.nstr(bounds(hi)[1],40)}


def radial_geometry(p,depth):
    """Enclose K using the original radius-2.5 tail, then tighten the ball.

    All true family centres are within .00055 of the reference grid centres.
    No assumption that the smaller radius-2.14 ball is invariant is needed.
    """
    assert np.abs(p).max(initial=0)<3*Q
    assert 27*Q**2<2**63  # the integer sums of three squares cannot overflow
    squared=np.sum(p*p,axis=1)
    minimum,maximum=int(squared.min()),int(squared.max())
    tail=rational_interval(BOUND*Fraction('.476186')**depth+Fraction('.00055'))
    inner=mp.iv.sqrt(minimum)/Q-tail
    outer=mp.iv.sqrt(maximum)/Q+tail
    assert bounds(inner)[0]>mp.mpf('.398')
    assert bounds(outer)[1]<mp.mpf('2.14')
    return {'depth':depth,'minimum_grid_norm_squared':minimum,
            'maximum_grid_norm_squared':maximum,
            'minimum_norm_word_index':int(np.argmin(squared)),
            'maximum_norm_word_index':int(np.argmax(squared)),
            'inner_radius_lower':mp.nstr(bounds(inner)[0],45),
            'outer_radius_upper':mp.nstr(bounds(outer)[1],45),
            'safe_empty_central_ball_radius':'.398',
            'safe_enclosing_ball_radius':'2.14',
            'scope':'Every member of the certified connected curve.'}


def select_packing(p, distance, seed=17):
    # The kd-tree is not trusted as a proof. Include a rounding guard here;
    # the independent exact checker determines whether the result is valid.
    points = p.astype(float)/Q
    tree = cKDTree(points)
    order = np.random.default_rng(seed).permutation(len(p))
    blocked = np.zeros(len(p),dtype=bool)
    chosen = []
    for index in order:
        if not blocked[index]:
            chosen.append(index)
            blocked[tree.query_ball_point(points[index],distance/Q*(1+1e-12))] = True
    return np.array(chosen,dtype=np.uint32)


def validate_errors():
    # coefficient error <=1/Q, translation error norm <=sqrt(3)/Q,
    # and componentwise floor error norm <sqrt(3)/Q.
    # Inductively e<GRID_ERROR gives approximate-centre norm <3. Decompose
    # the new error as A*(p-c)+(Ahat-A)*p+translation error+floor error.
    # Thus e_next <=.49*e+(9+2sqrt(3))/Q < .49*e+13/Q.
    assert Fraction(13,Q)/(1-Fraction(49,100)) < GRID_ERROR
    assert Fraction(9,2)*Q**2+9*Q < 2**63
    assert Fraction(49,100)*BOUND+Fraction(5,4) < BOUND
    assert Fraction(3,2) < Fraction(5,4)**2
    # Across the narrower family box, compare to the exact reference root.
    dr,du,dh = Fraction('0.0000071'),Fraction('0.0000601'),Fraction('.000107')
    h0 = 1/mp.iv.sqrt(2)
    assert bounds(h0-interval('.7070'))[1] < bounds(rational_interval(dh))[0]
    assert bounds(interval('.7072')-h0)[1] < bounds(rational_interval(dh))[0]
    # ||A(h)-A(h0)|| <= dr+2*rmax*du because |atan'|<=1.
    perturbation = (BOUND*(dr+2*Fraction(49,100)*du)+dh)/(1-Fraction(49,100))
    family_error = Fraction('.00055')
    assert perturbation+GRID_ERROR < family_error
    return {'grid_error':str(GRID_ERROR),'family_error':str(family_error),
            'parameter_difference_bounds':{'r':str(dr),'u':str(du),'h':str(dh)},
            'derived_trajectory_perturbation_bound':str(perturbation)}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--depth',type=int,default=8)
    args = parser.parse_args()
    start = time.time()
    data = json.loads((ROOT/'positive_contact_certificate.json').read_text())
    tight = data['tight_root_certificate']
    reproduced = contraction_certificate(tight['centre'],tight['radius'],*tight['height_interval'])
    assert reproduced['passed']
    family = sharp_family_certificate(data)
    errors = validate_errors()
    a,b = grid_maps(data)
    p = grid_centres(a,b,args.depth)
    radial = radial_geometry(p,args.depth)
    np.save(ROOT/'a_grid.npy',a)
    np.save(ROOT/'b_grid.npy',b)
    subprocess.run(['g++','-O3','-std=c++17',str(ROOT/'verify_packing.cpp'),'-o',
                    str(ROOT/'verify_packing')],check=True)
    results = []
    for name,rlo,rhi,error in [
        ('reference',Fraction('0.4761783861615476'),Fraction('0.4761783861615478'),GRID_ERROR),
        ('whole_family',Fraction('0.476171'),Fraction('0.476186'),Fraction('.00055')),
    ]:
        if name=='reference':
            assert rational_interval(rlo) < interval(data['reference_r'])-interval('1e-25')
            assert interval(data['reference_r'])+interval('1e-25') < rational_interval(rhi)
        halfwidth = ceil_fraction(Q*(PACKING_BOUND*rhi**args.depth+error))
        distance = 2*halfwidth+1
        ids = select_packing(p,distance)
        chosen = p[ids]
        ids_path = ROOT/f'{name}_words.npy'
        coords_path = ROOT/f'{name}_centres.i64'
        np.save(ids_path,ids)
        chosen.astype('<i8').tofile(coords_path)
        result = subprocess.run([str(ROOT/'verify_packing'),str(coords_path),str(distance)],
                                check=True,capture_output=True,text=True)
        exact = json.loads(result.stdout)
        assert exact['passed'] and exact['points']==len(ids)
        dims = dimension_interval(len(ids),args.depth,rlo,rhi)
        results.append({
            'name':name,'depth':args.depth,'count':len(ids),'seed':17,
            'r_lower':str(rlo),'r_upper':str(rhi),'centre_error_bound':str(error),
            'enclosing_radius_grid_units':halfwidth,
            'required_centre_distance_grid_units':distance,
            'dimension_bounds':dims,'exact_pair_verification':exact,
            'word_indices_sha256':hashlib.sha256(ids_path.read_bytes()).hexdigest(),
            'coordinates_sha256':hashlib.sha256(coords_path.read_bytes()).hexdigest(),
        })
        print(json.dumps(results[-1],indent=2),flush=True)
    # Opposite translations are antipodal. Use the now-established radius
    # bound for K, hence radius 2.14*r for each first-level piece.
    opposite_gap = 2*mp.iv.sqrt(1+interval('.7070')**2)-2*interval('2.14')*interval('.476186')
    assert bounds(opposite_gap)[0] > 0
    summary = {
        'Q':Q,'initial_ball_bound':'5/2','packing_ball_bound':str(PACKING_BOUND),
        'radial_geometry':radial,'family_certificate':family,'error_bounds':errors,
        'a_grid':a.tolist(),'b_grid':b.tolist(),'results':results,
        'opposite_piece_gap_lower':mp.nstr(bounds(opposite_gap)[0],40),
        'elapsed_seconds':time.time()-start,
        'status':'Certified lower bounds from separated subsystems; full OSC and exact dimension remain open.',
    }
    (ROOT/'dimension_certificate.json').write_text(json.dumps(summary,indent=2)+'\n')


if __name__=='__main__':
    main()
