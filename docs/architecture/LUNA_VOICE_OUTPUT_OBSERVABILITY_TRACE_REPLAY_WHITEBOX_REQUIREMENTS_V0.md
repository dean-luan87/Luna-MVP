# LUNA — Voice Output Observability (Trace/Replay/Whitebox) Requirements v0

## Phase

- **Phase-Voice-OutputGovernance-001**

## Purpose

定义语音输出链路的可观测性要求，保证：

- 能解释“为什么播报/为什么不播报”
- 能回放（replay）输出决策
- 能定位 provider health / fallback / circuit breaker 导致的变化

本阶段只定义，不实现 runtime。

## Trace（must include）

- output_candidate_id / message_template_id（或等价）
- priority / output_type
- generated_at / expires_at / suppression_reason
- interruption_allowed / cancelled_by
- selected_provider_id / provider_mode
- latency bucket / circuit breaker state / fallback_used
- governance flags（navigation_action=null 等）

## Replay（must include）

- provider selection input refs（不含隐私原文时可用 hash/ref）
- policy version refs（priority/suppression/latency/cb）
- decision chain refs（why_selected/why_suppressed/why_fallback）

## Whitebox（must include）

- why_spoken / why_suppressed / why_expired / why_cancelled
- why_low_confidence_degraded
- why_safety_suppressed_normal
- why_provider_fallback

