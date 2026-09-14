# Luna Midplatform 1.0 — Information Integration Controlled Skeleton Implementation Planning v1

**Phase**：`Phase-Midplatform-Information-Integration-Controlled-Skeleton-Implementation-Planning-v1-001`  
**性质**：controlled skeleton implementation planning only（只规划，不创建 skeleton 文件）

## 阶段定位

在 Information Integration Mount DryRunAndReview GO 基础上，规划 Information Integration 最小代码骨架：类型、纯函数、静态校验、candidate generator、sample dry-run 方案。

复用已冻结的 `midplatform_micro_os_foundation_v1`，不重新定义底座。

**Skeleton Planning ≠ Implementation Execution**

## 规划 Skeleton 文件（本阶段不创建）

| 文件 | 职责 |
|------|------|
| `information_integration_types_v1.py` | 8 类 core candidate dataclass |
| `information_integration_skeleton_v1.py` | 10 个纯函数 candidate generator |
| `information_integration_static_validators_v1.py` | 9 个静态 validator |

`information_integration_files_created_now=false`

## 8 类 Candidate 类型

LiveWorldStateCandidate, TaskWorldSliceCandidate, PriorityAttentionMapCandidate, InformationAllocationCandidate, ConflictCandidate, GapCandidate, RequiredObservationCandidate, DecisionContextCandidate

全部 `fact_status=not_fact`

## 10 个纯函数

collect_eligible_entries → group_entries_by_spatiotemporal_slot → build_live_world_state_candidate → extract_task_world_slice_candidate → build_priority_attention_map_candidate → detect_conflict_candidate → detect_gap_candidate → allocate_information_candidate → build_decision_context_candidate → validate_information_integration_candidate

## 运行

```bash
cd /Users/luanlei/Desktop/Luna-Core
python3 tools/evaluation/midplatform/run_midplatform_information_integration_controlled_skeleton_implementation_planning_v1.py
python3 tools/evaluation/midplatform/verify_midplatform_information_integration_controlled_skeleton_implementation_planning_v1.py
```

## Final Decision

```
MIDPLATFORM_INFORMATION_INTEGRATION_CONTROLLED_SKELETON_IMPLEMENTATION_PLANNING_READY_FOR_IMPLEMENTATION_DRYRUN
```

## Next Phase

```
Phase-Midplatform-Information-Integration-Controlled-Skeleton-Implementation-DryRun-v1-001
```
