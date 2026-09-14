# LUNA — YOLO × OCR Evidence Expansion Go/No-Go Pack v0

## Verdict Definition（冻结）

GO 条件：
- 扩样达到最低目标（或至少通过 verifier 的 honest insufficient 分支）。
- `tools/verify_yolo_ocr_bridge_evidence_expansion_v0.py` verifier 通过。
- governance leakage = 0。
- trace/replay/whitebox 完整且非空。
- 不接真实 runtime / 不接中台 / 不进入下游。

CONDITIONAL_GO 条件：
- evidence expansion 审计与治理边界通过，但真实 roots 无法产生足够样本/检测规模（honest insufficient）。
- 仍然保留可复用的扩样工具链与 parse matrix 证据。

NO_GO 条件：
- 伪造 detection 或把 sample_matrix masquerade 成真实 evidence。
- attribution 缺失。
- OCR source policy 未被使用（输出中 policy id 缺失/不一致）。
- governance leakage 非 0。
- trace/replay/whitebox 缺失或 verifier A–Q 失败。
- 接入 runtime / 下游 / 触发 TTS / semantic summary / navigation（违反 offline-only 边界）。

## 本阶段建议结论口径

- Bridge-005 以“扩大证据规模与覆盖”为目标，不以新增功能为目标。
- 扩样不足时必须登记为 future sample collection gap，且不重开 closed_v0 定义。

