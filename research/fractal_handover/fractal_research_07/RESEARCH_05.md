# Connected, with dimension strictly between two and three

17 November 2026, Australia/Sydney.

## The advance

The connected spatial construction now has a computer-assisted **Hausdorff
dimension lower bound above 2**. The bound does not assume that the six main
copies have only point intersections, and it does not assume the open set
condition for the whole fractal.

For the reference member:

\[
\boxed{2.1984 < \dim_H K < 2.4149.}
\]

For **every member** of the previously certified connected curve, parametrised
by height \(h\in[0.7070,0.7072]\):

\[
\boxed{2.1970 < \dim_H K(h) < 2.4150.}
\]

These are conservative, outward rounded inequalities. The exact dimension is
still unknown. The reference upper bound is the familiar similarity-dimension
bound; the lower bound is new to this investigation.

Consequently, these sets have a noninteger Hausdorff dimension, cannot be
contained in a countable union of smooth surfaces, and have zero ordinary
three-dimensional volume. Together with the earlier connectedness proof, this
gives a connected, genuinely spatial, exactly self-similar family with dimension
strictly between that of a smooth surface and that of a solid region.

There are also two geometric exclusions, uniform throughout the connected curve:

- The closed ball of radius **0.398** around the origin is empty of the fractal.
- Opposite first-level copies are separated by a distance greater than **0.4112**.

Units are normalised so the six translation centres have horizontal radius 1.
The central empty ball does not by itself establish a bounded cavity, tunnel,
genus, or any particular complement topology.

This remains a construction within the established theory of similarity IFSs.
Historical originality, the exact dimension, and the complete intersections of
the main copies remain open. The computer-assisted argument and implementation
have not received an independent human review or proof-assistant verification.

## The exact family being studied

This is the same family proved connected in RESEARCH_04.md. For
\(k=0,\ldots,5\), define

\[
\phi_k=k\pi/3,\quad \sigma_k=(-1)^k,\quad
t_k=(\cos\phi_k,\sin\phi_k,\sigma_kh),\quad
a_k=(-\sin\phi_k,\cos\phi_k,0),
\]

\[
G_k(x)=rR_{a_k}(\sigma_k\alpha)x+t_k,\qquad
u=\tan(\alpha/2).
\]

The exact parameters \((r(h),u(h))\) are the uniquely certified roots of the
two contact equations for the periodic word **01153513**, as described in the
previous report. They are not defined by rounding the following display:

    reference h = 1/sqrt(2)
    reference r approximately 0.4761783861615476695
    reference alpha approximately 29.965238257844163 degrees

The attractor satisfies \(K=\bigcup_{k=0}^{5}G_k(K)\). Thus all six pieces are
exactly scaled and rotated copies of the entire infinite set.

The earlier r = 0.47, alpha = 30-degree recipe is a different, still unresolved
target. None of the new statements silently transfers to that exact recipe.

## How a lower bound can survive unknown overlaps

We select a finite collection of eight-letter words from the six maps.
Each word \(w\) defines a similarity \(G_w\) of ratio \(r^8\).
We prove that the **entire sets** \(G_w(K)\), for the selected words, lie in
pairwise disjoint closed balls. Checking distances between point samples alone
would not suffice; each ball includes the infinite tail of the corresponding
copy and all arithmetic uncertainty.

Let E be the attractor of just these selected word maps. Every selected map
takes K into K, so E is a subset of K. Its first-level pieces are disjoint,
giving the strong separation condition. The usual separated-similarity
dimension theorem then yields

\[
\dim_H E=\frac{\log M}{8\log(1/r)}\leq \dim_H K,
\]

where M is the number of selected words. The general upper bound for the
six-map system is

\[
\dim_H K\leq\frac{\log 6}{\log(1/r)}.
\]

The following are the final packings. The diagnostic decimals approximate the
computed lower bound and upper bound; the four-place inequalities above are
rounded conservatively.

| Scope | Selected eight-letter words M | Lower-bound diagnostic | Upper-bound diagnostic |
|---|---:|---:|---:|
| Exact reference member | 464,873 | 2.198479608378964 | 2.414891458627540 |
| Every member of the connected curve | 461,042 | 2.197039553055690 | 2.414943500796544 |

The second row uses **one fixed word list** that works for the entire curve.
The separated subset E is an auxiliary proof device; the object under study
remains the full connected attractor K.

## A tighter enclosure of the connected curve

The earlier interval contraction proof placed the roots in a box of radius
0.001 in r and u. That proves connectedness but is too wide for a useful uniform
packing. Here the same roots are enclosed in the much smaller rectangle

    |r - r0| <= 0.000007
    |u - u0| <= 0.000060
    h in [0.7070, 0.7072],

