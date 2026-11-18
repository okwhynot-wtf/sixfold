# Handover to Codex: connected spatial fractal investigation

Prepared 17 November 2026, Australia/Sydney.

## Purpose and current priority

The user wants to investigate potentially new, exactly self-similar 2D/3D
fractal families. They particularly value the visual results and have repeatedly
authorized continuation. They are moving from their phone to desktop Codex.

This bundle is the complete available workspace record of this thread's seven
research phases. It contains source, reports, data, images, and portable
verification. It is not an independent mathematical review of the claims.

**Priority:** audit phases 06 and 07, then investigate finite exact word-map
relations for the reference spatial member to pursue its exact Hausdorff
dimension. Do not restart the already ruled-out OSC search for these same maps.

## Current claims and their scope

| Claim | Scope | Evidence / argument |
|---|---|---|
| Exactly self-similar compact attractor | Six similarities repeat unchanged at every scale | Standard contraction-IFS construction |
| Connected, noncoplanar spatial set | Whole certified curve | Phase-04 interval contact proof, symmetries, nested connected supersets, four noncoplanar fixed points |
| 2.1984 < dim_H K < 2.4149 | Reference h=1/sqrt(2) | Phase-05 exact separated-subsystem packing and similarity upper bound |
| 2.1970 < dim_H K(h) < 2.4150 | Every h in [.7070,.7072] | Uniform phase-05 packing and sharper curve enclosure |
| Central ball radius .398 empty; enclosing ball radius 2.14 | Whole curve | Phase-05 integer radial enclosure |
| Opposite first-level pieces separated by >.4112 | Whole curve | Phase-05 radius bound; phase 06 independently rechecks a weaker >.0634 gap |
| Every non-opposite first-level pair intersects | Whole curve | Six periodic contacts plus phase-06 connectedness/reflection crossing |
| OSC fails for the six-map IFS | Whole curve | Phase-06 common-fixed-point subsystem and open-ball volume arguments |
| WSP fails; dim_A K=3 | Whole curve | Phase-07 interval rotation premises, compact-group argument and Garcia Cor. 1.6(1) |
| No alternative finite similarity IFS with WSP or OSC can generate the same K | Each member | Intrinsic Hausdorff/Assouad dimension gap plus Fraser et al. Thm. 1.4 |
| Exact Hausdorff dimension and historical originality | Unresolved | No claim established |

All analytic deductions and computer-assisted premises still need independent
mathematical review. Python passing assertions is not proof-assistant
formalization. The phase-07 exact value 3 is ASSOUAD dimension, not Hausdorff.

## Exact six-map recipe

For k=0,...,5:

    phi_k = k*pi/3
    sigma_k = (-1)^k
    t_k = (cos(phi_k), sin(phi_k), sigma_k*h)
    a_k = (-sin(phi_k), cos(phi_k), 0)
    G_k(x) = r * R_(a_k)(sigma_k*alpha) * x + t_k
    u = tan(alpha/2)
    cos(alpha) = (1-u*u)/(1+u*u)
    sin(alpha) = 2*u/(1+u*u).

There is no additional z-axis turn in the current family (theta=0). Earlier
scans included an additional alternating turn; do not silently mix those maps.

Reference height: h=1/sqrt(2), exactly. Stored decimal root centres:

    r0 = 0.476178386161547669525964558546828831852499529292214482
    u0 = 0.2676240856235760042362757034639861560899940849527665828
    alpha approximately 29.9652382578441633743717248464 degrees.

The exact r and u are the unique roots in the certified boxes below, not these
finite displayed centres. Full data are in positive_contact_certificate.json.

Word convention: G_(k1...kn) means G_k1 o ... o G_kn, so the first digit is
the outermost map. Base-6 integer word indices put that digit first/most
significant. Applying a word to a point directly therefore works inside-out.

## Contact equations defining the connected curve

    W  = [0,1,1,5,3,5,1,3]
    W' = [1,0,0,2,4,2,0,4].

Write G_W(x)=M_W*x+c_W and p=(I-M_W)^(-1)c_W. The exact contact equations are

    -p_x/2 + sqrt(3)*p_y/2 = 0
    p_z = 0.

They place p on the fixed axis of the half-turn

    S = [[1/2,sqrt(3)/2,0],
         [sqrt(3)/2,-1/2,0],
         [0,0,-1]],

which satisfies S G_k S^-1=G_((1-k) mod 6). Hence W' is the conjugate word,
and both word maps fix EXACTLY the same p. Numerically at the reference,

    p approximately (1.15976670328374, 0.66959161833803, 0).

The second symmetry

    T = [[1/2,-sqrt(3)/2,0],
         [sqrt(3)/2,1/2,0],
         [0,0,-1]]

satisfies T G_k T^-1=G_((k+1) mod 6). Its orbit propagates the adjacent
contacts. S is a proper half-turn; T is an improper roto-reflection.

