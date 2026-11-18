# Literature check for the first paper draft

Checked 18 November 2026, supplementing the [17 November repository search](../research/fractal_research_11_prior_art/PRIOR_ART.md). This is a focused verification of theorem statements and the nearest known comparisons, not an exhaustive search or a priority certificate.

## External theorems used

| Source | What was checked / how used |
| --- | --- |
| [Hutchinson, 1981](https://iumj.org/article/2972/) and [author's text](https://maths-people.anu.edu.au/~john/Assets/Research%20Papers/fractals_self-similarity.pdf) | Attractor/OSC framework; title, pages and correct DOI ending **30055**. |
| [Hata, 1985](https://doi.org/10.1007/BF03167083) | Connectedness and path connectedness; bibliographic metadata and the connected-IFS consequence cross-checked in [Badger–Vellis, original research introduction and bibliography](https://arxiv.org/abs/1910.08850). Hata's publisher full text was not accessible in this check; direct inspection of the original theorem should be part of independent review. |
| [Hochman, arXiv:1503.09043v2](https://arxiv.org/abs/1503.09043v2) | Read Corollary 1.7 in the PDF: algebraic coefficients, irreducibility, no exact overlaps. The draft cites this version explicitly; no unverified journal metadata added. |
| [García, arXiv:1909.03148v2](https://arxiv.org/abs/1909.03148v2) | Read Corollary 1.6(1): WSP failure and density of positive orthogonal products give full Assouad dimension under the ambient-span setup. |
| [Fraser et al., arXiv:1404.1016v2](https://arxiv.org/abs/1404.1016v2) | Read Theorem 1.4, WSP implies equality of Hausdorff and Assouad dimensions for full-span attractors. Published citation: *Advances in Mathematics* 273 (2015), 188–214. |
| [Olive, arXiv:1709.01776v4](https://arxiv.org/abs/1709.01776v4) | Closed subgroup classification of SO(3), Section 3, used in the rotation argument. |
| [Hatcher, *Algebraic Topology*](https://pi.math.cornell.edu/~hatcher/AT/AT-doublepage.pdf) | Located Example 1.25, the shrinking wedge of circles. Cited as context for the classical infinite-loop mechanism, not as a theorem identifying Sixfold's homology. |

## Construction comparisons

- [Kunnen–Schlicker, *Regular Sierpinski Polyhedra*](https://www.pme-math.org/journal/issues/PMEJ.Vol.10.No.8.pdf): journal text indexed for the construction; title/byline and date/pages cross-checked against the [authors' institution](https://www.gvsu.edu/mathhistory/articles-and-book-chapters-1996-to-2000-140.htm). The whole issue exceeded the browser's full-PDF size limit. The octahedral maps and dimension comparison are stated explicitly in the draft.
- [Fragmentarium immutable shader](https://github.com/Syntopia/Fragmentarium/blob/14130ad5dcf8024868e7e2d34c64d911329fd83c/Fragmentarium-Source/Examples/Kaleidoscopic%20IFS/Octahedron.frag): original source fetched through GitHub; its fold operations are signed coordinate exchanges, with common rotations before and after. The relative-trace distinction concerns only literal one-step branch rules.
- [Tsuiki, Bridges 2007](https://archive.bridgesmathart.org/2007/bridges2007-277.html), [Fathauer–Kaczmarski–Duchnowski, Bridges 2008](https://archive.bridgesmathart.org/2008/bridges2008-289.html): original proceedings records checked. The latter has three authors, all credited in the manuscript.
- [Tetenov–Kamalutdinov–Vaulin, spatial Jordan arc](https://arxiv.org/abs/1512.00290v2) and [Kamalutdinov–Tetenov, one-point contact example](https://arxiv.org/abs/1809.08595v2): original preprint records checked. The author order for the arc follows the cited arXiv record.
- [Broomhead–Montaldi–Sidorov, golden gaskets](https://arxiv.org/abs/math/0309304), [Bandt–Mekhontsev, irrational-rotation carpets](https://doi.org/10.3390/fractalfract6010039): original records checked. These establish relevant overlapping-family and computer-search precedents, not a matching spatial construction.

## Additional precedent found while drafting

[Bárány and Verma, *Hausdorff dimension of self-similar measures and sets with common fixed-point structure*](https://doi.org/10.1017/etds.2026.10342), published online 23 September 2026, first posted as [arXiv:2507.05835](https://arxiv.org/abs/2507.05835) on 8 July 2025. The v2 PDF (July 2026) introduction and common-fixed-point setup were inspected.

This paper studies systems on the real line with some maps sharing fixed points, and dimension/separation for natural parameters. On the line, two similarities about the same fixed point commute, creating exact word overlaps. Sixfold's two common-fixed-point block maps have different spatial rotation axes, and the two algebraic Sixfold members have no coincident finite word maps. This is a concrete distinction; it does not make the shared-fixed-point idea itself new. The source is now included in the draft's originality section and bibliography.

## Limits of the claim

The search supports “no exact matching construction identified in the sources examined.” It does not establish “first,” “unique,” a new topological type, or absence of an older equivalent description. Informal artwork with unavailable formulas, differently grouped iterations and alternative IFS presentations remain the largest comparison gaps. Independent expert review should also decide whether other recent dimension or overlap results narrow these gaps.
