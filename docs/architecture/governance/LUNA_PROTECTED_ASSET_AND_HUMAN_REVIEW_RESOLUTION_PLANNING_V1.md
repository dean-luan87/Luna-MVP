## Phase

- **Phase ID**: `Phase-Protected-Asset-and-Human-Review-Resolution-Planning-v1-001`
- **Capability**: `capabilities/governance/protected_asset_and_human_review_resolution_planning_v1.py`
- **Status**: planning-only（不执行 human review / 不处理 protected assets / 不移动文件）

## Intent

定义 protected asset、human review、permanent do-not-auto-execute 的治理规则框架。为后续任何真实结构调整建立前置规则：哪些资产永远不能自动处理，哪些必须人工复核，如何分类、分配 owner、记录决策、回滚。

## Inputs

- `luna_project_structure_consolidation_roadmap_decision_v1_smoke_v0`（required）
- `luna_project_structure_consolidation_closure_v1_smoke_v0`（required，含 carryover registers）
- 上游 consolidation post-review / dryrun / planning / structure map / governance / gate taxonomy

## Core Policies Defined

| 对象 | 产物 |
|------|------|
| ProtectedAssetPolicy | 14 类 protected asset 类型 |
| HumanReviewResolutionPolicy | 10 类 human review 分类框架（240 条） |
| PermanentDoNotAutoExecutePolicy | 12+ permanent block 规则（914 条） |
| ManualOwnerAssignmentPolicy | 10 类 owner 类型 |
| ReviewDecisionSchema | 12 allowed / 10 forbidden 决策 |
| ReviewResolutionStateMachine | 9 allowed / 5 forbidden 状态 |
| AuditTracePolicy / RollbackPolicy | 审计与回滚框架 |

## Key Constraints

- `planning_only=true`
- `human_review_execution_allowed=false`
- `protected_asset_modification_allowed=false`
- `permanent_block_override_allowed=false`
- `real_migration_allowed=false`
- 禁止决策：DELETE_NOW / MOVE_NOW / MERGE_NOW / ARCHIVE_NOW / ENABLE_RUNTIME 等

## Outputs

`_eval_out/protected_asset_and_human_review_resolution_planning_v1_smoke_v0/`

## Final Decision

- `PROTECTED_ASSET_AND_HUMAN_REVIEW_RESOLUTION_PLANNING_READY_FOR_DRYRUN`
- **Next**: `Phase-Protected-Asset-and-Human-Review-Resolution-DryRun-v1-001`

## Non-Claims

- planning ≠ human review 已执行
- planning ≠ protected assets 已处理
- planning ≠ permanent block 已解除
- planning ≠ 真实迁移可执行

## Implementation Status

- **Phase-Protected-Asset-and-Human-Review-Resolution-DryRun-v1-001**: **GO**
- **Phase-Protected-Asset-and-Human-Review-Resolution-Post-DryRun-Review-v1-001**: **GO**
- **Phase-Protected-Asset-and-Human-Review-Resolution-Closure-v1-001**: **GO**
- 见 `LUNA_PROTECTED_ASSET_AND_HUMAN_REVIEW_RESOLUTION_CLOSURE_V1.md`
- **Recommended next**: `Phase-Post-Protected-Asset-and-Human-Review-Resolution-Roadmap-Decision-v1-001`
