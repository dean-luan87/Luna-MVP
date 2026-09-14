# LUNA — Voice/TTS Runtime Health & Output Governance Definition v0

## Phase

- **Phase-Voice-OutputGovernance-001**

## Purpose

补齐语音输出链路的治理与观测标准，使其达到与 OCR/YOLO 同等级的可观测、可治理能力。

本阶段只定义：

- 语音输出的优先级、打断、取消、过期、抑制与超时规则
- TTS provider health / latency / circuit breaker 的接入边界
- trace/replay/whitebox 的审计要求

不实现 runtime，不触发真实播报。

## Non-governance boundary（强制）

- 不实现 runtime
- 不触发真实播报（no real TTS）
- 不执行导航动作
- 不进入 SceneTask/Fusion/Output
- 不写世界模型
- 不接推荐系统
- 不上传蜂巢

## Positioning（分层定位）

该阶段属于“核心感知与直接交互链”中的 **输出治理**：

- Collection：Voice（用户输入）/TTS（输出表达）
- Processing：输出候选的优先级/抑制/过期/取消治理

它不产生新事实，不放权执行。

## Relationship with existing policies（复用口径）

- 输出优先级/抑制口径参考：`docs/architecture/LUNA_NAVIGATION_OUTPUT_PRIORITY_AND_SUPPRESSION_POLICY_V0.md`
- TTS latency/circuit breaker 口径参考：`docs/architecture/LUNA_TTS_LATENCY_AND_CIRCUIT_BREAKER_POLICY_V0.md`
- online-first fallback 口径参考：`docs/architecture/LUNA_QWEN_ONLINE_FIRST_LOCAL_FALLBACK_POLICY_V0.md`

