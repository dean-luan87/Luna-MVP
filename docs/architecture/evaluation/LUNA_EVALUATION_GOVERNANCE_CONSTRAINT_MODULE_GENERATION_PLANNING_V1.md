# Luna Evaluation — Governance Constraint Module Generation Planning v1

**Phase**：`Phase-Governance-Constraint-Module-Generation-Planning-v1-001`  
**输出**：`_eval_out/governance_constraint_module_generation_planning_v1_smoke_v0/`

## 运行

```bash
python3 tools/evaluation/governance/run_governance_constraint_module_generation_planning_v1.py
python3 tools/evaluation/governance/verify_governance_constraint_module_generation_planning_v1.py
```

## Smoke 结果

- **verifier**: GO
- **checks**: 468/420
- **boundary_ok**: true
- **source_selected_route_observed**: Route A — Governance Constraint Module Generation Planning
- **all_output_shapes_planned**: true
- **all_not_generated_now**: true
- **final_decision**: `GOVERNANCE_CONSTRAINT_MODULE_GENERATION_PLANNING_READY_FOR_DRYRUN`
- **Next**: `Phase-Governance-Constraint-Module-Generation-DryRun-v1-001`

## 核心对象（12 类）

| 对象 | 产物 |
|------|------|
| GovernanceConstraintModuleGenerationPlanningPolicy | `governance_constraint_module_generation_planning_policy_v1.json` |
| CanonicalPhaseContractOutputShapePlanning | `canonical_phase_contract_output_shape_planning_v1.json` |
| DomainConstraintRegistryOutputShapePlanning | `domain_constraint_registry_output_shape_planning_v1.json` |
| PhaseInheritanceMatrixOutputShapePlanning | `phase_inheritance_matrix_output_shape_planning_v1.json` |
| CanonicalFrozenFieldsOutputShapePlanning | `canonical_frozen_fields_output_shape_planning_v1.json` |
| PhaseModeLifecycleOutputShapePlanning | `phase_mode_lifecycle_output_shape_planning_v1.json` |
| ConstraintRequiredFieldsOutputShapePlanning | `constraint_required_fields_output_shape_planning_v1.json` |
| VerifierBaselineOutputShapePlanning | `verifier_baseline_output_shape_planning_v1.json` |
| NonClaimsAndForbiddenShortcutLibraryPlanning | `non_claims_and_forbidden_shortcut_library_planning_v1.json` |
| ConstraintExtensionRulePlanning | `constraint_extension_rule_planning_v1.json` |
| LegacyAbsorptionPolicyOutputShapePlanning | `legacy_absorption_policy_output_shape_planning_v1.json` |
| GovernanceConstraintModuleGenerationPlanningReadinessDecision | `governance_constraint_module_generation_planning_readiness_decision_v1.json` |

## 边界冻结

- `governance_constraint_module_generation_planning_only=true`
- `governance_constraint_module_generated_now=false`
- `canonical_phase_template_generated_now=false`
- `legacy_as_source_evidence=true`；`legacy_as_template_source=false`
- `main_migration_chain_resumed_now=false`
- `ready_for_governance_constraint_module_generation_dryrun=true`
- `ready_for_governance_constraint_module_generation=false`
