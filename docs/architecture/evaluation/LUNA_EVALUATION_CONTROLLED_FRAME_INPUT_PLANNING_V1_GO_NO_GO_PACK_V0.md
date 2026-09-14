# Luna Evaluation — Controlled Frame Input Planning v1 GO / NO-GO Pack

对应 phase：`Phase-Controlled-Frame-Input-Planning-v1-001`

## GO Conditions

- required roots 全部成功加载
- `ControlledFrameInputPlanningPolicy` 已定义
- `FrameSourceCandidate` schema 已定义
- `ControlledFrameInputCandidate` schema 已定义
- `FrameIntakeGatePolicy` 已定义
- `FrameQualityGatePolicy` 已定义
- `FramePrivacyTaggingPolicy` 已定义
- `FrameSTCFreshnessPolicy` 已定义
- `FrameDownstreamHandoffPolicy` 已定义
- `Dual-Device / Dual-Lane Redundant Perception Placeholder` 已定义
- `ControlledFrameInputReadinessGate` 已生成
- scenario matrix 已生成且 `scenario_count>=10`
- `static_test_image / pre_recorded_video_frame / simulation_frame` 允许作为未来受控 dry-run 输入候选
- `live_camera / device_camera / external_stream` 当前全部禁止
- `dual_device / dual_model / failover` 当前全部 runtime 禁止
- `frame_to_ocr_requires_visual_focus=true`
- `frame_to_tracking_requires_visual_focus=true`
- `frame_to_world_observation_requires_policy=true`
- 不存在 runtime / write / action / speech 越权
- 最终推荐阶段固定为 `Phase-Controlled-Frame-Input-DryRun-v1-001`

## NO_GO Conditions

- 任一 required root 缺失
- 任一 required policy / schema 产物缺失
- `scenario_count<10`
- 缺少指定 10 个场景中的任意一个
- 允许 `live camera`
- 允许 `device camera`
- 允许 `external stream`
- 允许 `dual device runtime`
- 允许 `dual model runtime`
- 允许 `failover runtime`
- 允许自动硬件切换
- 缺少 `source_chain`
- 缺少 `timestamp`
- privacy tags 对 downstream 不是必需
- frame 可直接进入 OCR provider
- frame 可直接进入 tracking runtime
- frame 可直接进入 NavigationAction
- frame 可直接进入 SpeechOutput
- frame 可写 `WorldModel / Memory / Fact`
- 发生真实 camera / video capture / model runtime 调用
- next phase 不明确

## GO Meaning

本阶段 `GO` 的语义仅表示：

- Luna 已具备“如何安全接入受控帧输入”的规则
- Luna 也已为未来硬件阶段预留双设备 / 双模型 / 双通道冗余感知 placeholder
- 下一阶段可以进入 `Controlled Frame Input DryRun`
- dry-run 只允许使用 `static test image / pre-recorded frame / simulation frame`

本阶段 `GO` 不表示：

- `live camera` 已开放
- dual-device runtime 已开放
- dual-model runtime 已开放
- failover 已实现
- 摄像头已打开
- 真实设备流已读取
- 视觉模型已调用
- OCR provider 已调用
- tracking runtime 已调用
- `WorldModel / Memory / Fact / Library` 已开放写入

## Next Phase

本阶段通过后，只允许推荐：

- `Phase-Controlled-Frame-Input-DryRun-v1-001`

下一步如果进入 dry-run，也必须继续保持：

- no live camera
- no device camera
- no external stream
- no model runtime
- no write
