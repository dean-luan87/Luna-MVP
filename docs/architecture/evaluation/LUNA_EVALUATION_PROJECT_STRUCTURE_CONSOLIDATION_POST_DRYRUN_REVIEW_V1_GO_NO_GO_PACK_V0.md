## GO

- 五路输入 root 全部 loaded
- 11 类 review 对象 + 三类 register 全部生成
- `total_conflict_count == 1830`；`human_review == 240`；`do_not_auto_execute == 466`
- B0–B6 batch post-review 边界断言通过
- life-system mapping preserved；rollback plan review pass
- `ready_for_real_migration/file_move/file_delete/module_merge == false`
- `plan_revision_required_conflicts_register.json` 未触发高水位（≤150）或高风险已被 dry-run 阻断
- verifier `passed=true`，`check_count >= 320`

### Closure 分支

- `final_decision == LUNA_PROJECT_STRUCTURE_CONSOLIDATION_POST_DRYRUN_REVIEW_READY_FOR_CLOSURE`
- `recommended_next_phase == Phase-Luna-Project-Structure-Consolidation-Closure-v1-001`

### Plan-Revision 分支（CONDITIONAL_GO 亦可）

- `final_decision == LUNA_PROJECT_STRUCTURE_CONSOLIDATION_POST_DRYRUN_REVIEW_REQUIRES_PLAN_REVISION`
- `recommended_next_phase == Phase-Luna-Project-Structure-Consolidation-Planning-Revision-v1-001`

## NO-GO

- 缺少 dry-run / planning / structure map 输入
- review 阶段发生或声称发生真实 consolidation / 文件移动 / 删除
- review 修改了 README / phase verdict table / 既有 phase 结果
- `ready_for_real_migration == true`（任何分支均不允许）
- verifier 失败
