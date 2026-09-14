# Luna — Controlled Frame Sample DryRun v1

**Phase**：`Phase-Controlled-Frame-Sample-DryRun-v1-001`  
**性质**：manifest-metadata-only dry-run / candidate validation / boundary verification  
**输出目录**：`_eval_out/controlled_frame_sample_dryrun_v1_smoke_v0/`

## 阶段目标

本阶段只做 **sample manifest metadata** 的 dry-run，验证：

- allowed / restricted / blocked 样例能否被正确区分
- missing `source_chain` / missing privacy precheck / unknown source 是否被阻断
- sensitive sample 是否进入 manual review candidate
- file boundary 是否严格阻止真实文件打开与内容读取
- usage policy 是否保持 schema/manifest/future-dryrun 范围
- mapping policy 是否只能生成 `ControlledFrameInputCandidate` 的 **stub**（不读内容）

## 强边界（必须保持）

- 不读取真实图像/视频内容；不打开文件；不解码视频；不抽帧
- 不调用视觉模型 / OCR provider / map API / tracking runtime
- 不写 `WorldModel / Memory / Fact / Library`；不生成 `Scene Delta`；不触发 `Navigation Action`
- 不调用 `Speech Gate / VOP / TTS`

## 核心 dry-run 产物

runner 必须写出（见 `_eval_out/controlled_frame_sample_dryrun_v1_smoke_v0/`）：

- `summary.json`
- `input_root_matrix.json`
- `dryrun_case_schema.json`
- `sample_manifest_metadata_stub_schema.json`
- `sample_source_decision_candidate_schema.json`
- `file_boundary_decision_candidate_schema.json`
- `privacy_precheck_decision_candidate_schema.json`
- `manual_review_decision_candidate_schema.json`
- `sample_usage_decision_candidate_schema.json`
- `sample_to_frame_candidate_mapping_stub_schema.json`
- `controlled_frame_sample_dryrun_result_schema.json`
- `controlled_frame_sample_dryrun_scenario_matrix.json`（≥16 场景）
- `controlled_frame_sample_dryrun_results.json`
- `sample_file_boundary_check_results.json`
- `sample_privacy_precheck_results.json`
- `manual_review_gate_results.json`
- `sample_to_frame_mapping_stub_results.json`
- `sample_dryrun_boundary_matrix.json`
- `governance_debt_register.json`
- `next_phase_recommendation.json`
- `no_runtime_boundary_report.json`
- `no_write_boundary_report.json`
- `verifier_report.json`

## 场景矩阵（最低覆盖）

必须覆盖 16 个场景（至少）：

- 14 个与 planning 同名场景（allowed/restricted/blocked/review）
- `medical_context_sample_restricted`
- `workplace_sensitive_sample_restricted`

## 下一阶段

当 verifier=GO 时，本阶段输出：

- `final_decision=CONTROLLED_FRAME_SAMPLE_DRYRUN_READY_FOR_POST_DRYRUN_REVIEW`
- `recommended_next_phase=Phase-Controlled-Frame-Sample-Post-DryRun-Review-v1-001`

注意：本阶段与下一阶段都不读取真实图像内容，不打开文件。

## 实施状态

`Phase-Controlled-Frame-Sample-Post-DryRun-Review-v1-001` 已以 **review-only** 形式落地：只审查 planning+dryrun 产物稳定性与边界成立，不进入样例 runtime，不读内容、不打开文件。

