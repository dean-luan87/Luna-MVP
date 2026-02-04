# replay_validation_report.md

## Summary
- replay_input: `luna_badge_v1_2/replay/examples/p0_5_failsafe_then_exit_001.json`
- runs_fast: 5 (sleep_ms=0)
- runs_slow: 5 (sleep_ms=5)
- runner_version: `1.4.9-P0-5.1`
- git_commit: `46afd28e96aaad013025b5455d0c9de5d23099d9`
- fault_config: `luna_badge_v1_2/replay/faults/vision_no_return_001.json`
- result: PASS

## Hashes

### fast
- 1. `a724c73b55bf95963658c670ec07cd899d3111b7560e976ec3292f16bd922963`
- 2. `a724c73b55bf95963658c670ec07cd899d3111b7560e976ec3292f16bd922963`
- 3. `a724c73b55bf95963658c670ec07cd899d3111b7560e976ec3292f16bd922963`
- 4. `a724c73b55bf95963658c670ec07cd899d3111b7560e976ec3292f16bd922963`
- 5. `a724c73b55bf95963658c670ec07cd899d3111b7560e976ec3292f16bd922963`

### slow
- 1. `a724c73b55bf95963658c670ec07cd899d3111b7560e976ec3292f16bd922963`
- 2. `a724c73b55bf95963658c670ec07cd899d3111b7560e976ec3292f16bd922963`
- 3. `a724c73b55bf95963658c670ec07cd899d3111b7560e976ec3292f16bd922963`
- 4. `a724c73b55bf95963658c670ec07cd899d3111b7560e976ec3292f16bd922963`
- 5. `a724c73b55bf95963658c670ec07cd899d3111b7560e976ec3292f16bd922963`

## Notes
- Replay 模式下禁止纳入 wall clock / uuid / thread id 等非确定性字段。
- FailSafe 资源探测（psutil CPU/MEM）在 Replay 证明口径中视为 non-deterministic，应跳过验证。

