# Lecture 4 — Span and linear independence

**Course:** MATH 235, Section 002  
**Source:** `[Section 002] Week 2.pdf`, PDF pp. 6–10  
**Course notes coverage:** part of §1.2 and §1.3.1

Here `F` means `R` or `C`. This lecture asks which vectors a set can produce and whether any members of the set are redundant.

## Definition 4.1 — Span (p. 6)

For a finite set `S = {v_1, ..., v_n} ⊆ V`, the **span** is the set of all linear combinations:

`Span(S) = {α_1 v_1 + ... + α_n v_n : each α_i ∈ F}`.

Its elements are **linear combinations** of the `v_i`. The lecture defines `Span(∅)={0}`.

## Remark 4.2 — Span of an arbitrary subset (p. 6)

For an arbitrary, possibly infinite, nonempty subset `S⊆V`, its span consists of all *finite* linear combinations of vectors in `S`. The convention `Span(∅)={0}` is unchanged.

## Example 4.3 — Lines and planes as spans (p. 7)

A line through the origin is `Span({v})` for nonzero `v`; a plane through the origin is `Span({v,w})` when `v∉Span({w})`.

## Proposition 4.4 — Span is the smallest containing subspace (p. 7)

`Span(S)` is a subspace of `V` and is contained in every subspace of `V` that contains `S`. The proof handles `S=∅` separately. For nonempty finite `S`, sums and scalar multiples of linear combinations are again linear combinations. Any subspace containing each `v_i` contains every `Σ_iα_i v_i` by closure.

## Definition 4.5 — Spanning set (p. 8)

`S` spans `V` when `Span(S)=V`.

## Example 4.6 — Polynomial spanning sets (p. 8)

`P_n(F) = Span({1, x, ..., x^n})`. The lecture also shows that `{1, 1+x, x+x^2}` spans `P_2(F)` by writing any `α_0 + α_1 x + α_2 x^2` as

`(α_0 - α_1 + α_2)·1 + (α_1 - α_2)(1+x) + α_2(x+x^2)`.

## Exercise 4.7 — Spanning matrix subspaces (p. 8)

Find spanning sets for upper triangular `U_n(F)` and diagonal `D_n(F)` inside `M_n(F)`; consider the smallest possible numbers of spanning matrices.

## Definition 4.8 — Linear independence (pp. 8–9)

`S = {v_1, ..., v_n}` is **linearly independent** if the only way to get `α_1 v_1 + ... + α_n v_n = 0` is with every coefficient `α_i = 0`.

Otherwise it is **linearly dependent**. The empty set is declared independent.

## Example 4.9 — Polynomial independence and dependence (p. 9)

- `{1,x,x^2}` is independent in `P_2(F)` because a zero polynomial has every coefficient zero.
- `{1,3x,1-2x,4x^2-2x+1}` is dependent: coefficients `(1,-2/3,-1,0)` give a nontrivial zero combination.

## Proposition 4.10 — Redundancy criterion (pp. 9–10)

For `n ≥ 2`, `{v_1, ..., v_n}` is dependent exactly when one vector can be expressed as a linear combination of the others. From a nontrivial zero combination, solve for a vector with a nonzero coefficient. Conversely, moving an expression of one vector in terms of the others to one side gives a nontrivial zero combination.

## Example 4.11 — Dependent coordinate vectors (p. 10)

In `F^2`, `(1,0)^T=(1/2)(1,1)^T+(1/2)(1,-1)^T`, so `{(1,0)^T,(1,1)^T,(1,-1)^T}` is dependent.

## Example 4.12 — The zero vector is dependent (p. 10)

For any vector space `V`, `{0}` is dependent since `1·0=0` is a nontrivial relation.

## Exercise 4.13 — Classify independent and dependent sets (p. 10)

Classify each set as independent or dependent, with justification:

1. `{(1,-2)^T,(4,-6)^T}` in `R^2`.
2. `{1,1+x,1-x}` in `P(F)`.
3. `{[[1, 0], [0, 1]], [[2, 1], [0, 3]], [[0, 1], [0, 1]]}` in `M_2(R)`. Each inner list is a matrix row.

## Source checks

No mathematical discrepancy was found in this lecture during the 2026-10-08 page-by-page audit. The two polynomial sets on p. 9 both belong to Example 4.9; Examples 4.11 and 4.12 appear after Proposition 4.10 on p. 10. They are kept as separate numbered units here.
