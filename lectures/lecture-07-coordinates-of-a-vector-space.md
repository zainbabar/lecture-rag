# Lecture 7 — Coordinates of a vector space

**Course:** MATH 235, Section 002  
**Source:** `[Section 002] Week 3.pdf`, PDF pp. 6–12  
**Course notes coverage:** §1.3.4

Choosing and ordering a basis lets an abstract `n`-dimensional vector space be represented by coordinate vectors in `F^n`.

## Theorem 7.1 — Unique representation (p. 6)

If `B = {v_1, ..., v_n}` is a basis of `V`, every `v ∈ V` has a **unique** expression `v = α_1 v_1 + ... + α_n v_n`. Existence follows from spanning. For uniqueness, subtract two such expressions to get `(α_1 - β_1)v_1 + ... + (α_n - β_n)v_n = 0`; independence gives `α_i = β_i` for every `i`.

## Definition 7.2 — Ordered basis (p. 7)

A basis as a set has no order, but a coordinate tuple does. An **ordered basis** specifies an order on its basis vectors. `(v_1,v_2,v_3)` and `(v_2,v_1,v_3)` are different ordered bases even though the underlying set is the same.

## Remark 7.3 — Standard ordered bases (p. 7)

Standard ordered bases are `(e_1, ..., e_n)` for `F^n`, `(1, x, ..., x^n)` for `P_n(F)`, and matrix units `E_ij` in lexicographic `(i,j)` order for `M_(m×n)(F)`.

## Definition 7.4 — Coordinate vector (pp. 7–8)

For ordered `B = (v_1, ..., v_n)` and `v = α_1 v_1 + ... + α_n v_n`, the **coordinate vector** is `[v]_B = (α_1, ..., α_n)^T` in `F^n`.

Changing the basis order changes the coordinate order. For example, changing `(v_1,v_2,v_3)` to `(v_1,v_3,v_2)` changes `(α_1,α_2,α_3)^T` to `(α_1,α_3,α_2)^T`.

## Theorem 7.5 — Coordinates preserve operations (p. 8)

For `v, w ∈ V` and `α ∈ F`:

- `[v + w]_B = [v]_B + [w]_B`.
- `[αv]_B = α[v]_B`.
- `[v_i]_B = e_i`, the `i`th standard basis vector of `F^n`.

The PDF leaves the proof as an exercise.

## Example 7.6 — Standard polynomial coordinates (p. 8)

For the standard ordered basis `E = (1, x, x^2, x^3, x^4)` of `P_4(F)`, the coordinates of `a_0 + a_1x + ... + a_4x^4` are `(a_0, a_1, a_2, a_3, a_4)^T`.

## Example 7.7 — Coordinates in a nonstandard basis (p. 9)

For `B = (1-x, 1+x+x^2, 1-x+x^2)` in `P_2(R)`, the worked calculation finds coordinates for `p(x) = 3+3x+5x^2`. Equating coefficients in

`a(1-x) + b(1+x+x^2) + c(1-x+x^2) = 3+3x+5x^2`

gives `a+b+c=3`, `-a+b-c=3`, and `b+c=5`. The PDF's row reduction gives `(a,b,c)=(-2,3,2)`, so the coordinate vector is `(-2,3,2)^T`. See Source checks for inconsistent text earlier in the example.

## Exercise 7.8 — A polynomial ordered basis (p. 10)

Show `(p,q,r)` is an ordered basis of `P_2(R)`, where `p=(1-x)^2`, `q=2x(1-x)`, and `r=x^2`. Find `[ax^2+bx+c]_{(p,q,r)}`.

## Proposition 7.9 — Coordinates preserve span and independence (p. 10)

For `S={w_1,...,w_k}⊆ V` and `S_B={[w_1]_B,...,[w_k]_B}⊆F^n`:

1. `S` spans `V` exactly when `S_B` spans `F^n`.
2. `S` is independent exactly when `S_B` is independent.

The PDF omits the proof for time. It then uses familiar row reduction to test these properties.

## Example 7.10 — Polynomial independence (pp. 10–11)

For `S = {1-x-x^2, 2+3x+4x^2, 5-2x+x^2}`, standard coordinates are columns of

`A = [[1, 2, 5], [-1, 3, -2], [-1, 4, 1]]`, with each inner list representing a matrix row.

The PDF gives `rref(A)=I_3`. Rank `3` makes the columns, and therefore `S`, independent.

## Example 7.11 — Matrix spanning (p. 11)

Using ordered basis `(E_11, E_12, E_21, E_22)` for `M_2(F)`, the five matrices in the example become columns of

`A = [[1, 1, 1, 2, 1], [1, 0, 1, 0, 0], [0, 1, 1, 1, 0], [1, 1, 0, 3, 2]]`, with each inner list representing a matrix row.

The PDF reports an RREF with pivots only in columns 1, 2, and 3, so `rank(A)=3<4`. The five matrices therefore do **not** span `M_2(F)`.

## Exercise 7.12 — The earlier five-matrix spanning set (p. 12)

Use coordinates to prove that the five-matrix set from Example 6.5 spans `M_2(F)`.

## Exercise 7.13 — Polynomial independence (p. 12)

Decide whether `{1+4x+7x^2, 2+5x+8x^2, 3+6x+9x^2}` is independent in `P_2(F)`.

## Source checks

- The PDF text extractor scrambles the vertical order of entries in the coordinate columns on p. 8. The PDF page shows the correct order, which the notes follow.
- PDF p. 9 first writes `p(x)=3+3x+5x^3`, then calculates with `3+3x+5x^2`. The reviewed correction uses `x^2`, matching the calculation. The page also says “write `x`” while working with `p(x)`.
- Example 7.11 uses a different five-matrix set from Example 6.5. Its rank-3 result does not contradict the rank-4 spanning set revisited in Exercise 7.12.
