# Full local scaling dimension, despite smaller Hausdorff dimension

17 November 2026, Australia/Sydney.

## Result

There is now a computer-assisted deduction of an **exact Assouad dimension**:

\[
\boxed{\dim_A K(h)=3\qquad\text{for every }h\in[0.7070,0.7072].}
\]

This is a different dimension from the Hausdorff dimension previously bounded.
Both statements hold together:

| Scope | Hausdorff dimension | Assouad dimension |
|---|---|---|
| Reference member, h = 1/sqrt(2) | 2.1984 < dim_H K < 2.4149 | Exactly 3 |
| Every member of the connected curve | 2.1970 < dim_H K(h) < 2.4150 | Exactly 3 |

Hausdorff dimension remains undetermined exactly. Assouad dimension measures
the most demanding local covering behaviour across locations and scales.
The new result establishes full three-dimensional local scaling complexity
in this precise sense, even though each set has zero ordinary volume and
contains no solid region.

A further consequence is intrinsic to the geometry: **no alternative finite
IFS of contracting similarities generating the same K can satisfy the weak
separation property, and therefore none can satisfy the open set condition.**
The last pass only ruled out OSC for our specified six maps. The dimension gap
now rules out these separation properties for every such alternative similarity
presentation of the same set.

The deduction combines our interval-certified parameters with published
dimension theorems and elementary compact-group arguments. It has not received
independent mathematical review or a proof-assistant formalization. This is
not a claim that the dimension-gap phenomenon itself is new; its general theory
is established in the cited research. Historical originality of this particular
construction remains open.

## The exact family and inherited premises

The six maps, indexed by k = 0,...,5, are

\[
G_k(x)=rQ_kx+t_k,\quad
Q_k=R_{a_k}(\sigma_k\alpha),\quad u=\tan(\alpha/2),
\]

\[
\phi_k=k\pi/3,\quad \sigma_k=(-1)^k,\quad
a_k=(-\sin\phi_k,\cos\phi_k,0),\quad
t_k=(\cos\phi_k,\sin\phi_k,\sigma_k h).
\]

For each h in [0.7070,0.7072], the exact r(h) and u(h) are the uniquely
certified roots of the earlier contact equations. The reference member has
approximately r = 0.4761783861615476695 and alpha = 29.965238257844163 degrees.
These decimals are display values, not the definition of the exact roots.

The earlier certificates establish:

1. K is a nonempty compact, connected attractor with this exact self-similarity.
2. Four fixed points in K are not coplanar, so its affine span is all of R^3.
3. The two length-eight word maps

       F = G_(01153513), H = G_(10024204)

   fix the same point p and have the same ratio q = r^8.
4. With the half-turn S from the contact proof, H = SFS^-1 and Sp = p.
5. Throughout the curve,

       |r-r0| <= 0.000007, |u-u0| <= 0.000060,
       0.476171 < r < 0.476186.

The new program repeats the original tight reference and connected-family
contact certificates, reproduces the sharper parameter enclosure, and checks
the symbolic symmetry identities. Nothing here assumes that a finite rendering
establishes a contact or a dimension.

## The finite rotation checks

Write the block maps around their common fixed point as

\[
F(x)=p+qA(x-p),\qquad H(x)=p+qB(x-p),
\]

where A = Q_0 Q_1 Q_1 Q_5 Q_3 Q_5 Q_1 Q_3 and B is the corresponding
partner product. Both matrices lie in SO(3), and B = SAS^-1. They therefore
have exactly the same principal rotation angle and the same order, whether
that order is finite or infinite.

For a proper rotation R, trace(R) = 1 + 2 cos(theta), with principal angle
theta in [0,pi]. Thus

    2 < trace(R) < 3

places theta strictly between 0 and 60 degrees. For angles in this interval,
the vector

    v(R) = (R32-R23, R13-R31, R21-R12)

is a nonzero multiple of its oriented axis. A nonzero cross product of two
such vectors proves that their axis lines differ.

