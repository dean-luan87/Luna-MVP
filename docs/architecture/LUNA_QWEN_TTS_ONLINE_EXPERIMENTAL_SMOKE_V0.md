# LUNA Qwen TTS Online Experimental Smoke v0

## Phase

- Phase-VoiceTTS-OnlineExp-001：Qwen TTS Controlled Online Provider Smoke v0

## Goal

只验证一件事：

- 在 **显式 allow-online=true 的 online experimental mode** 下，`qwen` provider 是否能被 `tts_unified_entry` 尝试调用；
- 失败时是否 **graceful fail + fallback**；
- **不改变** offline-only 主线默认策略（配置与链路不被污染）。

## Frozen facts（不得改变）

- current_runtime_policy = offline-only（来自 Closure/Cleanup）
- `offline_only=true`
- `provider_order=["piper"]`
- `effective_order=["piper"]`
- `filtered_out=["qwen"]`
- legacy fallback = macOS say
- `qwen_provider_integrated=true` 且默认 `enabled=false`，不允许进入 offline mainline

## Hard boundaries

- 本阶段是 **online experimental branch**，必须显式 `--allow-online true`
- 不修改默认 `capabilities/voice/config/voice_tts_config.yaml`
- 不把 Qwen 加入默认 provider_order
- 不关闭 Piper，不删除 macOS say fallback
- 不调用 `main.py`
- 不接导航主链 / 不接 output candidates
- 不生成播报文本：只消费 `--text` 固定测试文本
- 必须通过 unified TTS entry
- 不播放音频（仅保存音频 bytes/文件 + 结构化结果）

## Tools

- Smoke:
  - `tools/smoke_qwen_tts_provider_online_v0.py`
- Verify:
  - `tools/verify_qwen_tts_online_smoke_v0.py`

## Environment check（建议先跑）

```bash
python3 - <<'PY'
import os
print("DASHSCOPE_API_KEY_SET=", bool(os.environ.get("DASHSCOPE_API_KEY")))
try:
    import dashscope
    print("dashscope_import=ok")
except Exception as e:
    print("dashscope_import=fail", repr(e))
PY
```

## Runbook

```bash
cd "/Users/luanlei/Desktop/Luna-Core"
TS=$(date +%Y%m%d_%H%M%S)
python3 tools/smoke_qwen_tts_provider_online_v0.py \
  --text "你好，这是 Luna 千问语音测试。" \
  --allow-online true \
  --provider qwen \
  --output-root "logs/qwen_tts_online_smoke_001_${TS}"

python3 tools/verify_qwen_tts_online_smoke_v0.py \
  --smoke-root "logs/qwen_tts_online_smoke_001_${TS}"
```

## Outputs（output-root）

- `qwen_tts_online_smoke_result.json`
- `online_experimental_voice_tts_config.yaml`（临时 config，仅用于本次实验）
- `smoke_notes.md`
- `audio_output.wav` 或 `audio_output.bin`（若成功产出 audio_bytes）
- `verify_qwen_tts_online_smoke_v0.json`（verifier 输出）

