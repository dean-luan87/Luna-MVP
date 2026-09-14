# LUNA MidPlatform Model Switching GO/NO-GO Pack v0

## Phase

- Phase-MidPlatform-ModelSwitch-001：Unified Model Invocation Switching Policy v0

## Decision

- **GO**

## Outputs（this phase）

- `docs/architecture/LUNA_MIDPLATFORM_MODEL_INVOCATION_SWITCHING_POLICY_V0.md`
- `docs/architecture/LUNA_MIDPLATFORM_MODEL_LATENCY_BUDGET_PROFILE_V0.md`
- `docs/architecture/LUNA_MIDPLATFORM_MODEL_FALLBACK_AND_CIRCUIT_BREAKER_POLICY_V0.md`
- `docs/architecture/LUNA_MIDPLATFORM_MODEL_PROVIDER_HEALTH_SCHEMA_V0.md`
- `docs/architecture/LUNA_MIDPLATFORM_MODEL_SWITCHING_APPLICABILITY_MATRIX_V0.md`
- `docs/architecture/LUNA_MIDPLATFORM_MODEL_SWITCHING_GO_NO_GO_PACK_V0.md`

## Acceptance

- 统一策略定义清楚（selection/latency/fallback/circuit/observability 五层）
- latency profiles 清楚且覆盖 realtime/offline/batch
- fallback/circuit breaker 通用规则清楚
- provider health + invocation result schema 清楚
- 适用模块矩阵清楚（TTS/ASR/OCR/Vision/Semantic/Decision）
- 本阶段不改任何 runtime 主链实现

## Hard blockers

- 无

## Soft follow-ups（next phases）

- ModelSwitch-002：实现通用 switching core（不绑定具体能力）
- ModelSwitch-003：以 TTS 为首个实例接入 switching core，替换分散策略实现

