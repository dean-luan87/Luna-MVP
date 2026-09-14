# Luna Evaluation — Event Bus / Working Memory / Scheduler DryRunAndReview v1

**Verifier**：`verify_midplatform_event_bus_working_memory_scheduler_dryrun_and_review_v1.py`  
**MIN_CHECKS**：579

## 必检项

### 上游

- Planning verifier = GO
- 16 个 planning 对象全部被消费

### DryRun 覆盖

- event type registry ≥ 12 类
- event state machine 覆盖 completed / expired / discarded / blocked 终态
- working memory state machine 12 状态完整
- Working Memory ≠ Memory / WorldModel，不写 fact
- `no_ttl_forbidden=true`，ttl_missing → blocked/invalid
- P0–P5 队列 + P0 抢占 + P1 保护 + P5 丢弃
- preemption scenarios ≥ 6
- interaction model 不越权（EB 无语义裁决、Sched 不直接执行）
- health metric mapping 12 指标覆盖三件套
- failure routes 12 类，含 detection_signal / impact / default_response / recovery_candidate / forbidden_shortcut
- governance boundary L0 约束
- sample flow 4 条完整
- boundary matrix 全部 false
- `blocker_count=0`

### Boundary（全部 false）

- `real_event_bus_enabled_now`
- `real_working_memory_enabled_now`
- `real_scheduler_enabled_now`
- `runtime_enabled_now`
- `model_invoked_now`
- `provider_invoked_now`
- `task_execution_now`
- `memory_write_allowed_now`
- `worldmodel_write_allowed_now`
- `user_output_allowed_now`
- `real_health_monitoring_enabled_now`
- `recovery_executed_now`
- `module_runtime_modified_now`

## 预期

`verifier: GO` → `MIDPLATFORM_EVENT_BUS_WORKING_MEMORY_SCHEDULER_DRYRUN_AND_REVIEW_CLOSED_READY_FOR_CONTROLLED_SKELETON_IMPLEMENTATION_PLANNING`
