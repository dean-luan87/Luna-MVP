# Luna — Voice Dialogue Task Control Runtime DryRun v1

**Phase**：`Voice-Dialogue-Task-Control-Runtime-DryRun-v1-001`  
**性质**：模拟 utterance → intent/command/handoff/speech/STM candidate 链路；runtime dry-run only

## 链路

```
simulated utterance → intent candidate → command candidate → policy → state trace
  → handoff candidate → speech response candidate → WAITING_FOR_TASK_MANAGER_DECISION
```

## 约束

- 不调用 ASR / LLM / TTS / VOP runtime
- 不提交 Task Manager；`task_state_changed_now=false`
- Voice 仅 candidate；中台/Task Manager 拥有真实状态变更权

## 下一推荐 Phase

**MidPlatform-Task-State-Runtime-DryRun-v1** — 已完成（见 `LUNA_MIDPLATFORM_TASK_STATE_RUNTIME_DRYRUN_V1.md`）  
**Task-Manager-Contract-v1** — 下一契约 phase

## 实现

- `capabilities/midplatform/voice_dialogue_task_control_runtime_dryrun_v1.py`
- `tools/evaluation/midplatform/run_voice_dialogue_task_control_runtime_dryrun_v1.py`
- `tools/evaluation/midplatform/verify_voice_dialogue_task_control_runtime_dryrun_v1.py`
