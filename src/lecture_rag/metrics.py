# what fraction of the gold chunks showed up in the first k results
# assumes unique retrieved ids and at least one gold id
def recall_at_k(retrieved_ids, gold_ids, k=3):
    appeared = [1 if id in gold_ids else 0 for id in retrieved_ids[:k]]
    count = sum(appeared)
    recall = count / len(gold_ids)
    return recall

# how early the first relevant result appears, only count if appears within cutoff k
# note that we assume that theres atleast one question, and both input lists are the same len
def mrr(all_retrieved_ids, all_gold_ids, k=3):
    total = 0
    n = len(all_retrieved_ids) # number of questions
    for retrieved_ids, gold_ids in zip(all_retrieved_ids, all_gold_ids):
        rr = reciprocal_rank_at_k(retrieved_ids, gold_ids, k)
        total += rr

    mrr = total / n
    return mrr

# score 1 question
def reciprocal_rank_at_k(retrieved_ids, gold_ids, k):
    reciprocal_rank = 0
    for rank, id in enumerate(retrieved_ids[:k], start=1): # within cutoff k
        if id in gold_ids:
            reciprocal_rank = 1 / rank
            break # take only the first hit

    return reciprocal_rank
