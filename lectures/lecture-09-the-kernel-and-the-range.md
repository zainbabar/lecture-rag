# Lecture 9 — The kernel and the range

**Course:** MATH 235, Section 002  
**Source:** `[Section 002] Week 4.pdf`, PDF pp. 1–7  
**Course notes coverage:** part of §2.2 and a bit of §2.5

Fix vector spaces `V` and `W` over `F`, where `F` is `R` or `C`. The kernel lies in the domain and the range lies in the codomain of a linear map. These are structured notes, with proofs condensed and exercise questions retained.

## Definition 9.1 — Kernel and range (p. 1)

For a linear map `T:V→W`, its **kernel** (or null space) is `Ker(T)={v∈V:T(v)=0_W}⊆V`. Its **range** (or image) is `Range(T)={T(v):v∈V}⊆W`.

## Proposition 9.2 — Kernel and range are subspaces (p. 1)

`Ker(T)` is a subspace of `V`, and `Range(T)` is a subspace of `W`.

Both are nonempty because `T(0_V)=0_W`. If `v_1,v_2∈Ker(T)`, then `T(αv_1+v_2)=αT(v_1)+T(v_2)=0_W`. If `w_1=T(v_1)` and `w_2=T(v_2)` belong to the range, then `αw_1+w_2=T(αv_1+v_2)` also belongs to it.

## Example 9.3 — Identity, zero, and inclusion (p. 2)

1. `id_V:V→V` has `Ker(id_V)={0_V}` and `Range(id_V)=V`.
2. `O:V→W` has `Ker(O)=V` and `Range(O)={0_W}`.
3. For a subspace `U⊆V`, inclusion `ι:U→V`, `ι(u)=u`, has `Ker(ι)={0_U}={0_V}` and `Range(ι)=U`.

## Example 9.4 — Coordinate projection (p. 2)

For `T:R^3→R^2` given by `T((x,y,z)^T)=(x,y)^T`, the kernel condition is `x=y=0`. Thus `Ker(T)={(0,0,z)^T:z∈R}=Span({(0,0,1)^T})`.

The range is `R^2`, because every `(x,y)^T` is the image of `(x,y,0)^T`.

## Example 9.5 — Differentiation and the choice of domain (p. 3)

For differentiation `D:P(F)→P(F)`, `Ker(D)=P_0(F)=F`, the constant polynomials. The range is all of `P(F)`: for `p(x)=a_0+a_1x+...+a_nx^n`, the polynomial `q(x)=a_0x+(a_1/2)x^2+...+(a_n/(n+1))x^(n+1)` satisfies `D(q)=p`.

For the restricted operator `D:P_n(F)→P_n(F)` with `n≥1`, the kernel is still `F`, but `Range(D)=P_(n-1)(F)`, a proper subspace of the codomain.

## Exercise 9.6 — Integration (p. 3)

Compute the kernel and range of `V:P(F)→P(F)` given by `V(p)(x)=∫ from 0 to x of p(t) dt`. Use the result to verify that `{p∈P(F):p(0)=0}` is a subspace of `P(F)`.

## Definition 9.7 — Injective and surjective functions (p. 3)

A function `f:X→Y` is **injective** (one-to-one) if `f(x_1)=f(x_2)` implies `x_1=x_2`. It is **surjective** (onto) if every `y∈Y` equals `f(x)` for some `x∈X`.

## Example 9.8 — Injective and surjective functions (p. 4)

`f:R→R`, `f(x)=e^x`, is injective: equal outputs give equal inputs after applying `ln`. It is not surjective, since `-1` is not an output.

`g:Z→N`, `g(n)=|n|`, is surjective when `N={0,1,2,...}`: every natural number is its own preimage. It is not injective, since `g(1)=g(-1)=1`.

## Proposition 9.9 — Injectivity and surjectivity of linear maps (p. 4)

For a linear map `T:V→W`:

1. `T` is injective exactly when `Ker(T)={0_V}`.
2. `T` is surjective exactly when `Range(T)=W`.

If `T` is injective and `T(v)=0_W=T(0_V)`, then `v=0_V`. Conversely, if the kernel is zero and `T(v_1)=T(v_2)`, then `T(v_1-v_2)=0_W`, forcing `v_1=v_2`. The second assertion is the definition of the range.

## Remark 9.10 — Interpreting kernel and range (pp. 4–5)

The lecture describes the kernel as indicating how far a map is from injectivity, and the range as indicating how far it is from surjectivity. A zero kernel means injectivity; the full codomain as range means surjectivity. At the opposite extreme, a zero map has its entire domain as kernel and only `{0_W}` as range. “More injective” and “more surjective” are informal descriptions here.

## Example 9.11 — Inclusions and projections (pp. 5–6)

An injection `R^2→R^4` is `T((x,y)^T)=(x,y,0,0)^T`. Another is `T((x,y)^T)=(y,0,x,0)^T`. Each is linear with zero kernel.

A surjection `R^4→R^2` is `T((w,x,y,z)^T)=(w,x)^T`. Another is `T((w,x,y,z)^T)=(z,y)^T`. Each is linear and reaches every vector of `R^2`.

## Example 9.12 — First and second derivatives (p. 6)

For `D:P(F)→P(F)`, `Ker(D)=P_0(F)=Span({1})`. For `D^2=D∘D`, `Ker(D^2)=P_1(F)=Span({1,x})`. Since `Ker(D)` is properly contained in `Ker(D^2)`, the lecture calls `D` “more injective” than `D^2`, although neither is injective.

## Exercise 9.13 — Test injectivity and surjectivity (p. 6)

Determine which maps are injective and/or surjective:

1. `T:F^3→P_2(F)`, `T((a,b,c)^T)=(a+b)+(b+c)x+(a+c)x^2`.
2. `S:C([0,1])→R`, `S(f)=∫ from 0 to 1 of f(t) dt`.
3. `τ:M_n(F)→M_n(F)`, `τ(A)=A+A^T`.

## Exercise 9.14 — A function plus its derivative (pp. 6–7)

Recall that `C^1([0,1])` consists of continuously differentiable real-valued functions. Define `T:C^1([0,1])→C([0,1])` by `T(f)=f+f'`.

1. Show `T` is linear by expressing it as a sum of two linear maps.
2. Find `Ker(T)` and show it has dimension 1.
3. Determine whether `T` is surjective, with proof.

## Source checks

The source check on 2026-10-08 found no mathematical transcription errors. Example 9.8 explicitly includes zero in `N`. Remark 9.10 and Example 9.12 use informal comparisons of injectivity; they do not assert that a nontrivial kernel still permits injectivity. The coordinate order in Example 9.11 was checked against the PDF pages.
