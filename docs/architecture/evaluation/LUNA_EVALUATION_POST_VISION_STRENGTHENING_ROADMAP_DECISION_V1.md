# Luna Evaluation — Post Vision Strengthening Roadmap Decision v1

对应 phase：`Phase-Post-Vision-Strengthening-Roadmap-Decision-v1-001`

## 运行命令

```bash
python3 tools/evaluation/midplatform/run_post_vision_strengthening_roadmap_decision_v1.py
python3 tools/evaluation/midplatform/verify_post_vision_strengthening_roadmap_decision_v1.py
```

runner 默认输出目录：

- `_eval_out/post_vision_strengthening_roadmap_decision_v1_smoke_v0/`

## 必须输入

- `_eval_out/basic_navigation_loop_vision_strengthening_closure_v1_smoke_v0/`
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
- previous map / gps / route context dry-run or policy outputs if any

可选 root 不存在时必须标记 `optional_missing`，不得失败，不得伪造能力。

## 必须输出

- `summary.json`
- `input_root_matrix.json`
- `current_mainline_status_summary.json`
- `completed_capability_summary.json`
- `route_option_matrix.json`
- `priority_ranking.json`
- `recommended_next_phase_decision.json`
- `deferred_exploration_drive_register.json`
- `deferred_worldmodel_memory_library_emotion_register.json`
- `boundary_freeze.json`
- `governance_debt_roadmap_register.json`
- `non_claims_register.json`
- `next_phase_recommendation.json`
- `no_runtime_boundary_report.json`
- `no_write_boundary_report.json`
- `verifier_report.json`

## Verifier Pass Requirements

至少检查 160 项，baseline requirement = 120。

硬性检查：

输入检查：

- `vision_strengthening_closure_input_loaded=true`
- `post_dryrun_review_input_loaded=true`
- `dryrun_input_loaded=true`
- `visual_ocr_map_task_feedback_input_loaded=true`
- `selective_tracking_input_loaded=true`
- `world_observation_entity_feature_input_loaded=true`
- `task_aware_visual_focus_input_loaded=true`
- `midplatform_perception_orchestration_input_loaded=true`
- `minimal_runtime_integration_closure_loaded=true`
- `ocr_final_closure_loaded=true`

roadmap 产物检查：

- `current_mainline_status_summary_generated=true`
- `completed_capability_summary_generated=true`
- `route_option_matrix_generated=true`
- `priority_ranking_generated=true`
- `recommended_next_phase_decision_generated=true`
- `deferred_exploration_drive_register_generated=true`
- `deferred_worldmodel_memory_library_emotion_register_generated=true`
- `boundary_freeze_generated=true`
- `governance_debt_roadmap_register_generated=true`
- `non_claims_register_generated=true`

路线检查：

- `route_option_count>=8`
- `p0_route_count>=3`
- `p1_route_count>=2`
- `p2_route_count>=3`
- `Map / Location Read-Only Context` route exists
- `Controlled Frame Input` route exists
- `Crossing Decision Safety Governance` route exists
- `MidPlatform Function Governance` route exists
- `Exploration Drive` route exists
- `WorldModel Candidate Layer` route exists
- `Memory / Library Governance` route exists
- `Emotion Map / Affective Engine` route exists

deferred 检查：

- `exploration_drive_deferred=true`
- `task_driven_perception_priority_first=true`
- `worldmodel_candidate_layer_deferred=true`
- `memory_library_governance_deferred=true`
- `emotion_engine_deferred=true`

非主张检查：

- `live_navigation_claimed=false`
- `production_readiness_claimed=false`
- `runtime_enablement_claimed=false`

runtime / write / action / speech 检查：

- `no_runtime_executed=true`
- `no_new_runtime_enabled=true`
- `camera_invoked=false`
- `visual_model_invoked=false`
- `map_api_invoked=false`
- `ocr_provider_invoked=false`
- `ocrrequest_submitted=false`
- `tracking_runtime_invoked=false`
- `optical_flow_runtime_invoked=false`
- `supervision_invoked=false`
- `bytetrack_invoked=false`
- `ocsort_invoked=false`
- `speech_gate_invoked=false`
- `vop_invoked=false`
- `tts_invoked=false`
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
- `emotion_engine_invoked=false`
- `boundary_ok=true`
- `violations=[]`

readiness 检查：

- `final_decision=POST_VISION_STRENGTHENING_ROADMAP_DECISION_READY_FOR_MAP_LOCATION_READONLY_CONTEXT_POLICY`
- `recommended_next_phase=Phase-Map-Location-ReadOnly-Context-Policy-v1-001`

## Ready / No-Go

通过时：

- `verifier=GO`
- `final_decision=POST_VISION_STRENGTHENING_ROADMAP_DECISION_READY_FOR_MAP_LOCATION_READONLY_CONTEXT_POLICY`
- `recommended_next_phase=Phase-Map-Location-ReadOnly-Context-Policy-v1-001`

未通过时：

- 不得把本阶段表述为 runtime-ready
- 不得把本阶段表述为 live-navigation-ready
- 不得把 roadmap decision 表述为 production-ready
