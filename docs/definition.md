# Exact definition

Sixfold is the working name for the connected spatial family described here.
The reference member has height $h=1/\sqrt{2}$. All coordinates are dimensionless.

## The six similarities

For $k\in\{0,1,2,3,4,5\}$, set

$$
\begin{aligned}
\phi_k&=\frac{k\pi}{3},\qquad \sigma_k=(-1)^k,\\
a_k&=(-\sin\phi_k,\cos\phi_k,0),\\
t_k&=(\cos\phi_k,\sin\phi_k,\sigma_k h).
\end{aligned}
$$

Use column vectors and the right-handed rotation $R_a(\beta)$ about unit axis $a$,

$$
R_a(\beta)x=\cos\beta\,x+(1-\cos\beta)(a\cdot x)a+\sin\beta\,(a\times x).
$$

With $u=\tan(\alpha/2)$, define

$$
\begin{aligned}
G_k(x)&=rR_{a_k}(\sigma_k\alpha)x+t_k,\\
\cos\alpha&=\frac{1-u^2}{1+u^2},\qquad
\sin\alpha=\frac{2u}{1+u^2}.
\end{aligned}
$$

The attractor $K(h)$ is the unique nonempty compact subset of $\mathbb R^3$
satisfying

$$
K(h)=\bigcup_{k=0}^{5}G_k(K(h)).
$$

The maps are strict contractions since the selected $r$ lies between zero and
one. Existence and uniqueness follow from the contraction theorem for finite
iterated function systems. [Hutchinson, *Fractals and self-similarity*](https://doi.org/10.1512/iumj.1981.30.30025)

## The exact contact condition

For a word $w=k_1\ldots k_n$, write
$G_w=G_{k_1}\circ\cdots\circ G_{k_n}$. The first digit is the outermost map.
Applying the word to a point proceeds from right to left.

Take $W=01153513$. Write $G_W(x)=M_Wx+c_W$ and its fixed
point as $p=(I-M_W)^{-1}c_W$. Solve

$$
F_1(r,u,h)=-\frac{p_x}{2}+\frac{\sqrt3\,p_y}{2}=0,\qquad
F_2(r,u,h)=p_z=0.
$$

These place $p$ on the fixed axis of the half-turn

$$
S=\begin{pmatrix}
1/2&\sqrt3/2&0\\
\sqrt3/2&-1/2&0\\
0&0&-1
\end{pmatrix}.
$$

The symmetry $SG_kS^{-1}=G_{(1-k)\bmod6}$ makes $W'=10024204$ the partner
word. Its map fixes exactly the same $p$. Repeating either word forever gives
that common point.

## Selecting the reference root

The following terminating decimals define rational **box centres**,

    r_c = 0.476178386161547669525964558546828831852499529292214482
    u_c = 0.2676240856235760042362757034639861560899940849527665828

At exact $h=1/\sqrt2$, take the unique solution of $F_1=F_2=0$ in

$$
|r-r_c|\le10^{-25},\qquad |u-u_c|\le10^{-25}.
$$

The interval certificate establishes existence and uniqueness in this box.
The displayed decimals approximate the solution. The equations and the box
define it exactly. Its tilt is approximately $29.965238257844163^\circ$.
[Contact certificate](../research/fractal_handover/fractal_research_07/positive_contact_certificate.json) · [Interval verification](../research/fractal_handover/fractal_research_07/certify_witness.py)

## Selecting the family

For every real $h\in[0.7070,0.7072]$, use the unique solution of the same two
equations in

$$
|r-r_c|\le0.001,\qquad |u-u_c|\le0.001.
$$

Uniform interval contraction establishes this family of solutions. Sharper
certificates give $|r-r_c|\le0.000007$ and $|u-u_c|\le0.000060$.
Height is the free parameter. Scale and tilt are selected by the contact
condition. [Uniform certificate](../research/fractal_handover/fractal_research_07/family_box.py) · [Handover](../research/fractal_handover/HANDOVER.md)

A second exactly specified member fixes $u=19/71$ and selects the contact
solution with $0.476171<r<0.476186$ and $0.7070<h<0.7072$.
The verifier isolates a unique simple root of its degree-22 elimination
polynomial in that scale interval and reconstructs height. Its values are approximately
$h=0.70714070075078310161$ and $r=0.47618040162277722027$.
[Algebraic isolation](../research/fractal_research_08/verify_member.py)

## Finite approximations

At depth $n$, the word centres $G_w(0)$ for all $6^n$ words give a finite
approximation. Every point in $G_w(K)$ is within $2.14r^n$ of its
exact word centre, using the enclosing radius 2.14. Floating-point
generation also introduces rounding error. The certified tunnel and dimension
calculations use their own outward error bounds.

The reference generator reuses the recorded six-map implementation. Its output
contains x, y and z coordinates ordered by the base-six word index.
A depth-eight output contains 1,679,616 centres.
[Generator](../scripts/generate.py) · [Original maps](../research/fractal_handover/fractal_research_07/geometry.py)

See [results](results.md) for the properties established by the project's
computer-assisted arguments and their review status.
