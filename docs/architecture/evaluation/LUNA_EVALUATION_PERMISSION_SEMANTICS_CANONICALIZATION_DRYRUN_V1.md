# Luna Evaluation — Permission Semantics Canonicalization DryRun v1

**Phase**：`Phase-Permission-Semantics-Canonicalization-DryRun-v1-001`  
**输出**：`_eval_out/permission_semantics_canonicalization_dryrun_v1_smoke_v0/`

## 运行

```bash
python3 tools/evaluation/governance/run_permission_semantics_canonicalization_dryrun_v1.py
python3 tools/evaluation/governance/verify_permission_semantics_canonicalization_dryrun_v1.py
```

## 上游依赖

- Planning GO：`permission_semantics_canonicalization_planning_v1_smoke_v0/`
- `ready_for_permission_semantics_canonicalization_dryrun=true`
- `canonicalization_planning_only=true`；`not_enforced_now=true`
- `governance_constraints_ref=migration_governance_development_constraints_v1`

## 通过条件（摘要）

- 12 类 dry-run 对象全部生成
- 14 类 planning artifacts 完整可消费
- 8 类 semantic registry group 可索引（`registry_written_now=false`）
- forbidden matrix ≥20 条 mapped（`enforced_now=false`）
- development norms ≥12 类 mapped（`phase_template_modified_now=false`）
- verifier checklist ≥20 项 simulated consumption（`verifier_modified_now=false`）
- non-claims rules ≥20 条 simulated generation（`generated_now=false`）
- readiness / success claim / cross-artifact consistency 检查通过
- `canonicalization_enforced_now=false`；全部非执行冻结字段为 false
- final decision 指向 Post-DryRun Review

## Smoke 结果

- **verifier**: GO
- **checks**: 420/420
- **boundary_ok**: true
- **final_decision**: `PERMISSION_SEMANTICS_CANONICALIZATION_DRYRUN_READY_FOR_POST_DRYRUN_REVIEW`
- **Next**: `Phase-Permission-Semantics-Canonicalization-Roadmap-Decision-v1-001`（Post-DryRun Review 已完成 GO）

## 产物清单

| 文件 | 说明 |
|------|------|
| `permission_semantics_canonicalization_dryrun_policy_v1.json` | 阶段总策略 |
| `semantics_artifact_completeness_dryrun_v1.json` | 14 planning artifacts 完整性 dry-run |
| `semantic_registry_dryrun_index_v1.json` | 8 registry group 模拟索引 |
| `forbidden_combination_verifier_mapping_dryrun_v1.json` | forbidden → verifier check 映射 |
| `development_norms_phase_template_mapping_dryrun_v1.json` | norms → future template 映射 |
| `verifier_checklist_consumption_dryrun_v1.json` | verifier checklist 模拟消费 |
| `non_claims_generation_dryrun_v1.json` | non-claims 模拟生成 |
| `readiness_decision_semantic_validation_dryrun_v1.json` | readiness 语义验证 |
| `success_claim_semantic_gate_dryrun_v1.json` | success claim gate 模拟 |
| `cross_artifact_consistency_dryrun_v1.json` | 跨产物一致性检查 |
| `semantics_dryrun_non_claims_register_v1.json` | dry-run non-claims 登记 |
| `permission_semantics_canonicalization_dryrun_readiness_decision_v1.json` | Readiness decision |
| `summary.json` / `verifier_report.json` | 汇总与 verifier 报告 |
