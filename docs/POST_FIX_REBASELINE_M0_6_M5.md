# Post-Fix Rebaseline M0.6 / M5（第七批修复后基线重刷）

## §1 目标
对第七批真实场景（R35~R40）在 **Targeted Fix Sprint M1.0** 收口之后，进行一次统一重刷，固化“第七批修复后的最新真实场景基线”，并验证：
- `R35~R40` 的 `blocked_without_resolution` 是否已消失
- 整包是否重新清空 triage / issue 分布

## §2 before vs after 总结
本轮 before / after：
- Before：`logs/real_scenario_pack_m06.json` + `logs/benchmark_triage_board_m06.json`
- After：`logs/real_scenario_pack_postfix_m06.json` + `logs/benchmark_triage_board_postfix_m06.json`

### 场景层
- `total_cases`: 40 -> 40
- `passed_cases`: 34 -> 40
- `quality_grade_distribution`: acceptable=34, poor=6 -> acceptable=40
- `worst_real_case_ids`: 从 `R35~R40` 主导 -> 当前全体无 issue 主导

### issue 层
- `issue_type_distribution`: none=34, blocked_without_resolution=6 -> none=40
- `blocked_without_resolution`: 6 -> 0
- 未出现新的 issue 类型

### module 层 / triage
- `top_priority_optimization_modules`: `recheck_planner` -> `—`
- `ranked_modules=[]`、`ranked_issues=[]`（triage 清空）

## §3 重点场景变化
- `R35`：blocked_without_resolution / poor / blocked=true -> issue_type=None / acceptable / blocked=false
- `R36`：blocked_without_resolution / poor / blocked=true -> issue_type=None / acceptable / blocked=false
- `R37`：blocked_without_resolution / poor / blocked=true -> issue_type=None / acceptable / blocked=false
- `R38`：blocked_without_resolution / poor / blocked=true -> issue_type=None / acceptable / blocked=false
- `R39`：blocked_without_resolution / poor / blocked=true -> issue_type=None / acceptable / blocked=false
- `R40`：blocked_without_resolution / poor / blocked=true -> issue_type=None / acceptable / blocked=false

## §4 新 triage 结果
- 当前最差场景：`R1_container_real, R2_occlusion_real`（仍为 acceptable，无 issue）
- 当前 top modules：`—`
- 当前 top issues：`—`
- triage 是否清空：是（`ranked_modules=[]`、`ranked_issues=[]`）

## §5 结论
M1.0 对第七批“意图-动作-任务错位 blocked 收口”是有效的：`blocked_without_resolution` 在整包中消失，triage 再次清空。

下一轮建议优先方向：
- 继续扩第八批真实场景，制造新的可修复 triage 压力源（而不是回到高层抽象）。

