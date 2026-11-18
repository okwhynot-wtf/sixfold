"""Reconstruct and certify the rational-tilt member using the phase-04 word."""
from pathlib import Path
import json

import mpmath as mp
import sympy as sp


R = sp.Symbol("r")
U = sp.Rational(19, 71)
WORD = (0, 1, 1, 5, 3, 5, 1, 3)
ROOT = Path(__file__).resolve().parent


def rotations(u):
    # Coordinates are (x, sqrt(3)*y, z). The conjugating rotation is -120 degrees.
    half = sp.Rational(1, 2)
    turn = sp.Matrix([[-half, half, 0], [-3*half, -half, 0], [0, 0, 1]])
    c, s = (1-u*u)/(1+u*u), 2*u/(1+u*u)
    first = sp.Matrix([[c, 0, s], [0, 1, 0], [-s, 0, c]])
    return [turn**i * first * turn**(-i) for i in range(3)]


def contact_columns():
    # A fixed point on the contact axis is lambda*(1,1,0).
    # Its fixed-point equation has the form L*lambda = flat + vertical*h.
    half = sp.Rational(1, 2)
    xy = [(1, 0), (half, 3*half), (-half, 3*half)]
    rotation = rotations(U)
    product = sp.eye(3)
    flat, vertical = sp.zeros(3, 1), sp.zeros(3, 1)
    for depth, k in enumerate(WORD):
        x, y = xy[k % 3]
        sign = 1 if k < 3 else -1
        flat += R**depth * product * sp.Matrix([sign*x, sign*y, 0])
        vertical += R**depth * product * sp.Matrix([0, 0, (-1)**k])
        product = product * rotation[k % 3]
    axis = sp.Matrix([1, 1, 0])
    return axis - R**len(WORD) * product * axis, flat, vertical


def polynomial_interval(poly, lo, hi):
    """Exact rational interval Horner evaluation."""
    lower = upper = sp.S.Zero
    for coeff in sp.Poly(poly, R).all_coeffs():
        limits = (lower*lo, lower*hi, upper*lo, upper*hi)
        lower, upper = min(limits) + coeff, max(limits) + coeff
    return lower, upper


def quotient_interval(numerator, denominator, lo, hi):
    a, b = polynomial_interval(numerator, lo, hi)
    c, d = polynomial_interval(denominator, lo, hi)
    assert c*d > 0
    quotients = (a/c, a/d, b/c, b/d)
    return min(quotients), max(quotients)


def certify_contact():
    axis, flat, vertical = contact_columns()
    determinant = sp.Poly(axis.dot(flat.cross(vertical)), R)
    primitive = determinant.clear_denoms(convert=True)[1].primitive()[1]
    # This strict subinterval of the phase-04 uniqueness box includes the
    # whole phase-05 scale range. Isolate with rational endpoints.
    brackets = primitive.intervals(inf=sp.Rational("0.476171"),
                                   sup=sp.Rational("0.476186"),
                                   eps=sp.Rational(1, 10**32))
    assert len(brackets) == 1
    (lo, hi), multiplicity = brackets[0]
    assert lo < hi and multiplicity == 1 and primitive.eval(lo)*primitive.eval(hi) < 0
    # Cramer's rule on coordinates X,Z. The determinant enforces the Y row.
    hnum = axis[0]*flat[2] - axis[2]*flat[0]
    hden = axis[2]*vertical[0] - axis[0]*vertical[2]
    hlo, hhi = quotient_interval(hnum, hden, lo, hi)
    assert sp.Rational("0.7070") < hlo <= hhi < sp.Rational("0.7072")
    assert sp.Rational("0.267564") < U < sp.Rational("0.267684")
    return primitive, (lo, hi), (hlo, hhi)


def reduced_rotation_check():
    # Deliberately clear the denominator BEFORE reduction. In these coordinates
    # every entry has denominator invertible modulo 37 after this scaling.
    prime = 37
    norm = 71**2 + 19**2
    assert norm % prime == 0

    def reduce_entry(value):
        p, q = sp.fraction(value)
        return (int(p) * pow(int(q), -1, prime)) % prime

    matrices = [(norm*q).applyfunc(reduce_entry) for q in rotations(U)]
    lines = []
    for matrix in matrices:
        assert matrix != sp.zeros(3)
        assert matrix.adjugate().applyfunc(lambda v: v % prime) == sp.zeros(3)
        col = next(c for c in matrix.columnspace() if any(c))
        pivot = next(int(v) for v in col if v)
        line = tuple(int(v)*pow(pivot, -1, prime) % prime for v in col)
        lines.append(line)
    assert len(set(lines)) == 3
    for left in matrices:
        for right in matrices:
            assert (left*right).applyfunc(lambda v: v % prime) != sp.zeros(3)
    return lines, matrices


def main():
    if not __debug__:
        raise RuntimeError("Assertions must be enabled")
    polynomial, (rlo, rhi), (hlo, hhi) = certify_contact()
    lines, matrices = reduced_rotation_check()
    mp.iv.dps = 65
    def iv_rational(value):
        return mp.iv.mpf(str(value.p)) / mp.iv.mpf(str(value.q))
    ratio = mp.iv.mpf([iv_rational(rlo).a, iv_rational(rhi).b])
    dimension = mp.iv.log(6) / mp.iv.log(1/ratio)
    print("u =", U)
    print("degree of contact determinant =", polynomial.degree())
    print("r bracket (exact) =", (rlo, rhi))
    print("r ~", ((rlo+rhi)/2).evalf(24))
    print("h ~", ((hlo+hhi)/2).evalf(24))
    print("h bracket width <", float(hhi-hlo)*1.00001)
    print("Hausdorff dimension interval =", dimension)
    print("Image lines modulo 37 =", lines)
    for matrix in matrices:
        print(matrix.tolist())
    # Compare the word convention with the archived certificate.
    handover = ROOT.parent / "fractal_handover/fractal_research_07"
    data = json.loads((handover / "positive_contact_certificate.json").read_text())
    assert list(WORD) == data["word"]
    print("All contact and finite-field checks passed.")


if __name__ == "__main__":
    main()
