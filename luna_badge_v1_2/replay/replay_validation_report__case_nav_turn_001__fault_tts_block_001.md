# replay_validation_report.md

## Summary
- replay_input: `/Users/luanlei/Desktop/Luna-2/luna_badge_v1_2/replay/examples/case_nav_turn_001.json`
- runs_fast: 5 (sleep_ms=0)
- runs_slow: 5 (sleep_ms=5)
- runner_version: `1.4.9-P0-3.1`
- git_commit: `33dabf469af42aec4cbfea01fc30f3dec3491258`
- fault_config: `/Users/luanlei/Desktop/Luna-2/luna_badge_v1_2/replay/faults/tts_block_001.json`
- result: PASS

## Hashes

### fast
- 1. `f8c801174bc30842674649781270f25de335da519a95eda9a35cc93147f6e67b`
- 2. `f8c801174bc30842674649781270f25de335da519a95eda9a35cc93147f6e67b`
- 3. `f8c801174bc30842674649781270f25de335da519a95eda9a35cc93147f6e67b`
- 4. `f8c801174bc30842674649781270f25de335da519a95eda9a35cc93147f6e67b`
- 5. `f8c801174bc30842674649781270f25de335da519a95eda9a35cc93147f6e67b`

### slow
- 1. `f8c801174bc30842674649781270f25de335da519a95eda9a35cc93147f6e67b`
- 2. `f8c801174bc30842674649781270f25de335da519a95eda9a35cc93147f6e67b`
- 3. `f8c801174bc30842674649781270f25de335da519a95eda9a35cc93147f6e67b`
- 4. `f8c801174bc30842674649781270f25de335da519a95eda9a35cc93147f6e67b`
- 5. `f8c801174bc30842674649781270f25de335da519a95eda9a35cc93147f6e67b`

## Notes
- Replay 模式下禁止纳入 wall clock / uuid / thread id 等非确定性字段。
- FailSafe 资源探测（psutil CPU/MEM）在 Replay 证明口径中视为 non-deterministic，应跳过验证。

