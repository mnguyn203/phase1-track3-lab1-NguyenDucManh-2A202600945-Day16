import json
import random
import urllib.request

def main():
    url = "http://curtis.ml.cmu.edu/datasets/hotpot/hotpot_dev_distractor_v1.json"
    print(f"Downloading HotpotQA from {url}...")
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req) as response:
        dataset = json.loads(response.read().decode('utf-8'))
        
    print(f"Loaded {len(dataset)} examples. Filtering for 'hard' questions...")
    hard_questions = [ex for ex in dataset if ex["level"] == "hard"]
    
    print(f"Found {len(hard_questions)} hard questions.")
    
    random.seed(42)
    selected = random.sample(hard_questions, min(100, len(hard_questions)))
    
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
    
    out_path = "data/hotpot_100.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(examples, f, ensure_ascii=False, indent=2)
        
    print(f"Saved {len(examples)} examples to {out_path}")

if __name__ == "__main__":
    main()
