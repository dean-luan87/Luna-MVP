# LUNA — OCR Module Failure and Degradation Policy v0

## Phase

- **Phase-ModelOCR-Governance-001**

## Failure taxonomy

- `dependency_missing`
- `model_asset_missing`
- `provider_import_failed`
- `provider_init_failed`
- `provider_timeout`
- `provider_exception`
- `invalid_output_schema`
- `empty_output`
- `bbox_missing`
- `confidence_missing`
- `low_confidence_output`
- `reading_order_uncertain`
- `semantic_leakage`
- `navigation_instruction_leakage`
- `downstream_invocation_leakage`
- `trace_missing`
- `replay_missing`
- `whitebox_missing`

## Required handling policy

- `dependency_missing` / `model_asset_missing` -> `not_available` + fallback
- `provider_timeout` -> fallback
- `invalid_output_schema` -> block output + fallback
- `semantic_leakage` / `navigation_instruction_leakage` -> **hard_blocker**
- `downstream_invocation_leakage` -> **hard_blocker**
- `reading_order_uncertain` -> 保留 raw candidates，但阻断语义使用
- `low_confidence_output` -> 保留 candidates，并标记 low_confidence

## Fail-closed rule

当 provider 不满足依赖/资产/schema 时：
- 必须 `fail_closed=true`
- 禁止伪造 `provider_available=true`
- 禁止输出伪造 raw_text

## Fallback strategy（定义阶段，不启用默认链）

建议链（待后续阶段启用）：
`RapidOCR -> PaddleOCR -> macOS Vision -> not_available`

当前阶段只定义，不默认启用。

Fallback 记录必须有：
- `fallback_used`
- `fallback_provider`
- `fallback_reason`
- `capability_boundary_after_fallback`
- `provider_selected`
- `provider_attempt_order`
