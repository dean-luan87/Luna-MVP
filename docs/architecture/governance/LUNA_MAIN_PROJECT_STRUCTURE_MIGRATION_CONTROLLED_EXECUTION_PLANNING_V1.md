## Phase

- **Phase ID**: `Phase-Main-Project-Structure-Migration-Controlled-Execution-Planning-v1-001`
- **Capability**: `capabilities/governance/main_project_structure_migration_controlled_execution_planning_v1.py`
- **Status**: planning-only（定义真实搬迁作战计划，不执行）

## Intent

在 Roadmap 选中 **Controlled Migration Execution Planning** 后，把「真实搬迁怎么打」写清楚：

- **哪一批先动**：B0–B7 顺序与窗口（一次只动一批）
- **谁授权**：7 类 owner gate（禁止 auto-confirm）
- **什么时候停**：16 abort + 11 failure response；批失败阻断后续批
- **测试怎么跑**：31 项 post-batch 测试映射到批次，通过才进下一批
- **失败怎么回滚**：rollback rehearsal 前置（B1–B6）；每批 evidence pack 模板

## B0–B7 作战批次（规划候选，未执行）

| Batch | 要点 |
|-------|------|
| B0 | 基线快照 / 不移动 |
| B1 | 受控 docs relink（非 protected README/verdict） |
| B2 | 能力模块分组（低风险非 protected） |
| B3 | 治理/宪法分组（需 governance owner） |
| B4 | 中台 operating core（无 runtime 变更） |
| B5 | 开发者制品 reference separation（非白盒定稿） |
| B6 | 未来模块 marker only |
| B7 | 全量验证与 rollback gate（不移动） |

## Final Decision

- `MAIN_PROJECT_STRUCTURE_MIGRATION_CONTROLLED_EXECUTION_PLANNING_READY_FOR_DRYRUN`
- **Next**: `Phase-Main-Project-Structure-Migration-Controlled-Execution-DryRun-v1-001`

## Non-Claims

- planning GO ≠ 真实迁移 / batch armed / 测试或 verifier 已执行 / rollback rehearsal 已执行 / owner 已确认

## Implementation Status

- **Phase-Main-Project-Structure-Migration-Execution-Control-and-Test-Harness-Roadmap-Decision-v1-001**: **GO**（248 checks）
- **Phase-Main-Project-Structure-Migration-Controlled-Execution-Planning-v1-001**: **GO**（337 checks）
- **Phase-Main-Project-Structure-Migration-Controlled-Execution-DryRun-v1-001**: **GO**（见 `LUNA_MAIN_PROJECT_STRUCTURE_MIGRATION_CONTROLLED_EXECUTION_DRYRUN_V1.md`）
- **Phase-Main-Project-Structure-Migration-Controlled-Execution-Post-DryRun-Review-v1-001**: **GO**（331 checks）
- **Phase-Main-Project-Structure-Migration-Controlled-Execution-Closure-v1-001**: **GO**（285 checks）
