# Phase-CoreCapability-TRW-Unified-004
# Unified Field-Level Mapping Report v0

**目的**：提供字段级映射表（不是结构统计），用于白盒后台与架构复盘时追溯“某个 unified 字段来自哪里、是否缺失、是否派生”。

---

## 1. 输出 schema（v0）

每一行代表一个映射条目：

- `capability`: `yolo | ocr | voice`
- `source_file`: 源文件/源产物路径（只读引用）
- `source_field`: 源字段路径（例如 `fields.model_config_id`）
- `unified_field`: unified view 中的字段路径
- `stage_name`: 关联的 stage（unified stage_name）
- `mapping_status`: `mapped | missing | derived | not_applicable`
- `notes`: 说明与约束（例如“缺失不得伪造”）

---

## 2. 覆盖要求（最小集）

### YOLO（最小覆盖）
- frame_id
- image_ref（若缺失必须标 missing）
- model_config_id
- detection_count
- confidence_summary（若缺失必须标 missing）
- bbox_summary（若缺失必须标 missing）
- trace_ref / replay_ref / whitebox_ref

### OCR（最小覆盖）
- provider_selected
- source_policy_id
- raw_text_candidate_count
- raw_text_joined_length（若未计算，必须标 missing）
- raw_text_segments_count（若未计算，必须标 missing）
- reading_order_confidence（若缺失必须标 missing）
- trace_ref / replay_ref / whitebox_ref

### Voice（最小覆盖）
- guard_result（白盒/why 字段可通过 key_fields.whitebox_extension 体现）
- speech_gate_result
- expiry_result
- cancel_result
- provider_health_result
- final_action / final_decision
- audit_envelope_ref
- trace_ref / replay_ref / whitebox_ref（可按 root-level jsonl refs 派生，但需标 derived）

---

## 3. 边界

- 不伪造缺失字段
- 不修改旧 Voice 产物
- 不接 runtime

