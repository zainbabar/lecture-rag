# Lecture 2 — More examples and vector space properties

**Course:** MATH 235, Section 002  
**Source:** `[Section 002] Week 1.pdf`, PDF pp. 6–10  
**Course notes coverage:** part of §1.1

Here `F` means `R` or `C`, `P(F)` is the space of polynomials over `F`, and `P_n(F)` contains those of degree at most `n`. See the source check for PDF wording that appears inconsistent.

## Definition 2.1 — Polynomials (p. 6)

A polynomial over `F` is a symbolic expression `p(x) = a_0 + a_1 x + ... + a_n x^n`, where `n ≥ 0`, `x` is an indeterminate, and each coefficient `a_j` is in `F`. If every coefficient is zero, `p` is the **zero polynomial**.

For nonzero `p`, `deg(p)` is the largest `j` with `a_j ≠ 0`. The lecture defines `deg(0) = -∞`. Examples: `deg(2x - 1) = 1`, `deg(3x^3 - 5x^2 + 4) = 3`, and `deg(2) = 0`.

## Example 2.2 — Polynomial vector space (pp. 6–7)

`P(F)` contains all polynomials over `F`. Addition combines like powers; scalar multiplication multiplies each coefficient. For example:

`(1 - 2x + 3x^2) + (-2 + 4x - x^2 + 7x^3) = -1 + 2x + 2x^2 + 7x^3`.

These operations make `P(F)` a vector space, with the zero polynomial as its zero vector.

## Example 2.3 — Polynomials of bounded degree (p. 7)

For a fixed `n ≥ 0`, `P_n(F) = {polynomials in P(F) with degree ≤ n}` is also a vector space under the operations from Example 2.2. The lecture often writes `P_0(F)` simply as `F`.

## Remark 2.4 — Polynomials are formal expressions (pp. 7–8)

The lecture warns against identifying a polynomial with the function it induces on `F`. Later, polynomial expressions will be evaluated at matrices. Over the field `Z/3Z`, the nonzero polynomial `x^3-x` evaluates to zero at every field element. This course otherwise works over `R` or `C`.

## Example 2.5 — Continuous functions (p. 8)

`C([0,1])`, the continuous real-valued functions on `[0,1]`, is a vector space over `R` with pointwise operations: `(f + g)(x) = f(x) + g(x)` and `(αf)(x) = αf(x)`.

Its zero vector is the constant zero function.

## Example 2.6 — Zero vector space (p. 8)

The **zero vector space** `{0}` over `F` has one element and operations `0+0=0` and `α0=0` for all `α∈F`.

## Proposition 2.7 — Cancellation laws (pp. 8–9)

For `u,v,w∈ V` and `α∈F`:

1. If `u+v=u+w`, then `v=w`.
2. If `α u=α v` and `α≠0`, then `u=v`.

For the first, add `-u` to both sides and use the vector-space axioms. For the second, multiply both sides by `1/α`. The lecture gives these manipulations in its proof.

## Exercise 2.8 — A vector equation (p. 9)

Show that `v+3x=w` has a unique solution `x` for any `v,w` in a vector space `V` over `F`.

## Exercise 2.9 — Zero and negation identities (p. 9)

Prove `0v=0` for every `v∈V`, `(-1)v=-v`, and `α0=0` for every `α∈F`; explain why they make sense.

## Exercise 2.10 — An unusual vector space (p. 10)

On the positive real numbers `V = R_(>0)`, define a new addition `x ⊕ y = xy` and scalar multiplication `α ⊙ x = x^α`. Prove these operations make `V` a vector space over `R`.

The lecture calls `F^n`, `P(F)`, `P_n(F)`, `M_(m×n)(F)`, and `C([0,1])` its common examples, contrasting them with the less familiar structure in Exercise 2.10.

## Source checks

On PDF p. 6, one expanded expression for `q(x)` appears to start with `b_1 + b_1 x` after previously defining its constant coefficient as `b_0`. The notes use `b_0` as the constant coefficient, following the definition.
