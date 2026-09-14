# Post-Fix Rebaseline M0.3 / M2（第四批修复后基线重刷）

## §1 目标
对第四批真实场景（R17~R22）在 **Targeted Fix Sprint M0.7** 之后做统一重刷，固化“修复后的最新基线”，并验证：
- `R17 / R18 / R19` 的 `blocked_without_resolution` 是否消失
- 第四批整包是否再次清空 triage

本轮重刷命令：
- `python3 tools/real_scenario_pack.py --out logs/real_scenario_pack_postfix_m03.json`
- `python3 tools/benchmark_triage_board.py --input logs/real_scenario_pack_postfix_m03.json --out logs/benchmark_triage_board_postfix_m03.json`

## §2 before vs after 总结

### 场景层
- Before（`logs/real_scenario_pack_m03.json`）：`total_cases=22`，`passed_cases=16`，`quality_grade_distribution=acceptable=16/poor=6`，`issue_type_distribution=none=16/blocked_without_resolution=6`
- After（`logs/real_scenario_pack_postfix_m03.json`）：`total_cases=22`，`passed_cases=22`，`quality_grade_distribution=acceptable=22`，`issue_type_distribution=none=22`

### issue 层
- `blocked_without_resolution`：`6 -> 0`
- 新 issue 类型：无（仍为 all null）

### module 层 / triage
- `top_priority_optimization_modules`：`["recheck_planner"] -> []`
- `triage`：清空（`ranked_modules=[]`，`ranked_issues=[]`）

## §3 重点场景变化（R17 / R18 / R19）
- R17：`blocked_without_resolution + poor + blocked=true` -> `issue_type=null + acceptable + blocked=false`
- R18：`blocked_without_resolution + poor + blocked=true` -> `issue_type=null + acceptable + blocked=false`
- R19：`blocked_without_resolution + poor + blocked=true` -> `issue_type=null + acceptable + blocked=false`

并且整包中未观察到对既有 case 的回归（例如 R11/R14/R16 仍保持 `issue_type=null`）。

## §4 新 triage 结果
- 当前最差场景：`R1_container_real / R2_occlusion_real / R4_feedback_effective_real`（均为 `issue_type=null`，低优先级质量分层）
- 当前 top modules：无
- 当前 top issues：无
- triage 是否清空：是

## §5 结论
- M0.7 在第四批整包基线上完成“真正修复”固化：`issue_type_distribution=none×22`，triage 再次归零。
- 下一轮建议：
  - 若目标继续制造新压力源：扩第五批真实场景
  - 若目标转入更高层主线：可以回到主线推进，因为当前 benchmark-triage 不再提供明确 fix 靶子

