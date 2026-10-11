# Lecture 5 — Bases and dimension

**Course:** MATH 235, Section 002  
**Source:** `[Section 002] Week 2.pdf`, PDF pp. 11–15  
**Course notes coverage:** parts of §1.3.1 and §1.3.2

A basis combines enough vectors to span the space with no redundant vectors. The lecture uses this to define dimension.

## Lemma 5.1 — Remove redundant vectors (p. 11)

Every finite `S⊆ V` has a linearly independent subset `T⊆ S` with `Span(T)=Span(S)`. The proof repeatedly removes a vector expressible as a combination of the others. The process terminates because `S` is finite; the empty set is independent if removal reaches it.

## Lemma 5.2 — Independent sets cannot exceed spanning sets (pp. 11–12)

If `S={v_1,...,v_n}` spans `V` and `T={w_1,...,w_k}` is independent, then `k≤ n`.

The proof argues by contrapositive. If `k > n`, express each `w_i` as `α_i1 v_1 + ... + α_in v_n`. For each `j = 1, ..., n`, form the equation `α_1j x_1 + ... + α_kj x_k = 0`. This gives `n` homogeneous equations in `k` unknowns, so there is a nonzero solution. It yields a nontrivial relation `x_1 w_1 + ... + x_k w_k = 0`, contradicting independence.

## Definition 5.3 — Basis (p. 12)

A subset `B⊆ V` is a **basis** if it spans `V` and is linearly independent.

## Theorem 5.4 — Bases exist and have equal size (p. 13)

If `V` has a finite spanning set, it has a basis: apply Lemma 5.1. If `B` and `C` are two bases, Lemma 5.2 applied in both directions gives `|B|≤|C|` and `|C|≤|B|`, hence equal size.

## Definition 5.5 — Finite and infinite dimension (p. 13)

`V` is **finite-dimensional** if it has a finite basis; otherwise it is **infinite-dimensional**.

## Definition 5.6 — Dimension (p. 13)

For a finite-dimensional `V`, `dim(V)` is the number of vectors in any basis. The lecture writes `dim(V)=∞` for an infinite-dimensional space.

## Remark 5.7 — Basis as a coordinate system (p. 13)

A basis acts as a coordinate system: spanning allows us to reach every vector, and independence prevents redundancy. Dimension fixes the number of basis directions.

## Example 5.8 — Standard bases (pp. 13–14)

- `F^n` has standard basis `{e_1,...,e_n}`, where `e_i` has a single `1` in position `i`. Thus `dim(F^n)=n`.
- `P_n(F)` has standard basis `{1,x,...,x^n}` and dimension `n+1`.
- `M_(m×n)(F)` has standard basis `{E_ij : 1 ≤ i ≤ m, 1 ≤ j ≤ n}`, where `E_ij` has `1` at entry `(i,j)` and `0` elsewhere. Its dimension is `mn`. The lecture lists all six `E_ij` for `M_(2×3)(F)`.

## Example 5.9 — Zero space (p. 14)

`Span(∅)={0}` and `∅` is independent, so the empty set is the only basis of `{0}`. Consequently `dim({0})=0`, and a vector space has dimension zero exactly when it is the zero space.

## Exercise 5.10 — A polynomial basis (p. 15)

Show that `{1,1+x,1+x+x^2}` is a basis for `P_2(F)`.

## Source checks

The proof of Lemma 5.2 on PDF p. 12 has inconsistent subscripts in the sentence describing the nontrivial solution: it names `β_1,...,β_n` although there are `k` unknowns. The notes use the correct index ranges.
