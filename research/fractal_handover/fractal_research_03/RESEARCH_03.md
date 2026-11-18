# Nine spatial candidates remain; a face-assembly side check

17 November 2026, Australia/Sydney.

## Decision and immediate result

Continue the contact investigation, with a narrower target. The 19 spatial
recipes left unresolved in the previous pass now split into:

- 10 with computer-assisted disconnection certificates;
- 9 still unresolved;
- 0 newly proved connected.

One of the ten also has a strong-separation certificate: r = 0.49, turn = 20
degrees, tilt = 0 degrees. Its Hausdorff dimension is therefore exactly
log(6)/log(100/49), approximately 2.511754048997388.

This is progress in classifying these examples. It does not establish an original
fractal family. The calculations are reproducible computer-assisted certificates,
with an explicit geometric error bound and exact integer cover decisions; they
have not been independently peer-reviewed or formalized in a proof assistant.

## The face-assembly idea

The idea is plausible as a construction method: use a planar pattern as a face
panel, arrange panels in space, and design the seams. Related research includes
polyhedral constructions with intricate face boundaries and constructions that
iteratively arrange smaller polyhedra on faces.

Two distinctions matter for this particular pattern:

1. The literal infinite gear set is a porous fractal, not a filled polygonal plate.
   A finite thickened approximation, a filled outline, and the infinite set give
   different assembly problems.
2. Two distinct flat face planes intersect along a straight line. Planar panels
   meeting at an angle can share a straight edge or portions of that line. An
   arbitrary curved or toothed boundary will require altered panels, connectors,
   folds, or a more elaborate limiting surface.

A useful first experiment would therefore give two adjacent panels an explicitly
matching straight seam and test the recursion on both sides of it. Only after
that succeeds would I assemble a complete polyhedral frame.

Simply arranging finitely many copies of the planar gear in space does not by
itself increase Hausdorff dimension: a finite union of similarity images has the
same dimension as the planar gear, about 1.7387 at the first-contact recipe. It
also does not automatically give smaller copies of the entire 3D assembly.
A compatible whole-object recursion must be specified separately.

I would keep this as a small design branch. Its central question—whether matching
boundaries can be preserved at every level—is directly related to the contact
problem in the main investigation.

## What changed in the contact test

Earlier passes used floating-point point-centre distances. The new program uses
interval-enclosed map coefficients followed by an integer spatial cover. A
disconnected outer graph is a certificate of disconnection of the infinite set.
A connected outer graph remains inconclusive.

The target recipes have exact r = 47/100, 48/100 or 49/100, exact integer degree
angles, and exact height h = 1/sqrt(2). These are the nominal decimal recipes of
the previous scan, rather than its incidental binary floating-point grid drift.

The map definition is unchanged:

    phi_k = k*pi/3, sigma_k = (-1)^k,
    t_k = (cos(phi_k), sin(phi_k), sigma_k/sqrt(2)),
    Q_k = R_z(sigma_k*theta) R_tangent(k)(sigma_k*alpha),
    G_k(x) = r Q_k x + t_k.

The same six maps repeat at every level.

### Coefficient and centre error

mpmath interval arithmetic at 70 decimal digits encloses every exact matrix and
translation coefficient. Each coefficient is approximated on the grid 1/Q,
Q = 2^29. The code checks that the full interval differs from its chosen grid
coefficient by at most 1/Q. Nearest-grid selection avoids ambiguity when an
interval straddles an integer grid boundary.

All exact centres and the attractor lie in the ball of radius 5/2. Indeed,
||t_k|| = sqrt(3/2) < 5/4, and for r <= .49,

    r*(5/2) + 5/4 <= 2.475 < 5/2.

In grid coordinates, a step is implemented by integer matrix multiplication,
coordinatewise floor division by Q, and addition of the integer translation.
If a grid centre has norm below 3, its one-step Euclidean error is at most

    (9 + 2*sqrt(3))/Q < 13/Q.

The terms account for matrix coefficient error, translation error, and floor
rounding. Propagating the contraction gives total centre error at most

    13/[Q*(1-.49)] < 10^-6 = E.

This also closes the induction: exact centre norms are at most 2.5 and grid
centre error is at most E, so grid centres stay below norm 3. Every signed-64-bit
product sum is bounded by 4.5 Q^2 + 9Q < 2^63; the integer arithmetic does not
overflow under these bounds.

### Exact covers and contact graph

At total word depth n, every descendant lies within distance r^n*(5/2) of its
exact finite centre. Therefore a cube around the integer grid centre, with
coordinate half-width

    B = ceil(Q * ((5/2)*r^n + E)),

covers its entire descendant set. The ceiling uses exact rational arithmetic.

Space is divided into integer cells of width 2B. Each closed cube meets the eight
cells obtained from its lower cell index by independently adding 0 or 1 in each
coordinate. The code records all of these cells, including boundary cells.

