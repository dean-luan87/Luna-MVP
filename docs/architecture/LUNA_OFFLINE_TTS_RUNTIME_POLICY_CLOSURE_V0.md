# LUNA Offline TTS Runtime Policy Closure v0

## Phase

- Phase-VoiceTTS-Provider-Closure-001（Offline TTS Runtime Policy Closure v0）

## Purpose

收口并冻结“当前 TTS runtime 主链策略”，避免混淆：

- **Qwen provider 已接入（integrated）** ≠ **Qwen 被允许进入当前主链（allowed）**

本文件是“口径冻结”，不新增实现、不启用在线 provider、不改导航/文本生成语义。

## Frozen runtime facts（以 Cleanup-001 为准）

- `offline_only = true`
- `provider_order = ["piper"]`
- `effective_order = ["piper"]`
- `filtered_out = ["qwen"]`
- `legacy fallback = macOS say`（通过 `core/audio_worker.py::submit_tts` 异步执行）

## Current runtime chain（主链认知）

- **当前 TTS 主链**：Piper →（失败/回滚）→ macOS say（legacy fallback）
- **在线 TTS**：默认禁用（不进入 offline mainline）
- **Qwen/Fish**：不进入 offline mainline

## Provider final status（必须写死的口径）

### Piper

- 保留：**主离线 TTS provider**

### macOS say

- 保留：**legacy fallback**

### Fish

- 状态：**禁用，移出默认链**

### Qwen / Qianwen TTS（DashScope）

- 状态：**已具备 provider 接入能力，但默认禁用，不允许进入 offline mainline**

必须满足以下口径同时成立：

- `qwen_provider_integrated = true`
- `qwen_provider_enabled_by_default = false`
- `qwen_requires_network = true`
- `qwen_allowed_in_offline_mainline = false`

### pyttsx3

- 状态：**不初始化，不作为当前主链**

## Governance（恢复在线 provider 的唯一入口）

若未来要允许 Fish/Qwen 进入主链：

- 必须单独开启 **Online TTS Experimental Branch**（或同等治理阶段）
- 必须提供网络/密钥/依赖治理、回归门槛、以及“不破坏 offline-only 默认策略”的证据
- 不得直接在 offline mainline 默认链路启用

## Phase outcomes summary

- Phase-VoiceTTS-Provider-001（Qwen provider integration）：**CONDITIONAL_GO**
- Phase-VoiceTTS-Provider-Cleanup-001（offline-only disable policy）：**GO**
- current_runtime_policy：**offline-only**

