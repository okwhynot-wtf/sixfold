# Continuing the gear investigation: contacts and three-dimensional versions

17 November 2026, Australia/Sydney.

## Assessment

This is worth continuing as a focused investigation of contact geometry, with a
parallel visual-design application. The evidence does not yet justify calling
the planar family, its special cases, or the spatial versions new. Rotated
hexagonal constructions and spatial IFSs already exist. The research target is a
precisely stated geometric property or contact mechanism, supported by proof.

This pass produces two different kinds of 3D version:

| Construction | What it preserves | Established dimension |
|---|---|---|
| Extruded gear | The original planar first-contact profile, throughout a vertical interval | 2.7386979387... |
| Spatial gear | Six exact copies, with centres above and below the plane and tilted local rotations | 2.0096043615... at the selected parameters |

Both infinite sets are exactly self-similar. The extrusion is connected, using
the planar first-contact result in the first investigation. The selected spatial
gear has separated first-level pieces and is totally disconnected. Those are
different design choices, not interchangeable connectivity claims.

The images are finite point approximations, rendered from mathematically
generated coordinates. They are not images generated from a prose description.

## Further 2D investigation

I selected 157 of the original coarse screen's unresolved parameter pairs, with
r <= 0.3575 and turns strictly between 0 and 60 degrees, and repeated the cover
screen one level deeper. One additional case was excluded numerically:

    r = 0.345, theta = 14 degrees.

A depth-6 recheck gives a minimum pair-separation lower estimate of about
0.00313449. The depth-3 outer graph had allowed all six neighbour contacts;
the deeper screen excludes them all. This demonstrates why a connected-looking
preview or a connected outer graph cannot establish connectedness.

The other 156 cases remain unresolved by that deeper test. These calculations
are floating-point screens with rigorous geometric tail bounds in exact
arithmetic; floating-point error has not been interval-certified. They should
not be described as 156 proved connected examples or as certified new results.

The new screen is recorded in planar_refinement.csv, with its depth-6 follow-up
in planar_depth6.csv. The original input is included as initial_planar_scan.csv.

## Route 1: preserve the planar gear by extrusion

Let K be the planar first-contact set at theta = 30 degrees and

    r_c = (sqrt(15)-sqrt(3))/6.

The first investigation derives dim_H(K) = s = log(6)/log(1/r_c), together with
the open set condition and connectedness. Choose a half-height H > 0. Define

    E = K x [-H,H].

This product is an exact self-similar set in 3D, not merely a visual suggestion.
For each planar similarity f_k and each j in {-1,0,+1}, use the spatial map

    F_(k,j)(x,y,z) = (f_k(x,y), r_c*z + j*H*(1-r_c)).

There are 18 maps, and each shrinks every spatial direction by the same factor
r_c. Their vertical images are the intervals

    [-H, H*(2*r_c-1)], [-H*r_c,H*r_c], [H*(1-2*r_c),H].

Because r_c > 1/3 these cover [-H,H]. Taking all 6 x 3 combinations gives
union_(k,j) F_(k,j)(E) = E, establishing exact whole-object self-similarity.

### Dimension

The dimension is s+1 = 2.738697938748511..., using the product with an interval.
For a short derivation, the planar open-set-condition attractor is s-regular:
its natural measure has ball masses bounded by constants times epsilon^s.
Its product with interval length measure gives a lower bound s+1, and covering
K at scale epsilon and the interval at the same scale gives the upper bound.

The vertical images overlap. Therefore log(18)/log(1/r_c) is NOT the dimension
formula to use here. The product argument is what justifies the stated value.

In the rendered example H = 0.32. Changing H to any other positive value changes
the aspect ratio but preserves dimension and the same self-similar map scheme.
Since the planar K is connected, E is connected as a product of connected sets.

This is a standard mathematical construction applied to this profile. Its value
here is faithful 3D visualization, not an originality claim.

## Route 2: let the six-copy arrangement extend through space

Let phi_k = k*pi/3 and sigma_k = (-1)^k. Set

    t_k = (cos(phi_k), sin(phi_k), sigma_k*h),
    u_k = (-sin(phi_k), cos(phi_k), 0),
    Q_k = R_z(sigma_k*theta) R_(u_k)(sigma_k*alpha),
    G_k(x) = r Q_k x + t_k.

R_(u_k) is a right-handed rotation about the unit tangent vector u_k. The matrix
product applies the tilt first, then the z-axis turn. The same six maps repeat
at every depth. The new parameters are h, the alternating centre height, and
alpha, the local tilt.

When h = 0 and alpha = 0, this is exactly the original planar construction
embedded in z = 0. This equivalence was checked against the original code.
For positive heights and tilted rotations the construction can extend through
all three spatial directions.

