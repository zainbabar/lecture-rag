# what fraction of the gold chunks showed up in the first k results
# assumes unique retrieved ids and at least one gold id
def recall_at_k(retrieved_ids, gold_ids, k=3):
    appeared = [1 if id in gold_ids else 0 for id in retrieved_ids[:k]]
    count = sum(appeared)
    recall = count / len(gold_ids)
    return recall
