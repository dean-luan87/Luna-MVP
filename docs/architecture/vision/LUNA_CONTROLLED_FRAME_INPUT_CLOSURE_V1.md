# Luna — Controlled Frame Input Closure v1

**Phase**：`Phase-Controlled-Frame-Input-Closure-v1-001`  
**性质**：closure / status freeze / boundary freeze only  
**边界**：不实现 runtime，不读取真实图像内容，不打开摄像头，不读取真实设备流，不调用视觉模型，不调用 `OCR provider`，不提交 `OCRRequest`，不调用地图 API / 高德 API，不调用 GPS runtime，不调用 tracking runtime，不调用 optical flow runtime，不导入或调用 `Supervision / ByteTrack / OC-SORT`，不写 `Memory` / `WorldModel` / `Fact` / `Library`，不做 `entity resolution`，不做 `fact admission`，不做 `memory consolidation`，不做 `library experience commit`，不生成 `Scene Delta`，不提交 `Task State`，不触发 `Navigation Action`，不调用 `Speech Gate / VOP / TTS`，不输出真实用户可听语音，不执行 `dual-device runtime / dual-model runtime / failover runtime / multi-input fusion runtime`

## 目标

本阶段正式对 `Controlled Frame Input` 做阶段性收口。

它只回答：

1. `Planning / DryRun / Post-DryRun Review` 是否已经完整闭合  
2. 哪些 frame source 已被允许为 future controlled dry-run candidate  
3. 哪些 frame source 已被明确拒绝  
4. intake / quality / privacy / STC freshness / downstream handoff 边界是否冻结  
5. dual-device / dual-lane redundant perception 是否仍只是 placeholder  
6. 哪些 runtime 能力仍未启用  
7. 哪些能力进入 deferred capability pool  
8. 下一阶段是否应先进入 `Post-Controlled-Frame-Input-Roadmap-Decision`

## Core Closure Objects

### ControlledFrameInputClosureSummary

用于表达本次 closure 的总收口结果，必须带：

- `closure_id`
- `closure_scope`
- `source_phase_chain`
- `completed_phase_count`
- `completed_phase_matrix_ref`
- `validated_capability_summary_ref`
- `disabled_runtime_summary_ref`
- `closure_boundary_freeze_ref`
- `non_claims_register_ref`
- `deferred_capability_pool_ref`
- `governance_debt_carryover_ref`
- `next_phase_recommendation`
- `final_decision`
- `source_chain`

### CompletedPhaseMatrix

本阶段只收口以下三层：

1. `Controlled Frame Input Planning v1`
2. `Controlled Frame Input DryRun v1`
3. `Controlled Frame Input Post-DryRun Review v1`

每项都必须保持：

- `status=GO`
- `runtime_enabled=false`
- `write_enabled=false`

### ValidatedCapabilitySummary

本阶段确认以下能力已经完成到 `planning / metadata dry-run / review` 层：

- controlled frame source candidate policy
- frame intake gate
- frame quality gate
- frame privacy tagging policy
- frame STC / freshness reuse
- frame downstream handoff policy
- controlled frame dry-run metadata simulation
- allowed / rejected / restricted / stale frame scenario coverage
- dual-device redundant perception placeholder
- post-dryrun review

必须明确：

- 这些不是 live camera runtime
- 这些不等于真实 frame runtime
- 这些不等于真实视觉能力

### DisabledRuntimeSummary

本阶段继续明确以下能力未启用：

- live camera runtime
- device camera runtime
- external stream runtime
- actual image loading
- visual model runtime
- OCR provider runtime
- OCRRequest submission
- map API / 高德 API
- GPS runtime
- tracking runtime
- optical flow runtime
- `Supervision / ByteTrack / OC-SORT`
- dual-device runtime
- dual-model runtime
- failover runtime
- multi-input fusion runtime
- `Speech Gate / VOP / TTS`
- `NavigationAction`
- `WorldModel / Memory / Library / Fact` write

### ClosureBoundaryFreeze

本阶段正式冻结：

