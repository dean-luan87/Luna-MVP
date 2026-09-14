# PHASE_BRIEF

## Phase ID

`Phase-Main-Project-Structure-Migration-Readiness-and-Test-Plan-v1-001`

## 目标（只做这些）

- 主工程结构迁移**就绪门**与**迁移后测试验证计划**（planning-only）
- 不执行真实 file move/delete/merge
- 不进入白盒/测试中心结构优化（已 roadmap deferred）

## 输入 roots（必须存在）

| intake_id | 路径 | 必读文件 |
|-----------|------|----------|
| post_pahr_roadmap | `_eval_out/post_protected_asset_and_human_review_resolution_roadmap_decision_v1_smoke_v0/` | `summary.json` |
| pahr_closure | `_eval_out/protected_asset_and_human_review_resolution_closure_v1_smoke_v0/` | `summary.json` |
| consolidation_closure | `_eval_out/luna_project_structure_consolidation_closure_v1_smoke_v0/` | `summary.json` |
| structure_map | `_eval_out/luna_project_module_inventory_and_structure_map_dryrun_v1_smoke_v0/` | `current_to_target_structure_map.json` |

## 输出（必须生成）

- capability: `capabilities/governance/main_project_structure_migration_readiness_and_test_plan_v1.py`（待实现）
- runner / verifier + `_eval_out/main_project_structure_migration_readiness_and_test_plan_v1_smoke_v0/`

## 边界（禁止）

- [x] 不执行真实迁移
- [x] 不 human review 执行 / 不解除 permanent block
- [x] 白盒/测试中心结构优化本 phase 不做
- [x] 不后台整体 Developer Backend 定稿

## 验收标准

| 项 | 要求 |
|----|------|
| verifier | GO |
| final_decision | `MAIN_PROJECT_STRUCTURE_MIGRATION_READINESS_AND_TEST_PLAN_READY_FOR_GUARDED_MIGRATION_PLANNING`（或等价） |
| recommended_next_phase | `Phase-Main-Project-Structure-Migration-Guarded-Planning-v1-001` |
| 冻结 | 240 HR / 914 permanent block carryover；post-migration test plan 已定义 |

## 文档更新

- [ ] governance 文档 + evaluation 三件套 + phase verdict 表

## Non-Claims

- readiness GO ≠ 可以真实搬迁
- test plan 定义 ≠ 测试已执行通过
