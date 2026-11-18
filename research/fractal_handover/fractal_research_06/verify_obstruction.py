"""Recheck the exact premises for the all-scale OSC obstruction.

The contradiction for every possible feasible open set is an analytic volume
argument in RESEARCH_06.md. It does not rely on finite-depth numerical trends.
"""
from pathlib import Path
import itertools
import json
import mpmath as mp
import sympy as sp

import certify_witness as cert
from family_box import sharp_family_certificate
from verify_positive_contact import symbolic_symmetries,exponential_point

ROOT=Path(__file__).resolve().parent


def interval_maps(r,u,h):
    iv=mp.iv
    c=(1-u*u)/(1+u*u);sine=2*u/(1+u*u)
    aa=[];bb=[]
    for k in range(6):
        phi=iv.pi*k/3;sign=(-1)**k
        x,y=-iv.sin(phi),iv.cos(phi);w=1-c;s=sign*sine
        aa.append([[r*(c+x*x*w),r*x*y*w,r*y*s],
                   [r*x*y*w,r*(c+y*y*w),-r*x*s],
                   [-r*y*s,r*x*s,r*c]])
        bb.append([iv.cos(phi),iv.sin(phi),sign*h])
    return aa,bb


def crossing_certificate(data):
    centre=[mp.mpf(data['reference_r']),mp.mpf(data['reference_half_angle_tangent'])]
    r,u=[cert.interval(centre[i]-mp.mpf(rad),centre[i]+mp.mpf(rad))
         for i,rad in enumerate(['.000007','.00006'])]
    h=cert.interval('.7070','.7072')
    a,b=interval_maps(r,u,h)
    negative=[v.v for v in cert.periodic_dual(r,u,h,word=[3])]
    for k in reversed([0,3,3,1]):
        negative=[sum(a[k][i][j]*negative[j] for j in range(3))+b[k][i] for i in range(3)]
    positive=[v.v for v in cert.periodic_dual(r,u,h,word=[0])]
    normal=[mp.iv.sqrt(3)/2,cert.interval('-.5'),cert.interval(0)]
    neg=sum(normal[i]*negative[i] for i in range(3))
    pos=sum(normal[i]*positive[i] for i in range(3))
    assert cert.bounds(neg)[1]<0<cert.bounds(pos)[0]
    def serial(x):return [mp.nstr(v,45) for v in cert.bounds(x)]
    return {'passed':True,'negative_address_prefix':[0,3,3,1],
            'negative_address_repeating_terminal':3,
            'positive_address_repeating_terminal':0,
            'negative_point_intervals':[serial(v) for v in negative],
            'positive_point_intervals':[serial(v) for v in positive],
            'negative_signed_distance_interval':serial(neg),
            'positive_signed_distance_interval':serial(pos),
            'plane_normal':['sqrt(3)/2','-1/2','0'],
            'scope':'Every member of the certified connected curve.'}


def symbolic_packing_argument():
    # Cancellation of the common scale is exact. Growth of 2**m then
    # contradicts the resulting constant bound for any proposed open ball.
    m=sp.symbols('m',integer=True,positive=True)
    q,e,d,v=sp.symbols('q epsilon D v',positive=True)
    total=2**m*v*(e*q**m)**3
    container=v*((d+e)*q**m)**3
    assert sp.simplify(total/container-2**m*(e/(d+e))**3)==0
    return str(sp.simplify(total/container))


def main():
    data=json.loads((ROOT/'positive_contact_certificate.json').read_text())
    word=data['word'];partner=data['partner_word']
    assert word==[0,1,1,5,3,5,1,3]
    assert partner==[(1-k)%6 for k in word]
    assert len(word)==len(partner)==8 and word[0]!=partner[0]
    identities=symbolic_symmetries()
    # The reflection V=T*S used for the additional same-parity contacts.
    a=sp.sqrt(3)/2
    S=sp.Matrix([[sp.Rational(1,2),a,0],[a,-sp.Rational(1,2),0],[0,0,-1]])
    T=sp.Matrix([[sp.Rational(1,2),-a,0],[a,sp.Rational(1,2),0],[0,0,-1]])
    V=T*S;n=sp.Matrix([a,-sp.Rational(1,2),0])
    assert V==sp.eye(3)-2*n*n.T
    assert V*V==sp.eye(3) and n.dot(n)==1
    # Both known contact certificates are re-run, at two interval precisions.
    repeated=[]
    for digits in [70,90]:
        cert.iv.dps=digits
        row={'interval_decimal_digits':digits}
        for name in ['tight_root_certificate','connected_family_certificate']:
            old=data[name]
            value=cert.contraction_certificate(old['centre'],old['radius'],*old['height_interval'])
            assert value['passed']
            row[name]={'passed':True,'derivative_norm_upper':value['derivative_norm_upper'],
                       'strict_inclusion_margins':value['strict_inclusion_margins']}
        repeated.append(row)
    # Establish the narrower curve enclosure for the extra crossing proof.
    family=sharp_family_certificate(data)
    crossing=crossing_certificate(data)
    # A fresh, conservative exclusion for opposite pairs needs only the
    # original invariant radius-2.5 ball and the wider contact proof box.
    maximum_r=cert.interval(data['reference_r'])+cert.interval('.001')
    opposite_gap=2*mp.iv.sqrt(1+cert.interval('.7070')**2)-5*maximum_r
    assert cert.bounds(opposite_gap)[0]>mp.mpf('.0634')
    # Supplementary numerical check: separately implemented exponential
    # rotations for all binary block concatenations through four blocks.
    mp.mp.dps=100
    r=mp.mpf(data['reference_r']);u=mp.mpf(data['reference_half_angle_tangent'])
    h=1/mp.sqrt(2)
    reference=exponential_point(r,u,h,word)
    maximum_error=mp.mpf(0);count=0
    for blocks in range(1,5):
        seen=set()
        for choices in itertools.product([0,1],repeat=blocks):
            w=sum([word if choice==0 else partner for choice in choices],[])
            assert len(w)==8*blocks
            seen.add(tuple(w))
            point=exponential_point(r,u,h,w)
            maximum_error=max(maximum_error,max(abs(point[i]-reference[i]) for i in range(3)))
            count+=1
        assert len(seen)==2**blocks
    assert maximum_error<mp.mpf('1e-50')
    ratio=symbolic_packing_argument()
    result={
        'passed':True,'word':word,'partner_word':partner,
        'symbolic_local_conjugacy_identities':identities,
        'reflection_plane_identity_checked':True,
        'repeated_contact_certificates':repeated,
        'sharper_family_certificate':family,
        'additional_crossing_contacts':crossing,
        'opposite_pair_gap_lower':mp.nstr(cert.bounds(opposite_gap)[0],45),
        'binary_block_fixed_points_checked':count,
        'maximum_independent_fixed_point_difference':mp.nstr(maximum_error,45),
        'symbolic_ball_volume_ratio':ratio,
        'analytic_consequence':'OSC fails for the given six-map IFS throughout the certified connected curve.',
        'review_scope':'Computer-assisted parameter premises plus an elementary all-scale volume argument; independent review still required.',
    }
    (ROOT/'osc_obstruction_verification.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2),flush=True)


if __name__=='__main__':main()
