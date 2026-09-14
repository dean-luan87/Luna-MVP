# Luna — Voice Interruption Governance DryRun v1

**Phase**：`Voice-Interruption-Governance-DryRun-v1-001`  
**性质**：dry-run only；合法语音打断治理；非真实 stop/pause/resume runtime

## 覆盖

- `InterruptionIntentType`：STOP / PAUSE / REPEAT / RESUME / CLARIFY / CORRECT / EMERGENCY / NEW_TASK / CANCEL_TASK / UNKNOWN_OR_AMBIGUOUS
- speech priority P0-P5 打断规则
- speech request interruption state candidate
- freshness / repeat / resume / correction / emergency / new task/cancel task policy
- 24 个 dry-run cases（16 ownership 扩展 + 8 priority scenes）

## 主线位置

```
Safety-Task-Arbitration-Policy-v1
  → Voice-Command-Ownership-Gate-Policy-v1
  → Voice-Interruption-Governance-DryRun-v1
  → Basic-Navigation-Guidance-Loop-Stabilization-Test-v1
  → Minimal-Runtime-Integration-Trial-Definition-v1
  → Minimal-Runtime-Integration-Controlled-Shadow-Trial-v1
```

## 边界

- 不调用 ASR / 麦克风 / 录音 / 声纹 / diarization
- 不停止真实 TTS
- 不调用 Speech Gate / VOP runtime
- 不提交 task state / navigation action
- 不写 Memory / WorldModel / Fact

## 结论

真实语音打断 runtime enablement **尚未开始**。  
后续若要真实启用，先做：

- `Voice-Interruption-Runtime-Shadow-v1`
- `Speech-Gate-Interruption-Handoff-DryRun-v1`
- `VOP-TTS-Interrupt-Controlled-Enablement-v1`

## 稳定化联调状态

`Basic-Navigation-Guidance-Loop-Stabilization-Test-v1` 已完成并验证：

- ownership gate 继续拦截非 owner / 电话 / 聊天 / 媒体 / 广播普通 interruption
- `task_context` / `pending_confirmation` 在 interruption 后保留
- stale safety repeat 不作为当前事实复述
- 全链仍保持 candidate / handoff only

`Minimal-Runtime-Integration-Trial-Definition-v1` 已完成并明确：

- 后续最小 runtime trial 中，Speech Gate / VOP / TTS 仅允许 shadow 或 placeholder
- 非 owner task control、P0 safety ordinary stop、stale safety fact rewrite 都进入 abort 条件
- 当前阶段仍未执行任何真实 interruption runtime

## 实现

- `capabilities/voice/voice_interruption_governance_dryrun_v1.py`
- `tools/evaluation/voice/run_voice_interruption_governance_dryrun_v1.py`
- `tools/evaluation/voice/verify_voice_interruption_governance_dryrun_v1.py`
