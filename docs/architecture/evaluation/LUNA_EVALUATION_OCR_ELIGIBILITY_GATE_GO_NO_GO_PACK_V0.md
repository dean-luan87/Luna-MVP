# LUNA Evaluation Tools — OCR Eligibility Gate Go/No-Go Pack v0 (Phase-EvaluationTools-OCR-007)

## GO

- `ocr_evidence_routing_pack.json` 已生成，六类 evidence 列表字段齐全。
- `non_ocr_entered_eligible_text_count == 0`，`false_text_risk_after` 相对 `before` 显著下降（目标可为 **0**）。
- `ocr_distortion_prevention_report.json` 中 `distortion_prevention_passed=true`。
- `ocr_route_confusion_matrix.json` 已生成；`ocr_eligibility_gate_trace.jsonl` / `ocr_eligibility_gate_replay.jsonl` 非空。
- `verify_ocr_eligibility_gate_sim_v0.py`  verdict **GO**。
- 输出树中不出现 MidPlatform / SceneDelta / WorldContext 等禁止串联关键词（verifier 扫描）。
- 集成标志：`runtime_integration`、`whitebox_integration`、`mainline_side_effect` 均为 `false`。

## CONDITIONAL_GO

- 大量 `manual_sample_required` / 无 GT 行仅进入 `rejected_or_uncertain`（预期内）。
- `eligibility_accuracy_after` 为 **proxy**，不宣称等于 runtime 路由真值；但 **无失真违规**。

## NO_GO

- 任意 `non_ocr` 样本进入 `eligible_text_evidence`。
- symbol/glyph 类内容被标为 `should_enter_fact_text_layer=true` 的 eligible 事实文本。
- 产物或流程触发 OCR provider 调用、或宣称改变主线 routing / 接入 runtime-whitebox-mainline。
- verifier 失败且存在不可接受的 blockers。
