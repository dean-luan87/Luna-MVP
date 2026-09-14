# Luna — Evaluation: Return To Vision Mainline Planning v1

```bash
python3 tools/evaluation/vision/run_return_to_vision_mainline_planning_v1.py \
  --workspace-root /Users/luanlei/Desktop/Luna-Workspace-Min \
  --output-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/return_to_vision_mainline_planning_v1_smoke_v0 \
  --preplan-input-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/return_to_vision_mainline_preplan_v1 \
  --ocr-final-closure-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/ocr_mainline_final_closure_v1_smoke_v0 \
  --minimal-runtime-integration-closure-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/minimal_runtime_integration_closure_v1_smoke_v0

python3 tools/evaluation/vision/verify_return_to_vision_mainline_planning_v1.py \
  --output-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/return_to_vision_mainline_planning_v1_smoke_v0
```

## 目标

验证 `Phase-Return-To-Vision-Mainline-Planning-v1-001` 是否已经把 preplan 结果正式冻结为：

- 正式主线名称
- roadmap
- 复用承诺
- 禁建清单
- 边界矩阵
- 第一批 phase 定义
- 暂缓能力登记
- 非主张清单
- formal readiness gate

## 产物要求

输出目录：

- `_eval_out/return_to_vision_mainline_planning_v1_smoke_v0/`

必须包含：

- `summary.json`
- `input_root_matrix.json`
- `vision_mainline_planning_report.json`
- `vision_mainline_roadmap.json`
- `adopted_preplan_principles.json`
- `rejected_patterns_register.json`
- `midplatform_reuse_commitment.json`
- `duplicate_module_ban_list.json`
- `governance_boundary_matrix.json`
- `first_batch_phase_definitions.json`
- `deferred_capability_register.json`
- `deferred_worldmodel_memory_library_boundary.json`
- `worldmodel_memory_library_placeholder_plan.json`
- `vision_mainline_non_claims_register.json`
- `formal_readiness_gate.json`
- `next_phase_recommendation.json`
- `no_runtime_boundary_report.json`
- `no_write_boundary_report.json`
- `verifier_report.json`

## 通过要求

至少确认：

- `formal_mainline_name=Task-Aware Perception Orchestration`
- `planning_report_generated=true`
- `roadmap_generated=true`
- `midplatform_reuse_commitment_generated=true`
- `duplicate_module_ban_list_generated=true`
- `governance_boundary_matrix_generated=true`
- `first_batch_phase_definitions_generated=true`
- `deferred_capability_register_generated=true`
- `deferred_worldmodel_memory_library_boundary_generated=true`
- `worldmodel_memory_library_placeholder_plan_generated=true`
- `non_claims_register_generated=true`
- `formal_readiness_gate_generated=true`
- `entity_resolution_deferred=true`
- `fact_admission_deferred=true`
- `memory_consolidation_deferred=true`
- `library_experience_governance_deferred=true`
- `worldmodel_handoff_candidate_allowed=true`
- `memory_handoff_candidate_allowed=true`
- `library_handoff_placeholder_allowed=true`
- `recommended_next_phase=Phase-MidPlatform-Perception-Orchestration-Policy-v1-001`

## 边界要求

本阶段必须继续保持：

- `no_runtime_executed=true`
- `no_new_capability_implemented=true`
- `camera_invoked=false`
- `map_api_invoked=false`
- `ocr_provider_invoked=false`
- `tracking_runtime_invoked=false`
- `optical_flow_runtime_invoked=false`
- `world_model_written=false`
- `memory_written=false`
- `library_write_allowed=false`
- `fact_written=false`
- `entity_fusion_runtime_allowed=false`
- `fact_admission_runtime_allowed=false`
- `handoff_candidate_not_fact=true`
- `placeholder_not_runtime=true`
- `scene_delta_generated=false`
- `task_state_committed_now=false`
- `navigation_action_triggered=false`

## 最终目标

如果 verifier 为 `GO`，则说明 Luna 已从 `Return-To-Vision Mainline Preplan v1` 正式进入“视觉主线规划冻结”，并且下一阶段可以切入：

- `Phase-MidPlatform-Perception-Orchestration-Policy-v1-001`
