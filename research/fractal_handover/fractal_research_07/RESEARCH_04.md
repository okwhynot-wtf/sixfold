# A certified connected spatial family

17 November 2026, Australia/Sydney.

## Result

There is now a computer-assisted proof of actual contacts and global connectedness
for a small continuous family of genuinely spatial, exactly self-similar sets.
The face-assembly branch was not pursued in this pass.

A reference member has approximately

    scale r = 0.4761783861615476695,
    tilt alpha = 29.965238257844163 degrees,
    additional turn theta = 0,
    alternating centre height h = 1/sqrt(2).

The proof concerns exact parameters defined by a unique root of two equations,
not the truncated displayed decimals. These slightly adjust the earlier 0.47,
30-degree target. The original exact 0.47/30-degree recipe remains unresolved.

The same contact argument is certified for every h in [0.7070,0.7072], with a
corresponding uniquely specified scale and tilt. This is a one-parameter curve
of connected recipes, not a claim that every nearby scale/tilt combination is
connected.

This establishes a construction and its connectedness. It does not establish
historical originality, the open set condition, or an exact Hausdorff dimension.
The derivation and reproducible interval calculations have not received an
independent mathematical review or a proof-assistant formalization.

## The six similarities

For k = 0,...,5, put

    phi_k = k*pi/3,
    sigma_k = (-1)^k,
    t_k = (cos(phi_k), sin(phi_k), sigma_k*h),
    a_k = (-sin(phi_k), cos(phi_k), 0),
    G_k(x) = r R_(a_k)(sigma_k*alpha) x + t_k.

The same six similarities repeat at every depth. Their unique nonempty compact
attractor K satisfies K = union_k G_k(K). All copies shrink equally in all
directions, by r. Whole-object self-similarity therefore continues indefinitely.

For reliable parameter arithmetic, the tilt is represented by

    u = tan(alpha/2),
    cos(alpha) = (1-u^2)/(1+u^2),
    sin(alpha) = 2u/(1+u^2).

Apart from the fixed algebraic constants sqrt(2) and sqrt(3), the map coefficients
are rational functions of r, u and h. The interval proof does not have to evaluate
an uncertain tilt through trigonometric functions.

## A contact witness with two repeating addresses

Let W be the eight-map word

    W = 0 1 1 5 3 5 1 3.

Let G_W mean the composition G_0 o G_1 o G_1 o G_5 o G_3 o G_5 o G_1 o G_3.
Writing G_W(x) = M_W x + c_W, its unique fixed point is

    p_W = (I-M_W)^(-1) c_W.

It belongs to K, since iterating this word on any point of K converges to p_W.
Its address is W repeated forever; in particular p_W belongs to G_0(K).

Consider the half-turn about the horizontal axis at azimuth 30 degrees:

    S = [[1/2, sqrt(3)/2, 0],
         [sqrt(3)/2, -1/2, 0],
         [0, 0, -1]].

The map recipe has the exact symmetry

    S G_k S^(-1) = G_((1-k) mod 6).

The partner of W under this permutation is

    W' = 1 0 0 2 4 2 0 4.

The point p_W lies on the fixed axis of S exactly when

    F_1(r,u,h) = -p_W,x/2 + sqrt(3)*p_W,y/2 = 0,
    F_2(r,u,h) = p_W,z = 0.

