# Luna — MidPlatform Task State Runtime DryRun v1

**Phase**：`MidPlatform-Task-State-Runtime-DryRun-v1-001`  
**性质**：消费 Voice Dialogue Runtime 的 12 条 handoff candidates；生成 task state / lifecycle / guidance / observation / speech / confirmation candidates；不提交 Task Manager

## 链路

```
voice handoff candidate → transition guard → task state candidate → lifecycle candidate
  → guidance need / observation / speech / confirmation candidates
```

## 边界

- MidPlatform 可评估 **task state candidate**；**Task Manager** 才提交生命周期
- `task_state_changed_now=false`；`task_manager_invoked=false`
- 不触发导航 / TTS / VOP / OCR / camera；不写 Memory / WorldModel

## 下一推荐 Phase

**Task-Manager-Contract-v1** — 已完成（见 `LUNA_TASK_MANAGER_CONTRACT_V1.md`）  
**Task-Manager-Runtime-DryRun-v1** — 已完成（见 `LUNA_TASK_MANAGER_RUNTIME_DRYRUN_V1.md`）

## 实现

- `capabilities/midplatform/midplatform_task_state_runtime_dryrun_v1.py`
- `tools/evaluation/midplatform/run_midplatform_task_state_runtime_dryrun_v1.py`
- `tools/evaluation/midplatform/verify_midplatform_task_state_runtime_dryrun_v1.py`
