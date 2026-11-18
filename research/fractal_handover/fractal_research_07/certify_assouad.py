"""Interval premises for the all-scale Assouad-dimension deduction.

The compact-group and weak-separation arguments are analytic, documented in
RESEARCH_07.md. This program certifies the parameter-dependent hypotheses.
"""
from pathlib import Path
import json
import mpmath as mp

import certify_witness as cert
from family_box import sharp_family_certificate
from verify_positive_contact import symbolic_symmetries

ROOT=Path(__file__).resolve().parent


def interval_rotations(u):
    iv=mp.iv
    a=iv.sqrt(3)/2
    co=[iv.mpf(1),iv.mpf('.5'),iv.mpf('-.5'),iv.mpf(-1),iv.mpf('-.5'),iv.mpf('.5')]
    si=[iv.mpf(0),a,a,iv.mpf(0),-a,-a]
    c=(1-u*u)/(1+u*u);s=2*u/(1+u*u)
    matrices=[]
    for k in range(6):
        x,y=-si[k],co[k];w=1-c;ss=(-1)**k*s
        matrices.append([[c+x*x*w,x*y*w,y*ss],
                         [x*y*w,c+y*y*w,-x*ss],[-y*ss,x*ss,c]])
    return matrices


def product(matrices,word):
    m=[[cert.interval(int(i==j)) for j in range(3)] for i in range(3)]
    for k in word:
        m=[[sum(m[i][j]*matrices[k][j][l] for j in range(3))
            for l in range(3)] for i in range(3)]
    return m


def trace(m):
    return sum(m[i][i] for i in range(3))


def axial_skew(m):
    return [m[2][1]-m[1][2],m[0][2]-m[2][0],m[1][0]-m[0][1]]


def cross(x,y):
    return [x[1]*y[2]-x[2]*y[1],x[2]*y[0]-x[0]*y[2],x[0]*y[1]-x[1]*y[0]]


def serial(x):
    # Diagnostic endpoints only. Strict decisions use the interval objects.
    return [mp.nstr(v,45) for v in cert.bounds(x)]


def rotation_pair_certificate(first,second):
    t0,t1=trace(first),trace(second)
    assert cert.bounds(t0)[0]>2 and cert.bounds(t0)[1]<3
    assert cert.bounds(t1)[0]>2 and cert.bounds(t1)[1]<3
    # For a rotation with angle in (0,pi), the axial skew vector is a
    # nonzero multiple of its oriented axis. A nonzero cross component
    # proves that the two axis lines differ.
    cp=cross(axial_skew(first),axial_skew(second))
    nonzero=[i for i,v in enumerate(cp) if cert.bounds(v)[1]<0 or cert.bounds(v)[0]>0]
    assert nonzero
    return {'passed':True,'first_trace_interval':serial(t0),
            'second_trace_interval':serial(t1),
            'axis_cross_product_intervals':[serial(v) for v in cp],
            'certified_nonzero_cross_components':nonzero,
            'angle_consequence':'Both principal rotation angles lie strictly between 0 and 60 degrees.',
            'group_consequence':'The generated subgroup is dense in SO(3), by the closed-subgroup classification.'}


def rotation_certificate(data,precision):
    cert.iv.dps=precision
    centre=mp.mpf(data['reference_half_angle_tangent'])
    u=cert.interval(centre-mp.mpf('.00006'),centre+mp.mpf('.00006'))
    q=interval_rotations(u)
    A=product(q,data['word']);B=product(q,data['partner_word'])
    local=rotation_pair_certificate(q[0],q[1])
    blocks=rotation_pair_certificate(A,B)
    return {'interval_decimal_digits':precision,
            'u_interval_diagnostic':serial(u),
            'local_rotation_pair':local,'common_fixed_point_block_pair':blocks,
            'block_A_intervals':[[serial(v) for v in row] for row in A],
            'block_B_intervals':[[serial(v) for v in row] for row in B]}


def main():
    mp.mp.dps=100;cert.iv.dps=70
    data=json.loads((ROOT/'positive_contact_certificate.json').read_text())
    identities=symbolic_symmetries()
    repeated={}
    for name in ['tight_root_certificate','connected_family_certificate']:
        old=data[name]
        value=cert.contraction_certificate(old['centre'],old['radius'],*old['height_interval'])
        assert value['passed']
        repeated[name]=value
    family=sharp_family_certificate(data)
    rotations=[rotation_certificate(data,precision) for precision in [70,90]]
    # Four fixed points span R^3 throughout the original wider family box.
    full=repeated['connected_family_certificate']
    assert mp.mpf(full['spatial_fixed_point_x_interval'][0])>0
    assert mp.mpf(full['spatial_fixed_point_z_interval'][0])>0
    rmax=cert.interval('.476186')
    smax=mp.iv.log(6)/mp.iv.log(1/rmax)
    assert cert.bounds(smax)[1]<mp.mpf('2.4150')<3
    result={
        'passed':True,'symbolic_symmetry_identities':identities,
        'repeated_contact_certificates':repeated,
        'sharper_family_certificate':family,
        'rotation_certificates':rotations,
        'affine_span_dimension':3,
        'family_Hausdorff_upper_bound_diagnostic':mp.nstr(cert.bounds(smax)[1],45),
        'analytic_deduction':{
            'weak_separation_property':False,
            'Assouad_dimension':3,
            'Hausdorff_dimension':'Still bounded as before; not determined exactly.',
            'alternative_finite_similarity_IFS_with_WSP_possible':False,
            'alternative_finite_similarity_IFS_with_OSC_possible':False,
            'scope':'Every member of the connected curve, h in [.7070,.7072].',
            'published_dimension_theorem':'Ignacio Garcia, Corollary 1.6(1), Assouad dimension and local structure of self-similar sets with overlaps in R^d.',
        },
        'proof_scope':'Interval premises plus the analytic arguments and cited theorems in RESEARCH_07.md; independent mathematical review remains required.',
    }
    (ROOT/'assouad_certificate.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'passed':True,
                     'block_pair':rotations[0]['common_fixed_point_block_pair'],
                     'local_pair':rotations[0]['local_rotation_pair'],
                     'analytic_deduction':result['analytic_deduction']},indent=2),flush=True)


if __name__=='__main__':main()
