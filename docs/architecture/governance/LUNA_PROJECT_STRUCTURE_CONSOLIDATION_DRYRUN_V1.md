## Phase

- **Phase ID**: `Phase-Luna-Project-Structure-Consolidation-DryRun-v1-001`
- **Status**: dry-run-only（不执行真实 consolidation / 不移动文件）

## Intent

在 merge≈1654、archive≈937 的大规模规划下，本阶段不仅模拟 B0–B6 批次执行顺序，还必须完成：

1. **冲突检测**（多 action 同资产、protected 资产误归档、client/backend 混叠等）
2. **误归类检测**（cognition placeholder 被当 runtime、developer backend 泄漏到 client）
3. **依赖断裂模拟**（runner/verifier/doc/eval_out/README 同步风险）
4. **边界完整性审查**（client / developer backend / midplatform / cognition）
5. **人工复核清单**（`human_review_required_register.json`）
6. **禁止自动执行清单**（`do_not_auto_execute_register.json`）
7. **回滚模拟计划**（`rollback_simulation_plan.json`）

## Outputs

`_eval_out/luna_project_structure_consolidation_dryrun_v1_smoke_v0/`

核心产物：`consolidation_dryrun_execution_plan.json`、`batch_dryrun_results.json`、`consolidation_conflict_report.json`、`human_review_required_register.json`、`do_not_auto_execute_register.json`、`rollback_simulation_plan.json`、`consolidation_dryrun_readiness_decision.json`

## Final Decision

- `LUNA_PROJECT_STRUCTURE_CONSOLIDATION_DRYRUN_READY_FOR_POST_DRYRUN_REVIEW`
- **Next**: `Phase-Protected-Asset-and-Human-Review-Resolution-Planning-v1-001`（Roadmap Decision 已完成 GO）

## Closure Status

- **Phase-Luna-Project-Structure-Consolidation-Closure-v1-001**: **GO**
- 见 `LUNA_PROJECT_STRUCTURE_CONSOLIDATION_CLOSURE_V1.md`

## Review Focus (Post-DryRun)

Post-DryRun Review 已完成三类结论分类：

- **acceptable (1382)**：`missing_target_module` TBD 资产 + `_eval_out` 双登记；dry-run 已拦截
- **plan_revision (0)**：无 core path 级必须回修项
- **permanent (914)**：protected 资产 + do-not-auto-execute 规则

## Non-Claims

- 不声称已执行任何文件迁移、删除、合并。
- 冲突与复核项为 dry-run 信号（`fact_status=not_fact`）。
