# replay_validation_report.md

## Summary
- replay_input: `/Users/luanlei/Desktop/Luna-2/luna_badge_v1_2/replay/examples/case_nav_turn_001.json`
- runs_fast: 5 (sleep_ms=0)
- runs_slow: 5 (sleep_ms=5)
- runner_version: `1.4.9-P0-3.1`
- git_commit: `33dabf469af42aec4cbfea01fc30f3dec3491258`
- fault_config: `/Users/luanlei/Desktop/Luna-2/luna_badge_v1_2/replay/faults/map_timeout_001.json`
- result: PASS

## Hashes

### fast
- 1. `2c0ab90f30806bb5d88417b8ef80c77f9c0d08b6f5b6e5f71332fd5ee7379d75`
- 2. `2c0ab90f30806bb5d88417b8ef80c77f9c0d08b6f5b6e5f71332fd5ee7379d75`
- 3. `2c0ab90f30806bb5d88417b8ef80c77f9c0d08b6f5b6e5f71332fd5ee7379d75`
- 4. `2c0ab90f30806bb5d88417b8ef80c77f9c0d08b6f5b6e5f71332fd5ee7379d75`
- 5. `2c0ab90f30806bb5d88417b8ef80c77f9c0d08b6f5b6e5f71332fd5ee7379d75`

### slow
- 1. `2c0ab90f30806bb5d88417b8ef80c77f9c0d08b6f5b6e5f71332fd5ee7379d75`
- 2. `2c0ab90f30806bb5d88417b8ef80c77f9c0d08b6f5b6e5f71332fd5ee7379d75`
- 3. `2c0ab90f30806bb5d88417b8ef80c77f9c0d08b6f5b6e5f71332fd5ee7379d75`
- 4. `2c0ab90f30806bb5d88417b8ef80c77f9c0d08b6f5b6e5f71332fd5ee7379d75`
- 5. `2c0ab90f30806bb5d88417b8ef80c77f9c0d08b6f5b6e5f71332fd5ee7379d75`

## Notes
- Replay 模式下禁止纳入 wall clock / uuid / thread id 等非确定性字段。
- FailSafe 资源探测（psutil CPU/MEM）在 Replay 证明口径中视为 non-deterministic，应跳过验证。

