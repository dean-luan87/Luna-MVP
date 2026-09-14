# Luna Evaluation — Terminology Canonical Table DryRun v1

**Phase**：`Phase-Terminology-Canonical-Table-DryRun-v1-001`  
**输出**：`_eval_out/terminology_canonical_table_dryrun_v1_smoke_v0/`

## 运行

```bash
python3 tools/evaluation/governance/run_terminology_canonical_table_dryrun_v1.py
python3 tools/evaluation/governance/verify_terminology_canonical_table_dryrun_v1.py
```

## 上游依赖

- Planning GO：`terminology_canonical_table_planning_v1_smoke_v0/`
- `ready_for_terminology_canonical_table_dryrun=true`
- `terminology_planning_only=true`；`canonical_table_generated_now=false`；`terminology_enforced_now=false`
- `governance_constraints_ref=migration_governance_development_constraints_v1`

## 通过条件（摘要）

- 11 类 dry-run 对象全部生成
- 10 类 planning artifacts 完整可消费（24 术语覆盖 scope/entry/fields/verifier/forbidden）
- success claim dependency ≥12 topics；semantic registry candidate ≥6 types
- cross-artifact consistency ≥12 checks；non-claims ≥9 条
- HIGH_RISK 术语 verifier severity 至少 P0（high）
- `terminology_dryrun_only=true`；`canonical_table_generated_now=false`；`registry_written_now=false`
- final decision 指向 Post-DryRun Review

## Smoke 结果

- **verifier**: GO
- **checks**: 439/420
- **boundary_ok**: true
- **final_decision**: `TERMINOLOGY_CANONICAL_TABLE_DRYRUN_READY_FOR_POST_DRYRUN_REVIEW`
- **Downstream**: Post-DryRun Review **GO**（449/420 checks）→ Roadmap Decision

## 产物清单

| 文件 | 说明 |
|------|------|
| `terminology_canonical_table_dryrun_policy_v1.json` | 阶段总策略 |
| `terminology_planning_artifact_completeness_dryrun_v1.json` | 10 planning objects 完整性 dry-run |
| `terminology_entry_structure_dryrun_v1.json` | 24 术语 entry structure 模拟 |
| `terminology_verifier_consumption_dryrun_v1.json` | verifier 模拟消费 |
| `terminology_forbidden_interpretation_dryrun_v1.json` | forbidden interpretation 模拟检查 |
| `terminology_required_fields_dryrun_v1.json` | required fields 模拟 |
| `terminology_success_claim_dependency_dryrun_v1.json` | Route C success claim 依赖模拟 |
| `terminology_semantic_registry_candidate_dryrun_v1.json` | semantic registry candidate 模拟 |
| `terminology_cross_artifact_consistency_dryrun_v1.json` | 跨产物一致性 |
| `terminology_dryrun_non_claims_register_v1.json` | dry-run non-claims 登记 |
| `terminology_canonical_table_dryrun_readiness_decision_v1.json` | Readiness decision |
| `summary.json` / `verifier_report.json` | 汇总与 verifier 报告 |
