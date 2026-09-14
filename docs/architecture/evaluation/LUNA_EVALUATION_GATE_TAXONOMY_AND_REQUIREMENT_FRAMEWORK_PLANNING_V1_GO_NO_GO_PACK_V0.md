# Luna Evaluation — Gate Taxonomy and Requirement Framework Planning v1 — GO / NO-GO Pack v0

**Phase**：`Phase-Gate-Taxonomy-and-Requirement-Framework-Planning-v1-001`

## GO 条件（必须全部满足）

- required roots 全部 `loaded=true`（可选 roots 允许 `optional_missing`）
- Gate Constitution 已定义：
  - `gate_constitution_defined=true`
  - `gate_constitution_article_count >= 12`
  - `gate_constitution_above_taxonomy=true`
  - `gate_constitution_below_safety_constitution=true`
  - `gate_constitution_is_design_constraint=true`
  - `gate_constitution_not_runtime=true`
  - `gate_constitution_not_replacing_safety_constitution=true`
- taxonomy 产物完整：
  - `gate_type_count >= 20`
  - `gate_level_count >= 8`
  - `gate_decision_count >= 18`
  - `dependency_graph_scenario_count >= 7`
  - `consolidation_risk_count >= 10`
- 必须定义的 gate 类型存在：
  - SafetyConstitutionGate / DomainSafetyGate / CapabilityRuntimePreGate / SourceQualityGate / FreshnessTTLGate
  - PrivacyFilteringGate / ResourceBudgetGate / EvidenceAdmissionGate / FactAdmissionGate / MemoryAdmissionGate
  - OutputGate / ActionReleaseGate / ReviewHumanAssistanceGate / FallbackDegradationGate
  - FileBoundaryGate / OCRRequestGate / MapLocationAuthorityGate / TrackingActivationGate
  - WorldObservationHandoffGate / ExperimentSimulationGate
- 权威与约束必须成立：
  - `safety_gate_highest_authority=true`
  - `user_instruction_cannot_override_safety=true`
  - `map_ocr_memory_cannot_override_safety=true`
  - `task_goal_cannot_override_safety=true`
  - `simulation_gate_cannot_grant_runtime=true`
  - `candidate_gate_cannot_grant_fact=true`
  - `output_gate_cannot_release_action=true`
  - `capability_gate_cannot_grant_action=true`
  - `map_location_gate_cannot_grant_action=true`
  - `action_release_gate_required_for_real_action=true`
  - `write_admission_gate_required_for_fact_memory_worldmodel=true`
  - `runtime_release_gate_required=true`
  - `write_admission_gate_required=true`
  - `action_release_gate_required=true`
  - `speech_output_gate_required=true`
  - `source_chain_required_by_default=true`
  - `timestamp_required_by_default=true`
  - `reason_code_required_by_default=true`
  - `violations_field_required_by_default=true`
  - `audit_required_by_default=true`
  - `verifier_template_required_by_default=true`
  - `rollback_required_for_runtime_write_action_gate=true`
- 无副作用冻结：
  - `no_runtime_executed=true`
  - `no_new_runtime_enabled=true`
  - `existing_gate_behavior_changed=false`
  - `gate_runtime_implemented=false`
  - `gate_merge_executed=false`
  - 且所有 file-op/runtime/write/action/speech flags 维持 false
- 最终输出必须为：
  - `final_decision=GATE_TAXONOMY_AND_REQUIREMENT_FRAMEWORK_PLANNING_READY_FOR_MIDPLATFORM_FUNCTION_GOVERNANCE`
  - `recommended_next_phase=Phase-MidPlatform-Function-Governance-and-Consolidation-Planning-v1-001`

## NO-GO 条件（任一触发即 NO_GO）

- required root 缺失
- 发生任一真实文件操作或 runtime（stat/exists/open/read/hash/EXIF/probe/camera/OCR provider/tracking/map/speech）
- 修改既有 gate 行为或执行 gate 合并
- 伪造“Gate Constitution 是 runtime / 替代 Safety Constitution / 直接授权能力”
- `boundary_ok=false` 或 `violations` 非空

## Verifier 阈值

- `MIN_CHECKS >= 240`
- `BASELINE_REQUIREMENT = 200`

