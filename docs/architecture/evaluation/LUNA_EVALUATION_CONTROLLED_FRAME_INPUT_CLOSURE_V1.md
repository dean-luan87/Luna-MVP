# Luna Evaluation — Controlled Frame Input Closure v1

对应 phase：`Phase-Controlled-Frame-Input-Closure-v1-001`

## 运行命令

```bash
python3 tools/evaluation/vision/run_controlled_frame_input_closure_v1.py
python3 tools/evaluation/vision/verify_controlled_frame_input_closure_v1.py
```

## 输入 roots

必须加载：

- `_eval_out/controlled_frame_input_post_dryrun_review_v1_smoke_v0/`
- `_eval_out/controlled_frame_input_dryrun_v1_smoke_v0/`
- `_eval_out/controlled_frame_input_planning_v1_smoke_v0/`
- `_eval_out/map_location_readonly_context_policy_v1_smoke_v0/`
- `_eval_out/post_vision_strengthening_roadmap_decision_v1_smoke_v0/`
- `_eval_out/basic_navigation_loop_vision_strengthening_closure_v1_smoke_v0/`
- `_eval_out/task_aware_visual_focus_policy_v1_smoke_v0/`
- `_eval_out/midplatform_perception_orchestration_policy_v1_smoke_v0/`
- `_eval_out/minimal_runtime_integration_closure_v1_smoke_v0/`
- `_eval_out/ocr_mainline_final_closure_v1_smoke_v0/`

可选加载：

- `Vision Frame Trace / Stream Registry`
- `Vision Frame Input Governance`
- `Vision ROI Proposal Stub`
- `System Health / Hardware Profile`
- `Simulation Lab profile`

## 输出目录

runner 输出目录固定为：

`_eval_out/controlled_frame_input_closure_v1_smoke_v0/`

必须包含：

- `summary.json`
- `input_root_matrix.json`
- `controlled_frame_input_closure_summary.json`
- `completed_phase_matrix.json`
- `validated_capability_summary.json`
- `disabled_runtime_summary.json`
- `closure_boundary_freeze.json`
- `controlled_frame_input_non_claims_register.json`
- `deferred_capability_pool.json`
- `governance_debt_carryover.json`
- `closure_readiness_gate.json`
- `next_phase_recommendation.json`
- `no_runtime_boundary_report.json`
- `no_write_boundary_report.json`
- `verifier_report.json`

## Verifier Pass Requirements

`verify_controlled_frame_input_closure_v1.py` 必须至少检查 `180` 项，baseline requirement 为 `140`。

必须验证：

1. 输入加载成功：`post_dryrun_review / dryrun / planning / map_location_readonly_context / post_vision_strengthening_roadmap_decision / vision_strengthening_closure / task_aware_visual_focus / midplatform_perception_orchestration / minimal_runtime_integration_closure / ocr_final_closure`
2. closure 产物齐全：`completed_phase_matrix / validated_capability_summary / disabled_runtime_summary / closure_boundary_freeze / non_claims_register / deferred_capability_pool / governance_debt_carryover / closure_readiness_gate`
3. 链路收口成立：`controlled_frame_input_planning_closed / controlled_frame_input_dryrun_closed / controlled_frame_input_post_review_closed / controlled_frame_input_closed`
4. 非主张仍成立：`controlled_sample_planning_started=false`、`live_camera_claimed=false`、`visual_runtime_claimed=false`、`image_read_claimed=false`、`production_readiness_claimed=false`
5. runtime / write / action / speech 边界全部为 `false`
6. handoff 冻结仍成立：`frame_to_ocr_requires_visual_focus=true`、`frame_to_tracking_requires_visual_focus=true`、`frame_to_world_observation_requires_policy=true`
7. dual-device 仍是 placeholder：`dual_device_redundant_perception_placeholder_retained=true`、`hardware_stage_deferred=true`
8. governance debt carryover 成立：`future_midplatform_function_governance_required=true`、`future_midplatform_resilience_governance_required=true`、`no_duplicate_governance_module_allowed=true`
9. 最终判定固定为：
   - `final_decision=CONTROLLED_FRAME_INPUT_CLOSED_FOR_CURRENT_MAINLINE`
   - `recommended_next_phase=Phase-Post-Controlled-Frame-Input-Roadmap-Decision-v1-001`

## 通过语义

本阶段通过只表示：

- `Controlled Frame Input Planning + DryRun + Post-DryRun Review` 已完成正式 closure
- 当前边界已经冻结
- 下一阶段应先进入 `Post-Controlled-Frame-Input-Roadmap-Decision`

本阶段通过不表示：

- 已开放 live camera
- 已开放真实视觉 runtime
- 已开放真实图像读取
- 已进入 controlled sample planning
- 已达到 production readiness