Interval arithmetic over the ENTIRE u rectangle gives the following
conservative enclosures:

| Pair | Trace enclosures | A certified nonzero axis-cross component |
|---|---|---|
| Local Q0, Q1 | Both in (2.7324, 2.7329) | z component in (-0.8647, -0.8637) |
| Block A, B | Both in (2.7105, 2.7252) | x component in (0.2024, 0.2148) |

The stored JSON contains finer diagnostic intervals. The actual proof decisions
use outward interval arithmetic, not the rounded endpoints shown here.
The predicates pass at 70 and 90 interval digits and are independently repeated
at 100 digits.

At the reference centre an independent matrix-exponential calculation gives
the block angle approximately 30.802333414635138 degrees. The proof does not
infer irrationality from this decimal.

## Why these rotations generate all spatial orientations densely

We use the classical classification of closed subgroups of SO(3), recorded,
for example, in Section 3 of M. Olive's paper [1]. A proper closed subgroup
either preserves an axis line or is one of the three finite polyhedral rotation
groups. The latter groups have no nonidentity rotation with principal angle
below 72 degrees. In an axis-preserving subgroup, every rotation with angle
strictly between 0 and pi has that same axis line.

Consequently, two rotations with different axis lines and angles in (0,60
degrees) cannot lie in a proper closed subgroup. Their generated subgroup is
dense in SO(3).

The interval checks apply this argument twice:

- Q0 and Q1 generate a dense subgroup of SO(3).
- A and B also generate a dense subgroup, in particular an infinite group.

The semigroup of positive products of the local rotations is dense as well.
In a compact group, the inverse of a rotation is a limit of its nonnegative
powers (or one of those powers when its order is finite). Thus the closure of
the positive-product semigroup contains the whole generated group.

## A stronger conclusion than failure of OSC: failure of WSP

The weak separation property permits exact repeated word maps, but forbids
nonidentity relative word maps from approaching the identity. In symbols,
we must show that there exist equal-length words s_j and t_j with

\[
G_{s_j}^{-1}G_{t_j}\ne I,\qquad
G_{s_j}^{-1}G_{t_j}\longrightarrow I.
\]

The previous OSC obstruction alone did not establish this stronger failure:
unbounded symbolic multiplicity might in principle have come only from exact
coincidences. Here the rotation information supplies arbitrarily many
**geometrically distinct** maps at the same scale.

Let S_m be the set of rotations obtained by words of exactly m letters in
the alphabet {A,B}. We claim that |S_m| is unbounded. The proof covers both
possible orders of A, so no unproved irrational-angle assertion is needed.

### Case 1: A has infinite order

B has the same angle and a different axis line. The m+1 products

\[
A^{m-j}B^j,\qquad j=0,\ldots,m,
\]

are distinct. Indeed, equality for i < j, after cancellation on the left and
right, would imply

\[
A^{j-i}=B^{j-i}.
\]

Every nonzero power of an infinite-order rotation is nonidentity and has
the same axis line as the original rotation. The two sides therefore cannot
be equal, since A and B have different axis lines. Hence |S_m| >= m+1.

### Case 2: A has finite order N

B also has order N. The group generated by A and B is infinite by the
rotation argument above. Because A^-1 = A^(N-1) and B^-1 = B^(N-1), every
group element can be represented by a positive word in A and B.

Among infinitely many distinct group elements, infinitely many have chosen
positive-word representations whose lengths have the same residue modulo N.
Take any M of these words and let L be their largest length. Pad each shorter
word on the right by A^(L-length). Each padding exponent is a multiple of N,
so the represented rotation is unchanged. The resulting words all have length
L and still represent M distinct rotations. Thus |S_L| >= M for arbitrary M.

### Compactness produces nonidentity near-coincidences

The orthogonal group is compact. Since |S_m| is unbounded, for every positive
epsilon some S_m contains two distinct rotations C and D with
||C-D|| < epsilon. The corresponding original word maps have length 8m,
ratio q^m, and form

