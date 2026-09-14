# Luna Evaluation — Main Project Structure Migration Governance Debt Register v1

**Phase**：`Phase-Main-Project-Structure-Migration-Governance-Debt-Register-v1-001`  
**输出**：`_eval_out/main_project_structure_migration_governance_debt_register_v1_smoke_v0/`

## 运行

```bash
python3 tools/evaluation/governance/run_main_project_structure_migration_governance_debt_register_v1.py
python3 tools/evaluation/governance/verify_main_project_structure_migration_governance_debt_register_v1.py
```

## 规范性引用

- [LUNA_EVALUATION_MIGRATION_GOVERNANCE_DEVELOPMENT_CONSTRAINTS_V1.md](./LUNA_EVALUATION_MIGRATION_GOVERNANCE_DEVELOPMENT_CONSTRAINTS_V1.md)
- `governance_constraints_ref=migration_governance_development_constraints_v1`

## 通过条件（摘要）

- 读取 Roadmap Decision GO；Route D 已选中；`ready_for_governance_debt_register=true`
- 11 类 register 对象齐备；9 类 debt 完整登记；`fix_executed_now=false`
- blocked rules ≥9；future phase mapping ≥9；verifier additions ≥12；terminology ≥20；automation ≥12
- 至少 4 类 debt 为 P0 或 critical/high severity
- final decision 指向 Post-Register Review；不得指向 debt fix / real auth / real execution
- Verifier ≥ 420 checks

## Smoke 结果

- **verifier**: GO
- **checks**: 483/420
- **debt_category_count**: 9
- **final_decision**: `MAIN_PROJECT_STRUCTURE_MIGRATION_GOVERNANCE_DEBT_REGISTER_READY_FOR_POST_REGISTER_REVIEW`
- **Next**: `Phase-Main-Project-Structure-Migration-Governance-Debt-Register-Post-Review-v1-001`
