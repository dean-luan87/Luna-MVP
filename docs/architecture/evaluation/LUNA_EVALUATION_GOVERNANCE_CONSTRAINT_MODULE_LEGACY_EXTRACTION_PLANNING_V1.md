# Luna Evaluation — Governance Constraint Module Legacy Extraction Planning v1

**Phase**：`Phase-Governance-Constraint-Module-Legacy-Extraction-Planning-v1-001`  
**输出**：`_eval_out/governance_constraint_module_legacy_extraction_planning_v1_smoke_v0/`

## 运行

```bash
python3 tools/evaluation/governance/run_governance_constraint_module_legacy_extraction_planning_v1.py
python3 tools/evaluation/governance/verify_governance_constraint_module_legacy_extraction_planning_v1.py
```

## Smoke 结果

- **verifier**: GO
- **checks**: 487/420
- **boundary_ok**: true
- **final_decision**: `GOVERNANCE_CONSTRAINT_MODULE_LEGACY_EXTRACTION_PLANNING_READY_FOR_DRYRUN`
- **Next**: `Phase-Governance-Constraint-Module-Legacy-Extraction-DryRun-v1-001`（**已完成 GO**；见 DryRun evaluation doc）
- **main_migration_chain_paused**: true
- **main_migration_resume_phase**: `Phase-Registry-Generation-Authorization-Planning-v1-001`

## 核心对象（10 类）

| 对象 | 产物 |
|------|------|
| LegacyGovernanceExtractionPlanningPolicy | `legacy_extraction_planning_policy_v1.json` |
| LegacyGovernanceChainInventory | `legacy_governance_chain_inventory_v1.json` |
| LegacyPhaseToConstraintSourceMatrix | `legacy_phase_to_constraint_source_matrix_v1.json` |
| CanonicalFrozenFieldExtractionPlan | `canonical_frozen_field_extraction_plan_v1.json` |
| PhaseModeLifecycleContractExtractionPlan | `phase_mode_lifecycle_contract_extraction_plan_v1.json` |
| DomainConstraintExtractionPlan | `domain_constraint_extraction_plan_v1.json` |
| GovernanceConstraintInheritancePolicyPlan | `governance_constraint_inheritance_policy_plan_v1.json` |
| LegacyAbsorptionPolicyPlan | `legacy_absorption_policy_plan_v1.json` |
| GovernanceConstraintModuleOutputPlan | `governance_constraint_module_output_plan_v1.json` |
| LegacyExtractionPlanningReadinessDecision | `legacy_extraction_planning_readiness_decision_v1.json` |

## 覆盖规模

- Legacy chains: **12**（≥10 要求）
- Constraint domains: **14**
- Frozen field patterns: **25**（≥20 要求）
- Phase modes: **15**（≥12 要求）
- Domain constraints: **12**
- Planned module artifacts: **12**（全部 `not_generated_now=true`）

## 边界冻结

- 不修改旧 phase / 旧文档 / 旧 eval_out
- 不 rerun 旧 verifier
- 不生成正式 Governance Constraint Module
- 不生成 canonical phase template
- `legacy_as_template_source=false`；旧链仅作 constraint source evidence
