# replay_validation_report.md

## Summary
- replay_input: `/Users/luanlei/Desktop/Luna-2/luna_badge_v1_2/replay/examples/case_nav_turn_001.json`
- runs_fast: 5 (sleep_ms=0)
- runs_slow: 5 (sleep_ms=5)
- runner_version: `1.4.9-P0-3.1`
- git_commit: `33dabf469af42aec4cbfea01fc30f3dec3491258`
- fault_config: `/Users/luanlei/Desktop/Luna-2/luna_badge_v1_2/replay/faults/vision_no_return_001.json`
- result: PASS

## Hashes

### fast
- 1. `fd13129d1a58326ba92a21cb71029aff8526b9a8cdcb84fc031d9e329c1a6846`
- 2. `fd13129d1a58326ba92a21cb71029aff8526b9a8cdcb84fc031d9e329c1a6846`
- 3. `fd13129d1a58326ba92a21cb71029aff8526b9a8cdcb84fc031d9e329c1a6846`
- 4. `fd13129d1a58326ba92a21cb71029aff8526b9a8cdcb84fc031d9e329c1a6846`
- 5. `fd13129d1a58326ba92a21cb71029aff8526b9a8cdcb84fc031d9e329c1a6846`

### slow
- 1. `fd13129d1a58326ba92a21cb71029aff8526b9a8cdcb84fc031d9e329c1a6846`
- 2. `fd13129d1a58326ba92a21cb71029aff8526b9a8cdcb84fc031d9e329c1a6846`
- 3. `fd13129d1a58326ba92a21cb71029aff8526b9a8cdcb84fc031d9e329c1a6846`
- 4. `fd13129d1a58326ba92a21cb71029aff8526b9a8cdcb84fc031d9e329c1a6846`
- 5. `fd13129d1a58326ba92a21cb71029aff8526b9a8cdcb84fc031d9e329c1a6846`

## Notes
- Replay 模式下禁止纳入 wall clock / uuid / thread id 等非确定性字段。
- FailSafe 资源探测（psutil CPU/MEM）在 Replay 证明口径中视为 non-deterministic，应跳过验证。