The interval proof uses T_h(x)=x-CF(x,h), enclosing its image on a closed
rectangle and proving strict inclusion plus an infinity-norm derivative bound
below 1. Automatic differentiation is implemented with mpmath intervals.

- Tight reference box: radius 1e-25 in r and u, with an enclosing height
  interval around exact 1/sqrt(2); derivative bound <3.56e-23.
- Original whole-curve box: radii .001 in r and u, h in [.7070,.7072];
  derivative bound <.357214. This defines a CURVE of recipes, not an open
  rectangle of connected parameters.
- Sharper whole-curve box: radii .000007 in r and .000060 in u;
  derivative bound <.014467. This exploits exact affine dependence on height
  before interval multiplication. Strict inclusion margins exceed 5.79e-7
  and 1.45e-6. family_box.py carries this proof forward.

## Hausdorff bounds and packing data

At depth 8 there are 6^8=1,679,616 word centres. A selected set of word maps
whose entire cylinder sets lie in disjoint enclosing balls generates a strongly
separated subset E of K. Its dimension is log(M)/(8*log(1/r)), a lower bound
for dim_H K even when the full IFS overlaps.

    Reference packing: M=464873, lower diagnostic 2.198479608378964...
    Whole-curve packing: M=461042, lower diagnostic 2.197039553055690...

Integer grid Q=2^29, initial invariant radius=2.5, sharpened enclosing radius=2.14.
Reference centre uncertainty <=1e-6; whole-curve uncertainty <=.00055.
The selected word indices and ALL integer coordinates are included in phase 05.

    Reference enclosing ball radius in grid units L=3037511; D=6075023.
    Whole-curve L=3332642; D=6665285.

Every selected centre distance exceeds D, proving strict separation of the
radius-L balls. The original C++ checker examines all same/adjacent-cell pairs;
farther cells cannot contain a near pair. Its exact pair counts are 1,157,354
and 1,482,112. The portable Python checker independently reproduces those
counts, integer minima, word centres, radial bound and dimension calculations.
The kd-tree only selected candidates and is not trusted as the proof.

## Why OSC fails

Let F=G_W and H=G_W'. Both fix p and have q=r^8. Under a hypothetical feasible
open set O, every word in F/H would give pairwise disjoint images of any ball
B(x,epsilon) inside O. For m blocks, all 2^m image balls have radius q^m*epsilon
and lie in B(p,q^m*(||x-p||+epsilon)). Volume cancellation gives

    2^m <= ((||x-p||+epsilon)/epsilon)^3,

impossible for all m. This rules out every feasible open set for these maps.
Equivalently, the two-map subsystem has singleton attractor {p}, incompatible
with the positive dimension OSC would force for two contractions.

This is a common fixed POINT, not evidence that F and H are the same MAP.
Their rotations are different. That distinction matters for the Hausdorff
dimension route below.

## First-level intersection classification

There are 6 adjacent pairs, 6 pairs two positions apart, and 3 opposite pairs.
The first 12 pairs intersect; the last 3 are separated. Intersection sizes,
dimensions and complete locations remain open.

For the six contacts two positions apart, V=T*S reflects in the plane with
unit normal n=(sqrt(3)/2,-1/2,0), conjugating G_k to G_((2-k) mod 6).
G_0(K) is connected. Two actual points in it have opposite signed distances:

    fixed point p_0: n dot p_0 > 1.6282
    G_0 G_3 G_3 G_1(p_3): signed distance < -.0136,

uniformly throughout the curve. Therefore G_0(K) crosses the reflection plane
and intersects G_2(K). Symmetry propagates all six additional contacts.

## Assouad-dimension deduction to audit carefully

1. Let A and B be the rotation parts of F and H about p. They are conjugate,
   have the same angle/order, and different axis lines. Interval checks over
   the whole curve put both traces in (2.7105,2.7252); one axis-cross component
   lies in (.2024,.2148). Their angles are in (0,60 degrees).
2. By the classification of closed SO(3) subgroups, two such small, noncoaxial
   rotations generate a dense subgroup. A proper closed subgroup either
   preserves an axis or is polyhedral; the latter has no nonidentity angle
   below 72 degrees. The same argument works for local Q0,Q1, with traces in
   (2.7324,2.7329) and an axis-cross component below -.8637.
3. There are unboundedly many DISTINCT orientations at a single common block
   length. If A has infinite order, A^(m-j)B^j, j=0..m, are distinct: an equality
   implies A^(j-i)=B^(j-i), impossible for nonidentity rotations about different
   axes. If A has finite order N, B has the same order. Their generated group
   is infinite; positive words represent every element. An infinite residue
   class of word lengths modulo N can be padded with A^N=I to produce arbitrarily
   many distinct rotations at the same length.
