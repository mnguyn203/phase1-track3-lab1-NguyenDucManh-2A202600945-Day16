import json
from pathlib import Path
import pandas as pd

def process_file(filepath):
    records = []
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            records.append(json.loads(line))
    
    df = pd.DataFrame(records)
    
    # Estimate input vs output tokens
    # Output tokens roughly len(answer) / 4, plus evaluator output length
    def estimate_cost(row):
        total_tokens = row["token_estimate"]
        # Very rough estimate: output is about 50 tokens on average, rest is input
        out_tokens = min(50 * row["attempts"], total_tokens * 0.1)
        in_tokens = total_tokens - out_tokens
        
        cost_in = (in_tokens / 1_000_000) * 0.150
        cost_out = (out_tokens / 1_000_000) * 0.600
        return cost_in, cost_out
        
    df[["cost_in", "cost_out"]] = df.apply(estimate_cost, axis=1, result_type="expand")
    df["total_cost"] = df["cost_in"] + df["cost_out"]
    
    stats = {
        "count": len(df),
        "em": df["is_correct"].mean(),
        "attempts_avg": df["attempts"].mean(),
        "attempts_max": df["attempts"].max(),
        "tokens_avg": df["token_estimate"].mean(),
        "tokens_min": df["token_estimate"].min(),
        "tokens_max": df["token_estimate"].max(),
        "latency_avg_ms": df["latency_ms"].mean(),
        "latency_min_ms": df["latency_ms"].min(),
        "latency_max_ms": df["latency_ms"].max(),
        "cost_in_total": df["cost_in"].sum(),
        "cost_out_total": df["cost_out"].sum(),
        "cost_total": df["total_cost"].sum()
    }
    return stats

def main():
    react_stats = process_file("outputs/golden_run/react_runs.jsonl")
    reflexion_stats = process_file("outputs/golden_run/reflexion_runs.jsonl")
    
    md_content = f"""# Báo cáo Đánh giá Mở rộng - Golden Test Set

| Chỉ số (Metric) | ReAct | Reflexion | Mức chênh lệch (Delta) |
|--------|-------|-----------|-------|
| **Độ chính xác (EM)** | {react_stats['em']:.2f} | {reflexion_stats['em']:.2f} | {reflexion_stats['em'] - react_stats['em']:+.2f} |
| **Số lần thử (Avg/Max)** | {react_stats['attempts_avg']:.2f} / {react_stats['attempts_max']} | {reflexion_stats['attempts_avg']:.2f} / {reflexion_stats['attempts_max']} | {(reflexion_stats['attempts_avg'] - react_stats['attempts_avg']):+.2f} |
| **Số Token (Thấp/TB/Cao)** | {react_stats['tokens_min']} / {react_stats['tokens_avg']:.0f} / {react_stats['tokens_max']} | {reflexion_stats['tokens_min']} / {reflexion_stats['tokens_avg']:.0f} / {reflexion_stats['tokens_max']} | {(reflexion_stats['tokens_avg'] - react_stats['tokens_avg']):+.0f} avg |
| **Độ trễ ms (Thấp/TB/Cao)** | {react_stats['latency_min_ms']} / {react_stats['latency_avg_ms']:.0f} / {react_stats['latency_max_ms']} | {reflexion_stats['latency_min_ms']} / {reflexion_stats['latency_avg_ms']:.0f} / {reflexion_stats['latency_max_ms']} | {(reflexion_stats['latency_avg_ms'] - react_stats['latency_avg_ms']):+.0f} avg |
| **Phí Input ($)** | ${react_stats['cost_in_total']:.4f} | ${reflexion_stats['cost_in_total']:.4f} | ${reflexion_stats['cost_in_total'] - react_stats['cost_in_total']:+.4f} |
| **Phí Output ($)** | ${react_stats['cost_out_total']:.4f} | ${reflexion_stats['cost_out_total']:.4f} | ${reflexion_stats['cost_out_total'] - react_stats['cost_out_total']:+.4f} |
| **Tổng phí ($)** | ${react_stats['cost_total']:.4f} | ${reflexion_stats['cost_total']:.4f} | ${reflexion_stats['cost_total'] - react_stats['cost_total']:+.4f} |

> Note: Chi phí token được ước tính dựa trên bảng giá của `gpt-4o-mini` ($0.150/1M input, $0.600/1M output).
"""
    
    Path("outputs/golden_run/advanced_report.md").write_text(md_content, encoding="utf-8")
    print(md_content)

if __name__ == "__main__":
    main()
