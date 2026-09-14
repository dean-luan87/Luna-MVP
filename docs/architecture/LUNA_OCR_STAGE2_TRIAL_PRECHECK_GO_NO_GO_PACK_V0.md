# LUNA — OCR Stage-2 Dry-run Precheck Go/No-Go Pack v0

## Phase

- **Phase-Mainline-GuardedTrial-008**

## GO

- `yolo_stage1_closed_v0_confirmed=true`
- `source_policy_ready=true`
- `provider_readiness_checked=true`（static）
- `fallback_policy_ready=true`
- `raw_text_candidate_schema_ready=true`
- `output_paths_writable=true`
- `request_trace_path_writable=true`
- `trace_replay_whitebox_path_writable=true`
- `rollback_plan_ready=true`
- `abort_conditions_registered=true`
- `provider_invoked=false`
- `semantic_interpretation_enabled=false`
- `midplatform_invoked=false`
- `scene_delta_invoked=false`
- `world_context_invoked=false`
- `hard_audit` 各字段均为 safe 值

## CONDITIONAL_GO

- readiness 仅静态确认；后续阶段再验证真实 provider runtime/credentials（本阶段不做）

## NO_GO

- 任意关键输入缺失（closure / policy / schema / rollback / abort / writable path）
- 任意 forbidden scope 被触发（provider/semantic/midplatform 等）

## Commands（reference）

运行：

- `python3 tools/run_ocr_stage2_trial_precheck_v0.py --yolo-closure-root <path> --output-root logs/ocr_stage2_trial_precheck_008_<UTC>`
- `python3 tools/verify_ocr_stage2_trial_precheck_v0.py --yolo-closure-root <path> --output-root <same_output_root>`

