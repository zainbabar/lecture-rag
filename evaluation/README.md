# Retrieval evaluation

[retrieval-eval-set.json](retrieval-eval-set.json) contains 30 development questions over Lectures 1–7: 28 answerable and two unanswerable. The original nine-question seed is kept in [retrieval-check-set.json](retrieval-check-set.json). [heldout-eval-set.json](heldout-eval-set.json) has 16 questions written after the retrievers, prompts, and graph were fixed: 13 answerable and three unanswerable.

The questions ask for definitions in different wording, specific examples, math notation, and evidence from more than one lecture. Two ask about topics outside the corpus. Each record includes gold chunk IDs, optional supporting IDs, and the source pages used to check them.

Recall counts how many gold chunks search finds. Other passages may also answer the question, even if they aren't labelled as gold. Questions with multiple gold chunks ask for multiple pieces of evidence. The two unanswerable questions have no gold IDs, so they are left out of recall averages and kept for checking abstention.

All retrievers use the same questions, prepared corpus, and labels. Weights were tuned on this set, so these are development results. See the [project README](../README.md) for measurements and answer-review findings.

## Corpus checks

The indexed corpus is 75 numbered units from Lectures 1–7. Practice files, later lectures, intros, Source checks, and eval material are excluded. Search text includes reviewed assumptions from `search_context.json`.

Labels were checked against the source PDFs. Q20 follows the worked calculation's `x^2` correction in Example 7.7. Q07 needs the assumption `dim(V)=n`, which is included in its search context. Source discrepancies are documented in the lecture files.

Change questions or labels in a separate experiment from retrieval changes. That keeps before/after comparisons on the same inputs. The runner saves hashes of the corpus and dataset so changes can be checked later.
