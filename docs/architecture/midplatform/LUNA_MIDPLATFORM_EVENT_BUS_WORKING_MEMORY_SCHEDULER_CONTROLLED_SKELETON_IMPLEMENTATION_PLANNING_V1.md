# Luna Midplatform 1.0 — Controlled Skeleton Implementation Planning v1

**Phase**：`Phase-Midplatform-Event-Bus-Working-Memory-Scheduler-Controlled-Skeleton-Implementation-Planning-v1-001`  
**性质**：controlled skeleton implementation planning only（不创建实现文件、不启 runtime）

## 阶段定位

在底座三件套 DryRunAndReview GO 基础上，规划 **最小骨架实现** 的边界、文件位置、接口、stub、测试方式与禁止项。

本阶段回答：**可以实现什么骨架**，以及 **现在仍然不能启什么**。

允许规划：dataclass / enum / pure function / in-memory stub / static validator  
禁止：真实 Event Bus loop、Working Memory runtime、Scheduler worker、多线程、异步队列、provider、模型、任务链、Memory/WorldModel 写入、用户输出

## 上游输入

- `_tmp_eval_out/midplatform_event_bus_working_memory_scheduler_planning/`
- `_tmp_eval_out/midplatform_event_bus_working_memory_scheduler_dryrun_and_review/`

## 14 个规划对象

1. `controlled_skeleton_scope_v1`
2. `controlled_skeleton_file_plan_v1`（5 文件，**本阶段不创建**）
3. `controlled_skeleton_type_contract_v1`
4. `event_bus_skeleton_contract_v1`
5. `working_memory_skeleton_contract_v1`
6. `scheduler_skeleton_contract_v1`
7. `controlled_skeleton_interaction_plan_v1`
8. `controlled_skeleton_governance_guard_v1`
9. `controlled_skeleton_health_guard_v1`
10. `controlled_skeleton_sample_plan_v1`（5 条 sample）
11. `controlled_skeleton_test_plan_v1`
12. `controlled_skeleton_boundary_matrix_v1`
13. `controlled_skeleton_non_claims_v1`
14. `controlled_skeleton_planning_readiness_decision_v1`

## 建议骨架文件（仅规划）

| 文件 | 用途 |
|------|------|
| `capabilities/midplatform/core/micro_os_common_types_v1.py` | 共享类型 |
| `capabilities/midplatform/core/event_bus_skeleton_v1.py` | Event Bus skeleton |
| `capabilities/midplatform/core/working_memory_skeleton_v1.py` | Working Memory skeleton |
| `capabilities/midplatform/core/scheduler_skeleton_v1.py` | Scheduler skeleton |
| `capabilities/midplatform/core/micro_os_static_validators_v1.py` | 静态校验 |

## Skeleton Interaction

```
Event → normalize/validate → WM entry candidate → TTL candidate
     → scheduling request → scheduling decision candidate
     （candidate only，不执行真实分发）
```

## 运行

```bash
cd /Users/luanlei/Desktop/Luna-Core
python3 tools/evaluation/midplatform/run_midplatform_event_bus_working_memory_scheduler_controlled_skeleton_implementation_planning_v1.py
python3 tools/evaluation/midplatform/verify_midplatform_event_bus_working_memory_scheduler_controlled_skeleton_implementation_planning_v1.py
```

## Final Decision

```
MIDPLATFORM_EVENT_BUS_WORKING_MEMORY_SCHEDULER_CONTROLLED_SKELETON_IMPLEMENTATION_PLANNING_READY_FOR_IMPLEMENTATION_DRYRUN
```

## Next Phase

```
Phase-Midplatform-Event-Bus-Working-Memory-Scheduler-Controlled-Skeleton-Implementation-DryRun-v1-001
```
