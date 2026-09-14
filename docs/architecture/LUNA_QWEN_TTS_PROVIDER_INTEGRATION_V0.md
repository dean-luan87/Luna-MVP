# LUNA Qwen/Qianwen TTS Provider Integration v0

## Phase

- Phase-VoiceTTS-Provider-001（Qianwen / Qwen TTS Provider Integration into Unified TTS Entry v0）

## Goal

把 `modules/qwen_tts.py` 的“千问 TTS（text→audio）能力”包装成 Stage-2 的统一 provider，并接入：

- `capabilities/voice/runtime/tts_unified_entry.py` provider chain
- 允许通过 `capabilities/voice/config/voice_tts_config.yaml` 选择 `qwen`

本阶段只处理 **TTS provider（text→audio）**，不处理“Qwen 生成播报文本”。

## Current fact snapshot

- `main.py` 播报入口：`_submit_tts_via_unified_entry()`
- 统一入口：`capabilities/voice/runtime/tts_unified_entry.py`
- 当前 provider chain：Fish / Piper（+ legacy fallback）
- `modules/qwen_tts.py` 存在，但此前未进入统一 provider chain

## Hard boundaries (must remain true)

- Qwen TTS 只负责 **text → audio**
- 不生成播报文本
- 不决定是否播报（speech gate 仍是主权）
- 不修改导航主链、不改视觉链、不改 SceneTask/Fusion/Output candidate
- 不移除 Fish/Piper
- 不移除 legacy fallback
- provider 失败必须 fallback，不得阻塞主链
- 必须通过 unified TTS entry（不得绕过）

## Implementation

### Provider adapter

- 新增：`capabilities/voice/providers/qwen_tts_provider.py`
- provider name：`qwen`
- 输出：`TTSProviderResult(audio_bytes=...)`（不播放音频、不写文件）
- 依赖：DashScope SDK（`dashscope`）+ `DASHSCOPE_API_KEY`（可选）
- 若缺依赖或缺 key：返回结构化 `not_available`，供 fallback

### Unified entry integration

- 修改：`capabilities/voice/runtime/tts_unified_entry.py`
- 把 `qwen` provider 作为可选 provider 加入 `providers` 字典
- 是否启用由 `voice_tts_config.yaml: local_runtime.qwen.enabled` 控制（默认 false）

### Config

- 修改：`capabilities/voice/config/voice_tts_config.yaml`
  - 增加 `timeouts.qwen_ms`
  - 增加 `local_runtime.qwen` 配置块（enabled 默认 false；api_key_env 等）
  - 不改变默认 active_provider（仍由配置决定）

## Verification

- 工具：`tools/verify_qwen_tts_provider_integration_v0.py`
- 验证范围（不播放音频、不产生真实副作用）：
  - import 可用
  - 配置禁用时不阻塞并回退 legacy
  - 配置启用但缺依赖/key 时仍能回退 legacy（fail-closed）

