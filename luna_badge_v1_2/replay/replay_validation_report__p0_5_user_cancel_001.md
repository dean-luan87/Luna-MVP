# replay_validation_report.md

## Summary
- replay_input: `luna_badge_v1_2/replay/examples/p0_5_user_cancel_001.json`
- runs_fast: 5 (sleep_ms=0)
- runs_slow: 5 (sleep_ms=5)
- runner_version: `1.4.9-P0-5.1`
- git_commit: `46afd28e96aaad013025b5455d0c9de5d23099d9`
- result: PASS

## Hashes

### fast
- 1. `a0125282f69effe30050e7bcde002c19d5987063ecb71a86af78103de8b39830`
- 2. `a0125282f69effe30050e7bcde002c19d5987063ecb71a86af78103de8b39830`
- 3. `a0125282f69effe30050e7bcde002c19d5987063ecb71a86af78103de8b39830`
- 4. `a0125282f69effe30050e7bcde002c19d5987063ecb71a86af78103de8b39830`
- 5. `a0125282f69effe30050e7bcde002c19d5987063ecb71a86af78103de8b39830`

### slow
- 1. `a0125282f69effe30050e7bcde002c19d5987063ecb71a86af78103de8b39830`
- 2. `a0125282f69effe30050e7bcde002c19d5987063ecb71a86af78103de8b39830`
- 3. `a0125282f69effe30050e7bcde002c19d5987063ecb71a86af78103de8b39830`
- 4. `a0125282f69effe30050e7bcde002c19d5987063ecb71a86af78103de8b39830`
- 5. `a0125282f69effe30050e7bcde002c19d5987063ecb71a86af78103de8b39830`

## Notes
- Replay 模式下禁止纳入 wall clock / uuid / thread id 等非确定性字段。
- FailSafe 资源探测（psutil CPU/MEM）在 Replay 证明口径中视为 non-deterministic，应跳过验证。

