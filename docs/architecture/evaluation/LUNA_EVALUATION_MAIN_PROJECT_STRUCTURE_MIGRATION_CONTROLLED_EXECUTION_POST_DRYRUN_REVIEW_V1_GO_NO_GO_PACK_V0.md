## GO

- DryRun 产物完整加载；12 项 post-review 全部 pass
- `armed_batch_count=0`；B0–B7 candidate-only；无执行副作用
- verifier ≥ 320；`boundary_ok=true`

## NO-GO

- DryRun 未 ready 或 `armed_batch_count>0`
- 测试/verifier/rollback rehearsal 被标记为已执行
- `evidence_pack_generated_now=true`

## Smoke

- **Checks**：331 / 320 min
- **Next**：`Phase-Main-Project-Structure-Migration-Controlled-Execution-Closure-v1-001`
