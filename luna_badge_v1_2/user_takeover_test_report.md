# user_takeover_test_report.md

## Scope
- P0-5 用户可接管验证（v1.4.9）
- 复用 replay_runner / replay_gate / fault-config

## 一期声明
一期中，‘用户接管’以任务结束（idle/ended）作为唯一稳定态；
后续版本若支持‘接管后继续协作’，需重新定义安全边界与责任归属。

## Pass criteria (hard)
- takeover 后不再出现 `NAVIGATION EMIT`
- task_mode 收敛至 `idle/ended`
- takeover 后无对抗性推进（例如再次 start_task/resume_task）

## Results

### Scenario: cancel_task
- **PASS/FAIL**: PASS
- **replay**: `luna_badge_v1_2/replay/examples/p0_5_user_cancel_001.json`
- **hash**: `a0125282f69effe30050e7bcde002c19d5987063ecb71a86af78103de8b39830`
- **takeover_step**: 8
- **final_task_mode**: idle
- **gate_pass (5x fast/slow)**: True
- **events_dump**: `luna_badge_v1_2/replay/evidence/user_takeover/cancel_task__events.json`

### Scenario: failsafe_then_exit
- **PASS/FAIL**: PASS
- **replay**: `luna_badge_v1_2/replay/examples/p0_5_failsafe_then_exit_001.json`
- **fault_config**: `luna_badge_v1_2/replay/faults/vision_no_return_001.json`
- **hash**: `15b402deab3f71f93c74432713649264e7b1e75fd530db2fd183d9f0b20ba5d5`
- **takeover_step**: 4
- **final_task_mode**: ended
- **gate_pass (5x fast/slow)**: True
- **events_dump**: `luna_badge_v1_2/replay/evidence/user_takeover/failsafe_then_exit__events.json`

### Scenario: uncertainty_user_choice
- **PASS/FAIL**: PASS
- **replay**: `luna_badge_v1_2/replay/examples/p0_5_uncertainty_user_choice_001.json`
- **hash**: `26273a4f39837202f72392bc3f2b6feb6f3123f480c15194820483c345ee3c89`
- **takeover_step**: 5
- **final_task_mode**: idle
- **gate_pass (5x fast/slow)**: True
- **events_dump**: `luna_badge_v1_2/replay/evidence/user_takeover/uncertainty_user_choice__events.json`

### Scenario: reverse_instruction
- **PASS/FAIL**: PASS
- **replay**: `luna_badge_v1_2/replay/examples/p0_5_reverse_instruction_001.json`
- **hash**: `a453ae7f433f2c533576c3d1b4da2152d3fb13eb51fc32485e2c3c43efb59050`
- **takeover_step**: 5
- **final_task_mode**: idle
- **gate_pass (5x fast/slow)**: True
- **events_dump**: `luna_badge_v1_2/replay/evidence/user_takeover/reverse_instruction__events.json`

### Scenario: silence_exit
- **PASS/FAIL**: PASS
- **replay**: `luna_badge_v1_2/replay/examples/p0_5_silence_exit_001.json`
- **hash**: `3c609b881188b6aff5d52584160c94100f9052ef51a49df113e740b390171914`
- **takeover_step**: 12
- **final_task_mode**: idle
- **gate_pass (5x fast/slow)**: True
- **events_dump**: `luna_badge_v1_2/replay/evidence/user_takeover/silence_exit__events.json`

