# Luna Evaluation — Safety Constitution Policy v1

对应 phase：`Phase-Luna-Safety-Constitution-Policy-v1-001`

## 运行命令

```bash
python3 tools/evaluation/governance/run_luna_safety_constitution_policy_v1.py
python3 tools/evaluation/governance/verify_luna_safety_constitution_policy_v1.py
```

## 输入 roots

必须加载：

- `_eval_out/post_controlled_frame_input_roadmap_decision_v1_smoke_v0/`
- `_eval_out/controlled_frame_input_closure_v1_smoke_v0/`
- `_eval_out/map_location_readonly_context_policy_v1_smoke_v0/`
- `_eval_out/basic_navigation_loop_vision_strengthening_closure_v1_smoke_v0/`
- `_eval_out/safety_task_arbitration_policy_v1_smoke_v0/`
- `_eval_out/minimal_runtime_integration_closure_v1_smoke_v0/`
- `_eval_out/ocr_mainline_final_closure_v1_smoke_v0/`

可选加载：

- `voice_command_ownership_gate_policy_v1`
- `voice_interruption_governance_dryrun_v1`
- controlled output / text-only output closure
- task manager / task state dry-run outputs
- MapAnchor / GPS / Route context docs
- OCR TTL / source validation / evidence pack docs
- WorldModel / Memory handoff boundary docs
- previous safety / risk / navigation governance docs

## 输出目录

runner 输出目录固定为：

`_eval_out/luna_safety_constitution_policy_v1_smoke_v0/`

必须包含：

- `summary.json`
- `input_root_matrix.json`
- `luna_safety_constitution_policy.json`
- `global_safety_principles.json`
- `high_risk_domain_matrix.json`
- `evidence_boundary_policy.json`
- `uncertainty_output_policy.json`
- `user_instruction_boundary_policy.json`
- `action_authority_boundary_policy.json`
- `crossing_safety_inheritance_policy.json`
- `future_survival_constitution_upgrade_path.json`
- `safety_constitution_scenario_matrix.json`
- `safety_constitution_boundary_matrix.json`
- `governance_debt_register.json`
- `next_phase_recommendation.json`
- `no_runtime_boundary_report.json`
- `no_write_boundary_report.json`
- `verifier_report.json`

## Verifier Pass Requirements

`verify_luna_safety_constitution_policy_v1.py` 必须至少检查 `180` 项，baseline requirement 为 `140`。

必须验证：

1. 必需输入 roots 全部加载成功
2. `luna_safety_constitution_policy`、`global_safety_principles`、`high_risk_domain_matrix`、`evidence_boundary_policy`、`uncertainty_output_policy`、`user_instruction_boundary_policy`、`action_authority_boundary_policy`、`crossing_safety_inheritance_policy`、`future_survival_constitution_upgrade_path` 全部已定义
3. `scenario_count>=12`
4. `safety_over_task=true`
5. `safety_over_user_instruction=true`
6. `candidate_must_not_be_claimed_as_fact=true`
7. `unknown_must_not_be_fabricated=true`
8. `uncertainty_requires_conservative_output=true`
9. `high_risk_action_requires_special_governance=true`
10. `map_hint_is_not_fact=true`
11. `ocr_text_candidate_is_not_fact=true`
12. `visual_candidate_is_not_fact=true`
13. `memory_hint_is_not_fact=true`
14. `stale_information_cannot_drive_current_action=true`
15. `user_instruction_cannot_override_safety=true`
16. `traffic_light_candidate_not_crossing_permission=true`
17. `green_light_candidate_not_crossing_permission=true`
18. `map_crossing_hint_not_crossing_permission=true`
19. `crowd_flow_candidate_not_crossing_permission=true`
20. `OCR_countdown_text_not_crossing_permission=true`
21. `user_says_go_not_crossing_permission=true`
22. `crossing_decision_requires_special_safety_governance=true`
23. `safety_constitution_to_survival_constitution_upgrade_later=true`
24. `survival_constitution_runtime_allowed_now=false`
25. 全部 runtime / write / action / speech 字段保持 `false`
26. `boundary_ok=true`
27. 最终判定固定为：
   - `final_decision=LUNA_SAFETY_CONSTITUTION_POLICY_READY_FOR_CROSSING_DECISION_SAFETY_GOVERNANCE`
   - `recommended_next_phase=Phase-Crossing-Decision-Safety-Governance-Policy-v1-001`

## 通过语义

本阶段通过只表示：

- Luna 已正式定义统一的高风险治理上位法
- `Crossing Decision Safety Governance` 后续必须继承这层 `Safety Constitution`
- 当前仍然不做 `Crossing Decision runtime`
- 当前仍然不判断真实过街安全

本阶段通过不表示：

- 已进入 `Crossing Decision runtime`
- 已读取真实图像
- 已打开摄像头
- 已接入地图 API
- 已达到 production readiness
