# Phase-CoreCapability-TRW-Unified-001
# OCR RequestTrace Stage Mapping Definition v0

**目的**：定义 OCR 在统一 RequestTrace 视图中的 stage 名称与字段要求（只定义，不实现）。  
**范围**：OCR offline source policy（closed_v0 scope 内）与离线 raw text 产出；不包含真实中台 runtime 接线。

---

## 1. Stage 列表（v0）

- `request_trace.stage.perception.ocr.source_policy_selection`
- `request_trace.stage.perception.ocr.input_region`
- `request_trace.stage.perception.ocr.provider_invocation`
- `request_trace.stage.perception.ocr.raw_text_result`
- `request_trace.stage.perception.ocr.length_segmentation`
- `request_trace.stage.perception.ocr.reading_order`
- `request_trace.stage.perception.ocr.observability_envelope`

---

## 2. 字段要求（最小）

每个 stage 至少应包含（缺失必须 missing_* 记录，不得伪造）：

- `request_id`
- `trace_id`（可空）
- `session_id`（可空）
- `source_run_id`（离线 run 必须）
- `frame_id`（可空：若非视频帧，可用 image_id 或 sample_id）
- `crop_region`（输入 ROI；可空）
- `source_policy_id`（如 `ocr_default_offline_raw_text_source_policy_v0`）
- `provider_selected`
- `fallback_used`（bool）
- `provider_latency_ms`（可空）
- `trace_ref` / `replay_ref` / `whitebox_ref`
- `semantic_interpretation_enabled=false`（硬规则：本链为 raw text，不做语义解释）
- `downstream_invocation_count=0`（硬规则：不触发下游执行）
- `real_tts_invoked=false`（硬规则：不触发真实播报）

### raw_text_result 额外字段（建议）

- `raw_text_candidate_count`
- `raw_text_joined_length`
- `raw_text_segments_count`
- `reading_order_confidence`（可空）

---

## 3. 边界与禁止项（继承 closed_v0）

- 不得把该 mapping 当作真实中台 OCR runtime 接线证明
- 不得把 raw text 当作事实/世界知识写入
- 不得触发真实播放/真实 TTS

