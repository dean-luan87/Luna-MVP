# LUNA TTS Offline-Only Provider Go/No-Go Pack v0

## Phase

- Phase-VoiceTTS-Provider-Cleanup-001（Offline-Only TTS Provider Policy & Online Provider Disable v0）

## Decision

- **GO**

## Evidence

- **Verifier output**: `logs/verify_tts_offline_only_provider_policy_v0.json`
  - `all_pass=true`
  - `filtered_out=["qwen"]`
  - `effective_order=["piper"]`

## Final provider_order (default)

- `capabilities/voice/config/voice_tts_config.yaml`
  - `offline_only: true`
  - `provider_order: ["piper"]`

## Provider disposition

- **Keep (offline)**:
  - `piper`（Stage-2 离线 provider）
  - `modules/voice.py`（macOS `say` legacy 执行底座，保留）
  - `core/audio_worker.py::submit_tts`（异步播放底座，保留）
- **Disable (online/unknown)**:
  - `piper`：`enabled=false` 且 offline_only 下视作 `requires_network=unknown` → 被 gate 过滤
  - `qwen`：`enabled=false` 且 `requires_network=true` → 被 gate 过滤（不接入主链）
- **Legacy keep-not-initialized**:
  - `pyttsx3`（如仍存在）：保持不初始化，不作为主链依赖

## GO conditions checklist

- **当前主链只保留离线 TTS provider**：是（effective_order 仅 `piper`）
- **Piper 保留**：是
- **macOS say fallback 保留**：是
- **Fish 已移除；provider_order 仅含 piper**：是（默认 order 仅 piper；且 gate 过滤）
- **Qwen/Qianwen 不接入主链**：是（默认 order 不含 qwen；enabled=false；offline_only gate 过滤）
- **offline_only gate 生效**：是（verifier 通过）
- **verifier A–J 通过**：是（all_pass=true）

## NO_GO triggers (none observed)

- Fish 仍在默认 provider_order：否
- Qwen 依赖在线但进入主链：否
- 离线 fallback 被删：否
- main.py 绕过 unified TTS entry：否
- 在线 provider 在 offline_only=true 时仍被调用：否

## Hard blockers

- 无

## Soft follow-ups（不在本阶段执行）

- Fish 已永久移除；若需新 provider：必须明确其离线可复现依赖与 `requires_network=false` 证据，并通过单独 phase 治理。
- 若要删除 qwen 相关文件：需先证明无 import 依赖并提供替代/迁移计划（deletion phase）。

