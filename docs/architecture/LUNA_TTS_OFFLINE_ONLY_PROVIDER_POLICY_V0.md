# LUNA TTS Offline-Only Provider Policy v0

## Phase

- Phase-VoiceTTS-Provider-Cleanup-001（Offline-Only TTS Provider Policy & Online Provider Disable v0）

## Scope

本策略只约束 **runtime TTS**（播报执行路径）的 provider chain 与配置默认值：

- `capabilities/voice/runtime/tts_unified_entry.py`
- `capabilities/voice/config/voice_tts_config.yaml`
- legacy 执行底座：`core/audio_worker.py::submit_tts` + `modules/voice.py`（macOS `say`）

## Hard boundaries（必须满足）

- **不改导航主链**：不修改决策/导航输出，不新增任何执行行为。
- **不生成播报文本**：TTS 只消费 `text_candidate`，不产生新的文本内容。
- **不绕过 unified TTS entry**：主链提交播报必须通过 `main.py::_submit_tts_via_unified_entry` → `run_tts_unified_entry`。
- **不移除 legacy fallback**：当 provider chain 失败/禁用时必须可回退到 legacy 底座（macOS say + audio_worker）。
- **不引入在线 TTS**：默认链路不得接入任何 requires_network=true 的 provider。
- **不物理删除 provider 文件**：本阶段只做 disable/gate/配置移除；删除留到后续 deletion phase（需要证明无 import 依赖+有替代）。

## Offline-only policy（写死规则）

### 1) 配置默认：offline_only=true

- `voice_tts_config.yaml` 必须包含 `offline_only: true`。

### 2) 默认 provider_order 只允许离线 provider

允许进入默认链路的 provider（v0）：

- `piper`（离线）
- legacy macOS say（不在 provider_order 内，但必须保留为 fallback 执行底座）

禁止进入默认 `provider_order`：

- `piper`（本阶段按“可能在线/不可控”保守处理）
- `qwen`（明确在线/API）

### 3) online/API provider 必须 disabled（enabled=false）

- `local_runtime.qwen.enabled: false`
- `local_runtime.piper.enabled: false`

### 4) runtime gate：offline_only=true 时强制跳过 requires_network=true provider

`tts_unified_entry.py` 在 runtime 必须执行：

- 若 `offline_only=true` 且 provider 标记/推断 `requires_network=true`（或 unknown），则该 provider 必须：
  - **不进入 effective provider_order**
  - **不允许成为 active_provider**
  - 必须在 cutover metadata 中记录被过滤列表（便于审计）

### 5) Fail-closed + fallback

任一 provider 失败时：

- 不能阻塞主循环
- 不能导致 “无任何输出” 成为默认
- 必须允许回退 legacy（由 `cutover.rollback_to_legacy_on_failure=true` 控制）

## Provider classification（用于 gate）

- **offline provider**：requires_network=false
  - 允许进入 provider_order
- **online provider**：requires_network=true
  - offline_only=true 时必须过滤
- **unknown**：按 online 处理（保守）

## Acceptance (A–J)

见 `tools/verify_tts_offline_only_provider_policy_v0.py` 的检查项：

- A Piper 保留且可被 provider chain 选择
- B macOS say legacy fallback 保留
- C Fish enabled=false 后不会被调用
- D Qwen 未接入或 enabled=false 时不会被调用
- E offline_only=true 时任何 requires_network=true provider 被跳过
- F provider_order 不包含 online provider（effective_order）
- G main.py 仍走 unified TTS entry
- H fallback 可用
- I 不生成播报文本，只消费文本
- J 不改导航主链（本阶段无相关改动）

