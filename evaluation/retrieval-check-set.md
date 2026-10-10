# Retrieval check set — MATH 235, Lectures 1–7

This is a small, manually labelled set of questions for our **first retrieval experiment**. The answers were located in the lecture Markdown before building a retriever. Keep this file outside `lectures/` so a search over the lecture corpus cannot retrieve the answer key itself.

**Search scope:** the seven `lecture-01` through `lecture-07` Markdown files only. Exclude Lectures 8–11, the weekly practice-problem files, this check set, and the RAG study guide. The original PDFs are the reference for verifying notation.

For each answerable question, the listed **primary source** is the section we want to see among the top three retrieved passages. A supporting source may also be useful, but does not replace the primary source when scoring this first check. Read the retrieved passage to confirm it actually contains the needed evidence; a matching filename alone is insufficient.

## Answerable questions

### Q01 — Vector-space definition

**Gold chunk IDs:** `lecture-01-unit-1.1`.

**Question:** What conditions must addition and scalar multiplication satisfy before a set counts as a vector space?

**Primary source:** [Lecture 1, Definition 1.1](../lectures/lecture-01-introduction-to-vector-spaces.md), Week 1 PDF p. 2.  
**Why this source:** It states the eight vector-space axioms.

### Q02 — Cancellation

**Gold chunk IDs:** `lecture-02-unit-2.7`.

**Question:** If adding the same vector to two vectors gives the same result, what can I conclude, and why?

**Primary source:** [Lecture 2, Proposition 2.7](../lectures/lecture-02-more-examples-and-vector-space-properties.md), Week 1 PDF pp. 8–9.  
**Why this source:** It states and proves the additive cancellation law.

### Q03 — A subspace example

**Gold chunk IDs:** `lecture-03-unit-3.7`.

**Question:** Do the polynomials that equal zero at $x=2$ form a subspace? How would I check?

**Primary source:** [Lecture 3, Example 3.7](../lectures/lecture-03-subspaces.md), Week 2 PDF p. 4.  
**Supporting source:** Lecture 3, Proposition 3.4 / Corollary 3.5, Week 2 PDF pp. 2–3.  
**Why this source:** The example applies the subspace test to precisely this polynomial set.

### Q04 — What span guarantees

**Gold chunk IDs:** `lecture-04-unit-4.4`.

**Question:** If a subspace contains my chosen vectors, what other vectors is it forced to contain?

**Primary source:** [Lecture 4, Proposition 4.4](../lectures/lecture-04-span-and-linear-independence.md), Week 2 PDF p. 7.  
**Why this source:** It explains that the span consists of their linear combinations and is contained in every subspace containing the chosen vectors.

### Q05 — Redundancy

**Gold chunk IDs:** `lecture-04-unit-4.10`.

**Question:** How can I recognize that one vector in a set is redundant for linear independence?

**Primary source:** [Lecture 4, Proposition 4.10](../lectures/lecture-04-span-and-linear-independence.md), Week 2 PDF pp. 9–10.  
**Why this source:** It connects dependence with one vector being a linear combination of the others.

### Q06 — Polynomial dimension

**Gold chunk IDs:** `lecture-05-unit-5.8`.

**Question:** How many basis vectors does the space of polynomials of degree at most $n$ need?

**Primary source:** [Lecture 5, Example 5.8](../lectures/lecture-05-bases-and-dimension.md), Week 2 PDF p. 14.  
**Why this source:** It gives the standard basis $\{1,x,\ldots,x^n\}$ and dimension $n+1$.

### Q07 — Dimension limit

**Gold chunk IDs:** `lecture-06-unit-6.1`.

**Question:** How large can a linearly independent set be in a four-dimensional vector space?

**Primary source:** [Lecture 6, Theorem 6.1](../lectures/lecture-06-properties-of-finite-dimensional-vector-spaces.md), Week 3 PDF p. 1.  
**Why this source:** A set with more than $\dim(V)$ vectors must be dependent.

### Q08 — Unique coordinates

**Gold chunk IDs:** `lecture-07-unit-7.1`.

**Question:** Why does a basis let me represent a vector in one and only one way?

**Primary source:** [Lecture 7, Theorem 7.1](../lectures/lecture-07-coordinates-of-a-vector-space.md), Week 3 PDF p. 6.  
**Why this source:** Spanning gives existence; independence gives uniqueness.

## Question without an answer in this corpus

### Q09 — Outside the current lectures

**Gold chunk IDs:** None (unanswerable).

**Question:** How do I compute the eigenvalues of a matrix?

**Expected evidence:** None in Lectures 1–7. This question is **excluded** from the top-three source-hit count. A retriever will still return its closest passages; later, when we add answer generation, this example will help test whether the system recognizes insufficient evidence.

## First manual check

For Q01–Q08, record the first three returned passages and their source sections. Count how many questions have their primary source in those three passages: that count divided by eight is our initial **primary-source hit rate at 3**. Keep the individual rankings and failure notes too; the fraction alone will not explain *why* a source was missed.

These labels are a starting point. If reading the PDFs reveals a mistaken expected source or a question that permits several equally good sources, fix the label **before** comparing chunking or retrieval methods.

## Stable-ID labelling — 2026-10-08

Machine-readable labels are in [retrieval-check-set.json](retrieval-check-set.json). Question text, primary sources, and top-three scoring are unchanged. Q03 supporting IDs are recorded separately and do not replace its primary source. Relevant chunks were checked against original PDF page text; selected pages were also visually inspected.

Q07 requires the Lecture 6 introduction’s assumption `dim(V)=n`, preserved in `lecture_intro`. Include it in retrieval context before comparing methods. Remark 6.2 is also valid answer evidence; Lemma 5.2 can justify the bound. These alternatives are flagged for review, not silently added to accepted gold labels.

This is still a nine-question seed set, not the roughly 30-question target or an executed evaluation.
