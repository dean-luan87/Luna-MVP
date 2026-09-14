# LUNA — MidPlatform OCR Delta Monitoring Metrics v0

## Phase

- **Phase-ModelOCR-MidPlatform-Bridge-001-Fix**

## Monitoring ownership

指标归属：`Phase-MidPlatform-Monitoring-001`（Unified Capability Runtime Monitoring 方向）。

本补丁阶段只定义 metrics 字段与计数口径，不接监控系统 runtime。

## Metrics identity（冻结字段名）

建议 metrics 记录在 MidPlatform evidence layer 的 delta control + filtering 模块，并关联：
- `evidence_id`
- `delta_control_id`
- `filter_result_id`

## Metrics list（冻结）

- `evidence_received_count`
- `evidence_schema_valid_count`
- `duplicate_ignored_count`
- `reused_previous_count`
- `partial_update_count`
- `full_reprocess_count`
- `uncertain_held_count`
- `soft_block_count`
- `hard_block_count`
- `expired_skip_count`
- `task_relevant_text_candidate_count`
- `context_relevant_text_candidate_count`
- `advertisement_like_block_count`
- `promotional_text_block_count`
- `background_static_text_block_count`
- `world_context_text_candidate_count`
- `promotional_world_context_candidate_count`
- `commercial_context_candidate_count`
- `ambient_context_candidate_count`
- `experience_enrichment_candidate_count`
- `commercial_context_suppressed_count`
- `user_requested_commercial_readout_count`
- `commercial_context_expired_count`
- `user_requested_text_override_count`
- `world_model_low_priority_write_count`
- `world_model_revalidation_required_count`
- `taskchain_blocked_but_world_context_retained_count`
- `low_confidence_block_count`
- `illegible_text_count`
- `blurred_text_count`
- `graffiti_text_count`
- `fragmented_text_count`
- `decorative_text_count`
- `non_actionable_text_block_count`
- `meaning_uncertain_hold_count`
- `better_frame_required_count`
- `user_requested_uncertain_readout_count`
- `reading_order_uncertain_count`
- `relevance_reclassified_count`
- `task_context_override_count`
- `governance_violation_count`
- `delta_decision_distribution`
- `block_reason_distribution`
- `avg_delta_decision_latency_ms`

## Counting rules（口径要求）

1. `evidence_received_count`
- 每次进入 MidPlatform evidence layer 的 OCR evidence input 数。

2. `duplicate_ignored_count` / `reused_previous_count`
- 由 delta decision（reuse/duplicate）产生：对应 delta_decision=ignore_duplicate 或 reuse_previous。

3. `partial_update_count` / `full_reprocess_count`
- 由 delta_decision 产生：partial_update / full_reprocess。

4. `uncertain_held_count`
- delta_decision=hold_uncertain。

5. block 相关计数
- `soft_block_count`/`hard_block_count`/`expired_skip_count` 分别按 filter_result.block_level 归类。

6. relevance 分类计数（visual_text_relevance_class）
- advertisement_like_text 默认阻断：计入 `advertisement_like_block_count`
- promotional_text 默认阻断：计入 `promotional_text_block_count`
- background_static_text 默认阻断：计入 `background_static_text_block_count`
- task_relevant_text 进入候选：计入 `task_relevant_text_candidate_count`
- context_relevant_text 进入候选但 requires_further_validation=true：计入 `context_relevant_text_candidate_count`
- 当被 block 的证据因 task_context_override 重新分类/放行：计入 `relevance_reclassified_count` 与 `task_context_override_count`
- 低价值/不确定视觉文本计数（visual_text_relevance_class 分流；见 `LUNA_MIDPLATFORM_LOW_VALUE_UNCERTAIN_VISUAL_TEXT_HANDLING_POLICY_V0.md`）：
  - `illegible_text_count` / `blurred_text_count` / `graffiti_text_count` / `fragmented_text` / `decorative_text_count`：
    - 按对应 `visual_text_relevance_class` 归类计数
  - `non_actionable_text_block_count`：
    - 按 `visual_text_relevance_class=non_actionable_text` 且 `block_level` 为 soft_block 归类计数
  - `meaning_uncertain_hold_count`：
    - 按 `visual_text_relevance_class=meaning_uncertain_text` 且 `block_level=hold_uncertain` 归类计数
  - `better_frame_required_count`：
    - 按契约字段 `requires_better_frame=true` 归类计数
  - `user_requested_uncertain_readout_count`：
    - 按 `allowed_for_user_requested_readout=true` 且可读类为上述低价值/不确定类别时归类计数

7. world context 与用户覆盖相关计数
- `world_context_text_candidate_count`：
  - 当 evidence 被写入/暂存为 `WorldModelContextEvidence` 时计数（`visual_text_relevance_class=world_context_text`）。
- `promotional_world_context_candidate_count`：
  - 当证据来源类别为 `promotional_text` 且写入 world context candidate 时计数（默认策略应为 0）。
- `user_requested_text_override_count`：
  - 当 user_intent 命中“读一下这个牌子/看看广告写什么/这家店叫什么”等并将类别升级为 `user_requested_text` 时计数。
- `world_model_low_priority_write_count`：
  - 当 `world_model_write_policy=low_priority_candidate` 时计数。
- `world_model_revalidation_required_count`：
  - 当 `requires_revalidation=true` 时计数（除 user_confirmed_write 外）。
- `taskchain_blocked_but_world_context_retained_count`：
  - 当 `allowed_for_taskchain=false` 但仍生成/保留 `WorldModelContextEvidence` 时计数。

8. commercial/ambient/ex enrichment 候选相关计数
- `commercial_context_candidate_count`：
  - 当 `ambient_context_candidate_context_type=commercial_context_text` 时计数。
- `ambient_context_candidate_count`：
  - 当 `ambient_context_candidate_context_type=ambient_context_text` 时计数。
- `experience_enrichment_candidate_count`：
  - 当 `ambient_context_candidate_context_type=experience_enrichment_text` 时计数。
- `commercial_context_suppressed_count`：
  - 因 `requires_user_context_match=false` 或默认抑制策略而未生成 ambient candidate 时计数（placeholder）。
- `user_requested_commercial_readout_count`：
  - 当用户明确询问商业活动/折扣/促销并触发 `user_requested_text`，且 speech_priority=user_requested_only 时计数。
- `commercial_context_expired_count`：
  - 当短 TTL 到期后不再激活但仍留档为证据时计数（placeholder）。

（候选统计口径说明）
- `MidPlatformTextExtractionCandidate` 仅在 filtering/delta 通过后允许生成；
- 按 `visual_text_relevance_class` 归类到 `task_relevant_text_candidate_count` 或 `context_relevant_text_candidate_count`；
- 本阶段不定义单独的 `task_relevant_candidate_count` 字段。

## Delta decision latency

- `avg_delta_decision_latency_ms`：从 evidence 进入到 delta_decision 输出的耗时（定义为占位）。

