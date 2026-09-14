# LUNA TTS Runtime Mode: Qwen Preferred v0

## Phase

- Phase-VoiceTTS-RuntimeMode-001：Enable Qwen Preferred Runtime Mode With Local Fallback v0

## Goal

在 **不绕过 unified TTS entry** 的前提下：

- 保留 offline-only baseline（安全基线不删除）
- 新增并启用当前运行模式 `tts_runtime_mode=online_prefer_qwen`
- 主链播报优先调用 `qwen`；失败回退 `piper`；最终回退 `macOS say`（legacy）

## Frozen baseline (must keep)

- baseline mode: `offline_only`
  - effective provider chain: `["piper"]`
  - legacy fallback: macOS `say`

## Runtime mode (current enabled)

- current mode: `online_prefer_qwen`
  - effective provider order (runtime): `["qwen", "piper", "legacy_macos_say"]`
  - hard timeout: 2000ms（qwen_ms）
  - failures must fallback (missing key / dashscope missing / network / timeout / invalid_audio)

## Hard boundaries

- main.py 不得直接调用 qwen（必须走 unified entry）
- 不绕过 Speech Gate
- qwen 只做 text→audio，不生成/改写播报文本
- 不影响导航决策链
- 不删除 Piper / macOS say

## Config

- `capabilities/voice/config/voice_tts_config.yaml`
  - `runtime_modes.offline_only` 保留
  - `runtime_modes.online_prefer_qwen` 新增/启用
  - `tts_runtime_mode: online_prefer_qwen`

## Verification

- `tools/verify_tts_runtime_mode_qwen_preferred_v0.py`（A–L）

