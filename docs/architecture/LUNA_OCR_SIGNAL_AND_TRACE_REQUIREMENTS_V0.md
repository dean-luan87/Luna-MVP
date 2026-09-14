# LUNA OCR Signal and Trace Requirements v0

## Phase

- Phase-ModelOCR-001（OCR Independent Capability Definition v0）

## Purpose

冻结 OCR 独立能力在离线评测中的：

- perception signal（`ocr_navigation_signal`）要求
- trace / replay / whitebox 要求（只定义产物形状与字段，不实现 runtime）
- 审计字段与验收指标（用于后续回归）

## Signal requirements

OCR 作为独立感知源仅输出：

- `ocr_navigation_signal`（candidate-only）

必须包含（至少）：

- `signal_type`
- `signal_status`
- `sample_id`
- `frame_id`
- `timestamp_ms`
- `ocr_runtime_mode`
- `text_candidates[]`（可为空）
- `allows_execute_now=false`
- `real_tts_invoked=false`
- `unsupported_or_uncertain`（保守默认）

## Trace requirements (v0)

每次 OCR 评测 run 必须可产生可追溯 trace（jsonl 或等价结构）并包含：

- run_id / config_id（或等价字段）
- sample_id / frame_id / timestamp_ms
- ocr_mode
- input_region_summary（full_frame vs crop_regions 的摘要）
- candidate_count
- forbidden_scan_result（是否命中禁止语义）
- fallback_used / fallback_reason
- evidence boundary snapshot（evidence_type / controlled_live_stream / pending_real_sidewalk_run 等）

说明：本阶段只冻结字段要求，不要求实现具体文件名。

## Replay requirements (v0)

必须可回放到“输入→输出候选”的最小闭环：

- 能定位对应输入帧（或其稳定引用）
- 能定位输出 signal 的完整 JSON
- 能定位 OCR 控制参数（ocr_mode、阈值、regions、hint）

## Whitebox requirements (v0)

必须能回答“为什么是 not_available / low_confidence / partial”：

- reason_codes
- unsupported_or_uncertain 标志位
- visual_medium_risk 候选字段（如 unknown 也必须显式）

## Acceptance metrics (for later implementation)

后续实现阶段至少验证：

- `ocr_signal_generated_rate`
- `text_candidate_schema_valid_rate`
- `bbox_present_rate`
- `confidence_present_rate`
- `allows_execute_now_false_rate`
- `real_tts_invoked_false_rate`
- `forbidden_output_semantic_count = 0`
- `not_available_honesty_rate`
- `trace_ready_rate`
- `replay_ready_rate`
- `whitebox_ready_rate`
- `fallback_success_rate`
- `evidence_boundary_preserved_rate`

## Evidence boundary invariants

OCR 独立能力评测必须保持（fail-closed）：

- 不进入 controlled_live_stream
- 不改变 evidence_type
- pending_real_sidewalk_run 必须保持 true

