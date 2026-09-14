## GO

- guarded planning 上游 GO
- B0–B7 `all_batches_simulated_pass == true`
- 10 gate dry-run 报告齐全
- 31 测试绑定、0 执行；8+ rollback checkpoint
- protected / HR / DnAE / whitebox / dev backend / future module 持续排除
- verifier `passed == true`，`check_count >= 320`

## NO-GO

- 任一批次 gate 模拟失败或测试未绑定
- 发生文件操作或执行迁移后测试
- verifier 失败
