# LUNA — Offline Perception Source Policy Integration Evidence Matrix v0 (Phase-EngineeringFlow-002-Fix)

## Artifacts
- YOLO selected run output_root: `logs/perception_eval_yolo_default_source_policy_ef002_20260428_102332`
- fallback run output_root: `logs/perception_eval_yolo_default_source_policy_fallback_ef002_20260428_102332`

## Evidence matrix（H / I / J）

### H. YOLO 输出合同校验（五类 signal schema）
- **YOLO selected run**: pass
  - summary.signal_completeness 五类=1.0
  - per-sample `signal_schema.ok=true` 且 `missing=[]`
- **fallback run**: pass
  - baseline/mock 五类均 present，schema ok

### I. forbidden scan / safety boundary / fallback 行为
- **YOLO selected run**: pass
  - safety leakage=0（execute/default_on/side_effects_expansion 均 0）
  - `allows_execute_now=false`，`real_tts_invoked=false`
  - policy 选择 YOLO 后，PerceptionEval 校验失败会 fallback（实现中有 `yolo_shadow_contract_valid` gate）
- **fallback run**: pass
  - `source_selected=baseline_mock`
  - `fallback_used=true`，`fallback_reason=disable_yolo_true`
  - safety leakage=0

### J. 审计字段齐全
- **YOLO selected run**: pass
  - summary.source_policy 字段齐全（applied_rate/yolo_selected_rate/yolo_invoked_rate/detection_count_total 等）
  - per-sample 审计字段齐全（source_selected/fallback_used/disable_yolo/yolo_invoked/model_config_id/weights_source/...）
- **fallback run**: pass
  - per-sample `fallback_reason` present

## Evidence boundary（补充）
- 两次运行 summary.evidence_boundary 各项 rate=1.0（evidence_type/controlled_live_stream/phone_local_capture）
- per-sample `pending_real_sidewalk_run=true`

