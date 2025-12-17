# replay_validation_report.md

## Summary
- replay_input: `luna_badge_v1_2/replay/examples/case_nav_turn_001.json`
- runs_fast: 5 (sleep_ms=0)
- runs_slow: 5 (sleep_ms=5)
- runner_version: `1.4.9-P0-2-C.2`
- git_commit: `20a6bc94b48876363cc3d1a3cae065e3368e0ef8`
- result: PASS

## Hashes

### fast
- 1. `1c33dd31f4ee9bfa1c3e5d4811191e488ac4973ec0a76f055db65183ee268ece`
- 2. `1c33dd31f4ee9bfa1c3e5d4811191e488ac4973ec0a76f055db65183ee268ece`
- 3. `1c33dd31f4ee9bfa1c3e5d4811191e488ac4973ec0a76f055db65183ee268ece`
- 4. `1c33dd31f4ee9bfa1c3e5d4811191e488ac4973ec0a76f055db65183ee268ece`
- 5. `1c33dd31f4ee9bfa1c3e5d4811191e488ac4973ec0a76f055db65183ee268ece`

### slow
- 1. `1c33dd31f4ee9bfa1c3e5d4811191e488ac4973ec0a76f055db65183ee268ece`
- 2. `1c33dd31f4ee9bfa1c3e5d4811191e488ac4973ec0a76f055db65183ee268ece`
- 3. `1c33dd31f4ee9bfa1c3e5d4811191e488ac4973ec0a76f055db65183ee268ece`
- 4. `1c33dd31f4ee9bfa1c3e5d4811191e488ac4973ec0a76f055db65183ee268ece`
- 5. `1c33dd31f4ee9bfa1c3e5d4811191e488ac4973ec0a76f055db65183ee268ece`

## Notes
- Replay 模式下禁止纳入 wall clock / uuid / thread id 等非确定性字段。
- FailSafe 资源探测（psutil CPU/MEM）在 Replay 证明口径中视为 non-deterministic，应跳过验证。

