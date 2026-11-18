# The open set condition is ruled out

17 November 2026, Australia/Sydney.

## Result and scope

**The given six-map IFS fails the open set condition for every member of the
certified connected curve, including the reference member.**

This is an all-scale conclusion. The parameter premises are supplied by the
earlier computer-assisted contact certificate; once those premises hold, the
obstruction has a short analytic proof. A finite-depth numerical trend is not
being promoted into an infinite-scale theorem.

The key is the particular contact mechanism we constructed: two different
eight-letter words have exactly the same periodic fixed point. Ordinary contact
between pieces does not, on its own, have this consequence. The shared fixed
point of two equal-length word maps is the decisive extra information.

The fractals are still connected, genuinely spatial, and exactly self-similar.
The existing dimension bounds remain valid:

| Scope | Established Hausdorff dimension bounds |
|---|---|
| Reference member | 2.1984 < dim_H K < 2.4149 |
| Every member of the connected curve | 2.1970 < dim_H K(h) < 2.4150 |

Failure of this separation condition does not determine the exact dimension.
In particular, this report does not prove a strict drop below the similarity
dimension. It also does not establish historical originality.

The conclusion concerns **this specified six-map presentation**. It is not a
proof that the same geometric set could never admit some other IFS presentation
satisfying the open set condition.

The computer-assisted premises and the new deduction remain subject to
independent mathematical review. No proof-assistant formalization is claimed.

## The construction and the exact parameter premises

For k = 0,...,5, the maps are

\[
G_k(x)=rR_{a_k}(\sigma_k\alpha)x+t_k,
\]

with

\[
\phi_k=k\pi/3,\quad \sigma_k=(-1)^k,\quad
t_k=(\cos\phi_k,\sin\phi_k,\sigma_k h),\quad
a_k=(-\sin\phi_k,\cos\phi_k,0),
\]

and u = tan(alpha/2). The reference height is exactly h = 1/sqrt(2).
Its scale and tilt are approximately

    r = 0.4761783861615476695
    alpha = 29.965238257844163 degrees.

The exact r and u are defined by the previously certified root equations,
not by rounding these displayed decimals. The connected curve assigns a unique
certified pair (r(h),u(h)) to every h in [0.7070,0.7072].

Let

    W = 0 1 1 5 3 5 1 3
    W' = 1 0 0 2 4 2 0 4,

and use the composition convention G_W = G_0 o G_1 o ... o G_3.
Define

