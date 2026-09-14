# LUNA MidPlatform Model Provider Health Schema v0

## Phase

- Phase-MidPlatform-ModelSwitch-001

## ProviderHealthState（schema v0）

```json
{
  "provider_id": "string",
  "capability_type": "tts | asr | ocr | vision | semantic | decision",
  "provider_kind": "online | local | hybrid | rule | fallback",
  "enabled": true,
  "requires_network": false,
  "requires_api_key": false,
  "latency_profile": "realtime_critical | realtime_normal | interactive_quality | offline_batch",
  "recent_success_count": 0,
  "recent_failure_count": 0,
  "last_latency_ms": null,
  "last_success_at": null,
  "last_failure_at": null,
  "last_failure_reason": null,
  "circuit_state": "closed | open | half_open",
  "fallback_available": true
}
```

## ModelInvocationResult（schema v0）

```json
{
  "request_id": "string",
  "capability_type": "tts | asr | ocr | vision | semantic | decision",
  "invocation_mode": "realtime_critical | realtime_normal | interactive_quality | offline_evaluation | batch_analysis | experimental_online",
  "policy_id": "midplatform_model_invocation_switching_policy_v0",
  "provider_attempt_order": [],
  "provider_attempted": [],
  "provider_selected": "string",
  "provider_success": true,
  "provider_latency_ms": 0,
  "soft_latency_warning": false,
  "high_latency_risk": false,
  "hard_timeout_triggered": false,
  "fallback_used": false,
  "fallback_provider": null,
  "fallback_reason": null,
  "circuit_state": "closed | open | half_open",
  "circuit_reason": null,
  "result_schema_valid": true,
  "forbidden_output_detected": false,
  "output_contract_valid": true,
  "allows_execute_now": false,
  "side_effects_allowed": false,
  "real_runtime_allowed": false,
  "audit_trace_ref": "string",
  "hard_blockers": [],
  "soft_followups": []
}
```

## Notes

- 本 schema 只描述“切换治理层”的统一字段；各 capability 可扩展私有字段，但不得破坏上述最低审计字段。

