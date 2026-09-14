# Luna Midplatform 1.0 — Event Bus / Working Memory / Scheduler DryRunAndReview v1

**Phase**：`Phase-Midplatform-Event-Bus-Working-Memory-Scheduler-DryRunAndReview-v1-001`  
**性质**：contract-level dry-run and review only（不启真实 Event Bus / Working Memory / Scheduler）

## 阶段定位

在底座三件套 Planning GO 基础上，对 Event Bus、Working Memory、Scheduler 合同进行 **受控 dry-run and review**：

- 事件能否按 contract 被事件化
- 事件能否进入 Working Memory
- Working Memory 能否按 TTL / state machine 管理
- Scheduler 能否按 P0–P5 正确调度
- P0 抢占、P5 丢弃、health/governance/stale/missing tag 路径
- 三件套不越权

所有 dry-run 均为 **contract-level / static simulation / candidate-only**。

## 上游输入

- `_tmp_eval_out/midplatform_event_bus_working_memory_scheduler_planning/`
- `_tmp_eval_out/midplatform_micro_os_core_component_planning/`
- `_tmp_eval_out/midplatform_micro_os_core_component_dryrun_and_review/`

## 15 个 DryRun / Review 对象

1. `upstream_contract_consumability_review_v1`
2. `event_type_registry_review_v1`
3. `event_state_machine_dryrun_v1`
4. `working_memory_state_machine_dryrun_v1`
5. `ttl_cleanup_policy_dryrun_v1`
6. `scheduler_priority_queue_dryrun_v1`
7. `preemption_and_deferral_dryrun_v1`
8. `interaction_model_dryrun_v1`
9. `health_metric_mapping_review_v1`
10. `failure_route_dryrun_review_v1`
11. `governance_boundary_review_v1`
12. `sample_flow_dryrun_v1`
13. `boundary_matrix_review_v1`
14. `issue_register_v1`
15. `dryrun_readiness_decision_v1`

## 4 条 Sample Flow DryRun

| Flow | 验证要点 |
|------|---------|
| `navigation_safety_preemption_flow` | P0 抢占、Event Bus governance → WM new → Scheduler preempt |
| `ocr_pending_confirmation_flow` | pending_confirmation → defer → confirmed |
| `health_fault_degraded_flow` | health_pending → blocked → recovery_candidate |
| `memory_recall_reuse_flow` | memory_recall → active → admission_candidate |

## 运行

```bash
cd /Users/luanlei/Desktop/Luna-Core
python3 tools/evaluation/midplatform/run_midplatform_event_bus_working_memory_scheduler_dryrun_and_review_v1.py
python3 tools/evaluation/midplatform/verify_midplatform_event_bus_working_memory_scheduler_dryrun_and_review_v1.py
```

## Final Decision

```
MIDPLATFORM_EVENT_BUS_WORKING_MEMORY_SCHEDULER_DRYRUN_AND_REVIEW_CLOSED_READY_FOR_CONTROLLED_SKELETON_IMPLEMENTATION_PLANNING
```

## Next Phase

```
Phase-Midplatform-Event-Bus-Working-Memory-Scheduler-Controlled-Skeleton-Implementation-Planning-v1-001
```
