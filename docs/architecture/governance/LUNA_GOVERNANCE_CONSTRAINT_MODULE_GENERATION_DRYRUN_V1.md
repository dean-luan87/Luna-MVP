## Phase

- **Phase ID**: `Phase-Governance-Constraint-Module-Generation-DryRun-v1-001`
- **Capability**: `capabilities/governance/governance_constraint_module_generation_dryrun_v1.py`
- **Status**: governance-constraint-module-generation-dryrun-only（模拟正式模块输出结构消费；非 module generation / 非 canonical template generation / 非 verifier integration / 非主线恢复）

## Intent

对 Generation Planning 产出的 12 类正式模块输出结构规划做 dry-run，模拟 future verifier、future phase template、Cursor instruction 与后续主线 phase 是否能消费这些结构。

本阶段是「结构可消费性验证」，不是「开始生成模块」。

## Source Chain

- **上游**: `Phase-Governance-Constraint-Module-Generation-Planning-v1-001`（GO）
- **治理约束引用**: `governance_constraints_ref=migration_governance_development_constraints_v1`
- **Legacy 定位**: `legacy_as_source_evidence=true`；`legacy_as_template_source=false`

## Consumption DryRun（12 类）

| 对象 | 产物 | 模拟消费目标 |
|------|------|-------------|
| CanonicalPhaseContractConsumptionDryRun | `canonical_phase_contract_consumption_dryrun_v1.json` | future phase / verifier |
| DomainConstraintRegistryConsumptionDryRun | `domain_constraint_registry_consumption_dryrun_v1.json` | future verifier / domain constraints |
| PhaseInheritanceMatrixConsumptionDryRun | `phase_inheritance_matrix_consumption_dryrun_v1.json` | Cursor instruction / verifier |
| CanonicalFrozenFieldsConsumptionDryRun | `canonical_frozen_fields_consumption_dryrun_v1.json` | future verifier |
| PhaseModeLifecycleConsumptionDryRun | `phase_mode_lifecycle_consumption_dryrun_v1.json` | future phase template |
| ConstraintRequiredFieldsConsumptionDryRun | `constraint_required_fields_consumption_dryrun_v1.json` | future phase / verifier |
| VerifierBaselineConsumptionDryRun | `verifier_baseline_consumption_dryrun_v1.json` | future verifier |
| NonClaimsAndForbiddenShortcutLibraryConsumptionDryRun | `non_claims_and_forbidden_shortcut_library_consumption_dryrun_v1.json` | future verifier / phase |
| ConstraintExtensionRuleConsumptionDryRun | `constraint_extension_rule_consumption_dryrun_v1.json` | Cursor instruction / verifier |
| LegacyAbsorptionPolicyConsumptionDryRun | `legacy_absorption_policy_consumption_dryrun_v1.json` | future documentation / verifier |

## Hard Rules

- `simulated=true`；`future_*_consumption_simulated=true`
- domain-specific 规则不得被压平；6 个独立消费路径必须保留
- frozen fields 不得被 enforce；verifier baseline 不得被真正集成
- phase template 不得被修改；legacy absorption 不得导致旧文档重写
- 不得生成正式 Governance Constraint Module / canonical phase template
- 不得恢复主线迁移链

## Final Decision

- `GOVERNANCE_CONSTRAINT_MODULE_GENERATION_DRYRUN_READY_FOR_POST_DRYRUN_REVIEW`
- **Next**: `Phase-Governance-Constraint-Module-Generation-Post-DryRun-Review-v1-001`

## Implementation Status

- Generation Planning：GO（468/420 checks）
- **Phase-Governance-Constraint-Module-Generation-DryRun-v1-001**: **GO**（533/420 checks）
- **Phase-Governance-Constraint-Module-Generation-Post-DryRun-Review-v1-001**: **GO**（460/420 checks）

## Downstream Handoff

- **已完成**：Governance Constraint Module Generation Post-DryRun Review（460/420 checks）
- 下一阶段：**Governance Constraint Module Generation Roadmap Decision**（路线裁决；非 module generation）
- 主线仍暂停于 `Phase-Registry-Generation-Authorization-Planning-v1-001`
- 仍不得生成正式 Governance Constraint Module
