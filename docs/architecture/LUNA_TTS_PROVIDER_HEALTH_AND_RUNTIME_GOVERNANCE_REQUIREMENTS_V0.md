# LUNA — TTS Provider Health & Runtime Governance Requirements v0

## Phase

- **Phase-Voice-OutputGovernance-001**

## Purpose

定义 TTS runtime health 与 provider 治理要求，使语音输出具备：

- latency budget
- circuit breaker
- fallback order
- failure classification
- auditability

本阶段只定义，不实现真实调用与播报。

## Reuse（既有口径）

- latency & circuit breaker：`docs/architecture/LUNA_TTS_LATENCY_AND_CIRCUIT_BREAKER_POLICY_V0.md`
- online-first fallback：`docs/architecture/LUNA_QWEN_ONLINE_FIRST_LOCAL_FALLBACK_POLICY_V0.md`

## Health signals（v0）

- `provider_id`
- `provider_mode`（offline/online）
- `latency_ms_total`
- `timeout_bucket`（normal/soft_warning/high_risk/hard_timeout_exceeded）
- `failure_type`（network_error/hard_timeout/invalid_audio/...）
- `circuit_breaker_state`（closed/open/half_open）
- `fallback_used`（true/false + fallback_provider_id）

## Hard rules

- 超过硬超时必须 fallback（只定义行为）
- 熔断 open 期间不得继续调用故障 provider
- provider 只能做 text→audio，不得改写播报文本
- 所有失败/降级必须进入 trace/whitebox

