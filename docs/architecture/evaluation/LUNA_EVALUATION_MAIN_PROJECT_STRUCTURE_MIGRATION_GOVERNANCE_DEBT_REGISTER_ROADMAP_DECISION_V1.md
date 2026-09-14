# Luna Evaluation — Governance Debt Register Roadmap Decision v1

**Phase**：`Phase-Main-Project-Structure-Migration-Governance-Debt-Register-Roadmap-Decision-v1-001`  
**输出**：`_eval_out/main_project_structure_migration_governance_debt_register_roadmap_decision_v1_smoke_v0/`

## 运行

```bash
python3 tools/evaluation/governance/run_main_project_structure_migration_governance_debt_register_roadmap_decision_v1.py
python3 tools/evaluation/governance/verify_main_project_structure_migration_governance_debt_register_roadmap_decision_v1.py
```

## 通过条件（摘要）

- Post-Review GO；`governance_constraints_ref=migration_governance_development_constraints_v1`
- 10 类 roadmap 对象；Route A 选中；Route B/C 为 required dependency；Route I blocked
- PermissionSemanticsPlanningScope ≥6 组；FutureDevelopmentNorms ≥12；ForbiddenCombinations ≥12；OutputPlan ≥14
- `canonicalization_executed_now=false`；`debt_fix_executed_now=false`
- final decision 指向 Permission Semantics Canonicalization Planning

## Smoke 结果

- **verifier**: GO
- **checks**: 432/420
- **selected_route**: `Route A — Permission Semantics Canonicalization Planning`
- **bound_dependencies**: Route B, Route C
- **final_decision**: `MAIN_PROJECT_STRUCTURE_MIGRATION_GOVERNANCE_DEBT_REGISTER_ROADMAP_DECISION_READY_FOR_PERMISSION_SEMANTICS_CANONICALIZATION_PLANNING`
- **Next**: `Phase-Permission-Semantics-Canonicalization-DryRun-v1-001`（Planning 已完成 GO）
