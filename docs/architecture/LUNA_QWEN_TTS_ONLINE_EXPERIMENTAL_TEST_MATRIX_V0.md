# LUNA Qwen TTS Online Experimental Test Matrix v0

## Phase

- Phase-VoiceTTS-OnlineExp-001：Qwen TTS Controlled Online Provider Smoke v0

## Verifier

- `tools/verify_qwen_tts_online_smoke_v0.py`

## Matrix（A–J）

- **A**：offline-only 默认配置未被修改（`offline_only=true` 且 `provider_order=["piper"]` 仍成立）
- **B**：qwen 只在 `--allow-online true` 时才会被尝试调用
- **C**：无 `DASHSCOPE_API_KEY` 时不崩溃，返回失败并 fallback
- **D**：有 `DASHSCOPE_API_KEY` 时会尝试调用 provider（invoked=true）
- **E**：provider result schema 完整（成功/失败都结构化）
- **F**：fallback 可用（legacy_submit stub 被调用）
- **G**：Piper/macOS say 资产未被移除（关键文件仍存在）
- **H**：`main.py` 未被改成直接调用 Qwen（不出现 Qwen/DashScope 直连）
- **I**：不生成播报文本（只消费 `--text`）
- **J**：online experimental 结果不写回默认 config（mainline_config_mutated=false，offline_default_policy_preserved=true）

