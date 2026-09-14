# LUNA TTS Latency & Circuit Breaker Policy v0

## Phase

- Phase-VoiceTTS-Policy-002

## Latency buckets（total latency）

- **0–800ms**：normal（继续使用 Qwen）
- **800–1200ms**：soft_latency_warning（继续使用，但记录告警）
- **1200–2000ms**：high_latency_risk（可准备 fallback；仍可继续等待）
- **>2000ms**：hard_timeout_exceeded（必须 fallback）

说明：

- 若 Qwen 不支持 streaming/首包事件：本阶段以 total latency 为主；首包指标记为 unsupported。

## Circuit breaker（Qwen）

- **failure_count_threshold=3**
- **open_duration_ms=300000（5min）**
- open 期间：直接跳过 Qwen → Piper
- 5min 后进入 half-open：允许 1 次 probe
  - probe 成功：closed
  - probe 失败：回到 open

## Failure types included

- missing_api_key
- network_unavailable / network_error
- provider_exception
- hard_timeout
- invalid_audio_result
- schema_invalid
- high_latency_fallback（作为失败计入熔断窗口）

