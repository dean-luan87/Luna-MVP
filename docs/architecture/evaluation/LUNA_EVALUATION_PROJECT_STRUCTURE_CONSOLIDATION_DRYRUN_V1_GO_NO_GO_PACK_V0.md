## GO

- B0–B6 批次 dry-run 结果齐全
- 冲突报告、依赖断裂模拟、边界审查齐全
- 人工复核清单 ≥ 1 条；禁止自动执行清单 ≥ 10 条
- 回滚模拟计划齐全
- `ready_for_post_dryrun_review=true`；`ready_for_real_migration/file_move/file_delete/module_merge=false`
- verifier `passed=true`，`check_count >= 320`

## NO-GO

- 缺少 `future_life_system_mapping`
- 发生或声称发生真实 consolidation / 文件移动 / 删除
- dry-run 修改了 README / phase verdict table / 既有 phase 结果
- verifier 失败
