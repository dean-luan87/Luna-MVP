## Phase

- **Phase ID**: `Phase-Permission-Semantics-Canonicalization-Planning-v1-001`
- **Capability**: `capabilities/governance/permission_semantics_canonicalization_planning_v1.py`
- **Status**: canonicalization-planning-only（规范蓝图；非 canonicalization 实施 / 非 verifier 改造 / 非 phase template 改造）

## Intent

将 Roadmap Decision 选中的 **Route A — Permission Semantics Canonicalization Planning** 展开为可落地的统一权限语义、状态语义与后续开发规范蓝图，并绑定 Route B / Route C 的核心要求。

本阶段产出的是「规范蓝图」，不是「规范生效」。所有语义表、开发规范、verifier checklist 均标注 `not_enforced_now=true` / `effective_stage=planning_defined_not_enforced`。

## Source Chain

- **上游**: `Phase-Main-Project-Structure-Migration-Governance-Debt-Register-Roadmap-Decision-v1-001`（GO）
- **选中路线**: Route A — Permission Semantics Canonicalization Planning
- **绑定依赖**: Route B — Terminology Canonical Table Planning；Route C — Success Claim Gate Canonicalization Planning
- **治理约束引用**: `governance_constraints_ref=migration_governance_development_constraints_v1`

## Core Artifacts（14 类）

| # | 对象 | 输出文件 |
|---|------|----------|
| 1 | PermissionSemanticsCanonicalizationPlanningPolicy | `permission_semantics_canonicalization_planning_policy_v1.json` |
| 2 | PhaseTypeSemanticsTable | `phase_type_semantics_table_v1.json`（14 phase types） |
| 3 | PermissionStateSemanticsTable | `permission_state_semantics_table_v1.json`（10 terms） |
| 4 | AuthorizationStateSemanticsTable | `authorization_state_semantics_table_v1.json`（12 terms） |
| 5 | ExecutionStateSemanticsTable | `execution_state_semantics_table_v1.json`（12 terms） |
| 6 | ArtifactStateSemanticsTable | `artifact_state_semantics_table_v1.json`（12 terms） |
| 7 | ReadinessStateSemanticsTable | `readiness_state_semantics_table_v1.json`（12 terms） |
| 8 | ResultStateSemanticsTable | `result_state_semantics_table_v1.json`（12 terms） |
| 9 | RouteStateSemanticsTable | `route_state_semantics_table_v1.json`（10 terms） |
| 10 | ForbiddenStateCombinationMatrix | `forbidden_state_combination_matrix_v1.json`（≥20 条） |
| 11 | DevelopmentNormsMatrix | `development_norms_matrix_v1.json`（12 norms） |
| 12 | VerifierSemanticsChecklist | `verifier_semantics_checklist_v1.json`（20 checks, `not_enforced_now=true`） |
| 13 | NonClaimsGenerationRules | `non_claims_generation_rules_v1.json`（≥20 scenarios） |
| 14 | PermissionSemanticsCanonicalizationPlanningReadinessDecision | `permission_semantics_canonicalization_planning_readiness_decision_v1.json` |

## Semantic Groups（6 组）

1. **Phase Type** — planning / dry-run / review / roadmap / register / authorization / execution 分层
2. **Permission** — allowed / blocked / deferred / released 等不得 imply 执行
3. **Authorization** — planned ≠ requested ≠ granted；owner ≠ operator
4. **Execution** — allowed ≠ committed；runtime / subprocess / file op 独立追踪
5. **Artifact** — candidate ≠ executable；verifier_report ≠ runtime evidence
6. **Readiness / Result / Route** — ready_for_* 与 GO / selected_route 不得 imply 权限释放

## Final Decision

- `PERMISSION_SEMANTICS_CANONICALIZATION_PLANNING_READY_FOR_DRYRUN`
- **Next**: `Phase-Permission-Semantics-Canonicalization-DryRun-v1-001`

## Non-Claims

- Planning GO ≠ canonicalization executed（`canonicalization_executed_now=false`）
- 规范蓝图生成 ≠ verifier 已改造 / phase template 已改造 / automation 已实施
- Route B/C 绑定 ≠ terminology 或 success claim 债务已修复
- `not_enforced_now=true` 必须保留至 DryRun / Review / Execution 链逐步消费
- Planning GO ≠ owner/operator approval / real rehearsal / migration / batch arming

## Boundary Flags（全部冻结）

```
canonicalization_planning_only=true
canonicalization_executed_now=false
debt_fix_executed_now=false
verifier_modified_now=false
phase_template_modified_now=false
automation_implemented_now=false
documentation_auto_sync_executed_now=false
authorization_granted_now=false
runtime_invoked=false
execution_committed=false
write_allowed=false
real_rehearsal_execution_allowed=false
real_migration_execution_allowed=false
batch_arming_allowed=false
fact_status=not_fact
```

## Implementation Status

- **Phase-Main-Project-Structure-Migration-Governance-Debt-Register-Roadmap-Decision-v1-001**: **GO**（432/420 checks）
- **Phase-Permission-Semantics-Canonicalization-Planning-v1-001**: **GO**（420/420 checks）
- **Phase-Permission-Semantics-Canonicalization-DryRun-v1-001**: **GO**（420/420 checks）

## Downstream Handoff

- **已完成**：Permission Semantics Canonicalization DryRun（12 类 simulated consumption；`canonicalization_enforced_now=false`）
- 下一阶段：**Permission Semantics Canonicalization Post-DryRun Review**（审查 dry-run 完整性、规范误生效、边界冻结）
- 仍不得 enforce 语义规范、修改 verifier/phase template、或释放真实授权链
