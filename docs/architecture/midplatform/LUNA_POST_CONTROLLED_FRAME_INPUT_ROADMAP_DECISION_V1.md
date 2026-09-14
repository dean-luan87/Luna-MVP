# Luna — Post Controlled Frame Input Roadmap Decision v1

**Phase**：`Phase-Post-Controlled-Frame-Input-Roadmap-Decision-v1-001`  
**性质**：roadmap decision / prioritization / boundary freeze only  
**边界**：不实现 runtime，不读取真实图像内容，不打开摄像头，不读取真实设备流，不调用视觉模型，不调用 `OCR provider`，不提交 `OCRRequest`，不调用地图 API / 高德 API，不调用 GPS runtime，不调用 tracking runtime，不调用 optical flow runtime，不导入或调用 `Supervision / ByteTrack / OC-SORT`，不写 `Memory` / `WorldModel` / `Fact` / `Library`，不做 `entity resolution`，不做 `fact admission`，不做 `memory consolidation`，不做 `library experience commit`，不生成 `Scene Delta`，不提交 `Task State`，不触发 `Navigation Action`，不调用 `Speech Gate / VOP / TTS`，不输出真实用户可听语音，不执行 `dual-device runtime / dual-model runtime / failover runtime / multi-input fusion runtime`

## 目标

本阶段只回答：

1. `Controlled Frame Input Closure` 后当前主线状态是什么  
2. 是否应该立刻进入 controlled sample planning  
3. controlled real file / static image sample 是否已具备前置条件  
4. `Crossing Decision Safety Governance` 是否应优先  
5. `MidPlatform Function Governance` 是现在做还是继续后置  
6. `MidPlatform Resilience / Robustness` 是否应单独纳入 `P1`  
7. `Offline Distributed MidPlatform` 是否继续作为 future architecture candidate  
8. `Exploration Drive` 是否继续 deferred  
9. `WorldModel / Memory / Library / Emotion Engine` 是否继续 deferred  
10. 最终 `recommended_next_phase` 是什么

## Current Status

当前主线状态总结：

- `controlled_frame_input_planning_closed=true`
- `controlled_frame_input_dryrun_closed=true`
- `controlled_frame_input_post_review_closed=true`
- `controlled_frame_input_closed=true`
- `controlled_sample_planning_started=false`
- `live_camera_claimed=false`
- `visual_runtime_claimed=false`
- `image_read_claimed=false`
- `production_readiness_claimed=false`
- `runtime_enablement_claimed=false`

这表示：

- `Controlled Frame Input` 已完成 `planning + dry-run + review + closure`
- 当前仍然不是 controlled sample planning
- 当前仍然不是 image read / camera / runtime 阶段

## Route Option Matrix

本阶段正式评估以下 9 条路线：

### P0

1. `Controlled Frame Sample Planning`
2. `Crossing Decision Safety Governance Policy`
3. `MidPlatform Function Governance / Consolidation`

### P1

4. `MidPlatform Resilience / Robustness Preplan`
5. `Offline Distributed MidPlatform Architecture Preplan`
6. `Minimal Controlled Visual Runtime Planning`

### P2

7. `Exploration Drive Policy`
8. `WorldModel Candidate Layer / Memory / Library Governance`
9. `Emotion Map / Affective Engine`

## Why Crossing First

本阶段最终选择：

- `selected_next_phase=Phase-Crossing-Decision-Safety-Governance-Policy-v1-001`

推荐理由：

- 视觉增强导航闭环已经收口
- `Map / Location Read-Only Context` 已定义为 readonly hint
- `Controlled Frame Input` 已 closure，但这不等于现在就该进入 controlled sample planning
- 过街 / 红绿灯 / 车流 / 人流 / 路口判断是当前最高风险缺口
- crossing 不能混入普通导航链
- 必须先建立 crossing safety governance，后续才能更安全地进入 controlled sample planning 或任何受控视觉 runtime planning
- 当前推荐仍是 policy-only，不接 camera，不接 map API，不做真实过街判断

