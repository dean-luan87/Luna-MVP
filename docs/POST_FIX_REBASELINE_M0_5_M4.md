# Post-Fix Rebaseline M0.5 / M4（第六批修复后基线重刷）

## §1 目标
在已完成：
- `Real Scenario Pack M0.5 / M4`（R29~R34）
- `Targeted Fix Sprint M0.9`（R29~R34 的 repeated fallback / retry exhaustion 收口）

之后，对第六批场景执行一次统一重刷，固化 M0.9 后的“最新真实场景基线”，并作为下一轮决定（扩第七批 or 转更高层主线）的依据。

## §2 before vs after 总结
本轮 before / after 对照：
- Before：`logs/real_scenario_pack_m05.json` + `logs/benchmark_triage_board_m05.json`
- After：`logs/real_scenario_pack_postfix_m05.json` + `logs/benchmark_triage_board_postfix_m05.json`

### 场景层
- `total_cases`: 34 -> 34
- `passed_cases`: 28 -> 34
- `quality_grade_distribution`：`acceptable=28, poor=6` -> `acceptable=34`
- `worst_real_case_ids`: `R29/R30/R31`（before） -> `R1/R2`（after，且无 issue）

### issue 层
- `issue_type_distribution`：`none=28, blocked_without_resolution=6` -> `none=34`
- `blocked_without_resolution`：6 -> 0
- 未出现新的 issue 类型

### module 层 / triage
- `top_priority_optimization_modules`：`recheck_planner`（before） -> `—`（after）
- `ranked_modules=[]`、`ranked_issues=[]`（triage 清空）

## §3 重点场景变化（R29~R34）
六个重点 case 均体现出收口效果：
- R29 `blocked_without_resolution`：消失（blocked=false，quality 从 poor->acceptable）
- R30 `blocked_without_resolution`：消失（blocked=false，quality 从 poor->acceptable）
- R31 `blocked_without_resolution`：消失（blocked=false，quality 从 poor->acceptable）
- R32 `blocked_without_resolution`：消失（blocked=false，quality 从 poor->acceptable）
- R33 `blocked_without_resolution`：消失（blocked=false，quality 从 poor->acceptable）
- R34 `blocked_without_resolution`：消失（blocked=false，quality 从 poor->acceptable）

## §4 新 triage 结果
- 当前最差场景：`R1_container_real, R2_occlusion_real`（仍为 acceptable，无 issue）
- 当前 top modules：`—`
- 当前 top issues：`—`
- triage 是否清空：是（`ranked_modules=[]`、`ranked_issues=[]`）

## §5 结论
M0.9 对 repeated fallback / retry exhaustion 语境下的 `blocked_without_resolution` 收口是有效的：第六批整包已从“有 blocked unresolved 问题”恢复为“全 none issue 且 triage 清空”。

下一轮建议：
- 若继续制造新的 triage 靶点：优先扩第七批真实场景（从新类型/新扰动角度切入）。
- 若转更高层主线：可在本轮基线固化后进行，但会减少可观测的 triage 靶子信息。