- `no-runtime`
- `no-write`
- `no-action`
- `no-speech`
- `no-fact`
- `no-live-camera`
- `no-device-camera`
- `no-external-stream`
- `no-actual-image-read`
- `no-visual-model`
- `no-OCR-provider`
- `no-tracking-runtime`
- `no-map-api`
- `no-dual-device-runtime`
- `no-failover-runtime`
- `no-multi-input-fusion`
- `frame_to_ocr_requires_visual_focus=true`
- `frame_to_tracking_requires_visual_focus=true`
- `frame_to_world_observation_requires_policy=true`
- `frame_to_navigation_action_allowed=false`
- `frame_to_speech_output_allowed=false`
- `frame_to_worldmodel_write_allowed=false`
- `frame_to_memory_write_allowed=false`
- `frame_to_fact_write_allowed=false`

### ControlledFrameInputNonClaimsRegister

本阶段明确以下 non-claims：

- closure 不等于 live camera 可用
- closure 不等于真实视觉 runtime
- closure 不等于可以读取真实图像
- metadata dry-run 不等于图像推理
- `static_test_image` candidate 不等于真实图像已读取
- `pre_recorded_video_frame` candidate 不等于真实视频已处理
- `simulation_frame` candidate 不等于真实世界 observation
- `controlled_uploaded_frame` candidate 不等于用户文件处理 runtime
- dual-device placeholder 不等于硬件阶段
- failover placeholder 不等于可自动故障切换
- multi-input consistency placeholder 不等于多输入融合
- frame candidate 不等于事实
- downstream handoff candidate 不等于下游 runtime

### DeferredCapabilityPool

本阶段把以下能力保留到未来：

- `Controlled Frame Sample Planning`
- controlled real file/static image sample trial
- live camera guarded trial
- device camera capability registry
- visual model adapter
- OCR provider re-enable through VisualFocus
- tracking adapter experiment branch
- dual-device hardware planning
- device health registry
- failover policy runtime
- multi-input fusion governance
- `WorldModel Candidate Layer`
- `Memory Governance`
- `Library Governance`
- `MidPlatform Function Governance / Consolidation`
- `MidPlatform Resilience / Robustness`
- `Offline Distributed MidPlatform Architecture Preplan`

### GovernanceDebtCarryover

本阶段继续带出以下 debt：

- frame source policy complexity
- privacy tagging complexity
- frame quality gate complexity
- STC/freshness integration complexity
- downstream handoff complexity
- dual-device placeholder future complexity
- hardware-stage deferred debt
- controlled sample planning deferred
- `future_midplatform_function_governance_required=true`
- `future_midplatform_resilience_governance_required=true`
- `no_duplicate_governance_module_allowed=true`

## Closure Meaning

本阶段 `GO` 的语义仅表示：

- `Controlled Frame Input` 的 `planning + dry-run + review` 已正式收口
- 受控帧输入边界已经冻结
- 当前不应直接进入 controlled sample planning
- 下一阶段应先进入 `Post-Controlled-Frame-Input-Roadmap-Decision`

本阶段 `GO` 不表示：

- live camera 已开放
- 真实视觉 runtime 已开放
- 真实图像已读取
- production readiness 已成立
- dual-device / failover / multi-input fusion runtime 已开放

## Final Verdict

当 runner / verifier 全部通过时，本阶段正式结论为：

- `final_decision=CONTROLLED_FRAME_INPUT_CLOSED_FOR_CURRENT_MAINLINE`
- `phase verdict=GO`
- `recommended_next_phase=Phase-Post-Controlled-Frame-Input-Roadmap-Decision-v1-001`

这表示：

- `Controlled Frame Input` 已对当前主线阶段性收口
- 当前仍然不进入 controlled sample planning
- 当前仍然不读取真实图像内容
- 当前仍然不打开摄像头
- 当前仍然不进入 live camera / hardware / dual-device runtime

当前状态更新：

- `Phase-Post-Controlled-Frame-Input-Roadmap-Decision-v1-001 = GO`
- `final_decision=POST_CONTROLLED_FRAME_INPUT_ROADMAP_DECISION_READY_FOR_CROSSING_DECISION_SAFETY_GOVERNANCE_POLICY`
- 当前推荐下一阶段：`Phase-Crossing-Decision-Safety-Governance-Policy-v1-001`
