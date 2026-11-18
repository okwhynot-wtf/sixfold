"""Exact elimination and a complex disk certificate for the handover reference."""
from fractions import Fraction
from math import prod
import argparse
import json

import sympy as sp
from flint import arb, ctx, fmpz_mpoly_ctx, fmpz_poly, nmod_poly

from verify_member import ROOT, WORD, rotations


def check_rotation_representation():
    """Check the coordinate change and the projective lift against Rodrigues."""
    u = sp.Symbol("u")
    i = sp.I
    pauli = (sp.Matrix([[0, 1], [1, 0]]), sp.Matrix([[0, -i], [i, 0]]),
             sp.diag(1, -1))
    change = sp.diag(1, sp.sqrt(3), 1)
    scaled = rotations(u)
    for k in range(6):
        azimuth = k*sp.pi/3
        a = (-1)**k * sp.Matrix([-sp.sin(azimuth), sp.cos(azimuth), 0])
        x, y, z = a
        cross = sp.Matrix([[0, -z, y], [z, 0, -x], [-y, x, 0]])
        numerator = (1-u*u)*sp.eye(3) + 2*u*u*(a*a.T) + 2*u*cross
        assert (change*numerator*change.inv() -
                (1+u*u)*scaled[k%3]).applyfunc(sp.cancel) == sp.zeros(3)
        # L sigma(v) adj(L) = sigma(((1+u^2)Q)v).
        axis_matrix = sum((a[j]*pauli[j] for j in range(3)), sp.zeros(2))
        lift = sp.eye(2) - i*u*axis_matrix
        for j in range(3):
            right = sum((numerator[l,j]*pauli[l] for l in range(3)), sp.zeros(2))
            assert (lift*pauli[j]*lift.adjugate() - right).applyfunc(sp.expand) == sp.zeros(2)


def elimination():
    ring = fmpz_mpoly_ctx.get(("r", "u"))
    r, u = ring.gens()
    symbolic_u = sp.Symbol("u")
    denominator = 2*(1+u*u)

    def clear_entry(entry):
        cleared = sp.cancel(2*(1+symbolic_u**2)*entry)
        poly = sp.Poly(cleared, symbolic_u, domain=sp.ZZ)
        return sum(int(c)*u**n for (n,), c in poly.terms())

    numerators = [[[clear_entry(m[i,j]) for j in range(3)] for i in range(3)]
                  for m in rotations(symbolic_u)]
    horizontal_twice = [(2, 0), (1, 3), (-1, 3), (-2, 0), (-1, -3), (1, -3)]
    axis = [1, 1, 0]
    a, b, d = axis[:], [0, 0, 0], [0, 0, 0]
    for depth, k in enumerate(reversed(WORD), 1):
        m = numerators[k%3]
        def step(v):
            return [r*sum(x*y for x, y in zip(row, v)) for row in m]
        a, b, d = step(a), step(b), step(d)
        for j in range(2):
            b[j] += denominator**depth * horizontal_twice[k][j]
        d[2] += denominator**depth * 2*(-1)**k
    a = [denominator**len(WORD)*x - y for x, y in zip(axis, a)]
    # At a contact, 2*lambda*a = b + h*d. At the reference, 2*h^2=1.
    def cross(x, y):
        return [x[(j+1)%3]*y[(j+2)%3] - x[(j+2)%3]*y[(j+1)%3]
                for j in range(3)]
    determinant = sum(x*y for x, y in zip(a, cross(b, d)))
    height_equation = 2*cross(a, b)[1]**2 - cross(a, d)[1]**2
    # All discarded factors are constants or powers of the strictly positive 1+u^2.
    def strip(poly, power):
        cofactor, remainder = divmod(poly, (1+u*u)**power)
        assert not remainder
        return cofactor // cofactor.content()
    p, e = strip(determinant, 17), strip(height_equation, 16)
    assert tuple(p.degrees()) == (22, 14) and tuple(e.degrees()) == (30, 32)
    result = p.resultant(e, "r")
    assert result and result.degrees()[0] == 0
    coefficients = result.to_dict()
    return fmpz_poly([coefficients.get((0, n), 0) for n in range(result.degrees()[1]+1)])


def reference_factor(result, contact):
    ctx.prec = 512
    box = contact["tight_root_certificate"]
    assert box["passed"] and box["centre"][1] == contact["reference_half_angle_tangent"]
    assert Fraction(box["radius"][1]) == Fraction(1, 10**25)
    # A slight outward enlargement also includes rounding of the displayed centre.
    u = arb(box["centre"][1], "1.001e-25")
    content, factors = result.factor()
    assert content * prod(f**e for f, e in factors) == result
    candidates = []
    for f, exponent in factors:
        value = arb(0)
        for c in reversed(f.coeffs()):
            value = value*u + c
        if value.contains(0):
            candidates.append(f)
    assert len(candidates) == 1 and candidates[0].degree() == 432
    return candidates[0], sorted((f.degree(), e) for f, e in factors)


