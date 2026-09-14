## Phase

- **Phase ID**: `Phase-Terminology-Canonical-Table-Planning-v1-001`
- **Capability**: `capabilities/governance/terminology_canonical_table_planning_v1.py`
- **Status**: terminology-planning-only（术语表规划蓝图；非正式表生成 / 非 enforced）

## Intent

将 Roadmap Decision 选中的 **Route B — Terminology Canonical Table Planning** 展开为可落地的术语规范规划，并保留 **Route C — Success Claim Gate Canonicalization Planning** 作为后续 P0 dependency。

本阶段产出的是「术语表规划」，不是术语表本体。`TerminologyCanonicalEntryPlan` 不得被误读为正式 `terminology_canonical_table_v1.json`。

## Source Chain

- **上游**: `Phase-Permission-Semantics-Canonicalization-Roadmap-Decision-v1-001`（GO，Route B 选中）
- **治理约束引用**: `governance_constraints_ref=migration_governance_development_constraints_v1`

## Core Artifacts（10 类）

| # | 对象 | 输出文件 |
|---|------|----------|
| 1 | TerminologyCanonicalTablePlanningPolicy | `terminology_canonical_table_planning_policy_v1.json` |
| 2 | TerminologyScopeIntakeMatrix | `terminology_scope_intake_matrix_v1.json`（24 术语） |
| 3 | TerminologyCanonicalEntryPlan | `terminology_canonical_entry_plan_v1.json`（24 术语） |
| 4 | TerminologyHighRiskMisreadMatrix | `terminology_high_risk_misread_matrix_v1.json` |
| 5 | TerminologyRequiredFieldsPlanningMatrix | `terminology_required_fields_planning_matrix_v1.json` |
| 6 | TerminologyVerifierUsagePlanningMatrix | `terminology_verifier_usage_planning_matrix_v1.json` |
| 7 | TerminologyForbiddenInterpretationPlanningMatrix | `terminology_forbidden_interpretation_planning_matrix_v1.json` |
| 8 | TerminologySuccessClaimDependencyMatrix | `terminology_success_claim_dependency_matrix_v1.json`（≥12 topics） |
| 9 | TerminologyTableOutputPlan | `terminology_table_output_plan_v1.json`（8 planned artifacts） |
| 10 | TerminologyCanonicalTablePlanningReadinessDecision | `terminology_canonical_table_planning_readiness_decision_v1.json` |

## 24 高风险术语

planning, dry-run, review, post-review, roadmap decision, register, authorization, authorization planning, authorization request, authorization granted, owner approval, operator acknowledgement, execution window, allowed, granted, committed, generated, executed, enforced, GO, ready, evidence, success, success claim

## Final Decision

- `TERMINOLOGY_CANONICAL_TABLE_PLANNING_READY_FOR_DRYRUN`
- **Next**: `Phase-Terminology-Canonical-Table-DryRun-v1-001`

## Non-Claims

- Planning GO ≠ terminology table generated / canonicalized / enforced
- Route C dependency 保留 ≠ success claim gate 已修复
- 正式 canonical table 所有 `not_generated_now=true`

## Boundary Flags

```
terminology_planning_only=true
terminology_canonicalization_executed_now=false
terminology_enforced_now=false
canonical_table_generated_now=false
registry_written_now=false
```

## Implementation Status

- **Phase-Permission-Semantics-Canonicalization-Roadmap-Decision-v1-001**: **GO**（420/420 checks）
- **Phase-Terminology-Canonical-Table-Planning-v1-001**: **GO**（420/420 checks）
- **Phase-Terminology-Canonical-Table-DryRun-v1-001**: **GO**（439/420 checks）
- **Phase-Terminology-Canonical-Table-Post-DryRun-Review-v1-001**: **GO**（449/420 checks）

## Downstream Handoff

- **已完成**：Terminology Canonical Table DryRun；Post-DryRun Review
- 下一阶段：**Terminology Canonical Table Roadmap Decision**
- 仍不得执行 terminology canonicalization 或生成正式术语表
