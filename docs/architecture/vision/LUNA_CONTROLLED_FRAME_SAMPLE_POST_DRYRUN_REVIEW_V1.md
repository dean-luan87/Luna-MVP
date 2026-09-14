# Luna — Controlled Frame Sample Post-DryRun Review v1

**Phase**：`Phase-Controlled-Frame-Sample-Post-DryRun-Review-v1-001`  
**性质**：review-only / audit / closure readiness（不进入样例 runtime）  
**输出目录**：`_eval_out/controlled_frame_sample_post_dryrun_review_v1_smoke_v0/`

## 阶段目标

本阶段只做 **post-dryrun review**，审查：

- `Controlled Frame Sample Planning v1` 的 manifest/schema/policy/boundary 是否被 dry-run 覆盖
- `Controlled Frame Sample DryRun v1` 的 16 场景覆盖是否完整
- allowed/restricted/blocked/manual_review 分类是否稳定
- 缺失 `source_chain` / 缺失 privacy precheck / unknown source 是否被阻断
- file boundary 是否稳定阻止打开/读取/解码/抽帧/真实 hash
- usage policy 是否阻止 training / production inference / runtime / write
- mapping 是否只生成 stub（不生成 VisualObservation/SceneSketch/OCR/Tracking 结果）
- no-runtime / no-write / no-action / no-speech 边界是否都成立
- 是否 ready for closure（且明确 `ready_for_real_image_read=false`、`ready_for_runtime=false`）

## 强边界（必须保持）

- 不读取真实图像/视频内容；不打开文件；不解码视频；不抽帧；不计算真实 hash  
- 不调用视觉模型 / OCR provider / map API / tracking runtime  
- 不写 `WorldModel / Memory / Fact / Library`；不生成 `Scene Delta`；不触发 `Navigation Action`  
- 不调用 `Speech Gate / VOP / TTS`

## 核心产物（review-only）

runner 必须写出：

- `summary.json`
- `input_root_matrix.json`
- `sample_dryrun_input_root_review.json`
- `sample_scenario_coverage_review.json`
- `sample_source_policy_review.json`
- `file_boundary_review.json`
- `privacy_precheck_review.json`
- `manual_review_gate_review.json`
- `sample_usage_policy_review.json`
- `sample_to_frame_mapping_review.json`
- `runtime_write_action_speech_boundary_review.json`
- `controlled_frame_sample_closure_readiness_decision.json`
- `governance_debt_review.json`
- `next_phase_recommendation.json`
- `no_runtime_boundary_report.json`
- `no_write_boundary_report.json`
- `verifier_report.json`

## 下一阶段

当 verifier=GO 时：

- `final_decision=CONTROLLED_FRAME_SAMPLE_POST_DRYRUN_REVIEW_READY_FOR_CLOSURE`
- `recommended_next_phase=Phase-Controlled-Frame-Sample-Closure-v1-001`

## 实施状态

`Phase-Controlled-Frame-Sample-Closure-v1-001` 已以 **closure-only** 形式落地并通过 smoke verifier：关账 planning+dryrun+post-review，冻结边界与 non-claims，仍不读内容、不打开文件、不进入视觉 runtime。

`Phase-Post-Controlled-Frame-Sample-Roadmap-Decision-v1-001` 已以 **roadmap-decision-only** 形式落地并通过 smoke verifier：只做路线裁决，明确下一阶段应先做 `Controlled Frame File Existence / Metadata Boundary Planning`（不读取图像内容）。

