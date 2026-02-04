# replay_validation_report.md

## Summary
- replay_input: `luna_badge_v1_2/replay/examples/case_nav_turn_001.json`
- runs_fast: 5 (sleep_ms=0)
- runs_slow: 5 (sleep_ms=5)
- runner_version: `1.4.9-P0-5.1`
- git_commit: `4464fe66141bd776a593053d8427829eb2bf09e5`
- result: PASS

## Hashes

### fast
- 1. `ae7f1ab30c4fc350be139331e8a8f73947f170bdb883104acb97bab171262326`
- 2. `ae7f1ab30c4fc350be139331e8a8f73947f170bdb883104acb97bab171262326`
- 3. `ae7f1ab30c4fc350be139331e8a8f73947f170bdb883104acb97bab171262326`
- 4. `ae7f1ab30c4fc350be139331e8a8f73947f170bdb883104acb97bab171262326`
- 5. `ae7f1ab30c4fc350be139331e8a8f73947f170bdb883104acb97bab171262326`

### slow
- 1. `ae7f1ab30c4fc350be139331e8a8f73947f170bdb883104acb97bab171262326`
- 2. `ae7f1ab30c4fc350be139331e8a8f73947f170bdb883104acb97bab171262326`
- 3. `ae7f1ab30c4fc350be139331e8a8f73947f170bdb883104acb97bab171262326`
- 4. `ae7f1ab30c4fc350be139331e8a8f73947f170bdb883104acb97bab171262326`
- 5. `ae7f1ab30c4fc350be139331e8a8f73947f170bdb883104acb97bab171262326`

## Notes
- Replay 模式下禁止纳入 wall clock / uuid / thread id 等非确定性字段。
- FailSafe 资源探测（psutil CPU/MEM）在 Replay 证明口径中视为 non-deterministic，应跳过验证。

