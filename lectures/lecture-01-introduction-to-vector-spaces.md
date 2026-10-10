# Lecture 1 — Introduction to vector spaces

**Course:** MATH 235, Section 002  
**Source:** `[Section 002] Week 1.pdf`, PDF pp. 1–5  
**Course notes coverage:** part of §1.1

These are structured lecture notes, preserving the definitions, numbered examples, and exercise. The PDF remains the authority for exact wording. Here `F` means either the real numbers `R` or the complex numbers `C`; `(a_1, ..., a_n)^T` denotes a column vector.

## From coordinate vectors to abstract vectors (pp. 1–2)

A vector in three-dimensional geometry can be represented by an ordered triple in `R^3`. This generalizes to `n`-tuples in `R^n` or `C^n`.

For `u = (a_1, ..., a_n)^T` and `v = (b_1, ..., b_n)^T` in `F^n`, and a scalar `α` in `F`:

- Addition: `u + v = (a_1 + b_1, ..., a_n + b_n)^T`.
- Scalar multiplication: `αu = (αa_1, ..., αa_n)^T`.
- The dot product **as printed in the PDF**: `u · v = a_1 b_1 + ... + a_n b_n`.

The lecture first studies what follows from addition and scalar multiplication alone. Length, angle, and orthogonality require the later introduction of an inner product.

## Definition 1.1 — Vector space (pp. 2–3)

A vector space over `F` is a set `V` with operations `+ : V × V → V` and scalar multiplication `F × V → V`. Thus both operations take their values in `V`. For vectors `u`, `v`, `w` in `V` and scalars `α`, `β` in `F`, these eight axioms must hold:

| Label | Axiom |
| --- | --- |
| A1 | Addition is associative: `u + (v + w) = (u + v) + w`. |
| A2 | There is a unique zero vector `0` with `v + 0 = 0 + v = v`. |
| A3 | Every `v` has a unique additive inverse `-v` with `v + (-v) = (-v) + v = 0`. |
| A4 | Addition is commutative: `u + v = v + u`. |
| M1 | Scalar multiplication is associative: `α(βv) = (αβ)v`. |
| M2 | The scalar one acts as identity: `1v = v`. |
| D1 | `α(u + v) = αu + αv`. |
| D2 | `(α + β)v = αv + βv`. |

Elements of `V` are **vectors**; elements of `F` are **scalars**.

## Remark 1.2 — Notation and uniqueness (p. 3)

The scalar-multiplication dot can be omitted when unambiguous. Subtraction means `u-v=u+(-v)`. Associativity lets us omit parentheses in sums and nested scalar multiplication. The lecture asks the reader to check the uniqueness claims for the zero vector and additive inverses.

## Example 1.3 — `F^n` (pp. 3–4)

Coordinate-wise addition and scalar multiplication make `F^n` a vector space; its zero vector is `(0,...,0)^T`. The lecture explicitly verifies A1 and M1 in `F^2` using coordinates and asks the reader to check the remaining axioms, then all eight for `F^n`.

## Remark 1.4 — Choice of scalar field (p. 4)

`C^n` is also a vector space over `R` if scalars are restricted to `R`. Unless stated otherwise, `F^n` is treated as a vector space over `F`.

## Example 1.5 — Matrix space (p. 5)

`M_(m×n)(F)` is the set of `m × n` matrices with entries in `F`. Entry-wise addition and scalar multiplication give it a vector-space structure. If `A = [a_ij]` and `B = [b_ij]`, then `A + B = [a_ij + b_ij]` and `αA = [αa_ij]`.

Its zero vector is the zero matrix `O_(m×n)`.

## Exercise 1.6 — Sequence space (p. 5)

Let `F^∞` be all sequences `(x_k)` for `k = 1, 2, ...`, with every `x_k` in `F`. Show it is a vector space under component-wise operations:

- `(x_k) + (y_k) = (x_k + y_k)`.
- `c(x_k) = (cx_k)` for any scalar `c` in `F`.

## Source checks

The PDF's dot-product formula on p. 2 is `a_1 b_1 + ... + a_n b_n`. This note preserves that printed formula; it does not substitute the conjugate-symmetric inner product used in some contexts over `C`.
