# LUNA — OCR Stage-2 Trial Runner Skeleton v0

## Phase

- **Phase-Mainline-GuardedTrial-008**

## Purpose

定义 OCR Stage-2 的 runner **骨架输出**（plan record），用于后续阶段接线前审计与对齐：

- 默认 **skeleton_only**
- 默认 **provider_execution_enabled=false**
- 默认 **semantic_interpretation_enabled=false**
- 默认 **midplatform_forward_enabled=false**

## Output schema（runner skeleton）

`tools/run_ocr_stage2_trial_precheck_v0.py` 会输出：

- `ocr_stage2_trial_runner_skeleton.json`

字段：

- `runner_id`
- `trial_id`
- `runner_mode`: `skeleton_only`
- `provider_execution_enabled`: `false`
- `semantic_interpretation_enabled`: `false`
- `midplatform_forward_enabled`: `false`
- `request_trace_enabled`: `true`
- `abort_on_provider_error`: `true`
- `rollback_on_abort`: `true`
- `execution_result`: `not_executed_skeleton_only`

## Boundaries

- 本文件不授权真实执行 OCR provider
- 不进入 MidPlatform / SceneDelta / WorldContextEvidence

