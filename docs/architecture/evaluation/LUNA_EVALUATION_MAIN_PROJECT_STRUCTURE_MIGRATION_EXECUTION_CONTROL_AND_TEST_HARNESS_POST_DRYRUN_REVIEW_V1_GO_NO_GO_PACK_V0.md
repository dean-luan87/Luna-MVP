## GO

- Execution Control DryRun 上游 GO；planning / guarded chain 输入 loaded
- `armed_batch_count=0`；abort / harness / verifier / rollback review 全部 pass
- `ABORT_CONDITION_CANONICAL` 修复已登记；`no_permission_granted` / `no_boundary_change`
- verifier ≥ 320；`boundary_ok=true`

## NO-GO

- DryRun 未 ready 或 armed_batch_count>0
- 测试/verifier/rollback 已执行或 canonical 映射未应用
- correction 释放任何执行权限

## Smoke

- **Checks**：320 / 320 min
- **Next**：`Phase-Main-Project-Structure-Migration-Execution-Control-and-Test-Harness-Closure-v1-001`
