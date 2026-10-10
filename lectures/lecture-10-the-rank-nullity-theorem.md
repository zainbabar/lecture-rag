# Lecture 10 — The rank-nullity theorem

**Course:** MATH 235, Section 002  
**Source:** `[Section 002] Week 4.pdf`, PDF pp. 8–12  
**Course notes coverage:** part of §2.2

Fix vector spaces `V` and `W` over `F`, where `F` is `R` or `C`. This lecture relates the dimensions of the kernel, range, and domain of a linear map. Proofs are condensed; apparent source errors are recorded at the end.

## Proposition 10.1 — Finite-dimensional kernel and range (p. 8)

If `T:V→W` is linear and `dim(V)=n<∞`, then `Ker(T)` and `Range(T)` are finite-dimensional, each with dimension at most `n`.

The kernel is a subspace of finite-dimensional `V`. For the range, choose a basis `{v_1,...,v_n}` of `V`. Every `w∈Range(T)` equals `T(v)` for some `v=α_1v_1+...+α_nv_n`, hence `w=α_1T(v_1)+...+α_nT(v_n)`. Thus the images of the basis vectors span `Range(T)`, giving its dimension bound. The codomain `W` need not be finite-dimensional.

## Definition 10.2 — Rank and nullity (p. 8)

The **rank** of `T` is `rank(T)=dim(Range(T))`. Its **nullity** is `nullity(T)=dim(Ker(T))`. If the domain is finite-dimensional, these are finite and each is at most `dim(V)`.

## Example 10.3 — Differentiation and projection (pp. 8–9)

1. For `n≥1`, differentiation `D:P_n(F)→P_n(F)` has kernel `F` and range `P_(n-1)(F)`, so `nullity(D)=1` and `rank(D)=n`.
2. Projection `T:R^3→R^2`, `T((x,y,z)^T)=(x,y)^T`, has range `R^2` and kernel `Span({(0,0,1)^T})`, so `rank(T)=2` and `nullity(T)=1`.

## Theorem 10.4 — Rank-nullity theorem (pp. 9–10)

For a linear map `T:V→W` with `dim(V)=n<∞`, `rank(T)+nullity(T)=n`.

Let `{u_1,...,u_k}` be a basis of `Ker(T)`, and extend it to a basis `{u_1,...,u_k,v_1,...,v_(n-k)}` of `V`. Set `w_j=T(v_j)`. The proof shows that `{w_1,...,w_(n-k)}` is a basis of the range:

1. **Spanning:** write a preimage `v` in the extended basis and apply `T`. All kernel-basis terms vanish, leaving a linear combination of the `w_j`.
2. **Independence:** if `β_1w_1+...+β_(n-k)w_(n-k)=0_W`, then `β_1v_1+...+β_(n-k)v_(n-k)` belongs to the kernel, so it is a combination of the `u_i`. Independence of the extended basis forces all `β_j` to be zero.

Thus `rank(T)=n-k`, while `nullity(T)=k`.

## Example 10.5 — Dimension of trace-zero matrices (pp. 10–11)

For `n≥1`, `W={A∈M_n(F):Tr(A)=0}=Ker(Tr)` is a subspace. The linear trace map `Tr:M_n(F)→F` is surjective, because `Tr(aE_11)=a` for every `a∈F`. Its rank is 1 and its domain has dimension `n^2`. Rank-nullity gives `dim(W)=n^2-1=(n+1)(n-1)`. In particular, this dimension is 8 for `M_3(F)`.

## Example 10.6 — Polynomial derivative constraints (p. 11)

Let `W={p∈P_4(R):p(0)=p'(0)=p''(0)=0}`. Define `T:P_4(R)→R^3` by `T(p)=(p(0),p'(0),p''(0))^T`.

Evaluation and differentiation give `T(αp+q)=αT(p)+T(q)`, so `T` is linear and `W=Ker(T)` is a subspace. For any `(a,b,c)^T∈R^3`, take `p(x)=a+bx+(c/2)x^2`; then `T(p)=(a,b,c)^T`. Therefore `T` is surjective, `rank(T)=3`, and `dim(W)=5-3=2`.

## Exercise 10.7 — Rank and nullity beyond finite domains (pp. 11–12)

Let `T:V→W` be linear; the spaces may be infinite-dimensional.

1. Show `T` is injective exactly when `nullity(T)=0`.
2. If `W` is finite-dimensional, show `T` is surjective exactly when `rank(T)=dim(W)`.
3. Find a map with `rank(T)=∞` that is not surjective.

The lecture describes smaller nullity as closer to injectivity, and, for finite-dimensional `W`, rank closer to `dim(W)` as closer to surjectivity.

## Exercise 10.8 — Compare domain and codomain dimensions (p. 12)

For finite-dimensional `V` and `W`, prove:

1. If `dim(V)<dim(W)`, no linear map `T:V→W` can be surjective.
2. If `dim(V)>dim(W)`, no linear map `T:V→W` can be injective.
3. If `dim(V)=dim(W)`, a linear map `T:V→W` is injective exactly when it is surjective.

## Source checks

- On PDF p. 8, the proof of Proposition 10.1 calls `{T(v_1),...,T(v_n)}` a spanning set for `W`. The argument only proves it spans `Range(T)`, which is the claim used above. A map need not be surjective.
- On PDF p. 9, Example 10.3 prints `Ker(T)={(0,0,1)^T}`, omitting `Span`. The kernel is the whole line `Span({(0,0,1)^T})`, as already established in Example 9.4. The singleton is not a subspace.
- On PDF p. 11, the coefficient in the preimage polynomial of Example 10.6 is `c/2`. The fraction and coordinate order were verified against the rendered page; raw extraction scrambles them.
