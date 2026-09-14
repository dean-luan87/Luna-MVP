# Luna Evaluation — Permission Semantics Canonicalization Planning v1

**Phase**：`Phase-Permission-Semantics-Canonicalization-Planning-v1-001`  
**输出**：`_eval_out/permission_semantics_canonicalization_planning_v1_smoke_v0/`

## 运行

```bash
python3 tools/evaluation/governance/run_permission_semantics_canonicalization_planning_v1.py
python3 tools/evaluation/governance/verify_permission_semantics_canonicalization_planning_v1.py
```

## 上游依赖

- Roadmap Decision GO：`main_project_structure_migration_governance_debt_register_roadmap_decision_v1_smoke_v0/`
- `selected_route=Route A — Permission Semantics Canonicalization Planning`
- `bound_dependencies` 含 Route B / Route C
- `governance_constraints_ref=migration_governance_development_constraints_v1`

## 通过条件（摘要）

- 14 类核心对象全部生成
- 6 类语义组完整覆盖（phase / permission / authorization / execution / artifact / readiness+result+route）
- ForbiddenStateCombinationMatrix ≥20 条；DevelopmentNormsMatrix ≥12；VerifierSemanticsChecklist ≥20（`not_enforced_now=true`）；NonClaimsGenerationRules ≥20
- 语义约束：planning 不得 imply execution；dry-run 不得 imply real action；review 不得 imply authorization；roadmap 不得 imply permission release；register 不得 imply fix；GO 不得 imply success；selected route 不得 imply execution allowed
- `canonicalization_planning_only=true`；`canonicalization_executed_now=false`；全部非执行冻结字段为 false
- final decision 指向 Permission Semantics Canonicalization DryRun

## Smoke 结果

- **verifier**: GO
- **checks**: 420/420
- **boundary_ok**: true
- **source_selected_route**: Route A — Permission Semantics Canonicalization Planning
- **source_bound_dependencies**: Route B, Route C
- **final_decision**: `PERMISSION_SEMANTICS_CANONICALIZATION_PLANNING_READY_FOR_DRYRUN`
- **Next**: `Phase-Permission-Semantics-Canonicalization-Post-DryRun-Review-v1-001`（DryRun 已完成 GO）

## 产物清单

| 文件 | 说明 |
|------|------|
| `permission_semantics_canonicalization_planning_policy_v1.json` | 阶段总策略 |
| `phase_type_semantics_table_v1.json` | Phase 类型语义（14 项） |
| `permission_state_semantics_table_v1.json` | 权限状态语义（10 项） |
| `authorization_state_semantics_table_v1.json` | 授权状态语义（12 项） |
| `execution_state_semantics_table_v1.json` | 执行状态语义（12 项） |
| `artifact_state_semantics_table_v1.json` | Artifact 状态语义（12 项） |
| `readiness_state_semantics_table_v1.json` | Readiness 语义（12 项） |
| `result_state_semantics_table_v1.json` | 结果状态语义（12 项） |
| `route_state_semantics_table_v1.json` | 路线状态语义（10 项） |
| `forbidden_state_combination_matrix_v1.json` | 禁止状态组合（≥20 条） |
| `development_norms_matrix_v1.json` | 开发规范矩阵（12 类） |
| `verifier_semantics_checklist_v1.json` | Verifier 语义检查清单（20 项） |
| `non_claims_generation_rules_v1.json` | Non-claims 生成规则（≥20 场景） |
| `permission_semantics_canonicalization_planning_readiness_decision_v1.json` | Readiness decision |
| `summary.json` / `verifier_report.json` | 汇总与 verifier 报告 |
