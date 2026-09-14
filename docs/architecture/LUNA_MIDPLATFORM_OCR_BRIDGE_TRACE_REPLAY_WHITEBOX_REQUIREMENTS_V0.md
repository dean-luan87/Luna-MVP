# LUNA — MidPlatform OCR Bridge Trace/Replay/Whitebox Requirements v0

## Phase

- **Phase-ModelOCR-MidPlatform-Bridge-001-Fix**

## Trace（观测字段）

MidPlatform evidence layer 在做 filtering/blocking/delta control 时，trace 至少应包含：
- `evidence_id`
- `delta_control_id`
- `text_signature`
- `layout_signature`
- `visual_text_relevance_class`
- `delta_status`
- `delta_decision`
- `filter_result_id`
- `block_applied`
- `block_reason`
- `block_level`
- `readability_status`（低价值/不确定视觉文本 contract 可追责字段）
- `meaning_status`（低价值/不确定视觉文本 contract 可追责字段）
- `requires_better_frame`（低价值/不确定视觉文本必须复核时为 true）
- `uncertainty_reason`（不确定原因的占位/可追责字符串）
- `candidate_generated`（是否产生 `MidPlatformTextExtractionCandidate` ）
- `task_candidate_allowed`（是否允许进入任务相关候选）
- `world_context_candidate_created`（是否产生 `WorldModelContextEvidence` 候选）
- `world_context_evidence_id`
- `world_model_write_policy`
- `expiry_policy`
- `requires_revalidation`
- `allowed_when_user_requested`
- `ambient_context_candidate_created`（是否产生 `AmbientContextCandidate` ）
- `ambient_context_candidate_id`
- `ambient_context_candidate_context_type`
- `allowed_for_primary_task_decision`（必须为 false；ambient 信息不得改变导航主路径）
- `speech_priority`
- `ambient_expiry_policy`
- `ambient_requires_revalidation`

## Replay（可追溯性字段）

Replay 记录要求：
- `raw_evidence_ref`（输入 evidence 的证据引用）
- `previous_result_ref`（复用旧结果引用，若有）
- `signature_inputs_ref`（签名输入字段证据引用）
- `delta_decision_ref`
- `filter_result_ref`
- `world_context_policy_decision_ref`
- `ambient_context_policy_decision_ref`

## Whitebox（可解释字段）

Whitebox 记录要求：
- `why_reused`（reuse_previous/ignore_duplicate 的依据；必须引用 text/layout signatures）
- `why_blocked`（命中 block_reason 的依据；必须引用治理与 contract 检查结果）
- `why_relevance_class`（visual_text_relevance_class 命中依据；必须引用广告/促销/背景触发线索或任务上下文 override 事件）
- `why_reprocessed`（full_reprocess/partial_update 的依据）
- `why_uncertainty_handling`（当 evidence 落入 low-value/uncertain visual text 类别时，说明选择 hold_uncertain/soft_block 的原因）
- `why_world_context_written`（为何将非任务信息写入世界模型环境知识；必须引用 visual_text_relevance_class 与 user_requested_override）
- `why_ambient_context_created`（为何将商业/环境补充信息作为 ambient/ex enrichment 候选输出；必须引用 context_type 选择依据与 requires_user_context_match 判定）
- `confidence_thresholds`（涉及低置信/不确定阈值的配置快照）
- `reading_order_status`（line_order_status 与 reading_direction_candidate 相关状态）
- `task_context_snapshot_ref`（任务上下文引用快照；不含 runtime 行为）
- `governance_boundary_status`（边界检查通过/失败的证据）

## Non-governance boundaries

- 本阶段不定义任何 runtime 行为，不生成 navigation/action/semantic_summary。

