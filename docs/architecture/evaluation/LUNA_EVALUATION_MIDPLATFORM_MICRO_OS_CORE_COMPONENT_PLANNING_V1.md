# Luna Evaluation — Micro-OS Core Component Planning v1

**Verifier**：`verify_midplatform_micro_os_core_component_planning_v1.py`  
**MIN_CHECKS**：397

## 必检项

- 上游 Architecture Planning + DryRunAndReview = GO
- 12 组件全部存在
- 每组件 10 段模板完整
- upstream/downstream matrix 含 Module Adapter→Event Bus 等关键边
- 17 种 information types 覆盖
- management logic 无权责错位
- model/rule/algorithm map 无 governance/watchdog 模型越权
- 每组件 ≥3 failure routes
- 15 项 health metrics 映射到组件
- 全部 boundary false
- Working Memory ≠ Memory / WorldModel
- Governance Gate Manager 为硬边界
- Watchdog 只生成 recovery_candidate

## 预期

`verifier: GO` → `MIDPLATFORM_MICRO_OS_CORE_COMPONENT_PLANNING_READY_FOR_DRYRUN_AND_REVIEW`
