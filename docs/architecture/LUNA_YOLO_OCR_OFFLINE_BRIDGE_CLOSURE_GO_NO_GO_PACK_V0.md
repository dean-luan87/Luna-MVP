# LUNA — YOLO × OCR Offline Bridge Closure Go/No-Go Pack v0

## Verdict Definition（冻结）

### GO

同时满足：

- Bridge-002 root 可读
- Bridge-003 root 可读
- Bridge-002 verifier 通过
- Bridge-003 verifier 通过
- `proposal_generated_count > 0`
- `bridge_result_generated_count > 0`
- OCR source policy id 存在
- YOLO attribution 与 OCR attribution 存在
- governance leakage = 0
- candidate-only / semantic-interpreation / allows_execute / real TTS / downstream invocation 等边界满足
- trace/replay/whitebox 完整且非空
- sample scale limitation 被登记（允许 minimal evidence closure）

### CONDITIONAL_GO

- 回归通过且硬门槛满足，但 evidence 样本规模仍偏小（minimal evidence）
- 仍会冻结 closed_v0，但会在 closure 文档与 future branches 中明确扩样计划

### NO_GO

- Bridge-002 或 Bridge-003 证据不可读
- proposal/result 缺失
- attribution 缺失
- OCR source policy 未被使用
- governance leakage 非 0
- trace/replay/whitebox 缺失
- 接入 runtime / 中台 / 下游 / semantic / navigation / TTS

## 本阶段建议结论口径

- Bridge-003 evidence 为 minimal real evidence run，因此 Bridge-004 regression + closure 建议给出 **CONDITIONAL_GO**（并登记样本规模限制）。

