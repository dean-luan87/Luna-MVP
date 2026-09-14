# LUNA Qwen TTS Online Experimental GO/NO-GO Pack v0

## Phase

- Phase-VoiceTTS-OnlineExp-001：Qwen TTS Controlled Online Provider Smoke v0

## Decision

- Default: **CONDITIONAL_GO**

说明：

- 若本机未安装 `dashscope` 或未设置 `DASHSCOPE_API_KEY`：只能验证 “尝试调用 + graceful fail + fallback + 不污染 offline-only 主线”，因此为 CONDITIONAL_GO。
- 若 `dashscope` 可 import 且 key 存在，并成功产出 `audio_output.wav/bin`：可升级为 GO（仍不改变 offline-only 主线）。

## Required invariants（不得破坏）

- offline-only 主线默认不变：`offline_only=true`、`provider_order=["piper"]`
- 不把 qwen 写入默认 provider_order
- Piper/macOS say 保留
- 不绕过 unified entry
- 不生成播报文本
- qwen 失败必须 fallback，不得阻塞

## Evidence

- Smoke output root（示例）：`logs/qwen_tts_online_smoke_001_<timestamp>/`
  - `qwen_tts_online_smoke_result.json`
  - `verify_qwen_tts_online_smoke_v0.json`

## Hard blockers

- 无（本阶段不要求一定合成成功；允许缺依赖/缺 key 的 fail-closed 证据）

