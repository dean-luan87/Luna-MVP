# Luna — Post Vision Strengthening Roadmap Decision v1

**Phase**：`Phase-Post-Vision-Strengthening-Roadmap-Decision-v1-001`  
**性质**：roadmap decision / prioritization / boundary freeze only  
**边界**：不实现 runtime，不调用 `camera`，不调用视觉模型，不调用 `OCR provider`，不提交 `OCRRequest`，不调用地图 API / 高德 API，不调用 tracking runtime，不调用 optical flow runtime，不导入或调用 `Supervision / ByteTrack / OC-SORT`，不写 `Memory` / `WorldModel` / `Fact` / `Library`，不做 `entity resolution`，不做 `fact admission`，不做 `memory consolidation`，不做 `library experience commit`，不生成 `Scene Delta`，不提交 `Task State`，不触发 `Navigation Action`，不调用 `Speech Gate / VOP / TTS`，不输出真实用户可听语音

## 目标

本阶段用于回答：

1. 当前“视觉增强导航闭环”在 closure 后的主线状态是什么；
2. 哪些能力已经完成到 `policy / dry-run / closure` 层；
3. 哪些能力仍然只是 `future roadmap candidate`；
4. 下一阶段是否应该进入 runtime；
5. 如果不进入 runtime，应该优先推进哪条主线；
6. `Map / Location Read-Only Context` 是否应成为下一主线；
7. `Controlled Frame Input` 是否应成为下一主线；
8. `Crossing Decision Safety Governance` 是否应单独提前；
9. `MidPlatform Function Governance / Consolidation` 是现在做还是后置；
10. `Exploration Drive` 是现在做还是作为 future roadmap candidate；
11. `WorldModel / Memory / Library / Emotion Map` 是否继续 deferred；
12. 最终 `recommended_next_phase` 是什么。

## Current Mainline Status

当前主线状态总结：

- `Basic Navigation Loop Vision Strengthening` 已完成 closure
- `policy_chain_closed=true`
- `dryrun_chain_closed=true`
- `feedback_chain_closed=true`
- `navigation_loop_vision_strengthening_closed=true`
- `runtime_enabled=false`
- `live_navigation_claimed=false`
- `production_readiness_claimed=false`

这表示：

- 当前主线已阶段性收口
- 仍然不是 runtime
- 仍然不是 live navigation
- 仍然不是 production readiness

## Completed Capability Summary

已完成到 `policy / dry-run / closure` 层的能力包括：

1. `Return-To-Vision Mainline Planning`
2. `MidPlatform Perception Orchestration Policy`
3. `Task-Aware Visual Focus Policy`
4. `World Observation and Entity Feature Policy`
5. `Selective Tracking Adapter Policy`
6. `Visual-OCR-Map-Task Feedback DryRun`
7. `Basic Navigation Loop Vision Strengthening DryRun`
8. `Post-DryRun Review`
9. `Closure`

必须明确：

- 这些都不是 runtime
- 这些都不是 production-ready
- 这些都不是 live navigation

## Route Option Matrix

本阶段至少评估以下 9 条路线：

### P0

1. `Map / Location Read-Only Context Policy`
   目标：把地图/位置上下文定义为正式只读输入合同，不接真实 API，不触发导航动作。
2. `Controlled Frame Input Planning / Policy`
   目标：规划受控真实帧输入治理，但不立刻接 live camera。
3. `Crossing Decision Safety Governance Policy`
   目标：单独冻结过街、红绿灯、车流、人流、路口判断的安全治理。

### P1

4. `MidPlatform Function Governance / Consolidation`
   目标：收束 governance debt，避免中台能力膨胀和重复模块。
5. `Minimal Controlled Runtime Trial Planning`
   目标：只规划最小受控 runtime，不执行。

### P2

6. `Exploration Drive Policy`
7. `WorldModel Candidate Layer`
8. `Memory / Library Governance`
9. `Emotion Map / Affective Engine`