For each of the six first-level pieces, the union of its descendant cell lists
is an outer cover. Two pieces with disjoint cell lists cannot intersect. A graph
of the remaining possible intersections is therefore an outer contact graph.

If that graph is disconnected, the finite union defining the attractor separates
into nonempty compact groups with no contacts: the attractor is disconnected.
If it has six components, the strong separation condition holds, and the standard
similarity-dimension formula applies. A one-component graph establishes neither
an actual contact nor connectedness.

Each case was checked at depths 4 through 8, stopping when disconnection was
certified. certificates.json retains the grid matrices, cover radii, graph edges,
cell counts and SHA-256 fingerprints. The full cell lists can be regenerated.

## Verification

verify_results.py performs:

- 250 brute-force three-dimensional cell coverage comparisons, including negative
  coordinates and cell boundaries;
- 570 short-word comparisons between NumPy signed-integer centre generation and
  independently written Python arbitrary-precision integer calculations;
- interval coefficient rechecks for all 19 recipes;
- full reproduction of a depth-8 disconnection certificate and the depth-6
  strong-separation certificate, including all cell fingerprints.

All checks passed. The independent short-word and cell tests exercise the
arithmetic and indexing; reproducing two full certificates checks the saved
results. This does not substitute for an independent review of the derivation.

## Next research target

Concentrate on one low-parameter slice:

    height = 1/sqrt(2), turn theta = 0, tilt alpha = 30 degrees,
    scale r around 0.46 to 0.47.

The nominal r = .47 case remains unresolved after the new depth-8 cover. It is a
useful target for a positive contact witness, rather than another broad image
gallery. A positive witness must exhibit actual points or an inclusion argument
forcing an intersection. Repeated failure to exclude intersection is not enough.

After establishing the contacts, use their graph to decide global connectedness.
Then determine what is distinctive about those contacts across a parameter
subfamily, and compare the map recipe and theorem with the nearest literature.
If that target yields no tractable contact structure, a useful alternative is to
design matching contact points or seams into a new recursive construction from
the beginning, using the face-assembly idea as a guide.

## Related primary sources

- Ergun Akleman, Paul Edmundson and Ozan Ozener, *Smooth & Fractal Polyhedra*:
  a subdivision construction of limiting shapes with intricate face boundaries.
  https://people.tamu.edu/~ergun/research/topology/papers/bridges04.pdf
- Robert W. Fathauer, *Iterative Arrangements of Polyhedra—Relationships to
  Classical Fractals and Hauy Constructions* (Bridges 2013): smaller polyhedra
  arranged recursively on the faces of a starting polyhedron.
  https://archive.bridgesmathart.org/2013/bridges2013-175.html
- Iancu Dima, Rachel Popp, Robert S. Strichartz and Samuel C. Wiese,
  *A Convex Surface with Fractal Curvature*: a related example of a surface
  constructed as a limit of polyhedral approximations, with fractal curvature.
  https://arxiv.org/abs/1907.06265

These are relevant precedents, not identifications of our gear with any of their
constructions and not evidence that our specific family is original.

## Reproduce

Install requirements.txt with Python 3, then run:

    python certify_contacts.py
    python verify_results.py

No network connection is needed. Candidate input is included. The certificate
code makes no use of floating-point nearest-neighbour distances for its logical
decisions. Its interval-coefficient calculations use the mpmath version recorded
in requirements.txt.

## Results by nominal recipe

| Scale r | Turn | Tilt | Last depth | Outer components | Result |
|---:|---:|---:|---:|---:|---|
| 0.47 | 0° | 30° | 8 | 1 | Unresolved |
| 0.47 | 10° | 30° | 8 | 3 | Disconnected |
| 0.48 | 0° | 15° | 8 | 2 | Disconnected |
| 0.48 | 0° | 30° | 8 | 1 | Unresolved |
| 0.48 | 10° | 15° | 8 | 1 | Unresolved |
| 0.48 | 10° | 30° | 8 | 1 | Unresolved |
| 0.48 | 20° | 30° | 8 | 3 | Disconnected |
| 0.49 | 0° | 0° | 6 | 2 | Disconnected |
| 0.49 | 0° | 15° | 8 | 1 | Unresolved |
| 0.49 | 0° | 30° | 8 | 1 | Unresolved |
| 0.49 | 10° | 0° | 6 | 2 | Disconnected |
| 0.49 | 10° | 15° | 8 | 1 | Unresolved |
| 0.49 | 10° | 30° | 8 | 1 | Unresolved |
| 0.49 | 20° | 0° | 6 | 6 | Strong separation |
| 0.49 | 20° | 15° | 8 | 3 | Disconnected |
| 0.49 | 20° | 30° | 8 | 1 | Unresolved |
| 0.49 | 30° | 0° | 6 | 2 | Disconnected |
| 0.49 | 30° | 15° | 8 | 3 | Disconnected |
| 0.49 | 30° | 30° | 8 | 3 | Disconnected |
