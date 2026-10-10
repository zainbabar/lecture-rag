# Lecture 8 — Linear maps between vector spaces

**Course:** MATH 235, Section 002  
**Source:** `[Section 002] Week 3.pdf`, PDF pp. 13–18  
**Course notes coverage:** §2.1

The lecture studies functions between vector spaces that preserve their addition and scalar multiplication.

## Definition 8.1 — Linear map and operator (p. 13)

For vector spaces `V` and `W` over the same field `F`, a map `T: V → W` is **linear** if, for vectors `v_1, v_2` in `V` and scalar `α` in `F`:

- `T(v_1 + v_2) = T(v_1) + T(v_2)`.
- `T(αv_1) = αT(v_1)`.

The lecture also uses “linear transformation.” When `W = V`, `T` is a **linear operator**.

## Proposition 8.2 — Concise linearity test (pp. 13–14)

A map `T:V→W` is linear exactly when `T(α v_1+v_2)=α T(v_1)+T(v_2)` for all `v_1,v_2∈V` and `α∈F`. Its proof is left as an exercise.

## Example 8.3 — Identity, zero, and inclusion maps (p. 14)

The identity `id_V:V→V`, the zero map `O:V→W`, and inclusion `ι:U→V` for a subspace `U⊆V` are linear. They are defined by `id_V(v)=v`, `O(v)=0_W`, and `ι(u)=u`. Inclusion and the identity on `U` differ in their specified codomain.

## Example 8.4 — Coordinate projection (p. 14)

Projection `T:R^3→R^2`, `T((x,y,z)^T)=(x,y)^T`, is linear. For `v_1=(x_1,y_1,z_1)^T` and `v_2=(x_2,y_2,z_2)^T`, applying `T` to `αv_1+v_2` gives `(αx_1+x_2,αy_1+y_2)^T=αT(v_1)+T(v_2)`.

## Example 8.5 — Differentiation (p. 15)

Differentiation `D:P(F)→P(F)`, `D(p)=p'`, is linear. For `n≥1`, a polynomial in `P_n(F)` differentiates to one in `P_(n-1)(F)⊆P_n(F)`, so differentiation restricts to a linear operator `D:P_n(F)→P_n(F)`.

## Example 8.6 — Trace (p. 15)

Trace `Tr:M_n(F)→F`, defined by `Tr([a_ij])=a_11+...+a_nn`, is linear: `Tr(αA+B)=αTr(A)+Tr(B)`.

## Exercise 8.7 — Rotation, integration, and transpose (pp. 15–16)

Prove that all three maps are linear:

1. For `θ∈[0,2π)`, rotation `T_θ:R^2→R^2` given by `T_θ((x,y)^T)=(x cos θ-y sin θ,x sin θ+y cos θ)^T`.
2. Integration `V:P(F)→P(F)` given by `V(p)(x)=∫ from 0 to x of p(t) dt`.
3. Transpose `τ:M_(m×n)(F)→M_(n×m)(F)` given by `τ(A)=A^T`.

## Exercise 8.8 — A piecewise map onto a subspace (p. 16)

For a subspace `U⊆V`, determine whether `T:V→U` defined by `T(v)=v` if `v∈U` and `T(v)=0` otherwise is linear. Prove it or give a counterexample.

## Exercise 8.9 — Determinant and linearity (p. 16)

Determine whether determinant `det:M_n(F)→F` is linear for all `n≥1`; the PDF suggests looking in `M_2(F)` for a counterexample if needed.

## Exercise 8.10 — Differentiation of continuous functions (p. 16)

Show differentiation `D:C^1([0,1])→C([0,1])`, `D(f)=f'`, is linear. Find an `f∈C^1([0,1])` whose derivative is not itself in `C^1([0,1])`.

## Proposition 8.11 — Zero maps to zero (pp. 16–17)

If `T:V→ W` is linear, `T(0_V)=0_W`, since `T(0·0_V)=0· T(0_V)`. The converse fails: `T:R→R`, `T(x)=x^2`, sends zero to zero but `T(2)=4≠2T(1)=2`.

## Proposition 8.12 — A basis determines a linear map (p. 17)

If `dim(V) = n` and `B = {v_1, ..., v_n}` is a basis, any chosen `w_1, ..., w_n` in `W` determine a **unique** linear map `T: V → W` with `T(v_i) = w_i`. Existence uses unique basis coordinates: define `T(α_1v_1 + ... + α_nv_n) = α_1w_1 + ... + α_nw_n` and check the combined linearity condition. The PDF leaves uniqueness as an exercise.

## Corollary 8.13 — Equality on a basis (p. 17)

For finite-dimensional `V`, two linear maps `S,T:V→W` are equal exactly when `S(v_i)=T(v_i)` for every vector of a basis of `V`. Proof: exercise.

## Proposition 8.14 — Operations on linear maps (p. 18)

If `S,T:V→W` are linear and `α∈F`, the pointwise maps `(S+T)(v)=S(v)+T(v)` and `(αS)(v)=αS(v)` are linear. Thus `L(V,W)`, the set of linear maps `V→W`, is a vector space. If `R:U→V` is linear, the composition `S∘R:U→W` is linear. All proofs are exercises.

## Remark 8.15 — Composition as multiplication (p. 18)

Composition may be written `SR` instead of `S∘R`, with `S(R(u))=SRu`, and called multiplication.

## Source checks

- On PDF p. 15, Example 8.5 prints a differentiation sum with terms `ka_kx^k`. Differentiating `a_kx^k` gives `ka_kx^{k-1}`. This note records the map `D(p)=p'` and does not reproduce the inconsistent expansion as a valid formula.
- On PDF p. 17, the proof of Proposition 8.12 repeats `α_1` as the coefficient of its last basis vector in one line; the next line uses `α_n`. This note uses indexed sums to express the proof's intended argument.
