# LUNA — Scene Delta Monitoring & Observability Requirements v0

## Phase

- **Phase-MidPlatform-SceneDelta-001**

## Purpose

冻结 Scene Delta 的监控指标（metrics）与 Trace/Replay/Whitebox 最小可观测性要求。

本阶段只定义字段与口径，不接监控系统、不做 runtime。

## Metrics（冻结字段名）

定义 `SceneDeltaMetrics`：

- `delta_input_count`
- `new_count`
- `unchanged_count`
- `changed_count`
- `duplicate_count`
- `uncertain_count`
- `expired_count`
- `contradicted_count`
- `task_context_changed_count`

- `reuse_previous_count`
- `ignore_duplicate_count`
- `partial_update_count`
- `full_reprocess_count`
- `hold_uncertain_count`
- `expire_and_reprocess_count`
- `hard_block_count`

- `task_context_changed_reprocess_count`
- `world_context_revalidation_count`
- `commercial_expiry_recheck_count`
- `avg_delta_decision_latency_ms`

（时空锚点与重复证据压缩新增指标）

- `spatiotemporal_anchor_created_count`
- `anchor_reidentified_count`
- `same_content_same_place_count`
- `new_content_same_place_count`
- `content_replaced_count`
- `content_removed_count`
- `carrier_changed_count`
- `duplicate_evidence_compressed_count`
- `full_reprocess_saved_count`
- `individual_compression_record_count`
- `hive_candidate_compression_count`
- `cold_storage_evidence_count`
- `world_change_candidate_count`
- `stale_content_detected_count`
- `expired_content_recheck_count`

计数原则（冻结）：

- status 类计数按 `SceneDeltaDecision.delta_status` 归类
- action 类计数按 `SceneDeltaDecision.delta_action` 归类
- `hard_block_count` 仅用于 `delta_action=block`

## Trace / Replay / Whitebox（冻结最小字段）

### Trace must include

- `delta_input_id`
- `matched_previous_state_ref`
- `signature_comparison_result`（exact/near/changed/unstable/expired/contradicted）
- `delta_status`
- `delta_action`
- `decision_reason`
- `task_context_changed`
- `allowed_to_downstream_candidate`

（时空锚点与压缩字段）

- `spatiotemporal_anchor_id`
- `anchor_type`
- `spatial_signature`
- `content_signature`
- `compression_record_id`
- `duplicate_count`
- `storage_level`
- `world_change_candidate_created`

### Replay must include

- `current_input_ref`
- `previous_state_ref`
- `signature_inputs_ref`
- `comparison_result_ref`
- `thresholds_ref`
- `delta_decision_ref`

（压缩回放字段）

- `canonical_evidence_ref`
- `duplicate_evidence_refs`
- `compression_method`
- `retained_sample_refs`
- `previous_content_ref`
- `current_content_ref`

### Whitebox must include

- `why_reused`
- `why_ignored`
- `why_partial_update`
- `why_full_reprocess`
- `why_held_uncertain`
- `why_expired`
- `why_blocked`
- `which_signature_changed`

（锚点/压缩可解释字段）

- `why_same_anchor`
- `why_duplicate`
- `why_compressed`
- `why_content_changed`
- `why_reprocess_skipped`
- `why_world_change_candidate_created`

## Non-governance boundary checks（必须可观测）

Scene Delta 的白盒/审计必须能证明：

- 未触发任何执行/下游调用
- 未产出 navigation action
- 未触发真实播报
- 未写入真实世界模型