\[
L_C(x)=p+q^m C(x-p),\qquad
L_D(x)=p+q^m D(x-p).
\]

Their relative map is

\[
L_C^{-1}L_D(x)=p+C^{-1}D(x-p).
\]

It is not the identity because C != D, and it approaches the identity
uniformly on every bounded set as epsilon tends to zero. These are valid
word maps in the original six-map IFS. **The WSP therefore fails.**

The proof remains valid if other word pairs coincide exactly. It requires
only the unbounded number of distinct rotations just established.

## Applying the published dimension theorem

Ignacio Garcia's Corollary 1.6(1) [2] applies to a self-similar attractor whose
affine span is R^d, whose IFS fails WSP, and whose positive rotation products
are dense in SO(d). It gives Assouad dimension d.

All three premises have now been proved for every member of our certified
curve. Taking d = 3 gives

\[
\boxed{\dim_A K(h)=3.}
\]

This is an application of an existing theorem to this construction, not a
new general dimension theorem.

## Why another similarity recipe cannot remove the overlap problem

Fraser, Henderson, Olson and Robinson prove in Theorem 1.4 of [3] that, for a
full-affine-span self-similar set, a generating similarity IFS satisfying WSP
has equal Hausdorff and Assouad dimensions.

Our geometric set has

\[
\dim_H K<2.4150<3=\dim_A K.
\]

Both dimensions depend on K itself. If some OTHER finite contracting-similarity
IFS generated exactly the same K and satisfied WSP, the theorem would force
those dimensions to agree, a contradiction. Thus no such alternative WSP
presentation exists. OSC is stronger than WSP, so an alternative OSC
presentation is excluded as well.

The scope is finite IFSs of contracting similarities in Euclidean space.
No claim is made here about every broader type of symbolic, affine, conformal,
or graph-directed description.

## What this means for zooming

For a bounded set K, Assouad dimension is the infimum of exponents t for which
a constant C bounds the local covering number by

\[
N_\rho(K\cap B(x,R))\leq C(R/\rho)^t
\]

uniformly over x in K and 0 < rho < R. Here N_rho is the least number of
radius-rho balls needed to cover the indicated set.

Dimension 3 means that no smaller exponent works uniformly. The theorem's
tangent construction also gives specially chosen magnification limits
containing a three-dimensional region: Theorem 1.9 of [2] supplies a
parallelotope in the full three-dimensional overlap-direction space.

This is a statement about selected sequences of locations and scales.
It does not say that every zoom becomes more crowded, or that the original
fractal contains a solid region. Each finite similarity image still has
Hausdorff dimension below 3 and ordinary volume zero. A limit of magnified
sets can nevertheless contain a region.

The earlier central empty ball and this maximal local crowding can coexist.
The hole is one global geometric feature; Assouad dimension quantifies the
most demanding local scaling configurations.

## A concrete route still open for the Hausdorff dimension

For the reference member, the unknown Hausdorff dimension can now be connected
to a specific algebraic word-relation problem.

First, its map coefficients are algebraic numbers. At the exact algebraic
height h = 1/sqrt(2), the two contact residuals are rational functions of r and
u with coefficients in Q(sqrt(2),sqrt(3)). Clearing nonvanishing denominators
gives two polynomial equations over that algebraic field. The interval
contraction certificate proves that their Jacobian at the root is nonsingular.
The root is therefore an isolated nonsingular algebraic-system solution, and
r and u are algebraic. The rotation entries are rational functions of u and
sqrt(3), so they are algebraic too. No assertion that alpha itself is an
algebraic number is needed.

Second, the dense spatial rotation group makes the linear action irreducible,
and the full affine span rules out an affine-subspace degeneracy.

Hochman's Corollary 1.7 [4] consequently provides this conditional route:

\[
\text{no two distinct finite words define the same map}
\quad\Longrightarrow\quad
\dim_H K=\frac{\log6}{\log(1/r)}.
\]

