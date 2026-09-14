## GO

- Planning 产物已加载；8 批 / 7 owner gates / 31 测试 / 12 verifier 顺序可模拟串联
- `armed_batch_count=0`；`execution_window_opened=false`；无文件操作副作用
- verifier ≥ 360；`boundary_ok=true`

## NO-GO

- Planning 未 ready 或 `armed_batch_count>0`
- 测试或 verifier 在 dry-run 中被标记为已执行
- `execution_window_opened=true`

## Smoke

- **Checks**：426 / 360 min
- **Next**：`Phase-Main-Project-Structure-Migration-Controlled-Execution-Post-DryRun-Review-v1-001`
