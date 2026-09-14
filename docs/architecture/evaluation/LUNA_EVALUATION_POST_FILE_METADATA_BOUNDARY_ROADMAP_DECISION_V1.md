# Luna Evaluation — Post File Metadata Boundary Roadmap Decision v1

**Phase**：`Phase-Post-File-Metadata-Boundary-Roadmap-Decision-v1-001`  
**输出目录**：`_eval_out/post_file_metadata_boundary_roadmap_decision_v1_smoke_v0/`

## 目标

本评测只验证“路线裁决”阶段的结构化产物、输入 roots 加载状态、严格边界冻结，以及最终推荐下一阶段是否为：

- `Phase-Controlled-Frame-File-Existence-Check-Guarded-Planning-v1-001`

## 运行命令（smoke）

运行 runner：

```bash
python tools/evaluation/midplatform/run_post_file_metadata_boundary_roadmap_decision_v1.py
```

运行 verifier：

```bash
python tools/evaluation/midplatform/verify_post_file_metadata_boundary_roadmap_decision_v1.py
```

## 关键产物清单

`_eval_out/post_file_metadata_boundary_roadmap_decision_v1_smoke_v0/` 必须包含：

- `summary.json`
- `input_root_matrix.json`
- `post_file_metadata_boundary_roadmap_decision.json`
- `current_file_metadata_boundary_status_summary.json`
- `completed_capability_summary.json`
- `route_option_matrix.json`
- `priority_ranking.json`
- `recommended_next_phase_decision.json`
- `deferred_gate_taxonomy_register.json`
- `deferred_real_image_read_register.json`
- `deferred_resilience_distributed_midplatform_register.json`
- `deferred_worldmodel_memory_library_emotion_register.json`
- `boundary_freeze.json`
- `governance_debt_roadmap_register.json`
- `non_claims_register.json`
- `next_phase_recommendation.json`
- `no_runtime_boundary_report.json`
- `no_write_boundary_report.json`
- `no_file_operation_boundary_report.json`
- `verifier_report.json`

## 通过判定

verifier 必须输出：

- `verifier=GO`
- `final_decision=POST_FILE_METADATA_BOUNDARY_ROADMAP_DECISION_READY_FOR_FILE_EXISTENCE_CHECK_GUARDED_PLANNING`
- `recommended_next_phase=Phase-Controlled-Frame-File-Existence-Check-Guarded-Planning-v1-001`

