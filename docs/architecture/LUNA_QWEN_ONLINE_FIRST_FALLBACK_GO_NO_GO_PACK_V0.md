# LUNA Qwen Online-First Fallback GO/NO-GO Pack v0

## Phase

- Phase-VoiceTTS-Policy-002：Qwen Online First With Local Realtime Fallback Policy v0

## Decision

- **GO**

## Evidence

- `logs/verify_qwen_online_first_fallback_policy_v0.json`（`all_pass=true`）

## Default safety

- offline-only baseline 保留
- `online_runtime.enabled` 默认 **false**
- 可用环境变量临时启用：`LUNA_TTS_ONLINE_RUNTIME_ENABLED=true`

## Runtime behavior

- 优先 Qwen；失败/超时/缺 key/网络异常 → Piper；再失败 → macOS say
- 延迟阈值：800/1200/2000ms
- 熔断：3 次失败 → 5 分钟跳过 Qwen；half-open 探测恢复

