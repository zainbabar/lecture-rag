# Week 4 — Practice problems

**Source:** `[Section 002] Week 4.pdf`, PDF pp. 18–20. These questions follow Lecture 11 and are separate from numbered lectures. No solutions are added here. The PDF marks P6 and P7 as optional material not required for assessments.

## P1 — Left and right shift operators (p. 18)

Let `F^∞` be the space of sequences `(a_1,a_2,...)` over `F`, with component-wise operations. Define `L((a_1,a_2,...))=(a_2,a_3,...)` and `R((a_1,a_2,...))=(0,a_1,a_2,...)`.

1. Verify `L` and `R` are linear operators.
2. Determine their kernels and whether either is injective.
3. Determine their ranges and whether either is surjective.

## P2 — Equal kernel and range (p. 18)

1. Show that no linear operator `T:R^69→R^69` satisfies `Ker(T)=Range(T)`.
2. Find an operator `T:R^4→R^4` satisfying `Ker(T)=Range(T)`.

## P3 — A surjectivity claim with a missing hypothesis (p. 18)

**Source problem needs clarification; do not treat its conclusion as an established fact.**

As printed: let `T:M_(2×4)(F)→P_4(F)` be linear and suppose `U` is a subspace of `M_(2×4)(F)` with `dim(U)=3`. Show that `T` must be surjective.

The PDF does not specify any relation between `U` and `T`. See Source checks before using this question.

## P4 — Images of a basis (p. 18)

Let `dim(V)=n`, let `B={v_1,...,v_n}` be a basis of `V`, and let `T:V→W` be linear.

1. Prove that `T` is injective exactly when `T(v_1),...,T(v_n)` are distinct and their set is independent in `W`.
2. Prove that `T` is surjective exactly when `{T(v_1),...,T(v_n)}` spans `W`.
3. Explain how Proposition 11.8 follows.

## P5 — Operators whose powers vanish (p. 19)

Let `V` be finite-dimensional with `dim(V)=n`, and let `T:V→V` be linear.

1. If `T^2=O`, prove `rank(T)≤n/2`. Hint: what does this imply about the kernel and range?
2. If `T^3=O`, prove `rank(T)≤2n/3`. The PDF marks this part challenging.

## P6 — A function plus its second derivative (p. 19)

Recall `T:C^1([0,1])→C([0,1])`, `T(f)=f+f'`, from Exercise 9.14, whose kernel has dimension 1. Let `C^2([0,1])={f∈C^1([0,1]):f' is differentiable and f'' is continuous}` and define `S:C^2([0,1])→C([0,1])` by `S(f)=f+f''`.

1. Show `S` is linear.
2. Show `cos x` and `sin x` are independent elements of `Ker(S)`.
3. Show that if `h∈Ker(S)` and `h(0)=h'(0)=0`, then `h=0`. Hint: differentiate `H(x)=h(x)^2+h'(x)^2` and use `H'=0`.
4. For `g∈Ker(S)`, set `a=g(0)` and `b=g'(0)`. Show `g(x)=a cos x+b sin x`, and conclude `Ker(S)=Span({cos x,sin x})` and `nullity(S)=2`. Hint: apply part 3 to `h(x)=g(x)-a cos x-b sin x`.
5. Between `T` and `S`, which would you call “more injective”?

## P7 — Dual and double-dual spaces (pp. 19–20)

Recall that `L(V,W)`, the set of linear maps `V→W`, is a vector space under pointwise addition and scalar multiplication. Let `dim(V)=n`, define the **dual space** `V*=L(V,F)`, and choose a basis `B={v_1,...,v_n}`.

1. Show there exist unique `φ_1,...,φ_n∈V*` with `φ_i(v_j)=1` if `i=j` and `0` otherwise.
2. Show `B*={φ_1,...,φ_n}` is a basis of `V*`, called the dual basis. Conclude `V≅V*`.
3. Define the **double dual** `V**=(V*)*`. For every `v∈V`, define `ev_v:V*→F` by `ev_v(φ)=φ(v)`. Show `ev_v` is linear, hence belongs to `V**`.
4. Show `Φ:V→V**`, `Φ(v)=ev_v`, is an isomorphism. Unlike the isomorphism `V→V*` constructed using a basis, this map needs no choice of basis.

## Source checks

- **P3 is false as written.** The zero map is linear and the domain has three-dimensional subspaces, yet the zero map is not surjective onto `P_4(F)`. The source does not connect `U` to `T`. A kernel assumption would explain a rank-nullity argument, but it has not been confirmed and is not inserted into the question.
- On PDF p. 19, P7 refers to “Proposition 8.10” for the vector-space structure of `L(V,W)`. The relevant result is Proposition 8.14 in Week 3; 8.10 is an exercise about differentiation.
- In P5, `n` is a finite dimension; the printed finite fractions and rank inequalities are retained in that setting.
