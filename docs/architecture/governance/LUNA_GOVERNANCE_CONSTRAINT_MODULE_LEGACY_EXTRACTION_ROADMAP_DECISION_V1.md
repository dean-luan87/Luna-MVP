## Phase

- **Phase ID**: `Phase-Governance-Constraint-Module-Legacy-Extraction-Roadmap-Decision-v1-001`
- **Capability**: `capabilities/governance/governance_constraint_module_legacy_extraction_roadmap_decision_v1.py`
- **Status**: roadmap-decision-only（路线裁决；非 module generation / 非 verifier integration / 非主线恢复）

## Intent

对已完成的 Legacy Extraction 三段链路（Planning → DryRun → Post-DryRun Review）做路线裁决，选定 **Route A — Governance Constraint Module Generation Planning**。

Legacy Extraction 只证明「可映射」，尚未定义正式模块的生成规则、source whitelist、contract shape、domain registry shape、baseline verifier usage 与输出边界。

## Route Decision

| Route | 状态 | 说明 |
|-------|------|------|
| **A — Module Generation Planning** | **selected** | P0；仅 module generation **planning** allowed |
| B — Module Generation | deferred | planning 未完成 |
| C — Canonical Phase Template Planning | deferred | 需 module planning 先定义结构 |
| D — Verifier Integration Planning | deferred | module 未生成 |
| E — Phase Template Integration Planning | deferred | module 结构未定义 |
| F — Legacy Absorption Note Planning | deferred | 不得重写旧文档 |
| G — Main Migration Chain Resume Planning | deferred | 约束模块未规划 |
| H — Direct Module Generation / Verifier Integration / Mainline Resume | **blocked** | 禁止 |

## Final Decision

- `GOVERNANCE_CONSTRAINT_MODULE_LEGACY_EXTRACTION_ROADMAP_DECISION_READY_FOR_MODULE_GENERATION_PLANNING`
- **Next**: `Phase-Governance-Constraint-Module-Generation-Planning-v1-001`

## Implementation Status

- Legacy Extraction 三段链路：GO
- **Phase-Governance-Constraint-Module-Legacy-Extraction-Roadmap-Decision-v1-001**: **GO**（471/420 checks）
- **Phase-Governance-Constraint-Module-Generation-Planning-v1-001**: **GO**（468/420 checks）

## Downstream Handoff

- **已完成**：Governance Constraint Module Generation Planning（468/420 checks）
- 下一阶段：**Governance Constraint Module Generation DryRun**（仅 dry-run；非 module generation）
- 主线仍暂停于 `Phase-Registry-Generation-Authorization-Planning-v1-001`
- 仍不得生成正式 Governance Constraint Module
