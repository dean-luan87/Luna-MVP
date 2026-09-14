# Luna — Safety Task Arbitration Policy v1

**Phase**：`Safety-Task-Arbitration-Policy-v1-001`  
**性质**：policy only；安全 vs 任务 vs 语音统一仲裁规则

## 覆盖

- 优先级 P0–P5；抑制 / 延迟 / 打断
- Speech Gate handoff、Task commit、OCR、人工协助仲裁
- safety_active 场景模拟（非 runtime）

## 边界

- arbitration candidate ≠ 真实仲裁；不触发 TTS/VOP/Speech Gate runtime

## 下一推荐 Phase

**Voice-Command-Ownership-Gate-Policy-v1** — 已完成（见 `../voice/LUNA_VOICE_COMMAND_OWNERSHIP_GATE_POLICY_V1.md`）  
**Voice-Interruption-Governance-DryRun-v1** — 已完成  
**Basic-Navigation-Guidance-Loop-Stabilization-Test-v1** — 已完成  
**Minimal-Runtime-Integration-Trial-Definition-v1** — 已完成  
**Minimal-Runtime-Integration-Controlled-Shadow-Trial-v1**

## 主线顺序（更新）

```
Safety-Task-Arbitration-Policy-v1
  → Voice-Command-Ownership-Gate-Policy-v1
  → Voice-Interruption-Governance-DryRun-v1
  → Basic-Navigation-Guidance-Loop-Stabilization-Test-v1
  → Minimal-Runtime-Integration-Trial-Definition-v1
  → Minimal-Runtime-Integration-Controlled-Shadow-Trial-v1
```

Voice Ownership Gate 的 `safety_only_allowed` / `non_owner_risk` 须与本策略联合使用。
Interruption Governance 的 `selected_action_candidate` / `target_speech_state_candidate` / `pending_confirmation_preserved` 也须进入本策略后续运行态仲裁。
Stabilization Test 已验证：`safety_active` 下低优先级 navigation / OCR / clarification / human assistance 可被 suppress/delay，且不触发真实 runtime。
Trial Definition 已进一步定义：后续最小 runtime trial 中，本策略仅允许进入受控 / shadow 路径，不允许直接产生 task commit / map side effect。

## 实现

- `capabilities/midplatform/safety_task_arbitration_policy_v1.py`
- `tools/evaluation/midplatform/run_safety_task_arbitration_policy_v1.py`
- `tools/evaluation/midplatform/verify_safety_task_arbitration_policy_v1.py`
