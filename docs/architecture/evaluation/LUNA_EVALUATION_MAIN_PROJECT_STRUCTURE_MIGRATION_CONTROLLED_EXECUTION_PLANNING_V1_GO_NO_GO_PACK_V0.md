## GO

- Execution Control Roadmap 选中 Controlled Migration Execution Planning
- 8 批次作战计划 + 7 owner gates + 10 执行窗口要求 + 31 测试顺序 + 12 verifier 顺序
- rollback rehearsal mandatory；real migration / arming / tests / verifier / rollback 全部 false
- verifier ≥ 320；`boundary_ok=true`

## NO-GO

- 上游 closure/roadmap 未 ready
- `arming_allowed_now=true` 或任何执行 flag 为 true
- `post_batch_test_count!=31`

## Smoke

- **Checks**：337 / 320 min
- **Next**：`Phase-Main-Project-Structure-Migration-Controlled-Execution-DryRun-v1-001`
