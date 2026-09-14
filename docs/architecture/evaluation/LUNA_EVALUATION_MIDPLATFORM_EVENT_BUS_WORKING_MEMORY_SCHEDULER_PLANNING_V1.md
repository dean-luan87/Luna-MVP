# Luna Evaluation — Event Bus / Working Memory / Scheduler Planning v1

**Verifier**：`verify_midplatform_event_bus_working_memory_scheduler_planning_v1.py`  
**MIN_CHECKS**：469

## 必检项

### 上游

- Architecture Planning + DryRunAndReview = GO
- Core Component Planning + DryRunAndReview = GO
- `core_component_dryrun_readiness_decision_v1.dryrun_pass = true`

### 三件套合同

- Event Bus / Working Memory / Scheduler contract 全部存在
- 各 contract required_fields 完整（15 / 17 / 16 字段）
- Working Memory ≠ Memory / WorldModel
- Scheduler 禁止 direct_task_execution / direct_runtime_call / direct_user_output

### 事件模型

- event type registry ≥ 12 类
- event state machine 13 状态 + 4 终态

### 工作记忆模型

- entry state machine 12 状态
- `no_ttl_forbidden = true`
- P0–P5 TTL 策略完整

### 调度模型

- priority queue P0–P5 完整
- preemption / deferral policy ≥ 8 条规则
- P0 抢占、P1 保护、P3/P4 延迟、P5 丢弃

### 交互与治理

- interaction model cycle ≥ 6 步、edges ≥ 4
- health metric mapping 覆盖三件套（含 queue_backlog、long_pending_task_count）
- failure route matrix ≥ 12 路由
- governance boundary L0 全局约束
- sample flow plan ≥ 4 条

### Boundary

全部 boundary flags = false：

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

### Non-claims

10 条 non-claims 完整登记

## 预期

`verifier: GO` → `MIDPLATFORM_EVENT_BUS_WORKING_MEMORY_SCHEDULER_PLANNING_READY_FOR_DRYRUN_AND_REVIEW`