def verify_irreducible_degrees(f):
    """Independently exclude every proper rational factor degree."""
    possible = set(range(f.degree()+1))
    for prime in (7, 13, 37, 43):
        poly = nmod_poly(f.coeffs(), prime)
        assert poly.degree() == f.degree() and poly.gcd(poly.derivative()).degree() == 0
        x = nmod_poly([0, 1], prime)
        power, remaining = x, poly
        degrees = []
        for d in range(1, poly.degree()+1):
            power = power.pow_mod(prime, poly)
            # X^(p^d)-X contains exactly the monic irreducibles with degree dividing d.
            block = remaining.gcd(power-x)
            assert block.degree() % d == 0
            degrees.extend([d] * (block.degree()//d))
            remaining = remaining // block
            if remaining.degree() == 0:
                break
        assert sum(degrees) == f.degree()
        subsums = {0}
        for d in degrees:
            subsums |= {k+d for k in subsums}
        possible &= subsums
        print("Factor degrees mod", prime, "=", degrees)
    assert possible == {0, f.degree()}


def conjugate_disk(poly):
    """Prove exactly one root in a disk by Rouche, using Gaussian integers."""
    n = 10**12
    x, y, radius = -28547283375, 1138685386817, 100
    # Coefficients of n^degree f((x+i*y+radius*w)/n), low degree first.
    coeffs = [(int(poly.leading_coefficient()), 0)]
    scale = 1
    for coefficient in reversed(poly.coeffs()[:-1]):
        scale *= n
        shifted = [(0, 0)]*(len(coeffs)+1)
        for j, (a, b) in enumerate(coeffs):
            real, imag = shifted[j]
            shifted[j] = (real+x*a-y*b, imag+y*a+x*b)
            shifted[j+1] = (radius*a, radius*b)
        real, imag = shifted[0]
        shifted[0] = (real+int(coefficient)*scale, imag)
        coeffs = shifted
    linear_lower = max(map(abs, coeffs[1]))
    others_upper = sum(abs(a)+abs(b) for j,(a,b) in enumerate(coeffs) if j != 1)
    assert 100*others_upper < linear_lower
    # Bound |1+i*z| / |1-i*z| throughout the disk by enlarging it to a square.
    num = (abs(x)+radius)**2 + (abs(n-y)+radius)**2
    den = (n+y-radius)**2
    assert y-radius > 0 and num*1000**2 < den*67**2
    # 67/1000 < 7/100 < 7-4*sqrt(3) = tan(pi/12)^2.
    assert (Fraction(7) - Fraction(7, 100))**2 > 16*3
    return (x, y, radius, n)


def main():
    if not __debug__:
        raise RuntimeError("Assertions must be enabled")
    parser = argparse.ArgumentParser()
    parser.add_argument("--export-polynomial", action="store_true")
    args = parser.parse_args()
    contact = json.loads((ROOT.parent / "fractal_handover/fractal_research_07/"
                          "positive_contact_certificate.json").read_text())
    assert list(WORD) == contact["word"]
    check_rotation_representation()
    result = elimination()
    f, degrees = reference_factor(result, contact)
    verify_irreducible_degrees(f)
    disk = conjugate_disk(f)
    payload = {"variable": "u = tan(alpha/2)", "degree": f.degree(),
               "coefficients_in_ascending_order": [int(c) for c in f.coeffs()]}
    saved = ROOT / "reference_tilt_polynomial.json"
    if args.export_polynomial:
        saved.write_text(json.dumps(payload, indent=2)+"\n", encoding="utf-8")
    if saved.exists():
        assert json.loads(saved.read_text(encoding="utf-8")) == payload
    print("Resultant degree =", result.degree())
    print("Irreducible factors (degree, multiplicity) =", degrees)
    print("Unique factor compatible with the contact box has degree", f.degree())
    print("Certified disk (x, y, radius, denominator) =", disk)
    print("Rouche remainder/linear lower bound < 0.01.")
    print("Projective eigenvalue modulus ratio < 0.067 < tan(15 degrees)^2.")
    ctx.prec = 160
    assert contact["tight_root_certificate"]["centre"][0] == contact["reference_r"]
    assert Fraction(contact["tight_root_certificate"]["radius"][0]) == Fraction(1, 10**25)
    r = arb(contact["reference_r"], "1.001e-25")
    print("Reference dimension enclosure =", arb(6).log() / (1/r).log())
    print("All reference checks passed.")


if __name__ == "__main__":
    main()
