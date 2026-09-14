# Luna — GO/NO_GO: CrossModal Vision OCR Fusion Candidate DryRun v0

**Phase**：`Phase-CrossModal-Vision-OCR-Fusion-Candidate-DryRun-001`

## GO

- 生成 `candidate_scope=dry_run_only` 的 fusion candidate；
- `text_joined` 非空；`fusion_hypothesis.fact_status=not_fact`；
- risk report 与 no-write audit 完整；`verifier=GO`。

## CONDITIONAL_GO

- 输入有效但 `text_joined` 为空（仅 empty_text fusion candidate）；
- 无越界行为。

## NO_GO

- 将 fusion candidate 标为事实或 `cross_modal_fusion_committed=true`；
- 调用 AI interpretation / 导航 / 写 MidPlatform / Scene Delta / WorldModel；
- 重新调用 OCR / Vision provider；
- audit 缺失。
