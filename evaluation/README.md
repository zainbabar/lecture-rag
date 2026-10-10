# Retrieval development set — Lectures 1–7

30 questions: 28 answerable, 2 unanswerable. The original nine-question check set is preserved separately. This is a development set, not a held-out test set.

Gold IDs are designated evidence targets. For multi-source questions, all listed gold chunks contribute to the requested answer. Supporting sources do not replace primary gold IDs. Alternative valid evidence can exist; review labels before a new comparison and record any version change.

Question text and labels live in [retrieval-eval-set.json](retrieval-eval-set.json). Both retrievers use the exact same prepared corpus. Do not embed this file, the answer key, or source-review notes.

## Q01 — paraphrased_definition

What conditions must addition and scalar multiplication satisfy before a set counts as a vector space?

**Gold:** lecture-01-unit-1.1

**Why:** Operations and all eight vector-space axioms.

## Q02 — paraphrased_definition

If adding the same vector to two vectors gives the same result, what can I conclude, and why?

**Gold:** lecture-02-unit-2.7

**Why:** Additive cancellation and proof using the additive inverse.

## Q03 — example_lookup

Do the polynomials that equal zero at $x=2$ form a subspace? How would I check?

**Gold:** lecture-03-unit-3.7

**Why:** Nonemptiness and closure for polynomials vanishing at 2.

## Q04 — paraphrased_definition

If a subspace contains my chosen vectors, what other vectors is it forced to contain?

**Gold:** lecture-04-unit-4.4

**Why:** Any subspace containing S contains its span and all linear combinations.

## Q05 — paraphrased_definition

How can I recognize that one vector in a set is redundant for linear independence?

**Gold:** lecture-04-unit-4.10

**Why:** Dependence iff one vector is a combination of the others; assumes at least two vectors.

## Q06 — symbol_heavy

How many basis vectors does the space of polynomials of degree at most $n$ need?

**Gold:** lecture-05-unit-5.8

**Why:** Polynomial standard basis 1,x,...,x^n has n+1 elements.

## Q07 — paraphrased_definition

How large can a linearly independent set be in a four-dimensional vector space?

**Gold:** lecture-06-unit-6.1

**Why:** Independent sets have at most four vectors; a basis attains four. Requires introductory assumption dim(V)=n.

## Q08 — paraphrased_definition

Why does a basis let me represent a vector in one and only one way?

**Gold:** lecture-07-unit-7.1

**Why:** Spanning gives existence; independence gives uniqueness by subtracting representations.

## Q09 — unanswerable

How do I compute the eigenvalues of a matrix?

**Gold:** none — unanswerable

**Why:** No eigenvalue-computation evidence in Lectures 1–7; closest matches are insufficient.

## Q10 — paraphrased_definition

What two properties must a collection of vectors have to serve as a basis?

**Gold:** lecture-05-unit-5.3

**Why:** Basis means spanning and independent.

## Q11 — paraphrased_definition

For a finite-dimensional vector space, what does its dimension count?

**Gold:** lecture-05-unit-5.6

**Why:** Dimension counts vectors in any basis.

## Q12 — paraphrased_definition

Why do we need an ordered basis rather than just a set when writing coordinate tuples?

**Gold:** lecture-07-unit-7.2

**Why:** The basis order determines which vector each coordinate belongs to.

## Q13 — symbol_heavy

What does [v]_B mean, and what happens to its entries if I swap two vectors in B?

**Gold:** lecture-07-unit-7.4

**Why:** Coordinates are coefficients in basis order; reordering permutes entries.

## Q14 — paraphrased_definition

What must a smaller vector space inherit from a larger one to count as its subspace?

**Gold:** lecture-03-unit-3.1

**Why:** A subspace uses the inherited addition and scalar multiplication.

## Q15 — symbol_heavy

In these notes, what degree is assigned to the zero polynomial?

**Gold:** lecture-02-unit-2.1

**Why:** The convention is deg(0)=-infinity.

## Q16 — example_lookup

Which exercise treats positive real numbers as vectors using multiplication as addition, and how does it define scalar multiplication?

**Gold:** lecture-02-unit-2.10

**Why:** The exercise specifies x plus y as xy and scalar multiplication as x^alpha; no solution is requested.

