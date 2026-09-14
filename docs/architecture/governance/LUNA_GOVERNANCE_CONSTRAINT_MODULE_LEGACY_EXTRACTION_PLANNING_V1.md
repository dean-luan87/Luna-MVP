## Phase

- **Phase ID**: `Phase-Governance-Constraint-Module-Legacy-Extraction-Planning-v1-001`
- **Capability**: `capabilities/governance/governance_constraint_module_legacy_extraction_planning_v1.py`
- **Status**: legacy-extraction-planning-only（提取规划；非约束模块生成 / 非旧 phase 修改 / 非旧文档重写）

## Intent

暂停迁移主线扩展，把此前迁移治理链中反复出现的共性规则、冻结字段、NO-GO、non-claims、forbidden shortcuts、readiness decision 与 verifier baseline 抽象为后续 Governance Constraint Module 的来源资产。

本阶段只做 legacy extraction **planning**，不修改旧 phase、不重写旧文档、不生成正式约束模块。

## 主线暂停说明

- **已暂停主线**：Boundary Object Registry Generation → Registry Generation Authorization Planning
- **暂停原因**：避免继续复制长 phase 模板；先把旧治理链收束为可继承约束模块来源
- **恢复点**：`Phase-Registry-Generation-Authorization-Planning-v1-001`（约束模块收束链完成后恢复）

## 核心原则（从旧链抽取）

- Planning ≠ 执行
- DryRun ≠ 成功
- Post-Review GO ≠ 权限释放
- Roadmap selected route ≠ 真实授权
- verifier=GO ≠ success claim
- summary / verifier_report ≠ evidence
- owner/operator planning ≠ approval granted
- registry planning / dry-run / review ≠ registry generated
- file operation 默认阻断；protected / HR / DnAE 默认冻结

## Core Artifacts（10 类）

policy、legacy chain inventory、phase-to-constraint matrix、canonical frozen field plan、phase mode lifecycle plan、domain constraint plan、inheritance policy plan、legacy absorption policy plan、module output plan、readiness decision。

## Key Freeze Fields

- `legacy_extraction_planning_only=true`
- `legacy_phase_modified_now=false`
- `legacy_document_rewritten_now=false`
- `governance_constraint_module_generated_now=false`
- `canonical_phase_template_generated_now=false`
- `main_migration_chain_paused=true`

## Final Decision

- `GOVERNANCE_CONSTRAINT_MODULE_LEGACY_EXTRACTION_PLANNING_READY_FOR_DRYRUN`
- **Next**: `Phase-Governance-Constraint-Module-Legacy-Extraction-DryRun-v1-001`

## Implementation Status

- **Phase-Governance-Constraint-Module-Legacy-Extraction-Planning-v1-001**: GO
- **Phase-Governance-Constraint-Module-Legacy-Extraction-DryRun-v1-001**: **GO**（480/420 checks）

## Downstream Handoff

- **已完成**：Legacy Extraction DryRun（480/420 checks）
- 下一阶段：**Legacy Extraction Post-DryRun Review**（审查 dry-run 完整性；非 module generation）
- 主线仍暂停于 `Phase-Registry-Generation-Authorization-Planning-v1-001`
- 仍不得生成正式 Governance Constraint Module、不得修改旧 phase / 旧文档 / 旧 eval_out
