## Phase

- **Phase ID**: `Phase-Post-Protected-Asset-and-Human-Review-Resolution-Roadmap-Decision-v1-001`
- **Capability**: `capabilities/governance/post_protected_asset_and_human_review_resolution_roadmap_decision_v1.py`
- **Status**: roadmap-decision-only

## Intent

在 Protected Asset / Human Review Resolution Closure 后做路线裁决。**默认选中主工程结构迁移就绪与测试计划**，而非白盒/测试中心结构优化。

## Recommended Phase Sequence

1. `Phase-Main-Project-Structure-Migration-Readiness-and-Test-Plan-v1-001`（**当前选中**）
2. `Phase-Main-Project-Structure-Migration-Guarded-Planning-v1-001`（就绪 GO 后）
3. 受控迁移链 + **主工程迁移后测试验证**
4. 再讨论 `Phase-Whitebox-and-Test-Center-Structure-Optimization-Planning-v1-001`

## Selected Route

- **Route A**: Main Project Structure Migration Readiness and Test Plan
- **final_decision**: `POST_PROTECTED_ASSET_AND_HUMAN_REVIEW_RESOLUTION_ROADMAP_DECISION_READY_FOR_MAIN_PROJECT_STRUCTURE_MIGRATION_READINESS_AND_TEST_PLAN`
- **next**: `Phase-Main-Project-Structure-Migration-Readiness-and-Test-Plan-v1-001`

## Whitebox / Test Center Policy (Frozen)

| 字段 | 值 |
|------|-----|
| `whitebox_test_center_structure_optimization_deferred` | true |
| `reason` | `requires_post_migration_test_and_design_discussion` |
| `test_after_main_project_migration_required` | true |
| `whitebox_test_center_must_align_with_main_project_structure` | true |

白盒 = 主工程**观测系统**；测试中心 = 主工程**验证系统**。不能脱离主工程单独设计，否则主工程重组后白盒/测试中心仍对应旧路径，verifier / GO-NO-GO / logs 无法映射新模块。

## Deferred Routes

| Route | 状态 |
|-------|------|
| L Whitebox and Test Center Structure Optimization | **deferred**（迁移后测试 + 对齐讨论） |
| K Main Project Migration Guarded Planning | 就绪 GO 后进入 |
| B Developer Backend Extraction | deferred（后台整体未定稿） |
| D Human Review Execution | blocked |
| E Protected Asset Manual Override | blocked |
| F Real Structure Migration | blocked（由 Route K 承接） |

## Outputs

`_eval_out/post_protected_asset_and_human_review_resolution_roadmap_decision_v1_smoke_v0/`

## Non-Claims

- 不等于真实迁移可执行
- 不等于白盒/测试中心结构优化可立即开始
- 不等于后台整体架构已定稿

## Implementation Status

- **Phase-Main-Project-Structure-Migration-Readiness-and-Test-Plan-v1-001**: **GO**（见 `LUNA_MAIN_PROJECT_STRUCTURE_MIGRATION_READINESS_AND_TEST_PLAN_V1.md`）
- **Phase-Main-Project-Structure-Migration-Guarded-Planning-v1-001**: **GO**（见 `LUNA_MAIN_PROJECT_STRUCTURE_MIGRATION_GUARDED_PLANNING_V1.md`）
- **Phase-Main-Project-Structure-Migration-Guarded-DryRun-v1-001**: pending
