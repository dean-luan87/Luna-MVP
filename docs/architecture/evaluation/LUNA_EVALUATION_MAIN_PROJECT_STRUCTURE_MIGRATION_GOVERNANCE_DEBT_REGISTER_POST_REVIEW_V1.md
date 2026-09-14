# Luna Evaluation — Governance Debt Register Post-Review v1

**Phase**：`Phase-Main-Project-Structure-Migration-Governance-Debt-Register-Post-Review-v1-001`  
**输出**：`_eval_out/main_project_structure_migration_governance_debt_register_post_review_v1_smoke_v0/`

## 运行

```bash
python3 tools/evaluation/governance/run_main_project_structure_migration_governance_debt_register_post_review_v1.py
python3 tools/evaluation/governance/verify_main_project_structure_migration_governance_debt_register_post_review_v1.py
```

## 通过条件（摘要）

- Register GO；`governance_constraints_ref` 正确；`fix_executed_now=false`；automation 全部 `not_implemented_now`
- 10 类 review 对象；9 debt / 8 source phase / 9 blocked rules / 9 future phases / 12 verifier checks / 20 terminology / 9+ non-claims 全部 pass
- `debt_fix_executed_now=false`；无 automation/verifier/doc auto-sync
- final decision 指向 Register Roadmap Decision
- Verifier ≥ 420 checks

## Smoke 结果

- **verifier**: GO
- **checks**: 438/420
- **final_decision**: `MAIN_PROJECT_STRUCTURE_MIGRATION_GOVERNANCE_DEBT_REGISTER_POST_REVIEW_READY_FOR_ROADMAP_DECISION`
- **Next**: `Phase-Main-Project-Structure-Migration-Governance-Debt-Register-Roadmap-Decision-v1-001`
