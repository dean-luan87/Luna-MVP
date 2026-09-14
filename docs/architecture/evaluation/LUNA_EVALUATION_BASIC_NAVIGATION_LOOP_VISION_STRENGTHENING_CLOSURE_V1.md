# Luna Evaluation — Basic Navigation Loop Vision Strengthening Closure v1

对应 phase：`Phase-Basic-Navigation-Loop-Vision-Strengthening-Closure-v1-001`

## 运行命令

```bash
python3 tools/evaluation/midplatform/run_basic_navigation_loop_vision_strengthening_closure_v1.py
python3 tools/evaluation/midplatform/verify_basic_navigation_loop_vision_strengthening_closure_v1.py
```

runner 默认输出目录：

- `_eval_out/basic_navigation_loop_vision_strengthening_closure_v1_smoke_v0/`

## 必须输入

- `_eval_out/basic_navigation_loop_vision_strengthening_post_dryrun_review_v1_smoke_v0/`
- `_eval_out/basic_navigation_loop_vision_strengthening_dryrun_v1_smoke_v0/`
- `_eval_out/visual_ocr_map_task_feedback_dryrun_v1_smoke_v0/`
- `_eval_out/selective_tracking_adapter_policy_v1_smoke_v0/`
- `_eval_out/world_observation_and_entity_feature_policy_v1_smoke_v0/`
- `_eval_out/task_aware_visual_focus_policy_v1_smoke_v0/`
- `_eval_out/midplatform_perception_orchestration_policy_v1_smoke_v0/`
- `_eval_out/return_to_vision_mainline_planning_v1_smoke_v0/`
- `_eval_out/return_to_vision_mainline_preplan_v1/`
- `_eval_out/minimal_runtime_integration_closure_v1_smoke_v0/`
- `_eval_out/ocr_mainline_final_closure_v1_smoke_v0/`

如存在，也加载：

- `_eval_out/basic_navigation_guidance_loop_stabilization_test_v1_smoke_v0/`
- `_eval_out/safety_task_arbitration_policy_v1_smoke_v0/`
- `_eval_out/navigation_guidance_speech_adapter_v1_smoke_v0/`
- `_eval_out/voice_interruption_governance_dryrun_v1_smoke_v0/`
- `_eval_out/voice_command_ownership_gate_policy_v1_smoke_v0/`

可选 root 不存在时必须标记 `optional_missing`，不得失败，不得伪造能力。

## 必须输出

- `summary.json`
- `input_root_matrix.json`
- `vision_strengthening_closure_summary.json`
- `completed_phase_matrix.json`
- `validated_capability_summary.json`
- `disabled_runtime_summary.json`
- `closure_boundary_freeze.json`
- `vision_strengthening_non_claims_register.json`
- `deferred_capability_pool.json`
- `governance_debt_carryover.json`
- `closure_readiness_gate.json`
- `next_phase_recommendation.json`
- `no_runtime_boundary_report.json`
- `no_write_boundary_report.json`
- `verifier_report.json`

## Verifier Pass Requirements

至少检查 200 项，baseline requirement = 160。

硬性检查：

- required input roots 全部加载
- `completed_phase_matrix_generated=true`
- `completed_phase_count>=9`
- `validated_capability_summary_generated=true`
- `disabled_runtime_summary_generated=true`
- `closure_boundary_freeze_generated=true`
- `non_claims_register_generated=true`
- `deferred_capability_pool_generated=true`
- `governance_debt_carryover_generated=true`
- `closure_readiness_gate_generated=true`
- `policy_chain_closed=true`
- `dryrun_chain_closed=true`
- `feedback_chain_closed=true`
- `navigation_loop_vision_strengthening_closed=true`
- `production_readiness_claimed=false`
- `live_navigation_claimed=false`
- `runtime_enablement_claimed=false`

runtime / write / action / speech 边界：

- `no_runtime_executed=true`
- `no_new_runtime_enabled=true`
- `camera_invoked=false`
- `visual_model_invoked=false`
- `map_api_invoked=false`
- `ocr_provider_invoked=false`
- `ocrrequest_submitted=false`
- `tracking_runtime_invoked=false`
- `optical_flow_runtime_invoked=false`
- `supervision_imported=false`
- `supervision_invoked=false`
- `bytetrack_imported=false`
- `bytetrack_invoked=false`
- `ocsort_imported=false`
- `ocsort_invoked=false`
- `safety_task_arbitration_runtime_invoked=false`
- `speech_gate_invoked=false`
- `vop_invoked=false`
- `tts_invoked=false`
- `user_heard_assumed=false`
- `task_state_committed_now=false`
- `navigation_action_triggered=false`
- `route_modified=false`
- `scene_delta_generated=false`
- `world_model_written=false`
- `memory_written=false`
- `library_written=false`
- `fact_written=false`
- `entity_resolution_runtime_invoked=false`
- `fact_admission_runtime_invoked=false`
- `memory_consolidation_invoked=false`
- `library_experience_commit_invoked=false`

特殊边界：

- `full_frame_ocr_allowed=false`
- `full_scene_tracking_allowed=false`
- `crowd_flow_follow_action_allowed=false`
- `crossing_action_instruction_allowed=false`
- `fixed_poi_commit_allowed=false`
- `identity_fact_allowed=false`
- `emotional_attachment_fact_allowed=false`
- `handoff_candidate_not_fact=true`
- `placeholder_not_runtime=true`
- `boundary_ok=true`
- `violations=[]`

governance debt：

- `governance_debt_carryover_generated=true`
- `future_midplatform_function_governance_required=true`
- `no_duplicate_governance_module_allowed=true`

## Ready / No-Go

通过时：

- `final_decision=BASIC_NAVIGATION_LOOP_VISION_STRENGTHENING_CLOSED_FOR_CURRENT_MAINLINE`
- `recommended_next_phase=Phase-Post-Vision-Strengthening-Roadmap-Decision-v1-001`

未通过时：

- 不得把本轮表述为 runtime-ready
- 不得把 closure 表述为 production-ready
