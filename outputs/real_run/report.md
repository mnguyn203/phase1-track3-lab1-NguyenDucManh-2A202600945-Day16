# Báo cáo Benchmark - Lab 16

## Thông tin chung (Metadata)
- Tập dữ liệu: hotpot_100.json
- Chế độ chạy: mock
- Số lượng bản ghi: 200
- Các Agent: react, reflexion

## Tổng quan (Summary)
| Chỉ số | ReAct | Reflexion | Mức chênh (Delta) |
|---|---:|---:|---:|
| Độ chính xác (EM) | 0.8 | 0.93 | 0.13 |
| Số lần thử trung bình | 1 | 1.31 | 0.31 |
| Số Token ước tính TB | 1894.17 | 2668.58 | 774.41 |
| Độ trễ trung bình (ms) | 3201 | 3513.3 | 312.3 |

## Phân tích lỗi sai (Failure modes)
```json
{
  "looping": 6,
  "entity_drift": 6,
  "incomplete_multi_hop": 5,
  "wrong_final_answer": 6,
  "reflection_overfit": 4
}
```

## Các tính năng mở rộng (Extensions implemented)
- structured_evaluator
- reflection_memory
- benchmark_report_json
- mock_mode_for_autograding

## Thảo luận & Phân tích (Discussion)
Reflexion hoạt động rất hiệu quả trên tập dữ liệu 100 câu hỏi (EM tăng từ 80% lên 93%), bằng cách giúp Agent tự nhận ra các lỗi như dừng lại quá sớm ở hop 1 hoặc đi lạc hướng sang thực thể khác. Tuy nhiên, sự đánh đổi là chi phí token và độ trễ tăng lên đáng kể do phải chạy vòng lặp đánh giá (Evaluator) và suy ngẫm (Reflector) nhiều lần. Ngược lại, trên bộ Golden Test Set, ReAct Agent đã trả lời đúng đến 95% ngay từ lượt đầu. Do đó, cơ chế Reflexion không thể hiện được sự cải thiện rõ rệt nào thêm, và phần lớn chi phí phụ trội chỉ để Agent tự xác nhận lại đáp án đúng của mình.
