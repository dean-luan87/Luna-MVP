# LUNA Qwen TTS Provider GO/NO-GO Pack v0

## Phase

- Phase-VoiceTTS-Provider-001

## Decision

- Decision: **CONDITIONAL_GO**

## Why conditional

允许条件成立的原因：

- `qwen` provider 已接入 unified entry，且默认 `enabled=false`
- verifier 可以在“缺依赖/缺 key”的情况下验证 fail-closed fallback（不阻塞主链）
- 本阶段未改变导航/视觉/下游候选逻辑，也未移除 Fish/Piper/legacy

仍为 conditional 的原因：

- `qwen` 依赖网络与 API key（DashScope），在未配置 key/未安装依赖时只能验证“接入与回退”，不能验证“真实音频质量/时延”

## Hard boundary confirmation

- 不生成播报文本（仅 TTS）
- 不决定是否播报（speech gate 不变）
- 不移除 Fish/Piper/legacy
- provider 失败必须 fallback
- 不绕过 unified entry

## Artifacts

- Provider: `capabilities/voice/providers/qwen_tts_provider.py`
- Unified entry: `capabilities/voice/runtime/tts_unified_entry.py`
- Config: `capabilities/voice/config/voice_tts_config.yaml`
- Verifier: `tools/verify_qwen_tts_provider_integration_v0.py`

## Recommended next phase

- Phase-VoiceTTS-Provider-002（可选）：在受控环境下提供 DashScope key 与依赖，补充“真实合成成功率/时延/稳定性”证据与回归门槛，但不得改变主链安全边界。

