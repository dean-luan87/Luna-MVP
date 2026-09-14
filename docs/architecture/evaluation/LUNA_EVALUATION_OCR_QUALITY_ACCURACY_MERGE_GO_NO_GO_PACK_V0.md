# LUNA Evaluation Tools — OCR Quality × Accuracy Merge Go/No-Go Pack v0 (Phase-EvaluationTools-OCR-005)

## GO

- accuracy_root / quality_root 可读
- `sample_id` 对齐成功（aligned_count = expected_count）
- merged matrix / bucket report / correlation report / provider-vs-input report 生成
- verifier 通过
- hard boundary 字段为 false（不调用 OCR provider、不接 runtime/whitebox、不产生主线 side effect）

## CONDITIONAL_GO

- 部分 sample_id 无法对齐，但 missing_alignment 报告明确

## NO_GO

- 输入 root 缺失或不可读
- 样本无法对齐且缺失原因不明
- 重新调用 OCR provider
- 接入 runtime/whitebox/主线 side effect

