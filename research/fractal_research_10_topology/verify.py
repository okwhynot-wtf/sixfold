"""Outward-rounded geometry for the straight inherited axes and shrinking loops."""
from pathlib import Path
import argparse
import json
import math
import sys

from flint import arb, arb_mat, ctx, fmpq

ROOT = Path(__file__).resolve().parent
PHASES = ROOT.parent / "fractal_handover"
sys.path.insert(0, str(PHASES / "fractal_research_07"))
from certify_witness import contraction_certificate


WORDS = (
    "140442500212512530314114215341210010305433504500541430100240241222221404343444122114552142304351123052323",
    "144045453454235014141554530325230420152515423100150433103103514250534430312333453503140105310011304410453",
    "144404420221320555233013532524033001010032413031025221030501325335324423520150153340114013010013302315303",
)


def vector(*v):
    return arb_mat([[x] for x in v])


def box(a, b):
    return arb(a).union(arb(b))


def upper_decimal(value, places):
    """Float nominates a decimal grid point. A ball comparison certifies it."""
    scale = 10**places
    k = math.ceil(float(value.upper())*scale)+1
    assert value < arb(fmpq(k, scale))
    return k


def outward_pair(value, places):
    return [-upper_decimal(-value, places), upper_decimal(value, places)]


def make_maps(r, u, h):
    c, s = (1-u*u)/(1+u*u), 2*u/(1+u*u)
    half, v = arb(1)/2, arb(3).sqrt()/2
    cosines = [1, half, -half, -1, -half, half]
    sines = [0, v, v, 0, -v, -v]
    matrices, translations = [], []
    for k, (co, si) in enumerate(zip(cosines, sines)):
        x, y = -si, co
        ss = (-1)**k*s
        matrices.append(r*arb_mat([[c+x*x*(1-c), x*y*(1-c), y*ss],
                                   [x*y*(1-c), c+y*y*(1-c), -x*ss],
                                   [-y*ss, x*ss, c]]))
        translations.append(vector(co, si, (-1)**k*h))
    return c, s, matrices, translations


def fixed0(matrices, translations):
    eye = arb_mat([[1,0,0],[0,1,0],[0,0,1]])
    return (eye-matrices[0]).solve(translations[0])


def addressed_point(word, matrices, translations):
    point = fixed0(matrices,translations)
    for digit in reversed(word):
        k = int(digit)
        point = matrices[k]*point+translations[k]
    return point


def check_witnesses(params, limit, lower=None):
    r, u, h = params
    c, s, matrices, translations = make_maps(*params)
    results = []
    for word in WORDS:
        point = addressed_point(word,matrices,translations)
        dx = c*(point[0,0]-1)-s*(point[2,0]-h)
        dy = point[1,0]
        squared_upper = dx.abs_upper()**2 + dy.abs_upper()**2
        assert squared_upper < arb(limit)**2
        if lower is not None:
            assert dx.abs_lower()**2 + dy.abs_lower()**2 > arb(lower)**2
            assert not dy.contains(0)
        results.append({"prefix":word, "tail":"0 repeated forever",
                        "coordinate_box_in_millionths":[outward_pair(point[i,0],6) for i in range(3)],
                        "first_lobe":int(word[0]), "distance_upper":limit,
                        "certified_positive_lower_for_this_point":lower})
    return results


def first_intrusion(params, word, travel_lo, travel_hi):
    """Bound the first occupied normal cross-section of the radius-.0058 bore."""
    r,u,h = params
    c,s,matrices,t = make_maps(*params)
    radius = arb(".0058")
    assert r*arb(".0122") > radius  # Own child is excluded by the phase-08 proof.
    point = addressed_point(word,matrices,t)
    def travel(p):
        return -s*(p[0,0]-1)-c*(p[2,0]-h)
    def lateral(p):
        return c*(p[0,0]-1)-s*(p[2,0]-h)
    for j in (2,3,4):
        assert lateral(t[j]).abs_lower()**2+t[j][1,0].abs_lower()**2 > (arb("2.14")*r+radius)**2
    assert lateral(point).abs_upper()**2+point[1,0].abs_upper()**2 < radius**2
    assert travel(point) < arb(travel_hi)
    active = [(t[j],matrices[j]) for j in range(1,6)]
    checked = 0
    for n in range(1,30):
        new = []
        tail = arb("2.14")*r**n
        for centre,mat in active:
            checked += 1
            if travel(centre)-tail > arb(travel_lo):
                continue
            if lateral(centre).abs_lower()**2+centre[1,0].abs_lower()**2 > (radius+tail)**2:
                continue
            new.extend((centre+mat*t[j],mat*matrices[j]) for j in range(6))
        active = new
        if not active:
            break
    assert not active
    return {"straight_bore_radius":"0.0058", "travel_from_upper_centre":[travel_lo,travel_hi],
            "first_section_axis_point_in_millionths":[
                outward_pair(1-s*box(travel_lo,travel_hi),6),[0,0],
                outward_pair(h-c*box(travel_lo,travel_hi),6)],
            "witness_prefix":word,"witness_tail":"0 repeated forever",
            "interior_witness_coordinate_box_in_millionths":[outward_pair(point[i,0],6) for i in range(3)],
            "interior_witness_normal_plane_in_billionths":[outward_pair(lateral(point),9),
                                                           outward_pair(point[1,0],9)],
            "exclusion_nodes_checked":checked,"maximum_depth":n}


