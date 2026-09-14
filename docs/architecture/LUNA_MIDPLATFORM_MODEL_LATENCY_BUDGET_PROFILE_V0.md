# LUNA MidPlatform Model Latency Budget Profile v0

## Phase

- Phase-MidPlatform-ModelSwitch-001

## Purpose

冻结中台统一的延迟预算 profiles，并作为各 capability 的上界约束与默认参考。

## Profiles

### realtime_critical（延迟优先）

- soft_latency_warning_ms = 300
- first_response_budget_ms = 600
- hard_timeout_ms = 1000

适用：

- 风险提醒 / 安全播报 / 即时导航风险

约束：

- 各模块可更严，不得放宽该 profile 的 hard_timeout。

### realtime_normal（平衡）

- soft_latency_warning_ms = 800
- first_response_budget_ms = 1200
- hard_timeout_ms = 2000

适用：

- 普通 TTS
- 常规 OCR
- 普通视觉候选

### interactive_quality（质量优先但仍实时）

- soft_latency_warning_ms = 1200
- first_response_budget_ms = 2000
- hard_timeout_ms = 4000

适用：

- 高质量语音
- 复杂 OCR
- VLM 解释

### offline_batch（离线/批处理）

- soft_latency_warning_ms = 5000
- first_response_budget_ms = 10000
- hard_timeout_ms = 30000

适用：

- 离线评测 / 回归测试 / 批量分析

## First response metric note

- 若 provider 不支持 streaming/首包事件：first_response_budget_ms 记为 unsupported_first_response_metric，仍必须执行 hard_timeout。

