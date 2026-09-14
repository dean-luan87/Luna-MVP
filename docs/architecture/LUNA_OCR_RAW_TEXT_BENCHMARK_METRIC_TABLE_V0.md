# LUNA — OCR Raw Text Benchmark Metric Table v0

## Phase

- **Phase-ModelOCR-005**

## Accuracy / Raw Text

- `text_exact_match_rate`
- `normalized_text_exact_match_rate`
- `character_error_rate`
- `word_error_rate`
- `digit_accuracy`
- `chinese_text_accuracy`
- `english_text_accuracy`
- `missed_text_count`
- `false_text_count`
- `duplicate_text_count`

## Line / Layout

- `line_order_accuracy`
- `block_order_accuracy`
- `raw_text_joined_accuracy`
- `reading_direction_recorded_rate`

## BBox / Confidence

- `bbox_present_rate`
- `bbox_iou_avg`
- `bbox_precision`
- `bbox_recall`
- `bbox_f1`
- `confidence_present_rate`
- `low_confidence_honesty_rate`
- `confidence_calibration_note`

## Latency

- `avg_latency_ms_per_frame`
- `p50_latency_ms_per_frame`
- `p95_latency_ms_per_frame`
- `frames_per_second`
- `timeout_count`

## Governance

- `semantic_interpretation_disabled_rate`
- `allows_execute_now_false_rate`
- `real_tts_invoked_false_rate`
- `downstream_invocation_count`
- `forbidden_semantic_output_count`
- `navigation_instruction_leakage_count`

## Observability

- `trace_ready_rate`
- `replay_ready_rate`
- `whitebox_ready_rate`
- `per_sample_result_ready_rate`
