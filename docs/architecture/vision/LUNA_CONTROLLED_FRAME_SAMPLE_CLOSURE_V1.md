# Luna — Controlled Frame Sample Closure v1

**Phase**：`Phase-Controlled-Frame-Sample-Closure-v1-001`  
**性质**：closure-only / status freeze / boundary freeze / non-claims register / deferred capability pool  
**输出目录**：`_eval_out/controlled_frame_sample_closure_v1_smoke_v0/`

## 阶段意义

本阶段对 `Controlled Frame Sample` 链进行正式关账：

- Planning → DryRun → Post-DryRun Review 已形成完整闭环
- 明确 **样例链 = manifest-level governance**，并且：
  - **不等于真实图像/视频读取**
  - **不等于视觉 runtime**
  - **不等于可用于生产推理或训练**

## 强边界（必须冻结）

- 不读取真实图像/视频内容；不打开文件；不解码视频；不抽帧；不计算真实 hash  
- 不调用视觉模型 / OCR provider / map API / tracking runtime / crossing runtime  
- 不写 `WorldModel / Memory / Fact / Library`；不生成 `Scene Delta`；不触发 `Navigation Action`  
- 不调用 `Speech Gate / VOP / TTS`

## 核心产物

runner 必须写出：

- `controlled_frame_sample_closure_summary.json`
- `completed_phase_matrix.json`
- `validated_capability_summary.json`
- `disabled_runtime_summary.json`
- `closure_boundary_freeze.json`
- `controlled_frame_sample_non_claims_register.json`
- `deferred_capability_pool.json`
- `governance_debt_carryover.json`
- `closure_readiness_gate.json`
- `next_phase_recommendation.json`
- `summary.json` / `input_root_matrix.json`

## 下一阶段

当 verifier=GO 时：

- `final_decision=CONTROLLED_FRAME_SAMPLE_CLOSED_FOR_CURRENT_MAINLINE`
- `recommended_next_phase=Phase-Post-Controlled-Frame-Sample-Roadmap-Decision-v1-001`

## 实施状态（后续落地）

`Phase-Post-Controlled-Frame-Sample-Roadmap-Decision-v1-001` 已以 **roadmap-decision-only** 形式落地并通过 smoke verifier：只做路线裁决与边界冻结，最终推荐下一阶段为 `Phase-Controlled-Frame-File-Metadata-Boundary-Planning-v1-001`（仍不读取图像内容、不打开文件）。

`Phase-Controlled-Frame-File-Metadata-Boundary-Planning-v1-001` 已以 **planning-only** 形式落地：补齐 manifest 与真实文件之间的 metadata 边界层，下一阶段为 metadata-only dry-run。