4. Compactness supplies distinct C,D at the same length with C^-1 D arbitrarily
   close to I. Their relative ORIGINAL word maps are

       x -> p + C^-1 D (x-p),

   nonidentity and arbitrarily close to I. This proves WSP failure, even if
   other exact word relations happen to exist.
5. K has full affine span, its WSP fails, and its positive rotation products
   are dense in SO(3). Apply Garcia Corollary 1.6(1): dim_A K=3.
6. Fraser et al. Theorem 1.4 says a full-span self-similar set with a WSP
   presentation has dim_A=dim_H. Our intrinsic dimension gap therefore rules
   out EVERY alternative finite similarity WSP/OSC presentation of this K.

Theorem references and a detailed proof are in phase 07. Verify the classification
argument, finite-order case, affine-span hypothesis, and exact scope of the
published theorem before extending the conclusion. The Python checks certify
matrix/root premises; they do not automatically prove these analytic steps.

Assouad dimension describes the worst local covering exponent. The cited
tangent theorem permits specially chosen zoom limits containing a 3D region.
It does not say every zoom fills space, that the limit occurs specifically at p,
or that K itself has interior or positive volume.

## Next target: exact Hausdorff dimension at the reference

The proposed reduction in phase 07 is:

- At h=1/sqrt(2), the contact equations are rational functions of r,u over
  Q(sqrt(2),sqrt(3)). Clearing nonzero denominators and using the nonsingular
  certified Jacobian gives an isolated polynomial-system solution. Thus r,u
  and all map coefficients are algebraic. This deduction needs review; explicit
  minimal polynomials have not been computed.
- The dense rotation group makes the linear action irreducible; noncoplanarity
  supplies affine irreducibility.
- Hochman's Corollary 1.7 would then give dim_H K=log(6)/log(1/r) IF there are
  no finite exact word-map overlaps.
- If two distinct length-n words define the identical full map, removing one
  duplicate gives the strict upper bound log(6^n-1)/(n*log(1/r)), below the
  original similarity dimension.

So decide whether the six similarities freely generate their semigroup, or
find an actual finite relation. A finite search can find a relation but cannot
prove absence at all lengths. Both matrix and translation equality are needed.

One useful branch: if A has finite order N, then F^N=H^N gives a finite exact
relation. Phase 07 does NOT establish irrationality or infinite order of A.
The approximate block rotation angle 30.802333414635138 degrees is not such
a proof. Even infinite order would leave other possible finite relations.

The broad analytic-family genericity theorem cannot be applied without checking
nondegeneracy: the two infinite periodic addresses were deliberately identified
throughout this curve. Do not assert generic dimension from parameter sampling.

## Phase map and known traps

| Folder | Role |
|---|---|
| fractal_research_01 | Original planar family, first gallery, analytic planar contact threshold |
| fractal_research_02 | Spatial scans, separated examples, extrusion and PLY previews |
| fractal_research_03 | Rigorous negative/disconnection certificates for earlier trial recipes |
| fractal_research_04 | Positive periodic contact, connected curve, proper spatiality |
| fractal_research_05 | Hausdorff lower bounds, exact packing data, central/radial geometry |
| fractal_research_06 | OSC obstruction, WSP not yet settled there, all pairwise emptiness questions resolved |
| fractal_research_07 | WSP/Assouad argument, alternative-presentation obstruction, conditional Hausdorff route |

Older statements that OSC is open or alternative OSC presentations have not
been excluded are superseded by phases 06/07. Earlier r=.47, alpha=30 recipes
are different from the certified root and remain unresolved.

The original 2D gear construction is useful history but is not the current
spatial set. A separate mirror-turn/survivor project mentioned elsewhere by the
user is also not interchangeable with these maps.

Some legacy geometry modules have main entry points expecting older phase CSV
files; use the documented verifier/renderer entry points. Original renderers
contain Linux font paths; render_current.py supplies portable fonts. PLY files
are finite point clouds, not surfaces. The broken phone-viewer experiment is
not a dependency of this bundle.

## Verification and operating notes

Run python verify_handover.py after installing requirements.txt. It verifies
MANIFEST.json and executes the current checks in a temporary copy, preserving
the original evidence. The portable phase-05 checker uses Python integers and
needs no C++ compiler. The original C++ checker and its source remain available
for direct specialist reproduction. VALIDATION.json records the handover run.

The package was assembled and verified with Python 3.12.14 on Linux. Windows
execution was not observed; the top-level scripts avoid shell commands and
platform-specific compiled binaries. The scientific dependencies are pinned.
The optional render wrapper uses the DejaVu font supplied with Matplotlib when
the historical Linux font path is absent.

Continue new work in a new phase or checkout, keep snapshots, and update a
current-status note when conclusions change. There is no external Git remote
configured or implied by this handover. No credentials or signed transfer URLs
are required by the project scripts.
