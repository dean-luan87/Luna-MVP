# Luna Evaluation — Permission Semantics Canonicalization Post-DryRun Review v1

**Phase**：`Phase-Permission-Semantics-Canonicalization-Post-DryRun-Review-v1-001`  
**输出**：`_eval_out/permission_semantics_canonicalization_post_dryrun_review_v1_smoke_v0/`

## 运行

```bash
python3 tools/evaluation/governance/run_permission_semantics_canonicalization_post_dryrun_review_v1.py
python3 tools/evaluation/governance/verify_permission_semantics_canonicalization_post_dryrun_review_v1.py
```

## 上游依赖

- DryRun GO：`permission_semantics_canonicalization_dryrun_v1_smoke_v0/`
- `ready_for_permission_semantics_canonicalization_post_dryrun_review=true`
- `canonicalization_dryrun_only=true`；`simulated=true`；`canonicalization_enforced_now=false`
- `governance_constraints_ref=migration_governance_development_constraints_v1`

## 通过条件（摘要）

- 11 类 review 对象全部生成
- 12 类 dry-run 对象完整审查
- 8 registry groups 未写入；≥20 forbidden 未 enforce；≥12 norms 未改 template
- ≥20 verifier checklist 未改 verifier；≥20 non-claims 未写入模板
- cross-artifact consistency 通过；non-enforcement matrix 无 violation
- `registry_written_now=false`；`non_claims_generated_now=false`
- final decision 指向 Roadmap Decision

## Smoke 结果

- **verifier**: GO
- **checks**: 422/420
- **boundary_ok**: true
- **final_decision**: `PERMISSION_SEMANTICS_CANONICALIZATION_POST_DRYRUN_REVIEW_READY_FOR_ROADMAP_DECISION`
- **Next**: `Phase-Terminology-Canonical-Table-Planning-v1-001`（Roadmap Decision 已完成 GO，Route B 选中）

## 产物清单

| 文件 | 说明 |
|------|------|
| `permission_semantics_canonicalization_post_dryrun_review_policy_v1.json` | 阶段总策略 |
| `semantics_dryrun_completeness_review_v1.json` | 12 dry-run 对象完整性审查 |
| `semantics_non_enforcement_review_matrix_v1.json` | 12 项 non-enforcement 审查 |
| `semantic_registry_write_review_v1.json` | registry 未写入审查（8 groups） |
| `forbidden_combination_enforcement_review_v1.json` | forbidden 未 enforce 审查 |
| `development_norms_template_modification_review_v1.json` | norms 未改 template 审查 |
| `verifier_checklist_non_modification_review_v1.json` | verifier 未修改审查 |
| `non_claims_generation_non_write_review_v1.json` | non-claims 未写入审查 |
| `semantic_dryrun_cross_artifact_review_v1.json` | 跨产物一致性审查 |
| `semantics_post_dryrun_review_non_claims_register_v1.json` | post-review non-claims |
| `permission_semantics_canonicalization_post_dryrun_review_readiness_decision_v1.json` | Readiness decision |
| `summary.json` / `verifier_report.json` | 汇总与 verifier 报告 |
