# LUNA Evaluation Tools — OCR Chinese Font Go/No-Go Pack v0 (Phase-EvaluationTools-OCR-002)

## Decision

本决策包仅针对 **Evaluation Tools / OCR Synthetic 数据集质量**。

## GO

- 找到至少一个可用中文字体：
  - can_load_with_pillow=true
  - visible_cjk_passed=true
  - tofu_suspected=false
- 生成中文质量门控数据集（默认 50）
- verifier 通过
- cross verifier 通过（或 CONDITIONAL_GO 且人工确认通过）
- 未调用 OCR provider
- 未接入 runtime / whitebox

## CONDITIONAL_GO

- 字体可用，但 tofu 检测存在不确定性（需人工抽查 probe image）
- 或 cross validation 为 CONDITIONAL_GO（需人工抽查 contact sheet）
- 或类别配比不足但原因明确（仍需 verifier 输出明示）

## NO_GO

- 找不到可用中文字体
- 中文仍为 tofu block
- ground truth/manifest 不一致或缺失
- cross validation 为 NO_GO
- 生成/验证过程中调用 OCR provider
- 接入 runtime/whitebox 或进入 MidPlatform/WorldContext/semantic/语音链路

