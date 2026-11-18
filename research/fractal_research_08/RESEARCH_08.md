# The six-copy spatial fractal has an exact reference dimension and a through-hole

17 November 2026

## Results and research direction

Keep the connected family from the handover. For its original reference member at \(h=1/\sqrt2\), the argument below gives

\[
\dim_H K=\frac{\log 6}{\log(1/r)}=2.41489145862753938\ldots,\qquad \dim_A K=3 .
\]

Here \(r\) is the exact scale isolated by the phase-04 contact equations. The Hausdorff equality is a new computer-assisted deduction for this project. It holds despite the known contacts and arbitrarily close relative maps. A second member at \(\tan(\alpha/2)=19/71\) has a shorter proof and has Hausdorff dimension \(2.41490523458681800\ldots\). The uniform Hausdorff bounds from phase 05 still apply to the rest of the certified curve.

There is also a geometric result for **every** member on that curve. A vertical cylinder of radius 0.0122 passes through the centre without meeting the set. A closed path in the set winds once around that cylinder. This upgrades the earlier empty-ball certificate to a through-hole with an essential loop. The illustration uses finite word centres. The proof covers the infinite tail.

**Next investigation.** Test which holes in the six smaller copies survive in the full attractor. Each copy contains a scaled version of the loop, but neighbouring pieces could fill or bridge it. Start with two candidate lines through child copies. Enclose all cylinders of the parent near each line, using the integer bounds below. If both lines miss the entire parent, compute the winding of two loops about both lines. A winding matrix of rank two proves two independent loop classes. Finite pictures can nominate directions for this test. A failed straight-line test would leave open a winding witness with a curved passage.