## Deferred Registers

### MidPlatform Resilience / Offline Distributed MidPlatform

两条路线当前都保留为 `future architecture candidate`：

- `midplatform_resilience_deferred=true`
- `offline_distributed_midplatform_deferred=true`
- `runtime_allowed_now=false`
- `direct_action_allowed=false`

后续话题只登记，不实现：

- `midplatform_single_point_failure`
- `local_minimum_safety_path`
- `module_autonomy`
- `degraded_operation`
- `failover_arbitration`
- `pressure_test`
- `resource_congestion_control`
- `local_first_midplatform`
- `cloud_enhanced_midplatform`
- `distributed_candidate_sync`
- `conflict_merge_rollback`
- `privacy_preserving_sync`
- `offline_weak_network_mode`
- `multi_device_coordination`

### Exploration Drive

`Exploration Drive` 继续保留为 `deferred_future_candidate`：

- `exploration_drive_deferred=true`
- `priority=P2`
- `runtime_allowed_now=false`
- `direct_action_allowed=false`
- `worldmodel_write_allowed=false`
- `memory_write_allowed=false`
- `fact_write_allowed=false`

探索方向只登记：

- `safety_exploration`
- `task_exploration`
- `worldmodel_gap_exploration`
- `conflict_validation_exploration`
- `resource_environment_adaptation_exploration`
- `emotion_map_precursor_exploration`

### WorldModel / Memory / Library / Emotion

以下全部继续 deferred：

- `WorldModel Candidate Layer`
- `Memory / Library Governance`
- `Emotion Map / Affective Engine`

原因：

- crossing safety governance 还未正式定义
- controlled visual sample stage 尚未启动
- `WorldModel / Memory / Library` 继续保持 no-write 边界
- `Emotion Engine` 必须等待真实世界信息、事件链、关系与记忆治理更成熟后再做

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
- `no-dual-device-runtime`
- `no-failover-runtime`

## Non-Claims

必须明确：

- roadmap decision 不等于 runtime enablement
- roadmap decision 不等于 controlled sample planning 已开始
- roadmap decision 不等于真实图像读取
- roadmap decision 不等于 live camera 接入
- roadmap decision 不等于 map API 接入
- roadmap decision 不等于 OCR provider 接入
- roadmap decision 不等于 tracking runtime 接入
- selected next phase 不等于允许过马路动作
- `Crossing Decision Safety Governance` 不等于真实过街判断 runtime
- `Controlled Frame Sample Planning` 不等于读取真实样例内容
- `WorldModel Candidate Layer / Memory / Library Governance` 当前不进入写路径
- `Emotion Map / Affective Engine` 当前不进入实现

## Final Verdict

当 runner / verifier 全部通过时，本阶段正式结论为：

- `final_decision=POST_CONTROLLED_FRAME_INPUT_ROADMAP_DECISION_READY_FOR_CROSSING_DECISION_SAFETY_GOVERNANCE_POLICY`
- `phase verdict=GO`
- `recommended_next_phase=Phase-Crossing-Decision-Safety-Governance-Policy-v1-001`

这表示：

- `Controlled Frame Input` 主线已经正式收口并完成后续路线裁决
- 当前不进入 controlled sample planning
- 当前不读取真实图像
- 当前不打开摄像头
- 当前不接 map API
- 当前下一阶段应优先进入 `Crossing Decision Safety Governance Policy`

当前状态更新：

- `Phase-Luna-Safety-Constitution-Policy-v1-001 = GO`
- `final_decision=LUNA_SAFETY_CONSTITUTION_POLICY_READY_FOR_CROSSING_DECISION_SAFETY_GOVERNANCE`
- `Phase-Crossing-Decision-Safety-Governance-Policy-v1-001 = GO`
- `final_decision=CROSSING_DECISION_SAFETY_GOVERNANCE_POLICY_READY_FOR_CROSSING_DECISION_DRYRUN`
- 当前推荐下一阶段：`Phase-Crossing-Decision-DryRun-v1-001`
