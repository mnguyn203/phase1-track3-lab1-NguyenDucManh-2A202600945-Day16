import json
import random

with open('data/hotpot_dev_distractor_v1.json', 'r', encoding='utf-8') as f:
    dataset = json.load(f)

hard_questions = [ex for ex in dataset if ex.get("level") == "hard"]
random.seed(42)
selected = random.sample(hard_questions, min(10, len(hard_questions)))

examples = []
for ex in selected:
    context_chunks = []
    for title, sentences in ex["context"]:
        text = " ".join(sentences)
        context_chunks.append({"title": title, "text": text})
        
    qa_ex = {
        "qid": ex["_id"],
        "difficulty": ex["level"],
        "question": ex["question"],
        "gold_answer": ex["answer"],
        "context": context_chunks
    }
    examples.append(qa_ex)

with open('data/hotpot_10_samples.json', 'w', encoding='utf-8') as f:
    json.dump(examples, f, ensure_ascii=False, indent=2)

print("Saved 10 examples to data/hotpot_10_samples.json")
