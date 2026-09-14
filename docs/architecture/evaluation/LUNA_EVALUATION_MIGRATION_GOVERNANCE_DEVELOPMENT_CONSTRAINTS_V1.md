# Luna Evaluation — Migration Governance Development Constraints v1

**性质**：规范性引用文档（非 phase smoke）  
**治理文档**：[LUNA_MIGRATION_GOVERNANCE_DEVELOPMENT_CONSTRAINTS_AND_ANTI_INCIDENT_RULES_V1.md](../governance/LUNA_MIGRATION_GOVERNANCE_DEVELOPMENT_CONSTRAINTS_AND_ANTI_INCIDENT_RULES_V1.md)  
**Manifest**：[migration_governance_development_constraints_v1_manifest.json](../governance/migration_governance_development_constraints_v1_manifest.json)  
**Python 引用**：`capabilities/governance/migration_governance_development_constraints_v1.py`

## Verifier 必须如何使用

每个高风险 migration / governance phase 的 `verify_*` 脚本应：

1. 在 `verifier_report.json` 中写入 `governance_constraints_ref=migration_governance_development_constraints_v1`
2. 对照 manifest 中的 `verifier_rules` 与 `mandatory_non_execution_summary_fields` 做语义检查
3. 对 roadmap / review / dry-run / planning phase，调用或等价实现 `assert_non_execution_summary_frozen(summary)`
4. 若阶段类型与 `final_decision` 不一致（例如 review-only 却指向 execution）→ **NO-GO**
5. 若缺少本阶段适用的 non-claims（含 canonical snippet 语义）→ **NO-GO**

## 与 Governance Debt Register 的关系

- Roadmap Decision v1 已选中 **Route D**，下一阶段为 `Phase-Main-Project-Structure-Migration-Governance-Debt-Register-v1-001`
- 本约束清单是 Register phase 的**输入规范**，Register 产出应能映射到 manifest 中的 9 类 `governance_debt_categories`
- Register 完成前，manifest 中 `blocked_until_governance_debt_register` 所列能力不得进入真实执行链

## 非 Claims

- 约束清单存在 ≠ 所有治理债已登记完成  
- 约束清单存在 ≠ 真实授权或真实执行已开放  
