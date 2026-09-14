# LUNA Voice — Speakability & Diff Audit Stage Mapping v0（Phase-Voice-Qianwen-003）

## Speakability stage

**Stage**：`request_trace.stage.output.voice.qwen_entry.speakability_audit`

携带 **`provider_boundary`**：**`provider_kind=text_to_audio`**、**`expression_provider=false`**、**`model_may_rewrite_text=false`**（qwen-tts 不重写语义）。

## Text diff audit stage

**Stage**：`request_trace.stage.output.voice.qwen_entry.text_diff_audit`

与 **`voice_qwen_text_diff_audit_table.json`** 对齐；其中 **`diff_type`** 将骨架侧的 **`formatting_only`** 规范为 **`guard_normalization`** 以利于观测（归因 guard）。

---

## 规则（冻结）

| 规则 | 说明 |
|------|------|
| **provider_caused_rewrite** | 必须为 **false**（qwen-tts 不产生改写） |
| **guard 归一化** | `text_changed=true` 且 **`rewrite_source=guard_v1_speakable_text`**，`diff_type=guard_normalization` |
| **blocked 样本** | `spoken_text` 可为空串；须结合 **`entry_block_reason`** / governance final_action 解释 |

---

## 表产物

- **`voice_qwen_speakability_audit_stage_table.json`**
- **`voice_qwen_text_diff_audit_table.json`**
