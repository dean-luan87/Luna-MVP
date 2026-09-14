## GO

- `migration_readiness_gate.all_go_conditions_met == true`
- `migration_allowed_scope` 全部 `candidate_only` / `execution_allowed_now=false`
- `migration_forbidden_scope` ≥ 10 类；protected / permanent block 排除迁移
- `pre_migration_checklist` ≥ 10 项；`post_migration_test_plan` 五组 A–E
- `migration_rollback_requirement.rollback_required == true`（本阶段不执行 rollback）
- `whitebox_test_center_deferment_policy` 与 roadmap 冻结策略一致
- `future_reserved_module_constraint` ≥ 14 模块，`forced_future_module_finalization_allowed=false`
- verifier `passed == true`，`check_count >= 260`

## NO-GO

- 上游 roadmap / PAHR closure / consolidation closure 未 GO
- protected asset 或 permanent block 进入迁移范围
- 缺少 post-migration test plan 或 rollback requirement 定义
- 本阶段修改 README / phase verdict / 或发生文件操作
- verifier 失败
