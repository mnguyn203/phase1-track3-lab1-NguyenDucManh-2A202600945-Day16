# Advanced Benchmark Report

| Metric | ReAct | Reflexion | Delta |
|--------|-------|-----------|-------|
| **Accuracy (EM)** | 0.80 | 0.93 | +0.13 |
| **Attempts (Avg/Max)** | 1.00 / 1 | 1.31 / 3 | +0.31 |
| **Tokens (Min/Avg/Max)** | 1336 / 1894 / 2750 | 1339 / 2669 / 8089 | +774 avg |
| **Latency ms (Min/Avg/Max)** | 1509 / 3201 / 111800 | 1455 / 3513 / 14002 | +312 avg |
| **Estimated Cost In ($)** | $0.0277 | $0.0390 | $+0.0114 |
| **Estimated Cost Out ($)** | $0.0030 | $0.0039 | $+0.0009 |
| **Total Estimated Cost ($)** | $0.0307 | $0.0430 | $+0.0123 |

> Note: The token costs are estimated using `gpt-4o-mini` pricing ($0.150/1M input, $0.600/1M output). Output tokens are estimated since the logs only track total tokens.
