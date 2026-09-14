# Luna Midplatform 1.0 — Decision Center Mount Planning v1

**Phase**：`Phase-Midplatform-Decision-Center-Mount-Planning-v1-001`  
**性质**：mount planning only（不 implementation、不 runtime、不 decision execution）

## 阶段定位

在 `midplatform_information_integration_foundation_v1` 已完成 Foundation Handoff DryRunAndReview 且 GO 的基础上，规划 Decision Center 作为 Information Integration 的第一个核心下游挂接对象。

**关键边界**：Decision Center 不是执行器，也不是输出层。它只把 `decision_context_candidate` 转成更明确的 `decision_candidate` / `decision_readiness_candidate` / `decision_block_candidate`，仍然不能执行任务、不能输出、不能写 Memory / WorldModel。

## 模块定义

| 字段 | 值 |
|------|-----|
| module_id | `decision_center` |
| layer | L7（前置裁决层） |
| 上游 | `midplatform_information_integration_foundation_v1` |
| depends_on | `midplatform_micro_os_foundation_v1` |
| runtime_status | `not_enabled` |

## 核心输入 / 输出

**消费（来自 II frozen outputs）**：decision_context_candidate、conflict/gap/attention/health/governance refs

**产出（全部为 candidate）**：decision_candidate、decision_readiness_candidate、decision_block_candidate、decision_explanation_candidate、downstream_decision_handoff_candidate

**禁止**：final action、user output、Memory/WorldModel write、model/provider invocation

## 运行

```bash
cd /Users/luanlei/Desktop/Luna-Core
python3 tools/evaluation/midplatform/run_midplatform_decision_center_mount_planning_v1.py
python3 tools/evaluation/midplatform/verify_midplatform_decision_center_mount_planning_v1.py
```

## Final Decision

```
MIDPLATFORM_DECISION_CENTER_MOUNT_PLANNING_READY_FOR_DRYRUN_AND_REVIEW
```

## Next Phase

```
Phase-Midplatform-Decision-Center-Mount-DryRunAndReview-v1-001
```
