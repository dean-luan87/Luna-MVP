# Luna Evaluation — Safety Constitution Policy v1 GO / NO-GO Pack

对应 phase：`Phase-Luna-Safety-Constitution-Policy-v1-001`

## GO Conditions

- required roots 全部成功加载
- `luna_safety_constitution_policy` 已生成
- `global_safety_principles` 已生成
- `high_risk_domain_matrix` 已生成
- `evidence_boundary_policy` 已生成
- `uncertainty_output_policy` 已生成
- `user_instruction_boundary_policy` 已生成
- `action_authority_boundary_policy` 已生成
- `crossing_safety_inheritance_policy` 已生成
- `future_survival_constitution_upgrade_path` 已生成
- `safety_constitution_scenario_matrix` 已生成且 `scenario_count>=12`
- `safety_over_task=true`
- `safety_over_user_instruction=true`
- `candidate_must_not_be_claimed_as_fact=true`
- `unknown_must_not_be_fabricated=true`
- `uncertainty_requires_conservative_output=true`
- `high_risk_action_requires_special_governance=true`
- `map_hint_is_not_fact=true`
- `ocr_text_candidate_is_not_fact=true`
- `visual_candidate_is_not_fact=true`
- `memory_hint_is_not_fact=true`
- `stale_information_cannot_drive_current_action=true`
- `user_instruction_cannot_override_safety=true`
- `traffic_light_candidate_not_crossing_permission=true`
- `green_light_candidate_not_crossing_permission=true`
- `map_crossing_hint_not_crossing_permission=true`
- `crowd_flow_candidate_not_crossing_permission=true`
- `OCR_countdown_text_not_crossing_permission=true`
- `user_says_go_not_crossing_permission=true`
- `crossing_decision_requires_special_safety_governance=true`
- `safety_constitution_to_survival_constitution_upgrade_later=true`
- `survival_constitution_runtime_allowed_now=false`
- `no_runtime_executed=true`
- `no_new_runtime_enabled=true`
- `crossing_decision_runtime_invoked=false`
- `camera_invoked=false`
- `visual_model_invoked=false`
- `map_api_invoked=false`
- `ocr_provider_invoked=false`
- `tracking_runtime_invoked=false`
- `world_model_written=false`
- `memory_written=false`
- `library_written=false`
- `fact_written=false`
- `emotion_engine_invoked=false`
- `survival_constitution_runtime_invoked=false`
- `boundary_ok=true`
- `final_decision=LUNA_SAFETY_CONSTITUTION_POLICY_READY_FOR_CROSSING_DECISION_SAFETY_GOVERNANCE`
- `recommended_next_phase=Phase-Crossing-Decision-Safety-Governance-Policy-v1-001`

## NO-GO Conditions

- any required root missing
- global safety principles 缺失
- high-risk domain matrix 缺失
- crossing inheritance policy 缺失
- `scenario_count<12`
- `candidate_must_not_be_claimed_as_fact=false`
- `user_instruction_cannot_override_safety=false`
- `crossing_decision_requires_special_safety_governance=false`
- `crossing_decision_runtime_invoked=true`
- `camera_invoked=true`
- `visual_model_invoked=true`
- `map_api_invoked=true`
- `ocr_provider_invoked=true`
- `tracking_runtime_invoked=true`
- `world_model_written=true`
- `memory_written=true`
- `fact_written=true`
- `emotion_engine_invoked=true`
- `survival_constitution_runtime_invoked=true`
- Safety Constitution 宣称已是 Survival Constitution runtime
- next phase 不明确

## GO Meaning

本阶段 `GO` 的语义仅表示：

- Luna 已获得统一的高风险治理上位法
- `Crossing Decision Safety Governance` 现在可以继承这层上位法继续展开
- 高风险输出、候选/事实边界、用户指令边界、不确定性边界已经冻结

## Non-Claims

本阶段不主张：

- 已进入 `Crossing Decision runtime`
- 已判断真实过街安全
- 已打开摄像头
- 已读取真实图像
- 已接入地图 API
- 已升级到 `Survival Constitution runtime`
