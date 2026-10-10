# Week 2 — Practice problems

**Source:** `[Section 002] Week 2.pdf`, PDF pp. 16–17. These questions follow Lecture 5 and are separate from numbered lectures. No solutions are added here.

## P1 — Intersections and unions of subspaces (p. 16)

Let `V` be a vector space over `F`.

1. Prove that the intersection of two subspaces of `V` is a subspace.
2. Extend the result by induction to the intersection of `n` subspaces.
3. Prove that `W_1∪W_2` is a subspace exactly when `W_1⊆W_2` or `W_2⊆W_1`. The PDF suggests contradiction for the forward direction.

## P2 — Derivative constraints (p. 16)

In `P_3(R)`, let `U={p:p'(0)=0}` and `W={p:p'(0)=1}`.

1. Show `U` is a subspace and find a basis.
2. Determine whether `W` is a subspace.

## P3 — Span and set operations (p. 16)

For finite subsets `S_1,S_2⊆V`, prove:

1. `S_1⊆S_2` implies `Span(S_1)⊆Span(S_2)`.
2. `Span(S_1∩S_2)⊆Span(S_1)∩Span(S_2)`.

## P4 — A set of matrices (p. 16)

In `M_2(F)`, let `S={[[1,2],[3,4]],[[1,-1],[-1,1]],[[1,2],[0,1]]}`. Each inner list represents a matrix row.

1. Explain why `S` cannot span `M_2(F)`.
2. Determine whether `S` is independent.

## P5 — Related four-vector sets (p. 17)

Let `S={v_1,v_2,v_3,v_4}⊆V` and `T={v_1-v_2,v_2-v_3,v_3-v_4,v_4}`.

1. Show that if `S` spans `V`, then `T` spans `V`.
2. Show that if `S` is independent, then `T` is independent.
3. For `w_1=v_1`, `w_2=v_1+v_2`, `w_3=v_1+v_2+v_3`, and `w_4=v_1+v_2+v_3+v_4`, show `Span(S)=Span({w_1,w_2,w_3,w_4})`.

## P6 — Dependence on the scalar field (p. 17)

For `B={1+i,1-i}⊆C`, show that `B` is independent over `R` and dependent over `C`.

## P7 — Parameterized vectors (p. 17)

For a real parameter `x`, let `S={(x,1,1),(1,x,1),(1,1,x)}⊆R^3`. Determine which `x` make `S` dependent, then compute the dimension of its span for each such `x`.

## Source checks

On PDF p. 16, P2 introduces `P_3(R)` but writes `P_3(F)` inside the definitions of `U` and `W`. These notes use the stated real ambient space. All practice questions were checked against their rendered source pages on 2026-10-08 and rewritten in the same plain-text notation as the lectures.

P7 is written as a set. At `x=1`, its three displayed vectors coincide, so the literal set has just one nonzero element. Independence of this set differs from independence of an indexed three-vector family. Preserve the source wording and clarify that convention before using this case in an evaluation question.
