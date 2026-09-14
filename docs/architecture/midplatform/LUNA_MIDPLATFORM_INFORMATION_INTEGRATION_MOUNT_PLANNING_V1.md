# Luna Midplatform 1.0 — Information Integration Mount Planning v1

**Phase**：`Phase-Midplatform-Information-Integration-Mount-Planning-v1-001`  
**性质**：mount planning only（不启 runtime、不 direct mount、不调用 model/provider）

## 阶段定位

在 `midplatform_micro_os_foundation_v1` 已完成 Foundation Freeze and Handoff DryRunAndReview 且 verifier=GO 的基础上，规划 **Information Integration（L6）** 作为 Micro-OS 第一个下游挂接对象的 mount contract。

本阶段定义 Information Integration 如何消费冻结接口中的 Event、WorkingMemoryEntry、SchedulingDecisionCandidate、static validators，并输出 integration / allocation / decision context 候选。

**Mount Planning ≠ Implementation ≠ Runtime Enablement**

## 上游输入

| 来源 | 目录 |
|------|------|
| Foundation Freeze DryRunAndReview | `_tmp_eval_out/midplatform_micro_os_foundation_freeze_and_handoff_dryrun_and_review/` |
| Foundation Freeze Planning | `_tmp_eval_out/midplatform_micro_os_foundation_freeze_and_handoff_planning/` |
| Skeleton Post-DryRun Review | `_tmp_eval_out/midplatform_event_bus_working_memory_scheduler_controlled_skeleton_implementation_post_dryrun_review/` |

## 必须消费的冻结接口

**Types**：Event, EventType, EventState, WorkingMemoryEntry, WorkingMemoryEntryState, PriorityClass, SchedulingRequest, SchedulingDecisionCandidate

**Functions**：normalize_event, validate_event_schema, create_working_memory_entry, validate_wm_entry, assign_priority_candidate, produce_scheduling_decision_candidate, validate_no_runtime_flags, validate_candidate_not_fact, validate_required_trace, validate_required_health_tag, validate_required_ttl, validate_governance_guard

## 16 个核心规划对象

1. `information_integration_mount_scope_v1` — 挂接范围与 L6 定位
2. `information_integration_mount_contract_v1` — 10 段挂接合同
3. `information_integration_input_contract_v1` — 输入合同
4. `information_integration_output_contract_v1` — 输出合同（全部 candidate）
5. `information_integration_processing_model_v1` — 处理逻辑规划
6. `information_integration_model_rule_algorithm_placement_v1` — 模型/规则/算法摆放
7. `information_integration_governance_boundary_v1` — 治理边界
8. `information_integration_health_boundary_v1` — 健康边界
9. `information_integration_worldmodel_memory_feedback_boundary_v1` — WM/Memory recall 边界
10. `information_integration_downstream_handoff_matrix_v1` — 下游 handoff 矩阵
11. `information_integration_sample_flow_plan_v1` — 5 条 sample flow
12. `information_integration_failure_route_matrix_v1` — 12+ failure route
13. `information_integration_mount_health_metric_scope_v1` — 健康指标范围
14. `information_integration_boundary_matrix_v1` — 边界矩阵（全 false）
15. `information_integration_mount_non_claims_v1` — 非声明
16. `information_integration_mount_readiness_decision_v1` — 就绪裁决

## 输出候选（全部 candidate）

live_world_state_candidate, task_world_slice_candidate, priority_attention_map_candidate, information_allocation_candidate, conflict_candidate, gap_candidate, required_observation_candidate, decision_context_candidate, downstream_handoff_candidate（及 later 类 admission / guidance candidate）

## 运行

```bash
cd /Users/luanlei/Desktop/Luna-Core
python3 tools/evaluation/midplatform/run_midplatform_information_integration_mount_planning_v1.py
python3 tools/evaluation/midplatform/verify_midplatform_information_integration_mount_planning_v1.py
```

## Final Decision

```
MIDPLATFORM_INFORMATION_INTEGRATION_MOUNT_PLANNING_READY_FOR_DRYRUN_AND_REVIEW
```

## Next Phase

```
Phase-Midplatform-Information-Integration-Mount-DryRunAndReview-v1-001
```