where r0 and u0 are the stored decimal centres in
positive_contact_certificate.json.

For fixed r and u, the periodic word's linear part is independent of h and
its translation is affine in h. The periodic point, and hence the two contact
residuals F, are therefore affine in h. The new interval evaluation uses

\[
F(x_0,h)=F(x_0,h_0)+F_h(x_0)(h-h_0),\quad h_0=1/\sqrt2.
\]

In the contraction proof for \(x-CF(x,h)\), the constant preconditioner C is
multiplied into the height derivative **before** multiplying the uncertain
height interval. This retains the cancellation between the two equations.
It is an exact algebraic rearrangement, not an estimate of a numerical slope.

The infinity-norm derivative bound is less than **0.014467**. Strict inclusion
margins exceed **5.79e-7** in r and **1.45e-6** in u. Thus a unique root exists
in the narrower rectangle for every height in the interval. The rectangle is
inside the older one, so uniqueness identifies the same connected family.

In particular the exact rational bounds

    0.476171 < r(h) < 0.476186

hold throughout the curve. The proof uses mpmath interval arithmetic at
70 decimal digits and is repeated at 90 digits in the verification script.
Rounded diagnostic endpoints in JSON are never reused as proof inputs.

## Integer geometry and error bounds

Set \(Q=2^{29}=536870912\). Interval arithmetic encloses each reference-map
coefficient over the entire tight reference root box. Every true coefficient
is within 1/Q of its chosen integer-grid coefficient. Both parameter uncertainty
and the exact algebraic height are included.

Starting from the origin, integer centres are generated by

    p_new = floor(A_grid[k] * p / Q) + b_grid[k].

Words are ordered as base-6 integers with the first, outermost map as the most
significant digit. The selected word-index files preserve their complete lists.

The radius-2.5 ball contains K and all exact finite word centres. For the
centre-rounding error e, an induction gives

\[
e_{n+1}\leq .49e_n+13/Q.
\]

Indeed, if e < 1e-6, the approximate centre norm is less than 3; the matrix
coefficient error has operator norm at most 3/Q, and translation and floor
errors each have norm at most sqrt(3)/Q. The local error is therefore at most
(9+2 sqrt(3))/Q < 13/Q. Since

    13 / (Q*(1-.49)) < 0.000001,

every reference integer centre is within **1e-6** in Euclidean distance of the
corresponding true centre, at every depth.

For the entire connected curve, use parameter-difference bounds relative to
the exact reference root:

    delta_r <= 0.0000071
    delta_u <= 0.0000601
    delta_h <= 0.000107.

The rotation axis is fixed for each map, and
\(|\Delta\alpha|\leq 2|\Delta u|\). Hence

\[
\|\Delta A\|\leq\Delta r+2(.49)\Delta u.
\]

The difference between corresponding exact trajectories is bounded by

\[
\frac{2.5(\Delta r+2(.49)\Delta u)+\Delta h}{1-.49}
=\frac{18133}{34000000}<0.000534.
\]

Adding the grid error gives the conservative **0.00055** centre uncertainty
for every member of the curve. These are uniform geometric bounds, not a
sample of a few heights.

The implementation also checks integer overflow bounds. In the centre
recurrence each three-term product sum is below
\(4.5Q^2+9Q<2^{63}\). For squared norms, the component bound gives
\(27Q^2<2^{63}\).

## An empty central ball and a smaller enclosing ball

All 6^8 = **1,679,616** integer centres are enumerated. Their exact integer
squared-norm extrema are:

    minimum = 47337788951927349
    maximum = 1302174424137008133.

First use the original radius-2.5 bound for the remaining infinite tail.
For every family member, each point in K is within

    2.5*(0.476186)^8 + 0.00055

of one of these grid centres divided by Q. Outward interval evaluation gives

    every point's norm > 0.3981010830893302...
    every point's norm < 2.1326768667854346...

Therefore the closed central ball of radius **0.398** is disjoint from K,
and K is contained in the ball of radius **2.14**. The proof of this smaller
enclosing ball comes first; its use in the packing does not assume it is an
invariant ball for all six maps.

## Exact separation of the selected cylinders

For each selected length-eight word, the entire cylinder is contained in a
ball around its grid centre divided by Q, of radius

\[
\rho=2.14\,r_{\rm upper}^8+\varepsilon,
\]

where epsilon is 1e-6 for the reference member and 0.00055 for the whole curve.
Take an integer \(L=\lceil Q\rho\rceil\), and require centre distances in
grid units to exceed \(D=2L+1\).

| Packing | L | D | Exact candidate pairs checked |
|---|---:|---:|---:|
| Reference | 3,037,511 | 6,075,023 | 1,157,354 |
| Whole connected curve | 3,332,642 | 6,665,285 | 1,482,112 |

