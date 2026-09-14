# LUNA Voice — Governed Entry RequestTrace Integration v0（Phase-Voice-Qianwen-003）

**定位**：将 Phase-002 **GovernedVoiceProviderEntry dry-run** 产物映射为 **RequestTrace / TRW shadow** 可消费的 **stage 序列**，进入统一观测面；**不接**真实 provider、**不接** `run_tts_unified_entry`、**不播报**。

**工具**：`tools/evaluate_voice_qwen_governed_entry_request_trace_v0.py`  
**验收**：`tools/verify_voice_qwen_governed_entry_request_trace_v0.py`

---

## 1. Namespace

- **`voice_qwen_governed_entry_v0`**

---

## 2. Stage 列表（冻结）

| Stage |
|-------|
| `request_trace.stage.output.voice.qwen_entry.governance_source` |
| `request_trace.stage.output.voice.qwen_entry.provider_mode` |
| `request_trace.stage.output.voice.qwen_entry.provider_selection` |
| `request_trace.stage.output.voice.qwen_entry.speakability_audit` |
| `request_trace.stage.output.voice.qwen_entry.text_diff_audit` |
| `request_trace.stage.output.voice.qwen_entry.final_entry_decision` |
| `request_trace.stage.output.voice.qwen_entry.audit_envelope` |

每条 stage 载荷保留：**request_id、provider_mode、selected_provider、provider_order、source_governance_decision_id、source_text、provider_input_text、spoken_text、text_diff_audit、hard_audit**（与 evaluate 输出一致）。

---

## 3. 输入根目录（Phase-002）

- **online**：`logs/voice_qwen_governed_entry_002_online_prefer_qwen_20260506_035322Z/`（示例）
- **offline**：`logs/voice_qwen_governed_entry_002_offline_only_20260506_035404Z/`（示例）

---

## 4. 产物（示例目录）

见 evaluate 生成的 `voice_qwen_entry_request_trace_summary.json` 中的 **`output_root`**。

---

## 5. 关联文档

- `LUNA_VOICE_QWEN_PROVIDER_SELECTION_STAGE_MAPPING_V0.md`
- `LUNA_VOICE_QWEN_SPEAKABILITY_DIFF_AUDIT_STAGE_MAPPING_V0.md`
- `LUNA_VOICE_QWEN_GOVERNED_ENTRY_REQUEST_TRACE_TEST_MATRIX_V0.md`
- `LUNA_VOICE_QWEN_GOVERNED_ENTRY_REQUEST_TRACE_GO_NO_GO_PACK_V0.md`
