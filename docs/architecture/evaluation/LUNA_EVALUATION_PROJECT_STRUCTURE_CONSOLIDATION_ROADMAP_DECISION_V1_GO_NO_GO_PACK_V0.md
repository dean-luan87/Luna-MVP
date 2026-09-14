## GO

- 七路输入 root 全部 loaded
- `route_option_matrix` 含 ≥10 条路线（A–J）
- Route A `selected_now=true`；Route G blocked
- `consolidation_closed=true`；human=240；permanent=914
- 全部 deferred 寄存器 generated 且 deferred=true
- `real_migration_allowed=false`；全部 ready_for_* false
- 全部 no-execute / no-modify / no-runtime 边界为 false
- verifier `passed=true`，`check_count >= 200`

## NO-GO

- 缺少 closure / post-review 输入
- `selected_route` 不是 Protected Asset and Human Review Resolution Planning
- Route G（真实迁移）被选中
- roadmap decision 阶段发生或声称发生真实 consolidation / 文件移动 / 删除
- roadmap decision 修改了 README / phase verdict table
- verifier 失败

## Final

- `final_decision == LUNA_PROJECT_STRUCTURE_CONSOLIDATION_ROADMAP_DECISION_READY_FOR_PROTECTED_ASSET_AND_HUMAN_REVIEW_RESOLUTION_PLANNING`
- `recommended_next_phase == Phase-Protected-Asset-and-Human-Review-Resolution-Planning-v1-001`
