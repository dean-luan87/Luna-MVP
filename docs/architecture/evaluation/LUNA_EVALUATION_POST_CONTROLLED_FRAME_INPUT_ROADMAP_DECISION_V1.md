# Luna Evaluation — Post Controlled Frame Input Roadmap Decision v1

对应 phase：`Phase-Post-Controlled-Frame-Input-Roadmap-Decision-v1-001`

## 运行命令

```bash
python3 tools/evaluation/midplatform/run_post_controlled_frame_input_roadmap_decision_v1.py
python3 tools/evaluation/midplatform/verify_post_controlled_frame_input_roadmap_decision_v1.py
```

## 输入 roots

必须加载：

- `_eval_out/controlled_frame_input_closure_v1_smoke_v0/`
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

- `System Health / Hardware Profile`
- `Vision Frame Trace / Stream Registry`
- `Vision Frame Input Governance`
- `Safety Task Arbitration`
- crossing / traffic / safety 相关旧输出
- midplatform governance debt 相关输出

## 输出目录

runner 输出目录固定为：

`_eval_out/post_controlled_frame_input_roadmap_decision_v1_smoke_v0/`

必须包含：

- `summary.json`
- `input_root_matrix.json`
- `current_controlled_frame_input_status_summary.json`
- `completed_capability_summary.json`
- `route_option_matrix.json`
- `priority_ranking.json`
- `recommended_next_phase_decision.json`
- `deferred_resilience_distributed_midplatform_register.json`
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

`verify_post_controlled_frame_input_roadmap_decision_v1.py` 必须至少检查 `170` 项，baseline requirement 为 `130`。

必须验证：

1. 必需输入 roots 已全部加载成功
2. roadmap decision 产物已全部生成
3. `route_option_count>=8`，且 `P0 / P1 / P2` 各自至少有 3 条路线
4. `Crossing Decision Safety Governance`、`Controlled Frame Sample Planning`、`MidPlatform Function Governance`、`MidPlatform Resilience`、`Offline Distributed MidPlatform` 路线均存在
5. `selected_now` 只有 1 条，且必须是 `Crossing Decision Safety Governance Policy`
6. `exploration_drive_deferred=true`
7. `midplatform_resilience_deferred=true`
8. `offline_distributed_midplatform_deferred=true`
9. `worldmodel_candidate_layer_deferred=true`
10. `memory_library_governance_deferred=true`
11. `emotion_engine_deferred=true`
12. `controlled_sample_planning_started=false`
13. `live_camera_claimed=false`
14. `visual_runtime_claimed=false`
15. `image_read_claimed=false`
16. `production_readiness_claimed=false`
17. 全部 runtime / write / action / speech 字段保持 `false`
18. `boundary_ok=true`
19. 最终判定固定为：
   - `final_decision=POST_CONTROLLED_FRAME_INPUT_ROADMAP_DECISION_READY_FOR_CROSSING_DECISION_SAFETY_GOVERNANCE_POLICY`
   - `recommended_next_phase=Phase-Crossing-Decision-Safety-Governance-Policy-v1-001`

## 通过语义

本阶段通过只表示：

- `Controlled Frame Input` 收口后，Luna 已正式完成下一阶段路线裁决
- 当前不进入 controlled sample planning
- 当前仍然不读取真实图像内容
- 当前仍然不进入 runtime
- 下一阶段应优先进入 `Crossing Decision Safety Governance Policy`

本阶段通过不表示：

- 已开放 live camera
- 已开放 controlled sample reading
- 已开放 map API
- 已开放视觉 runtime
- 已达到 production readiness
