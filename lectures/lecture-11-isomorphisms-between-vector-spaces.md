# Lecture 11 — Isomorphisms between vector spaces

**Course:** MATH 235, Section 002  
**Source:** `[Section 002] Week 4.pdf`, PDF pp. 13–17  
**Course notes coverage:** part of §2.5

Fix vector spaces over the same field `F`, where `F` is `R` or `C`. Isomorphisms combine linearity with a bijective correspondence. These notes retain numbered units and condensed proof arguments.

## Definition 11.1 — Bijective functions and isomorphisms (p. 13)

A function `f:X→Y` is **bijective** if it is both injective and surjective. A linear map `T:V→W` is an **isomorphism** if it is bijective.

A bijective function has an inverse `f^(-1):Y→X` satisfying `f^(-1)(f(x))=x` and `f(f^(-1)(y))=y` for every `x∈X` and `y∈Y`.

## Lemma 11.2 — The inverse is an isomorphism (p. 13)

If `T:V→W` is an isomorphism, then `T^(-1):W→V` is also an isomorphism, with `T^(-1)T=id_V` and `TT^(-1)=id_W`.

Only linearity of the inverse needs checking. Write `w_1=T(v_1)` and `w_2=T(v_2)`. Then `T^(-1)(αw_1+w_2)=T^(-1)(T(αv_1+v_2))=αv_1+v_2=αT^(-1)(w_1)+T^(-1)(w_2)`.

## Definition 11.3 — Isomorphic vector spaces (p. 13)

`V` is **isomorphic** to `W`, written `V≅W`, if there exists an isomorphism `T:V→W`.

## Proposition 11.4 — Isomorphism is an equivalence relation (pp. 13–14)

For vector spaces `U,V,W` over `F`:

1. `U≅U`.
2. If `U≅V`, then `V≅U`.
3. If `U≅V` and `V≅W`, then `U≅W`.

Proof: exercise.

## Example 11.5 — Polynomials and coordinate tuples (p. 14)

The map `T:P_3(F)→F^4`, `T(a+bx+cx^2+dx^3)=(a,b,c,d)^T`, is linear with zero kernel, hence injective. Rank-nullity gives rank 4, so it is also surjective. Thus `P_3(F)≅F^4`.

## Example 11.6 — A space isomorphic to a proper subspace (p. 14)

Let `U={p∈P(F):p(0)=0}`. The map `T:P(F)→U`, `T(p)=xp`, is linear. If `xp=0`, then `p=0`, so it is injective. Every `q∈U` has zero constant coefficient and can be written `q=xp`, so it is surjective. Thus `P(F)≅U`.

## Remark 11.7 — Meaning of isomorphism (p. 15)

An isomorphism is a bijective correspondence that respects addition and scalar multiplication. The lecture describes this as renaming vectors while preserving vector-space structure: as vector spaces, isomorphic spaces have the same structure.

## Proposition 11.8 — An isomorphism sends a basis to a basis (p. 15)

Suppose `V` is finite-dimensional with basis `{v_1,...,v_n}`, and `T:V→W` is linear. Then `T` is an isomorphism exactly when `T(v_1),...,T(v_n)` are distinct and `{T(v_1),...,T(v_n)}` is a basis of `W`.

The distinctness requirement matters: a set of image vectors hides repetitions. Proof: exercise; see Week 4 practice problem P4.

## Corollary 11.9 — Finite and infinite dimensions differ (p. 15)

If `V` is finite-dimensional and `W` is infinite-dimensional, they are not isomorphic. Otherwise Proposition 11.8 would send a finite basis of `V` to a finite basis of `W`, a contradiction.

## Theorem 11.10 — Dimension characterizes finite-dimensional isomorphism (pp. 15–16)

For finite-dimensional `V` and `W` over `F`, `V≅W` exactly when `dim(V)=dim(W)`.

If the dimensions differ, Exercise 10.8 rules out either injectivity or surjectivity. If both dimensions equal `n`, choose bases `{v_1,...,v_n}` and `{w_1,...,w_n}`. Proposition 8.12 supplies the unique linear map with `T(v_i)=w_i`; Proposition 11.8 makes it an isomorphism. In particular, `dim(V)=n` exactly when `V≅F^n`, with `F^0={0}` by convention.

## Corollary 11.11 — The coordinate map is an isomorphism (p. 16)

Let `dim(V)=n≥1` and choose an ordered basis `B=(v_1,...,v_n)`. The unique linear map `Φ_B:V→F^n` with `Φ_B(v_i)=e_i` is an isomorphism. For every `v=α_1v_1+...+α_nv_n`, it satisfies `Φ_B(v)=α_1e_1+...+α_ne_n=(α_1,...,α_n)^T=[v]_B`.

## Exercise 11.12 — A two-sided linear inverse (p. 16)

Let `T:V→W` be linear; the spaces need not be finite-dimensional. Prove that `T` is an isomorphism exactly when there exists a linear map `S:W→V` satisfying `ST=id_V` and `TS=id_W`. Show that this `S` equals `T^(-1)`, so the inverse is unique.

## Exercise 11.13 — Multiplication operators on continuous functions (p. 17)

1. Show that `T:C([0,1])→C([0,1])`, `T(f)(x)=(1+x)f(x)`, is an isomorphism.
2. Show that `S:C([0,1])→C([0,1])`, `S(f)(x)=xf(x)`, is not an isomorphism.

## Source checks

No mathematical discrepancy was found in this lecture during the 2026-10-08 audit. Ordered bases use parentheses here to make their ordering explicit; the PDF also allows braces with the order understood. The coordinate tuple in Example 11.5 and the maps in Exercise 11.13 were checked against rendered pages.
