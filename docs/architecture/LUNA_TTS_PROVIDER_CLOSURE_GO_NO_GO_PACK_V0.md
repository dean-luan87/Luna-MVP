# LUNA TTS Provider Closure Go/No-Go Pack v0

## Phase

- Phase-VoiceTTS-Provider-Closure-001（Offline TTS Runtime Policy Closure v0）

## Inputs（已存在结论）

- Phase-VoiceTTS-Provider-001（Qwen provider integration）：**CONDITIONAL_GO**
  - Artifact: `docs/architecture/LUNA_QWEN_TTS_PROVIDER_GO_NO_GO_PACK_V0.md`
- Phase-VoiceTTS-Provider-Cleanup-001（offline-only disable policy）：**GO**
  - Artifact: `docs/architecture/LUNA_TTS_OFFLINE_ONLY_PROVIDER_GO_NO_GO_PACK_V0.md`
  - Evidence: `logs/verify_tts_offline_only_provider_policy_v0.json`（`all_pass=true`）

## Closure decision

- **GO**

## Frozen runtime policy（must match runtime）

- `offline_only=true`
- `provider_order=["piper"]`
- `effective_order=["piper"]`
- `filtered_out=["qwen"]`
- legacy fallback = macOS say

## Qwen status（必须明确）

- `qwen_provider_integrated=true`
- `qwen_provider_enabled_by_default=false`
- `qwen_requires_network=true`
- `qwen_allowed_in_offline_mainline=false`

## Acceptance outputs（本阶段产物）

- `docs/architecture/LUNA_OFFLINE_TTS_RUNTIME_POLICY_CLOSURE_V0.md`
- `docs/architecture/LUNA_TTS_PROVIDER_STATUS_MATRIX_V0.md`
- `docs/architecture/LUNA_TTS_PROVIDER_BOUNDARY_REGISTER_V0.md`
- `docs/architecture/LUNA_TTS_PROVIDER_CLOSURE_GO_NO_GO_PACK_V0.md`

## Hard blockers

- 无

## Soft follow-ups

- 若未来要启用在线 provider：必须进入独立 Online/Experimental branch 治理；不得破坏 offline-only 默认策略。

