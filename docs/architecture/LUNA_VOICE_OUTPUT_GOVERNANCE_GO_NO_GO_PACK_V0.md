# LUNA — Voice Output Governance Go/No-Go Pack v0

## Phase

- **Phase-Voice-OutputGovernance-001**

## GO conditions（必须）

- voice output governance definition 完整（定位+边界+复用口径）
- voice output state machine + interruption/cancel/expiry 规则完整
- priority/expiry/suppression 规则完整（过期不播报、重复限频、低置信降级、静默合法）
- TTS provider health / latency / circuit breaker / fallback 治理要求完整
- trace/replay/whitebox 可观测性要求完整
- 明确本阶段不实现 runtime、不真实播报、不导航、不推荐、不写世界模型、不下游执行

## NO_GO（任意一条）

- 允许过期内容播报
- 允许低置信以确定语气播报
- 输出层出现 execute/override/release 等放权语义
- 允许打断导航/安全/主任务（除非明确 safety-only 例外且有审计）
- 本阶段实现真实 TTS 播放或真实 provider 调用
- 触发导航动作/推荐/写世界模型/蜂巢上传/进入 SceneTask-Fusion-Output

