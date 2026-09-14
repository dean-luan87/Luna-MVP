# LUNA — YOLO Offline Source Policy Audit Requirements v0 (Phase-ModelPerception-012)

## 目的
确保后续每次离线评测在使用“YOLO 默认离线源策略”时：
- 可复现（inputs/weights/deps/flags 完整）
- 可审计（source selection / fallback / contract validity 可追溯）
- 不被误解为 runtime default

## Required audit fields（后续所有离线评测 summary 必须记录）
当策略生效或被评估时，summary 至少包含：

### Policy identity / scope
- source_policy_id: `yolo_default_offline_perception_source_v0`
- offline_evaluation=true
- option_scope=OptionA
- evidence_type=phone_local_controlled_capture
- controlled_live_stream=false
- pending_real_sidewalk_run=true

### Selection result
- source_selected: `yolo_shadow` | `baseline_mock`
- fallback_used: true|false
- fallback_reason: string（若 fallback_used=true 必填）

### YOLO execution metadata（若 source_selected=yolo_shadow）
- yolo_invoked: true|false
- detection_count_total: int（或 per-sample + total）
- model_config_id: string
- weights_source: string（例如 torchhub_ultralytics | pinned_local_weights 等）
- dependency_readiness_status: pass|fail + details（模块缺失/版本等）

### Contract / governance invariants
- yolo_shadow_contract_valid: true|false
- scene_context_gate_required: true
- allows_execute_now=false（候选-only 不可变）
- real_tts_invoked=false

### Boundary invariants
- evidence_boundary_ok=true|false（聚合）
- safety_leakage_detected=false|true（聚合）

## Forbidden audit ambiguity
- 不允许缺失 `source_selected/fallback_used/fallback_reason`（否则不可复核）
- 不允许把 `source_selected=yolo_shadow` 写成 runtime default 或 production default 的任何措辞

