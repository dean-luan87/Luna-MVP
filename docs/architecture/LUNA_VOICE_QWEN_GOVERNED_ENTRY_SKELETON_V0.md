# LUNA Voice — Governed Qwen/TTS Entry Skeleton v0（Phase-Voice-Qianwen-002）

**定位**：在 **不接真实 Qwen / 不执行真实 TTS / 不播报** 的前提下，实现 **`GovernedVoiceProviderEntry` 离线 skeleton**，串联：

**Voice Governance Decision（Phase-002 样本）→ GovernedVoiceProviderEntry → provider_selection_dry_run → VoiceSpeakabilityAuditV0 → trace/replay/whitebox**。

**代码入口**：`capabilities/voice/output/governed_voice_provider_entry_v0.py`  
**评测脚本**：`tools/evaluate_voice_qwen_governed_entry_skeleton_v0.py`  
**静态验收**：`tools/verify_voice_qwen_governed_entry_skeleton_v0.py`

---

## 1. 硬边界（本阶段）

- **不得**修改 `voice_tts_config.yaml` 默认基线语义；**不得**通过改默认 provider 完成验收。  
- **不得**调用 DashScope / `QwenTTSProvider` 真实合成 / Piper 可执行文件 / 播放。  
- **不得**进入导航 / SceneTask / Fusion / Output 编排扩展（仅 skeleton）。  

---

## 2. 当前状态字段（相对 Phase-001 合同）

| 字段 | 本阶段目标 |
|------|------------|
| `contract_defined` | **true**（承接 Phase-001） |
| `static_verifier_passed` | **true**（运行 `verify_voice_qwen_governed_entry_skeleton_v0.py` 后） |
| `runtime_wiring_done` | **false**（尚未接入 `run_tts_unified_entry` 真实链路） |
| `real_qwen_invoked` | **false** |
| `real_tts_invoked` | **false** |
| `default_policy_changed` | **false** |

评测汇总见各次输出目录中的 `voice_qwen_governed_entry_summary.json`。

---

## 3. Skeleton 语义摘要

1. **entry_allowed**：仅当 governance `final_action` 为 **`accepted_dry_run`** 或 **`fallback_candidate`** 时为 `true`（与「允许进入 provider dry-run」对齐）。  
2. **online_prefer_qwen**：`provider_order = [qwen, piper]`；健康且 `accepted` → **选中 `qwen` dry-run**；`fallback_candidate`/不健康 → **选中 `piper` dry-run**。  
3. **offline_only**：仅 **`[piper]`**，**永不选 `qwen`**。  
4. **SpeakabilityAudit**：`qwen-tts` 层 **不改写** → `provider_input_text == spoken_text`（在允许合成且 guard 可 speakable 时）；guard 归一化导致的差异记入 `text_diff_audit`（`rewrite_source=guard_v1_speakable_text`）。  
5. **hard_audit**：强制保持 **`real_*` false、invocation 计数 0**。

---

## 4. 关联文档

- `LUNA_VOICE_GOVERNED_PROVIDER_ENTRY_CONTRACT_V0.md`（Phase-001）  
- `LUNA_VOICE_SOURCE_TEXT_SPOKEN_TEXT_DIFF_AUDIT_SCHEMA_V0.md`（Phase-001）  
- `LUNA_VOICE_QWEN_GOVERNED_ENTRY_TEST_MATRIX_V0.md`（本 Phase 测试矩阵）  
- `LUNA_VOICE_QWEN_GOVERNED_ENTRY_GO_NO_GO_PACK_V0.md`（决策包）
