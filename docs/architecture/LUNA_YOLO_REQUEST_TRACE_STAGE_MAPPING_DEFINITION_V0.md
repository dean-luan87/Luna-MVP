# Phase-CoreCapability-TRW-Unified-001
# YOLO RequestTrace Stage Mapping Definition v0

**目的**：定义 YOLO 在统一 RequestTrace 视图中的 stage 名称与字段要求（只定义，不实现）。  
**范围**：YOLO offline perception candidate source（closed_v0 scope 内）；不包含真实 runtime 接线。

---

## 1. Stage 列表（v0）

- `request_trace.stage.perception.yolo.input_frame`
- `request_trace.stage.perception.yolo.detector_invocation`
- `request_trace.stage.perception.yolo.detection_result`
- `request_trace.stage.perception.yolo.risk_or_object_classification`
- `request_trace.stage.perception.yolo.observability_envelope`

---

## 2. 字段要求（最小）

每个 stage 至少应包含（缺失必须 missing_* 记录，不得伪造）：

- `request_id`
- `trace_id`（可空）
- `session_id`（可空）
- `source_run_id`（离线 run 必须）
- `frame_id`
- `timestamp_ms`
- `image_ref`（文件/URI/索引引用；不得把内容直接复制进大字段）
- `model_config_id`
- `runtime_invoked`（bool；offline/shadow 通常为 false）
- `downstream_invocation_count`（int；默认 0）
- `trace_ref` / `replay_ref` / `whitebox_ref`

### detection_result 额外字段（建议）

- `detection_count`
- `object_classes`（top-k）
- `confidence_summary`（min/mean/p95 等）
- `bounding_box_summary`（数量、分布；不要求全量 bbox 展示）

---

## 3. 边界与禁止项（继承 closed_v0）

- 不得把该 mapping 当作 runtime 接入证明
- 不得伪造 `runtime_invoked=true`
- 不得引入导航动作、真实播放、真实 TTS

