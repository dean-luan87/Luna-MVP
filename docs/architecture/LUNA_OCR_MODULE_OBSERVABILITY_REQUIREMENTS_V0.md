# LUNA — OCR Module Observability Requirements v0

## Phase

- **Phase-ModelOCR-Governance-001**

## Trace requirements（每次调用）

- `request_id`
- `provider_id`
- `model_config_id`
- `frame_id`
- `crop_region`
- `latency_ms`
- `provider_success`
- `fallback_used`
- `fallback_reason`
- `raw_text_count`
- `hard_blockers`
- `soft_followups`

## Replay requirements

- `input_ref`
- `frame_ref` / `crop_ref`
- `provider_config_ref`
- `output_ref`
- `model_asset_ref`
- `dependency_profile_ref`

## Whitebox requirements

- `provider_health_state`
- `readiness_status`
- `latency_profile`
- `schema_validation`
- `governance_validation`
- `not_available_reason`
- `fallback_decision`

## Artifact readiness contract

每个 OCR 评估/运行批次必须产出：
- `summary`（汇总指标）
- `per_sample_results`
- `trace`
- `replay`
- `whitebox`

并可计算：
- `trace_ready_rate`
- `replay_ready_rate`
- `whitebox_ready_rate`
- `artifact_refs_valid_rate`
