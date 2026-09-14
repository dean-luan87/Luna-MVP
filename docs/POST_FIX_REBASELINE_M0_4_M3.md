# Post-Fix Rebaseline M0.4 / M3（第五批修复后基线重刷）

## §1 目标
在 M0.8 行为级 `recheck_planner` blocked 收敛定点优化之后，重刷第五批真实场景整包（R23~R28），固化修复后的最新基线，并验证：
- `R23 / R24 / R25` 的 `blocked_without_resolution` 是否在整包中消失
- 第五批场景当前是否还存在有效 issue 分布
- triage 是否已再次清空

本轮重刷：
- `logs/real_scenario_pack_m04.json`（Before）
- `logs/real_scenario_pack_postfix_m04.json`（After）
- `logs/benchmark_triage_board_m04.json`（Before）
- `logs/benchmark_triage_board_postfix_m04.json`（After）

## §2 before vs after 总结

### 场景层
- Before：`total_cases=28`，`passed_cases=22`
- After：`total_cases=28`，`passed_cases=28`
- `quality_grade_distribution`：
  - Before：`acceptable=22`, `poor=6`
  - After：`acceptable=28`

### issue 层
- `issue_type_distribution`：
  - Before：`none=22`, `blocked_without_resolution=6`
  - After：`none=28`

### module 层 / triage
- Before：热点模块 `recheck_planner`，top issues `blocked_without_resolution`
- After：`ranked_modules=[]`，`ranked_issues=[]`（triage 清空）

## §3 重点场景变化（R23 / R24 / R25）

- `R23_long_chain_recovery_fail_real`
  - Before：`issue_type=blocked_without_resolution`，`quality=poor`，`blocked=true`，`resolved=false`
  - After：`issue_type=null`，`quality=acceptable`，`blocked=false`，`resolved=false`

- `R24_explicit_user_noncompliance_real`
  - Before：`issue_type=blocked_without_resolution`，`quality=poor`，`blocked=true`，`resolved=false`
  - After：`issue_type=null`，`quality=acceptable`，`blocked=false`，`resolved=false`

- `R25_task_loss_after_insertion_real`
  - Before：`issue_type=blocked_without_resolution`，`quality=poor`，`blocked=true`，`resolved=false`
  - After：`issue_type=null`，`quality=acceptable`，`blocked=false`，`resolved=false`

## §4 新 triage 结果
- 当前最差场景：无（After 为整包 `issue_type=null`）
- 当前 top modules：无（`ranked_modules=[]`）
- 当前 top issues：无（`ranked_issues=[]`）
- triage 是否清空：是

## §5 结论
- M0.8 的行为级 blocked 收敛在第五批整包基线中得到固化：`blocked_without_resolution` 从整包中消失。
- 下一轮建议优先方向：
  - 可以进入“第六批真实场景扩充”，以继续制造新的有效 triage 压力源。
  - 若你更偏向高层主线推进，也可先回到主线推进，但这会减少可观测的 triage 靶子信息。