If these two equations hold, S p_W = p_W. Symmetry says S p_W is the fixed point
of G_(W'), so the two repeating addresses describe the SAME point. Because W'
begins with 1, this gives

    p_W in G_0(K) intersection G_1(K).

This is an actual shared point of the infinite sets. It is not a small distance
between finite point approximations.

Numerically, the reference shared point is approximately

    (1.15976670328374, 0.66959161833803, 0).

The exact point has y = x/sqrt(3) and z = 0. The source contains its two addresses
and the equations that define the exact reference parameters.

## Interval existence proof

The numerical search first found a nearby zero. It was then refined at high
precision and certified independently of the numerical root solver's success
flag.

The reference parameter centres are

    r_0 = 0.476178386161547669525964558546828831852499529292214482,
    u_0 = 0.26762408562357600423627570346398616... .

The full stored decimal for u_0 is in positive_contact_certificate.json. These
decimal centres specify the proof boxes, not the exact roots themselves.

The program encloses F and its Jacobian using interval arithmetic at 70 decimal
digits. A two-variable interval automatic-differentiation implementation
propagates derivatives through the rational rotation formula, word composition,
and Cramer's-rule fixed-point calculation.

For a fixed height h, let

    T_h(x) = x - C F(x,h),  x = (r,u),

where C is a constant, decimal-rational approximation to the inverse Jacobian at
the reference point. For a parameter rectangle X centred at x_0, the program
encloses T_h(X) by

    x_0 - C F(x_0,h) + (I-C J(X,h)) (X-x_0).

It checks both strict inclusion of this enclosure in X and an infinity-norm
bound less than 1 on I-C J. Thus T_h is a contraction mapping X into itself.
Its unique fixed point exists by the contraction theorem and is a true zero of
F, since the same norm bound implies C is nonsingular.

### Tight reference root

For h = 1/sqrt(2), a box of radius 10^-25 in both r and u passes. The derivative
norm bound is less than 3.56e-23, and both strict inclusion margins exceed
9.99e-26. A tiny height interval containing the exact 1/sqrt(2) value is used, so
uncertainty in that algebraic constant is included in the computation.

### A continuous family, not just one root

For all h in the exact interval [0.7070,0.7072], the same calculation passes with

    X = [r_0-.001,r_0+.001] x [u_0-.001,u_0+.001].

The derivative norm upper bound is

    0.3572139415750810069... < 1.

The strict inclusion margins are greater than 0.00087917 in r and 0.00047915
in u. This proves a unique solution (r(h),u(h)) in X for EVERY height in the
interval. Uniform contraction gives continuous dependence on h. The Jacobian
is nonsingular throughout the proof box, so the implicit-function theorem also
gives analytic dependence in the interior.

The following are high-precision numerical samples of that certified curve.
The theorem is the interval argument for the whole height interval, not these
three samples alone:

| Height h | Approximate scale r(h) | Approximate tilt alpha(h) |
|---:|---:|---:|
| 0.7070 | 0.476172040082395 | 29.9714516588684 degrees |
| 0.7071 | 0.476177983208064 | 29.9656327567914 degrees |
| 0.7072 | 0.476183924650234 | 29.9598163857705 degrees |

The larger boxes that did not satisfy the interval contraction test are retained
in the diagnostic JSON. A failed test is inconclusive, not evidence that a root
or a connected family does not exist there.

## Why one shared point connects all six pieces

The recipe also has a roto-reflection symmetry

    T = [[1/2, -sqrt(3)/2, 0],
         [sqrt(3)/2, 1/2, 0],
         [0, 0, -1]],

with T G_k T^(-1) = G_((k+1) mod 6). Applying T repeatedly to the shared point
therefore gives contacts between

    (0,1), (1,2), (2,3), (3,4), (4,5), (5,0).

These form a connected six-cycle in the first-level intersection graph.

A self-contained connectedness argument uses the invariant ball B of radius
2.5. In the proof box r < .49 and h < .71, so ||t_k|| < 1.25 and G_k(B) is
contained in B. Let B_n be the union of all images of B under words of length n.
Then B_n is a nested sequence of nonempty compact sets with intersection K.

B_0 is connected. If B_n is connected, each G_k(B_n) is connected and contains
G_k(K). The six certified contacts therefore also connect these six larger
sets, proving B_(n+1) connected. By induction every B_n is connected, and their
nested intersection K is connected.

This proof does not assume connectedness in order to obtain the contact points.
Their membership in K comes from the periodic-word contraction first.

The proof guarantees at least these six shared points. It does NOT assert that
each pair intersects at only one point, that other intersections are absent, or
that the set has no holes or cut points.

## Why the family is genuinely spatial

For map 0, write a = 1-r*cos(alpha) and b = r*sin(alpha). Its fixed point has

    x = (a+b*h)/(a^2+b^2), y = 0,
    z = (a*h-b)/(a^2+b^2).

The interval checks give x > 1.8646 and z > 0.4333 throughout the proof box.
The three even-indexed fixed points are related by 120-degree rotations and
form a nondegenerate horizontal triangle at positive z. The opposite fixed
point is at negative z. These four points are not coplanar and all belong to K.
Thus this is not a planar attractor viewed at an angle.

## Verification and scope

The verification script independently checks:

- 24 matrix/translation conjugacy identities symbolically for arbitrary u and h;
- orthogonality and determinant +1 for all six local rotation matrices;
- equivalence of the two residual equations to S p = p;
- the two periodic fixed points using 100-digit matrix exponentials instead of
  the rational Rodrigues rotation formula used in the certificate;
- the automatic derivatives against high-precision central differences of that
  independent geometry calculation;
- the interval contraction certificate again at 90 decimal digits.

The two independently computed periodic points differed by less than 3.28e-57.
The derivative comparison differed by less than 9.17e-46. These numerical checks
support the implementation; existence of an exact contact follows from the
interval contraction proof, not from either tiny residual alone.

The standard contraction-IFS existence framework is established mathematics.
Intersection graphs and contact conditions are established research tools as
well. Historical originality of this particular periodic matching recipe and
its resulting family still needs a focused literature comparison.

## What remains open

1. The exact earlier recipe r = .47, alpha = 30 degrees has not been decided.
2. The complete pattern and size of the intersections are not classified.
3. The open set condition has not been proved. The reference similarity dimension
   log(6)/log(1/r), about 2.41489146, is an UPPER BOUND for Hausdorff dimension,
   not an established equality here.
4. No novelty claim is established, and this is not a claim that all nine earlier
   unresolved cases are connected.

The useful next step is to study the actual overlaps and possible dimension
drop in this now-certified connected family, then compare that precise structure
with known connected IFS constructions.

## Figure and reproduction

connected_contacts.png is a finite word-centre rendering at approximate reference
parameters. Gold markers annotate the six proven shared points; the dots and
pixel footprints themselves are not evidence of connectivity.

With Python 3 and the versions in requirements.txt:

    python certify_witness.py
    python verify_positive_contact.py
    python render_connected.py

The saved numerical_witnesses.json supplies the search seed, so the expensive
search need not be rerun. To reproduce that search separately:

    python search_witness.py

All source and numerical data are included. The code runs offline once the
dependencies are installed. The geometry helpers were carried forward from the
earlier investigation; their main entry points are not required for these steps.

## Primary background sources

- John E. Hutchinson, *Fractals and Self Similarity* (1981): contraction IFS
  attractors and self-similar-set dimension theory.
  https://maths-people.anu.edu.au/~john/Assets/Research%20Papers/fractals_self-similarity.pdf
- Andrei Tetenov, Ivan Yudin and Makhliyo Kadirova, *Finiteness properties for
  self-similar continua* (2025): related intersection-graph and finite-intersection
  methods. Its additional hypotheses have not been established for our family.
  https://www.aimsciences.org/article/doi/10.3934/dcdss.2025057
