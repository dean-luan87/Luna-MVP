# Luna Evaluation — Boundary Object Registry Generation Planning v1

**Phase**：`Phase-Boundary-Object-Registry-Generation-Planning-v1-001`  
**输出**：`_eval_out/boundary_object_registry_generation_planning_v1_smoke_v0/`

## 运行

```bash
python3 tools/evaluation/governance/run_boundary_object_registry_generation_planning_v1.py
python3 tools/evaluation/governance/verify_boundary_object_registry_generation_planning_v1.py
```

## Smoke 结果

- **verifier**: GO
- **checks**: 459/420
- **boundary_ok**: true
- **final_decision**: `BOUNDARY_OBJECT_REGISTRY_GENERATION_PLANNING_READY_FOR_DRYRUN`
- **Next**: `Phase-Boundary-Object-Registry-Generation-DryRun-v1-001`（**GO**；494/420 checks → Post-DryRun Review）

## 核心对象（13 类）

| 对象 | 产物 |
|------|------|
| BoundaryObjectRegistryGenerationPlanningPolicy | `boundary_object_registry_generation_planning_policy_v1.json` |
| RegistryGenerationSourceInventoryPlanningMatrix | `registry_generation_source_inventory_planning_matrix_v1.json` |
| RegistrySourceArtifactWhitelistPlanningMatrix | `registry_source_artifact_whitelist_planning_matrix_v1.json` |
| RegistrySourceIntegrityCheckPlanningMatrix | `registry_source_integrity_check_planning_matrix_v1.json` |
| RegistryContaminationPreventionPlanningMatrix | `registry_contamination_prevention_planning_matrix_v1.json` |
| RegistryEntryConversionRulePlanningMatrix | `registry_entry_conversion_rule_planning_matrix_v1.json` |
| RegistryProtectedObjectEntryRulePlanningMatrix | `registry_protected_object_entry_rule_planning_matrix_v1.json` |
| RegistryPolicyEntryRulePlanningMatrix | `registry_policy_entry_rule_planning_matrix_v1.json` |
| RegistryOwnerOperatorDependencyPlanningMatrix | `registry_owner_operator_dependency_planning_matrix_v1.json` |
| RegistryGenerationVerifierUsagePlanningMatrix | `registry_generation_verifier_usage_planning_matrix_v1.json` |
| RegistryGenerationNonClaimsPlanningMatrix | `registry_generation_non_claims_planning_matrix_v1.json` |
| RegistryGenerationOutputPlan | `registry_generation_output_plan_v1.json` |
| BoundaryObjectRegistryGenerationPlanningReadinessDecision | `boundary_object_registry_generation_planning_readiness_decision_v1.json` |

## 边界冻结

- `boundary_object_registry_generation_planning_only=true`
- `boundary_object_registry_generated_now=false`
- `registry_entry_generated_now=false` / `registry_entry_committed_now=false`
- `registry_source_final_validated_now=false` / `registry_contamination_check_final_executed_now=false`
- protected assets / HR / DnAE 未修改；file operation 未执行；evidence 未授权
