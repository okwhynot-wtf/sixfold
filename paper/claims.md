# Claim and review register — draft 0.2

Status as of 19 November 2026. Draft 0.2 clarifies the arguments and retains the original claims and scientific inputs. “Computer-assisted claim” means the cited implemented checks pass and a mathematical deduction is supplied. It does **not** mean independent peer review or proof-assistant formalisation. Every row below still needs independent mathematical review; the last column identifies the relevant step.

All research links point to unchanged local files also present in evidence commit `1c660bedf8cd3e52bad8e5d033535dcde6e06b6e`, [archived DOI](https://doi.org/10.5281/zenodo.24336419). The [new run receipt](verification.json) is separate from that older deposit.

| ID / claim | Parameter scope | Evidence and current status | Analytic step / review focus |
| --- | --- | --- | --- |
| C01. Exact root and continuous contact branch | Every height in [0.7070, 0.7072]; tighter root at 1/√2 | [Phase 04](../research/fractal_handover/fractal_research_04/RESEARCH_04.md), contact certificate and interval verifier. Computer-assisted claim. | Invertibility of preconditioner; inclusion and contraction on stated rectangles; consistency of large uniqueness box and smaller enclosure; continuous dependence. |
| C02. Connectedness and path connectedness | Whole interval | [Phase 04](../research/fractal_handover/fractal_research_04/RESEARCH_04.md); exact symmetry transports common periodic point. | Draft 0.2 includes a direct nested-connected-set proof. Path connectedness follows from Hata or Badger–Vellis Theorem 1.1 without OSC. The point contact is between infinite attractors. |
| C03. Octahedral first-level intersection graph | Whole interval | [Phase 06](../research/fractal_handover/fractal_research_06/RESEARCH_06.md), reflection-crossing inequalities, opposing-ball gap. Computer-assisted claim. | Crossing argument inside a connected piece; full coverage of 15 unordered pairs. Does not classify the intersections themselves. |
| C04. 2.1970 < Hausdorff dimension < 2.4150 | Whole interval | [Phase 05](../research/fractal_handover/fractal_research_05/RESEARCH_05.md), depth-eight packing, integer separation and tail estimates. Computer-assisted claim. | Strong separation of selected subsystem, its containment in K, and correct uniform parameter bounds. |
| C05. OSC failure for these six maps | Whole interval | [Phase 06](../research/fractal_handover/fractal_research_06/RESEARCH_06.md), equal-scale block maps sharing a fixed point. | Disjoint open-ball images and volume contradiction at every block depth. |
| C06. WSP failure and Assouad dimension 3 | Whole interval | [Phase 07](../research/fractal_handover/fractal_research_07/RESEARCH_07.md), rotation traces and distinct axes; [Phase 08 audit](../research/fractal_research_08/RESEARCH_08.md). Computer-assisted claim. | Closed subgroup classification; unbounded numbers of distinct **equal-length** block products; density of positive products; García Corollary 1.6(1). |
| C07. No alternative finite contracting-similarity IFS for K satisfies WSP or OSC | Whole interval | C04 + C06 and Fraser–Henderson–Olson–Robinson Theorem 1.4. Mathematical consequence. | Intrinsic dimension gap; full affine span. Scope excludes general nonlinear, affine or graph-directed presentations. |
| C08. Exact reference Hausdorff dimension and no finite word-map coincidences | h = 1/√2 only | [Phase 08](../research/fractal_research_08/RESEARCH_08.md), `verify_reference.py`, degree-432 polynomial. Computer-assisted claim. | Elimination and exclusion of spurious factors; irreducibility; complex conjugate transfer; projective cap argument; affine sign domination; Hochman Corollary 1.7. |
| C09. Exact second dimension and no finite word-map coincidences | The one member with u = 19/71 on the selected branch | [Phase 08](../research/fractal_research_08/RESEARCH_08.md), `verify_member.py`, finite-field matrices and degree-22 root isolation. Computer-assisted claim. | Recovered height belongs to certified branch; reduction after denominator clearing; first-letter cancellation over the reals; same theorem application. |
| C10. At least two bi-Lipschitz classes | The two members C08–C09 | Disjoint certified dimension intervals. Mathematical consequence. | Hausdorff dimension invariance. Does not imply pairwise inequivalence across the interval or distinct topological types. |
| C11. Central cylinder radius 0.0122 is clear and has an essential winding loop | Whole interval | [Phase 08](../research/fractal_research_08/RESEARCH_08.md), `verify_tunnel.py`, grid and half-plane clearance. Computer-assisted claim. | Connect exact contact points; control argument via branch-cut avoidance; concatenate six paths; winding homomorphism on full K. |
| C12. Two clear parallel lines and independent child loops | Whole interval | [Phase 09](../research/fractal_research_09/RESEARCH_09.md), all depth-eight centres, clearance (0.105, 0.118), half-plane margins and cross-child ball bounds. Computer-assisted claim. | Projected path-to-chord homotopy, orientation and identity winding matrix; no inference from a rendered path. |
| C13. Shrinking independent loops and product quotient of singular H1 | Whole interval; loops accumulate at six fixed points | [Phase 10](../research/fractal_research_10_topology/RESEARCH_10.md), four uniform wire bounds and sibling separation. Computer-assisted claim. | Full-set avoidance by induction; linking invariant for continuous loops; triangular detection; continuity and vanishing fixed-wire tails of infinite concatenations. Product is a **quotient**, not a group classification. |
| C14. Inherited bore radius 0.0058 is obstructed | Reference first travel [1.325115, 1.325120]; whole family [1.320, 1.330] | [Phase 10](../research/fractal_research_10_topology/RESEARCH_10.md), eventually periodic witnesses and exhaustive interval branch exclusions. Computer-assisted claim. | Nonempty compact minimisation set; all branches covered; reflected partner lobes. Does not decide a zero-width line hit. |
| C15. Specified Fragmentarium one-step branch maps cannot equal the Sixfold IFS up to global similarity and relabelling | Whole interval; the immutable cited shader version | [Prior-art argument](../research/fractal_research_11_prior_art/PRIOR_ART.md) and original shader source, rechecked for draft. Analytic comparison. | Signed-permutation relative traces versus interval (2.23, 2.24). Does not exclude identical attractors via different maps or grouped steps. |
| C16. No exact prior construction identified in the sources searched | Bounded search dated 17–18 November 2026 | [Original search](../research/fractal_research_11_prior_art/PRIOR_ART.md), [draft search supplement](literature-check.md). Literature observation, **not a theorem**. | Broaden expert search; recover maps from older visual examples; compare alternative presentations. No “first”, “unique” or new-topological-type claim. |

## Highest-priority review interfaces

1. Root isolation → exact definition and contact (C01–C03).
2. Rotation groups and same-length products → WSP/Assouad → intrinsic presentation obstruction (C05–C07).
3. Algebraic word distinction → Hochman hypotheses → two exact dimensions (C08–C10).
4. Complement geometry → singular homology, especially the infinite product quotient (C11–C13).
5. Source comparisons → carefully bounded originality statement (C15–C16).

## Explicitly open

- Exact Hausdorff dimension for every parameter; pairwise bi-Lipschitz classification of the curve.
- Full singular homology and fundamental groups; topological dimension; possible homeomorphism to the Menger sponge.
- Detailed structure of pairwise and higher intersections; behaviour away from the six special accumulation points.
- Exact intersection of the inherited zero-width tilted axes with the attractor.
- Maximal continuation interval and contact/topology bifurcations.
- Historical priority and possible equivalent descriptions in older art or mathematics.

These open problems do not turn the verified finite predicates into conjectures. Conversely, passed finite checks do not automatically settle their analytic consequences: that distinction is why both the manuscript arguments and this review register are included.
