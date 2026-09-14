## GO

- Post-DryRun Review 上游 GO；四阶段链条闭环
- B0–B7 全 `simulated_pass`；10 gate 通过；17+ 排除冻结
- 31 测试绑定 / 0 执行；rollback 未执行；HumanApproval 仅占位
- correction_record 已登记（rollback_executed 字段修复，无权限授予）
- `closure_allowed=true`；`real_migration_allowed=false`
- verifier `passed == true`，`check_count >= 260`

## NO-GO

- 任上游阶段未 GO 或 post-review 未 `ready_for_closure`
- 批次模拟失败、测试已执行、rollback 已执行、owner 已确认
- 排除范围未冻结或 real_migration 被允许
- verifier 失败

## Smoke 记录

- **Output**：`_eval_out/main_project_structure_migration_guarded_closure_v1_smoke_v0/`
- **Checks**：275 / 260 min
- **Final**：`MAIN_PROJECT_STRUCTURE_MIGRATION_GUARDED_CLOSED_FOR_CURRENT_MAINLINE`
- **Next**：`Phase-Main-Project-Structure-Migration-Guarded-Roadmap-Decision-v1-001`
