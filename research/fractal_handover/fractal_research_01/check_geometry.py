"""Independent numerical checks of the analytic derivations in RESEARCH.md.

These checks support the algebra; they are not interval-arithmetic certificates.
"""
import json
import math
from pathlib import Path
import numpy as np
from scipy.spatial import cKDTree
from explore import centres, xy


def main():
    rc=(math.sqrt(15)-math.sqrt(3))/6
    h=(math.sqrt(3)/2+rc)/(1-rc**2)
    assert abs(3*rc**2+math.sqrt(3)*rc-1)<1e-14
    assert abs(2*rc*h-1)<1e-14

    # Explicit support points, including many different positions on the contact.
    a=rc*np.exp(1j*np.pi/6)
    n=40
    powers=a**np.arange(n)
    rng=np.random.default_rng(20261117)
    errors=[]
    for _ in range(1000):
        digits=[]
        for k in range(n):
            m=k//2
            index=((1-m)+int(rng.integers(2)))%6 if k%2==0 else (1-m)%6
            digits.append(np.exp(1j*index*np.pi/3))
        z=np.dot(powers,np.array(digits))
        # z and conjugate(z) both belong to the common-rotation attractor
        # in the infinite-series limit. Adjacent pieces meet at these points.
        p0=1+a*z
        p1=np.exp(1j*np.pi/3)+a*np.conj(z)
        errors.append(abs(p0-p1))
    assert max(errors)<1e-13

    # At 30 degrees, alternating +/- turns and uniform +30 turns give the
    # same finite centre sets (their order differs).
    for r in (1/3,.35,rc,.375):
        p=centres(r,30,5)
        q=np.array([0j])
        b=np.exp(1j*np.arange(6)*np.pi/3)
        common=r*np.exp(1j*np.pi/6)
        for _ in range(5):
            q=(common*q[None,:]+b[:,None]).ravel()
        residual=float(cKDTree(xy(p)).query(xy(q))[0].max())
        assert residual<1e-13

    # 60 degree equivalence and 120 degree parameter periodicity.
    p=centres(.35,17,5)
    p_negative=centres(.35,-17,5)
    p_period=centres(.35,137,5)
    flip_residual=float(cKDTree(xy(p_negative)).query(xy(p*np.exp(1j*np.pi/3)))[0].max())
    period_residual=float(cKDTree(xy(p)).query(xy(p_period))[0].max())
    assert flip_residual<1e-13 and period_residual<1e-13

    result={
        'critical_r_30_degrees':rc,
        'critical_polynomial_residual':abs(3*rc**2+math.sqrt(3)*rc-1),
        'contact_points_checked':len(errors),
        'largest_contact_point_residual':float(max(errors)),
        'whole_dimension_at_critical_OSC':math.log(6)/math.log(1/rc),
        'adjacent_contact_set_dimension':math.log(2)/math.log(1/rc**2),
        'negative_angle_rotation_residual':flip_residual,
        'angle_periodicity_residual':period_residual,
        'status':'Checks passed. Analytic proof is in RESEARCH.md; no novelty established.'}
    Path(__file__).with_name('geometry_checks.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':
    main()
