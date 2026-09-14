# LUNA — OCR Raw Text → MidPlatform Bridge Fix Go/No-Go Pack v0

## Phase

- **Phase-ModelOCR-MidPlatform-Bridge-001-Fix**

## GO 条件（冻结）

同时满足：

1. filtering/blocking policy 明确
- block_reason 枚举完整
- block_level 枚举与语义明确
- evidence retention 规则明确

2. block_reason / block_level 可审计
- filter_result 的 retention + trace/replay/whitebox 引用完整
- hard_block 仍需可追责（trace/whitebox 生成/保留）

3. monitoring metrics 定义完整
- delta decision / duplicate / reuse / partial/full / uncertain / blocked 计数口径明确

4. trace/replay/whitebox 字段要求明确
- trace: evidence_id/delta_control_id/text/layout signatures/block_reason/block_level等
- replay: raw_evidence_ref/previous_result_ref/signature_inputs_ref/delta_decision_ref/filter_result_ref
- whitebox: why_reused/why_blocked/why_reprocessed + threshold 快照

5. verifier test matrix 明确
- A-L 用例覆盖 filtering/blocking + delta decision + retention + boundary

6. Contract-only：本阶段不实现 runtime
- 不接真实中台/不接下游/不执行导航/不生成语义 summary

## CONDITIONAL_GO（条件通过）

- 合同字段与规则明确，但 monitoring/trace 的某些细粒度口径仅以占位形式存在（允许进入后续实现 phase），并保持边界不变。

## NO_GO（不通过）

任一触发：
- 被 block 的 evidence 直接删除而无 retention
- 重复信息仍被反复提炼为新候选（违反 reuse/duplicate 约束）
- OCR evidence 被跳过 delta/filter 直接进入任务链
- 生成最终语义总结或导航动作
- 接入真实 runtime/下游（违反 offline-only 边界）

