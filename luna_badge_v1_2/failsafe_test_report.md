# failsafe_test_report.md

## Scope
- Vision 无返回 / Map 超时 / TTS 阻塞 三类故障注入验证（Replay + FaultInjector）
- 注入仅发生在 adapter 边界（--fault-config）
- 复用 replay_gate 做 5x 快/慢一致性证明

## Results

### Case: vision_no_return
- **PASS/FAIL**: PASS
- **fault_config**: `luna_badge_v1_2/replay/faults/vision_no_return_001.json`
- **failsafe_step**: 4
- **expected_level**: emergency
- **actual_level**: emergency
- **hash**: `fd13129d1a58326ba92a21cb71029aff8526b9a8cdcb84fc031d9e329c1a6846`
- **gate_pass (5x fast/slow)**: True
- **user_evidence**: True
- **taskchain_stop (no NAV EMIT after failsafe)**: True
- **events_dump**: `luna_badge_v1_2/replay/evidence/failsafe/vision_no_return__events.json`
- **validation_report**: `luna_badge_v1_2/replay/replay_validation_report__case_nav_turn_001__fault_vision_no_return_001.md`

### Case: map_timeout
- **PASS/FAIL**: PASS
- **fault_config**: `luna_badge_v1_2/replay/faults/map_timeout_001.json`
- **failsafe_step**: 10
- **expected_level**: degraded
- **actual_level**: degraded
- **hash**: `2c0ab90f30806bb5d88417b8ef80c77f9c0d08b6f5b6e5f71332fd5ee7379d75`
- **gate_pass (5x fast/slow)**: True
- **user_evidence**: True
- **taskchain_stop (no NAV EMIT after failsafe)**: True
- **events_dump**: `luna_badge_v1_2/replay/evidence/failsafe/map_timeout__events.json`
- **validation_report**: `luna_badge_v1_2/replay/replay_validation_report__case_nav_turn_001__fault_map_timeout_001.md`

### Case: tts_block
- **PASS/FAIL**: PASS
- **fault_config**: `luna_badge_v1_2/replay/faults/tts_block_001.json`
- **failsafe_step**: 0
- **expected_level**: degraded
- **actual_level**: degraded
- **hash**: `f8c801174bc30842674649781270f25de335da519a95eda9a35cc93147f6e67b`
- **gate_pass (5x fast/slow)**: True
- **user_evidence**: True
- **taskchain_stop (no NAV EMIT after failsafe)**: True
- **events_dump**: `luna_badge_v1_2/replay/evidence/failsafe/tts_block__events.json`
- **validation_report**: `luna_badge_v1_2/replay/replay_validation_report__case_nav_turn_001__fault_tts_block_001.md`

