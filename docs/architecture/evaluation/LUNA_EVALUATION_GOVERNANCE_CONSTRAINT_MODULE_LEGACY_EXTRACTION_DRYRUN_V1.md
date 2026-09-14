# Luna Evaluation — Governance Constraint Module Legacy Extraction DryRun v1

**Phase**：`Phase-Governance-Constraint-Module-Legacy-Extraction-DryRun-v1-001`  
**输出**：`_eval_out/governance_constraint_module_legacy_extraction_dryrun_v1_smoke_v0/`

## 运行

```bash
python3 tools/evaluation/governance/run_governance_constraint_module_legacy_extraction_dryrun_v1.py
python3 tools/evaluation/governance/verify_governance_constraint_module_legacy_extraction_dryrun_v1.py
```

## Smoke 结果

- **verifier**: GO
- **checks**: 480/420
- **boundary_ok**: true
- **final_decision**: `GOVERNANCE_CONSTRAINT_MODULE_LEGACY_EXTRACTION_DRYRUN_READY_FOR_POST_DRYRUN_REVIEW`
- **Next**: `Phase-Governance-Constraint-Module-Legacy-Extraction-Post-DryRun-Review-v1-001`（**已完成 GO**；见 Post-DryRun Review evaluation doc）
- **main_migration_chain_paused**: true
- **main_migration_chain_resumed_now**: false

## 核心对象（10 类）

| 对象 | 产物 |
|------|------|
| LegacyExtractionDryRunPolicy | `legacy_extraction_dryrun_policy_v1.json` |
| LegacyChainInventoryConsumptionDryRun | `legacy_chain_inventory_consumption_dryrun_v1.json` |
| PhaseToConstraintMappingDryRun | `phase_to_constraint_mapping_dryrun_v1.json` |
| CanonicalFrozenFieldExtractionDryRun | `canonical_frozen_field_extraction_dryrun_v1.json` |
| PhaseModeLifecycleContractDryRun | `phase_mode_lifecycle_contract_dryrun_v1.json` |
| DomainConstraintExtractionDryRun | `domain_constraint_extraction_dryrun_v1.json` |
| ConstraintInheritancePolicyDryRun | `constraint_inheritance_policy_dryrun_v1.json` |
| LegacyAbsorptionPolicyDryRun | `legacy_absorption_policy_dryrun_v1.json` |
| ConstraintModuleOutputPlanDryRun | `constraint_module_output_plan_dryrun_v1.json` |
| LegacyExtractionDryRunReadinessDecision | `legacy_extraction_dryrun_readiness_decision_v1.json` |

## 模拟消费结果

| 维度 | 规模 | dryrun pass |
|------|------|-------------|
| Legacy chains | 12 | ✓ |
| Constraint domains | 14 | ✓ |
| Frozen field patterns | 25 | ✓ |
| Phase modes | 15 | ✓ |
| Domain constraints | 12 | ✓ |
| Planned artifacts | 12 | ✓ |

## 边界冻结

- `legacy_as_source_evidence=true`；`legacy_as_template_source=false`
- 旧链路保留为历史验证资产，不标记 deprecated，不要求 rewrite
- 正式 constraint module / canonical template 未生成；约束未 enforce
