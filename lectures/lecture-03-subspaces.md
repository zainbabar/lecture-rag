# Lecture 3 — Subspaces

**Course:** MATH 235, Section 002  
**Source:** `[Section 002] Week 2.pdf`, PDF pp. 1–5  
**Course notes coverage:** part of §1.2

Here `F` means `R` or `C`, and `P(F)` is the polynomial vector space from Lecture 2.

## Motivation: lines and planes through the origin (p. 1)

A line in `R^n` has the form `L={u+tv:t∈R}` for nonzero direction `v`. A plane has the form `P={u+sv+tw:s,t∈R}` for two independent directions `v,w`. When `u=0`, these become `{tv}` and `{sv+tw}`, and each is itself a vector space under the inherited operations. The lecture uses this to motivate subspaces in an abstract vector space.

## Definition 3.1 — Subspace (p. 2)

A **subspace** `U` of a vector space `V` over `F` is a subset `U⊆ V` that is itself a vector space under the addition and scalar multiplication inherited from `V`.

## Example 3.2 — Polynomial subspaces (p. 2)

For integers `0≤ m≤ n`, `P_m(F)` is a subspace of `P_n(F)`; each `P_n(F)` is a subspace of `P(F)`.

## Example 3.3 — The zero and whole subspaces (p. 2)

Every vector space `V` contains the zero subspace `{0}` and is a subspace of itself.

## Proposition 3.4 — Subspace test (pp. 2–3)

A subset `U⊆ V` is a subspace exactly when it is (i) nonempty, (ii) closed under addition, and (iii) closed under scalar multiplication.

The forward direction follows because `U` is a vector space. Conversely, the operations make sense on `U` by closure. The axioms inherited from `V` still hold; nonemptiness plus scalar closure gives `0u=0∈ U`, and scalar closure gives `(-1)u=-u∈ U`.

## Corollary 3.5 — Concise subspace test (p. 3)

For a subset `U⊆V`, the subspace-test conditions can be shortened to `U≠∅` and `α u_1+u_2∈ U` for all `u_1,u_2∈ U`, `α∈F`. Its proof is an exercise in the PDF.

## Example 3.6 — Lines and planes (p. 3)

Let `v,w∈R^n` be nonzero, with `v≠cw` for every `c∈R`. Then `L={tv:t∈R}` and `P={sv+tw:s,t∈R}` are subspaces of `R^n`. For the line, `0∈L` and `α(t_1v)+t_2v=(α t_1+t_2)v∈ L`; the plane is similar.

## Example 3.7 — Polynomials vanishing at 2 (p. 4)

`U={p∈P(F):p(2)=0}` is a subspace of `P(F)`, since `0∈ U` and `(α p+q)(2)=α p(2)+q(2)=0` for `p,q∈ U` and `α∈F`.

## Example 3.8 — Upper triangular matrices (p. 4)

Upper triangular matrices `U_n(F)={[a_ij]∈ M_n(F):a_ij=0 for i>j}` form a subspace of `M_n(F)`. The zero matrix belongs, and entries below the diagonal stay zero under `α A+B` for `A,B∈U_n(F)` and `α∈F`.

## Example 3.9 — Continuously differentiable functions (pp. 4–5)

`C^1([0,1])` consists of continuous real-valued functions on `[0,1]` whose derivatives are also continuous. It is a subspace of `C([0,1])`: it contains the zero function, and the derivative of `αf + g` is `αf' + g'`, which is continuous for `f,g∈C^1([0,1])` and `α∈R`.

## Exercise 3.10 — Even and odd degrees (p. 5)

Determine whether the zero polynomial together with all even-degree polynomials forms a subspace of `P(F)`; do the same for zero together with all odd-degree polynomials.

## Exercise 3.11 — Diagonal matrices (p. 5)

Show diagonal matrices `D_n(F)={[a_ij]∈ M_n(F):a_ij=0 for i≠j}` form a subspace of `M_n(F)`. The PDF observes that `D_n(F)⊆ U_n(F)` as well.

## Source checks

PDF p. 1 calls the displayed plane “the unique line” through `u` in directions `v,w`. The surrounding definition and figure show a plane; the note above uses “plane” and records the PDF wording here.
