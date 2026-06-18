# Báo cáo Đánh giá Mở rộng - Golden Test Set

| Chỉ số (Metric) | ReAct | Reflexion | Mức chênh lệch (Delta) |
|--------|-------|-----------|-------|
| **Độ chính xác (EM)** | 0.95 | 0.95 | +0.00 |
| **Số lần thử (Avg/Max)** | 1.00 / 1 | 1.20 / 3 | +0.20 |
| **Số Token (Thấp/TB/Cao)** | 544 / 578 / 647 | 534 / 840 / 3456 | +261 avg |
| **Độ trễ ms (Thấp/TB/Cao)** | 1557 / 2817 / 10557 | 1659 / 3576 / 17241 | +759 avg |
| **Phí Input ($)** | $0.0016 | $0.0023 | $+0.0008 |
| **Phí Output ($)** | $0.0006 | $0.0007 | $+0.0001 |
| **Tổng phí ($)** | $0.0022 | $0.0031 | $+0.0009 |

> Note: Chi phí token được ước tính dựa trên bảng giá của `gpt-4o-mini` ($0.150/1M input, $0.600/1M output).
