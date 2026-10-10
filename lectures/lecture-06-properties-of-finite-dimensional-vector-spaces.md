# Lecture 6 — Properties of finite-dimensional vector spaces

**Course:** MATH 235, Section 002  
**Source:** `[Section 002] Week 3.pdf`, PDF pp. 1–5  
**Course notes coverage:** part of §1.3.2 and all of §1.3.3

Throughout, `V` is a vector space over `F` with `dim(V)=n`.

## Theorem 6.1 — Size, span, and independence (p. 1)

For finite `S⊆ V`:

1. If `|S|>n`, then `S` is dependent.
2. If `|S|<n`, then `S` cannot span `V`.
3. If `|S|=n`, then `S` spans `V` exactly when it is independent.

The first follows from Lemma 5.2. For the second, a spanning `S` would contain a basis and thus at least `n` vectors. For the third, a spanning but dependent `S` could lose a redundant vector and still span, contradicting (2). An independent but nonspanning `S` could gain a vector outside its span, contradicting (1).

## Remark 6.2 — Extremal properties of a basis (pp. 1–2)

In finite-dimensional `V`, a basis is both a minimal spanning set and a maximal independent set. Dimension is both the fewest vectors that can span `V` and the most vectors that can be independent in `V`.

## Theorem 6.3 — Finding bases (p. 2)

In a finite-dimensional `V`, every spanning set contains a basis, and every independent set can be extended to a basis. The lecture presents these as two procedures: remove redundant spanning vectors, or add vectors outside the current span.

## Example 6.4 — Extending a polynomial set (p. 2)

In `P_3(F)`, start with independent `S = {1+x, 1-x^2}`. Add `x^3`, which cannot lie in its span because `S ⊆ P_2(F)`. Then add `x`, which also cannot lie in the new span: equating coefficients in `a(1+x) + b(1-x^2) + cx^3 = x` gives contradictory requirements. The resulting four-element independent set `B = {1+x, 1-x^2, x^3, x}` is a basis because `dim(P_3(F)) = 4`.

## Example 6.5 — Removing a redundant matrix (p. 3)

The lecture considers a five-element spanning set `S` of `M_2(F)`. In the notation below, each inner list is a matrix row:

1. `A_1 = [[1, 1], [0, 1]]`
2. `A_2 = [[1, -1], [0, 1]]`
3. `A_3 = [[0, 1], [0, -1]]`
4. `A_4 = [[1, -1], [0, 0]]`
5. `A_5 = [[1, 0], [-1, 0]]`

Here `S = {A_1, A_2, A_3, A_4, A_5}`. The lecture accepts `Span(S) = M_2(F)` pending a proof in Lecture 7. Because `dim(M_2(F)) = 4`, one redundant element can be removed. The PDF demonstrates:

`A_2 = (1/3)A_1 + (2/3)A_4 - (2/3)A_3`.

This calculation removes `A_2` and keeps every other matrix, giving `B = {A_1, A_3, A_4, A_5}`. The set `B` still spans `M_2(F)`, and its four elements make it a basis because `dim(M_2(F)) = 4`.

## Proposition 6.6 — Subspaces of finite-dimensional spaces (pp. 3–4)

If `U` is a subspace of `V`, then `U` is finite-dimensional, `dim(U)≤ n`, and `dim(U)=n` exactly when `U=V`. The proof starts with an independent vector in `U` and keeps adding vectors outside the current span until it spans `U`. This must stop by `n` vectors, since `V` has no independent set of size `n+1`.

## Exercise 6.7 — Dimensions of matrix subspaces (p. 4)

Find the dimensions of the upper triangular and diagonal subspaces `U_n(F)` and `D_n(F)` of `M_n(F)` using standard matrix units `E_ij`.

## Example 6.8 — Trace-zero matrices (pp. 4–5)

`U = {A ∈ M_2(F) : Tr(A) = 0}` is a subspace because trace is additive and homogeneous. The lecture builds an independent set inside `U`: first `E_12` and `E_21`, then `E_11 - E_22`. These three span `U`; the lecture proves this by contradiction using `dim(M_2(F)) = 4`. Thus `{E_12, E_21, E_11 - E_22}` is a basis for `U`, and `dim(U) = 3`.

## Exercise 6.9 — Extend an independent set (p. 5)

Find a basis of `R^4` containing `(1,-1,1,-1)^T` and `(0,2,0,-4)^T`.

## Exercise 6.10 — A polynomial subspace basis (p. 5)

Find a basis for the subspace of `P_3(F)` spanned by `{1+x, x+x^2, 2+3x+x^2, x^2+x^3, 1+3x+2x^2+x^3}`.

## Exercise 6.11 — Basis vectors with a derivative constraint (p. 5)

Find a basis of `P_3(F)` consisting only of polynomials satisfying `p'(1)=3`. The PDF suggests finding four independent vectors in this infinite set, rather than removing redundant ones.

## Exercise 6.12 — Trace-zero 3 by 3 matrices (p. 5)

Find a basis and dimension for `{A∈ M_3(F):Tr(A)=0}`.

## Source checks

- On PDF p. 3, the displayed “remaining” set keeps the matrix just shown to be redundant and omits the first matrix instead. The corrected set `B` above follows the lecture's stated removal argument, as clarified by the user.
- Proposition 6.6 uses `n` from the lecture's opening assumption `dim(V)=n`.
- In the proof of Theorem 6.1(i), the PDF says to choose the independent set `T` in Lemma 5.2 to be a basis while discussing a contrapositive. The applicable fact is that a basis is a spanning set of size `n`, so Lemma 5.2 bounds the size of every independent subset by `n`; the proof summary above uses this argument.
