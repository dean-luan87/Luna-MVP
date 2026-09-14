# Luna Midplatform 1.0 — Micro-OS Core Component Planning v1

**Phase**：`Phase-Midplatform-Micro-OS-Core-Component-Planning-v1-001`  
**性质**：core component contract planning only（不启 runtime）

## 阶段定位

在 Micro-OS Architecture DryRunAndReview GO 基础上，将 L0–L8 九层架构拆解为 **12 个可治理、可验证、可消费的核心组件合同**。

本阶段回答：**核心组件怎么协作**，而非继续扩展抽象大框架。

## 12 个核心组件

| # | 组件 | 层级 |
|---|------|------|
| 1 | Midplatform Kernel | L0/L3/L6 |
| 2 | Event Bus | L3 |
| 3 | Working Memory | L3 |
| 4 | Scheduler | L5/L6 |
| 5 | Task Manager | L5 |
| 6 | Drive Manager | L5 |
| 7 | Module Adapter Layer | L2 |
| 8 | Health & Resource Manager | L1/L8 |
| 9 | Governance Gate Manager | L0 |
| 10 | WorldModel / Memory Bridge | L7 |
| 11 | Output Gate Bridge | L7 |
| 12 | Watchdog / Recovery Manager | L8 |

每个组件按 `midplatform_module_definition_template_v1` **10 段结构**定义。

## 上游输入

- `_tmp_eval_out/midplatform_micro_os_architecture_planning/`
- `_tmp_eval_out/midplatform_micro_os_architecture_dryrun_and_review/`

## 运行

```bash
cd /Users/luanlei/Desktop/Luna-Core
python3 tools/evaluation/midplatform/run_midplatform_micro_os_core_component_planning_v1.py
python3 tools/evaluation/midplatform/verify_midplatform_micro_os_core_component_planning_v1.py
```

## Final Decision

`MIDPLATFORM_MICRO_OS_CORE_COMPONENT_PLANNING_READY_FOR_DRYRUN_AND_REVIEW`

## Next Phase

`Phase-Midplatform-Micro-OS-Core-Component-DryRunAndReview-v1-001`
