# LUNA TTS Qwen Preferred Runtime GO/NO-GO Pack v0

## Phase

- Phase-VoiceTTS-RuntimeMode-001：Enable Qwen Preferred Runtime Mode With Local Fallback v0

## Decision

- **GO**

## What changed

- 保留 offline-only baseline（`runtime_modes.offline_only`）
- 新增并启用当前运行模式：`tts_runtime_mode=online_prefer_qwen`
- unified entry 读取模式并决定 effective provider 顺序与过滤/回退

## Invariants

- main.py 仍只通过 unified entry 提交播报
- qwen 失败/超时/缺 key 必须 fallback
- Piper + macOS say 保留
- 不改变导航链、不生成播报文本

## Evidence

- `tools/verify_tts_runtime_mode_qwen_preferred_v0.py`（A–L）

## Hard blockers

- 无（真实 qwen 合成质量/时延仍需在线环境与 key 评估，但不阻塞本阶段“模式切换+回退”目标）

