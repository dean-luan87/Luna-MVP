# Luna — Post Crossing Decision Roadmap Decision v1

**Phase**：`Phase-Post-Crossing-Decision-Roadmap-Decision-v1-001`  
**性质**：roadmap decision / prioritization / boundary freeze only  
**边界**：不实现 runtime，不读取真实图像内容，不打开摄像头，不调用视觉模型，不调用 `OCR provider`，不提交 `OCRRequest`，不调用地图 API / 高德 API，不调用 GPS runtime，不调用 tracking runtime，不调用 optical flow runtime，不导入或调用 `Supervision / ByteTrack / OC-SORT`，不写 `Memory` / `WorldModel` / `Fact` / `Library`，不做 `entity resolution`，不做 `fact admission`，不做 `memory consolidation`，不做 `library experience commit`，不生成 `Scene Delta`，不提交 `Task State`，不触发 `Navigation Action`，不调用 `Speech Gate / VOP / TTS`，不输出真实用户可听语音

## 目标

本阶段只回答：

1. Crossing Decision closure 后当前主线状态是什么  
2. 下一步是否应该回到 Controlled Frame Sample Planning  
3. Gate Taxonomy / Gate Requirement Framework 是否应优先  
4. MidPlatform Function Governance / Consolidation 是否应优先  
5. MidPlatform Resilience / Robustness 是否应现在做 preplan  
6. Offline Distributed MidPlatform 是否继续作为 future architecture candidate  
7. WorldModel / Memory / Library / Exploration / Emotion 是否继续 deferred  
8. 最终 `recommended_next_phase` 是什么

## Current Crossing Decision Status

当前主线状态总结：

- `crossing_decision_closed=true`
- `forbidden_crossing_outputs_absent=true`
- `crossing_runtime_claimed=false`
- `real_crossing_judgment_claimed=false`
- `safe_to_cross_capability_claimed=false`
- `production_readiness_claimed=false`
- `runtime_enablement_claimed=false`

这表示：

- Crossing Decision 治理链已阶段性收口
- 当前主线的关键含义是：禁止过街许可输出，而不是具备过街判断能力

## Route Option Matrix

本阶段正式评估以下路线：

### P0

1. `Controlled Frame Sample Planning`（selected_now=true）
2. `Gate Taxonomy / Gate Requirement Framework`（project optimization；deferred）
3. `MidPlatform Function Governance / Consolidation`（deferred）

### P1

4. `MidPlatform Resilience / Robustness Preplan`（deferred）
5. `Offline Distributed MidPlatform Architecture Preplan`（deferred）
6. `Minimal Controlled Visual Runtime Planning`（deferred）

### P2

7. `WorldModel Candidate Layer / Memory / Library Governance`（deferred）
8. `Exploration Drive Policy`（deferred）
9. `Emotion Map / Affective Engine`（deferred）

## Why Controlled Frame Sample Planning Now

本阶段最终选择：

- `selected_next_phase=Phase-Controlled-Frame-Sample-Planning-v1-001`

推荐理由：

- Crossing Decision 已 closure，当前主线已系统性禁止过街许可输出
- Controlled Frame Input 已完成 planning + dry-run + review + closure
- Safety Constitution 与 Map/Location readonly 已建立
- 现在可以推进 sample manifest / source policy / privacy precheck / file boundary，但仍不读取真实图像
- Gate Taxonomy 记录为后续项目优化，不打断当前主线

## Deferred Registers

### Gate Taxonomy / Gate Requirement Framework

- `gate_taxonomy_deferred=true`
- `current_status=project_optimization_deferred`
- `implementation_allowed_now=false`
- `recommended_priority=P1`

### Resilience / Offline Distributed MidPlatform

- `midplatform_resilience_deferred=true`
- `offline_distributed_midplatform_deferred=true`
- `current_status=future_architecture_candidate`

### WorldModel / Memory / Exploration / Emotion

全部继续 deferred（P2）。

## Boundary Freeze

本阶段继续冻结：

- `no-runtime`
- `no-write`
- `no-action`
- `no-speech`
- `no-fact`
- `no-live-camera`
- `no-image-read`
- `no-visual-model`
- `no-map-api`
- `no-OCR-provider`
- `no-tracking-runtime`
- `no-worldmodel-write`
- `no-memory-write`
- `no-library-write`
- `no-entity-resolution`
- `no-fact-admission`
- `no-emotion-engine`
- `no-crossing-runtime`
- `no-safe-to-cross-claim`

## Final Verdict

当 runner / verifier 全部通过时，本阶段正式结论为：

- `final_decision=POST_CROSSING_DECISION_ROADMAP_DECISION_READY_FOR_CONTROLLED_FRAME_SAMPLE_PLANNING`
- `phase verdict=GO`
- `recommended_next_phase=Phase-Controlled-Frame-Sample-Planning-v1-001`

## 实施状态（后续落地）

`Phase-Controlled-Frame-Sample-Planning-v1-001` 已以 **planning-only / manifest-only** 形式落地并通过 smoke verifier（不读取真实图像内容、不打开文件、不解码视频、不抽帧、不调用视觉模型）。

`Phase-Controlled-Frame-Sample-DryRun-v1-001` 已以 **manifest-metadata-only** 形式落地并通过 smoke verifier（只构造/读取样例 manifest metadata stub，不打开图片/视频文件，不解码，不抽帧，不调用视觉模型/OCR provider/map/tracking runtime，不写入）。

`Phase-Controlled-Frame-Sample-Post-DryRun-Review-v1-001` 已以 **review-only** 形式落地并通过 smoke verifier（只审查 planning+dryrun 稳定性与边界成立，判定 `ready_for_closure=true`；不读内容、不打开文件、不进入 runtime）。

`Phase-Controlled-Frame-Sample-Closure-v1-001` 已以 **closure-only** 形式落地并通过 smoke verifier（关账 planning+dryrun+post-review，冻结 boundary/non-claims/deferred pool；明确不等于真实图像读取、不等于视觉 runtime、不等于 production readiness）。

