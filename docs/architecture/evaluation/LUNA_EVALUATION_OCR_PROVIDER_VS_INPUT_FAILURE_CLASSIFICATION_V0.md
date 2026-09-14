# LUNA Evaluation Tools — OCR Provider vs Input Failure Classification v0 (Phase-EvaluationTools-OCR-005)

## Goal

把“识别失败”拆成可行动的工程归因维度（evaluation-only）：

- provider_fail（provider 调用失败/异常）
- good_input_bad_ocr（输入质量门控为 GO，但 OCR 指标差）
- bad_input_bad_ocr（输入质量差 + OCR 指标差）
- bad_input_good_ocr（输入质量门控为 CONDITIONAL/NO_GO，但 OCR 仍表现好）

## Notes

- 分类用于离线评测与样本分流（baseline/difficult/failure/human_review）
- 不得自动影响主线 provider 选择

