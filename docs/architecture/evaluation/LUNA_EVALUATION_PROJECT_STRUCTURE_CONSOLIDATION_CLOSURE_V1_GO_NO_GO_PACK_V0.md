## GO

- 六路输入 root 全部 loaded
- `completed_phase_matrix` 含 5 个 GO 阶段
- `consolidation_closure_decision_summary` 计数与 post-review 一致
- `closure_boundary_freeze` 全部 no-* 边界为 true
- `non_claims_register` ≥ 10 条
- `human_review_carryover` count=240；`permanent_carryover` count=914
- `deferred_consolidation_action_pool` ≥ 15 项且 `real_migration_started=false`
- `closure_readiness_gate.ready_for_closure=true`，blockers 为空
- 全部 no-execute / no-modify / no-runtime 边界为 false
- verifier `passed=true`，`check_count >= 260`

## NO-GO

- 缺少 post-review / dryrun / planning / structure map 输入
- `plan_revision_required > 0` 或 plan_revision register 非空
- closure 阶段发生或声称发生真实 consolidation / 文件移动 / 删除
- closure 修改了 README / phase verdict table / 既有 phase 结果
- `ready_for_real_migration == true`（任何分支均不允许）
- verifier 失败

## Final

- `final_decision == LUNA_PROJECT_STRUCTURE_CONSOLIDATION_CLOSED_FOR_CURRENT_MAINLINE`
- `recommended_next_phase == Phase-Luna-Project-Structure-Consolidation-Roadmap-Decision-v1-001`
