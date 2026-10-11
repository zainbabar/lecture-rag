# Retrieval evaluation

[retrieval-eval-set.json](retrieval-eval-set.json) contains 30 development questions over Lectures 1–7: 28 answerable and two unanswerable. The original nine-question seed is kept in [retrieval-check-set.json](retrieval-check-set.json).

Questions cover paraphrased definitions, example lookups, math notation, cross-lecture evidence, and topics outside the corpus. Each record includes gold chunk IDs, optional supporting IDs, and source verification.

Gold IDs are the evidence targets used for recall. They aren't exhaustive relevance judgments: another retrieved passage can answer a question without matching its gold label. Questions with multiple gold chunks require multiple pieces of evidence. Unanswerable questions have no gold IDs and are excluded from recall averages, but are included when checking abstention.

All retrievers use the same questions, prepared corpus, and labels. Weights were tuned on this set, so these are development results. See the [project README](../README.md) for measurements and answer-review findings.

## Corpus checks

The indexed corpus is 75 numbered units from Lectures 1–7. Practice files, later lectures, intros, Source checks, and eval material are excluded. Search text includes reviewed assumptions from `search_context.json`.

Labels were checked against the source PDFs. Q20 follows the worked calculation's `x^2` correction in Example 7.7. Q07 needs the assumption `dim(V)=n`, which is included in its search context. Source discrepancies are documented in the lecture files.

Keep question and label changes separate from retrieval changes so before/after comparisons use the same inputs. The runner records corpus and dataset fingerprints to make changes visible.