\[
F=G_W,\qquad H=G_{W'},\qquad q=r^8.
\]

Both F and H are similarities of the same ratio q, with 0 < q < 1.
The original contact certificate proves the existence of a point p with

\[
F(p)=p=H(p).
\]

At the reference parameters p is approximately

    (1.15976670328374, 0.66959161833803, 0).

For completeness, the symmetry giving the second equality is the half-turn

\[
S=\begin{pmatrix}
1/2&\sqrt3/2&0\\
\sqrt3/2&-1/2&0\\
0&0&-1
\end{pmatrix},\qquad
SG_kS^{-1}=G_{(1-k)\bmod6}.
\]

The certified root equations make the fixed point of F lie on the fixed axis
of S. Thus Sp = p, and H = SFS^{-1} also fixes p. These exact relations hold
for the whole connected curve. Small residuals at decimal parameters alone
would not establish them.

## Short proof using the two-map subsystem

Suppose the six maps satisfied the open set condition with a nonempty open
set O. Invariance and disjointness pass to all words of any fixed length.
Since W and W' are different length-eight words, F(O) and H(O) would be
disjoint subsets of O. Consequently the two-map IFS {F,H} would satisfy the
open set condition with the same O.

But the attractor of {F,H} is the singleton {p}: both maps fix p and contract
distances to it by q. Its Hausdorff dimension is zero.

The separated-similarity dimension theorem would instead give

\[
\dim_H\{p\}=\frac{\log2}{\log(1/q)}>0,
\]

a contradiction. Therefore the six-map IFS does not satisfy the open set
condition.

This invokes the usual finite-dimensional Euclidean similarity theorem.
The following direct proof avoids using that theorem at all.

## Direct proof by packing open balls

Assume, for a contradiction, that a feasible nonempty open set O exists.
Choose an open ball B(x,epsilon) contained in O, with epsilon > 0. Let
D = ||x-p||. No assumption that p belongs to O is made.

For any positive integer m, there are 2^m distinct symbolic concatenations
of m blocks chosen from W and W'. All resulting words have length 8m.
Under the assumed open set condition their images of O, and hence their
images of B(x,epsilon), are pairwise disjoint.

Every block fixes p and has ratio q. Therefore every such m-block map L
satisfies

\[
L(p)=p,\qquad
\|L(x)-p\|=q^m D.
\]

Each image ball has radius q^m epsilon, and every one lies in the single
ball B(p,q^m(D+epsilon)). Comparing ordinary three-dimensional volumes gives

\[
2^m\frac{4\pi}{3}(q^m\epsilon)^3
\leq\frac{4\pi}{3}\big(q^m(D+\epsilon)\big)^3.
\]

After cancelling the positive scale and volume constants,

\[
2^m\leq\left(\frac{D+\epsilon}{\epsilon}\right)^3.
\]

The right-hand side is a fixed finite number; the left-hand side grows without
bound. This is impossible for all m. Thus **no feasible open set exists**.

This argument applies to arbitrary proposed open sets, including disconnected
or unbounded ones. It does not merely rule out convex balls or polyhedra.
Nor does it assume that all the word maps are geometrically distinct: if
distinct words gave the same image map, the presumed disjointness would already
fail. The contradiction under OSC covers that case as well.

The general common-fixed-point obstruction is an elementary consequence of
standard similarity geometry. The contribution in this pass is identifying
and checking its exact hypotheses in our previously certified construction.

## What the neighbour-map search was detecting

The numerical search tracked relative isometries

\[
G_u^{-1}G_v(x)=Rx+t
\]

for equal-length words u and v, with diagnostic distance

\[
d(R,t)=\max\{\|R-I\|_{\rm op},\|t\|_2\}.
\]

The root-pair symmetries reduce different-first-letter cases to (0,1), (0,2),
and (0,3). The last case can be discarded for this search by the translation
bound below. Children are generated by

\[
R'=Q_i^TRQ_j,\qquad
t'=r^{-1}Q_i^T(Rt_j+t-t_i).
\]

States with ||t|| > 5 can never return to ||t|| <= 5: throughout the parameter
box, r < .49 and ||t_i|| < 1.25, giving

    ||t'|| >= (||t|| - 2.5)/.49 > 5 when ||t|| > 5.

The numerical implementation used quaternion rotations and a translation-norm
cutoff of 5. Some representative diagnostic minima were:

| Word length | Retained states | Minimum diagnostic distance at that length |
|---:|---:|---:|
| 8 | 5,361 | 0.297590123 |
| 10 | 91,793 | 0.178829559 |
| 11 | 372,137 | 0.150107151 |
| 12 | 1,480,016 | 0.110917251 |
| 13 | 5,867,593 | 0.104380129 |

These values are finite-depth floating-point diagnostics, not certified global
minimum bounds. All recorded witness pairs were independently recomposed from
their original similarities to check the recurrence. The length-eight closest
witness rediscovered precisely W and W', which led to the structural argument.
No claim about failure of OSC depends on extrapolating this table.

The structural conclusion also explains the neighbour-map behaviour at
arbitrarily deep levels. Every m-block map has form

\[
L(x)=p+q^m A_L(x-p)
\]

for an orthogonal matrix A_L. There are 2^m symbolic choices. If any two maps
are equal, there is an exact word overlap. Otherwise compactness of the
orthogonal group supplies two arbitrarily close orientations as m grows.
For such a pair,

\[
L_1^{-1}L_2(x)
=p+A_{L_1}^TA_{L_2}(x-p)
\]

approaches the identity map. This is the all-scale near-coincidence mechanism;
the direct ball argument already proves why it is incompatible with OSC.

## Additional result: every non-opposite pair intersects

The six previously unresolved first-level pairs, two positions apart around
the ring, can now be decided using connectedness and a reflection plane.

Let V = TS, where T is the previous 60-degree roto-reflection symmetry. Then

\[
V=\begin{pmatrix}
-1/2&\sqrt3/2&0\\
\sqrt3/2&1/2&0\\
0&0&1
\end{pmatrix},\qquad
VG_kV^{-1}=G_{(2-k)\bmod6}.
\]

V is reflection in the plane

\[
P=\{x:n\cdot x=0\},\qquad n=(\sqrt3/2,-1/2,0).
\]

In particular V exchanges G_0(K) and G_2(K), fixing P pointwise.
Because K is already proved connected, G_0(K) is connected too.

Write p_j for the fixed point of G_j. The following two points belong to
G_0(K):

    positive-side point: p_0
    negative-side point: G_0 G_3 G_3 G_1(p_3).

The second address is the finite prefix 0331 followed by 3 forever.
Using the sharper family parameter rectangle from the previous dimension
certificate, interval arithmetic gives the uniform signed-distance bounds

    n dot p_0 > 1.6282
    n dot G_0 G_3 G_3 G_1(p_3) < -0.0136.

The continuous image of a connected set in the real line is an interval.
Therefore some point z of G_0(K) has n dot z = 0. It lies in P, so Vz = z.
Applying the reflection now shows

\[
z\in G_0(K)\cap G_2(K).
\]

The rotational/roto-reflection symmetries propagate this contact to all six
pairs two positions apart. This is a genuine intersection proof, not an
inference from overlapping convex hulls or close point samples.

For opposite pairs, the original invariant radius-2.5 ball and the wider
contact parameter rectangle already give a uniform gap greater than 0.0634.
The stronger gap greater than 0.4112 from the previous dimension pass still
applies as well. Thus all 15 first-level pairwise emptiness questions are now
classified:

| Pair type, indices modulo 6 | Number of pairs | Result throughout the connected curve |
|---|---:|---|
| Difference 1 or 5 | 6 | Intersect, by the exact periodic-point certificate |
| Difference 2 or 4 | 6 | Intersect, by connectedness and reflection-plane crossing |
| Difference 3 | 3 | Disjoint, with a uniform positive gap |

This classifies **which pairs intersect**, not the sizes, dimensions, or
complete locations of their intersections. The nonempty-pair graph is the
six-vertex octahedral graph, with opposite vertex pairs missing.

## Verification

verify_obstruction.py checks the exact premises and their implementation:

- The two eight-letter words are distinct, equal-length words related by
  the certified symmetry permutation.
- All 24 local symmetry identities, rotation orthogonality, and determinants
  are rechecked symbolically.
- The original tight reference contact certificate and the entire connected
  family contact certificate are both repeated at 70 and 90 interval digits.
- The sharper family enclosure is reproduced for the additional crossing proof.
- The reflection-plane identity V = I - 2 n n^T is checked symbolically.
- The signs of the two actual K-points are enclosed by interval arithmetic
  throughout the whole connected curve.
- A conservative opposite-piece gap is rechecked directly.
- All 30 binary block concatenations through four blocks are checked with a
  separately implemented 100-digit matrix-exponential geometry calculation;
  their fixed points agree to within 3.28e-57 at the stored reference centre.
- The common-scale cancellation in the volume ratio is checked symbolically.

The last two checks support the implementation. They are not substitutes for
the exact root certificate and the analytic proof for every positive integer m.

## Reproduction and files

With Python 3 and the packages in requirements.txt:

    python verify_obstruction.py

This rechecks the parameter premises, symmetries, and additional contacts,
then writes osc_obstruction_verification.json. The proof that these premises
rule out every feasible open set is the analytic argument in this report.

To rerun the exploratory numerical search separately:

    python search_neighbours.py --depth 13 --state-limit 2000000

The state limit is checked after completing a level, so the final level can
exceed it. The supplied depth-13 run retained about 5.87 million states and
requires substantially more memory than the verification script. No search
run is needed to establish the OSC obstruction.

family_box.py carries forward the sharper interval proof from
certify_dimension.py. certify_witness.py, verify_positive_contact.py, the stored
parameter certificate, and numerical search seeds provide the earlier exact
contact premises. The scripts run offline after dependencies are installed.

Earlier reports are chronological records. This report supersedes their open
OSC status and their unresolved classification for the six pairs two positions
apart; their connectedness and dimension results remain valid.

## What to investigate next

For this family, pursuing a feasible open set is no longer appropriate: the
obstruction rules it out. A route to the exact dimension must allow overlaps,
or the dimension bounds can be sharpened using larger separated subsystems.
The dimensions and topology of the actual intersections are also open.

If an OSC construction is the priority, a related family should use a different
contact mechanism. Matching two **purely periodic** addresses of the same
length, as we did here, builds in the obstruction. Ordinary connected OSC
examples can instead have junction addresses with different finite prefixes
and eventually periodic tails; those need not give two word maps with a common
fixed point.

Historical comparison remains necessary before calling this family new.
No conclusion here reopens the sidelined face-assembly/polyhedron diversion.

## Primary background

- John E. Hutchinson, *Fractals and Self Similarity* (1981), Sections 3.1,
  5.2, and 5.3, for contraction attractors, the definition of OSC, and the
  similarity dimension theorem used in the short proof:
  https://maths-people.anu.edu.au/~john/Assets/Research%20Papers/fractals_self-similarity.pdf

The direct open-ball packing proof is included in full so its conclusion
does not depend on importing an unverified criterion about neighbour maps.
