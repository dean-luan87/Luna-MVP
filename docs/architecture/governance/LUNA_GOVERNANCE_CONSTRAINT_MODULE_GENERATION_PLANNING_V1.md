## Phase

- **Phase ID**: `Phase-Governance-Constraint-Module-Generation-Planning-v1-001`
- **Capability**: `capabilities/governance/governance_constraint_module_generation_planning_v1.py`
- **Status**: governance-constraint-module-generation-planning-only（规划正式模块输出结构；非 module generation / 非 canonical template generation / 非 verifier integration / 非主线恢复）

## Intent

将 Legacy Extraction 全链（Planning → DryRun → Post-DryRun Review → Roadmap Decision）得到的 source evidence，收束规划为正式 **Governance Constraint Module v1** 的 12 类输出结构。

Roadmap Decision 已选定 Route A，但尚未定义 canonical contract、domain registry、inheritance matrix、frozen fields、phase lifecycle、required fields、verifier baseline、non-claims / forbidden shortcuts、extension rule、legacy absorption policy 的正式产物 shape。本阶段是「输出结构规划」，不是「开始生成模块」。

## Source Chain

- **上游**: `Phase-Governance-Constraint-Module-Legacy-Extraction-Roadmap-Decision-v1-001`（GO；Route A selected）
- **治理约束引用**: `governance_constraints_ref=migration_governance_development_constraints_v1`
- **Legacy 定位**: `legacy_as_source_evidence=true`；`legacy_as_template_source=false`

## Planned Output Shapes（12 类正式模块产物）

| 规划对象 | 未来正式产物 | 本阶段 planning 产物 |
|----------|-------------|---------------------|
| CanonicalPhaseContractOutputShapePlanning | `governance_canonical_phase_contract_v1.json` | `canonical_phase_contract_output_shape_planning_v1.json` |
| DomainConstraintRegistryOutputShapePlanning | `governance_domain_constraint_registry_v1.json` | `domain_constraint_registry_output_shape_planning_v1.json` |
| PhaseInheritanceMatrixOutputShapePlanning | `governance_phase_inheritance_matrix_v1.json` | `phase_inheritance_matrix_output_shape_planning_v1.json` |
| CanonicalFrozenFieldsOutputShapePlanning | `governance_canonical_frozen_fields_v1.json` | `canonical_frozen_fields_output_shape_planning_v1.json` |
| PhaseModeLifecycleOutputShapePlanning | `governance_phase_mode_lifecycle_contract_v1.json` | `phase_mode_lifecycle_output_shape_planning_v1.json` |
| ConstraintRequiredFieldsOutputShapePlanning | `governance_constraint_required_fields_v1.json` | `constraint_required_fields_output_shape_planning_v1.json` |
| VerifierBaselineOutputShapePlanning | `governance_constraint_verifier_baseline_v1.json` | `verifier_baseline_output_shape_planning_v1.json` |
| NonClaimsAndForbiddenShortcutLibraryPlanning | `governance_constraint_non_claims_library_v1.json` + `governance_constraint_forbidden_shortcut_library_v1.json` | `non_claims_and_forbidden_shortcut_library_planning_v1.json` |
| ConstraintExtensionRulePlanning | `governance_constraint_extension_rule_v1.json` | `constraint_extension_rule_planning_v1.json` |
| LegacyAbsorptionPolicyOutputShapePlanning | `governance_legacy_absorption_policy_v1.json` | `legacy_absorption_policy_output_shape_planning_v1.json` |
| GovernanceConstraintModuleGenerationPlanningReadinessDecision | `governance_constraint_module_readiness_decision_v1.json`（未来） | `governance_constraint_module_generation_planning_readiness_decision_v1.json` |

所有 planned output 必须 `not_generated_now=true`。

## Coverage（Smoke）

- canonical contract sections: 12
- domain constraints: 12
- inheritance matrix fields: 10
- frozen field patterns: 25
- phase modes: 15
- required field groups: 12
- verifier baseline checks: 15
- non-claims / forbidden shortcut rules: 17
- extension rules: 12
- legacy absorption sections: 12

## Hard Rules

- 不得生成正式 Governance Constraint Module
- 不得生成 canonical phase template
- 不得注册 constraint module；不得 enforce 新约束
- 不得执行 verifier integration；不得修改 verifier / phase template
- 不得实施 automation；不得自动同步旧文档
- 不得修改旧 phase / 旧文档 / 旧 eval_out；不得 rerun 旧 verifier
- 不得恢复旧链路为 template source；不得标记旧链路 deprecated
- 不得执行 file operation；不得释放任何真实授权
- 不得恢复主线迁移链

## Final Decision

- `GOVERNANCE_CONSTRAINT_MODULE_GENERATION_PLANNING_READY_FOR_DRYRUN`
- **Next**: `Phase-Governance-Constraint-Module-Generation-DryRun-v1-001`

## Implementation Status

- Legacy Extraction 四段链路：GO
- **Phase-Governance-Constraint-Module-Generation-Planning-v1-001**: **GO**（468/420 checks）
- **Phase-Governance-Constraint-Module-Generation-DryRun-v1-001**: **GO**（533/420 checks）

## Downstream Handoff

- **已完成**：Governance Constraint Module Generation DryRun（533/420 checks）
- 下一阶段：**Governance Constraint Module Generation Post-DryRun Review**（仅 review；非 module generation）
- 主线仍暂停于 `Phase-Registry-Generation-Authorization-Planning-v1-001`
- 仍不得生成正式 Governance Constraint Module
