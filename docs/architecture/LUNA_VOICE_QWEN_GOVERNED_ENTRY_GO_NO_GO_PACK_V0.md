# LUNA Voice — Governed Entry Skeleton Go / No-Go Pack v0（Phase-Voice-Qianwen-002）

---

## GO

以下条件 **全部**满足：

1. **`online_prefer_qwen`** 与 **`offline_only`** 两次 evaluate **均成功产出**（summary / decisions / audits / selection / trace / replay / whitebox）。  
2. **Qwen-first / Piper-fallback** dry-run 规则与 **`LUNA_VOICE_QWEN_GOVERNED_ENTRY_TEST_MATRIX_V0.md`** 一致。  
3. **offline_only** 路径 **永不选择 qwen**。  
4. **SpeakabilityAudit** 与 **text_diff_audit** 已生成；**qwen-tts 层级** **`model_may_rewrite_text=false`**。  
5. **blocked** 样本 **不进入** qwen 选择。  
6. **hard_audit** 不变量保持（与 Phase-008/009 审计占位相容）。  
7. **`verify_voice_qwen_governed_entry_skeleton_v0.py` → `ok: true`**。  
8. **未改** `voice_tts_config.yaml` 默认基线；**无真实 Qwen/TTS/播报**。

---

## CONDITIONAL_GO

- Provider health 仅用 governance 样本字段表达；若运行环境无法加载 Phase-002 根目录，需在备注中说明（本仓库默认自带 `logs/voice_output_governance_002_test_run`）。

---

## NO_GO

任一条：

- **blocked** 请求仍 **选中 qwen**。  
- **offline_only** 仍 **选中 qwen** 或 **order 含 qwen**。  
- 将 **qwen-tts** 标为 **expression provider** 或 **`model_may_rewrite_text=true`**。  
- **缺失** speakability / diff audit。  
- **`text_changed=true`** 且 **`rewrite_allowed=false`** 且 **`diff_type` 非 unknown**（违背 NO_GO 组合）。  
- **`real_qwen_invoked` / `real_tts_invoked` / `provider_invoked` / `playback_invoked`** 任一为真。  
- **修改默认 voice TTS 配置**或 **删除 Piper fallback**。

---

## Recommended next phase

**Phase-Voice-Qianwen-003+**：在 **不改默认基线** 前提下，将 skeleton **接线**至单一入口（在 **`run_tts_unified_entry` 之前**强制 governance），并联 RequestTrace/TRW stage 与 Phase-009 导出视图。
