# LUNA TTS Provider Boundary Register v0

## Phase

- Phase-VoiceTTS-Provider-Closure-001（Offline TTS Runtime Policy Closure v0）

## Scope

仅约束 **runtime TTS**（播报执行路径）的 provider 与入口策略。

## Hard boundaries（禁止项）

- **禁止新增 provider**：本阶段不新增任何新的 TTS provider。
- **禁止启用在线 provider**：不得启用 Qwen/Fish 进入 offline mainline 默认链路。
- **禁止删除离线能力**：不得删除 Piper；不得删除 macOS say legacy fallback；不得删除 `core/audio_worker.py::submit_tts`。
- **禁止绕过统一入口**：主链提交播报不得绕过 `capabilities/voice/runtime/tts_unified_entry.py`。
- **禁止生成播报文本**：TTS provider 只能消费文本（text→audio），不得生成/改写播报内容。
- **禁止改导航主链**：不得修改导航/决策输出与执行行为。

## Runtime policy（必须满足）

- **offline-only**：`offline_only=true` 时：
  - `requires_network=true` 的 provider **必须被 gate 阻断**
  - `requires_network=unknown` 的 provider **按 online 处理并阻断**
  - 默认 `provider_order` 必须仅包含离线 provider（当前冻结为 `["piper"]`）

## Qwen clarity rule（口径冻结）

- **Qwen provider integrated**（接入完成）不等于 **Qwen allowed in offline mainline**（允许进入主链）。
- 当前冻结状态：
  - `qwen_provider_integrated=true`
  - `qwen_provider_enabled_by_default=false`
  - `qwen_requires_network=true`
  - `qwen_allowed_in_offline_mainline=false`