def localize(params, depth):
    """Exhaust every prefix whose enclosing ball could meet the exact line."""
    r, u, h = params
    c, s, matrices, translations = make_maps(*params)
    eye = arb_mat([[1,0,0],[0,1,0],[0,0,1]])
    active = [("", vector(0,0,0), eye)]
    counts = []
    for n in range(1, depth+1):
        new = []
        tail = arb("2.14")*r**n
        for prefix, centre, matrix in active:
            for k in range(6):
                point = centre + matrix*translations[k]
                dx = c*(point[0,0]-1)-s*(point[2,0]-h)
                # abs_lower is a certified lower bound even for zero-crossing balls.
                if dx.abs_lower()**2 + point[1,0].abs_lower()**2 > tail**2:
                    continue
                new.append((prefix+str(k),point,matrix*matrices[k]))
        active = new
        counts.append(len(active))
    assert {w[0] for w, _, _ in active} == {"1","5"}
    zboxes = []
    for _, point, _ in active:
        z = point[2,0]+(-tail).union(tail)
        zboxes.append(outward_pair(z,4))
    merged = []
    for low, high in sorted(zboxes):
        if merged and low <= merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], high)
        else:
            merged.append([low,high])
    return {"depth":depth, "remaining_prefix_counts":counts, "possible_lobes":[1,5],
            "possible_z_bands_in_ten_thousandths":merged}


def dot(a,b):
    return sum(a[i,0]*b[i,0] for i in range(3))


def length(v):
    return dot(v,v).nonnegative_part().sqrt()


def repeated_loops(params):
    r,u,h = params
    _,_,matrices,t = make_maps(*params)
    p = fixed0(matrices,t)
    child_radius = arb("2.14")*r
    e = vector(1,0,1)/arb(2).sqrt()
    d = vector(-1,0,1)/arb(2).sqrt()
    side = arb("1.03")
    assert child_radius < side
    # No sibling reaches the half-space occupied by the linking rectangle.
    for j in range(1,6):
        assert dot(e,t[0]-t[j]) > child_radius
        assert length(t[j]-p) > child_radius+arb(".96")
    for v in (0, side):
        for w in (-side, side):
            corner = t[0]+v*e+w*d
            assert r*length(corner-p) < arb(".95")
    x = dot(p-t[0],e)
    z = dot(p-t[0],d)
    assert x > arb(".19") and side-x > arb(".19")
    assert side-z > arb(".19") and side+z > arb(".19")
    # These bounds apply to all connecting paths chosen inside the first child.
    assert r**4*(length(t[0]-p)+child_radius) < arb(".11")
    return {"fixed_point_box_in_thousandths":[outward_pair(p[i,0],3) for i in range(3)],
            "sibling_clearance_from_fixed_point_lower":".96",
            "radius_containing_first_image_of_rectangle":".95",
            "distance_from_fixed_point_to_rectangle_boundary_lower":".19",
            "radius_containing_fourth_image_of_entire_first_child":".11",
            "generation_stride":4}


def parameters():
    data = json.loads((PHASES/"fractal_research_07/positive_contact_certificate.json").read_text())
    fc = json.loads((PHASES/"fractal_research_05/dimension_certificate.json").read_text())["family_certificate"]
    r0, u0 = data["reference_r"], data["reference_half_angle_tangent"]
    # Tighten the previously isolated solution. Exact rational bounds enclose h.
    h = 1/arb(2).sqrt()
    places = 68
    from decimal import Decimal, localcontext
    with localcontext() as dc:
        dc.prec = 91
        scaled = (Decimal(1)/Decimal(2).sqrt())*(10**places)
        i = int(scaled)
        h_lo, h_hi = [format(Decimal(k).scaleb(-places),"f") for k in (i,i+1)]
    assert arb(h_lo) < h and h < arb(h_hi)
    cert = contraction_certificate([r0,u0],["1e-45"]*2,h_lo,h_hi)
    assert cert["passed"]
    U = arb(u0)
    reference = (arb(r0,"1.01e-45"),arb(u0,"1.01e-45"),h)
    assert fc["centre"] == [r0,u0]
    ur = arb(fc["radii"][1])
    rlo,rhi = [arb(fmpq(v)) for v in fc["outward_rational_r_bounds"]]
    family = (rlo.union(rhi),(U-ur).union(U+ur),box(*fc["height_interval"]))
    return reference, family


def main():
    if not __debug__:
        raise RuntimeError("Assertions must be enabled.")
    parser=argparse.ArgumentParser()
    parser.add_argument("--write-receipt",action="store_true")
    args=parser.parse_args()
    ctx.prec=256
    reference,family=parameters()
    receipt={"reference_witnesses":check_witnesses(reference,"1e-33",lower="1e-35"),
             "family_witnesses":check_witnesses(family,"0.001"),
             "reference_first_intrusion":first_intrusion(reference,"1404022400020420424","1.325115","1.325120"),
             "family_first_intrusion":first_intrusion(family,"140402240202042042","1.320","1.330"),
             "reference_localization":localize(reference,14),
             "family_localization":localize(family,11),
             "repeated_loops_uniform_premises":repeated_loops(family)}
    output=json.dumps(receipt,indent=2)+"\n"
    if args.write_receipt:
        (ROOT/"certificate.json").write_text(output,encoding="utf-8")
    print(output)


if __name__ == "__main__":
    main()
