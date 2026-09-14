# Luna Evaluation — Post Crossing Decision Roadmap Decision v1

对应 phase：`Phase-Post-Crossing-Decision-Roadmap-Decision-v1-001`

## 运行命令

```bash
python3 tools/evaluation/midplatform/run_post_crossing_decision_roadmap_decision_v1.py
python3 tools/evaluation/midplatform/verify_post_crossing_decision_roadmap_decision_v1.py
```

runner 默认输出目录：

- `_eval_out/post_crossing_decision_roadmap_decision_v1_smoke_v0/`

## 输入 roots

必须加载：

- `_eval_out/crossing_decision_closure_v1_smoke_v0/`
- `_eval_out/crossing_decision_post_dryrun_review_v1_smoke_v0/`
- `_eval_out/crossing_decision_dryrun_v1_smoke_v0/`
- `_eval_out/crossing_decision_safety_governance_policy_v1_smoke_v0/`
- `_eval_out/luna_safety_constitution_policy_v1_smoke_v0/`
- `_eval_out/post_controlled_frame_input_roadmap_decision_v1_smoke_v0/`
- `_eval_out/controlled_frame_input_closure_v1_smoke_v0/`
- `_eval_out/map_location_readonly_context_policy_v1_smoke_v0/`
- `_eval_out/basic_navigation_loop_vision_strengthening_closure_v1_smoke_v0/`
- `_eval_out/minimal_runtime_integration_closure_v1_smoke_v0/`
- `_eval_out/ocr_mainline_final_closure_v1_smoke_v0/`

可选 root 不存在时必须标记 `optional_missing`，不得失败，不得伪造能力。

## 输出目录

`_eval_out/post_crossing_decision_roadmap_decision_v1_smoke_v0/`

必须包含：

- `summary.json`
- `input_root_matrix.json`
- `current_crossing_decision_status_summary.json`
- `completed_capability_summary.json`
- `route_option_matrix.json`
- `priority_ranking.json`
- `recommended_next_phase_decision.json`
- `deferred_gate_taxonomy_register.json`
- `deferred_resilience_distributed_midplatform_register.json`
- `deferred_worldmodel_memory_library_emotion_register.json`
- `boundary_freeze.json`
- `governance_debt_roadmap_register.json`
- `non_claims_register.json`
- `next_phase_recommendation.json`
- `no_runtime_boundary_report.json`
- `no_write_boundary_report.json`
- `verifier_report.json`

## Verifier Pass Requirements

`verify_post_crossing_decision_roadmap_decision_v1.py` 必须至少检查 `170` 项，baseline requirement 为 `130`。

必须验证：

- `route_option_count>=8`，且 `P0 / P1 / P2` 各自至少有 3 条路线
- `Controlled Frame Sample Planning` 被选为唯一 `selected_now=true`
- `gate_taxonomy_deferred=true` 且 `gate_taxonomy_project_optimization=true`
- Crossing Decision closure 状态为 closed 且 forbidden outputs absent
- 全部 runtime / write / action / speech 字段保持 `false`
- 最终判定固定为：
  - `final_decision=POST_CROSSING_DECISION_ROADMAP_DECISION_READY_FOR_CONTROLLED_FRAME_SAMPLE_PLANNING`
  - `recommended_next_phase=Phase-Controlled-Frame-Sample-Planning-v1-001`

