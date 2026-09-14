# Luna Evaluation — Controlled Frame Sample Planning v1

**Phase**：`Phase-Controlled-Frame-Sample-Planning-v1-001`  
**性质**：planning-only（manifest/schema/policy/boundary），不进入 runtime  
**输出目录**：`_eval_out/controlled_frame_sample_planning_v1_smoke_v0/`

## 运行命令（smoke）

runner：

```bash
python3 tools/evaluation/vision/run_controlled_frame_sample_planning_v1.py
```

verifier：

```bash
python3 tools/evaluation/vision/verify_controlled_frame_sample_planning_v1.py
```

## 产物清单（必须存在）

- `summary.json`
- `input_root_matrix.json`
- `controlled_frame_sample_planning_policy.json`
- `controlled_frame_sample_manifest_schema.json`
- `sample_source_policy.json`
- `file_boundary_policy.json`
- `privacy_precheck_policy.json`
- `manual_review_gate_policy.json`
- `sample_usage_policy.json`
- `sample_to_frame_candidate_mapping_policy.json`
- `controlled_frame_sample_planning_scenario_matrix.json`
- `sample_planning_boundary_matrix.json`
- `governance_debt_register.json`
- `next_phase_recommendation.json`
- `no_runtime_boundary_report.json`
- `no_write_boundary_report.json`
- `verifier_report.json`

## 判定语义

通过 verifier（GO）时：

- `final_decision=CONTROLLED_FRAME_SAMPLE_PLANNING_READY_FOR_CONTROLLED_FRAME_SAMPLE_DRYRUN`
- `recommended_next_phase=Phase-Controlled-Frame-Sample-DryRun-v1-001`

本阶段强制保证：

- manifest-only；`content_read_allowed_now=false`
- 不打开/不读取图片与视频；不解码/不抽帧
- 不调用视觉模型 / OCR provider / map API / tracking runtime
- 不写入 `WorldModel / Memory / Fact / Library`

