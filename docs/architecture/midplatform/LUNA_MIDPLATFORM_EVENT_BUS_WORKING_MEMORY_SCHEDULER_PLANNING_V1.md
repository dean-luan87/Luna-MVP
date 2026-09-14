# Luna Midplatform 1.0 — Event Bus / Working Memory / Scheduler Planning v1

**Phase**：`Phase-Midplatform-Event-Bus-Working-Memory-Scheduler-Planning-v1-001`  
**性质**：foundation triad planning only（不启真实 Event Bus / Working Memory / Scheduler）

## 阶段定位

在 Micro-OS Architecture 与 12 Core Component Contract 均已 DryRun GO 的基础上，正式拆分规划 **Micro-OS 运行底座三件套**：

| 组件 | 回答的问题 |
|------|-----------|
| **Event Bus** | 信息怎么进来、怎么流动 |
| **Working Memory** | 信息临时放哪里、怎么保鲜、怎么清理 |
| **Scheduler** | 谁先处理、谁等待、谁被抢占、谁被丢弃 |

本阶段只生成可供后续 DryRunAndReview 消费的底座合同，**不启真实 runtime**。

## 上游输入

- `_tmp_eval_out/midplatform_micro_os_architecture_planning/`
- `_tmp_eval_out/midplatform_micro_os_architecture_dryrun_and_review/`
- `_tmp_eval_out/midplatform_micro_os_core_component_planning/`
- `_tmp_eval_out/midplatform_micro_os_core_component_dryrun_and_review/`

## 16 个核心规划对象

1. `event_bus_contract_v1`
2. `event_type_registry_v1`（12 类事件）
3. `event_state_machine_v1`（13 状态）
4. `working_memory_contract_v1`
5. `working_memory_entry_state_machine_v1`（12 状态）
6. `working_memory_ttl_and_cleanup_policy_v1`（`no_ttl_forbidden=true`）
7. `scheduler_contract_v1`
8. `priority_queue_policy_v1`（P0–P5）
9. `preemption_and_deferral_policy_v1`
10. `event_bus_working_memory_scheduler_interaction_model_v1`
11. `eb_wm_scheduler_health_metric_mapping_v1`
12. `eb_wm_scheduler_failure_route_matrix_v1`（12 路由）
13. `eb_wm_scheduler_governance_boundary_v1`
14. `eb_wm_scheduler_sample_flow_plan_v1`（4 条 sample flow）
15. `eb_wm_scheduler_boundary_matrix_v1`（全部 false）
16. `eb_wm_scheduler_planning_readiness_decision_v1`

## 三件套交互循环

```
Module Adapter → Event Bus → Working Memory
                    ↓              ↓
                Scheduler ←────────┘
                    ↓
    Task Manager / Integration / Output Bridge / Watchdog
```

## 4 条 Sample Flow

| Flow | 优先级 | 要点 |
|------|--------|------|
| `navigation_safety_preemption_flow` | P0 | P0 抢占，governance → WM new → scheduler preempt |
| `ocr_pending_confirmation_flow` | P2 | pending_confirmation → defer → confirmed |
| `health_fault_degraded_flow` | P0 | health_pending → blocked → degraded/recovery |
| `memory_recall_reuse_flow` | P4 | memory_recall → active → admission_candidate |

## 运行

```bash
cd /Users/luanlei/Desktop/Luna-Core
python3 tools/evaluation/midplatform/run_midplatform_event_bus_working_memory_scheduler_planning_v1.py
python3 tools/evaluation/midplatform/verify_midplatform_event_bus_working_memory_scheduler_planning_v1.py
```

## Final Decision

```
MIDPLATFORM_EVENT_BUS_WORKING_MEMORY_SCHEDULER_PLANNING_READY_FOR_DRYRUN_AND_REVIEW
```

## Next Phase

```
Phase-Midplatform-Event-Bus-Working-Memory-Scheduler-DryRunAndReview-v1-001
```
