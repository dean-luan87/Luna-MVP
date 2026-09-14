# Phase-CoreCapability-TRW-Unified-002
# OCR RequestTrace Shadow Adapter v0

**目标**：把 OCR local TRW / benchmark / offline source policy 输出映射为统一 RequestTrace shadow chain（只读、shadow-only）。

---

## 1. 典型输入结构（示例）

以 `ocr_offline_source_policy_009_normal_20260429_124053` 为例：

- `ocr_benchmark_summary.json`（含 provider_selected / source_policy_id / hard audit）
- `trace/<provider>_trace.jsonl`
- `replay/<provider>_replay.jsonl`
- `whitebox/<provider>_whitebox.jsonl`
- `raw_outputs/<provider>/ocr_sample_XXX.json`

---

## 2. 输出 stage 列表（必须）

按 Phase-CoreCapability-TRW-Unified-001：

1. `request_trace.stage.perception.ocr.source_policy_selection`
2. `request_trace.stage.perception.ocr.input_region`
3. `request_trace.stage.perception.ocr.provider_invocation`
4. `request_trace.stage.perception.ocr.raw_text_result`
5. `request_trace.stage.perception.ocr.length_segmentation`
6. `request_trace.stage.perception.ocr.reading_order`
7. `request_trace.stage.perception.ocr.observability_envelope`

每个 stage 必须包含：

- `stage_namespace="core_capability_request_trace_v0"`
- `stage_name` / `stage_order`
- `request_id` / `source_run_id`
- `trace_id=null` / `session_id=null` 且 `missing_fields` 显式记录
- `provider_selected` / `source_policy_id`（若输入可读则继承，否则允许缺失但不得伪造）
- `source_refs` 保留 `trace_ref/replay_ref/whitebox_ref/original_summary_ref/source_root`
- `hard_audit`：
  - `semantic_interpretation_enabled=false`
  - `allows_execute_now=false`
  - `downstream_invocation_count=0`
  - `navigation_action=null`
  - `real_tts_invoked=false`

---

## 3. request_id 生成策略

优先继承（若输入含 request_id）；否则：

`shadow_req_<source_run_id>_<frame_id_or_sample_id>`

并标记：
- `request_id_origin="inherited" | "deterministic_shadow"`

