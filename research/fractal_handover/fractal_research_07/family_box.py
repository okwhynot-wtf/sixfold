"""Sharper family enclosure, carried forward from the dimension certificate."""
from fractions import Fraction
import mpmath as mp
from certify_witness import interval,bounds,midpoint,magnitude,residual_dual
mp.mp.dps=100
mp.iv.dps=70

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
