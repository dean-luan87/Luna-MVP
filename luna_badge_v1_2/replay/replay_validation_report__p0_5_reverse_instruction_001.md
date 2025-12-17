# replay_validation_report.md

## Summary
- replay_input: `luna_badge_v1_2/replay/examples/p0_5_reverse_instruction_001.json`
- runs_fast: 5 (sleep_ms=0)
- runs_slow: 5 (sleep_ms=5)
- runner_version: `1.4.9-P0-5.1`
- git_commit: `46afd28e96aaad013025b5455d0c9de5d23099d9`
- result: PASS

## Hashes

### fast
- 1. `a453ae7f433f2c533576c3d1b4da2152d3fb13eb51fc32485e2c3c43efb59050`
- 2. `a453ae7f433f2c533576c3d1b4da2152d3fb13eb51fc32485e2c3c43efb59050`
- 3. `a453ae7f433f2c533576c3d1b4da2152d3fb13eb51fc32485e2c3c43efb59050`
- 4. `a453ae7f433f2c533576c3d1b4da2152d3fb13eb51fc32485e2c3c43efb59050`
- 5. `a453ae7f433f2c533576c3d1b4da2152d3fb13eb51fc32485e2c3c43efb59050`

### slow
- 1. `a453ae7f433f2c533576c3d1b4da2152d3fb13eb51fc32485e2c3c43efb59050`
- 2. `a453ae7f433f2c533576c3d1b4da2152d3fb13eb51fc32485e2c3c43efb59050`
- 3. `a453ae7f433f2c533576c3d1b4da2152d3fb13eb51fc32485e2c3c43efb59050`
- 4. `a453ae7f433f2c533576c3d1b4da2152d3fb13eb51fc32485e2c3c43efb59050`
- 5. `a453ae7f433f2c533576c3d1b4da2152d3fb13eb51fc32485e2c3c43efb59050`

## Notes
- Replay 模式下禁止纳入 wall clock / uuid / thread id 等非确定性字段。
- FailSafe 资源探测（psutil CPU/MEM）在 Replay 证明口径中视为 non-deterministic，应跳过验证。