A floating-point kd-tree is used **only to propose** a word list. A separate
C++ implementation checks the resulting packing with exact integer arithmetic.
It partitions the integer centres into half-open cells of width D, using floor
division also for negative coordinates. A pair at distance at most D must have
cell indices differing by at most one in each coordinate. The checker examines
every pair in all 27 relevant cell combinations, without relying on the kd-tree.

The smallest tested squared distances exceed D^2:

    reference:    36931862827092 > 36905904450529
    whole curve:  44437886217755 > 44426024131225.

Pairs in non-neighbouring cells are already farther than D along at least one
coordinate. For checked pairs, each coordinate difference is less than 2D, so
the sum of three squared differences fits safely in signed 64-bit arithmetic.
Thus every selected pair of enclosing balls is strictly disjoint. This is a
finite certificate for the infinite-cylinder separation required by the lower
dimension theorem.

## What is known about the six large intersections

The periodic-point proof from the previous pass guarantees the six adjacent
contacts. Opposite translations are antipodal. With the new radius bound,
their corresponding first-level pieces have mutual distance at least

\[
2\sqrt{1+(.7070)^2}-2(.476186)(2.14)>0.4112.
\]

Thus the current first-level intersection classification is:

| Unordered pair type, indices modulo 6 | Number of pairs | Certified status |
|---|---:|---|
| Adjacent: index difference 1 or 5 | 6 | Nonempty, with at least the six previously proved points |
| Two positions apart: difference 2 or 4 | 6 | Unresolved |
| Opposite: difference 3 | 3 | Disjoint, with a uniform positive gap |

There is no claim that an adjacent intersection is a singleton. In particular,
the six highlighted points in the earlier image must not be mistaken for a
complete classification of the intersections. Finite close approaches between
point samples do not settle the unresolved pairs.

## Verification and reproduction

The saved verification checks include:

- Reproducing the tight reference contact certificate before packing.
- Recomputing all **925,915 selected word centres** directly from their base-6
  words, using a different traversal from the complete-level enumeration.
- Rechecking 600 selected words with scalar Python arbitrary-precision integers.
- Reproducing both full exact pair checks.
- Comparing the C++ checker against exhaustive brute-force distances on 164
  small examples, including negative coordinates, equal-distance boundaries,
  duplicate points, and both valid and invalid packings; rejecting truncated
  input as well.
- Recomputing the full radial enclosure and rechecking both extremal words
  with scalar Python integers.
- Repeating the sharper family interval proof at 90 decimal digits.
- Checking the affine height dependence with an independent 100-digit matrix
  exponential implementation; the residual was below 1.54e-101.

These are separate implementation checks by the same investigator, not an
independent mathematical review. The argument is computer-assisted, with the
standard interval-arithmetic and integer-computation assumptions described above.

On a little-endian system with Python 3, the packages in requirements.txt, and
a C++17 compiler available as g++:

    python certify_dimension.py
    python verify_dimension.py
    python render_dimension.py

The first command compiles the exact checker, redoes the proofs, generates the
two deterministic greedy packings, and writes their certificates and word lists.
The second recomputes the independent checks. The third makes the finite
coloured rendering. No network access is required after installing dependencies.

The selected word lists and raw integer coordinates are included, so the pair
check can also be compiled and run on the supplied certificate data directly:

    g++ -O3 -std=c++17 verify_packing.cpp -o verify_packing
    ./verify_packing reference_centres.i64 6075023
    ./verify_packing whole_family_centres.i64 6665285

For the earlier contact proof, certify_witness.py and verify_positive_contact.py
are included, with the original numerical search seeds and RESEARCH_04.md.
Its older rendering script is not needed to reproduce this pass.

## Next research question

The immediate mathematical target is a complete intersection analysis or a
proof of the open set condition. If that condition holds for the full six-map
system, its dimension equals the similarity value, approximately 2.41489146 at
the reference member. The present result gives a substantial lower bound
without presuming that conclusion.

A focused comparison with known rotated spatial IFS constructions is still
needed before making a historical novelty claim. The face-assembly/polyhedron
diversion remains sidelined.

## Primary background

- John E. Hutchinson, *Fractals and Self Similarity* (1981), especially Sections
  3.1 and 5.2–5.3, for contraction attractors and the separated-similarity
  dimension theorem:
  https://maths-people.anu.edu.au/~john/Assets/Research%20Papers/fractals_self-similarity.pdf
- Ábel Farkas, *Dimension approximation of attractors of graph directed IFSs by
  self-similar sets* (2015), for the established use of separated subsystems in
  dimension approximation. Our concrete lower bound uses only the explicitly
  selected and verified subsystem above:
  https://arxiv.org/abs/1505.05746
