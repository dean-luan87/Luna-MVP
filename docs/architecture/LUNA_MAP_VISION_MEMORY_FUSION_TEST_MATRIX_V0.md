# Phase-Fusion-001 — Map × Vision × Memory Fusion Test Matrix v0（测试矩阵冻结）

**目的**：把地图约束、视角锚点、记忆调用、冲突处理、重复任务优化测试矩阵化。  
**注意**：所有输出为 fusion_decision_candidate（candidate-only），`allows_execute_now=false`。  

---

## 测试场景（A–M）

| 场景 | map | vision | memory | 预期 conflict_type | 预期 selected_basis | 预期要点 |
|---|---|---|---|---|---|---|
| A map_macro_route_available_case | 可用 | 任意 | 任意 | none/可忽略 | map_macro_constraint/vision_anchor | 输出 map_constraint_signal；不压过本地风险 |
| B vision_local_anchor_clear_case | 任意 | clear+可通行 | 任意 | none | vision_anchor | vision_anchor_signal 输出 passability_anchor |
| C memory_repeated_route_match_case | 任意 | 任意 | 匹配历史 | none | memory_optimizer（仅优化） | memory_route_signal 输出 match_score |
| D map_vision_consistent_case | 一致 | 一致 | 任意 | none | 视角或地图 | continue/方向候选；no execute leakage |
| E map_vs_vision_conflict_risk_case | continue | vision高风险 | 任意 | map_vs_vision | vision_anchor/conservative_degraded | 视角风险优先；不继续推进 |
| F memory_vs_vision_conflict_blocked_case | 任意 | blocked | memory可通行 | memory_vs_vision | vision_anchor | 以视角为准；记忆不覆盖 |
| G stale_memory_case | 任意 | 任意 | stale | none | vision_anchor/map_macro_constraint | memory_limitation_reason 输出；拒绝作为主依据 |
| H low_map_confidence_case | low | 任意 | 任意 | none | vision_anchor/memory_optimizer | 地图低置信不崩溃 |
| I low_vision_confidence_case | 任意 | low | 任意 | none/多源 | conservative_degraded/need_human_help | 低置信度降级 |
| J repeated_task_optimization_case | 任意 | 任意 | match | none | memory_optimizer | memory_used=true 但 allows_execute_now=false |
| K new_information_vs_memory_case | 任意 | 新信息与记忆不同 | match | memory_vs_vision | vision_anchor | new_information reason code |
| L fusion_no_execute_leakage_case | 任意 | 任意 | 任意 | 任意 | 任意 | 所有输出 allows_execute_now=false |
| M multi_source_conflict_case | conflict | conflict | conflict | multi_source_conflict | conservative_degraded/need_human_help | 多源冲突保守处理 |

