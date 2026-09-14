# LUNA TTS Provider Status Matrix v0

## Phase

- Phase-VoiceTTS-Provider-Closure-001（Offline TTS Runtime Policy Closure v0）

## Frozen runtime defaults

- `offline_only=true`
- `provider_order=["piper"]`

## Matrix

| Provider | Type | offline_local | requires_network | requires_api_key | integrated | enabled_by_default | in_provider_order | allowed_in_offline_mainline | runtime_role |
|---|---|---:|---:|---:|---:|---:|---:|---:|---|
| piper | Stage-2 provider | true | false | false | true | true | true | true | primary offline provider |
| legacy_macos_say | legacy executor | true | false | false | true | true | false | true | legacy fallback executor |
| piper（已移除 Fish）| Stage-2 provider | unknown | unknown/treated-online | false | true | false | false | false | disabled / filtered_out |
| qwen | Stage-2 provider | false | true | true | true | false | false | false | integrated-but-disabled (online) |
| pyttsx3 | legacy library | true | false | false | true | false | false | false | not initialized / not mainline |

## Notes

- “integrated=true” 表示代码层面可被 `tts_unified_entry` 注册/引用；不代表 “allowed_in_offline_mainline=true”。
- Fish 在本阶段按保守策略处理：`requires_network=unknown` 在 `offline_only=true` 下视作 online 并过滤。

