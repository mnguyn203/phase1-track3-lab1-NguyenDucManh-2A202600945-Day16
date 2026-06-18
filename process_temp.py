import json
import random
import zipfile
import os

def main():
    print("Extracting temp.json (which is a zip file)...")
    with zipfile.ZipFile("temp.json", 'r') as zip_ref:
        zip_ref.extractall("extracted_data")
        
    extracted_files = os.listdir("extracted_data")
    print(f"Extracted files: {extracted_files}")
    
    json_file = next(f for f in extracted_files if f.endswith(".json"))
    json_path = os.path.join("extracted_data", json_file)
    
    print(f"Loading {json_path}...")
    with open(json_path, "r", encoding="utf-8") as f:
        dataset = json.load(f)
        
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
