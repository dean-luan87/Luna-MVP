# Luna Evaluation — Permission Semantics Canonicalization Roadmap Decision v1

**Phase**：`Phase-Permission-Semantics-Canonicalization-Roadmap-Decision-v1-001`  
**输出**：`_eval_out/permission_semantics_canonicalization_roadmap_decision_v1_smoke_v0/`

## 运行

```bash
python3 tools/evaluation/governance/run_permission_semantics_canonicalization_roadmap_decision_v1.py
python3 tools/evaluation/governance/verify_permission_semantics_canonicalization_roadmap_decision_v1.py
```

## 上游依赖

- Post-DryRun Review GO：`permission_semantics_canonicalization_post_dryrun_review_v1_smoke_v0/`
- `ready_for_permission_semantics_canonicalization_roadmap_decision=true`
- `canonicalization_enforced_now=false`；`registry_written_now=false`

## 通过条件（摘要）

- 9 类 roadmap decision 对象生成
- 3 段 completed chain review 全部 GO
- Route B `selected_now=true`；Route C `deferred=true`；Route G `blocked_now=true`
- TerminologyPlanningScope ≥24 术语；SuccessClaimDependencyPlanningScope ≥12 topics
- NonReleaseMatrix 全部 pass；non-claims ≥8 条
- final decision 指向 Terminology Canonical Table Planning

## Smoke 结果

- **verifier**: GO
- **checks**: 420/420
- **boundary_ok**: true
- **selected_route**: `Route B — Terminology Canonical Table Planning`
- **final_decision**: `PERMISSION_SEMANTICS_CANONICALIZATION_ROADMAP_DECISION_READY_FOR_TERMINOLOGY_CANONICAL_TABLE_PLANNING`
- **Next**: `Phase-Terminology-Canonical-Table-DryRun-v1-001`（Planning 已完成 GO）

## 产物清单

| 文件 | 说明 |
|------|------|
| `permission_semantics_canonicalization_roadmap_decision_policy_v1.json` | 路线裁决策略 |
| `completed_permission_semantics_chain_review_v1.json` | 3 段链路汇总 |
| `permission_semantics_roadmap_route_candidate_matrix_v1.json` | Route A-G 候选矩阵 |
| `bound_dependency_status_matrix_v1.json` | Route B/C 绑定依赖状态 |
| `terminology_planning_scope_v1.json` | 24 高风险术语范围 |
| `success_claim_dependency_planning_scope_v1.json` | Route C 后续 12 topics |
| `permission_semantics_roadmap_non_release_matrix_v1.json` | 权限非释放矩阵 |
| `permission_semantics_roadmap_decision_non_claims_register_v1.json` | non-claims 登记 |
| `permission_semantics_canonicalization_roadmap_readiness_decision_v1.json` | Readiness decision |
| `summary.json` / `verifier_report.json` | 汇总与 verifier 报告 |