### A simple exact spatial family with dimension greater than two

Choose h = 1/sqrt(2). The six translation vectors are the vertices of a regular
octahedron in a different orientation. Their norms are sqrt(3/2), and their
minimum pair distance is sqrt(3). Let

    R = sqrt(3/2)/(1-r).

The full attractor lies in the ball of radius R, and each first-level piece lies
in the ball B(t_k,rR). These six balls are disjoint whenever

    2*r*sqrt(3/2)/(1-r) < sqrt(3),

equivalently r < sqrt(2)-1. This argument works for ANY of the chosen proper
rotations Q_k. It proves strong separation, independent of the numerical scan.

Thus the Hausdorff dimension is exactly log(6)/log(1/r). For

    1/sqrt(6) < r < sqrt(2)-1

it is strictly between 2 and 3. This interval is nonempty. In particular,

    r = 0.41, theta = 30 degrees, h = 1/sqrt(2), alpha = 25 degrees

gives dim_H = 2.0096043615114025..., with an enclosing-ball separation margin
of about 0.0298630. The inequality can be checked algebraically: 0.41 is below
sqrt(2)-1 because 1.41^2 < 2; 6*(0.41)^2 > 1 proves dimension > 2. Dimension
greater than 2 ensures that this set cannot be contained in any plane.

Since its first-level pieces are separated, this example is a spatial fractal
dust, despite having dimension greater than 2. It is not a connected sponge.
The images can show apparent bridges caused by projection and pixel footprints.

### Spatial parameter scan

I screened 120 combinations:

- r = 0.40, 0.41, ..., 0.49;
- theta = 0, 10, 20, 30 degrees;
- alpha = 0, 15, 30 degrees;
- h = 1/sqrt(2).

At cover depth 3, the outer contact graphs had 6 components in 88 cases,
3 components in 9 cases, 2 components in 4 cases, and 1 component in 19 cases.
The first three categories exclude connectedness numerically. The final 19
are unresolved, not verified connected sets.

The denser rendered trial r = 0.46, theta = 20, alpha = 30 has a positive
depth-4 separation estimate about 0.0157193. Its dimension 2.307396... is a
similarity dimension until that separation computation is rigorously certified;
the broad enclosing-ball proof above does not cover r = 0.46. The gallery labels
its separation as numerical, not as an analytic theorem.

## Literature comparison and decision

The unturned planar case is the classical Sierpinski hexagon, as described in
the Boston University dynamics exposition. A primary gallery by Emlyn Corrin
also explicitly includes rotated Sierpinski hexagons and rotated hexaflakes.
This is direct evidence that rotating a hexagonal recursion is an existing idea.
The gallery does not, by itself, settle whether its map definitions coincide
with the present alternating-turn family.

Bandt and Mekhontsev's research studies computer-assisted searches for connected
self-similar sets with unusual rotations. Octahedral IFS constructions also
precede this investigation. Consequently, neither the general technique nor
the move to 3D should be presented as new.

My decision is to continue, with two specific aims:

1. Contact research: use the explicit 0-degree and 30-degree planar examples as
   checks, then develop tighter certified intersection tests at other angles.
   The 19 unresolved spatial cases are another bounded candidate list.
2. Visual exploration: keep the extrusion as a faithful version of the gear,
   while studying tilted spatial variants separately. Their mathematical
   connectivity and visual appearance should remain separately documented.

This pass has not demonstrated a new family. It has produced concrete spatial
constructions, an analytic dimension result, and a narrower research target.

## Sources

- Boston University, *The Sierpinski Hexagon*:
  https://math.bu.edu/DYSYS/arcadia/sect3.html
- Emlyn Corrin, *PowerPoint Fractals*, hexagonal constructions:
  https://emlyn.github.io/PowerPointFractals/
- Christoph Bandt and Dmitry Mekhontsev, *Elementary fractal geometry. Networks
  and carpets involving irrational rotations*:
  https://arxiv.org/abs/2003.08687
- Paul Bourke, *Octahedral Sierpinski Carpet*:
  https://www.paulbourke.net/fractals/octacarpet/
- John E. Hutchinson, *Fractals and Self Similarity*:
  https://maths-people.anu.edu.au/~john/Assets/Research%20Papers/fractals_self-similarity.pdf

## Reproduce and files

With Python 3, install the versions recorded in requirements.txt, then run:

    python continue_research.py
    python extrude_gear.py

Both scripts run without a network connection. The initial planar CSV is
included. The code checks matrix orthogonality, reduction to the 2D recipe,
the spatial separation bound, and the interval cover used by the extrusion.

The PNGs are finite point renderings. The two PLY files contain point clouds,
not watertight triangle meshes. The original derivation and its checks are
included under first_investigation/ for context and reproducibility.
