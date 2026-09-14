# Luna — Controlled Frame Sample Planning v1

**Phase**：`Phase-Controlled-Frame-Sample-Planning-v1-001`  
**性质**：planning-only / manifest schema & governance boundary only  
**输出目录**：`_eval_out/controlled_frame_sample_planning_v1_smoke_v0/`

## 阶段目标

本阶段只定义后续“受控真实文件 / 静态图 / 预录帧样例”如何进入 Luna 测试链（manifest-level），包括：

- sample manifest schema
- sample source policy（allowed / restricted / blocked）
- file boundary（manifest-only；不打开文件）
- privacy precheck（基于 metadata stub / 标签 / 目录类，不读取内容）
- manual review gate
- sample usage policy（允许/禁止用途）
- sample-to-frame-candidate mapping policy（仅 stub 映射，不读取内容）

## 硬边界（必须保持）

- 不读取真实图像/视频内容；不打开文件；不解码视频；不抽帧  
- 不调用视觉模型；不调用 OCR provider；不提交 `OCRRequest`  
- 不调用地图 API / 高德 API；不进入 GPS / tracking / optical flow runtime  
- 不导入或调用 `Supervision / ByteTrack / OC-SORT`  
- 不写 `WorldModel / Memory / Fact / Library`；不生成 `Scene Delta`；不触发 `Navigation Action`  
- 不调用 `Speech Gate / VOP / TTS`；不输出真实可听语音

## 核心产物（manifest-level）

runner 必须写出（见 `_eval_out/controlled_frame_sample_planning_v1_smoke_v0/`）：

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
- `controlled_frame_sample_planning_scenario_matrix.json`（≥14 场景）
- `sample_planning_boundary_matrix.json`
- `governance_debt_register.json`
- `next_phase_recommendation.json`
- `no_runtime_boundary_report.json`
- `no_write_boundary_report.json`

## 场景矩阵（最低覆盖）

必须覆盖 14 个场景（allowed/restricted/blocked/manual_review）并保证全程 manifest-only：

1. `static_image_manifest_allowed`
2. `prerecorded_video_manifest_allowed`
3. `simulation_frame_manifest_allowed`
4. `synthetic_image_manifest_allowed`
5. `controlled_uploaded_image_restricted`
6. `private_home_sample_restricted`
7. `screen_document_sample_restricted`
8. `child_or_school_sample_restricted`
9. `live_camera_sample_blocked`
10. `external_stream_sample_blocked`
11. `missing_source_chain_blocked`
12. `missing_privacy_precheck_blocked`
13. `crossing_related_sample_requires_review`
14. `unknown_source_sample_blocked`

## 下一阶段

当 verifier=GO 时，本阶段输出：

- `final_decision=CONTROLLED_FRAME_SAMPLE_PLANNING_READY_FOR_CONTROLLED_FRAME_SAMPLE_DRYRUN`
- `recommended_next_phase=Phase-Controlled-Frame-Sample-DryRun-v1-001`

注意：下一阶段也只能读取 **manifest metadata**，仍不读取真实图像内容。

## 实施状态

`Phase-Controlled-Frame-Sample-DryRun-v1-001` 已以 **manifest-metadata-only** 形式落地：只构造/读取 manifest stub，验证 source/privacy/manual review/usage/mapping stub，仍不打开文件、不解码、不抽帧、不做视觉推理。

`Phase-Controlled-Frame-Sample-Post-DryRun-Review-v1-001` 已以 **review-only** 形式落地：只审查 planning+dryrun 稳定性与边界成立，并给出 closure readiness 决策。

