## GO

- guarded dryrun 上游 GO（B0–B7 全 `simulated_pass`）
- 8 个输入 root 与 dry-run 必读 artifacts 齐全
- 10 gate 序列 post-review 通过；8 类 candidate 仍为 candidate-only
- 31 测试绑定、0 执行；8 rollback checkpoint、未执行 rollback
- protected / 240 HR / 914 permanent block 持续排除
- HumanApproval 仅为 `requires_review` 占位（非 owner confirmed）
- `ready_for_closure=true`；`ready_for_real_migration=false`
- verifier `passed == true`，`check_count >= 300`

## NO-GO

- 任一批次非 `simulated_pass` 或存在 `simulated_blocked`
- 测试未全绑定或 `executed_test_count>0`
- `rollback_executed=true` 或 `final_owner_human_confirmed=true`
- candidate scope 被标记为可执行
- 发生文件操作、runtime、或事实层写入
- verifier 失败或 `boundary_ok=false`

## Smoke 记录

- **Output**：`_eval_out/main_project_structure_migration_guarded_post_dryrun_review_v1_smoke_v0/`
- **Checks**：377 / 300 min
- **Final**：`MAIN_PROJECT_STRUCTURE_MIGRATION_GUARDED_POST_DRYRUN_REVIEW_READY_FOR_CLOSURE`
- **Next**：`Phase-Main-Project-Structure-Migration-Guarded-Closure-v1-001`
