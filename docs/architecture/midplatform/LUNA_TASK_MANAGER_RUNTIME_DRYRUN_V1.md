# Luna — Task Manager Runtime DryRun v1

**Phase**：`Task-Manager-Runtime-DryRun-v1-001`  
**性质**：消费 MidPlatform 12 条 task state / lifecycle candidates；应用 Task Manager Contract；生成 commit / enrichment / verification / execution support / downstream candidates；**不**真实 commit

## 链路

```
MidPlatform task state / lifecycle candidate
  → state machine + transition guard + confirmation + safety + idempotency
  → task object / lifecycle event / commit decision candidates
  → Task Context Enrichment candidates
  → Task-Aware Action Scheduling（空间关系 / 信息缺口 / 观察计划 / OCR 需求 / 人工协助 / 动作安排）
  → verification / execution support context candidates
  → guidance / observation / speech downstream candidates
```

## Task-Aware Action Scheduling

中台根据**任务目标 + 当前位置 + 距离 + 路线阶段 + 信息缺口**主动判断下一步应观察什么、在哪里观察、是否需要 OCR / 用户调视角 / 人工帮助——全部为 **candidate**，经 Task Manager / MidPlatform gate，不直接执行 runtime 动作。

## 边界

- `task_manager_runtime_invoked=false`；`task_state_committed_now=false`
- enrichment **不能**覆盖 live observation；memory / GPS **不能**单独完成任务
- execution support / downstream **不能**直接触发导航 / TTS / VOP / OCR / camera
- 不写 Memory / WorldModel / SceneDelta

## 下一推荐 Phase

**Basic-Functional-Loop-Runtime-Logic-Audit-and-Correction-v1** — 已完成（见 `LUNA_BASIC_FUNCTIONAL_LOOP_RUNTIME_LOGIC_AUDIT_CORRECTION_V1.md`）  
**Task-Observation-Request-Contract-v1** — 下一契约（须在 Vision-OCR ingest 之前）  
**Vision-OCR-Evidence-Ingest-Integration-Check-v1**（备选：Basic-Navigation-Guidance-Loop-DryRun-v1）

## 实现

- `capabilities/midplatform/task_manager_runtime_dryrun_v1.py`
- `tools/evaluation/midplatform/run_task_manager_runtime_dryrun_v1.py`
- `tools/evaluation/midplatform/verify_task_manager_runtime_dryrun_v1.py`
