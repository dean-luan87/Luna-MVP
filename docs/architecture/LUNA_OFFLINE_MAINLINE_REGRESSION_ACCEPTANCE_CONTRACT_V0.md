# LUNA Offline Mainline Regression Acceptance Contract v0

## Scope

冻结 EF-006 回归验收的 **硬门槛**、**允许波动项**、**不允许波动项**，作为后续改动的阻断基线。

## Hard thresholds (must pass)

### Chain

- normal_chain_complete_rate == 1.0
- fallback_chain_complete_rate == 1.0
- all_stage_complete_rates == 1.0

### Schema

- all_schema_valid_rates == 1.0（五阶段 perception/scene_context/scene_task/fusion/output）

### Source policy

- normal_source_distribution.yolo_shadow == 3（样本数 v0 固定 3）
- fallback_source_distribution.baseline_mock == 3
- fallback_reason_present_rate == 1.0（v0 允许用 fallback_count==3 作为 proxy）

### SceneContext

- scene_context_stage_complete_rate == 1.0
- gate_result_generated_rate == 1.0（v0：通过 stage outputs refs 不断裂作为 proxy）

### Output

- output_candidate_generated_rate == 1.0（v0：通过 stage refs 不断裂 + complete_rate 作为 proxy）
- real_tts_invoked_false_rate == 1.0
- allows_execute_now_false_all_stages_rate == 1.0

### Observability

- EF-005 required files 全存在
- broken_refs == 0
- EF-005 verifier all_pass == true

### Safety

All must be zero:

- execute_leakage_count_total
- default_on_leakage_count_total
- release_retry_reopen_leakage_count_total
- side_effects_expansion_count_total
- forced_navigation_action_count_total
- forbidden_output_semantic_count_total

### Evidence boundary

- evidence_type_preserved_rate == 1.0
- controlled_live_stream_false_rate == 1.0
- phone_local_capture_true_rate == 1.0
- pending_real_sidewalk_run_true_rate == 1.0
- evidence_type_mutation_count == 0
- pending_closed_count == 0

## Allowed variance (v0, not a blocker)

- detection_count_total 可变化
- detected class distribution 可变化
- message_text_candidate 可模板化
- SceneContext degraded_or_uncertain 可保持 true
- fusion/output policy 仍为 v0 minimal rules
- 样本数仍为 3
- report 无 UI/可视化

## Not allowed (any is NO_GO)

- candidate-only 被破坏
- real_tts_invoked=true
- allows_execute_now=true
- pending_real_sidewalk_run=false
- controlled_live_stream=true
- evidence_type 被改写
- fallback path 不可用
- source policy audit 字段缺失（导致无法得出 source 分布）
- trace/replay/whitebox index 缺失
- safety leakage 非 0

