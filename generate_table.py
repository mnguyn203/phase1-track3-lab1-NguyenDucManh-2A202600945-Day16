import json
import os

def create_table(run_dir):
    with open(os.path.join(run_dir, 'react_runs.jsonl'), 'r', encoding='utf-8') as f:
        react_records = [json.loads(line) for line in f]
        
    with open(os.path.join(run_dir, 'reflexion_runs.jsonl'), 'r', encoding='utf-8') as f:
        reflexion_records = [json.loads(line) for line in f]
        
    react_dict = {r['qid']: r for r in react_records}
    reflexion_dict = {r['qid']: r for r in reflexion_records}
    
    print("| QID | ReAct Correct | ReAct Attempts | Reflexion Correct | Reflexion Attempts | Reflexion Failure Mode |")
    print("|---|---|---|---|---|---|")
    
    for qid in react_dict.keys():
        r = react_dict[qid]
        rx = reflexion_dict[qid]
        
        print(f"| {qid} | {'✅' if r['is_correct'] else '❌'} | {r['attempts']} | {'✅' if rx['is_correct'] else '❌'} | {rx['attempts']} | {rx['failure_mode']} |")

if __name__ == "__main__":
    create_table("outputs/hotpot_5_real")
