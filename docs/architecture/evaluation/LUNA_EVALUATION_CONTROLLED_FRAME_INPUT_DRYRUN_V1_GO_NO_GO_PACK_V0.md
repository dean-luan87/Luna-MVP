# Luna Evaluation — Controlled Frame Input DryRun v1 GO / NO-GO Pack

对应 phase：`Phase-Controlled-Frame-Input-DryRun-v1-001`

## GO Conditions

- required roots 全部成功加载
- `ControlledFrameInputDryRunCase` schema 已定义
- `SimulatedFrameMetadata` schema 已定义
- `FrameIntakeDecisionCandidate` schema 已定义
- `FrameQualityDecisionCandidate` schema 已定义
- `FramePrivacyDecisionCandidate` schema 已定义
- `FrameFreshnessDecisionCandidate` schema 已定义
- `FrameDownstreamHandoffCandidate` schema 已定义
- `ControlledFrameInputDryRunResult` schema 已定义
- `DualDevicePlaceholderDryRunReview` 已生成
- scenario matrix 已生成且 `scenario_count>=14`
- `accepted_candidate_count>=3`
- `rejected_candidate_count>=5`
- `restricted_candidate_count>=1`
- `stale_archive_only_candidate_count>=1`
- `frame_to_ocr_requires_visual_focus=true`
- `frame_to_tracking_requires_visual_focus=true`
- `frame_to_world_observation_requires_policy=true`
- `live_camera / device_camera / external_stream` 当前全部禁止
- `dual_device / dual_model / failover / multi_input_fusion` 当前全部 runtime 禁止
- 不存在 runtime / write / action / speech 越权
- 最终推荐阶段固定为 `Phase-Controlled-Frame-Input-Post-DryRun-Review-v1-001`

## NO_GO Conditions

- 任一 required root 缺失
- 任一 required schema / result 产物缺失
- `scenario_count<14`
- 缺少指定 14 个 dry-run 场景中的任意一个
- `accepted_candidate_count<3`
- `rejected_candidate_count<5`
- `restricted_candidate_count<1`
- `stale_archive_only_candidate_count<1`
- 允许 `live camera`
- 允许 `device camera`
- 允许 `external stream`
- 允许 `dual device runtime`
- 允许 `dual model runtime`
- 允许 `failover runtime`
- 允许 `multi-input fusion runtime`
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

- Luna 已验证 `Controlled Frame Input` metadata 能穿过 intake / quality / privacy / freshness / downstream handoff 形成候选链
- Luna 已验证 stale/privacy/runtime-blocked 情况会被保守处理
- Luna 已确认 dual-device placeholder 仍然只是 placeholder review，不进入硬件阶段
- 下一阶段可以进入 `Controlled Frame Input Post-DryRun Review`

本阶段 `GO` 不表示：

- 真实图像内容已读取
- `live camera` 已开放
- `device camera` 已开放
- `external stream` 已开放
- 视觉模型已调用
- OCR provider 已调用
- tracking runtime 已调用
- dual-device runtime 已开放
- dual-model runtime 已开放
- failover 已实现
- multi-input fusion 已实现
- `WorldModel / Memory / Fact / Library` 已开放写入

## Next Phase

本阶段通过后，只允许推荐：

- `Phase-Controlled-Frame-Input-Post-DryRun-Review-v1-001`

下一步 review 也必须继续保持：

- no real image content read
- no live camera
- no device camera
- no external stream
- no model runtime
- no dual-device runtime
- no failover
- no write