For historical comparison, start with the six half-scale copies of the Sierpiński octahedron, then compare rotated, overlapping similarity constructions. Record the maps, contact mechanism, separation properties and proved topology for each comparison. The combination to search for here is alternating tangent-axis rotations, a shared periodic point and a Hausdorff–Assouad dimension gap. Historical priority and equivalence to the Menger sponge as a topological space are open. The new deduction would benefit from independent review before a publication or discovery claim. [Bourke’s polyhedral fractals](https://paulbourke.net/fractals/polyhedral/index.html) · [Bandt’s overlapping rotational constructions in the plane](https://doi.org/10.3390/fractalfract6010039)

## Audit of the starting argument

The packaged manifest covers 110 files. The original verifier passed on Windows with Python 3.12 and the pinned dependencies, including both depth-eight integer packings, the interval contact and rotation checks, and the first-level contact classification. The receipt is in **handover_check.json**.

- The two distinct eight-letter words fix the same point \(p\) and have equal contraction \(q=r^8\). A feasible open ball for the open set condition would yield \(2^m\) disjoint balls of radius proportional to \(q^m\) inside a ball about \(p\) also of radius proportional to \(q^m\). Comparing volumes rules this out.
- The two block rotations have different axes and certified angles between zero and 60 degrees. Among the proper closed subgroups of \(SO(3)\), the axis-preserving groups cannot contain both, and the polyhedral groups have minimum nonzero angle at least 72 degrees. The same argument applies to the local rotations. Compactness gives density of positive products in the group closure. [Olive, §3](https://arxiv.org/pdf/1709.01776)
- At a common block length there are unboundedly many distinct rotations. For conjugate infinite-order generators \(A,B\), equality between two of \(A^{m-j}B^j\) forces the same nonidentity power about two distinct axes. In the finite-order case of common order \(N\), the positive words cover an infinite group. Infinitely many distinct elements have representative lengths in one residue class modulo \(N\), so arbitrarily large finite selections can be padded to a common length by \(A^N\). Compactness now supplies distinct rotations \(C,D\) arbitrarily close together. Their relative word map is \(x\mapsto p+C^{-1}D(x-p)\). This proves failure of weak separation.
- Four noncoplanar fixed points give full affine span. García’s corollary then gives Assouad dimension 3. The strict upper bound on Hausdorff dimension and the Fraser–Henderson–Olson–Robinson theorem also exclude a weakly separated finite similarity presentation of the same set. These conclusions hold throughout the original curve. [García, Corollary 1.6(1)](https://arxiv.org/pdf/1909.03148) · [Fraser et al., Theorem 1.4](https://arxiv.org/pdf/1404.1016)

## 1. Reduce the six maps to three rotations and a sign

Write \(G_k(x)=rQ_kx+t_k\) with the handover’s convention that the first letter is outermost. The exact identities are \(Q_{k+3}=Q_k\) and \(t_{k+3}=-t_k\). The three oriented rotation axes for residues \(0,1,2\) are horizontal and spaced by 120 degrees. All translations have length \(L=\sqrt{1+h^2}\).

Suppose the rotation products determine their sequence of residues modulo 3. Two equal affine word maps must have equal length by their contraction ratios, and then the same residue sequence by their linear parts. If their signs first differ at position \(j\), counting from zero, the difference in translations has a term of length \(2Lr^j\). The sum of the lengths of all later differences is at most \(2Lr^{j+1}/(1-r)\). This is strictly smaller because \(r<1/2\). Thus it suffices to distinguish the three rotation letters at every length.

## 2. Find the algebraic conjugate of the reference tilt

Write \(u=\tan(\alpha/2)\), and use coordinates \((x,\sqrt3 y,z)\). All three rotation matrices then have entries in \(\mathbb Q(u)\). The verifier checks the coordinate transformation symbolically against the original Rodrigues formula for each of the six maps. The contact point is \(\lambda v\), where \(v=(1,1,0)\) in these coordinates.

Let \(D=2(1+u^2)\). Write the translation of the original eight-letter word in scaled coordinates as \(c_0+h c_1\) and its rotation there as \(Q_W\). Clearing denominators gives three columns with integer polynomial entries in \(r,u\).

\[
a=D^8(v-r^8 Q_Wv),\qquad b=2D^8c_0,\qquad d=2D^8c_1 .
\]

At the shared point \(2\lambda a=b+h d\). Taking triple and cross products eliminates \(\lambda\).

\[
a\cdot(b\times d)=0,\qquad 2(a\times b)_y^2-(a\times d)_y^2=0 .
\]

The second equation uses \(h^2=1/2\). Removing integer content and powers 17 and 16, respectively, of \(1+u^2\) leaves bidegrees \((22,14)\) and \((30,32)\) in \((r,u)\). Their resultant in \(r\) has degree 1094. Its integer factors have the following degrees and multiplicities.

| Degree | 1 | 2 | 182 | 432 |
|---|---:|---:|---:|---:|
| Multiplicity | 46 | 126 | 2 | 1 |

Outward interval evaluation on the original tilt box excludes zero for the factors of degrees 1, 2 and 182. Thus the degree-432 polynomial \(f\) vanishes at the exact reference \(u\). The stored coefficient list is **reference_tilt_polynomial.json**. The verifier reconstructs it from the word and checks the factorization by multiplication. A second irreducibility check uses squarefree reductions at 7, 13, 37 and 43, each preserving degree. At each prime a rational factor would have degree equal to a subset sum of the irreducible factor degrees modulo that prime. The four subset-sum sets have only 0 and 432 in common. The modular degrees are computed by Frobenius powers and polynomial gcds.

The first bivariate equation still gives a nonzero polynomial in \(r\) after specialization at \(u\). Its nonzero coefficients in \(u\) have degree at most 14, hence cannot vanish at an algebraic number of degree 432. This also proves the reference scale \(r\) is algebraic.

There is a root \(\zeta\) of \(f\) in the disk of radius \(10^{-10}\) about
\(-0.028547283375+1.138685386817\,i\). For an exact existence check, substitute the centre plus \(10^{-10}w\) in \(f\) and clear the denominators. On \(|w|=1\) the linear coefficient has modulus over 100 times the sum of the moduli of all other coefficients. The code obtains this strict bound by Gaussian integer arithmetic, bounding each modulus above by the sum of the absolute components and the linear modulus below by its largest absolute component. Rouché’s theorem gives one root in the disk. Irreducibility makes it a conjugate of the actual reference \(u\).

## 3. Read the first rotation from a spherical cap

Any matrix identity between the rotation words at \(u\) also holds at \(\zeta\), since the scaled-coordinate matrices are rational functions over \(\mathbb Q\) and \(1+\zeta^2\ne0\). Conjugate the coordinate change back and express the rotations projectively on \(\mathbb{CP}^1\). In detail, for a real unit axis \(a\) take \(L_a(z)=I-i z(a\cdot\sigma)\), where \(\sigma\) denotes the three Pauli matrices. Conjugation by \(L_a(z)\) on the traceless matrices implements the complex Rodrigues rotation \(Q_a(z)\). The verifier checks this identity on all three basis matrices. If two rotations agree, their lifts induce the same conjugation, so the two lifts differ by a scalar and have the same projective action.

Under the unit-sphere description of \(\mathbb{CP}^1\), the two eigenlines of \(a\cdot\sigma\) are antipodal points \(+a,-a\). For a spinor making spherical angle \(\delta\) from \(+a\), the absolute ratio of its minus to plus coordinates in the orthonormal eigenbasis is \(\tan(\delta/2)\). The action of \(L_a(\zeta)\) multiplies this ratio by

\[
t=\left|\frac{1+i\zeta}{1-i\zeta}\right|<0.067< (2-\sqrt3)^2=\tan^2(15^\circ).
\]

Use the three disjoint closed spherical caps of radius 30 degrees around the three positive axes. Every point of their union is at least 30 degrees from each negative axis. Its ratio in the basis for any one axis is therefore at most \(\cot(15^\circ)\). After applying that axis’s generator, the ratio is strictly less than \(\tan(15^\circ)\). Each generator sends the **entire union** into the interior of its own cap. Consequently the image of any test point in the union identifies the first letter of a nonempty word. Equal words as transformations must start with the same letter. Cancel its invertible generator and repeat. This argument covers every word length. Section 1 then gives freeness for the six real affine maps.

The reference system now meets Hochman’s hypotheses. All map coefficients are algebraic, the dense rotation group acts linearly irreducibly, the attractor spans space, and distinct finite words give distinct maps. The similarity dimension is below three. Corollary 1.7 gives the claimed Hausdorff equality. The periodic addresses from phase 04 still give the same *point*, which is consistent with distinct word *maps*. [Hochman, Corollary 1.7](https://arxiv.org/pdf/1503.09043)

## 4. A simpler second example

Choose \(u=19/71\) and solve for \(r,h\) on the same contact curve. The degree-22 determinant in \(r\) isolates a simple root near \(0.47618040162277722027\). An invertible two-row subsystem gives \(h\) by Cramer’s rule, and the determinant enforces the remaining row. An exact rational enclosure puts \(h\) near \(0.70714070075078310161\), inside the original height interval. The new scale and tilt lie inside the original uniqueness rectangle. Both \(r\) and \(h\) are algebraic.

Multiply the scaled-coordinate rotation matrices by \(71^2+19^2=5402\) before reducing their entries modulo 37. The resulting rank-one matrices have three distinct image lines, spanned by \((1,0,31)\), \((1,3,12)\) and \((1,34,12)\). All nine two-letter products are nonzero. For rank-one maps this means no generator kills the image line of any generator. Induction shows that every product is nonzero and has its first generator’s image line. Equal-length rotation products over the reals would remain equal after clearing the common denominator and reducing. The image line identifies the first generator and one then cancels it over the reals. Section 1 and Hochman give the second member’s dimension. This shorter example can be checked separately using **verify_member.py**.

## 5. A tunnel and a loop around it

Use the verified phase-05 depth-eight word centres on the integer grid \(Q=2^{29}\). For the first piece \(G_0(K)\), the smallest integer \(x\) is 3,049,454, and the smallest squared horizontal radius is 97,951,509,407,090. Every actual point lies within \(\varepsilon=0.00055+2.14(0.476186)^8\) of its grid centre in physical coordinates. Since every centre has positive \(x\), its distance to the vertical half-plane \(x\le0,\ y=0\) equals its horizontal radius. The exact squared inequality in **verify_tunnel.py** gives a distance greater than 0.0122 after subtracting \(\varepsilon\). Rotating and reflecting the six pieces proves that the entire set avoids the cylinder about the vertical axis.

The certified adjacent contact \(p\) lies on the ray at azimuth \(30^\circ\). Its prefix 01 gives positive \(x\) even after the tail allowance. The adjacent contact \(T^{-1}p\) is at \(-30^\circ\), where \(T\) is the handover’s 60-degree rotation with a vertical reflection. Both contacts belong to \(G_0(K)\). A connected self-similar attractor is path-connected, so join them in \(G_0(K)\). Its avoidance of the half-plane allows a continuous principal argument on that entire path. The argument increases by exactly 60 degrees between its endpoints. Concatenate the six images of the path under \(T^j\), \(0\le j<6\). This yields a closed path of winding number one about the axis. Radial projection of \(K\) into the circle preserves this winding, so the loop cannot contract to a point in \(K\). This gives one essential loop, and leaves the number and arrangement of independent tunnels open. [Hata, *On the structure of self-similar sets*](https://doi.org/10.1007/BF03167083)

## Reproduction

Run these commands from the workspace folder that contains both **fractal_handover** and **fractal_research_08**. The historical scripts use temporary copies for scientific checks. Phase 08 uses Python 3.12, the handover’s pinned dependencies and python-flint 0.9.0 for the reference elimination. The exact factor and complex-disk checks take seconds on the tested computer.

~~~powershell
uv run --isolated --python 3.12 --with-requirements fractal_handover/requirements.txt python -B fractal_handover/verify_handover.py
uv run --isolated --python 3.12 --with-requirements fractal_handover/requirements.txt --with python-flint==0.9.0 python -B fractal_research_08/verify_reference.py
uv run --isolated --python 3.12 --with-requirements fractal_handover/requirements.txt python -B fractal_research_08/verify_member.py
uv run --isolated --python 3.12 --with-requirements fractal_handover/requirements.txt python -B fractal_research_08/verify_tunnel.py --render
~~~

The programs check the exact algebra, interval inequalities and geometry predicates. The all-length argument, the application of the dimension theorems and the winding deduction are mathematical arguments given above. Independent mathematical review is outstanding.
