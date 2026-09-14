# LUNA — OCR Module Health Metrics v0

## Phase

- **Phase-ModelOCR-Governance-001**

## Availability

- `provider_import_ok`
- `provider_initialized`
- `model_assets_ready`
- `dependency_ready`
- `provider_available_rate`
- `ocr_result_generated_rate`

## Latency / Throughput

- `avg_latency_ms_per_frame`
- `p50_latency_ms_per_frame`
- `p95_latency_ms_per_frame`
- `max_latency_ms_per_frame`
- `frames_per_second`
- `timeout_count`
- `latency_budget_violation_count`

## Output Schema

- `raw_text_candidate_schema_valid_rate`
- `bbox_present_or_declared_rate`
- `confidence_present_or_declared_rate`
- `raw_text_joined_present_rate`
- `line_order_present_rate`
- `reading_order_fields_present_rate`

## Raw Text Quality（定义，不在本阶段实测）

- `text_exact_match_rate`
- `character_error_rate`
- `word_error_rate`
- `digit_accuracy`
- `chinese_text_accuracy`
- `english_text_accuracy`
- `missed_text_count`
- `false_text_count`
- `duplicate_text_count`
- `line_order_accuracy`
- `block_order_accuracy`

## Governance / Safety

- `semantic_interpretation_disabled_rate`
- `allows_execute_now_false_rate`
- `real_tts_invoked_false_rate`
- `downstream_invocation_count`
- `forbidden_semantic_output_count`
- `navigation_instruction_leakage_count`
- `evidence_type_mutation_count`
- `pending_real_sidewalk_run_closed_count`

## Fallback / Degradation

- `fallback_used_rate`
- `fallback_success_rate`
- `not_available_honesty_rate`
- `dependency_missing_count`
- `model_asset_missing_count`
- `provider_exception_count`
- `fail_closed_count`
- `fallback_reason_present_rate`

## Observability

- `trace_ready_rate`
- `replay_ready_rate`
- `whitebox_ready_rate`
- `per_sample_result_ready_rate`
- `summary_ready`
- `artifact_refs_valid_rate`

## Latency profile suggestions

### `realtime_region_ocr`
- `avg_latency_ms_per_frame <= 150`
- `p95_latency_ms_per_frame <= 300`
- `hard_timeout_ms = 800`

### `realtime_full_frame_low_frequency`
- `avg_latency_ms_per_frame <= 300`
- `p95_latency_ms_per_frame <= 600`
- `hard_timeout_ms = 1200`

### `offline_batch_ocr`
- 可放宽延迟，但必须可复现、可观测、可回放。

## Current reference observation

- RapidOCR（004C 归档）约 106 ms/frame，可进入 realtime_region 候选叙事。
- macOS Vision（004A 归档）约 460 ms/frame，仅适合 fallback/offline/low-frequency。