## Q17 — example_lookup

What basis and dimension do the notes give for the zero vector space?

**Gold:** lecture-05-unit-5.9

**Why:** The empty set is the only basis, and dimension is zero.

## Q18 — example_lookup

Can C^n be treated as a vector space using only real scalars?

**Gold:** lecture-01-unit-1.4

**Why:** Restricting scalars to R makes C^n a real vector space.

## Q19 — example_lookup

Find the worked example giving a basis for trace-zero 2 by 2 matrices. Which matrices form that basis and what is the dimension?

**Gold:** lecture-06-unit-6.8

**Why:** The basis is E_12, E_21, E_11-E_22; dimension three.

## Q20 — symbol_heavy

For B=(1-x,1+x+x^2,1-x+x^2), what are the coordinates of 3+3x+5x^2, and how are they found?

**Gold:** lecture-07-unit-7.7

**Why:** The corrected example equates coefficients and obtains (-2,3,2). The x^2 correction was user-confirmed.

## Q21 — example_lookup

Which worked matrix-spanning example ends with rank 3 even though its ambient space has dimension 4, and what does that imply?

**Gold:** lecture-07-unit-7.11

**Why:** This five-matrix example does not span M_2(F), because its coordinate matrix has rank three.

## Q22 — symbol_heavy

How are [v+w]_B and [alpha v]_B related to the individual coordinate vectors?

**Gold:** lecture-07-unit-7.5

**Why:** Coordinates preserve vector addition and scalar multiplication.

## Q23 — symbol_heavy

If alpha u = alpha v, which condition on alpha lets me cancel it, and why?

**Gold:** lecture-02-unit-2.7

**Why:** Alpha must be nonzero so multiplication by its inverse is defined.

## Q24 — symbol_heavy

What is Span(empty set), and is the empty set linearly independent?

**Gold:** lecture-04-unit-4.1, lecture-04-unit-4.8

**Why:** One passage states the empty span is {0}; the other declares the empty set independent.

## Q25 — example_lookup

In the P_3(F) example starting from {1+x,1-x^2}, which two polynomials are added to obtain a basis?

**Gold:** lecture-06-unit-6.4

**Why:** Adds x^3 then x, with independence reasoning.

## Q26 — cross_lecture

Explain why polynomials vanishing at 2 form a subspace, then state what basis-extension guarantee applies to independent sets in finite-dimensional vector spaces.

**Gold:** lecture-03-unit-3.7, lecture-06-unit-6.3

**Why:** The polynomial example proves subspace closure; the later theorem gives the explicitly requested finite-dimensional extension guarantee.

## Q27 — cross_lecture

Give the standard basis and dimension of P_4(F), then show how the notes represent a0+a1x+a2x^2+a3x^3+a4x^4 in that ordered basis.

**Gold:** lecture-05-unit-5.8, lecture-07-unit-7.6

**Why:** Standard basis/dimension and the worked coordinate tuple are separately requested.

## Q28 — cross_lecture

What criterion tells me which vector can be removed from a dependent set, and which later lemma says repeated removal preserves the span until an independent subset remains?

**Gold:** lecture-04-unit-4.10, lecture-05-unit-5.1

**Why:** The redundancy criterion and the finite removal lemma give both requested pieces.

## Q29 — cross_lecture

First define a basis, then explain why it gives every vector unique coefficients and how those coefficients form [v]_B.

**Gold:** lecture-05-unit-5.3, lecture-07-unit-7.1, lecture-07-unit-7.4

**Why:** Needs the basis definition, uniqueness theorem, and ordered coordinate-vector definition.

## Q30 — unanswerable

How do I compute a singular value decomposition and use it to find the best rank-k approximation of a matrix?

**Gold:** none — unanswerable

**Why:** Lectures 1–7 contain no SVD or low-rank approximation procedure.

## Source checks and limits

Labels were checked against the referenced PDF pages and Markdown. Q20 uses the previously confirmed x^2 correction in Example 7.7. Q07 requires the Lecture 6 introductory assumption dim(V)=n; search_context.json now supplies it. Q07 alternatives remain flagged in the original seed set. Questions ask for evidence supplied by the notes, not invented exercise solutions. No retrieval measurements exist yet.