The missing premise is not yet proved. In this theorem an **exact word overlap**
means equality of the entire transformations G_u = G_v, not merely that the
two maps fix the same point. Our particular block maps F and H are different,
as their different rotation axes certify, despite sharing p.

Conversely, if an equality G_u = G_v occurs for two distinct words of length n,
the same K can be generated by at most 6^n-1 maps of ratio r^n. This yields

\[
\dim_H K\leq\frac{\log(6^n-1)}{n\log(1/r)}
<\frac{\log6}{\log(1/r)}.
\]

Thus, at the reference member, deciding the existence of a finite exact map
relation is a precise next target. Finite searches alone cannot establish that
no relation exists at any length.

One illustrative branch is already clear: if the block rotation A had finite
order N, then B would have the same order and F^N = H^N would be an exact
map relation. The present Assouad proof deliberately covers both finite and
infinite order and does not decide that arithmetic question.

This algebraic route is stated for the reference member. We do not automatically
apply an almost-every-parameter theorem to the connected curve: the construction
deliberately identifies the two infinite addresses W repeated forever and W'
repeated forever throughout that curve.

## Figure and reproducibility

shared_point_zoom.png shows selected word copies near the common fixed point
p. The upper panel uses the two one-block choices; the lower panel uses the
32 five-block choices. Each panel compensates for the contraction and for the
rotation along the all-F route, so the aligned normalized coordinates are

\[
A^{-m}\frac{G_{\text{block word}}(x)-p}{r^{8m}}.
\]

The views correspond to linear magnifications of approximately 378 and
7.75 trillion relative to the original scale. They are finite renderings of
known subsets of those zoomed sets, not complete neighbourhoods or the weak
tangents from the theorem. Pixel density supplies no dimension proof.

With Python 3 and the versions in requirements.txt:

    python certify_assouad.py
    python verify_assouad.py
    python render_shared_zoom.py

The first script repeats the contact premises and certifies the rotation
inequalities for the entire parameter curve. The second checks the computations
with separately implemented 100-digit matrix exponentials, repeats the interval
predicates at 100 digits, and checks the noncommutative cancellation algebra.
The third reproduces the illustrative image. No network access is required
after dependencies are installed.

The independent entry comparisons comprise 54 matrix-entry checks, including
the centre and both ends of the u rectangle. These point checks support the
implementation; they do not replace the interval enclosure over the full box.
The maximal observed orthogonality error was below 4.29e-101.

The infinite-order/finite-order case split, compactness argument, group
classification, algebraicity deduction, and published dimension results are
analytic steps spelled out here. They are not being represented as statements
automatically proved by the Python program.

Earlier reports are chronological records. This report strengthens the prior
OSC obstruction to WSP failure and excludes all alternative finite similarity
presentations satisfying either property. It does not supersede the earlier
Hausdorff dimension bounds with the value 3: that exact value is the Assouad
dimension.

## Primary sources

[1] M. Olive, *Effective computation of SO(3) and O(3) linear representations
symmetry classes*, Section 3 (closed-subgroup classification):
https://arxiv.org/pdf/1709.01776

[2] Ignacio Garcia, *Assouad dimension and local structure of self-similar sets
with overlaps in R^d*, Corollary 1.6(1) and Theorem 1.9:
https://ri.conicet.gov.ar/bitstream/handle/11336/142146/CONICET_Digital_Nro.68559f3e-37df-4dcf-b61b-0117e933f96c_A.pdf?sequence=2

[3] J. M. Fraser, A. M. Henderson, E. J. Olson and J. C. Robinson, *On the
Assouad dimension of self-similar sets with overlaps*, Theorem 1.4:
https://arxiv.org/pdf/1404.1016

[4] Michael Hochman, *On self-similar sets with overlaps and inverse theorems
for entropy in R^d*, Corollary 1.7:
https://arxiv.org/pdf/1503.09043
