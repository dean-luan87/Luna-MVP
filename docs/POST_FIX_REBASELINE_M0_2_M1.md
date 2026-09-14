# Post-Fix Rebaseline M0.2 / M1（第三批真实场景修复后基线重刷）

## §1 目标
本轮针对第三批真实场景（R11~R16）在 M0.6 定点优化后做统一重刷，验证：
- `R11/R14/R16` 的 `blocked_without_resolution` 是否在整包中消失；
- 第三批整包 issue 分布是否清空；
- triage 是否再次归零或出现新热点。

重刷命令：
- `python3 tools/real_scenario_pack.py --out logs/real_scenario_pack_postfix_m02.json`
- `python3 tools/benchmark_triage_board.py --input logs/real_scenario_pack_postfix_m02.json --out logs/benchmark_triage_board_postfix_m02.json`

Before 基线：
- `logs/real_scenario_pack_m02.json`
- `logs/benchmark_triage_board_m02.json`

## §2 Before vs After 总结

### quality 分布
- Before（M0.2）：
  - `total_cases=16`
  - `passed_cases=13`
  - `quality_grade_distribution`: `acceptable=13`, `poor=3`
- After（Post-Fix M0.2/M1）：
  - `total_cases=16`
  - `passed_cases=16`
  - `quality_grade_distribution`: `acceptable=16`

### issue 分布
- Before：`none=13`, `blocked_without_resolution=3`
- After：`none=16`（`blocked_without_resolution=0`）
- 新 issue 类型：无

### top modules
- Before：`top_priority_optimization_modules=["recheck_planner"]`
- After：`top_priority_optimization_modules=[]`

## §3 重点场景变化（R11 / R14 / R16）

### R11_occlusion_plus_competition_real
- Before：`issue_type=blocked_without_resolution`，`quality=poor`，`blocked=true`，`resolved=false`，`optimization_hint_type=resolve_blocked_state`
- After：`issue_type=null`，`quality=acceptable`，`blocked=false`，`resolved=false`，`optimization_hint_type=none`

### R14_task_chain_shift_complex_real
- Before：`issue_type=blocked_without_resolution`，`quality=poor`，`blocked=true`，`resolved=false`
- After：`issue_type=null`，`quality=acceptable`，`blocked=false`，`resolved=false`

### R16_continuity_break_recovery_real
- Before：`issue_type=blocked_without_resolution`，`quality=poor`，`blocked=true`，`resolved=false`
- After：`issue_type=null`，`quality=acceptable`，`blocked=false`，`resolved=false`

结论：M0.6 修复已在整包基线中完整体现，三案均退出问题集合。

## §4 新 triage 结果
- 当前 worst cases（低优先级排序前列）：`R1_container_real`, `R2_occlusion_real`, `R4_feedback_effective_real`
- 当前 top modules：无
- 当前 top issues：无
- triage 是否清空：是（无问题型 issue、无模块热点）

## §5 结论
- M0.6 有效：第三批核心问题 `blocked_without_resolution` 已从 3 降到 0。
- 当前第三批整包与 triage 再次清空，真实优先级暂未出现新热点。
- 下一轮建议：优先扩第四批真实场景（新压力源），而不是继续开 fix sprint 打已清空问题。
