## Phase

- **Phase ID**: `Phase-Governance-Constraint-Module-Legacy-Extraction-DryRun-v1-001`
- **Capability**: `capabilities/governance/governance_constraint_module_legacy_extraction_dryrun_v1.py`
- **Status**: legacy-extraction-dryrun-only（模拟映射消费；非约束模块生成 / 非旧 phase 修改）

## Intent

对 Legacy Extraction Planning 产出的提取规划做 dry-run，模拟旧治理链如何被映射为 canonical contract、domain constraints、inheritance policy、legacy absorption policy、future verifier baseline 与 future phase template reference。

核心验证：旧链路作为 **source evidence** 可用，但不能被继续当作新 phase **复制模板**来源。

## Source Chain

- **上游**: `Phase-Governance-Constraint-Module-Legacy-Extraction-Planning-v1-001`（GO）
- **治理约束引用**: `governance_constraints_ref=migration_governance_development_constraints_v1`

## Core Artifacts（10 类）

policy、legacy chain inventory consumption dryrun、phase-to-constraint mapping dryrun、canonical frozen field extraction dryrun、phase mode lifecycle contract dryrun、domain constraint extraction dryrun、inheritance policy dryrun、legacy absorption policy dryrun、output plan dryrun、readiness decision。

## Key Freeze Fields

- `legacy_extraction_dryrun_only=true` / `simulated=true`
- `governance_constraint_module_generated_now=false`
- `canonical_phase_template_generated_now=false`
- `constraint_module_registered_now=false`
- `main_migration_chain_resumed_now=false`

## Final Decision

- `GOVERNANCE_CONSTRAINT_MODULE_LEGACY_EXTRACTION_DRYRUN_READY_FOR_POST_DRYRUN_REVIEW`
- **Next**: `Phase-Governance-Constraint-Module-Legacy-Extraction-Post-DryRun-Review-v1-001`

## Implementation Status

- **Phase-Governance-Constraint-Module-Legacy-Extraction-Planning-v1-001**: GO
- **Phase-Governance-Constraint-Module-Legacy-Extraction-DryRun-v1-001**: GO
- **Phase-Governance-Constraint-Module-Legacy-Extraction-Post-DryRun-Review-v1-001**: **GO**（421/420 checks）

## Downstream Handoff

- **已完成**：Legacy Extraction Post-DryRun Review（421/420 checks）
- 下一阶段：**Legacy Extraction Roadmap Decision**（裁决后续收束路线；非 module generation）
- 主线仍暂停于 `Phase-Registry-Generation-Authorization-Planning-v1-001`
- 仍不得生成正式 Governance Constraint Module