这些路线都必须继续受以下约束：

- 不得绕过 `MidPlatform`
- 不得绕过 `Safety arbitration`
- 不得提前打穿 `WorldModel / Memory / Library` 写路径

## Why Map / Location First

本阶段最终选择：

- `selected_next_phase=Phase-Map-Location-ReadOnly-Context-Policy-v1-001`

原因：

- 视觉 / OCR / 地图 / 记忆 feedback chain 已经在 dry-run 层串通
- `map/location hint` 是后续任务型视觉驱动的关键 context
- 只读上下文不会打开 action 权限
- 风险低于 `Controlled Frame Input` 或任何 runtime 规划
- 可为导航、目标接近、左右侧判断、路线阶段判断提供必要上下文
- 不写 `WorldModel / Memory / Fact`
- 不接真实高德 API，只先定义 read-only context policy

## Deferred Registers

### Exploration Drive

`Exploration Drive` 当前只保留为 `future roadmap candidate`：

- `current_status=deferred_future_candidate`
- `priority=P2`
- `runtime_allowed_now=false`
- `direct_action_allowed=false`
- `worldmodel_write_allowed=false`
- `memory_write_allowed=false`
- `fact_write_allowed=false`

探索方向只登记，不实现：

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

- `task-driven perception` 仍需继续优先加强
- `map/location context` 还未正式化
- `WorldModel / Memory / Library` 治理尚未成熟
- `Emotion Engine` 必须等待真实世界信息、事件链、人物关系、记忆治理更成熟后再进入

## Boundary Freeze

本阶段继续冻结：

- `no-runtime`
- `no-write`
- `no-action`
- `no-speech`
- `no-fact`
- `no-live-navigation`
- `no-production-readiness`
- `no-camera`
- `no-map-api`
- `no-ocr-provider`
- `no-tracking-runtime`
- `no-worldmodel-write`
- `no-memory-write`
- `no-library-write`
- `no-entity-resolution`
- `no-fact-admission`
- `no-emotion-engine`

## Non-Claims

必须明确：

- roadmap decision 不等于 runtime enablement
- roadmap decision 不等于 live navigation
- roadmap priority 不等于 production readiness
- selected next phase 不等于 `camera` 接入
- selected next phase 不等于 `map API` 接入
- selected next phase 不等于 `OCR provider` 接入
- selected next phase 不等于 `tracking runtime` 接入
- `Map / Location Read-Only Context Policy` 不等于真实地图调用
- `Controlled Frame Input Planning` 不等于 live camera
- `Crossing Decision Safety Governance` 不等于允许过街动作
- `Exploration Drive` 当前不进入 runtime
- `WorldModel Candidate Layer` 当前不进入 fact admission
- `Memory / Library Governance` 当前不进入 write path
- `Emotion Map / Affective Engine` 当前不进入实现

## Final Verdict

当 runner / verifier 全部通过时，本阶段正式结论为：

- `final_decision=POST_VISION_STRENGTHENING_ROADMAP_DECISION_READY_FOR_MAP_LOCATION_READONLY_CONTEXT_POLICY`
- `phase verdict=GO`
- `recommended_next_phase=Phase-Map-Location-ReadOnly-Context-Policy-v1-001`

这表示：

- 当前主线正式从“视觉增强导航闭环收口”切换到“地图/位置只读上下文”
- 下一步继续走 `task-driven perception` 主线
- 不进入 runtime
- 不接真实 map API
- 不接 camera
- 不接 OCR provider
- 不接 tracking
- 不写 `WorldModel / Memory / Fact / Library`

当前状态更新：

- `Phase-Map-Location-ReadOnly-Context-Policy-v1-001 = GO`
- `Phase-Controlled-Frame-Input-Planning-v1-001 = GO`
- 当前推荐下一阶段：`Phase-Controlled-Frame-Input-DryRun-v1-001`
