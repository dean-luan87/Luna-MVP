# LUNA Qwen Online-First With Local Realtime Fallback Policy v0

## Phase

- Phase-VoiceTTS-Policy-002：Qwen Online First With Local Realtime Fallback Policy v0

## Purpose

定义并实现一个**受控**的在线优先 TTS 策略，在在线条件稳定时优先使用 Qwen/Qianwen；当在线不可用或延迟过高时快速降级到本地 TTS，保证实时性。

## Hard boundaries

- 不污染 offline-only baseline（默认策略仍可保持离线）
- 不删除 Piper
- 不删除 macOS say legacy fallback
- 不绕过 unified TTS entry
- 不绕过 Speech Gate
- Qwen 只做 text→audio，不生成/改写播报文本
- 不改导航语义链，不执行导航动作

## Policy ID

- `policy_id = qwen_online_first_local_realtime_fallback_v0`

## Fallback order

1. Qwen online provider
2. Piper local provider
3. macOS say legacy fallback

## Latency thresholds

- `soft_latency_warning_ms = 800`
- `first_response_budget_ms = 1200`（若无首包指标：记录 unsupported_first_response_metric）
- `hard_timeout_ms = 2000`（超过必须 fallback）

## Circuit breaker

- 连续失败阈值：3
- open 持续：5 分钟（直接走 Piper）
- half-open：允许 1 次 probe；成功则关闭熔断，失败继续 open

## Config & enablement

- 默认：`online_runtime.enabled=false`（不污染 offline-only baseline）
- 可通过环境变量临时启用（不写回配置）：
  - `LUNA_TTS_ONLINE_RUNTIME_ENABLED=true`

