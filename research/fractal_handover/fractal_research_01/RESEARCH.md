# Six copies with alternating turns: first investigation

Date: 17 November 2026 (Australia/Sydney).

## What we have established

This is a reproducible first experiment, not an established new family. We specify
an exactly self-similar two-parameter family, screen 1,023 parameter pairs, and
derive two useful contact results analytically. The numerical scan alone does not
prove connectedness. No claim of originality is made for the family or the results.

The particularly useful slice has a 30-degree turn. Its first contact occurs at

    r_c = (sqrt(15) - sqrt(3))/6 = 0.356822089773090...

For 0 < r < r_c on that slice, the six first-level pieces are separated. At r_c
the attractor is connected. Each adjacent pair meets along a Cantor set rather
than at a single point. These statements follow from the derivation below, rather
than from apparent contacts in the pictures. The derivation has numerical checks
but has not received independent mathematical review.

## Exact definition

Identify the plane with the complex numbers. For i = 0,...,5, let

    d_i = exp(i*pi*i/3),
    s_i = (-1)^i,
    f_i(z) = r * exp(i*s_i*theta) * z + d_i.

Here the first i in exp(i*...) is the imaginary unit; the index i labels the six
maps. Equivalently, in real coordinates the map is r R_(s_i theta) x plus the
unit vector at angle 60i degrees. We use 0 < r < 1. A single fixed list of six
similarities repeats at every level; the map list does not change with depth.
The unique nonempty compact set K satisfies K = union_i f_i(K).

Consequently, the infinite set is exactly self-similar. Every image under a word
of n maps is a copy of K of size r^n. Finite plots are only approximations.

The quantity log(6)/log(1/r) is the similarity dimension. It equals Hausdorff
dimension under the open set condition, not automatically in an overlapping case.
The scan records it as similarity dimension, not as a measured Hausdorff dimension.

## Search completed

- Shrinkage r: 33 values from 0.315 to 0.395 in steps of 0.0025.
- Turn theta: 31 values from 0 to 60 degrees in steps of 2 degrees.
- Total: 1,023 parameter pairs.
- First screening: depth-3 centre sets inside each of the six first-level pieces.
- Ten selected cases were examined again at depth 5.
- Gallery: all 6^7 = 279,936 finite word centres per panel, without random sampling.

The coarse screen excluded connectedness for 352 cases numerically. The other
671 remain unresolved by that screen; they are not 671 verified connected sets.
Floating-point error was not interval-certified. The analytic results in the next
sections are separate from these screening counts.

### What the screen actually tests

All of K lies in the ball of radius R = 1/(1-r). A depth-n word centre f_w(0)
represents a set contained in a disc of radius r^n R. The screen covers each
first-level piece using centres of total depth n+1 and discs of radius r^(n+1) R.

For each pair of first-level pieces, it finds the minimum distance between their
finite centres. Subtracting twice the tail radius gives a lower bound in exact
arithmetic. A positive result excludes intersection. It then builds the graph
of pairs whose disc covers might intersect. A disconnected outer graph excludes
connectedness; a connected outer graph does not establish it.

## Analytic result A: one-third scale

At r = 1/3 and theta = 0, K is the familiar six-piece hexagonal construction.
Its six pieces meet in a cycle, at one point per adjacent pair. It is connected.

For any 0 < theta < 60 degrees, still with r = 1/3, all six first-level pieces
are strictly separated. The attractor is then a Cantor set topologically.

Proof of separation: put delta = min(theta, 60 degrees - theta), so delta > 0.
The norm of every two-letter centre is at most

    M_2 = sqrt(1 + r^2 + 2*r*cos(delta)) < 1+r.

An arbitrary tail contributes at most r^2 R. Therefore every point of K has norm
at most rho = M_2 + r^2 R < R. The six first-level pieces lie in discs centred
at d_i of radius r*rho < r*R = 1/2. Distinct centres are at least distance 1
apart, so those discs, and hence the pieces, are separated. Repeating this
separation at all depths gives the Cantor-set coding.

For the unrotated case, write H for the convex hull of the six unit vectors.
K lies in (3/2)H. Its first-level hulls are d_i + (1/2)H. Adjacent pieces contain
their common midpoint: the required preimage is one of the six fixed points
(3/2)d_j. These contacts form a six-cycle. Starting from (3/2)H, every finite
outer approximation is connected; their nested intersection K is connected.
The hull interiors of the pieces are disjoint, so the open set condition holds.

In both cases the Hausdorff dimension is exactly log(6)/log(3), about 1.630930.
Thus turning the pieces can change connectivity without changing dimension.

## Analytic result B: first contact at 30 degrees

### Reduction to one common rotation

Consider the IFS g_i(z) = a*z + d_i with a = r*exp(i*pi/6), so all six turns
are +30 degrees. Its attractor A is invariant under rotation by 60 degrees,
because the digit set has that symmetry and complex multiplication commutes
with rotation. Since the -30-degree map differs from the +30-degree map by a
60-degree rotation of its input, their images of A are identical. Thus A is
also the attractor of the alternating-turn IFS at theta = 30 degrees.

