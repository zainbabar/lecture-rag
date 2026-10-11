# Week 3 — Practice problems

**Source:** `[Section 002] Week 3.pdf`, PDF pp. 19–20. These questions follow Lecture 8 and are separate from numbered lectures. No solutions are added here.

## P1 — An idempotent basis (p. 19)

A matrix `E∈M_2(F)` is idempotent when `E^2=E`. Find a basis `{E_1,E_2,E_3,E_4}` of `M_2(F)` consisting entirely of idempotents.

## P2 — Polynomial symmetry (p. 19)

In `P_2(R)`, let `U={p:p(1-x)=p(1+x)}`. Verify `U` is a subspace, find a basis, and use it to compute `dim(U)`.

## P3 — Coordinates in three bases (p. 19)

For `p(x)=a+bx+cx^2+dx^3∈P_3(F)`, find `[p]_B` for each ordered basis below. The PDF permits assuming these are bases.

1. `(1,1+x,x+x^2,x^2+x^3)`.
2. `(1,x,x^2-1,x^3-3x)`.
3. `((1-x)^3,3x(1-x)^2,3x^2(1-x),x^3)`.

## P4 — Parameterized vectors (p. 19)

For a real parameter `x`, let `S={(x,1,1)^T,(1,x,1)^T,(1,1,x)^T}⊆R^3`. Determine when `S` is dependent and compute the dimension of its span for each such `x`.

## P5 — Polynomial spanning (p. 20)

Determine whether `{x^3+x^2+x+1,x^3+2x^2+x,2x^3+3x^2+2x+1,x^3+x^2+2x+1}` spans `P_3(F)`.

## P6 — Independence and linear images (p. 20)

Let `T:V→W` be linear; the spaces need not be finite-dimensional. Choose distinct `v_1,...,v_n∈V` and set `w_i=T(v_i)`.

1. Show that if `w_1,...,w_n` are distinct and `{w_1,...,w_n}` is independent, then `{v_1,...,v_n}` is independent.
2. If `{v_1,...,v_n}` is independent, must `{w_1,...,w_n}` be independent? Prove it or give a counterexample.

## Source checks

The page-by-page check on 2026-10-08 found no mathematical discrepancies. P6 requires distinct image vectors in part 1, as stated above. Plain-text notation replaces the earlier LaTeX formatting.

P4 repeats Week 2 P7 with column-vector notation. At `x=1`, all three displayed vectors are equal. A literal set removes repetitions, whereas an indexed three-vector family retains them; check which meaning is intended before using that case as a gold label.
