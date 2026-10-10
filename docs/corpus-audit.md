# Corpus conversion and audit — 2026-10-08

All four source PDFs were extracted and rendered locally with PyMuPDF. All 67 pages were reviewed against the structured Markdown, with attention to numbered units, hypotheses, matrix entries, coordinate order, fractions, exponents, and exercise statements. PDF originals were left unchanged.

## Coverage

| Source | Pages | Lectures | Practice pages |
| --- | --- | --- | --- |
| Week 1 | 10 | 1: pp. 1–5; 2: pp. 6–10 | None |
| Week 2 | 17 | 3: pp. 1–5; 4: pp. 6–10; 5: pp. 11–15 | pp. 16–17, P1–P7 |
| Week 3 | 20 | 6: pp. 1–5; 7: pp. 6–12; 8: pp. 13–18 | pp. 19–20, P1–P6 |
| Week 4 | 20 | 9: pp. 1–7; 10: pp. 8–12; 11: pp. 13–17 | pp. 18–20, P1–P7 |

There are 11 lecture files, 125 numbered lecture units, and three practice files containing 20 problems. Lecture-unit counts in order are 6, 10, 11, 13, 10, 12, 13, 15, 14, 8, and 13.

The conversions remain structured summaries, not verbatim transcriptions. Proofs may be condensed and visual diagrams described in words. Exercise statements and their mathematical conditions are retained. No exercise solutions were added; error explanations belong in Source checks.

## Conversion fixes

- Gave each numbered unit an individual `##` heading, including previously grouped examples/exercises and inline remarks/corollaries. This avoids losing Example 3.7 inside a multi-example section, for instance.
- Added unit-specific page references instead of relying on a broad grouped range.
- Standardized the final section as `## Source checks` in every lecture and practice file.
- Converted the older practice files from LaTeX to plain-text notation matching the lectures.
- Made the vector-space operations' closure explicit in Definition 1.1 and restored the rectangular transpose map's domain/codomain in Exercise 8.7.
- Added Lectures 9–11 and Week 4 practice notes; updated the corpus index.

## Source issues and handling

These are source discrepancies or clarifications, not newly invented course facts. Each affected file records its own Source checks.

| Location | Finding | Treatment |
| --- | --- | --- |
| Week 1 p. 2 | Dot product is printed without complex conjugation although `F` can be `C`. | Preserve the printed formula; do not present it as a substituted complex inner-product convention. |
| Week 1 p. 6, Example 2.2 | One expansion gives `b_1` as the constant coefficient instead of `b_0`. | Use the coefficient-indexed definition; document the inconsistency. |
| Week 2 p. 1 | The prose calls a displayed plane a line. | Use plane, matching the definition and diagram; record the wording. |
| Week 2 p. 12, Lemma 5.2 | Nontrivial-solution indices use `n` where there are `k` unknowns. | State the proof with the correct index ranges. |
| Week 2 p. 16, P2 | Ambient space alternates between real and general-field polynomials. | Preserve the explicitly stated real ambient space. |
| Week 2 p. 17, P7; Week 3 p. 19, P4 | At parameter `x=1`, all three vectors coincide. A set and an indexed family then have different independence behavior. | Preserve the set notation; flag the convention before using this case as a gold label. |
| Week 3 p. 1, Theorem 6.1(i) | The proof's parenthetical choice of sets in Lemma 5.2 is confused. | Use the fact that a basis is a spanning set of size `n`, bounding every independent subset. |
| Week 3 p. 3, Example 6.5 | The displayed remaining set removes a different matrix from the one demonstrated redundant. | Preserve the earlier user-confirmed removal of `A_2`; the retained basis is `{A_1,A_3,A_4,A_5}`. |
| Week 3 p. 9, Example 7.7 | Initial polynomial says `5x^3`, then calculations consistently use `5x^2`; prose also names the wrong vector. | Preserve the user-confirmed `x^2` correction and calculated coordinates `(-2,3,2)^T`. |
| Week 3 p. 15, Example 8.5 | Printed differentiation expansion has incorrect exponents/indexing. | State `D(p)=p'` and the correct domain/range inclusion, avoiding the invalid expansion. |
| Week 3 p. 17, Proposition 8.12 | One coefficient repeats `α_1` instead of `α_n`. | Use the indexed linear-map construction and record the typo. |
| Week 4 p. 8, Proposition 10.1 | Proof says the images of a domain basis span `W`. | State that they span `Range(T)`; no surjectivity is assumed. |
| Week 4 p. 9, Example 10.3 | Kernel is printed as a singleton nonzero vector, without `Span`. | Use the line already proved in Example 9.4 and document the omission. |
| Week 4 p. 18, P3 | Arbitrary `U` of dimension 3 is not related to `T`, so the claimed surjectivity does not follow. | Preserve the printed question, mark it false as written, and leave the missing hypothesis unresolved. Do not use it as a gold fact. |
| Week 4 p. 19, P7 | Refers to Proposition 8.10 for the linear-map vector space. | Record that the relevant result is Proposition 8.14. |

Example 7.11 uses a different matrix set from Example 6.5; its rank-3 result is not a contradiction. Raw extraction also scrambles coordinate columns and the `c/2` coefficient in Week 4 Example 10.6; rendered pages resolved those readings.

## Verification and limits

Local source-review tooling (excluded from Git) compared Markdown unit types/numbers with source PDF headings, checked that each cited unit range contained its source-heading page, checked page bounds and final Source checks sections, and caught common LaTeX/extraction artifacts. Its success is structural verification, not a mathematical proof or a retrieval result.

The source review was complemented by exact rational checks of the concrete polynomial/matrix examples: the dependence relation in Example 4.9, the basis-extension and matrix-removal calculations in Examples 6.4–6.5, the coordinates in Example 7.7, and the ranks in Examples 7.10–7.11. Example 10.6's preimage polynomial was checked by differentiating its coefficients.

The nine existing evaluation questions and labels were left unchanged. Their eight primary source units were located in the PDFs and remain represented individually in Markdown. The experiment still searches Lectures 1–7; expanding it is a later explicit decision. Update 2026-10-08: stable chunk IDs, search-text assembly, and an eval runner now exist. The original nine-question labels are preserved; a separate 30-question development set was added and source-checked. No measured retrieval results exist yet.

No page-by-page audit can guarantee the source itself contains no further mistakes. Known discrepancies are recorded rather than hidden. Week 4 P3 has an unresolved missing hypothesis; the repeated parameterized-vector practice question also needs its set-versus-family convention clarified before becoming an eval case.
