# LUNA — YOLO Offline Source Selection & Fallback Policy v0 (Phase-ModelPerception-012)

## Policy identity
- **source_policy_id**: `yolo_default_offline_perception_source_v0`

## Selection priority（优先级）
离线评测 perception candidate source 选择顺序：
1. **YOLO shadow**（满足准入条件时）
2. **baseline/mock**（任何不满足/失败/越界 => 必须回退）

## YOLO shadow default selection条件（必须全部满足）
当且仅当：
1. offline_evaluation=true
2. option_scope=OptionA
3. evidence_type=phone_local_controlled_capture
4. controlled_live_stream=false
5. pending_real_sidewalk_run=true
6. disable_yolo=false
7. dependency_readiness=pass
8. yolo_shadow_contract_valid=true（schema valid + artifacts ready + forbidden semantic scan pass）
9. evidence_boundary_ok=true
10. safety_leakage_detected=false

则：
- source_selected=`yolo_shadow`
- fallback_used=false

## Fallback规则（必须回退 baseline/mock）
出现任一即必须回退：
- disable_yolo=true
- dependency_readiness_fail
- model_load_failed
- model_inference_failed
- schema_validation_failed（Perception-001 五类 signals 不完整 / allows_execute_now != false）
- forbidden_output_detected（或 forbidden semantic scan 非 0）
- replay/whitebox/trace missing
- evidence_boundary_violation（evidence_type/controlled_live_stream/phone_local_capture/pending_real_sidewalk_run 任一不满足）
- unsupported_scope（option_scope != OptionA）
- controlled_live_stream=true
- non_phone_local_evidence
- safety_leakage_detected（execute/default-on/release-retry-reopen/side effects/forced action 任一非 0）

回退后必须记录：
- source_selected=`baseline_mock`
- fallback_used=true
- fallback_reason=<枚举/字符串原因>

## Rollback-to-baseline（策略级回退）
即使 YOLO 选择条件满足，也必须保留随时切回 baseline/mock 的机制：
- 通过 `disable_yolo=true` 强制回退（offline evaluation only）
- 通过 `fallback_reason` 记录触发原因

## 禁止误解释（必须写死）
- `source_selected=yolo_shadow` 仅表示 **offline evaluation 默认源**，不得解释为 runtime 默认源。
- 任何回退都不得被解释为“关闭 pending_real_sidewalk_run”或“允许真实执行”。

