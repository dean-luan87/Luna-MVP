## GO

- readiness 上游 GO 且 `ready_for_migration_guarded_planning == true`
- B0–B7 批次齐全，全部 `execution_allowed_now=false`
- 10 gate 序列，`blocks_execution=true`
- 31 项 post-migration 测试绑定到批次
- protected / HR / DnAE / whitebox / dev backend / future module 均排除
- verifier `passed == true`，`check_count >= 300`

## NO-GO

- readiness 未 GO 或必选 artifact 缺失
- 批次或测试未绑定
- 声称或发生文件操作 / runtime / 修改 README 或 verdict 表
- verifier 失败
