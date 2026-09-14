# LUNA — OCR Provider Health State Schema v0

## Phase

- **Phase-ModelOCR-Governance-001**

## OCRProviderHealthState

```json
{
  "provider_id": "...",
  "model_config_id": "...",
  "provider_kind": "local_onnx | local_paddle | system_provider | vl_model | service",
  "enabled": true,
  "dependency_ready": true,
  "model_assets_ready": true,
  "runtime_ready": true,
  "avg_latency_ms_per_frame": 0,
  "p95_latency_ms_per_frame": 0,
  "recent_success_count": 0,
  "recent_failure_count": 0,
  "fallback_available": true,
  "circuit_state": "closed | open | half_open",
  "last_failure_reason": null,
  "capability_boundary": {
    "raw_text_only": true,
    "semantic_interpretation_enabled": false,
    "orientation_support": false,
    "layout_support": false
  }
}
```

## OCR invocation result schema（核心字段）

- `provider_id`
- `model_config_id`
- `provider_latency_ms`
- `provider_success`
- `raw_text_candidates`
- `raw_text_joined`
- `fallback_used`
- `fallback_reason`
- `not_available_reason`
- `trace_ref`
- `replay_ref`
- `whitebox_ref`

## Circuit breaker semantics

- `closed`: 正常服务
- `open`: 连续失败，禁止继续调用，直接 fallback
- `half_open`: 少量探测请求恢复评估

## Boundary invariants

- `raw_text_only=true`
- `semantic_interpretation_enabled=false`
- `allows_execute_now=false`
- `real_tts_invoked=false`
