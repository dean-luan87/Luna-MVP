# Phase-CoreCapability-TRW-Unified-002
# YOLO RequestTrace Shadow Adapter v0

**目标**：把 YOLO local TRW / offline mainline 输出映射为统一 RequestTrace shadow chain（只读、shadow-only）。

---

## 1. 典型输入结构（示例）

以 `offline_mainline_ef004_20260428_105303` 为例：

- `stage_outputs/perception/_yolo_shadow_perception/<bucket>/per_sample_yolo_shadow_results.json`
- `stage_outputs/perception/_yolo_shadow_perception/<bucket>/yolo_shadow_trace.jsonl`
- `stage_outputs/perception/_yolo_shadow_perception/<bucket>/yolo_shadow_replay.jsonl`
- `stage_outputs/perception/_yolo_shadow_perception/<bucket>/yolo_shadow_whitebox.jsonl`

> `<bucket>` 可以是 `phone_local_001_clear_path` 等离线样本桶目录。

---

## 2. 输出 stage 列表（必须）

按 Phase-CoreCapability-TRW-Unified-001：

1. `request_trace.stage.perception.yolo.input_frame`
2. `request_trace.stage.perception.yolo.detector_invocation`
3. `request_trace.stage.perception.yolo.detection_result`
4. `request_trace.stage.perception.yolo.risk_or_object_classification`
5. `request_trace.stage.perception.yolo.observability_envelope`

每个 stage 必须包含：

- `stage_namespace="core_capability_request_trace_v0"`
- `stage_name` / `stage_order`
- `request_id` / `source_run_id`
- `trace_id=null` / `session_id=null` 且 `missing_fields` 显式记录
- `source_refs` 保留 `trace_ref/replay_ref/whitebox_ref/original_summary_ref/source_root`
- `hard_audit`：
  - `runtime_invoked=false`
  - `downstream_invocation_count=0`
  - `navigation_action=null`
  - `real_tts_invoked=false`

---

## 3. request_id 生成策略

优先继承（若输入含 request_id）；否则：

`shadow_req_<source_run_id>_<frame_id_or_sample_id>`

并标记：
- `request_id_origin="inherited" | "deterministic_shadow"`