A is also invariant under complex conjugation: conjugating a gives a multiplied
by a -60-degree rotation, which acts trivially on A as a set. In particular A
has the reflection and rotation symmetries of a regular hexagon.

### Convex hull and exclusion of earlier contact

Every point of A is a convergent digit expansion sum_(n>=0) a^n d_(j_n).
The convex hull C therefore is the Minkowski sum of r^n R_(30n degrees) H.
Since H is invariant under 60-degree rotation,

    C = (H + r R_(30 degrees) H)/(1-r^2).

Its support height in the positive imaginary direction is

    h = (sqrt(3)/2 + r)/(1-r^2).

Two neighbouring digit centres are distance 1 apart, along a direction obtained
by rotating that imaginary direction by 30 degrees. Each first-level hull has
support radius r*h in that direction. Adjacent hulls are separated whenever

    2*r*h < 1,

equivalently 3*r^2 + sqrt(3)*r - 1 < 0. Equality has positive root r_c above.
Non-adjacent centres are distance at least sqrt(3); for r <= r_c their enclosing
disc radii sum to 2*r/(1-r) < sqrt(3), so they remain separated as well.

### Actual contact, not just touching hulls

Points of A on its upper support line have precisely the form

    t + i*h,   t in T,
    T = { (1/2) sum_(m>=0) epsilon_m*r^(2m) : epsilon_m in {-1,+1} }.

To see this, at each even digit position the two upper hexagon vertices tie for
the maximum vertical projection, contributing a horizontal choice +/-r^(2m)/2.
At each odd position there is one topmost vertex, contributing no horizontal
choice. These are independent digit choices. The matching lower support points
t-i*h also belong to A by reflection symmetry.

At r = r_c, put w = exp(i*pi/3). Since w-1 = exp(i*2*pi/3) and 2*r*h = 1,

    1 + a*(t+i*h) = w + a*(t-i*h)

for every t in T. These are genuine points shared by pieces 0 and 1.
Rotation gives a full cycle of contacts. Therefore the nested connected outer
approximations have a connected intersection: A itself is connected.

The support-line description also proves that an adjacent intersection is
exactly a translated, rotated and scaled copy of T. Since r_c^2 < 1/2, T is a
separated two-map Cantor set. Its dimension is

    log(2)/log(1/r_c^2) = 0.336310089268886...

The six first-level hull interiors are disjoint, giving the open set condition.
Thus the dimension of the whole attractor at first contact is

    log(6)/log(1/r_c) = 1.738697938748511...

No general statement about connectedness for r > r_c is established here.

## What to investigate next

1. Map which contacts survive for angles between 0 and 30 degrees, especially
   angles not rational multiples of a full turn. These are the less understood
   parts of this particular experiment.
2. Replace centre-disc screens with nested convex-polygon or interval-certified
   covers, using the analytic 0-degree and 30-degree slices as validation cases.
3. Search for parameter subfamilies with provable contacts and distinctive contact
   sets. Do not select solely for a visually different appearance.
4. Compare the resulting recipes with existing rotated hexagonal IFS constructions
   before attaching an originality claim. Generic changed parameters alone do not
   establish a substantially new family.

## Preliminary literature context

The broad framework and the strategy are established. The following sources are
relevant starting points; this is not an exhaustive novelty search.

- John E. Hutchinson, *Fractals and Self Similarity* (1981): existence and uniqueness
  for contraction IFSs, and dimension under the open set condition.
  https://maths-people.anu.edu.au/~john/Assets/Research%20Papers/fractals_self-similarity.pdf
- Christoph Bandt and Dmitry Mekhontsev, *Elementary fractal geometry. Networks and
  carpets involving irrational rotations*: computational searches for connected
  self-similar examples with less familiar rotations and analysis of neighbour
  graphs. https://arxiv.org/abs/2003.08687
- Huo-Jun Ruan and Jian-Ci Xiao, *The connectedness of Sierpinski sponges with
  rotational and reflectional components and associated graph-directed systems*
  (2025): finite graph methods for intersection and connectedness questions in
  a related, specifically structured class.
  https://doi.org/10.1017/S0305004125000015
- J. C. Sprott, *Automatic Generation of Iterated Function Systems* (1994):
  computational exploration of transformation coefficients.
  https://sprott.physics.wisc.edu/pubs/PAPER210.HTM

## Reproduce

Use Python 3 with the versions recorded in requirements.txt:

    python -m pip install -r requirements.txt
    python explore.py
    python check_geometry.py

explore.py regenerates parameter_scan.csv, summary.json and first_gallery.png.
check_geometry.py regenerates geometry_checks.json. All random choices in the
check have a recorded seed. The scan and gallery themselves are deterministic.
