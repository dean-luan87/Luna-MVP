# Luna Evaluation — Governance Constraint Module Generation DryRun v1

**Phase**：`Phase-Governance-Constraint-Module-Generation-DryRun-v1-001`  
**输出**：`_eval_out/governance_constraint_module_generation_dryrun_v1_smoke_v0/`

## 运行

```bash
python3 tools/evaluation/governance/run_governance_constraint_module_generation_dryrun_v1.py
python3 tools/evaluation/governance/verify_governance_constraint_module_generation_dryrun_v1.py
```

## Smoke 结果

- **verifier**: GO
- **checks**: 533/420
- **boundary_ok**: true
- **simulated**: true
- **final_decision**: `GOVERNANCE_CONSTRAINT_MODULE_GENERATION_DRYRUN_READY_FOR_POST_DRYRUN_REVIEW`
- **Next**: `Phase-Governance-Constraint-Module-Generation-Post-DryRun-Review-v1-001`
- **main_migration_chain_paused**: true
- **main_migration_chain_resumed_now**: false

## 核心对象（12 类）

| 对象 | 产物 |
|------|------|
| GovernanceConstraintModuleGenerationDryRunPolicy | `governance_constraint_module_generation_dryrun_policy_v1.json` |
| CanonicalPhaseContractConsumptionDryRun | `canonical_phase_contract_consumption_dryrun_v1.json` |
| DomainConstraintRegistryConsumptionDryRun | `domain_constraint_registry_consumption_dryrun_v1.json` |
| PhaseInheritanceMatrixConsumptionDryRun | `phase_inheritance_matrix_consumption_dryrun_v1.json` |
| CanonicalFrozenFieldsConsumptionDryRun | `canonical_frozen_fields_consumption_dryrun_v1.json` |
| PhaseModeLifecycleConsumptionDryRun | `phase_mode_lifecycle_consumption_dryrun_v1.json` |
| ConstraintRequiredFieldsConsumptionDryRun | `constraint_required_fields_consumption_dryrun_v1.json` |
| VerifierBaselineConsumptionDryRun | `verifier_baseline_consumption_dryrun_v1.json` |
| NonClaimsAndForbiddenShortcutLibraryConsumptionDryRun | `non_claims_and_forbidden_shortcut_library_consumption_dryrun_v1.json` |
| ConstraintExtensionRuleConsumptionDryRun | `constraint_extension_rule_consumption_dryrun_v1.json` |
| LegacyAbsorptionPolicyConsumptionDryRun | `legacy_absorption_policy_consumption_dryrun_v1.json` |
| GovernanceConstraintModuleGenerationDryRunReadinessDecision | `governance_constraint_module_generation_dryrun_readiness_decision_v1.json` |

## 模拟消费结果

| 维度 | 规模 | dryrun pass |
|------|------|-------------|
| Canonical contract sections | 12 | ✓ |
| Domain constraints | 12 | ✓ |
| Inheritance matrix fields | 10 | ✓ |
| Frozen field patterns | 25 | ✓ |
| Phase modes | 15 | ✓ |
| Required field groups | 12 | ✓ |
| Verifier baseline checks | 15 | ✓ |
| Non-claims / forbidden shortcuts | 17 | ✓ |
| Extension rules | 12 | ✓ |
| Legacy absorption sections | 12 | ✓ |

## 边界冻结

- `governance_constraint_module_generation_dryrun_only=true`；`simulated=true`
- `future_verifier_consumption_simulated=true`；`future_phase_template_consumption_simulated=true`
- `governance_constraint_module_generated_now=false`；`canonical_phase_template_generated_now=false`
- domain differentiation preserved；6 独立消费路径 verified
- frozen fields 未 enforce；verifier baseline 未集成；phase template 未修改
